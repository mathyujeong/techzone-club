import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Imports
content = content.replace(
    'import { Save, X, Lock } from \'lucide-react\';',
    'import { Save, X, Lock, Edit2, UserPlus, CheckSquare, Square, Users as UsersIcon } from \'lucide-react\';'
)

# 2. Add new states inside AdminPage
state_additions = """
  const [isPlayerManageModalOpen, setIsPlayerManageModalOpen] = useState(false);
  const [editingTournamentId, setEditingTournamentId] = useState<string | null>(null);
  const [editingTournamentName, setEditingTournamentName] = useState("");
"""
content = content.replace('const [tournaments, setTournaments] = useState<any[]>([]);', 'const [tournaments, setTournaments] = useState<any[]>([]);\n' + state_additions)

# 3. Add new functions for Tournament renaming and Player management
function_additions = """
  // --- Tournament Renaming ---
  const saveTournamentName = async (id: string) => {
    if(!editingTournamentName.trim()) return;
    await supabase.from('tournaments').update({ title: editingTournamentName }).eq('id', id);
    setTournaments(tournaments.map(t => t.id === id ? { ...t, title: editingTournamentName } : t));
    setEditingTournamentId(null);
  };

  // --- Player Management ---
  const handleAddGuest = async () => {
    const name = prompt("게스트/새 회원 이름을 입력하세요:");
    if (!name) return;
    const grade = prompt("급수를 입력하세요 (예: A, B, C, D, E, S):", "E");
    if (!grade) return;
    
    const { data, error } = await supabase.from('players').insert({ name, grade }).select().single();
    if (data) {
      setDbPlayers([...dbPlayers, data].sort((a, b) => a.grade.localeCompare(b.grade)));
      // Automatically select the new guest
      const newSet = new Set(selectedPlayerIds);
      newSet.add(data.id);
      setSelectedPlayerIds(newSet);
      alert(`${name} 님이 추가되었습니다.`);
    } else {
      alert('추가 실패: ' + (error?.message || '알 수 없는 오류'));
    }
  };

  const updatePlayerGrade = async (id: string, newGrade: string) => {
    await supabase.from('players').update({ grade: newGrade }).eq('id', id);
    setDbPlayers(dbPlayers.map(p => p.id === id ? { ...p, grade: newGrade } : p));
  };
"""
content = content.replace('async function fetchPlayersAndTournaments() {', function_additions + '\n  async function fetchPlayersAndTournaments() {')


# 4. Sidebar Tournament Edit UI and "회원 관리" button
old_sidebar = """        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          <h2 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 ml-1">누적 대회 목록</h2>
          {tournaments.map(t => ("""

new_sidebar = """        <div className="p-4 border-b border-gray-200 dark:border-gray-800 pt-0">
          <button onClick={() => setIsPlayerManageModalOpen(true)} className="w-full bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 px-4 py-3 rounded-xl font-bold text-sm flex justify-center items-center gap-2 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
            <UsersIcon className="w-4 h-4" /> 회원 명단 관리
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          <h2 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 ml-1">누적 대회 목록</h2>
          {tournaments.map(t => ("""
content = content.replace(old_sidebar, new_sidebar)

# 5. Tournament List UI with Edit Icon
old_t_button = """              <div className="flex items-center justify-between">
                <span className={`font-bold text-sm ${selectedTournamentId === t.id ? 'text-yellow-700 dark:text-yellow-400' : 'text-gray-700 dark:text-gray-300'}`}>{t.title}</span>
                <div className={`w-2 h-2 rounded-full ${t.status === 'IN_PROGRESS' ? 'bg-green-500' : 'bg-gray-300'}`} />
              </div>
              <span className="text-[10px] text-gray-400">{new Date(t.created_at).toLocaleDateString()}</span>
            </button>"""

new_t_button = """              <div className="flex items-center justify-between w-full">
                {editingTournamentId === t.id ? (
                  <input 
                    type="text" 
                    value={editingTournamentName}
                    onChange={e => setEditingTournamentName(e.target.value)}
                    onBlur={() => saveTournamentName(t.id)}
                    onKeyDown={e => e.key === 'Enter' && saveTournamentName(t.id)}
                    autoFocus
                    className="flex-1 text-sm font-bold border border-blue-400 rounded px-1 py-0.5 w-full bg-white dark:bg-gray-800 text-black dark:text-white"
                    onClick={(e) => e.stopPropagation()}
                  />
                ) : (
                  <span className={`font-bold text-sm flex-1 ${selectedTournamentId === t.id ? 'text-yellow-700 dark:text-yellow-400' : 'text-gray-700 dark:text-gray-300'}`}>{t.title}</span>
                )}
                <div className="flex items-center gap-2 shrink-0">
                  {editingTournamentId !== t.id && (
                    <button 
                      onClick={(e) => { e.stopPropagation(); setEditingTournamentId(t.id); setEditingTournamentName(t.title); }} 
                      className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded text-gray-400 hover:text-gray-600"
                    >
                      <Edit2 className="w-3 h-3" />
                    </button>
                  )}
                  <div className={`w-2 h-2 rounded-full ${t.status === 'IN_PROGRESS' ? 'bg-green-500' : 'bg-gray-300'}`} />
                </div>
              </div>
              <span className="text-[10px] text-gray-400">{new Date(t.created_at).toLocaleDateString()}</span>
            </button>"""
