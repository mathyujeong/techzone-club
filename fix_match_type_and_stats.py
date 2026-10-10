import re

# 1. Update src/app/admin/page.tsx
with open('src/app/admin/page.tsx', 'r') as f:
    admin = f.read()

# Update saveTournament to update match_type in tournaments table
old_save_tournament_start = """  const saveTournament = async () => {
    if (!selectedTournamentId) {
      alert("선택된 대회가 없습니다. 왼쪽 메뉴에서 대회를 먼저 선택하거나 '새 대회 추가'를 눌러주세요.");
      return;
    }"""

new_save_tournament_start = """  const saveTournament = async () => {
    if (!selectedTournamentId) {
      alert("선택된 대회가 없습니다. 왼쪽 메뉴에서 대회를 먼저 선택하거나 '새 대회 추가'를 눌러주세요.");
      return;
    }

    // Save match_type to the tournament in Supabase
    await supabase.from('tournaments').update({ match_type: matchType }).eq('id', selectedTournamentId);
    setTournaments(tournaments.map(t => t.id === selectedTournamentId ? { ...t, match_type: matchType } : t));"""

admin = admin.replace(old_save_tournament_start, new_save_tournament_start)

# Update Admin Stats calculation for Wins and Losses
old_admin_stats_calc = """  const playerStatsMap: Record<string, { matches: number, wins: number, team: 'BLUE' | 'WHITE' | 'MIXED' }> = {};
  dbPlayers.forEach(p => {
    playerStatsMap[p.name] = { matches: 0, wins: 0, team: 'MIXED' }; // initialize everyone
  });
  
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

new_admin_stats_calc = """  const playerStatsMap: Record<string, { matches: number, wins: number, losses: number, team: 'BLUE' | 'WHITE' | 'MIXED' }> = {};
  dbPlayers.forEach(p => {
    playerStatsMap[p.name] = { matches: 0, wins: 0, losses: 0, team: 'MIXED' };
  });
  
  currentMatches.forEach(m => {
    const isCompleted = m.status === 'completed';
    const blueWon = isCompleted && m.blue_score > m.white_score;
    const whiteWon = isCompleted && m.white_score > m.blue_score;
    
    const addStat = (pName: string, isBlue: boolean) => {
      if (!pName) return;
      if (!playerStatsMap[pName]) playerStatsMap[pName] = { matches: 0, wins: 0, losses: 0, team: isBlue ? 'BLUE' : 'WHITE' };
      
      playerStatsMap[pName].matches++;
      if (playerStatsMap[pName].team !== (isBlue ? 'BLUE' : 'WHITE')) {
        playerStatsMap[pName].team = 'MIXED';
      }
      
      if (isCompleted) {
        if ((isBlue && blueWon) || (!isBlue && whiteWon)) {
          playerStatsMap[pName].wins++;
        } else if ((isBlue && whiteWon) || (!isBlue && blueWon)) {
          playerStatsMap[pName].losses++;
        }
      }
    };

    addStat(m.blue_player1, true);
    addStat(m.blue_player2, true);
    addStat(m.white_player1, false);
    addStat(m.white_player2, false);
  });

  const allStats = Object.entries(playerStatsMap).map(([name, data]) => ({ name, ...data }));
  
  const blueTeamStats = allStats.filter(s => s.team === 'BLUE').sort((a, b) => b.matches - a.matches || b.wins - a.wins);
  const whiteTeamStats = allStats.filter(s => s.team === 'WHITE').sort((a, b) => b.matches - a.matches || b.wins - a.wins);
  const individualStats = [...allStats].sort((a, b) => b.wins - a.wins || a.losses - b.losses || b.matches - a.matches);"""

admin = admin.replace(old_admin_stats_calc, new_admin_stats_calc)

# Update Admin Stats UI to show ~승 ~패
old_admin_stats_ui = """          {isIndividualMode ? (
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
          ) : ("""

new_admin_stats_ui = """          {isIndividualMode ? (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
              {individualStats.map(s => (
                <div key={s.name} className="bg-gray-50 border border-gray-200 text-gray-800 p-3 rounded-2xl text-sm dark:bg-gray-800 dark:border-gray-700 dark:text-gray-200 flex flex-col items-center justify-between shadow-sm hover:border-yellow-400 transition-colors">
                  <span className="font-black text-base mb-1">{s.name}</span>
                  <div className="flex items-center gap-1.5 text-xs">
                    <span className="text-blue-600 font-black">{s.wins}승</span>
                    <span className="text-gray-300 dark:text-gray-600">•</span>
                    <span className="text-red-500 font-black">{s.losses}패</span>
                  </div>
                  <span className="text-[10px] text-gray-400 font-bold mt-1">총 {s.matches}경기</span>
                </div>
              ))}
            </div>
          ) : ("""

admin = admin.replace(old_admin_stats_ui, new_admin_stats_ui)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(admin)

# 2. Update src/app/tournament/page.tsx
with open('src/app/tournament/page.tsx', 'r') as f:
    member = f.read()

# Update Member Stats Calculation
old_member_stats_calc = """  // 선수별 통계
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
    .map(([name, data]) => ({ name, ...data }));
  
  const blueTeamStats = allStats.filter(s => s.team === 'BLUE').sort((a, b) => b.matches - a.matches || b.wins - a.wins);
  const whiteTeamStats = allStats.filter(s => s.team === 'WHITE').sort((a, b) => b.matches - a.matches || b.wins - a.wins);
  const individualStats = [...allStats].sort((a, b) => b.wins - a.wins || b.matches - a.matches);"""

new_member_stats_calc = """  // 선수별 통계
  const isIndividualMode = activeTournament?.match_type === 'INDIVIDUAL';
  const playerStatsMap: Record<string, { matches: number, wins: number, losses: number, team: 'BLUE' | 'WHITE' | 'MIXED' }> = {};
  
  dbPlayers.forEach(p => {
    playerStatsMap[p.name] = { matches: 0, wins: 0, losses: 0, team: 'MIXED' };
  });

  matches.forEach(m => {
    const isCompleted = m.status === 'completed';
    const blueWon = isCompleted && m.blue_score > m.white_score;
    const whiteWon = isCompleted && m.white_score > m.blue_score;
    
    const addStat = (pName: string, isBlue: boolean) => {
      if (!pName) return;
      if (!playerStatsMap[pName]) playerStatsMap[pName] = { matches: 0, wins: 0, losses: 0, team: isBlue ? 'BLUE' : 'WHITE' };
      
      playerStatsMap[pName].matches++;
      if (playerStatsMap[pName].team !== (isBlue ? 'BLUE' : 'WHITE')) {
        playerStatsMap[pName].team = 'MIXED';
      }
      
      if (isCompleted) {
        if ((isBlue && blueWon) || (!isBlue && whiteWon)) {
          playerStatsMap[pName].wins++;
        } else if ((isBlue && whiteWon) || (!isBlue && blueWon)) {
          playerStatsMap[pName].losses++;
        }
      }
    };

    addStat(String(m.blue_player1), true);
    addStat(String(m.blue_player2), true);
    addStat(String(m.white_player1), false);
    addStat(String(m.white_player2), false);
  });

  const allStats = Object.entries(playerStatsMap)
    .map(([name, data]) => ({ name, ...data }));
  
  const blueTeamStats = allStats.filter(s => s.team === 'BLUE').sort((a, b) => b.matches - a.matches || b.wins - a.wins);
  const whiteTeamStats = allStats.filter(s => s.team === 'WHITE').sort((a, b) => b.matches - a.matches || b.wins - a.wins);
  const individualStats = [...allStats].sort((a, b) => b.wins - a.wins || a.losses - b.losses || b.matches - a.matches);"""

member = member.replace(old_member_stats_calc, new_member_stats_calc)

# Update Member Live Scoreboard (Hide 청팀 vs 백팀 scoreboard if INDIVIDUAL)
old_member_scoreboard = """        {/* 상단 스코어 보드 */}
        <div className="flex justify-center items-center gap-4 md:gap-12 mb-6 max-w-2xl mx-auto bg-white dark:bg-gray-900 rounded-[2rem] p-8 shadow-xl border-4 border-gray-50 dark:border-gray-800">
          <div className="flex-1 text-center">
            <h2 className="text-lg md:text-xl font-bold text-blue-600 dark:text-blue-400 mb-2">청팀</h2>
            <div className="text-6xl md:text-8xl font-black text-blue-600 dark:text-blue-400 tracking-tighter">{totalBlueWins}</div>
          </div>
          
          <div className="text-gray-300 dark:text-gray-700 font-black text-3xl md:text-5xl italic px-4">VS</div>
          
          <div className="flex-1 text-center">
            <h2 className="text-lg md:text-xl font-bold text-gray-800 dark:text-gray-200 mb-2">백팀</h2>
            <div className="text-6xl md:text-8xl font-black text-gray-800 dark:text-gray-200 tracking-tighter">{totalWhiteWins}</div>
          </div>
        </div>
        
        <p className="text-gray-500 dark:text-gray-400 font-bold text-sm tracking-widest uppercase">Live Scoreboard</p>"""

new_member_scoreboard = """        {/* 상단 스코어 보드 */}
        {!isIndividualMode ? (
          <>
            <div className="flex justify-center items-center gap-4 md:gap-12 mb-6 max-w-2xl mx-auto bg-white dark:bg-gray-900 rounded-[2rem] p-8 shadow-xl border-4 border-gray-50 dark:border-gray-800">
              <div className="flex-1 text-center">
                <h2 className="text-lg md:text-xl font-bold text-blue-600 dark:text-blue-400 mb-2">청팀</h2>
                <div className="text-6xl md:text-8xl font-black text-blue-600 dark:text-blue-400 tracking-tighter">{totalBlueWins}</div>
              </div>
              
              <div className="text-gray-300 dark:text-gray-700 font-black text-3xl md:text-5xl italic px-4">VS</div>
              
              <div className="flex-1 text-center">
                <h2 className="text-lg md:text-xl font-bold text-gray-800 dark:text-gray-200 mb-2">백팀</h2>
                <div className="text-6xl md:text-8xl font-black text-gray-800 dark:text-gray-200 tracking-tighter">{totalWhiteWins}</div>
              </div>
            </div>
            <p className="text-gray-500 dark:text-gray-400 font-bold text-sm tracking-widest uppercase">Live Scoreboard</p>
          </>
        ) : (
          <div className="bg-white dark:bg-gray-900 rounded-3xl p-6 shadow-xl border-4 border-gray-50 dark:border-gray-800 max-w-md mx-auto mb-6 flex flex-col items-center">
            <span className="text-xs font-black text-yellow-600 dark:text-yellow-500 uppercase tracking-widest mb-1">Individual Matches</span>
            <h2 className="text-xl font-black text-gray-900 dark:text-gray-100">🏆 개인전 실시간 진행 현황</h2>
            <div className="mt-3 flex items-center gap-3 text-sm font-bold text-gray-600 dark:text-gray-300">
              <span>완료된 경기: <strong className="text-blue-600 font-black text-base">{matches.filter(m => m.status === 'completed').length}</strong> / {matches.length}</span>
            </div>
          </div>
        )}"""

member = member.replace(old_member_scoreboard, new_member_scoreboard)

# Update Member Stats UI to show ~승 ~패 in a single box layout
old_member_stats_ui = """          {isIndividualMode ? (
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
          ) : ("""

new_member_stats_ui = """          {isIndividualMode ? (
            <div className="flex flex-col gap-2">
              {individualStats.map(s => {
                const isSelected = selectedPlayer === s.name;
                return (
                  <div key={s.name} onClick={() => setSelectedPlayer(isSelected ? null : s.name)} className={`flex justify-between items-center text-sm cursor-pointer p-2.5 rounded-xl transition-all ${isSelected ? 'bg-yellow-50 dark:bg-yellow-900/30 ring-2 ring-yellow-500 shadow-sm' : 'bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800'}`}>
                    <span className={`font-bold text-base ${isSelected ? 'text-yellow-700 dark:text-yellow-400' : 'text-gray-800 dark:text-gray-200'}`}>{s.name}</span>
                    <div className="flex items-center gap-2 text-xs">
                      <span className="text-blue-600 font-black text-sm">{s.wins}승</span>
                      <span className="text-gray-300 dark:text-gray-600">•</span>
                      <span className="text-red-500 font-black text-sm">{s.losses}패</span>
                      <span className="text-gray-400 text-[10px] ml-1">({s.matches}경기)</span>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : ("""

member = member.replace(old_member_stats_ui, new_member_stats_ui)

with open('src/app/tournament/page.tsx', 'w') as f:
    f.write(member)

