-- AbyssalSkillsD 1.1.0: additive cloud migration. Run as project owner.
-- No existing skill/account is deleted. Legacy role fields cease granting authority.
begin;
set local statement_timeout='30s';
set local lock_timeout='5s';
create schema if not exists abyssal_private;
revoke all on schema abyssal_private from public, anon, authenticated;
create schema if not exists abyssal_backup;
revoke all on schema abyssal_backup from public, anon, authenticated;
create table if not exists abyssal_backup.profiles_20261101 as table public.profiles;
create table if not exists abyssal_backup.skills_20261101 as table public.skills;
create table if not exists abyssal_backup.references_20261101 as table public.skill_references;
create table if not exists abyssal_backup.errors_20261101 as table public.system_error_reports;
create table if not exists abyssal_backup.policies_20261101 as select * from pg_policies where schemaname='public';

alter table abyssal_backup.profiles_20261101 enable row level security;
alter table abyssal_backup.skills_20261101 enable row level security;
alter table abyssal_backup.references_20261101 enable row level security;
alter table abyssal_backup.errors_20261101 enable row level security;
alter table abyssal_backup.policies_20261101 enable row level security;

create table if not exists abyssal_private.admin_users(user_id uuid primary key references auth.users(id));
alter table abyssal_private.admin_users enable row level security;
create or replace function public.abyssal_is_admin() returns boolean
language sql stable security definer set search_path='' as $$
 select exists(select 1 from abyssal_private.admin_users where user_id=auth.uid());
$$;
revoke all on function public.abyssal_is_admin() from public, anon;
grant execute on function public.abyssal_is_admin() to authenticated;

alter table public.skills add column if not exists slug text;
update public.skills set slug=id where slug is null;
create unique index if not exists skills_author_slug on public.skills(author_id,slug);
alter table public.skills add column if not exists rules jsonb not null default '[]';
alter table public.skills add column if not exists hidden_reason text;
alter table public.skills add column if not exists removed_at timestamptz;
create table if not exists public.skill_favorites(user_id uuid references auth.users(id), skill_id text references public.skills(id), primary key(user_id,skill_id));
alter table public.skill_favorites enable row level security;
create table if not exists public.community_reports(id uuid primary key default gen_random_uuid(),skill_id text references public.skills(id),reporter_id uuid not null references auth.users(id),reason text not null,created_at timestamptz default now(),unique(skill_id,reporter_id));
alter table public.community_reports enable row level security;
create table if not exists abyssal_private.install_requests(request_id uuid primary key,skill_id text not null references public.skills(id),created_at timestamptz default now());
create table if not exists abyssal_private.diagnostic_requests(user_id uuid not null references auth.users(id),request_id uuid not null,report_id uuid not null references public.system_error_reports(id),created_at timestamptz not null default now(),primary key(user_id,request_id));
alter table abyssal_private.install_requests enable row level security;
alter table abyssal_private.diagnostic_requests enable row level security;

-- Remove legacy policies, preserving their definitions in the backup schema.
do $$ declare p record; begin
 for p in select * from pg_policies where schemaname='public' and tablename in ('profiles','skills','skill_references','system_error_reports') loop
  execute format('drop policy %I on public.%I',p.policyname,p.tablename);
 end loop;
end $$;
revoke all on public.profiles, public.skills, public.skill_references, public.system_error_reports,public.skill_favorites,public.community_reports from anon,authenticated;
grant select(id,display_name,avatar_url,bio) on public.profiles to anon,authenticated;
grant select on public.skills,public.skill_references to anon,authenticated;
create policy profile_public on public.profiles for select to anon,authenticated using(true);
create policy skill_public on public.skills for select to anon,authenticated using((is_public and removed_at is null and hidden_reason is null) or author_id=auth.uid() or public.abyssal_is_admin());
create policy reference_public on public.skill_references for select to anon,authenticated using(exists(select 1 from public.skills s where s.id=skill_id));

