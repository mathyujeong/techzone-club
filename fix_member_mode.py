import re

with open('src/app/tournament/page.tsx', 'r') as f:
    content = f.read()

# 1. Add states
content = content.replace("const [selectedPlayer, setSelectedPlayer] = useState<string | null>(null);", 
"""const [selectedPlayer, setSelectedPlayer] = useState<string | null>(null);
  const [dbPlayers, setDbPlayers] = useState<any[]>([]);
  const [showGrades, setShowGrades] = useState(false);
  
  const getPlayerGrade = (name: string) => {
    const p = dbPlayers.find(player => player.name === name);
    return p ? p.grade : '';
  };""")

# 2. Add players fetch to fetchAllData
fetch_logic = """  async function fetchAllData() {
    const { data: tData } = await supabase
      .from('tournaments')
      .select('*')
      .order('created_at', { ascending: false });

    if (tData) {
      setTournaments(tData);
      if (tData.length > 0) {
        setActiveTournament(tData[0]);
        fetchMatches(tData[0].id);
      } else {
        setLoading(false);
      }
    }
  }"""
new_fetch_logic = """  async function fetchAllData() {
    const { data: pData } = await supabase.from('players').select('*');
    if (pData) setDbPlayers(pData);

    const { data: tData } = await supabase
      .from('tournaments')
      .select('*')
      .order('created_at', { ascending: false });

    if (tData) {
      setTournaments(tData);
      if (tData.length > 0) {
        setActiveTournament(tData[0]);
        fetchMatches(tData[0].id);
      } else {
        setLoading(false);
      }
    }
  }"""
content = content.replace(fetch_logic, new_fetch_logic)

# 3. Add the toggle UI next to the Select Dropdown
old_dropdown = """          {tournaments.length > 1 && (
            <div className="relative w-full max-w-xl mx-auto mb-10">
              <select 
                className="w-full appearance-none bg-white/90 dark:bg-gray-900/90 text-gray-900 dark:text-gray-100 font-black text-xl md:text-3xl text-center py-4 px-12 rounded-3xl border-4 border-yellow-500/30 hover:border-yellow-500 transition-colors shadow-2xl cursor-pointer"
                value={activeTournament?.id || ''}
                onChange={(e) => {
                  const t = tournaments.find(t => t.id === e.target.value);
                  if (t) {
                    setActiveTournament(t);
                    fetchMatches(t.id);
                  }
                }}
              >
                {tournaments.map(t => (
                  <option key={t.id} value={t.id}>{t.title}</option>
                ))}
              </select>
              <div className="absolute inset-y-0 right-4 flex items-center pointer-events-none">
                <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M19 9l-7 7-7-7" /></svg>
              </div>
            </div>
          )}"""

new_dropdown = """          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 w-full max-w-2xl mx-auto mb-10">
            {tournaments.length > 1 && (
              <div className="relative w-full">
                <select 
                  className="w-full appearance-none bg-white/90 dark:bg-gray-900/90 text-gray-900 dark:text-gray-100 font-black text-xl md:text-2xl text-center py-4 px-12 rounded-2xl border-4 border-yellow-500/30 hover:border-yellow-500 transition-colors shadow-xl cursor-pointer"
                  value={activeTournament?.id || ''}
                  onChange={(e) => {
                    const t = tournaments.find(t => t.id === e.target.value);
                    if (t) {
                      setActiveTournament(t);
                      fetchMatches(t.id);
                    }
                  }}
                >
                  {tournaments.map(t => (
                    <option key={t.id} value={t.id}>{t.title}</option>
                  ))}
                </select>
                <div className="absolute inset-y-0 right-4 flex items-center pointer-events-none">
                  <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M19 9l-7 7-7-7" /></svg>
                </div>
              </div>
            )}
            
            <label className="flex items-center gap-2 text-sm font-bold text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 px-5 py-4 rounded-2xl shadow-xl border-4 border-gray-100 dark:border-gray-800 cursor-pointer whitespace-nowrap hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              <input type="checkbox" checked={showGrades} onChange={e => setShowGrades(e.target.checked)} className="w-5 h-5 rounded text-yellow-600 focus:ring-yellow-500 cursor-pointer" />
              급수 보기
            </label>
          </div>"""
content = content.replace(old_dropdown, new_dropdown)

# 4. Show grades on the match cards
content = content.replace(
    '<div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed">{match.blue_player1}</div>',
    '<div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed flex items-center gap-2"><span>{match.blue_player1}</span> {showGrades && <span className="text-[10px] font-black opacity-50 bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded">{getPlayerGrade(match.blue_player1)}</span>}</div>'
)
content = content.replace(
    '<div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed">{match.blue_player2}</div>',
    '<div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed flex items-center gap-2"><span>{match.blue_player2}</span> {showGrades && <span className="text-[10px] font-black opacity-50 bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded">{getPlayerGrade(match.blue_player2)}</span>}</div>'
)
content = content.replace(
    '<div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed">{match.white_player1}</div>',
    '<div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed flex items-center gap-2"><span>{match.white_player1}</span> {showGrades && <span className="text-[10px] font-black opacity-50 bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded">{getPlayerGrade(match.white_player1)}</span>}</div>'
)
content = content.replace(
    '<div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed">{match.white_player2}</div>',
    '<div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed flex items-center gap-2"><span>{match.white_player2}</span> {showGrades && <span className="text-[10px] font-black opacity-50 bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded">{getPlayerGrade(match.white_player2)}</span>}</div>'
)


with open('src/app/tournament/page.tsx', 'w') as f:
    f.write(content)
