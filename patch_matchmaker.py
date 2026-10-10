with open('src/lib/matchMaker.ts', 'r') as f:
    content = f.read()

old_sig = """export const generateMatches = (
  players: Player[], 
  matchType: 'TEAM' | 'INDIVIDUAL',
  numCourts: number = 3,
  numRounds: number = 5
) => {"""

new_sig = """export const generateMatches = (
  players: Player[], 
  matchType: 'TEAM' | 'INDIVIDUAL',
  numCourts: number = 3,
  numRounds: number = 5,
  ignoreGrade: boolean = false
) => {"""

content = content.replace(old_sig, new_sig)

old_pairing = """    // Sort roundPlayers by grade to balance High + Low
    roundPlayers.sort((a, b) => getGradeValue(b.grade) - getGradeValue(a.grade));

    // Greedy pairing
    const pairs: Player[][] = [];
    while (roundPlayers.length >= 2) {
      const p1 = roundPlayers.shift()!;
      const p2 = roundPlayers.pop()!;
      pairs.push([p1, p2]);
    }"""

new_pairing = """    const pairs: Player[][] = [];
    
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
    }"""

content = content.replace(old_pairing, new_pairing)

with open('src/lib/matchMaker.ts', 'w') as f:
    f.write(content)