create or replace function public.save_my_profile(p_name text,p_bio text default '',p_avatar text default '') returns jsonb
language plpgsql security definer set search_path='' as $$
declare u uuid:=auth.uid(); result jsonb;
begin
 if u is null then raise insufficient_privilege; end if;
 if length(p_name)>120 or length(p_bio)>2000 or length(p_avatar)>2048 then raise exception 'profile too large'; end if;
 if p_avatar<>'' and p_avatar !~ '^https://' and p_avatar !~ '^assets/logo/[a-zA-Z0-9_.-]+$' then raise exception 'invalid avatar'; end if;
 insert into public.profiles(id,username,display_name,bio,avatar_url,role) values(u,'user_'||replace(u::text,'-',''),p_name,p_bio,p_avatar,'creator')
 on conflict(id) do update set display_name=excluded.display_name,bio=excluded.bio,avatar_url=excluded.avatar_url,updated_at=now();
 select jsonb_build_object('id',id,'full_name',display_name,'bio',bio,'avatar_url',avatar_url,'role',case when public.abyssal_is_admin() then 'admin' else 'creator' end) into result from public.profiles where id=u;
 return result;
end $$;

create or replace function public.get_my_cloud_profile() returns jsonb
language sql stable security definer set search_path='' as $$
 select jsonb_build_object('id',p.id,'full_name',p.display_name,'bio',p.bio,'avatar_url',p.avatar_url,'role',case when public.abyssal_is_admin() then 'admin' else 'creator' end,'contributed_count',(select count(*) from public.skills where author_id=auth.uid() and removed_at is null),'favorites_count',(select count(*) from public.skill_favorites where user_id=auth.uid())) from public.profiles p where p.id=auth.uid();
$$;

create or replace function public.publish_skill(p_skill jsonb) returns jsonb
language plpgsql security definer set search_path='' as $$
declare u uuid:=auth.uid(); sid text; item jsonb; existing public.skills; slug_value text:=p_skill->>'slug';
begin
 if u is null then raise insufficient_privilege; end if;
 if slug_value !~ '^[a-zA-Z0-9][a-zA-Z0-9_-]{0,127}$' or slug_value is null then raise exception 'invalid slug'; end if;
 if octet_length(p_skill::text)>2000000 or coalesce(length(p_skill->>'skill_content'),0)=0 or length(p_skill->>'display_title')>200 or length(p_skill->>'description')>5000 then raise exception 'invalid skill payload'; end if;
 if jsonb_typeof(coalesce(p_skill->'references','[]'))<>'array' or jsonb_typeof(coalesce(p_skill->'rules','[]'))<>'array' then raise exception 'invalid documents'; end if;
 for item in select value from jsonb_array_elements(coalesce(p_skill->'references','[]')||coalesce(p_skill->'rules','[]')) loop
  if (item->>'filename') is null or (item->>'filename') !~ '^[a-zA-Z0-9_-][a-zA-Z0-9_./ -]*$' or (item->>'filename') ~ '(^|/)\.\.(/|$)' or length(item->>'filename')>240 then raise exception 'invalid document path'; end if;
 end loop;
 if not exists(select 1 from public.profiles where id=u) then perform public.save_my_profile('Developer'); end if;
 if nullif(p_skill->>'id','') is not null then
  select * into existing from public.skills where id=p_skill->>'id' for update;
  if not found or existing.author_id<>u then raise insufficient_privilege; end if;
  if existing.hidden_reason is not null then raise exception 'content hidden by administrator'; end if;
  sid:=existing.id;
 else
  select * into existing from public.skills where author_id=u and slug=slug_value for update;
  if found then
   if existing.hidden_reason is not null then raise exception 'content hidden by administrator'; end if;
   sid:=existing.id;
  else sid:=gen_random_uuid()::text; end if;
 end if;
 insert into public.skills(id,author_id,slug,name,display_title,description,category,skill_content,version,tags,yaml_frontmatter,rules,is_public)
 values(sid,u,slug_value,slug_value,coalesce(p_skill->>'display_title',slug_value),coalesce(p_skill->>'description',''),coalesce(p_skill->>'category','Community'),p_skill->>'skill_content',coalesce(p_skill->>'version','1.0.0'),array(select jsonb_array_elements_text(coalesce(p_skill->'tags','[]'))),coalesce(p_skill->'yaml_frontmatter','{}'),coalesce(p_skill->'rules','[]'),true)
 on conflict(id) do update set name=excluded.name,slug=excluded.slug,display_title=excluded.display_title,description=excluded.description,category=excluded.category,skill_content=excluded.skill_content,version=excluded.version,tags=excluded.tags,yaml_frontmatter=excluded.yaml_frontmatter,rules=excluded.rules,is_public=true,removed_at=null,updated_at=now();
 delete from public.skill_references where skill_id=sid;
 for item in select value from jsonb_array_elements(coalesce(p_skill->'references','[]')) loop
  insert into public.skill_references(skill_id,title,filename,content,category) values(sid,coalesce(item->>'title','Reference'),item->>'filename',coalesce(item->>'content',''),coalesce(item->>'category','general'));
 end loop;
 return jsonb_build_object('id',sid,'slug',slug_value,'display_title',p_skill->>'display_title','author_id',u);
