import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Add handleAddNewTournament
new_func = """  const handleAddNewTournament = async () => {
    const { data, error } = await supabase.from('tournaments').insert({ title: '새 월례회' }).select().single();
    if (data) {
      setTournaments([data, ...tournaments]);
      setSelectedTournamentId(data.id);
      setEditingTournamentId(data.id);
      setEditingTournamentName(data.title);
      setEditingTournamentDate(new Date(data.created_at).toISOString().split('T')[0]);
    } else {
      alert('대회 추가 실패: ' + (error?.message || ''));
    }
  };"""

content = content.replace("  // --- Tournament Renaming ---", new_func + "\n\n  // --- Tournament Renaming ---")

# 2. Change the sidebar button to call handleAddNewTournament
old_btn = """<button onClick={() => { setGeneratedBracket([]); setIsGeneratorModalOpen(true); }} className="w-full bg-blue-600 text-white px-4 py-3 rounded-xl font-bold text-sm flex justify-center items-center gap-2 hover:bg-blue-700 shadow-sm transition-colors">
            <RefreshCw className="w-4 h-4" /> 새 대회 추가
          </button>"""
new_btn = """<button onClick={handleAddNewTournament} className="w-full bg-blue-600 text-white px-4 py-3 rounded-xl font-bold text-sm flex justify-center items-center gap-2 hover:bg-blue-700 shadow-sm transition-colors">
            <RefreshCw className="w-4 h-4" /> 새 대회 추가
          </button>"""
content = content.replace(old_btn, new_btn)

# 3. Fix saveTournament to insert into selectedTournamentId instead of creating a new one
old_save = """  const saveTournament = async () => {
    const { data: tData, error: tError } = await supabase.from('tournaments').insert({ title: '새 월례회' }).select().single();
    if (tError || !tData) {
      alert('대회 생성 실패: ' + (tError?.message || ''));
      return;
    }
    
    const matchInserts = generatedBracket.map((m, i) => ({
      tournament_id: tData.id,
      round_num: m.round_num || Math.floor(i / numCourts) + 1,
      court_num: m.court_num || (i % numCourts) + 1,
      match_type: matchType + ':0:0', // Update match type format
      blue_player1: m.blue_team[0].name,
      blue_player2: m.blue_team[1].name,
      white_player1: m.white_team[0].name,
      white_player2: m.white_team[1].name,
      blue_handicap: m.blue_handicap,
      white_handicap: m.white_handicap
    }));

    const { error: mError } = await supabase.from('matches').insert(matchInserts);
    if (mError) {
      alert('경기 저장 실패: ' + mError.message);
      return;
    }

    setIsGeneratorModalOpen(false);
    fetchPlayersAndTournaments();
    setSelectedTournamentId(tData.id);
  };"""

new_save = """  const saveTournament = async () => {
    if (!selectedTournamentId) {
      alert('선택된 대회가 없습니다.');
      return;
    }
    
    const matchInserts = generatedBracket.map((m, i) => ({
      tournament_id: selectedTournamentId,
      round_num: m.round_num || Math.floor(i / numCourts) + 1,
      court_num: m.court_num || (i % numCourts) + 1,
      match_type: matchType + ':0:0',
      blue_player1: m.blue_team[0].name,
      blue_player2: m.blue_team[1].name,
      white_player1: m.white_team[0].name,
      white_player2: m.white_team[1].name,
      blue_handicap: m.blue_handicap,
      white_handicap: m.white_handicap
    }));

    const { error: mError } = await supabase.from('matches').insert(matchInserts);
    if (mError) {
      alert('경기 저장 실패: ' + mError.message);
      return;
    }

    setIsGeneratorModalOpen(false);
    fetchPlayersAndTournaments();
  };"""
content = content.replace(old_save, new_save)


# Wait! `matchType + ':0:0'` inside the old string might fail replacement if I already replaced something else. Let's do regex or replace a smaller chunk.
