with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. State Additions
state_old = 'const [isPlayerManageModalOpen, setIsPlayerManageModalOpen] = useState(false);'
state_new = """const [isPlayerManageModalOpen, setIsPlayerManageModalOpen] = useState(false);
  const [isGuestModalOpen, setIsGuestModalOpen] = useState(false);
  const [guestName, setGuestName] = useState("");
  const [guestGrade, setGuestGrade] = useState("E");"""
content = content.replace(state_old, state_new)

# 2. Function Updates
func_old = """  const handleAddGuest = async () => {
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
  };"""

func_new = """  const openGuestModal = () => {
    setGuestName("");
    setGuestGrade("E");
    setIsGuestModalOpen(true);
  };

  const saveGuest = async () => {
    if (!guestName.trim()) return;
    const { data, error } = await supabase.from('players').insert({ name: guestName.trim(), grade: guestGrade }).select().single();
    if (data) {
      setDbPlayers([...dbPlayers, data].sort((a, b) => a.grade.localeCompare(b.grade)));
      const newSet = new Set(selectedPlayerIds);
      newSet.add(data.id);
      setSelectedPlayerIds(newSet);
      setIsGuestModalOpen(false);
    } else {
      alert('추가 실패: ' + (error?.message || '알 수 없는 오류'));
    }
  };"""
content = content.replace(func_old, func_new)

# 3. Button Click handler change
content = content.replace('onClick={handleAddGuest}', 'onClick={openGuestModal}')

# 4. Modal UI insertion
modal_ui = """
      {/* --- 게스트 추가 모달 --- */}
      {isGuestModalOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[60] flex items-center justify-center p-4">
          <div className="bg-white dark:bg-gray-900 rounded-3xl w-full max-w-sm p-6 shadow-2xl border border-gray-100 dark:border-gray-800">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold flex items-center gap-2 text-gray-800 dark:text-white">
                <UserPlus className="text-blue-600 w-6 h-6" /> 새 게스트 추가
              </h2>
              <button onClick={() => setIsGuestModalOpen(false)} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full">
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">이름</label>
                <input 
                  type="text" 
                  value={guestName} 
                  onChange={(e) => setGuestName(e.target.value)} 
                  placeholder="홍길동"
                  autoFocus
                  className="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all font-medium"
                  onKeyDown={(e) => e.key === 'Enter' && saveGuest()}
                />
              </div>
              <div className="relative">
                <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">급수</label>
                <select 
                  value={guestGrade} 
                  onChange={(e) => setGuestGrade(e.target.value)}
                  className="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all font-medium cursor-pointer appearance-none"
                >
                  <option value="S">S급</option>
                  <option value="A">A급</option>
                  <option value="B">B급</option>
                  <option value="C">C급</option>
                  <option value="D">D급</option>
                  <option value="E">E급 (초심)</option>
                </select>
                <ChevronDown className="absolute right-4 top-10 w-5 h-5 text-gray-400 pointer-events-none" />
              </div>
            </div>
            <button 
              onClick={saveGuest}
              disabled={!guestName.trim()}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50 transition-all shadow-md"
            >
              추가하기
            </button>
          </div>
        </div>
      )}
"""
content = content.replace("      </main>\n    </div>\n  );\n}", modal_ui + "      </main>\n    </div>\n  );\n}")

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
