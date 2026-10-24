-- Supabase > SQL Editor에서 전체를 한 번 실행하세요. 다시 실행해도 기존 기록을 유지합니다.
-- 기존 관리자 계정(admin@techzone.club)을 그대로 사용합니다.
begin;

-- 최신 회원 38명. 기존 급수/성별/ID는 그대로 유지합니다.
insert into public.players (name, grade, default_penalty) values
('강봉선','S',-8), ('김기원','B',-3), ('김세라','A',-4), ('김승현','E',0),
('김여진','A',-4), ('김진수','D',-1), ('김창수','A',-4), ('김태섭','A',-4),
('박지윤','S',-5), ('박진현','A',-4), ('배진희','E',0), ('백숙호','D',-1),
('손병근','E',0), ('신나리','S',-5), ('양하나','A',-4), ('오성환','E',0),
('유반석','B',-3), ('유소라','A',-4), ('이정훈','B',-3), ('이청아','C',-2),
('장기철','E',0), ('장상원','E',0), ('장성학','A',-4), ('정광종','A',-4),
('정규임','D',-1), ('정진선','S',-5), ('조아라','D',-1), ('조유정','D',-1),
('주원휘','E',0), ('최진용','A',-4), ('현정혜','B',-3), ('배형남','E',0),
('박수신','E',0), ('송온유','D',-1), ('박미자','C',-2), ('전영배','E',0),
('송환희','D',-1), ('강민정','E',0)
on conflict (name) do nothing;

-- 탈퇴 회원만 삭제합니다. matches의 과거 경기 이름과 기록은 수정하지 않습니다.
delete from public.players where name = '송지은';

create table if not exists public.club_checklists (
  id uuid primary key default gen_random_uuid(),
  title text not null check (char_length(btrim(title)) between 1 and 100),
  description text not null default '' check (char_length(description) <= 2000),
  input_label text not null default '주문 내용' check (char_length(btrim(input_label)) between 1 and 40),
  default_amount integer not null default 0 check (default_amount >= 0),
  archived boolean not null default false,
  created_at timestamptz not null default now()
);

create table if not exists public.club_checklist_entries (
  id uuid primary key default gen_random_uuid(),
  checklist_id uuid not null references public.club_checklists(id) on delete cascade,
  player_id uuid references public.players(id) on delete set null,
  player_name text not null,
  content text not null default '' check (char_length(content) <= 500),
  memo text not null default '' check (char_length(memo) <= 1000),
  amount integer not null default 0 check (amount >= 0),
  is_paid boolean not null default false,
  paid_at timestamptz,
  unique (checklist_id, player_id)
);

-- 기존 공개 대진표 테이블의 정책은 변경하지 않고, 새 두 테이블만 관리자 전용으로 설정합니다.
do $$
declare
  table_name text;
  policy_record record;
begin
  foreach table_name in array array['club_checklists', 'club_checklist_entries'] loop
    execute format('alter table public.%I enable row level security', table_name);
    for policy_record in
      select policyname from pg_policies where schemaname = 'public' and tablename = table_name
    loop
      execute format('drop policy %I on public.%I', policy_record.policyname, table_name);
    end loop;
    execute format(
      'create policy "checklist_admin_only" on public.%I for all to authenticated '
      'using ((select auth.jwt() ->> ''email'') = ''admin@techzone.club'') '
      'with check ((select auth.jwt() ->> ''email'') = ''admin@techzone.club'')', table_name
    );
    execute format('revoke all on public.%I from anon, authenticated', table_name);
    execute format('grant select, insert, update, delete on public.%I to authenticated', table_name);
  end loop;
end $$;

-- 보관한 목록은 DB에서도 수정을 막습니다. 납부 시각은 서버에서 기록합니다.
create or replace function public.guard_club_checklist_entry()
returns trigger language plpgsql security invoker set search_path = '' as $$
declare
  is_archived boolean;
