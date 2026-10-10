import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Add toggleMatchType function
old_place = "const saveTournament = async () => {"
new_func = """  const toggleMatchType = async (newType: 'TEAM' | 'INDIVIDUAL') => {
    if (!selectedTournamentId) return;
    await supabase.from('tournaments').update({ match_type: newType }).eq('id', selectedTournamentId);
    setTournaments(tournaments.map(t => t.id === selectedTournamentId ? { ...t, match_type: newType } : t));
  };

  const saveTournament = async () => {"""
content = content.replace(old_place, new_func)

# 2. Add Toggle UI to Stats Panel Header
old_stats_header = """          <h2 className="text-lg font-bold mb-6 flex items-center gap-2 border-b border-gray-100 dark:border-gray-800 pb-4">
            <Users className="text-yellow-600 w-5 h-5" />
            {isIndividualMode ? '개인별 배정 경기 수 및 승률 (성적순)' : '팀 구성 및 선수별 배정 경기 수'}
          </h2>"""

new_stats_header = """          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6 border-b border-gray-100 dark:border-gray-800 pb-4">
            <h2 className="text-lg font-bold flex items-center gap-2">
              <Users className="text-yellow-600 w-5 h-5" />
              {isIndividualMode ? '개인별 배정 경기 수 및 승률 (성적순)' : '팀 구성 및 선수별 배정 경기 수'}
            </h2>
            
            <div className="flex bg-gray-100 dark:bg-gray-800 p-1 rounded-xl text-xs font-bold self-end sm:self-auto shadow-inner">
              <button 
                onClick={() => toggleMatchType('TEAM')} 
                className={`px-3 py-1.5 rounded-lg transition-all ${!isIndividualMode ? 'bg-white dark:bg-gray-700 text-blue-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
              >
                청백전 (팀전)
              </button>
              <button 
                onClick={() => toggleMatchType('INDIVIDUAL')} 
                className={`px-3 py-1.5 rounded-lg transition-all ${isIndividualMode ? 'bg-white dark:bg-gray-700 text-yellow-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
              >
                개인전 (랜덤 매치)
              </button>
            </div>
          </div>"""

content = content.replace(old_stats_header, new_stats_header)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
