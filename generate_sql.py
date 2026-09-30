import json
with open('src/data/tournament.json', 'r') as f:
    schedule = json.load(f)
sql = """
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
"""
values = []
for m in schedule:
    b1, b2 = m['blue_team'][0].split('(')[0], m['blue_team'][1].split('(')[0]
    w1, w2 = m['white_team'][0].split('(')[0], m['white_team'][1].split('(')[0]
    values.append(f"({m['round']}, {m['court']}, '{m['type']}', '{b1}', '{b2}', '{w1}', '{w2}')")
sql += ",\n".join(values) + ";\n"
sql += """
alter table matches enable row level security;
drop policy if exists "public_select" on matches;
create policy "public_select" on matches for select using (true);
drop policy if exists "public_update" on matches;
create policy "public_update" on matches for update using (true);
drop policy if exists "public_insert" on matches;
create policy "public_insert" on matches for insert with check (true);
"""
with open('init_db.sql', 'w') as f:
    f.write(sql)
