import re

code = """import { Player } from './types';

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

export const buildCourtMatches = (available: Player[], ignoreGrade: boolean, sameGenderFirst: boolean) => {
  const matches: { blue_team: Player[], white_team: Player[], match_type: string }[] = [];

  let males = available.filter(p => p.gender === 'M' || !p.gender);
  let females = available.filter(p => p.gender === 'F');

  if (!ignoreGrade) {
    males.sort((a, b) => getGradeValue(b.grade) - getGradeValue(a.grade));
    females.sort((a, b) => getGradeValue(b.grade) - getGradeValue(a.grade));
  } else {
    males.sort(() => Math.random() - 0.5);
    females.sort(() => Math.random() - 0.5);
  }

  const pairFourSameGender = (four: Player[]) => {
    if (ignoreGrade) {
      return [ [four[0], four[1]], [four[2], four[3]] ];
    }
    // Balance 1st+4th vs 2nd+3rd for maximum game balance
    return [ [four[0], four[3]], [four[1], four[2]] ];
  };

  if (sameGenderFirst) {
    // 1. Form Pure MD Matches (Groups of 4 Males -> MD vs MD)
    while (males.length >= 4) {
      const four = males.splice(0, 4);
      const [team1, team2] = pairFourSameGender(four);
      matches.push({ blue_team: team1, white_team: team2, match_type: 'MD' });
    }

    // 2. Form Pure WD Matches (Groups of 4 Females -> WD vs WD)
    while (females.length >= 4) {
      const four = females.splice(0, 4);
      const [team1, team2] = pairFourSameGender(four);
      matches.push({ blue_team: team1, white_team: team2, match_type: 'WD' });
    }

    // 3. Form Pure Standard Mixed Doubles (Leftover 2 Males + 2 Females -> [M1, F1] vs [M2, F2])
    while (males.length >= 2 && females.length >= 2) {
      const m1 = males.shift()!;
      const m2 = males.shift()!;
      const f1 = females.shift()!;
      const f2 = females.shift()!;

      let team1 = [m1, f2];
      let team2 = [m2, f1];
      if (ignoreGrade) {
        team1 = [m1, f1];
        team2 = [m2, f2];
      }
      matches.push({ blue_team: team1, white_team: team2, match_type: 'XD' });
    }
  }

  // Leftover mixing if any odd players remain
  const remaining = [...males, ...females];
  while (remaining.length >= 4) {
    const four = remaining.splice(0, 4);
    const team1 = [four[0], four[1]];
    const team2 = [four[2], four[3]];
    matches.push({ blue_team: team1, white_team: team2, match_type: getMatchTypeLabel(team1, team2) });
  }

  return matches;
};

// Auto-generate doubles matches (Greedy approach + Randomization + Play Count Balancing)
export const generateMatches = (
  players: Player[], 
  matchType: 'TEAM' | 'INDIVIDUAL',
  numCourts: number = 3,
  numRounds: number = 5,
  ignoreGrade: boolean = false,
  manualBlueTeam: Player[] = [],
  manualWhiteTeam: Player[] = [],
  sameGenderFirst: boolean = true
) => {
  const matches = [];
  const playCounts: Record<string, number> = {};
  players.forEach(p => playCounts[p.id] = 0);
  manualBlueTeam.forEach(p => playCounts[p.id] = 0);
  manualWhiteTeam.forEach(p => playCounts[p.id] = 0);

  for (let r = 1; r <= numRounds; r++) {

    if (matchType === 'TEAM' && manualBlueTeam.length > 0 && manualWhiteTeam.length > 0) {
      const neededPlayersPerTeam = numCourts * 2;
      
      const getPairsForTeam = (teamPlayers: Player[]) => {
        const available = [...teamPlayers].sort((a, b) => {
          const countDiff = playCounts[a.id] - playCounts[b.id];
          if (countDiff !== 0) return countDiff;
          return Math.random() - 0.5;
        }).slice(0, neededPlayersPerTeam);

        // Simple pairing for team mode
        const pairs: Player[][] = [];
        for (let i = 0; i < available.length; i += 2) {
          if (i + 1 < available.length) pairs.push([available[i], available[i+1]]);
        }
        return pairs;
      };

      const bluePairs = getPairsForTeam(manualBlueTeam);
      const whitePairs = getPairsForTeam(manualWhiteTeam);
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
        bluePairs[i].forEach(p => playCounts[p.id]++);
        whitePairs[i].forEach(p => playCounts[p.id]++);
      }

    } else {
      const neededPlayers = numCourts * 4;
      const available = [...players].sort((a, b) => {
        const countDiff = playCounts[a.id] - playCounts[b.id];
        if (countDiff !== 0) return countDiff;
        return Math.random() - 0.5;
      }).slice(0, neededPlayers);

      const roundCourtMatches = buildCourtMatches(available, ignoreGrade, sameGenderFirst);
      const matchesThisRound = Math.min(roundCourtMatches.length, numCourts);

      for (let i = 0; i < matchesThisRound; i++) {
        const m = roundCourtMatches[i];
        matches.push({
          round_num: r,
          court_num: i + 1,
          match_type: m.match_type,
          blue_team: m.blue_team,
          white_team: m.white_team,
          blue_handicap: 0,
          white_handicap: 0,
        });

        m.blue_team.forEach(p => playCounts[p.id]++);
        m.white_team.forEach(p => playCounts[p.id]++);
      }
    }
  }

  return matches;
};
"""

with open('src/lib/matchMaker.ts', 'w') as f:
    f.write(code)
