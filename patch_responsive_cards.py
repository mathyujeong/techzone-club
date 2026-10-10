with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Update the grid classes
old_grid = '              <div className="grid grid-cols-3 gap-2">'
new_grid = '              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 md:gap-4">'
content = content.replace(old_grid, new_grid)

# 2. Update the Blue Team half
old_blue = """                    <div className={`p-1.5 flex justify-between items-center border-b border-gray-100 dark:border-gray-800 flex-1 ${m.status === 'completed' && m.blue_score > m.white_score ? 'bg-blue-50 dark:bg-blue-900/30' : ''}`}>
                      <div 
                        className="font-bold text-[12px] text-blue-700 dark:text-blue-400 cursor-pointer w-full"
                        onClick={() => editPlayers(m.id, 'blue', m.blue_player1, m.blue_player2)}
                      >
                        <div className="truncate w-full">{m.blue_player1}</div>
                        <div className="truncate w-full">{m.blue_player2}</div>
                        {bluePen && bluePen !== '0' && <div className="text-[9px] text-red-500">패널티 {bluePen}</div>}
                      </div>
                      <button 
                        onClick={() => setWinner(m.id, 'blue')} 
                        className={`w-7 h-7 flex justify-center items-center rounded-full border shrink-0 ml-1 shadow-sm ${
                          m.status === 'completed' && m.blue_score > m.white_score 
                            ? 'bg-blue-600 border-blue-600 text-white' 
                            : 'bg-white border-blue-200 text-blue-500 dark:bg-gray-800'
                        }`}
                      >
                        <span className="text-[10px] font-black leading-none">{m.status === 'completed' && m.blue_score > m.white_score ? 'WIN' : '승'}</span>
                      </button>
                    </div>"""

new_blue = """                    <div className={`p-2 md:p-3 flex justify-between items-center border-b border-gray-100 dark:border-gray-800 flex-1 ${m.status === 'completed' && m.blue_score > m.white_score ? 'bg-blue-50 dark:bg-blue-900/30' : ''}`}>
                      <div 
                        className="font-black text-sm sm:text-base md:text-lg text-blue-700 dark:text-blue-400 cursor-pointer w-full flex flex-col justify-center min-w-0 pr-2"
                        onClick={() => editPlayers(m.id, 'blue', m.blue_player1, m.blue_player2)}
                      >
                        <div className="truncate w-full">{m.blue_player1}</div>
                        <div className="truncate w-full">{m.blue_player2}</div>
                        {bluePen && bluePen !== '0' && <div className="text-[10px] md:text-xs font-bold text-red-500 mt-0.5">패널티 {bluePen}</div>}
                      </div>
                      <button 
                        onClick={() => setWinner(m.id, 'blue')} 
                        className={`w-9 h-9 md:w-11 md:h-11 flex justify-center items-center rounded-full border shrink-0 shadow-sm transition-all ${
                          m.status === 'completed' && m.blue_score > m.white_score 
                            ? 'bg-blue-600 border-blue-600 text-white' 
                            : 'bg-white border-blue-200 text-blue-500 hover:bg-blue-50 dark:bg-gray-800'
                        }`}
                      >
                        <span className="text-xs md:text-sm font-black leading-none">{m.status === 'completed' && m.blue_score > m.white_score ? 'WIN' : '승'}</span>
                      </button>
                    </div>"""
content = content.replace(old_blue, new_blue)

# 3. Update the White Team half
old_white = """                    <div className={`p-1.5 flex justify-between items-center flex-1 ${m.status === 'completed' && m.white_score > m.blue_score ? 'bg-gray-100 dark:bg-gray-800' : ''}`}>
                      <div 
                        className="font-bold text-[12px] text-gray-700 dark:text-gray-300 cursor-pointer w-full"
                        onClick={() => editPlayers(m.id, 'white', m.white_player1, m.white_player2)}
                      >
                        <div className="truncate w-full">{m.white_player1}</div>
                        <div className="truncate w-full">{m.white_player2}</div>
                        {whitePen && whitePen !== '0' && <div className="text-[9px] text-red-500">패널티 {whitePen}</div>}
                      </div>
                      <button 
                        onClick={() => setWinner(m.id, 'white')} 
                        className={`w-7 h-7 flex justify-center items-center rounded-full border shrink-0 ml-1 shadow-sm ${
                          m.status === 'completed' && m.white_score > m.blue_score 
                            ? 'bg-gray-600 border-gray-600 text-white' 
                            : 'bg-white border-gray-200 text-gray-400 dark:bg-gray-800'
                        }`}
                      >
                        <span className="text-[10px] font-black leading-none">{m.status === 'completed' && m.white_score > m.blue_score ? 'WIN' : '승'}</span>
                      </button>
                    </div>"""

