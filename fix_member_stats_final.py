import re

with open('src/app/tournament/page.tsx', 'r') as f:
    content = f.read()

# Replace playerStatsMap type & initialization
content = content.replace(
    "const playerStatsMap: Record<string, { matches: number, wins: number, team: 'BLUE' | 'WHITE' | 'MIXED' }> = {};",
    "const playerStatsMap: Record<string, { matches: number, wins: number, losses: number, team: 'BLUE' | 'WHITE' | 'MIXED' }> = {};"
)

content = content.replace(
    "playerStatsMap[p.name] = { matches: 0, wins: 0, team: 'MIXED' };",
    "playerStatsMap[p.name] = { matches: 0, wins: 0, losses: 0, team: 'MIXED' };"
)

content = content.replace(
    "if (!playerStatsMap[pName]) playerStatsMap[pName] = { matches: 0, wins: 0, team: isBlue ? 'BLUE' : 'WHITE' };",
    "if (!playerStatsMap[pName]) playerStatsMap[pName] = { matches: 0, wins: 0, losses: 0, team: isBlue ? 'BLUE' : 'WHITE' };"
)

# Replace addStat inner logic to calculate losses
old_add_stat_logic = """      if (isBlue && blueWon) playerStatsMap[pName].wins++;
      if (!isBlue && whiteWon) playerStatsMap[pName].wins++;"""

new_add_stat_logic = """      if (isCompleted) {
        if ((isBlue && blueWon) || (!isBlue && whiteWon)) {
          playerStatsMap[pName].wins++;
        } else if ((isBlue && whiteWon) || (!isBlue && blueWon)) {
          playerStatsMap[pName].losses++;
        }
      }"""

content = content.replace(old_add_stat_logic, new_add_stat_logic)

with open('src/app/tournament/page.tsx', 'w') as f:
    f.write(content)
