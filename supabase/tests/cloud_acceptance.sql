-- Append inside migration transaction before COMMIT; all fixtures are rolled back.
insert into auth.users(id,aud,role,email,created_at,updated_at) values
('a1100000-0000-4000-8000-000000000001','authenticated','authenticated','abyssal-audit-a@example.invalid',now(),now()),
('a1100000-0000-4000-8000-000000000002','authenticated','authenticated','abyssal-audit-b@example.invalid',now(),now());
set local role authenticated;
select set_config('request.jwt.claim.sub','a1100000-0000-4000-8000-000000000001',true);
select set_config('abyssal.test_skill_id',public.publish_skill('{"slug":"audit-cloud-test","display_title":"Audit cloud test","description":"Disposable transaction fixture","category":"Test","skill_content":"# Audit","references":[{"filename":"guide.md","content":"guide"}],"rules":[]}'::jsonb)->>'id',true);
do $$ begin
 if public.get_community_skill(current_setting('abyssal.test_skill_id'))->>'skill_content'<>'# Audit' then raise exception 'content roundtrip failed'; end if;
 begin
  update public.profiles set role='admin' where id=auth.uid();
  raise exception 'role self-escalation succeeded';
 exception when insufficient_privilege then null; end;
 if public.abyssal_is_admin() then raise exception 'untrusted role grants admin'; end if;
 perform public.submit_diagnostic('a1100000-0000-4000-8000-000000000003','{"fingerprint":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","error_type":"Audit","error_message":"Synthetic test only","module_name":"audit","app_version":"test","traceback":"synthetic"}');
 if (public.submit_diagnostic('a1100000-0000-4000-8000-000000000003','{"fingerprint":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}')->>'duplicate')::boolean is not true then raise exception 'retry not idempotent'; end if;
 begin perform public.submit_diagnostic('a1100000-0000-4000-8000-000000000004','{"fingerprint":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}');raise exception 'rate limit failed';exception when sqlstate 'P0001' then if sqlerrm='rate limit failed' then raise; end if;end;
end $$;
select set_config('request.jwt.claim.sub','a1100000-0000-4000-8000-000000000002',true);
do $$ begin
 if public.get_community_skill(current_setting('abyssal.test_skill_id')) is null then raise exception 'B cannot read public skill'; end if;
 begin perform public.remove_community_skill(current_setting('abyssal.test_skill_id'));raise exception 'B removed A content';exception when insufficient_privilege then null;end;
 begin perform public.publish_skill(jsonb_build_object('id',current_setting('abyssal.test_skill_id'),'slug','audit-cloud-test','skill_content','# Hacked'));raise exception 'B edited A content';exception when insufficient_privilege then null;end;
 perform public.set_skill_favorite(current_setting('abyssal.test_skill_id'),true);
 perform public.report_community_skill(current_setting('abyssal.test_skill_id'),'Synthetic report');
 begin perform public.list_community_reports();raise exception 'B read moderation reports';exception when insufficient_privilege then null;end;
 begin perform count(*) from public.system_error_reports;raise exception 'B read diagnostics';exception when insufficient_privilege then null;end;
end $$;
set local role anon;
select set_config('request.jwt.claim.sub','',true);
do $$ begin
 if public.get_community_skill(current_setting('abyssal.test_skill_id')) is null then raise exception 'anon cannot read public';end if;
 begin perform public.publish_skill('{"slug":"bad","skill_content":"bad"}');raise exception 'anon published';exception when insufficient_privilege then null;end;
 perform public.record_skill_install(current_setting('abyssal.test_skill_id'),'a1100000-0000-4000-8000-000000000005');
 perform public.record_skill_install(current_setting('abyssal.test_skill_id'),'a1100000-0000-4000-8000-000000000005');
 if (public.get_community_skill(current_setting('abyssal.test_skill_id'))->>'downloads_count')::integer<>1 then raise exception 'install retry counted twice';end if;
end $$;
set local role authenticated;
select set_config('request.jwt.claim.sub','a1100000-0000-4000-8000-000000000001',true);
select public.remove_community_skill(current_setting('abyssal.test_skill_id'));
set local role anon;
select set_config('request.jwt.claim.sub','',true);
do $$ begin
 if public.get_community_skill(current_setting('abyssal.test_skill_id')) is not null then raise exception 'removed skill remains public';end if;
end $$;
reset role;
select 'PASS: cloud roundtrip, owner isolation, role protection, anonymous read, favorites, reports, telemetry idempotency and cooldown, soft removal' as acceptance;
rollback;
