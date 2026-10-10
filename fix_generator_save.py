import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

old_save = """  const saveTournament = async () => {
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
      blue_score: 0,
      white_score: 0,
      status: 'pending'
    }));

    await supabase.from('matches').insert(matchInserts);
    setIsGeneratorModalOpen(false);
    fetchPlayersAndTournaments();
  };"""

new_save = """  const saveTournament = async () => {
    if (!selectedTournamentId) {
      alert("선택된 대회가 없습니다. 왼쪽 메뉴에서 대회를 먼저 선택하거나 '새 대회 추가'를 눌러주세요.");
      return;
    }

    const currentTournamentMatches = matches.filter(m => m.tournament_id === selectedTournamentId);
    let maxRound = 0;
    if (currentTournamentMatches.length > 0) {
      maxRound = Math.max(...currentTournamentMatches.map(m => m.round_num));
    }

    const matchInserts = generatedBracket.map((m, i) => {
      const generatedRound = m.round_num || Math.floor(i / numCourts) + 1;
      return {
        tournament_id: selectedTournamentId,
        round_num: generatedRound + maxRound,
        court_num: m.court_num || (i % numCourts) + 1,
        match_type: m.match_type + ':0:0',
        blue_player1: m.blue_team[0].name,
        blue_player2: m.blue_team[1].name,
        white_player1: m.white_team[0].name,
        white_player2: m.white_team[1].name,
        blue_score: 0,
        white_score: 0,
        status: 'pending'
      };
    });

    await supabase.from('matches').insert(matchInserts);
    setIsGeneratorModalOpen(false);
    fetchPlayersAndTournaments();
  };"""

content = content.replace(old_save, new_save)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
