import re

# 1. Admin page
with open('src/app/admin/page.tsx', 'r') as f:
    admin = f.read()

# Do not pre-fill dbPlayers into playerStatsMap, only populate from matches, and filter s.matches > 0
old_admin_prep = """  const playerStatsMap: Record<string, { matches: number, wins: number, losses: number, team: 'BLUE' | 'WHITE' | 'MIXED' }> = {};
  dbPlayers.forEach(p => {
    playerStatsMap[p.name] = { matches: 0, wins: 0, losses: 0, team: 'MIXED' };
  });"""

new_admin_prep = """  const playerStatsMap: Record<string, { matches: number, wins: number, losses: number, team: 'BLUE' | 'WHITE' | 'MIXED' }> = {};"""

admin = admin.replace(old_admin_prep, new_admin_prep)

old_admin_all_stats = "const allStats = Object.entries(playerStatsMap).map(([name, data]) => ({ name, ...data }));"
new_admin_all_stats = "const allStats = Object.entries(playerStatsMap).map(([name, data]) => ({ name, ...data })).filter(s => s.matches > 0);"
admin = admin.replace(old_admin_all_stats, new_admin_all_stats)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(admin)

# 2. Member page
with open('src/app/tournament/page.tsx', 'r') as f:
    member = f.read()

old_member_prep = """  const playerStatsMap: Record<string, { matches: number, wins: number, losses: number, team: 'BLUE' | 'WHITE' | 'MIXED' }> = {};
  
  dbPlayers.forEach(p => {
    playerStatsMap[p.name] = { matches: 0, wins: 0, losses: 0, team: 'MIXED' };
  });"""

new_member_prep = """  const playerStatsMap: Record<string, { matches: number, wins: number, losses: number, team: 'BLUE' | 'WHITE' | 'MIXED' }> = {};"""

member = member.replace(old_member_prep, new_member_prep)

old_member_all_stats = "const allStats = Object.entries(playerStatsMap)\n    .map(([name, data]) => ({ name, ...data }));"
new_member_all_stats = "const allStats = Object.entries(playerStatsMap)\n    .map(([name, data]) => ({ name, ...data })).filter(s => s.matches > 0);"
member = member.replace(old_member_all_stats, new_member_all_stats)

with open('src/app/tournament/page.tsx', 'w') as f:
    f.write(member)

