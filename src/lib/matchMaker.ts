import { Player } from './types';

// Convert grade to numeric value for balancing
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

  // Penalize pairings that are too far apart in skill on the same team (e.g., S + E is frowned upon if possible)
  // Or actually, in badminton, A+D is a common balancing tactic. 
  // We'll lightly penalize massive gaps just to prevent extreme mismatch, but keep it mostly about team total balancing.
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

// Auto-generate doubles matches (Greedy approach + Randomization)
export const generateMatches = (
  players: Player[], 
  matchType: 'TEAM' | 'INDIVIDUAL',
  targetMatches: number = 7 // Default matches per round
) => {
  // Sort players by grade (S -> E)
  const sorted = [...players].sort((a, b) => getGradeValue(b.grade) - getGradeValue(a.grade));
  
  const matches = [];
  const unused = [...sorted];
  
  // Basic greedy pairing: High + Low to balance teams
  const pairs = [];
  while (unused.length >= 2) {
    // Take the strongest available
    const p1 = unused.shift()!;
    // Take the weakest available to balance
    const p2 = unused.pop()!;
    pairs.push([p1, p2]);
  }

  // Shuffle pairs
  pairs.sort(() => Math.random() - 0.5);

  if (matchType === 'TEAM') {
    // Divide pairs into Blue and White teams
    const bluePairs: Player[][] = [];
    const whitePairs: Player[][] = [];
    
    pairs.forEach((pair, idx) => {
      if (idx % 2 === 0) bluePairs.push(pair);
      else whitePairs.push(pair);
    });

    // Create matches
    const totalMatches = Math.min(bluePairs.length, whitePairs.length, targetMatches);
    for (let i = 0; i < totalMatches; i++) {
      matches.push({
        match_type: 'MD', // Default, should be inferred by gender if we had it, but we'll use MD/WD/XD dynamically later
        blue_team: bluePairs[i],
        white_team: whitePairs[i],
        blue_handicap: 0,
        white_handicap: 0,
      });
    }
  } else {
    // INDIVIDUAL: Randomly match pairs against each other
    for (let i = 0; i < pairs.length - 1; i += 2) {
      matches.push({
        match_type: 'MD',
        blue_team: pairs[i],
        white_team: pairs[i+1],
        blue_handicap: 0,
        white_handicap: 0,
      });
    }
  }

  return matches;
};
