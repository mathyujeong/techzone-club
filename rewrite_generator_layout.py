import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# Extract parts to preserve the exact logic
# 1. dbPlayers map block
player_map_match = re.search(r'(\{dbPlayers\.map\(p => \(.*?\)\)\})', content, re.DOTALL)
if not player_map_match:
    print("Cannot find dbPlayers map")
    exit(1)
player_map_block = player_map_match.group(1)

# 2. Preview map block
preview_map_match = re.search(r'(\{generatedBracket\.map\(\(m, idx\) => \(.*?\)\)\})', content, re.DOTALL)
if not preview_map_match:
    print("Cannot find preview map")
    exit(1)
preview_map_block = preview_map_match.group(1)


new_layout = f"""            <div className="p-6 flex-1 overflow-y-auto flex flex-col gap-6 bg-gray-50 dark:bg-gray-950">
              
              {{/* --- TOP: SETTINGS PANEL --- */}}
              <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-4 shadow-sm flex flex-col xl:flex-row gap-4 items-center shrink-0">
                
                <div className="flex flex-col sm:flex-row w-full flex-1 gap-4 items-center">
                  <div className="w-full sm:w-auto">
                    <label className="text-xs text-gray-500 font-bold mb-1 block">경기 방식</label>
                    <select 
                      value={{matchType}} 
                      onChange={{e => setMatchType(e.target.value as 'TEAM' | 'INDIVIDUAL')}}
                      className="w-full sm:w-auto bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-3 py-2 rounded-xl font-bold outline-none cursor-pointer"
                    >
                      <option value="TEAM">청백전 (팀전)</option>
                      <option value="INDIVIDUAL">개인전 (랜덤 매치)</option>
                    </select>
                  </div>

                  <div className="flex gap-2 w-full sm:w-auto">
                    <div className="flex-1 sm:w-24 bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-3 py-1 flex flex-col justify-center">
                      <label className="text-[10px] text-gray-500 font-bold">코트 수</label>
                      <div className="flex items-center gap-1">
                        <input type="number" min="1" max="10" value={{numCourts}} onChange={{e => setNumCourts(parseInt(e.target.value) || 1)}} className="w-full bg-transparent font-black outline-none text-lg" />
                        <span className="text-xs text-gray-400 font-bold">면</span>
                      </div>
                    </div>
                    <div className="flex-1 sm:w-24 bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-3 py-1 flex flex-col justify-center">
                      <label className="text-[10px] text-gray-500 font-bold">총 라운드</label>
                      <div className="flex items-center gap-1">
                        <input type="number" min="1" max="20" value={{numRounds}} onChange={{e => setNumRounds(parseInt(e.target.value) || 1)}} className="w-full bg-transparent font-black outline-none text-lg" />
                        <span className="text-xs text-gray-400 font-bold">R</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-row sm:flex-col gap-4 sm:gap-2 w-full sm:w-auto bg-gray-50 dark:bg-gray-800/50 p-2 rounded-xl">
                    <label className="flex items-center gap-2 text-xs font-bold text-gray-700 dark:text-gray-300 cursor-pointer">
                      <input type="checkbox" checked={{ignoreGrade}} onChange={{e => setIgnoreGrade(e.target.checked)}} className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500" />
                      급수 무관 매칭
                    </label>
                    <label className="flex items-center gap-2 text-xs font-bold text-gray-700 dark:text-gray-300 cursor-pointer">
                      <input type="checkbox" checked={{hideGrade}} onChange={{e => setHideGrade(e.target.checked)}} className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500" />
                      대진표 급수 숨기기
                    </label>
                  </div>
                </div>

                <div className="w-full xl:w-auto shrink-0">
                  <button 
                    onClick={{handleGenerate}}
                    disabled={{isGenerating || selectedPlayerIds.size < 4}}
                    className="w-full xl:w-64 bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-xl font-black flex items-center justify-center gap-2 disabled:opacity-50 transition-all shadow-md text-lg"
                  >
                    <RefreshCw className={{`w-5 h-5 ${{isGenerating ? 'animate-spin' : ''}}`}} />
                    대진표 자동 짜기
                  </button>
                </div>
              </div>


              {{/* --- BOTTOM: PLAYERS & PREVIEW --- */}}
              <div className="flex flex-col lg:flex-row gap-6 flex-1 min-h-0">
                
                {{/* LEFT: PLAYERS */}}
                <div className="w-full lg:w-1/2 flex flex-col gap-3 h-full max-h-[70vh]">
                  <div className="flex justify-between items-center">
                    <h3 className="font-bold text-gray-800 dark:text-gray-200">참가자 선택</h3>
                    <div className="flex gap-2">
                      <span className="text-sm text-blue-600 font-bold bg-blue-50 px-2 py-1 rounded-md">{{selectedPlayerIds.size}}명 선택됨</span>
                    </div>
                  </div>
                  
                  <div className="flex justify-between gap-1 shrink-0">
                    <button onClick={{() => setSelectedPlayerIds(new Set(dbPlayers.map(p => p.id)))}} className="flex-1 text-xs bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 px-2 py-2 rounded-lg flex items-center justify-center gap-1 font-bold">
                      <CheckSquare className="w-4 h-4" /> 전체선택
                    </button>
                    <button onClick={{() => setSelectedPlayerIds(new Set())}} className="flex-1 text-xs bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 px-2 py-2 rounded-lg flex items-center justify-center gap-1 font-bold">
                      <Square className="w-4 h-4" /> 전체해제
                    </button>
                    <button onClick={{openGuestModal}} className="flex-1 text-xs bg-blue-100 text-blue-700 hover:bg-blue-200 px-2 py-2 rounded-lg flex items-center justify-center gap-1 font-bold">
                      <UserPlus className="w-4 h-4" /> 게스트 추가
                    </button>
                  </div>
                  {{matchType === 'TEAM' && (
                    <button onClick={{() => {{
                      const selected = dbPlayers.filter(p => selectedPlayerIds.has(p.id));
                      const sorted = [...selected].sort((a,b) => a.grade.localeCompare(b.grade));
                      const newAssignments = {{...teamAssignments}};
                      sorted.forEach((p, i) => {{
                          newAssignments[p.id] = i % 2 === 0 ? 'BLUE' : 'WHITE';
                      }});
                      setTeamAssignments(newAssignments);
                    }}}} className="w-full text-sm bg-indigo-100 text-indigo-700 hover:bg-indigo-200 px-4 py-3 rounded-lg flex items-center justify-center gap-2 font-bold shadow-sm">
                      <RefreshCw className="w-4 h-4" /> 선택된 인원 청백팀 균형있게 자동 나누기
                    </button>
                  )}}
                  
                  <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-3 flex-1 overflow-y-auto min-h-0 shadow-sm">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {player_map_block}
                    </div>
                  </div>
                </div>

                {{/* RIGHT: PREVIEW */}}
                <div className="w-full lg:w-1/2 flex flex-col h-full max-h-[70vh]">
                  <h3 className="font-bold mb-4 text-gray-800 dark:text-gray-200">대진표 미리보기 <span className="text-sm font-normal text-gray-500 ml-2">(이름 클릭 교체)</span></h3>
                  {{generatedBracket.length === 0 ? (
                    <div className="flex-1 flex flex-col items-center justify-center text-gray-400 border-2 border-dashed border-gray-200 dark:border-gray-800 rounded-2xl bg-white dark:bg-gray-900 min-h-[300px]">
                      <Trophy className="w-12 h-12 mb-3 opacity-30 text-blue-500" />
                      <p className="font-medium">위에서 생성 버튼을 눌러주세요</p>
                    </div>
                  ) : (
                    <div className="space-y-3 flex-1 overflow-y-auto pr-2">
                      {preview_map_block}
                    </div>
                  )}}
                </div>
              </div>
            </div>"""

start_token = '<div className="p-6 flex-1 overflow-y-auto flex flex-col md:flex-row gap-8 bg-gray-50 dark:bg-gray-950">'
end_token = '<div className="p-5 border-t border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-900 flex justify-end gap-3">'

start_idx = content.find(start_token)
end_idx = content.find(end_token)

if start_idx == -1 or end_idx == -1:
    print("Tokens not found!")
    exit(1)

final_content = content[:start_idx] + new_layout + '\n\n            ' + content[end_idx:]

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(final_content)
