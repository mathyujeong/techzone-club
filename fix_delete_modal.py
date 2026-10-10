import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Add States
state_old = """  const [isGuestModalOpen, setIsGuestModalOpen] = useState(false);"""
state_new = """  const [isGuestModalOpen, setIsGuestModalOpen] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState<{type: 'tournament'|'match', id: string} | null>(null);
  const [deleteCode, setDeleteCode] = useState("");"""
content = content.replace(state_old, state_new)

# 2. Modify Delete Functions
old_funcs = """  const deleteTournament = async (id: string) => {
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

  async function deleteMatch(id: string) {
    const code = prompt('이 경기를 완전히 삭제하려면 0000 을 입력하세요.');
    if (code === '0000') {
      setMatches(matches.filter(m => m.id !== id));
      await supabase.from('matches').delete().eq('id', id);
      setEditMatchModal(null);
    } else if (code !== null) {
      alert('입력한 코드가 틀렸습니다.');
    }
  }"""

new_funcs = """  const deleteTournament = (id: string) => {
    setDeleteCode("");
    setDeleteConfirm({ type: 'tournament', id });
  };

  const deleteMatch = (id: string) => {
    setDeleteCode("");
    setDeleteConfirm({ type: 'match', id });
  };

  const executeDelete = async () => {
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

content = content.replace(old_funcs, new_funcs)

# 3. Add Modal JSX
modal_jsx = """
      {/* --- 안전 삭제 모달 --- */}
      {deleteConfirm && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[70] flex items-center justify-center p-4">
          <div className="bg-white dark:bg-gray-900 rounded-3xl w-full max-w-sm p-6 shadow-2xl border border-red-100 dark:border-red-900/30">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold flex items-center gap-2 text-red-600 dark:text-red-500">
                <Trash2 className="w-6 h-6" /> 영구 삭제 확인
              </h2>
              <button onClick={() => setDeleteConfirm(null)} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full">
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-6 font-medium leading-relaxed">
              {deleteConfirm.type === 'tournament' 
                ? '이 대회와 관련된 모든 경기 기록이 완전히 삭제되며 복구할 수 없습니다.' 
                : '선택하신 경기가 완전히 삭제되며 복구할 수 없습니다.'}
              <br /><br />
              정말로 삭제하시려면 아래에 <strong className="text-red-500">0000</strong> 을 입력해주세요.
            </p>

            <div className="space-y-4">
              <input 
                type="text" 
                value={deleteCode} 
                onChange={(e) => setDeleteCode(e.target.value)} 
                placeholder="0000"
                maxLength={4}
                autoFocus
                className="w-full bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-900/50 rounded-xl px-4 py-4 outline-none focus:border-red-500 focus:ring-2 focus:ring-red-200 transition-all font-black text-center text-2xl tracking-[0.5em] text-red-600 placeholder-red-300"
                onKeyDown={(e) => e.key === 'Enter' && executeDelete()}
              />
              <button 
                onClick={executeDelete}
                disabled={deleteCode !== '0000'}
                className="w-full bg-red-600 hover:bg-red-700 text-white py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50 transition-all shadow-md"
              >
                <Trash2 className="w-5 h-5" /> 완전히 삭제하기
              </button>
            </div>
          </div>
        </div>
      )}
"""
content = content.replace("      </main>\n    </div>\n  );\n}", modal_jsx + "      </main>\n    </div>\n  );\n}")

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