content = content.replace(old_t_button, new_t_button)


# 6. Generator Modal UX: Select All / Deselect All / Add Guest
old_generator_header = """                <div className="flex justify-between items-center">
                  <h3 className="font-bold text-gray-800 dark:text-gray-200">참가자 선택</h3>
                  <span className="text-sm text-blue-600 font-bold bg-blue-50 px-2 py-1 rounded-md">{selectedPlayerIds.size}명 선택됨</span>
                </div>"""

new_generator_header = """                <div className="flex justify-between items-center">
                  <h3 className="font-bold text-gray-800 dark:text-gray-200">참가자 선택</h3>
                  <div className="flex gap-2">
                    <span className="text-sm text-blue-600 font-bold bg-blue-50 px-2 py-1 rounded-md">{selectedPlayerIds.size}명 선택됨</span>
                  </div>
                </div>
                <div className="flex justify-between gap-1 mt-2">
                  <button onClick={() => setSelectedPlayerIds(new Set(dbPlayers.map(p => p.id)))} className="flex-1 text-xs bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 px-2 py-1.5 rounded flex items-center justify-center gap-1 font-bold">
                    <CheckSquare className="w-3 h-3" /> 전체선택
                  </button>
                  <button onClick={() => setSelectedPlayerIds(new Set())} className="flex-1 text-xs bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 px-2 py-1.5 rounded flex items-center justify-center gap-1 font-bold">
                    <Square className="w-3 h-3" /> 전체해제
                  </button>
                  <button onClick={handleAddGuest} className="flex-1 text-xs bg-blue-100 text-blue-700 hover:bg-blue-200 px-2 py-1.5 rounded flex items-center justify-center gap-1 font-bold">
                    <UserPlus className="w-3 h-3" /> 게스트/추가
                  </button>
                </div>"""
content = content.replace(old_generator_header, new_generator_header)


# 7. Player Management Modal UI at the bottom
player_manage_modal = """
      {/* --- 회원 명단 관리 모달 --- */}
      {isPlayerManageModalOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white dark:bg-gray-900 rounded-3xl w-full max-w-xl max-h-[80vh] overflow-hidden flex flex-col shadow-2xl">
            <div className="p-6 border-b border-gray-100 dark:border-gray-800 flex items-center justify-between">
              <h2 className="text-xl font-bold flex items-center gap-2">
                <UsersIcon className="text-blue-600" /> 회원 명단 및 급수 관리
              </h2>
              <button onClick={() => setIsPlayerManageModalOpen(false)} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full">
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="p-6 flex-1 overflow-y-auto space-y-3 bg-gray-50 dark:bg-gray-950">
              <div className="flex justify-between items-center mb-4">
                <h3 className="font-bold">총 {dbPlayers.length}명</h3>
                <button onClick={handleAddGuest} className="bg-blue-600 text-white text-sm px-3 py-1.5 rounded-lg font-bold flex items-center gap-1 hover:bg-blue-700">
                  <UserPlus className="w-4 h-4" /> 새 회원 등록
                </button>
              </div>

              {dbPlayers.map(p => (
                <div key={p.id} className="flex items-center justify-between bg-white dark:bg-gray-900 p-3 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800">
                  <span className="font-bold">{p.name}</span>
                  <div className="flex items-center gap-3">
                    <span className="text-xs text-gray-400">급수 변경:</span>
                    <select 
                      value={p.grade}
                      onChange={(e) => updatePlayerGrade(p.id, e.target.value)}
                      className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg px-2 py-1 font-bold outline-none cursor-pointer"
                    >
                      <option value="S">S급</option>
                      <option value="A">A급</option>
                      <option value="B">B급</option>
                      <option value="C">C급</option>
                      <option value="D">D급</option>
                      <option value="E">E급</option>
                    </select>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
"""

# Insert just before the final `</main>\n    </div>`
content = content.replace("      </main>\n    </div>\n  );\n}", player_manage_modal + "\n      </main>\n    </div>\n  );\n}")

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
