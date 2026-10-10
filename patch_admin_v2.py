import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Add new imports
new_imports = """
import { generateMatches } from '@/lib/matchMaker';
import { Player } from '@/lib/types';
import { RefreshCw, Save, X } from 'lucide-react';
"""
content = content.replace('import { Settings, Plus,', new_imports + 'import { Settings, Plus,')

# 2. Add new states inside AdminPage component
new_states = """
  // --- New Bracket Generator State ---
  const [isGeneratorModalOpen, setIsGeneratorModalOpen] = useState(false);
  const [dbPlayers, setDbPlayers] = useState<Player[]>([]);
  const [selectedPlayerIds, setSelectedPlayerIds] = useState<Set<string>>(new Set());
  const [generatedBracket, setGeneratedBracket] = useState<any[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [tournaments, setTournaments] = useState<any[]>([]);

  async function fetchPlayersAndTournaments() {
    const { data: tData } = await supabase.from('tournaments').select('*').order('created_at', { ascending: false });
    if (tData) setTournaments(tData);

    const { data: pData } = await supabase.from('players').select('*').order('grade', { ascending: true });
    if (pData) {
      setDbPlayers(pData);
      setSelectedPlayerIds(new Set(pData.map(p => p.id)));
    }
  }

  useEffect(() => {
    if (authed) fetchPlayersAndTournaments();
  }, [authed]);

  const handleGenerate = () => {
    setIsGenerating(true);
    setTimeout(() => {
      const activePlayers = dbPlayers.filter(p => selectedPlayerIds.has(p.id));
      const matches = generateMatches(activePlayers, 'TEAM', 7);
      setGeneratedBracket(matches);
      setIsGenerating(false);
    }, 600);
  };

  const saveTournament = async () => {
    const { data: tData, error: tErr } = await supabase.from('tournaments').insert({
      title: `${new Date().getMonth() + 1}월 월례회`,
      match_type: 'TEAM',
      display_mode: 'SCORE',
      status: 'IN_PROGRESS'
    }).select().single();

    if (tErr || !tData) return alert('대회 생성 실패!');

    const matchInserts = generatedBracket.map((m, i) => ({
      tournament_id: tData.id,
      round_num: Math.floor(i / 3) + 1,
      court_num: (i % 3) + 1,
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
    fetchMatches();
    alert('새 대진표가 성공적으로 적용되었습니다!');
  };

  const handleSwapGenerated = (matchIndex: number, team: 'blue' | 'white', playerIndex: 0 | 1) => {
    const targetName = prompt('누구와 교체하시겠습니까? (정확한 이름 입력)');
    if (!targetName) return;
    
    const targetPlayer = dbPlayers.find(p => p.name === targetName);
    if (!targetPlayer) {
      alert('존재하지 않는 회원입니다.');
      return;
    }

    const newBracket = [...generatedBracket];
    if (team === 'blue') {
      newBracket[matchIndex].blue_team[playerIndex] = targetPlayer;
    } else {
      newBracket[matchIndex].white_team[playerIndex] = targetPlayer;
    }
    setGeneratedBracket(newBracket);
  };
"""
content = re.sub(r'(const \[editMatchModal.*?\] = useState.*?;)', r'\1' + '\n' + new_states, content)

# 3. Add button in Header
header_replacement = """
          <h1 className="text-xl md:text-2xl font-black flex items-center gap-2">
            <Settings className="text-gray-400" />
            점수 관리 보드
          </h1>
          <div className="flex gap-2">
            <button onClick={() => { setGeneratedBracket([]); setIsGeneratorModalOpen(true); }} className="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold text-sm flex items-center gap-1 hover:bg-blue-700 shadow-sm">
              <RefreshCw className="w-4 h-4" /> 새 대진표 자동생성
            </button>
            <button onClick={addMatch} className="bg-gray-900 dark:bg-gray-100 text-white dark:text-black px-4 py-2 rounded-lg font-bold text-sm flex items-center gap-1 hover:opacity-80">
              <Plus className="w-4 h-4" /> 빈 경기 추가
            </button>
          </div>
"""
content = re.sub(r'<h1 className="text-xl md:text-2xl.*?<Plus className="w-4 h-4" /> 경기 추가\n\s*</button>', header_replacement, content, flags=re.DOTALL)

