import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Add executeDelete function
execute_func = """  const executeDelete = async () => {
    if (deleteCode !== '0000') {
      alert('코드가 일치하지 않습니다.');
      return;
    }
    if (deleteConfirm?.type === 'tournament') {
      await supabase.from('tournaments').delete().eq('id', deleteConfirm.id);
      setTournaments(tournaments.filter(t => t.id !== deleteConfirm.id));
      if (selectedTournamentId === deleteConfirm.id) setSelectedTournamentId(null);
      setEditingTournamentId(null);
    } else if (deleteConfirm?.type === 'match') {
      setMatches(matches.filter(m => m.id !== deleteConfirm.id));
      await supabase.from('matches').delete().eq('id', deleteConfirm.id);
      setEditMatchModal(null);
      fetchPlayersAndTournaments();
    }
    setDeleteConfirm(null);
  };"""
content = content.replace("  const deleteTournament = async (id: string) => {", execute_func + "\n\n  const deleteTournament = async (id: string) => {")

# 2. Modify deleteTournament
old_dt = """  const deleteTournament = async (id: string) => {
    const code = prompt('이 대회와 모든 하위 경기가 삭제됩니다. 삭제하려면 0000 을 입력하세요.');
    if (code === '0000') {
      await supabase.from('tournaments').delete().eq('id', id);
      setTournaments(tournaments.filter(t => t.id !== id));
      if (selectedTournamentId === id) setSelectedTournamentId(null);
      setEditingTournamentId(null);
    } else if (code !== null) {
      alert('입력한 코드가 틀렸습니다.');
    }
  };"""
new_dt = """  const deleteTournament = (id: string) => {
    setDeleteCode("");
    setDeleteConfirm({ type: 'tournament', id });
  };"""
content = content.replace(old_dt, new_dt)

# 3. Modify deleteMatch
old_dm = """  async function deleteMatch(id: string) {
    const code = prompt('이 경기를 완전히 삭제하려면 0000 을 입력하세요.');
    if (code === '0000') {
      setMatches(matches.filter(m => m.id !== id));
      await supabase.from('matches').delete().eq('id', id);
      setEditMatchModal(null);
    } else if (code !== null) {
      alert('입력한 코드가 틀렸습니다.');
    }
  }"""
new_dm = """  const deleteMatch = (id: string) => {
    setDeleteCode("");
    setDeleteConfirm({ type: 'match', id });
  };"""
content = content.replace(old_dm, new_dm)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