end $$;

create or replace function public.get_community_skill(p_id text) returns jsonb
language sql stable security definer set search_path='' as $$
 select to_jsonb(s)||jsonb_build_object('author_name',coalesce(p.display_name,'Community'),'references',coalesce((select jsonb_agg(jsonb_build_object('id',r.id::text,'title',r.title,'filename',r.filename,'content',r.content,'category',r.category)) from public.skill_references r where r.skill_id=s.id),'[]'::jsonb)) from public.skills s left join public.profiles p on p.id=s.author_id where s.id=p_id and ((s.is_public and s.removed_at is null and s.hidden_reason is null) or s.author_id=auth.uid() or public.abyssal_is_admin());
$$;
create or replace function public.list_community_skills(p_query text default '',p_category text default '',p_page integer default 0) returns jsonb
language sql stable security definer set search_path='' as $$
 with eligible as(select s.*,p.display_name author_name,exists(select 1 from public.skill_favorites f where f.skill_id=s.id and f.user_id=auth.uid()) is_favorite from public.skills s left join public.profiles p on p.id=s.author_id where s.is_public and s.removed_at is null and s.hidden_reason is null and (p_category='' or s.category=p_category) and (p_query='' or (s.display_title||' '||s.description||' '||array_to_string(s.tags,' ')) ilike '%'||left(p_query,200)||'%')),
 page as(select * from eligible order by created_at desc,id limit 24 offset greatest(0,least(p_page,10000))*24)
 select jsonb_build_object('skills',coalesce((select jsonb_agg(to_jsonb(page)) from page),'[]'::jsonb),'count',(select count(*) from eligible),'page',p_page,'page_size',24);
$$;
create or replace function public.set_skill_favorite(p_id text,p_enabled boolean) returns boolean
language plpgsql security definer set search_path='' as $$
begin
 if auth.uid() is null or public.get_community_skill(p_id) is null then raise insufficient_privilege; end if;
 perform pg_advisory_xact_lock(hashtextextended(p_id,0));
 if p_enabled then insert into public.skill_favorites values(auth.uid(),p_id) on conflict do nothing;
 else delete from public.skill_favorites where user_id=auth.uid() and skill_id=p_id; end if;
 update public.skills set stars_count=(select count(*) from public.skill_favorites where skill_id=p_id) where id=p_id;
 return p_enabled;
end $$;
create or replace function public.record_skill_install(p_id text,p_request uuid) returns boolean
language plpgsql security definer set search_path='' as $$
begin
 if not exists(select 1 from public.skills where id=p_id and is_public and removed_at is null and hidden_reason is null) then raise insufficient_privilege; end if;
 insert into abyssal_private.install_requests(request_id,skill_id) values(p_request,p_id) on conflict do nothing;
 if found then update public.skills set downloads_count=downloads_count+1 where id=p_id; end if;
 return true;
end $$;
create or replace function public.remove_community_skill(p_id text) returns boolean
language plpgsql security definer set search_path='' as $$
begin
 update public.skills set is_public=false,removed_at=now(),updated_at=now() where id=p_id and author_id=auth.uid();
 if not found then raise insufficient_privilege; end if;
 return true;
