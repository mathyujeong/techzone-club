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

export const createPairs = (available: Player[], ignoreGrade: boolean, sameGenderFirst: boolean = true) => {
  const pairs: Player[][] = [];
  const used = new Set<string>();

  const tryPairGroup = (group: Player[]) => {
    if (!ignoreGrade) {
      group.sort((a, b) => getGradeValue(b.grade) - getGradeValue(a.grade));
    } else {
      group.sort(() => Math.random() - 0.5);
    }

    for (let i = 0; i < group.length; i++) {
      if (used.has(group[i].id)) continue;
      let bestPartner = -1;
      let minGradeDiff = Infinity;

      for (let j = i + 1; j < group.length; j++) {
        if (used.has(group[j].id)) continue;
        const diff = Math.abs(getGradeValue(group[i].grade) - getGradeValue(group[j].grade));
        if (ignoreGrade) {
          bestPartner = j; break;
        }
        if (diff < minGradeDiff) {
          minGradeDiff = diff;
          bestPartner = j;
        }
      }

      if (bestPartner !== -1) {
        pairs.push([group[i], group[bestPartner]]);
        used.add(group[i].id);
        used.add(group[bestPartner].id);
      }
    }
  };

  if (sameGenderFirst) {
    const males = available.filter(p => p.gender === 'M' || !p.gender);
    const females = available.filter(p => p.gender === 'F');

    tryPairGroup(males);
    tryPairGroup(females);

    // Pair leftover odd male/female together
    const leftovers = available.filter(p => !used.has(p.id));
    tryPairGroup(leftovers);
  } else {
    tryPairGroup([...available]);
  }

  return pairs;
};

export const matchPairsIntoCourts = (allPairs: Player[][], sameGenderFirst: boolean) => {
  const blue: Player[][] = [];
  const white: Player[][] = [];

  if (sameGenderFirst) {
    const mdPairs = allPairs.filter(p => p.every(x => x.gender === 'M' || !x.gender));
    const wdPairs = allPairs.filter(p => p.every(x => x.gender === 'F'));
    const xdPairs = allPairs.filter(p => !mdPairs.includes(p) && !wdPairs.includes(p));

    // 1. Pair MD vs MD (Male pair vs Male pair -> Pure MD)
    while (mdPairs.length >= 2) {
      blue.push(mdPairs.pop()!);
      white.push(mdPairs.pop()!);
    }

    // 2. Pair WD vs WD (Female pair vs Female pair -> Pure WD)
    while (wdPairs.length >= 2) {
      blue.push(wdPairs.pop()!);
      white.push(wdPairs.pop()!);
    }

    // 3. Pair XD vs XD (Mixed pair vs Mixed pair -> Pure XD)
    while (xdPairs.length >= 2) {
      blue.push(xdPairs.pop()!);
      white.push(xdPairs.pop()!);
    }

    // 4. Any leftover odd single pairs get matched together
    const remaining = [...mdPairs, ...wdPairs, ...xdPairs];
    while (remaining.length >= 2) {
      blue.push(remaining.pop()!);
      white.push(remaining.pop()!);
    }
  } else {
    const shuffled = [...allPairs].sort(() => Math.random() - 0.5);
    const half = Math.floor(shuffled.length / 2);
    blue.push(...shuffled.slice(0, half));
    white.push(...shuffled.slice(half, shuffled.length));
  }

  return { blue, white };
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
    let bluePairs: Player[][] = [];
    let whitePairs: Player[][] = [];

    if (matchType === 'TEAM' && manualBlueTeam.length > 0 && manualWhiteTeam.length > 0) {
      const neededPlayersPerTeam = numCourts * 2;
      
      const getPairsForTeam = (teamPlayers: Player[]) => {
        const available = [...teamPlayers].sort((a, b) => {
          const countDiff = playCounts[a.id] - playCounts[b.id];
          if (countDiff !== 0) return countDiff;
          return Math.random() - 0.5;
        }).slice(0, neededPlayersPerTeam);

        return createPairs(available, ignoreGrade, sameGenderFirst);
      };

      bluePairs.push(...getPairsForTeam(manualBlueTeam));
      whitePairs.push(...getPairsForTeam(manualWhiteTeam));

    } else {
      const neededPlayers = numCourts * 4;
      const available = [...players].sort((a, b) => {
        const countDiff = playCounts[a.id] - playCounts[b.id];
        if (countDiff !== 0) return countDiff;
        return Math.random() - 0.5;
      }).slice(0, neededPlayers);

      const pairs = createPairs(available, ignoreGrade, sameGenderFirst);
      const matched = matchPairsIntoCourts(pairs, sameGenderFirst);
      bluePairs = matched.blue;
      whitePairs = matched.white;
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

      bluePairs[i].forEach(p => playCounts[p.id]++);
      whitePairs[i].forEach(p => playCounts[p.id]++);
    }
  }

  return matches;
};
"""

with open('src/lib/matchMaker.ts', 'w') as f:
    f.write(code)