# 4. Add Modal UI at the bottom of the JSX before final closing div
modal_ui = """
      {/* --- 대진표 자동 생성 모달 --- */}
      {isGeneratorModalOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white dark:bg-gray-900 rounded-3xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col shadow-2xl">
            <div className="p-6 border-b border-gray-100 dark:border-gray-800 flex items-center justify-between">
              <h2 className="text-xl font-bold flex items-center gap-2">
                <RefreshCw className="text-blue-600" /> 대진표 자동 생성기
              </h2>
              <button onClick={() => setIsGeneratorModalOpen(false)} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 flex-1 overflow-y-auto flex flex-col md:flex-row gap-8 bg-gray-50 dark:bg-gray-950">
              <div className="w-full md:w-1/3 space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="font-bold text-gray-800 dark:text-gray-200">참가자 선택</h3>
                  <span className="text-sm text-blue-600 font-bold bg-blue-50 px-2 py-1 rounded-md">{selectedPlayerIds.size}명 선택됨</span>
                </div>
                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-4 max-h-[50vh] overflow-y-auto space-y-2">
                  {dbPlayers.map(p => (
                    <label key={p.id} className="flex items-center gap-3 p-2 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg cursor-pointer">
                      <input 
                        type="checkbox" 
                        className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500 border-gray-300"
                        checked={selectedPlayerIds.has(p.id)}
                        onChange={(e) => {
                          const next = new Set(selectedPlayerIds);
                          if (e.target.checked) next.add(p.id);
                          else next.delete(p.id);
                          setSelectedPlayerIds(next);
                        }}
                      />
                      <span className="font-medium text-sm text-gray-800 dark:text-gray-200">{p.name}</span>
                      <span className="text-xs font-bold text-gray-500 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded-md">{p.grade}급</span>
                    </label>
                  ))}
                </div>
                <button 
                  onClick={handleGenerate}
                  disabled={isGenerating || selectedPlayerIds.size < 4}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50 transition-all shadow-md"
                >
                  <RefreshCw className={`w-5 h-5 ${isGenerating ? 'animate-spin' : ''}`} />
                  알고리즘으로 대진표 짜기
                </button>
              </div>

              <div className="w-full md:w-2/3">
                <h3 className="font-bold mb-4 text-gray-800 dark:text-gray-200">대진표 미리보기 <span className="text-sm font-normal text-gray-500 ml-2">(이름을 클릭하여 수동 교체)</span></h3>
                {generatedBracket.length === 0 ? (
                  <div className="h-64 flex flex-col items-center justify-center text-gray-400 border-2 border-dashed border-gray-200 dark:border-gray-800 rounded-2xl bg-white dark:bg-gray-900">
                    <Trophy className="w-12 h-12 mb-3 opacity-30 text-blue-500" />
                    <p className="font-medium">좌측에서 생성 버튼을 눌러주세요</p>
                  </div>
                ) : (
                  <div className="space-y-3 max-h-[50vh] overflow-y-auto pr-2">
                    {generatedBracket.map((m, idx) => (
                      <div key={idx} className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-4 flex shadow-sm hover:border-blue-300 transition-colors">
                        <div className="flex-1 flex flex-col justify-center gap-2 border-r border-gray-100 dark:border-gray-800 pr-4">
                          <span className="text-xs font-black text-blue-600 bg-blue-50 px-2 py-1 rounded w-max">청팀</span>
                          <div className="flex gap-2">
                            <button onClick={() => handleSwapGenerated(idx, 'blue', 0)} className="text-sm bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-blue-200 transition-all">{m.blue_team[0].name} <span className="text-xs font-normal text-gray-400 ml-1">{m.blue_team[0].grade}</span></button>
                            <button onClick={() => handleSwapGenerated(idx, 'blue', 1)} className="text-sm bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-blue-200 transition-all">{m.blue_team[1].name} <span className="text-xs font-normal text-gray-400 ml-1">{m.blue_team[1].grade}</span></button>
                          </div>
                        </div>
                        <div className="px-5 flex items-center justify-center font-black text-gray-300 italic text-lg">VS</div>
                        <div className="flex-1 flex flex-col justify-center gap-2 pl-4">
                          <span className="text-xs font-black text-gray-600 bg-gray-100 px-2 py-1 rounded w-max">백팀</span>
                          <div className="flex gap-2">
                            <button onClick={() => handleSwapGenerated(idx, 'white', 0)} className="text-sm bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-gray-300 transition-all">{m.white_team[0].name} <span className="text-xs font-normal text-gray-400 ml-1">{m.white_team[0].grade}</span></button>
                            <button onClick={() => handleSwapGenerated(idx, 'white', 1)} className="text-sm bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-gray-300 transition-all">{m.white_team[1].name} <span className="text-xs font-normal text-gray-400 ml-1">{m.white_team[1].grade}</span></button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            <div className="p-5 border-t border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-900 flex justify-end gap-3">
              <button onClick={() => setIsGeneratorModalOpen(false)} className="px-6 py-3 font-bold text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-xl transition-colors">취소</button>
              <button 
                onClick={saveTournament}
                disabled={generatedBracket.length === 0}
                className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl flex items-center gap-2 disabled:opacity-50 transition-all shadow-md"
              >
                <Save className="w-5 h-5" />
                이 대진표로 실제 경기 생성하기
              </button>
            </div>
          </div>
        </div>
      )}
"""
# insert before the last </div>
content = content[:content.rfind('</div>')] + modal_ui + '\n    </div>\n  );\n}\n'

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
