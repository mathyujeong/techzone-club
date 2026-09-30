
create table if not exists matches (
  id uuid default gen_random_uuid() primary key,
  round_num integer not null,
  court_num integer not null,
  match_type text not null,
  blue_player1 text not null,
  blue_player2 text not null,
  white_player1 text not null,
  white_player2 text not null,
  blue_score integer default 0,
  white_score integer default 0,
  status text default 'pending'
);

delete from matches;

insert into matches (round_num, court_num, match_type, blue_player1, blue_player2, white_player1, white_player2) values
(1, 1, 'WD', '강민정', '김기원', '신나리', '김세라'),
(1, 2, 'MD', '유반석', '전영배', '이정훈', '최진용'),
(1, 3, 'WD', '현정혜', '배진희', '정규임', '조유정'),
(2, 1, 'WD', '현정혜', '양하나', '이청아', '정규임'),
(2, 2, 'MD', '김태섭', '유반석', '최진용', '김창수'),
(2, 3, 'WD', '강민정', '배진희', '신나리', '박지윤'),
(3, 1, 'WD', '김기원', '정진선', '박지윤', '이청아'),
(3, 2, 'MD', '강봉선', '주원희', '송온유', '이정훈'),
(3, 3, 'XD', '유반석', '유소라', '장상원', '정규임'),
(4, 1, 'MD', '강봉선', '주원희', '최진용', '송온유'),
(4, 2, 'XD', '전영배', '유소라', '김창수', '김세라'),
(4, 3, 'MD', '김태섭', '유반석', '백숙호', '장상원'),
(5, 1, 'WD', '현정혜', '유소라', '이청아', '신나리'),
(5, 2, 'WD', '배진희', '강민정', '조유정', '정규임'),
(5, 3, 'XD', '김태섭', '양하나', '이정훈', '김세라'),
(6, 1, 'MD', '강봉선', '김태섭', '송온유', '김창수'),
(6, 2, 'MD', '주원희', '전영배', '장상원', '백숙호'),
(6, 3, 'WD', '정진선', '김기원', '박지윤', '조유정'),
(7, 1, 'XD', '강봉선', '양하나', '백숙호', '박지윤'),
(7, 2, 'WD', '현정혜', '정진선', '이청아', '김세라');

alter table matches enable row level security;
drop policy if exists "public_select" on matches;
create policy "public_select" on matches for select using (true);
drop policy if exists "public_update" on matches;
create policy "public_update" on matches for update using (true);
drop policy if exists "public_insert" on matches;
create policy "public_insert" on matches for insert with check (true);
