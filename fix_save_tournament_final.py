import sys

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

start_token = "  const saveTournament = async () => {"
end_token = "    alert('새 대진표가 성공적으로 적용되었습니다!');\n  };"

start_idx = content.find(start_token)
end_idx = content.find(end_token)

if start_idx == -1 or end_idx == -1:
    print("Tokens not found!")
    sys.exit(1)

# Include the end_token's length
end_idx += len(end_token)

new_func = """  const saveTournament = async () => {
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
    await fetchMatches();
    alert('새 대진표가 성공적으로 적용되었습니다!');
  };"""

content = content[:start_idx] + new_func + content[end_idx:]

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)

print("Replaced successfully!")