new_white = """                    <div className={`p-2 md:p-3 flex justify-between items-center flex-1 ${m.status === 'completed' && m.white_score > m.blue_score ? 'bg-gray-100 dark:bg-gray-800' : ''}`}>
                      <div 
                        className="font-black text-sm sm:text-base md:text-lg text-gray-700 dark:text-gray-300 cursor-pointer w-full flex flex-col justify-center min-w-0 pr-2"
                        onClick={() => editPlayers(m.id, 'white', m.white_player1, m.white_player2)}
                      >
                        <div className="truncate w-full">{m.white_player1}</div>
                        <div className="truncate w-full">{m.white_player2}</div>
                        {whitePen && whitePen !== '0' && <div className="text-[10px] md:text-xs font-bold text-red-500 mt-0.5">패널티 {whitePen}</div>}
                      </div>
                      <button 
                        onClick={() => setWinner(m.id, 'white')} 
                        className={`w-9 h-9 md:w-11 md:h-11 flex justify-center items-center rounded-full border shrink-0 shadow-sm transition-all ${
                          m.status === 'completed' && m.white_score > m.blue_score 
                            ? 'bg-gray-600 border-gray-600 text-white' 
                            : 'bg-white border-gray-200 text-gray-500 hover:bg-gray-50 dark:bg-gray-800'
                        }`}
                      >
                        <span className="text-xs md:text-sm font-black leading-none">{m.status === 'completed' && m.white_score > m.blue_score ? 'WIN' : '승'}</span>
                      </button>
                    </div>"""
content = content.replace(old_white, new_white)

# 4. Check if the "대진표 미리보기" in the Generator Modal is also too small
# In Generator Modal, they used text-sm.
old_gen_blue = """                            <button onClick={() => handleSwapGenerated(idx, 'blue', 0)} className="text-sm bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-blue-200 transition-all">{m.blue_team[0].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.blue_team[0].grade}</span>}</button>
                            <button onClick={() => handleSwapGenerated(idx, 'blue', 1)} className="text-sm bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-blue-200 transition-all">{m.blue_team[1].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.blue_team[1].grade}</span>}</button>"""

new_gen_blue = """                            <button onClick={() => handleSwapGenerated(idx, 'blue', 0)} className="text-sm md:text-base bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-blue-200 transition-all min-w-0">{m.blue_team[0].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.blue_team[0].grade}</span>}</button>
                            <button onClick={() => handleSwapGenerated(idx, 'blue', 1)} className="text-sm md:text-base bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-blue-200 transition-all min-w-0">{m.blue_team[1].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.blue_team[1].grade}</span>}</button>"""
content = content.replace(old_gen_blue, new_gen_blue)

old_gen_white = """                            <button onClick={() => handleSwapGenerated(idx, 'white', 0)} className="text-sm bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-gray-300 transition-all">{m.white_team[0].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.white_team[0].grade}</span>}</button>
                            <button onClick={() => handleSwapGenerated(idx, 'white', 1)} className="text-sm bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-gray-300 transition-all">{m.white_team[1].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.white_team[1].grade}</span>}</button>"""

new_gen_white = """                            <button onClick={() => handleSwapGenerated(idx, 'white', 0)} className="text-sm md:text-base bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-gray-300 transition-all min-w-0">{m.white_team[0].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.white_team[0].grade}</span>}</button>
                            <button onClick={() => handleSwapGenerated(idx, 'white', 1)} className="text-sm md:text-base bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-gray-300 transition-all min-w-0">{m.white_team[1].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.white_team[1].grade}</span>}</button>"""
content = content.replace(old_gen_white, new_gen_white)


with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
