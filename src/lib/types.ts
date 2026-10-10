export type Grade = 'S' | 'A' | 'B' | 'C' | 'D' | 'E';

export interface Player {
  id: string;
  name: string;
  grade: Grade;
  default_penalty: number;
  gender?: 'M' | 'F';
  created_at: string;
}

export type MatchType = 'TEAM' | 'INDIVIDUAL';
export type DisplayMode = 'WIN_LOSS' | 'SCORE';
export type TournamentStatus = 'READY' | 'IN_PROGRESS' | 'COMPLETED';

export interface Tournament {
  id: string;
  title: string;
  match_type: MatchType;
  display_mode: DisplayMode;
  status: TournamentStatus;
  created_at: string;
}

export interface Match {
  id: string;
  tournament_id: string;
  round_num: number;
  court_num: number;
  match_type: string; // e.g. 'MD', 'WD', 'XD'
  blue_player1: string;
  blue_player2: string;
  white_player1: string;
  white_player2: string;
  blue_score: number;
  white_score: number;
  blue_handicap: number;
  white_handicap: number;
  status: 'pending' | 'completed';
}
