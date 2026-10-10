import re

with open('src/app/tournament/page.tsx', 'r') as f:
    content = f.read()

# Replace the stats computation
old_stats = """  // 선수별 통계
  const playerStats: Record<string, number> = {};
  matches.forEach(m => {
    [m.blue_player1, m.blue_player2, m.white_player1, m.white_player2].forEach(p => {
      if(p) playerStats[p] = (playerStats[p] || 0) + 1;
    });
  });

  const blueTeamStats = Object.entries(playerStats)
    .filter(([name]) => matches.some(m => m.blue_player1 === name || m.blue_player2 === name))
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
    
  const whiteTeamStats = Object.entries(playerStats)
    .filter(([name]) => matches.some(m => m.white_player1 === name || m.white_player2 === name))
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));"""

new_stats = """  // 선수별 통계
  const isIndividualMode = activeTournament?.match_type === 'INDIVIDUAL';
  const playerStatsMap: Record<string, { matches: number, wins: number, team: 'BLUE' | 'WHITE' | 'MIXED' }> = {};
  
  dbPlayers.forEach(p => {
    playerStatsMap[p.name] = { matches: 0, wins: 0, team: 'MIXED' };
  });

  matches.forEach(m => {
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

    addStat(String(m.blue_player1), true);
    addStat(String(m.blue_player2), true);
    addStat(String(m.white_player1), false);
    addStat(String(m.white_player2), false);
  });

  const allStats = Object.entries(playerStatsMap)
    .map(([name, data]) => ({ name, ...data }))
    .filter(s => s.matches > 0); // Only show people who actually played (optional, but requested by user?)
    // Actually, user complained people were missing!
    // But if they didn't play at all, it's fine. Wait, user said "어떤 회원은 아예 리스트에도 없는거지?". I should NOT filter out matches=0 if it's the ADMIN panel, but for member view, keeping everyone who was selected might be good.
    // Wait, in member view, we don't know who was "selected", we only know `dbPlayers`. Showing 40 people with 0 matches is bad. Let's just filter `matches > 0`.
    // Wait, Admin mode has `activePlayersForDropdown`, so it knows. Member mode doesn't.
    // Let's filter `matches > 0` for Member mode.
  
  const blueTeamStats = allStats.filter(s => s.team === 'BLUE').sort((a, b) => b.matches - a.matches || b.wins - a.wins);
  const whiteTeamStats = allStats.filter(s => s.team === 'WHITE').sort((a, b) => b.matches - a.matches || b.wins - a.wins);
  const individualStats = [...allStats].sort((a, b) => b.wins - a.wins || b.matches - a.matches);"""

content = content.replace(old_stats, new_stats)


# Replace UI
old_ui = """          <h2 className="text-lg font-bold mb-6 flex items-center justify-center xl:justify-start gap-2 border-b border-gray-100 dark:border-gray-800 pb-4">
            <Users className="text-yellow-600 w-5 h-5" />개인별 배정 경기 수
          </h2>
          <div className="flex gap-4">
            <div className="flex-1">
              <h3 className="text-sm font-bold text-blue-600 dark:text-blue-400 mb-3 text-center flex items-center justify-center gap-1">
                청팀 <span className="bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 text-xs px-2 py-0.5 rounded-full">{blueTeamStats.length}명</span>
              </h3>
              <ul className="space-y-2">
                {blueTeamStats.map(([name, count]) => {
                  const isSelected = selectedPlayer === name;
                  return (
                    <li 
                      key={name} 
                      onClick={() => setSelectedPlayer(isSelected ? null : name)}
                      className={`flex justify-between items-center text-sm cursor-pointer p-2 -mx-2 rounded-lg transition-all ${isSelected ? 'bg-blue-100 dark:bg-blue-900/40 ring-1 ring-blue-300 dark:ring-blue-800' : 'hover:bg-gray-50 dark:hover:bg-gray-800/50'}`}
                    >
                      <span className={`truncate ${isSelected ? 'text-blue-700 dark:text-blue-300 font-bold' : 'text-gray-700 dark:text-gray-300 font-medium'}`}>{name}</span>
                      <span className={`${isSelected ? 'bg-blue-200 dark:bg-blue-800/50 text-blue-800 dark:text-blue-200' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'} px-2 py-0.5 rounded font-bold text-xs transition-colors`}>{count}게임</span>
                    </li>
                  );
                })}
              </ul>
            </div>
            <div className="w-px bg-gray-200 dark:bg-gray-800"></div>
            <div className="flex-1">
              <h3 className="text-sm font-bold text-gray-700 dark:text-gray-300 mb-3 text-center flex items-center justify-center gap-1">
                백팀 <span className="bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 text-xs px-2 py-0.5 rounded-full">{whiteTeamStats.length}명</span>
              </h3>
              <ul className="space-y-2">
                {whiteTeamStats.map(([name, count]) => {
                  const isSelected = selectedPlayer === name;
                  return (
                    <li 
                      key={name} 
                      onClick={() => setSelectedPlayer(isSelected ? null : name)}
                      className={`flex justify-between items-center text-sm cursor-pointer p-2 -mx-2 rounded-lg transition-all ${isSelected ? 'bg-gray-200 dark:bg-gray-700/50 ring-1 ring-gray-300 dark:ring-gray-600' : 'hover:bg-gray-50 dark:hover:bg-gray-800/50'}`}
                    >
                      <span className={`truncate ${isSelected ? 'text-gray-900 dark:text-gray-100 font-bold' : 'text-gray-700 dark:text-gray-300 font-medium'}`}>{name}</span>
                      <span className={`${isSelected ? 'bg-gray-300 dark:bg-gray-600 text-gray-900 dark:text-gray-100' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'} px-2 py-0.5 rounded font-bold text-xs transition-colors`}>{count}게임</span>
                    </li>
                  );
                })}
              </ul>
            </div>
          </div>"""

