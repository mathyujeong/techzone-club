with open('src/app/tournament/page.tsx', 'r') as f:
    content = f.read()

# Replace fetchMatches logic
old_fetch = """  async function fetchMatches() {
    const { data, error } = await supabase
      .from('matches')
      .select('*')
      .order('round_num', { ascending: true })
      .order('court_num', { ascending: true });
    
    if (data) setMatches(data);
    setLoading(false);
  }"""

new_fetch = """  const [activeTournament, setActiveTournament] = useState<any>(null);

  async function fetchMatches() {
    // 1. Get the most recently active tournament (or just the latest one)
    const { data: tData } = await supabase
      .from('tournaments')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(1)
      .single();
      
    if (tData) {
      setActiveTournament(tData);
      
      // 2. Fetch matches ONLY for this tournament
      const { data, error } = await supabase
        .from('matches')
        .select('*')
        .eq('tournament_id', tData.id)
        .order('round_num', { ascending: true })
        .order('court_num', { ascending: true });
        
      if (data) setMatches(data);
    }
    setLoading(false);
  }"""

content = content.replace(old_fetch, new_fetch)

# Update Header title
old_header = """<h1 className="text-2xl md:text-3xl font-black mb-2 flex items-center justify-center gap-2">
            <Trophy className="text-yellow-400" />
            실시간 점수 및 대진표
          </h1>
          <p className="text-gray-300 text-sm md:text-base">현재 진행 중인 경기의 실시간 결과를 확인하세요.</p>"""

new_header = """<h1 className="text-2xl md:text-3xl font-black mb-2 flex items-center justify-center gap-2">
            <Trophy className="text-yellow-400" />
            {activeTournament ? activeTournament.title : '실시간 점수 및 대진표'}
          </h1>
          <p className="text-gray-300 text-sm md:text-base">현재 진행 중인 대회의 실시간 결과를 확인하세요.</p>"""
content = content.replace(old_header, new_header)


# Make sure the UI cards are responsive as well
old_blue_card = """                    <div className={`p-3 flex justify-between items-center border-b border-gray-100 dark:border-gray-800 flex-1 ${m.status === 'completed' && m.blue_score > m.white_score ? 'bg-blue-50 dark:bg-blue-900/30' : ''}`}>
                      <div className="font-bold text-sm text-blue-700 dark:text-blue-400">
                        <div>{m.blue_player1}</div>
                        <div>{m.blue_player2}</div>
                      </div>
                      <div className={`font-black text-2xl ${m.status === 'completed' && m.blue_score > m.white_score ? 'text-blue-600' : 'text-gray-300 dark:text-gray-600'}`}>
                        {m.blue_score}
                      </div>
                    </div>"""
new_blue_card = """                    <div className={`p-3 flex justify-between items-center border-b border-gray-100 dark:border-gray-800 flex-1 min-w-0 ${m.status === 'completed' && m.blue_score > m.white_score ? 'bg-blue-50 dark:bg-blue-900/30' : ''}`}>
                      <div className="font-black text-base md:text-lg text-blue-700 dark:text-blue-400 flex flex-col justify-center min-w-0 pr-2 w-full">
                        <div className="truncate w-full">{m.blue_player1}</div>
                        <div className="truncate w-full">{m.blue_player2}</div>
                      </div>
                      <div className={`font-black text-2xl shrink-0 ${m.status === 'completed' && m.blue_score > m.white_score ? 'text-blue-600' : 'text-gray-300 dark:text-gray-600'}`}>
                        {m.blue_score}
                      </div>
                    </div>"""
content = content.replace(old_blue_card, new_blue_card)


old_white_card = """                    <div className={`p-3 flex justify-between items-center flex-1 ${m.status === 'completed' && m.white_score > m.blue_score ? 'bg-gray-100 dark:bg-gray-800' : ''}`}>
                      <div className="font-bold text-sm text-gray-700 dark:text-gray-300">
                        <div>{m.white_player1}</div>
                        <div>{m.white_player2}</div>
                      </div>
                      <div className={`font-black text-2xl ${m.status === 'completed' && m.white_score > m.blue_score ? 'text-gray-600 dark:text-gray-400' : 'text-gray-300 dark:text-gray-600'}`}>
                        {m.white_score}
                      </div>
                    </div>"""
new_white_card = """                    <div className={`p-3 flex justify-between items-center flex-1 min-w-0 ${m.status === 'completed' && m.white_score > m.blue_score ? 'bg-gray-100 dark:bg-gray-800' : ''}`}>
                      <div className="font-black text-base md:text-lg text-gray-700 dark:text-gray-300 flex flex-col justify-center min-w-0 pr-2 w-full">
                        <div className="truncate w-full">{m.white_player1}</div>
                        <div className="truncate w-full">{m.white_player2}</div>
                      </div>
                      <div className={`font-black text-2xl shrink-0 ${m.status === 'completed' && m.white_score > m.blue_score ? 'text-gray-600 dark:text-gray-400' : 'text-gray-300 dark:text-gray-600'}`}>
                        {m.white_score}
                      </div>
                    </div>"""
content = content.replace(old_white_card, new_white_card)

# Change grid from 2 columns to responsive 1->2->3->4
old_grid = """<div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">"""
new_grid = """<div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">"""
content = content.replace(old_grid, new_grid)


with open('src/app/tournament/page.tsx', 'w') as f:
    f.write(content)
