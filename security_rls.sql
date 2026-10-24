-- 보안 강화: 대진표는 공개 조회, 주문/납부는 관리자 전용. 쓰기/수정/삭제는 관리자만 가능.
-- Supabase Dashboard > SQL Editor 에서 실행하세요.
-- (먼저 Authentication > Users 에서 admin@techzone.club 계정을 만들어야 합니다)

do $$
declare
  t record;
  p record;
begin
  for t in select tablename from pg_tables where schemaname = 'public' loop
    execute format('alter table public.%I enable row level security', t.tablename);

    -- 기존의 "누구나 수정 가능" 정책을 모두 제거
    for p in select policyname from pg_policies where schemaname = 'public' and tablename = t.tablename loop
      execute format('drop policy %I on public.%I', p.policyname, t.tablename);
    end loop;

    -- 주문/납부 테이블은 관리자 전용입니다. 대진표 등 공개 테이블만 조회를 허용합니다.
    if t.tablename not in ('club_checklists', 'club_checklist_entries') then
      execute format('create policy "public_read" on public.%I for select using (true)', t.tablename);
    end if;

    -- 관리자 계정만 추가/수정/삭제 가능
    execute format(
      'create policy "admin_write" on public.%I for all to authenticated '
      'using ((auth.jwt() ->> ''email'') = ''admin@techzone.club'') '
      'with check ((auth.jwt() ->> ''email'') = ''admin@techzone.club'')',
      t.tablename
    );
  end loop;
end $$;

-- 확인용: 각 테이블의 정책 목록
select tablename, policyname, cmd, roles from pg_policies where schemaname = 'public' order by tablename;
