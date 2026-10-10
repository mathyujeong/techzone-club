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

export const buildStrictCourtMatches = (
  playersPool: Player[], 
  numCourts: number, 
  ignoreGrade: boolean, 
  sameGenderFirst: boolean,
  playCounts: Record<string, number>
) => {
  const matches: { blue_team: Player[], white_team: Player[], match_type: string }[] = [];

  // STAGE 1: Sort strictly by playCounts ascending so lowest play count players ALWAYS play first
  let males = playersPool
    .filter(p => p.gender === 'M' || !p.gender)
    .sort((a, b) => (playCounts[a.id] - playCounts[b.id]) || (Math.random() - 0.5));

  let females = playersPool
    .filter(p => p.gender === 'F')
    .sort((a, b) => (playCounts[a.id] - playCounts[b.id]) || (Math.random() - 0.5));

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

  // STAGE 2: 이번 라운드의 코트 구성(남복 a개, 여복 b개, 혼복 c개)을 고른다.
  // 우선순위:
  //   1) 코트를 최대한 많이 채운다
  //   2) 출전 횟수 격차가 1을 넘지 않게 한다 (특정 성별/사람만 계속 쉬는 것 방지)
  //   3) 선호 종목: sameGenderFirst면 남복+여복(혼복 대비)을, 아니면 혼복을 더 많이
  //   4) 출전 횟수가 적은 사람이 더 많이 뛰도록
  //   ※ 남복과 여복 사이에는 우선순위가 없다.
  const M = males.length;
  const F = females.length;
  const sumFront = (arr: Player[], n: number) => arr.slice(0, n).reduce((s, p) => s + (playCounts[p.id] || 0), 0);

  type Option = { a: number; b: number; c: number; courts: number; gap: number; pref: number; cost: number; rand: number };
  let best: Option | null = null;
  const better = (x: Option, y: Option | null) => {
    if (!y) return true;
    if (x.courts !== y.courts) return x.courts > y.courts;
    if (x.gap !== y.gap) return x.gap < y.gap;
    if (x.pref !== y.pref) return x.pref > y.pref;
    if (x.cost !== y.cost) return x.cost < y.cost;
    return x.rand < y.rand;
  };

  for (let a = 0; 4 * a <= M; a++) {
    for (let b = 0; 4 * b <= F; b++) {
      for (let c = 0; 4 * a + 2 * c <= M && 4 * b + 2 * c <= F; c++) {
        const courts = a + b + c;
        if (courts > numCourts) break;
        const nM = 4 * a + 2 * c;
        const nF = 4 * b + 2 * c;
        // 이 구성으로 뛰었을 때의 출전 횟수 격차
        const after = [
          ...males.map((p, i) => (playCounts[p.id] || 0) + (i < nM ? 1 : 0)),
          ...females.map((p, i) => (playCounts[p.id] || 0) + (i < nF ? 1 : 0)),
        ];
        const gap = after.length ? Math.max(1, Math.max(...after) - Math.min(...after)) : 1;
        const opt: Option = {
          a, b, c, courts, gap,
          pref: sameGenderFirst ? a + b : c,
          cost: sumFront(males, nM) + sumFront(females, nF),
          rand: Math.random(),
        };
        if (better(opt, best)) best = opt;
      }
    }
  }

  if (!best) return matches;

  // STAGE 3: 출전 횟수가 적은 순서대로 뽑아서 코트에 배치
  const pickedM = males.splice(0, 4 * best.a + 2 * best.c).sort(() => Math.random() - 0.5);
  const pickedF = females.splice(0, 4 * best.b + 2 * best.c).sort(() => Math.random() - 0.5);

  const sameGenderMatches: { blue_team: Player[], white_team: Player[], match_type: string }[] = [];
  for (let i = 0; i < best.a; i++) {
    const [team1, team2] = pairFourSameGender(pickedM.splice(0, 4));
    sameGenderMatches.push({ blue_team: team1, white_team: team2, match_type: 'MD' });
  }
  for (let i = 0; i < best.b; i++) {
    const [team1, team2] = pairFourSameGender(pickedF.splice(0, 4));
    sameGenderMatches.push({ blue_team: team1, white_team: team2, match_type: 'WD' });
  }
  // 코트 번호가 항상 남복→여복 순으로 고정되지 않도록 섞어준다
  sameGenderMatches.sort(() => Math.random() - 0.5);
  matches.push(...sameGenderMatches);

  for (let i = 0; i < best.c; i++) {
    const [team1, team2] = pairFourXD(pickedM.splice(0, 2), pickedF.splice(0, 2));
    matches.push({ blue_team: team1, white_team: team2, match_type: 'XD' });
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
      const roundCourtMatches = buildStrictCourtMatches(players, numCourts, ignoreGrade, sameGenderFirst, playCounts);

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
