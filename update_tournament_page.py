with open('src/app/tournament/page.tsx', 'r') as f:
    content = f.read()

# 1. State for tournaments list
old_states = """  const [matches, setMatches] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPlayer, setSelectedPlayer] = useState<string | null>(null);

  const [activeTournament, setActiveTournament] = useState<any>(null);"""

new_states = """  const [tournaments, setTournaments] = useState<any[]>([]);
  const [activeTournament, setActiveTournament] = useState<any>(null);
  const [matches, setMatches] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPlayer, setSelectedPlayer] = useState<string | null>(null);"""
content = content.replace(old_states, new_states)

# 2. Fetch logic
old_fetch = """  async function fetchMatches() {
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
  }

  useEffect(() => {
    fetchMatches();

    // 실시간 점수 반영 구독
    const subscription = supabase
      .channel('matches_changes')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'matches' }, payload => {
        fetchMatches(); // 데이터가 변경되면 즉시 다시 불러오기
      })
      .subscribe();

    return () => {
      supabase.removeChannel(subscription);
    };
  }, []);"""

new_fetch = """  async function fetchAllData() {
    const { data: tData } = await supabase
      .from('tournaments')
      .select('*')
      .order('created_at', { ascending: false });
      
    if (tData && tData.length > 0) {
      setTournaments(tData);
      if (!activeTournament) {
        setActiveTournament(tData[0]);
        fetchMatches(tData[0].id);
      }
    } else {
      setLoading(false);
    }
  }

  async function fetchMatches(tournamentId: string) {
    setLoading(true);
    const { data, error } = await supabase
      .from('matches')
      .select('*')
      .eq('tournament_id', tournamentId)
      .order('round_num', { ascending: true })
      .order('court_num', { ascending: true });
      
    if (data) setMatches(data);
    setLoading(false);
  }

  const handleTournamentChange = (id: string) => {
    const t = tournaments.find(x => x.id === id);
    if (t) {
      setActiveTournament(t);
      setSelectedPlayer(null); // Reset player filter on tournament change
      fetchMatches(t.id);
    }
  };

  useEffect(() => {
    fetchAllData();

    const subscription = supabase
      .channel('matches_changes')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'matches' }, payload => {
        if (activeTournament) fetchMatches(activeTournament.id);
      })
      .subscribe();

    return () => {
      supabase.removeChannel(subscription);
    };
  }, [activeTournament?.id]);"""
content = content.replace(old_fetch, new_fetch)


# 3. Header UI
old_header = """      <div className="mb-12 text-center">
        <h1 className="text-3xl md:text-4xl font-black flex items-center justify-center gap-3 mb-8">
          <Trophy className="w-10 h-10 text-yellow-500" />
          제 1회 월례회 대진표
        </h1>"""

new_header = """      <div className="mb-12 text-center">
        <div className="flex flex-col items-center justify-center mb-8 space-y-4">
          <div className="flex items-center justify-center gap-3">
            <Trophy className="w-10 h-10 text-yellow-500" />
            <h1 className="text-3xl md:text-4xl font-black">
              대진표 및 실시간 점수
            </h1>
          </div>
          
          {tournaments.length > 0 && (
            <div className="relative inline-block w-full max-w-xs mt-4">
              <select 
                value={activeTournament?.id || ''} 
                onChange={(e) => handleTournamentChange(e.target.value)}
                className="w-full appearance-none bg-white dark:bg-gray-900 border-2 border-yellow-400 dark:border-yellow-600 rounded-2xl px-6 py-4 outline-none text-gray-900 dark:text-white focus:ring-4 focus:ring-yellow-500/20 transition-all font-bold text-center cursor-pointer shadow-md text-lg"
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
        </div>"""
content = content.replace(old_header, new_header)

with open('src/app/tournament/page.tsx', 'w') as f:
    f.write(content)
