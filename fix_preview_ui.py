import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

old_preview = """                    {generatedBracket.map((m, idx) => (
                      <div key={idx} className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-4 flex shadow-sm hover:border-blue-300 transition-colors">
                        <div className="flex-1 flex flex-col justify-center gap-2 border-r border-gray-100 dark:border-gray-800 pr-4">
                          <span className="text-xs font-black text-gray-500 mb-1">{m.round_num}R - {m.court_num}코트</span>
                          <span className={`text-xs font-black px-2 py-1 rounded w-max ${matchType === 'TEAM' ? 'text-blue-600 bg-blue-50' : 'text-gray-600 bg-gray-100 dark:bg-gray-800'}`}>{matchType === 'TEAM' ? '청팀' : 'A조'}</span>
                          <div className="flex gap-2">
                            <button onClick={() => handleSwapGenerated(idx, 'blue', 0)} className="text-sm md:text-base bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-blue-200 transition-all min-w-0">{m.blue_team[0].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.blue_team[0].grade}</span>}</button>
                            <button onClick={() => handleSwapGenerated(idx, 'blue', 1)} className="text-sm md:text-base bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-blue-200 transition-all min-w-0">{m.blue_team[1].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.blue_team[1].grade}</span>}</button>
                          </div>
                        </div>
                        <div className="px-5 flex items-center justify-center font-black text-gray-300 italic text-lg">VS</div>
                        <div className="flex-1 flex flex-col justify-center gap-2 pl-4">
                          <span className="text-xs font-black text-gray-600 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded w-max">{matchType === 'TEAM' ? '백팀' : 'B조'}</span>
                          <div className="flex gap-2">
                            <button onClick={() => handleSwapGenerated(idx, 'white', 0)} className="text-sm md:text-base bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-gray-300 transition-all min-w-0">{m.white_team[0].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.white_team[0].grade}</span>}</button>
                            <button onClick={() => handleSwapGenerated(idx, 'white', 1)} className="text-sm md:text-base bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-gray-300 transition-all min-w-0">{m.white_team[1].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.white_team[1].grade}</span>}</button>
                          </div>
                        </div>
                      </div>
                    ))}"""

new_preview = """                    {generatedBracket.map((m, idx) => (
                      <div key={idx} className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-3 flex flex-col shadow-sm hover:border-blue-300 transition-all">
                        <div className="flex justify-between items-center mb-3 pb-2 border-b border-gray-100 dark:border-gray-800">
                          <span className="text-xs font-black text-gray-500 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded-md">{m.round_num}R - {m.court_num}코트</span>
                          <span className="text-[10px] font-bold text-gray-400">{m.match_type.split(':')[0]}</span>
                        </div>
                        <div className="flex items-stretch justify-between gap-2">
                          {/* LEFT TEAM */}
                          <div className="flex-1 flex flex-col gap-1.5 min-w-0">
                            <span className={`text-[10px] font-black px-2 py-0.5 rounded w-max mb-0.5 ${matchType === 'TEAM' ? 'text-blue-600 bg-blue-50' : 'text-gray-600 bg-gray-100 dark:bg-gray-800'}`}>{matchType === 'TEAM' ? '청팀' : 'A조'}</span>
                            <button onClick={() => handleSwapGenerated(idx, 'blue', 0)} className="flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-800 hover:bg-blue-50 hover:text-blue-600 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent transition-all group min-w-0">
                              <span className="truncate">{m.blue_team[0].name}</span>
                              {!hideGrade && <span className="text-[10px] font-black text-gray-400 group-hover:text-blue-400 ml-1 shrink-0">{m.blue_team[0].grade}</span>}
                            </button>
                            <button onClick={() => handleSwapGenerated(idx, 'blue', 1)} className="flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-800 hover:bg-blue-50 hover:text-blue-600 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent transition-all group min-w-0">
                              <span className="truncate">{m.blue_team[1].name}</span>
                              {!hideGrade && <span className="text-[10px] font-black text-gray-400 group-hover:text-blue-400 ml-1 shrink-0">{m.blue_team[1].grade}</span>}
                            </button>
                          </div>
                          
                          {/* VS */}
                          <div className="flex items-center justify-center font-black text-gray-200 dark:text-gray-700 italic text-sm px-2">VS</div>
                          
                          {/* RIGHT TEAM */}
                          <div className="flex-1 flex flex-col gap-1.5 min-w-0 items-end">
                            <span className={`text-[10px] font-black px-2 py-0.5 rounded w-max mb-0.5 ${matchType === 'TEAM' ? 'text-gray-600 bg-gray-100 dark:bg-gray-800' : 'text-gray-600 bg-gray-100 dark:bg-gray-800'}`}>{matchType === 'TEAM' ? '백팀' : 'B조'}</span>
                            <button onClick={() => handleSwapGenerated(idx, 'white', 0)} className="flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 hover:text-gray-800 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent transition-all group min-w-0">
                              <span className="truncate">{m.white_team[0].name}</span>
                              {!hideGrade && <span className="text-[10px] font-black text-gray-400 group-hover:text-gray-500 ml-1 shrink-0">{m.white_team[0].grade}</span>}
                            </button>
                            <button onClick={() => handleSwapGenerated(idx, 'white', 1)} className="flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 hover:text-gray-800 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent transition-all group min-w-0">
                              <span className="truncate">{m.white_team[1].name}</span>
                              {!hideGrade && <span className="text-[10px] font-black text-gray-400 group-hover:text-gray-500 ml-1 shrink-0">{m.white_team[1].grade}</span>}
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}"""

content = content.replace(old_preview, new_preview)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
