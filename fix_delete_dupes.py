import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Remove duplicate Trash2 from line 9
content = content.replace("Edit2, UserPlus, CheckSquare, Square, Trash2", "Edit2, UserPlus, CheckSquare, Square")

# 2. Remove the duplicated deleteMatch function I just added
bad_delete_match = """  const deleteMatch = async (id: string) => {
    const code = prompt('이 경기를 삭제하려면 0000 을 입력하세요.');
    if (code === '0000') {
      await supabase.from('matches').delete().eq('id', id);
      setEditMatchModal(null);
      fetchPlayersAndTournaments();
    } else if (code !== null) {
      alert('입력한 코드가 틀렸습니다.');
    }
  };"""
content = content.replace(bad_delete_match, "")

# 3. Modify the original deleteMatch function
old_del = """  async function deleteMatch(id: string) {
    if (confirm("정말로 이 경기를 삭제하시겠습니까?")) {
      setMatches(matches.filter(m => m.id !== id));
      await supabase.from('matches').delete().eq('id', id);
    }
  }"""

new_del = """  async function deleteMatch(id: string) {
    const code = prompt('이 경기를 완전히 삭제하려면 0000 을 입력하세요.');
    if (code === '0000') {
      setMatches(matches.filter(m => m.id !== id));
      await supabase.from('matches').delete().eq('id', id);
      setEditMatchModal(null);
    } else if (code !== null) {
      alert('입력한 코드가 틀렸습니다.');
    }
  }"""
content = content.replace(old_del, new_del)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