begin
  -- 회원 삭제 시 FK의 SET NULL은 과거 체크리스트 기록을 보존하기 위해 허용합니다.
  if tg_op = 'UPDATE' and old.player_id is not null and new.player_id is null
    and (to_jsonb(new) - 'player_id') = (to_jsonb(old) - 'player_id') then
    return new;
  end if;
  if tg_op = 'UPDATE' and new.checklist_id <> old.checklist_id then
    raise exception '다른 체크리스트로 기록을 이동할 수 없습니다.';
  end if;
  select archived into is_archived from public.club_checklists
    where id = case when tg_op = 'DELETE' then old.checklist_id else new.checklist_id end
    for share;
  if is_archived then
    raise exception '보관한 체크리스트입니다. 다시 열고 수정해주세요.';
  end if;
  if tg_op = 'DELETE' then return old; end if;
  if new.is_paid then
    if tg_op = 'INSERT' then
      new.paid_at := now();
    elsif not old.is_paid then
      new.paid_at := now();
    else
      new.paid_at := old.paid_at;
    end if;
  else
    new.paid_at := null;
  end if;
  return new;
end $$;

drop trigger if exists guard_club_checklist_entry on public.club_checklist_entries;
create trigger guard_club_checklist_entry before insert or update or delete
  on public.club_checklist_entries for each row execute function public.guard_club_checklist_entry();

-- 명단과 체크리스트는 한 트랜잭션으로 생성되어 중간 실패 시 빈 목록이 남지 않습니다.
create or replace function public.create_club_checklist(
  p_title text, p_description text, p_input_label text, p_default_amount integer, p_player_ids uuid[]
) returns uuid language plpgsql security invoker set search_path = '' as $$
declare
  new_id uuid;
  expected_count integer;
  inserted_count integer;
begin
  if (select auth.jwt() ->> 'email') is distinct from 'admin@techzone.club' then
    raise exception '관리자만 생성할 수 있습니다.';
  end if;
  select count(distinct id) into expected_count from unnest(p_player_ids) as ids(id);
  if expected_count = 0 then raise exception '회원을 한 명 이상 선택해주세요.'; end if;

  insert into public.club_checklists (title, description, input_label, default_amount)
    values (btrim(p_title), p_description, btrim(p_input_label), p_default_amount) returning id into new_id;
  insert into public.club_checklist_entries (checklist_id, player_id, player_name, amount)
    select new_id, id, name, p_default_amount from public.players where id = any(p_player_ids);
  get diagnostics inserted_count = row_count;
  if inserted_count <> expected_count then
    raise exception '회원 명단이 변경되었습니다. 새로 불러온 뒤 다시 생성해주세요.';
  end if;
  return new_id;
end $$;

create or replace function public.add_club_checklist_members(p_checklist_id uuid, p_player_ids uuid[])
returns void language plpgsql security invoker set search_path = '' as $$
declare
  list_row public.club_checklists%rowtype;
begin
  if (select auth.jwt() ->> 'email') is distinct from 'admin@techzone.club' then
    raise exception '관리자만 추가할 수 있습니다.';
  end if;
  select * into strict list_row from public.club_checklists where id = p_checklist_id for update;
  if list_row.archived then raise exception '보관한 체크리스트입니다. 다시 열고 수정해주세요.'; end if;
  if coalesce(cardinality(p_player_ids), 0) = 0 then raise exception '회원을 선택해주세요.'; end if;
  if exists (select 1 from unnest(p_player_ids) as ids(id)
    where not exists (select 1 from public.players where players.id = ids.id)) then
    raise exception '회원 명단이 변경되었습니다. 새로 불러온 뒤 다시 추가해주세요.';
  end if;
  insert into public.club_checklist_entries (checklist_id, player_id, player_name, amount)
    select list_row.id, id, name, list_row.default_amount from public.players where id = any(p_player_ids)
    on conflict (checklist_id, player_id) do nothing;
end $$;

revoke all on function public.create_club_checklist(text, text, text, integer, uuid[]) from public, anon;
revoke all on function public.add_club_checklist_members(uuid, uuid[]) from public, anon;
grant execute on function public.create_club_checklist(text, text, text, integer, uuid[]) to authenticated;
grant execute on function public.add_club_checklist_members(uuid, uuid[]) to authenticated;
revoke all on function public.guard_club_checklist_entry() from public, anon;

notify pgrst, 'reload schema';
commit;