end $$;
create or replace function public.report_community_skill(p_id text,p_reason text) returns boolean
language plpgsql security definer set search_path='' as $$
begin
 if auth.uid() is null or length(trim(p_reason))<5 or length(p_reason)>2000 or public.get_community_skill(p_id) is null then raise insufficient_privilege; end if;
 insert into public.community_reports(skill_id,reporter_id,reason) values(p_id,auth.uid(),p_reason) on conflict(skill_id,reporter_id) do update set reason=excluded.reason;
 return true;
end $$;
create or replace function public.list_community_reports() returns jsonb
language plpgsql stable security definer set search_path='' as $$
begin
 if not public.abyssal_is_admin() then raise insufficient_privilege; end if;
 return coalesce((select jsonb_agg(to_jsonb(r)) from (select cr.id,cr.skill_id,cr.reason,cr.created_at,s.display_title,s.hidden_reason from public.community_reports cr join public.skills s on s.id=cr.skill_id order by cr.created_at desc limit 100) r),'[]'::jsonb);
end $$;
create or replace function public.moderate_community_skill(p_id text,p_reason text) returns boolean
language plpgsql security definer set search_path='' as $$
begin
 if not public.abyssal_is_admin() or length(trim(p_reason))<5 or length(p_reason)>2000 then raise insufficient_privilege; end if;
 update public.skills set hidden_reason=p_reason,is_public=false,updated_at=now() where id=p_id;
 return found;
end $$;
create or replace function public.submit_diagnostic(p_request uuid,p_payload jsonb) returns jsonb
language plpgsql security definer set search_path='' as $$
declare u uuid:=auth.uid(); rid uuid; count_value integer;
begin
 if u is null then raise insufficient_privilege; end if;
 if octet_length(p_payload::text)>64000 or length(p_payload->>'fingerprint')<>64 or p_payload->>'fingerprint' !~ '^[a-f0-9]+$' then raise exception 'invalid diagnostic'; end if;
 perform pg_advisory_xact_lock(hashtextextended(u::text,0));
 select report_id into rid from abyssal_private.diagnostic_requests where user_id=u and request_id=p_request;
 if rid is not null then return jsonb_build_object('accepted',true,'duplicate',true,'request_id',p_request); end if;
 if exists(select 1 from abyssal_private.diagnostic_requests where user_id=u and created_at>now()-interval '180 seconds') then raise sqlstate 'P0001' using message='rate limit: wait 180 seconds'; end if;
 insert into public.system_error_reports(fingerprint,error_type,error_message,module_name,app_version,os_info,sanitized_traceback)
 values(p_payload->>'fingerprint',left(coalesce(p_payload->>'error_type','Error'),120),left(coalesce(p_payload->>'error_message',''),12000),left(coalesce(p_payload->>'module_name',''),120),left(coalesce(p_payload->>'app_version','unknown'),40),'win32',left(coalesce(p_payload->>'traceback',''),12000))
 on conflict(fingerprint,app_version) do update set occurrences=public.system_error_reports.occurrences+1,last_seen_at=now()
 returning id,occurrences into rid,count_value;
 insert into abyssal_private.diagnostic_requests values(u,p_request,rid,now());
 return jsonb_build_object('accepted',true,'duplicate',false,'request_id',p_request,'occurrences',count_value);
end $$;

-- Explicit execute grants; SECURITY DEFINER functions do not inherit open PUBLIC execution.
do $$ declare f record; begin
 for f in select p.oid::regprocedure signature,p.proname name from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' and p.proname in ('save_my_profile','get_my_cloud_profile','publish_skill','get_community_skill','list_community_skills','set_skill_favorite','record_skill_install','remove_community_skill','report_community_skill','list_community_reports','moderate_community_skill','submit_diagnostic') loop
  execute format('revoke all on function %s from public,anon,authenticated',f.signature);
  execute format('grant execute on function %s to authenticated',f.signature);
  if f.name in ('list_community_skills','get_community_skill','record_skill_install') then execute format('grant execute on function %s to anon',f.signature); end if;
 end loop;
end $$;
-- Anonymous readers also need the safe current-user boolean used by public catalog functions.
grant execute on function public.abyssal_is_admin() to anon;
notify pgrst,'reload schema';
commit;