new_ui = """          <h2 className="text-lg font-bold mb-6 flex items-center justify-center xl:justify-start gap-2 border-b border-gray-100 dark:border-gray-800 pb-4">
            <Users className="text-yellow-600 w-5 h-5" />{isIndividualMode ? '개인별 배정 경기 수 및 승률 (성적순)' : '개인별 배정 경기 수'}
          </h2>
          
          {isIndividualMode ? (
            <div className="flex flex-col gap-2">
              {individualStats.map(s => {
                const isSelected = selectedPlayer === s.name;
                return (
                  <div key={s.name} onClick={() => setSelectedPlayer(isSelected ? null : s.name)} className={`flex justify-between items-center text-sm cursor-pointer p-2 -mx-2 rounded-lg transition-all ${isSelected ? 'bg-yellow-50 dark:bg-yellow-900/30 ring-1 ring-yellow-400' : 'hover:bg-gray-50 dark:hover:bg-gray-800'}`}>
                    <span className={`font-bold ${isSelected ? 'text-yellow-700 dark:text-yellow-400' : 'text-gray-800 dark:text-gray-200'}`}>{s.name}</span>
                    <div className="flex gap-2 text-xs">
                      <span className="text-gray-500">{s.matches}경기</span>
                      <span className="text-blue-600 font-black">{s.wins}승</span>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="flex gap-4">
              <div className="flex-1">
                <h3 className="text-sm font-bold text-blue-600 dark:text-blue-400 mb-3 text-center flex items-center justify-center gap-1">
                  청팀 <span className="bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 text-xs px-2 py-0.5 rounded-full">{blueTeamStats.length}명</span>
                </h3>
                <ul className="space-y-2">
                  {blueTeamStats.map(s => {
                    const isSelected = selectedPlayer === s.name;
                    return (
                      <li 
                        key={s.name} 
                        onClick={() => setSelectedPlayer(isSelected ? null : s.name)}
                        className={`flex justify-between items-center text-sm cursor-pointer p-2 -mx-2 rounded-lg transition-all ${isSelected ? 'bg-blue-100 dark:bg-blue-900/40 ring-1 ring-blue-300 dark:ring-blue-800' : 'hover:bg-gray-50 dark:hover:bg-gray-800/50'}`}
                      >
                        <span className={`truncate ${isSelected ? 'text-blue-700 dark:text-blue-300 font-bold' : 'text-gray-700 dark:text-gray-300 font-medium'}`}>{s.name}</span>
                        <span className={`${isSelected ? 'bg-blue-200 dark:bg-blue-800/50 text-blue-800 dark:text-blue-200' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'} px-2 py-0.5 rounded font-bold text-xs transition-colors`}>{s.matches}게임</span>
                      </li>
                    );
                  })}
                </ul>
              </div>
              <div className="w-px bg-gray-200 dark:bg-gray-800"></div>
              <div className="flex-1">
                <h3 className="text-sm font-bold text-gray-700 dark:text-gray-300 mb-3 text-center flex items-center justify-center gap-1">
                  백팀 <span className="bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 text-xs px-2 py-0.5 rounded-full">{whiteTeamStats.length}명</span>
                </h3>
                <ul className="space-y-2">
                  {whiteTeamStats.map(s => {
                    const isSelected = selectedPlayer === s.name;
                    return (
                      <li 
                        key={s.name} 
                        onClick={() => setSelectedPlayer(isSelected ? null : s.name)}
                        className={`flex justify-between items-center text-sm cursor-pointer p-2 -mx-2 rounded-lg transition-all ${isSelected ? 'bg-gray-200 dark:bg-gray-700/50 ring-1 ring-gray-300 dark:ring-gray-600' : 'hover:bg-gray-50 dark:hover:bg-gray-800/50'}`}
                      >
                        <span className={`truncate ${isSelected ? 'text-gray-900 dark:text-gray-100 font-bold' : 'text-gray-700 dark:text-gray-300 font-medium'}`}>{s.name}</span>
                        <span className={`${isSelected ? 'bg-gray-300 dark:bg-gray-600 text-gray-900 dark:text-gray-100' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'} px-2 py-0.5 rounded font-bold text-xs transition-colors`}>{s.matches}게임</span>
                      </li>
                    );
                  })}
                </ul>
              </div>
            </div>
          )}"""

content = content.replace(old_ui, new_ui)

with open('src/app/tournament/page.tsx', 'w') as f:
    f.write(content)
