import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Replace the stats logic
old_logic = """  const playerStats: Record<string, number> = {};
  currentMatches.forEach(m => {
    [m.blue_player1, m.blue_player2, m.white_player1, m.white_player2].forEach(p => {
      if(p) playerStats[p] = (playerStats[p] || 0) + 1;
    });
  });

  const blueTeamStats = Object.entries(playerStats)
    .filter(([name]) => currentMatches.some(m => m.blue_player1 === name || m.blue_player2 === name))
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
    
  const whiteTeamStats = Object.entries(playerStats)
    .filter(([name]) => currentMatches.some(m => m.white_player1 === name || m.white_player2 === name))
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));"""

new_logic = """  const selectedTournament = tournaments.find(t => t.id === selectedTournamentId);
  const isIndividualMode = selectedTournament?.match_type === 'INDIVIDUAL';

  const playerStatsMap: Record<string, { matches: number, wins: number, team: 'BLUE' | 'WHITE' | 'MIXED' }> = {};
  currentMatches.forEach(m => {
    const isCompleted = m.status === 'completed';
    const blueWon = isCompleted && m.blue_score > m.white_score;
    const whiteWon = isCompleted && m.white_score > m.blue_score;
    
    const addStat = (pName: string, isBlue: boolean) => {
      if (!pName) return;
      if (!playerStatsMap[pName]) playerStatsMap[pName] = { matches: 0, wins: 0, team: isBlue ? 'BLUE' : 'WHITE' };
      
      playerStatsMap[pName].matches++;
      if (playerStatsMap[pName].team !== (isBlue ? 'BLUE' : 'WHITE')) {
        playerStatsMap[pName].team = 'MIXED';
      }
      
      if (isBlue && blueWon) playerStatsMap[pName].wins++;
      if (!isBlue && whiteWon) playerStatsMap[pName].wins++;
    };

    addStat(m.blue_player1, true);
    addStat(m.blue_player2, true);
    addStat(m.white_player1, false);
    addStat(m.white_player2, false);
  });

  const allStats = Object.entries(playerStatsMap).map(([name, data]) => ({ name, ...data }));
  
  const blueTeamStats = allStats.filter(s => s.team === 'BLUE').sort((a, b) => b.matches - a.matches || b.wins - a.wins);
  const whiteTeamStats = allStats.filter(s => s.team === 'WHITE').sort((a, b) => b.matches - a.matches || b.wins - a.wins);
  const individualStats = [...allStats].sort((a, b) => b.wins - a.wins || b.matches - a.matches);"""

content = content.replace(old_logic, new_logic)

# 2. Replace the UI
old_ui = """      {/* 통계 패널 */}
      <div className="container mx-auto px-4 pt-8">
        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
          <h2 className="text-lg font-bold mb-6 flex items-center gap-2 border-b border-gray-100 dark:border-gray-800 pb-4">
            <Users className="text-yellow-600 w-5 h-5" />팀 구성 및 선수별 배정 경기 수
          </h2>
          <div className="flex flex-col md:flex-row gap-8">
            <div className="flex-1">
              <h3 className="text-sm font-bold text-blue-600 dark:text-blue-400 mb-3 flex items-center gap-1">
                청팀 <span className="bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 text-xs px-2 py-0.5 rounded-full">{blueTeamStats.length}명</span>
              </h3>
              <div className="flex flex-wrap gap-2">
                {blueTeamStats.map(([name, count]) => (
                  <span key={name} className="bg-blue-50 border border-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm dark:bg-blue-900/30 dark:border-blue-800 dark:text-blue-300">
                    {name} <span className="font-bold opacity-70">({count})</span>
                  </span>
                ))}
              </div>
            </div>
            <div className="hidden md:block w-px bg-gray-200 dark:bg-gray-800"></div>
            <div className="flex-1">
              <h3 className="text-sm font-bold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-1">
                백팀 <span className="bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300 text-xs px-2 py-0.5 rounded-full">{whiteTeamStats.length}명</span>
              </h3>
              <div className="flex flex-wrap gap-2">
                {whiteTeamStats.map(([name, count]) => (
                  <span key={name} className="bg-gray-100 border border-gray-200 text-gray-800 px-3 py-1 rounded-full text-sm dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300">
                    {name} <span className="font-bold opacity-70">({count})</span>
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>"""

new_ui = """      {/* 통계 패널 */}
      <div className="container mx-auto px-4 pt-8">
        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
          <h2 className="text-lg font-bold mb-6 flex items-center gap-2 border-b border-gray-100 dark:border-gray-800 pb-4">
            <Users className="text-yellow-600 w-5 h-5" />
            {isIndividualMode ? '개인별 성적 및 배정 경기 수' : '팀 구성 및 선수별 배정 경기 수'}
          </h2>
          
          {isIndividualMode ? (
            <div className="flex flex-wrap gap-3">
              {individualStats.map(s => (
                <div key={s.name} className="bg-gray-50 border border-gray-200 text-gray-800 px-3 py-2 rounded-xl text-sm dark:bg-gray-800 dark:border-gray-700 dark:text-gray-200 flex flex-col min-w-[100px]">
                  <span className="font-black text-center mb-1 text-base">{s.name}</span>
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>{s.matches}경기</span>
                    <span className="text-blue-600 font-bold">{s.wins}승</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col md:flex-row gap-8">
              <div className="flex-1">
                <h3 className="text-sm font-bold text-blue-600 dark:text-blue-400 mb-3 flex items-center gap-1">
                  청팀 <span className="bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 text-xs px-2 py-0.5 rounded-full">{blueTeamStats.length}명</span>
                </h3>
                <div className="flex flex-wrap gap-2">
                  {blueTeamStats.map(s => (
                    <div key={s.name} className="bg-blue-50 border border-blue-100 text-blue-800 px-3 py-1.5 rounded-xl text-sm dark:bg-blue-900/30 dark:border-blue-800 dark:text-blue-300 flex items-center gap-2">
                      <span className="font-bold">{s.name}</span>
                      <span className="text-xs opacity-70 border-l border-blue-200 pl-2">{s.matches}경기 <span className="font-bold text-blue-700">{s.wins}승</span></span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="hidden md:block w-px bg-gray-200 dark:bg-gray-800"></div>
              <div className="flex-1">
                <h3 className="text-sm font-bold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-1">
                  백팀 <span className="bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300 text-xs px-2 py-0.5 rounded-full">{whiteTeamStats.length}명</span>
                </h3>
                <div className="flex flex-wrap gap-2">
                  {whiteTeamStats.map(s => (
                    <div key={s.name} className="bg-gray-100 border border-gray-200 text-gray-800 px-3 py-1.5 rounded-xl text-sm dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300 flex items-center gap-2">
                      <span className="font-bold">{s.name}</span>
                      <span className="text-xs opacity-70 border-l border-gray-300 pl-2">{s.matches}경기 <span className="font-bold text-gray-700">{s.wins}승</span></span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>"""

content = content.replace(old_ui, new_ui)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
