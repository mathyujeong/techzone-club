import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# Replace the layout
# We will wrap the existing return statement inside a flex container.
# Currently, the return statement starts with:
# return (
#   <div className="min-h-screen bg-gray-50 dark:bg-gray-950 pb-20">

# We want to change the top level to have a sidebar.

sidebar_jsx = """
  const [selectedTournamentId, setSelectedTournamentId] = useState<string | null>(null);

  // set selected tournament when tournaments load
  useEffect(() => {
    if (tournaments.length > 0 && !selectedTournamentId) {
      // Find IN_PROGRESS first, otherwise first in list
      const active = tournaments.find(t => t.status === 'IN_PROGRESS') || tournaments[0];
      setSelectedTournamentId(active.id);
    }
  }, [tournaments]);

  const endTournament = async () => {
    if(!selectedTournamentId) return;
    if(confirm('정말로 이 대회를 최종 종료하시겠습니까? 종료 후에는 기록 보관소로 이동합니다.')) {
      await supabase.from('tournaments').update({ status: 'COMPLETED' }).eq('id', selectedTournamentId);
      setTournaments(tournaments.map(t => t.id === selectedTournamentId ? { ...t, status: 'COMPLETED' } : t));
      alert('대회가 종료되었습니다.');
    }
  };

  const currentMatches = matches.filter(m => m.tournament_id === selectedTournamentId);
  const activeTournament = tournaments.find(t => t.id === selectedTournamentId);

  // We need to override the matches logic for stats to only use currentMatches
  const playerStats: Record<string, number> = {};
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
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));

  const roundNums = Array.from(new Set(currentMatches.map(m => m.round_num))).sort((a, b) => a - b);
"""

# Find the stats generation block in original code:
stats_block_regex = r"const playerStats: Record<string, number> = \{\};\s*matches\.forEach\(m => \{.*?const roundNums = Array\.from\(new Set\(matches\.map\(m => m\.round_num\)\)\)\.sort\(\(a, b\) => a - b\);"
content = re.sub(stats_block_regex, sidebar_jsx, content, flags=re.DOTALL)

# Now for the return statement layout change:
# Find: return ( <div className="min-h-screen bg-gray-50 dark:bg-gray-950 pb-20">
# Replace with a wrapper that includes a sidebar

old_return_start = """  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 pb-20">"""

new_return_start = """  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex flex-col md:flex-row">
      {/* Sidebar */}
      <aside className="w-full md:w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col shrink-0">
        <div className="p-4 border-b border-gray-200 dark:border-gray-800">
          <h1 className="text-xl font-black flex items-center gap-2 mb-4">
            <Settings className="text-gray-400" />
            관리자 메뉴
          </h1>
          <button onClick={() => { setGeneratedBracket([]); setIsGeneratorModalOpen(true); }} className="w-full bg-blue-600 text-white px-4 py-3 rounded-xl font-bold text-sm flex justify-center items-center gap-2 hover:bg-blue-700 shadow-sm transition-colors">
            <RefreshCw className="w-4 h-4" /> 새 대회 생성
          </button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          <h2 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 ml-1">누적 대회 목록</h2>
          {tournaments.map(t => (
            <button 
              key={t.id}
              onClick={() => setSelectedTournamentId(t.id)}
              className={`w-full text-left p-3 rounded-xl transition-colors flex flex-col gap-1 ${selectedTournamentId === t.id ? 'bg-yellow-50 dark:bg-yellow-900/30 border border-yellow-200 dark:border-yellow-700/50' : 'hover:bg-gray-50 dark:hover:bg-gray-800 border border-transparent'}`}
            >
              <div className="flex items-center justify-between">
                <span className={`font-bold text-sm ${selectedTournamentId === t.id ? 'text-yellow-700 dark:text-yellow-400' : 'text-gray-700 dark:text-gray-300'}`}>{t.title}</span>
                <div className={`w-2 h-2 rounded-full ${t.status === 'IN_PROGRESS' ? 'bg-green-500' : 'bg-gray-300'}`} />
              </div>
              <span className="text-[10px] text-gray-400">{new Date(t.created_at).toLocaleDateString()}</span>
            </button>
          ))}
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto h-screen pb-20">"""

content = content.replace(old_return_start, new_return_start)

# Change header to remove the duplicate generator button and add End Tournament button
old_header = """      {/* 상단 헤더 */}
      <div className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-10 shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl md:text-2xl font-black flex items-center gap-2">
            <Settings className="text-gray-400" />
            점수 관리 보드
          </h1>
          <div className="flex gap-2">
            <button onClick={() => { setGeneratedBracket([]); setIsGeneratorModalOpen(true); }} className="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold text-sm flex items-center gap-1 hover:bg-blue-700 shadow-sm">
              <RefreshCw className="w-4 h-4" /> 새 대진표 자동생성
            </button>
            <button onClick={addMatch} className="bg-gray-900 dark:bg-gray-100 text-white dark:text-black px-4 py-2 rounded-lg font-bold text-sm flex items-center gap-1 hover:opacity-80">
              <Plus className="w-4 h-4" /> 빈 경기 추가
            </button>
          </div>
        </div>
      </div>"""

new_header = """      {/* 상단 헤더 */}
      <div className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-10 shadow-sm">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-xl md:text-2xl font-black flex items-center gap-2">
            <Trophy className="text-yellow-500" />
            {activeTournament?.title || '선택된 대회 없음'}
            {activeTournament?.status === 'COMPLETED' && <span className="text-xs bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-2 py-1 rounded-md flex items-center gap-1 ml-2"><Lock className="w-3 h-3"/> 종료됨</span>}
          </h1>
          <div className="flex gap-2">
            {activeTournament?.status === 'IN_PROGRESS' && (
              <button onClick={endTournament} className="bg-red-500 text-white px-4 py-2 rounded-lg font-bold text-sm flex items-center gap-1 hover:bg-red-600 shadow-sm">
                대회 최종 종료
              </button>
            )}
            <button onClick={addMatch} className="bg-gray-900 dark:bg-gray-100 text-white dark:text-black px-4 py-2 rounded-lg font-bold text-sm flex items-center gap-1 hover:opacity-80">
              <Plus className="w-4 h-4" /> 빈 경기 추가
            </button>
          </div>
        </div>
      </div>"""

content = content.replace(old_header, new_header)

# Ensure <main> gets closed before the modal.
# Modals are at the end of the file.
content = content.replace("    </div>\n  );\n}\n", "      </main>\n    </div>\n  );\n}\n")

# Finally, all `matches.filter` or `matches.length` inside the JSX needs to use `currentMatches`
# 1. matches.filter(m => (m.match_type || '').startsWith('MD')).length
# 2. matches.length
# 3. const roundMatches = matches.filter(m => m.round_num === roundNum);

content = content.replace("matches.filter(m => (m.match_type", "currentMatches.filter(m => (m.match_type")
content = content.replace("{matches.length}", "{currentMatches.length}")
content = content.replace("matches.filter(m => m.round_num === roundNum)", "currentMatches.filter(m => m.round_num === roundNum)")

# Add Lock to import
content = content.replace("import { Save, X }", "import { Save, X, Lock }")

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
