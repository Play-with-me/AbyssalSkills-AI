-- Explicit owner-selected bootstrap. Run only after confirming this exact account.
begin;
insert into abyssal_private.admin_users(user_id)
select id from auth.users where id='9e36935e-1538-401b-ac2e-9798ac5e784b' and lower(email)='kyuu449977@gmail.com' and email_confirmed_at is not null
on conflict do nothing;
commit;
