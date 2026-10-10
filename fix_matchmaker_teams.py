import re

with open('src/lib/matchMaker.ts', 'r') as f:
    content = f.read()

old_sig = """export const generateMatches = (
  players: Player[], 
  matchType: 'TEAM' | 'INDIVIDUAL',
  numCourts: number = 3,
  numRounds: number = 5,
  ignoreGrade: boolean = false
) => {"""

new_sig = """export const generateMatches = (
  players: Player[], 
  matchType: 'TEAM' | 'INDIVIDUAL',
  numCourts: number = 3,
  numRounds: number = 5,
  ignoreGrade: boolean = false,
  manualBlueTeam: Player[] = [],
  manualWhiteTeam: Player[] = []
) => {"""
content = content.replace(old_sig, new_sig)


# We need to completely replace the inside of generateMatches.
# We will use regex to replace everything from "const matches = [];" to "return matches;"

new_body = """  const matches = [];
  const playCounts: Record<string, number> = {};
  players.forEach(p => playCounts[p.id] = 0);
  manualBlueTeam.forEach(p => playCounts[p.id] = 0);
  manualWhiteTeam.forEach(p => playCounts[p.id] = 0);

  for (let r = 1; r <= numRounds; r++) {
    const bluePairs: Player[][] = [];
    const whitePairs: Player[][] = [];

    if (matchType === 'TEAM' && manualBlueTeam.length > 0 && manualWhiteTeam.length > 0) {
      // TEAM MODE: Independent pairing for Blue and White
      const neededPlayersPerTeam = numCourts * 2;
      
      const getPairsForTeam = (teamPlayers: Player[]) => {
        const available = [...teamPlayers].sort((a, b) => {
          const countDiff = playCounts[a.id] - playCounts[b.id];
          if (countDiff !== 0) return countDiff;
          return Math.random() - 0.5;
        }).slice(0, neededPlayersPerTeam);

        if (!ignoreGrade) {
          available.sort((a, b) => getGradeValue(b.grade) - getGradeValue(a.grade));
        } else {
          available.sort(() => Math.random() - 0.5);
        }

        const pairs: Player[][] = [];
        const used = new Set<string>();

        for (let i = 0; i < available.length; i++) {
          if (used.has(available[i].id)) continue;
          let bestPartner = -1;
          let minGradeDiff = Infinity;

          for (let j = i + 1; j < available.length; j++) {
            if (used.has(available[j].id)) continue;
            const diff = Math.abs(getGradeValue(available[i].grade) - getGradeValue(available[j].grade));
            if (ignoreGrade) {
              bestPartner = j; break; // Just take next random
            }
            if (diff < minGradeDiff) {
              minGradeDiff = diff;
              bestPartner = j;
            }
          }
          if (bestPartner !== -1) {
            pairs.push([available[i], available[bestPartner]]);
            used.add(available[i].id);
            used.add(available[bestPartner].id);
          }
        }
        return pairs;
      };

      bluePairs.push(...getPairsForTeam(manualBlueTeam));
      whitePairs.push(...getPairsForTeam(manualWhiteTeam));

    } else {
      // INDIVIDUAL MODE (or fallback): Mix everyone
      const neededPlayers = numCourts * 4;
      const available = [...players].sort((a, b) => {
        const countDiff = playCounts[a.id] - playCounts[b.id];
        if (countDiff !== 0) return countDiff;
        return Math.random() - 0.5;
      }).slice(0, neededPlayers);

      if (!ignoreGrade) {
        available.sort((a, b) => getGradeValue(b.grade) - getGradeValue(a.grade));
      } else {
        available.sort(() => Math.random() - 0.5);
      }

      const pairs: Player[][] = [];
      const used = new Set<string>();

      for (let i = 0; i < available.length; i++) {
        if (used.has(available[i].id)) continue;
        let bestPartner = -1;
        let minGradeDiff = Infinity;
        for (let j = i + 1; j < available.length; j++) {
          if (used.has(available[j].id)) continue;
          const diff = Math.abs(getGradeValue(available[i].grade) - getGradeValue(available[j].grade));
          if (ignoreGrade) {
            bestPartner = j; break;
          }
          if (diff < minGradeDiff) {
            minGradeDiff = diff;
            bestPartner = j;
          }
        }
        if (bestPartner !== -1) {
          pairs.push([available[i], available[bestPartner]]);
          used.add(available[i].id);
          used.add(available[bestPartner].id);
        }
      }

      pairs.sort(() => Math.random() - 0.5);
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

      bluePairs[i].forEach(p => playCounts[p.id]++);
      whitePairs[i].forEach(p => playCounts[p.id]++);
    }
  }

  return matches;
};"""

# Replace everything from `  const matches = [];` to `return matches;\n};`
content = re.sub(r'  const matches = \[\];.*?return matches;\n};', new_body, content, flags=re.DOTALL)

with open('src/lib/matchMaker.ts', 'w') as f:
    f.write(content)
