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

export const buildStrictCourtMatches = (
  playersPool: Player[], 
  numCourts: number, 
  ignoreGrade: boolean, 
  sameGenderFirst: boolean
) => {
  const matches: { blue_team: Player[], white_team: Player[], match_type: string }[] = [];

  // Sort candidate pool by play count (fewest games played first) + random jitter
  const pool = [...playersPool].sort(() => Math.random() - 0.5);

  let males = pool.filter(p => p.gender === 'M' || !p.gender);
  let females = pool.filter(p => p.gender === 'F');

  const pairFourSameGender = (four: Player[]) => {
    if (!ignoreGrade) {
      four.sort((a, b) => getGradeValue(b.grade) - getGradeValue(a.grade));
      // 1st+4th vs 2nd+3rd for grade balance
      return [ [four[0], four[3]], [four[1], four[2]] ];
    }
    return [ [four[0], four[1]], [four[2], four[3]] ];
  };

  const pairFourXD = (twoM: Player[], twoF: Player[]) => {
    if (!ignoreGrade) {
      twoM.sort((a, b) => getGradeValue(b.grade) - getGradeValue(a.grade));
      twoF.sort((a, b) => getGradeValue(b.grade) - getGradeValue(a.grade));
      // M1 + F2 vs M2 + F1
      return [ [twoM[0], twoF[1]], [twoM[1], twoF[0]] ];
    }
    return [ [twoM[0], twoF[0]], [twoM[1], twoF[1]] ];
  };

  if (sameGenderFirst) {
    // Priority 1: Form 4-Man MD Matches
    while (males.length >= 4 && matches.length < numCourts) {
      const four = males.splice(0, 4);
      const [team1, team2] = pairFourSameGender(four);
      matches.push({ blue_team: team1, white_team: team2, match_type: 'MD' });
    }

    // Priority 2: Form 4-Woman WD Matches
    while (females.length >= 4 && matches.length < numCourts) {
      const four = females.splice(0, 4);
      const [team1, team2] = pairFourSameGender(four);
      matches.push({ blue_team: team1, white_team: team2, match_type: 'WD' });
    }

    // Priority 3: Form Strict 2M + 2F XD Matches (남녀 vs 남녀)
    while (males.length >= 2 && females.length >= 2 && matches.length < numCourts) {
      const twoM = males.splice(0, 2);
      const twoF = females.splice(0, 2);
      const [team1, team2] = pairFourXD(twoM, twoF);
      matches.push({ blue_team: team1, white_team: team2, match_type: 'XD' });
    }
  } else {
    // MIXED MODE: Priority 1 - Strict XD (2M + 2F)
    while (males.length >= 2 && females.length >= 2 && matches.length < numCourts) {
      const twoM = males.splice(0, 2);
      const twoF = females.splice(0, 2);
      const [team1, team2] = pairFourXD(twoM, twoF);
      matches.push({ blue_team: team1, white_team: team2, match_type: 'XD' });
    }

    // Fallback MD
    while (males.length >= 4 && matches.length < numCourts) {
      const four = males.splice(0, 4);
      const [team1, team2] = pairFourSameGender(four);
      matches.push({ blue_team: team1, white_team: team2, match_type: 'MD' });
    }

    // Fallback WD
    while (females.length >= 4 && matches.length < numCourts) {
      const four = females.splice(0, 4);
      const [team1, team2] = pairFourSameGender(four);
      matches.push({ blue_team: team1, white_team: team2, match_type: 'WD' });
    }
  }

  // ABSOLUTELY NEVER ALLOW 3:1 or 1:3 RATIO MATCHES!
  // If any courts are still empty, and we have >= 4 males or >= 4 females, form MD/WD
  while (males.length >= 4 && matches.length < numCourts) {
    const four = males.splice(0, 4);
    const [team1, team2] = pairFourSameGender(four);
    matches.push({ blue_team: team1, white_team: team2, match_type: 'MD' });
  }

  while (females.length >= 4 && matches.length < numCourts) {
    const four = females.splice(0, 4);
    const [team1, team2] = pairFourSameGender(four);
    matches.push({ blue_team: team1, white_team: team2, match_type: 'WD' });
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
      // Sort all players by playCount first to ensure play count balancing across rounds
      const sortedPool = [...players].sort((a, b) => {
        const countDiff = playCounts[a.id] - playCounts[b.id];
        if (countDiff !== 0) return countDiff;
        return Math.random() - 0.5;
      });

      const roundCourtMatches = buildStrictCourtMatches(sortedPool, numCourts, ignoreGrade, sameGenderFirst);

      for (let i = 0; i < roundCourtMatches.length; i++) {
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
