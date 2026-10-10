import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

old_func = """  const saveTournament = async () => {
    const { data: tData, error: tErr } = await supabase.from('tournaments').insert({
      title: `${new Date().getMonth() + 1}월 월례회`,
      match_type: 'TEAM',
      display_mode: 'SCORE',
      status: 'IN_PROGRESS'
    }).select().single();

    if (tErr || !tData) return alert('대회 생성 실패!');

    const matchInserts = generatedBracket.map((m, i) => ({
      tournament_id: tData.id,
      round_num: m.round_num || Math.floor(i / numCourts) + 1,
      court_num: m.court_num || (i % numCourts) + 1,
      match_type: m.match_type + ':0:0',
      blue_player1: m.blue_team[0].name,
      blue_player2: m.blue_team[1].name,
      white_player1: m.white_team[0].name,
      white_player2: m.white_team[1].name,
      blue_handicap: m.blue_handicap,
      white_handicap: m.white_handicap
    }));

    const { error: mErr } = await supabase.from('matches').insert(matchInserts);
    if (mErr) return alert('경기 저장 실패!');

    setIsGeneratorModalOpen(false);
    fetchPlayersAndTournaments();
    setSelectedTournamentId(tData.id);
  };"""

new_func = """  const saveTournament = async () => {
    if (!selectedTournamentId) {
      alert('선택된 대회가 없습니다. 대회를 먼저 생성해주세요.');
      return;
    }

    const matchInserts = generatedBracket.map((m, i) => ({
      tournament_id: selectedTournamentId,
      round_num: m.round_num || Math.floor(i / numCourts) + 1,
      court_num: m.court_num || (i % numCourts) + 1,
      match_type: m.match_type + ':0:0',
      blue_player1: m.blue_team[0].name,
      blue_player2: m.blue_team[1].name,
      white_player1: m.white_team[0].name,
      white_player2: m.white_team[1].name,
      blue_handicap: m.blue_handicap,
      white_handicap: m.white_handicap
    }));

    const { error: mErr } = await supabase.from('matches').insert(matchInserts);
    if (mErr) return alert('경기 저장 실패!');

    setIsGeneratorModalOpen(false);
    fetchPlayersAndTournaments();
  };"""

content = content.replace(old_func, new_func)
with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
