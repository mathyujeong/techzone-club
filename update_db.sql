-- 1. Create players table
CREATE TABLE IF NOT EXISTS players (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    grade TEXT NOT NULL CHECK (grade IN ('S', 'A', 'B', 'C', 'D', 'E')),
    default_penalty INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert existing players
INSERT INTO players (name, grade, default_penalty) VALUES
('강봉선', 'S', -8), ('김태섭', 'A', -4), ('유반석', 'B', -3), ('전영배', 'E', 0), ('주원희', 'E', 0),
('정진선', 'S', -5), ('양하나', 'A', -4), ('유소라', 'A', -4), ('현정혜', 'B', -3), ('이청아', 'C', -2),
('정규임', 'D', -1), ('배진희', 'E', 0), ('최진용', 'A', -4), ('김창수', 'A', -4), ('이정훈', 'B', -3),
('송온유', 'D', -1), ('백숙호', 'D', -1), ('장상원', 'E', 0), ('박지윤', 'S', -5), ('신나리', 'S', -5),
('김세라', 'A', -4), ('김기원', 'B', -3), ('조유정', 'D', -1), ('강민정', 'E', 0)
ON CONFLICT (name) DO NOTHING;

-- 2. Create tournaments table
CREATE TABLE IF NOT EXISTS tournaments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL,
    match_type TEXT NOT NULL DEFAULT 'TEAM', -- 'TEAM' or 'INDIVIDUAL'
    display_mode TEXT NOT NULL DEFAULT 'WIN_LOSS', -- 'WIN_LOSS' or 'SCORE'
    status TEXT NOT NULL DEFAULT 'READY', -- 'READY', 'IN_PROGRESS', 'COMPLETED'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert a default tournament for existing matches
INSERT INTO tournaments (id, title, match_type, display_mode, status) 
VALUES ('00000000-0000-0000-0000-000000000000', '26년 최초 월례회', 'TEAM', 'WIN_LOSS', 'COMPLETED')
ON CONFLICT (id) DO NOTHING;

-- 3. Modify matches table safely
ALTER TABLE matches ADD COLUMN IF NOT EXISTS tournament_id UUID REFERENCES tournaments(id) ON DELETE CASCADE;
ALTER TABLE matches ADD COLUMN IF NOT EXISTS blue_handicap INTEGER DEFAULT 0;
ALTER TABLE matches ADD COLUMN IF NOT EXISTS white_handicap INTEGER DEFAULT 0;

UPDATE matches SET tournament_id = '00000000-0000-0000-0000-000000000000' WHERE tournament_id IS NULL;

-- 4. Set Row Level Security (RLS)
ALTER TABLE players ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "public_all_players" ON players;
CREATE POLICY "public_all_players" ON players FOR ALL USING (true);

ALTER TABLE tournaments ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "public_all_tournaments" ON tournaments;
CREATE POLICY "public_all_tournaments" ON tournaments FOR ALL USING (true);
