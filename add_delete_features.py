with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Imports
content = content.replace("Edit2, UserPlus, CheckSquare, Square", "Edit2, UserPlus, CheckSquare, Square, Trash2")

# 2. Add Delete Functions
delete_funcs = """  const deleteTournament = async (id: string) => {
    const code = prompt('이 대회와 모든 하위 경기가 삭제됩니다. 삭제하려면 0000 을 입력하세요.');
    if (code === '0000') {
      await supabase.from('tournaments').delete().eq('id', id);
      setTournaments(tournaments.filter(t => t.id !== id));
      if (selectedTournamentId === id) setSelectedTournamentId(null);
      setEditingTournamentId(null);
    } else if (code !== null) {
      alert('입력한 코드가 틀렸습니다.');
    }
  };

  const deleteMatch = async (id: string) => {
    const code = prompt('이 경기를 삭제하려면 0000 을 입력하세요.');
    if (code === '0000') {
      await supabase.from('matches').delete().eq('id', id);
      setEditMatchModal(null);
      fetchPlayersAndTournaments();
    } else if (code !== null) {
      alert('입력한 코드가 틀렸습니다.');
    }
  };"""

content = content.replace("  // --- Tournament Renaming ---", delete_funcs + "\n\n  // --- Tournament Renaming ---")

# 3. Add Delete Button for Tournaments
old_t_btns = """                    <div className={`w-2 h-2 rounded-full ${t.status === 'IN_PROGRESS' ? 'bg-green-500' : 'bg-gray-300'}`} />
                  </div>
                </div>"""
new_t_btns = """                    <div className={`w-2 h-2 rounded-full ${t.status === 'IN_PROGRESS' ? 'bg-green-500' : 'bg-gray-300'}`} />
                    {editingTournamentId !== t.id && (
                      <button 
                        onClick={(e) => { e.stopPropagation(); deleteTournament(t.id); }} 
                        className="p-1 hover:bg-red-100 dark:hover:bg-red-900/30 rounded text-red-400 hover:text-red-600 transition-colors"
                      >
                        <Trash2 className="w-3 h-3" />
                      </button>
                    )}
                  </div>
                </div>"""
content = content.replace(old_t_btns, new_t_btns)

# 4. Add Delete Button for Matches (in EditMatchModal)
old_m_btns = """            <div className="flex gap-3">
              <button 
                onClick={() => setEditMatchModal(null)} 
                className="flex-1 bg-gray-200 dark:bg-gray-800 text-gray-800 dark:text-gray-200 py-3.5 rounded-xl font-bold"
              >
                취소
              </button>
              <button 
                onClick={saveMatchInfo} 
                className="flex-1 bg-yellow-500 text-white py-3.5 rounded-xl font-bold"
              >
                저장
              </button>
            </div>"""

new_m_btns = """            <div className="flex flex-col gap-3">
              <div className="flex gap-3">
                <button 
                  onClick={() => setEditMatchModal(null)} 
                  className="flex-1 bg-gray-200 dark:bg-gray-800 text-gray-800 dark:text-gray-200 py-3.5 rounded-xl font-bold"
                >
                  취소
                </button>
                <button 
                  onClick={saveMatchInfo} 
                  className="flex-1 bg-yellow-500 text-white py-3.5 rounded-xl font-bold"
                >
                  저장
                </button>
              </div>
              <button 
                onClick={() => deleteMatch(editMatchModal.id)} 
                className="w-full bg-red-50 text-red-600 dark:bg-red-900/20 dark:text-red-400 py-3 rounded-xl font-bold text-sm hover:bg-red-100 dark:hover:bg-red-900/40 transition-colors flex items-center justify-center gap-2"
              >
                <Trash2 className="w-4 h-4" /> 이 경기 완전 삭제
              </button>
            </div>"""
content = content.replace(old_m_btns, new_m_btns)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
