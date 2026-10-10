import { Player } from './types';

// Convert grade to numeric value for balancing
export const getMatchTypeLabel = (team1: Player[], team2: Player[]) => {
  const allPlayers = [...team1, ...team2];
  const mCount = allPlayers.filter(p => p.gender === 'M' || !p.gender).length;
  const fCount = allPlayers.filter(p => p.gender === 'F').length;
  
  if (fCount === 0) return 'MD';
  if (mCount === 0) return 'WD';
  return 'XD';
};

export const getGradeValue = (grade: string): number => {
  const map: Record<string, number> = { 'S': 5, 'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0 };
  return map[grade] ?? 0;
};

// Evaluate how balanced a specific match is (lower penalty is better)
export const evaluateMatchCost = (team1: Player[], team2: Player[]): number => {
  const s1 = team1.reduce((sum, p) => sum + (p.default_penalty || 0), 0);
  const s2 = team2.reduce((sum, p) => sum + (p.default_penalty || 0), 0);
  const diff = Math.abs(s1 - s2);
  
  let penalty = (diff ** 2) * 100;
  if (team1.length === 2) {
    const d1 = Math.abs(getGradeValue(team1[0].grade) - getGradeValue(team1[1].grade));
    if (d1 >= 4) penalty += 2000;
  }
  if (team2.length === 2) {
    const d2 = Math.abs(getGradeValue(team2[0].grade) - getGradeValue(team2[1].grade));
    if (d2 >= 4) penalty += 2000;
  }
  return penalty;
};

// Auto-generate doubles matches (Greedy approach + Randomization + Play Count Balancing)
export const generateMatches = (
  players: Player[], 
  matchType: 'TEAM' | 'INDIVIDUAL',
  numCourts: number = 3,
  numRounds: number = 5,
  ignoreGrade: boolean = false
) => {
  const matches = [];
  const playCounts: Record<string, number> = {};
  players.forEach(p => playCounts[p.id] = 0);

  for (let r = 1; r <= numRounds; r++) {
    // Sort players primarily by fewest matches played, then randomly
    const available = [...players].sort((a, b) => {
      const countDiff = playCounts[a.id] - playCounts[b.id];
      if (countDiff !== 0) return countDiff;
      return Math.random() - 0.5;
    });

    // We need 4 players per court
    const neededPlayers = numCourts * 4;
    const roundPlayers = available.slice(0, Math.min(neededPlayers, available.length));
    
    const pairs: Player[][] = [];
    
    if (ignoreGrade) {
      roundPlayers.sort(() => Math.random() - 0.5);
      for (let i = 0; i < roundPlayers.length - 1; i += 2) {
        pairs.push([roundPlayers[i], roundPlayers[i+1]]);
      }
    } else {
      // Sort roundPlayers by grade to balance High + Low
      roundPlayers.sort((a, b) => getGradeValue(b.grade) - getGradeValue(a.grade));

      // Greedy pairing
      while (roundPlayers.length >= 2) {
        const p1 = roundPlayers.shift()!;
        const p2 = roundPlayers.pop()!;
        pairs.push([p1, p2]);
      }
    }

    pairs.sort(() => Math.random() - 0.5); // Shuffle pairs

    const bluePairs: Player[][] = [];
    const whitePairs: Player[][] = [];
    
    if (matchType === 'TEAM') {
      pairs.forEach((pair, idx) => {
        if (idx % 2 === 0) bluePairs.push(pair);
        else whitePairs.push(pair);
      });
    } else {
      // Individual: split randomly
      const half = Math.floor(pairs.length / 2);
      bluePairs.push(...pairs.slice(0, half));
      whitePairs.push(...pairs.slice(half, pairs.length));
    }

    const matchesThisRound = Math.min(bluePairs.length, whitePairs.length, numCourts);
    
    for (let i = 0; i < matchesThisRound; i++) {
      matches.push({
        round_num: r,
        court_num: i + 1,
        match_type: getMatchTypeLabel(bluePairs[i], whitePairs[i]),
        blue_team: bluePairs[i],
        white_team: whitePairs[i],
        blue_handicap: 0,
        white_handicap: 0,
      });

      // Update play counts
      bluePairs[i].forEach(p => playCounts[p.id]++);
      whitePairs[i].forEach(p => playCounts[p.id]++);
    }
  }

  return matches;
};
