import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. State
state_old = """  const [isGeneratorModalOpen, setIsGeneratorModalOpen] = useState(false);
  const [dbPlayers, setDbPlayers] = useState<Player[]>([]);
  const [selectedPlayerIds, setSelectedPlayerIds] = useState<Set<string>>(new Set());
  const [generatedBracket, setGeneratedBracket] = useState<any[]>([]);"""

state_new = """  const [isGeneratorModalOpen, setIsGeneratorModalOpen] = useState(false);
  const [dbPlayers, setDbPlayers] = useState<Player[]>([]);
  const [selectedPlayerIds, setSelectedPlayerIds] = useState<Set<string>>(new Set());
  const [teamAssignments, setTeamAssignments] = useState<Record<string, 'BLUE' | 'WHITE'>>({});
  const [generatedBracket, setGeneratedBracket] = useState<any[]>([]);"""
content = content.replace(state_old, state_new)

# 2. Auto-Split logic inside generator header
buttons_old = """                  <button onClick={() => setSelectedPlayerIds(new Set())} className="flex-1 text-xs bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 px-2 py-1.5 rounded flex items-center justify-center gap-1 font-bold">
                    <Square className="w-3 h-3" /> 전체해제
                  </button>
                  <button onClick={openGuestModal} className="flex-1 text-xs bg-blue-100 text-blue-700 hover:bg-blue-200 px-2 py-1.5 rounded flex items-center justify-center gap-1 font-bold">
                    <UserPlus className="w-3 h-3" /> 게스트/추가
                  </button>
                </div>"""

buttons_new = """                  <button onClick={() => setSelectedPlayerIds(new Set())} className="flex-1 text-xs bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 px-2 py-1.5 rounded flex items-center justify-center gap-1 font-bold">
                    <Square className="w-3 h-3" /> 전체해제
                  </button>
                  <button onClick={openGuestModal} className="flex-1 text-xs bg-blue-100 text-blue-700 hover:bg-blue-200 px-2 py-1.5 rounded flex items-center justify-center gap-1 font-bold">
                    <UserPlus className="w-3 h-3" /> 게스트/추가
                  </button>
                </div>
                {matchType === 'TEAM' && (
                  <button onClick={() => {
                    const selected = dbPlayers.filter(p => selectedPlayerIds.has(p.id));
                    const sorted = [...selected].sort((a,b) => a.grade.localeCompare(b.grade));
                    const newAssignments = {...teamAssignments};
                    sorted.forEach((p, i) => {
                        newAssignments[p.id] = i % 2 === 0 ? 'BLUE' : 'WHITE';
                    });
                    setTeamAssignments(newAssignments);
                  }} className="w-full text-xs bg-indigo-100 text-indigo-700 hover:bg-indigo-200 px-2 py-2 rounded flex items-center justify-center gap-1 font-bold shadow-sm">
                    <RefreshCw className="w-3 h-3" /> 선택된 인원 청백팀 균형있게 자동 나누기
                  </button>
                )}"""
content = content.replace(buttons_old, buttons_new)

# 3. UI for player item
ui_old = """                        <span className="font-bold text-sm text-gray-800 dark:text-gray-200">{p.name}</span>
                      </label>
                      <div className="flex gap-1 items-center bg-white dark:bg-gray-900 rounded-md border border-gray-200 dark:border-gray-700 p-0.5">"""

ui_new = """                        <span className="font-bold text-sm text-gray-800 dark:text-gray-200">{p.name}</span>
                        {matchType === 'TEAM' && selectedPlayerIds.has(p.id) && (
                          <div className="flex gap-0.5 ml-1">
                            <button onClick={(e) => { e.preventDefault(); setTeamAssignments({...teamAssignments, [p.id]: 'BLUE'}); }} className={`text-[10px] px-1.5 py-0.5 rounded font-black ${teamAssignments[p.id] !== 'WHITE' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-400 dark:bg-gray-700'}`}>청</button>
                            <button onClick={(e) => { e.preventDefault(); setTeamAssignments({...teamAssignments, [p.id]: 'WHITE'}); }} className={`text-[10px] px-1.5 py-0.5 rounded font-black ${teamAssignments[p.id] === 'WHITE' ? 'bg-gray-600 text-white' : 'bg-gray-200 text-gray-400 dark:bg-gray-700'}`}>백</button>
                          </div>
                        )}
                      </label>
                      <div className="flex gap-1 items-center bg-white dark:bg-gray-900 rounded-md border border-gray-200 dark:border-gray-700 p-0.5">"""
content = content.replace(ui_old, ui_new)


# 4. Generate Button Call
gen_old = """  const handleGenerate = () => {
    setIsGenerating(true);
    setTimeout(() => {
      const selectedPlayers = dbPlayers.filter(p => selectedPlayerIds.has(p.id));
      const matches = generateMatches(selectedPlayers, matchType, numCourts, numRounds, ignoreGrade);
      setGeneratedBracket(matches);
      setIsGenerating(false);
    }, 600);
  };"""

gen_new = """  const handleGenerate = () => {
    setIsGenerating(true);
    setTimeout(() => {
      const selectedPlayers = dbPlayers.filter(p => selectedPlayerIds.has(p.id));
      const manualBlueTeam = matchType === 'TEAM' ? selectedPlayers.filter(p => teamAssignments[p.id] !== 'WHITE') : [];
      const manualWhiteTeam = matchType === 'TEAM' ? selectedPlayers.filter(p => teamAssignments[p.id] === 'WHITE') : [];
      
      const matches = generateMatches(selectedPlayers, matchType, numCourts, numRounds, ignoreGrade, manualBlueTeam, manualWhiteTeam);
      setGeneratedBracket(matches);
      setIsGenerating(false);
    }, 600);
  };"""
content = content.replace(gen_old, gen_new)


with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
