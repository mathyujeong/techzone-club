import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# Replace Blue Team container
old_blue = """                    {/* 청팀 */}
                    <div className={`p-2 md:p-3 flex justify-between items-center border-b border-gray-100 dark:border-gray-800 flex-1 ${m.status === 'completed' && m.blue_score > m.white_score ? 'bg-blue-50 dark:bg-blue-900/30' : ''}`}>
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

new_blue = """                    {/* 청팀 */}
                    <div className={`p-3 flex justify-between items-center border-b border-gray-100 dark:border-gray-800 flex-1 ${m.status === 'completed' && m.blue_score > m.white_score ? 'bg-blue-50 dark:bg-blue-900/30' : ''}`}>
                      <div 
                        className="font-black text-sm sm:text-base text-blue-700 dark:text-blue-400 cursor-pointer w-full flex flex-col justify-center min-w-0 pr-2"
                        onClick={() => editPlayers(m.id, 'blue', m.blue_player1, m.blue_player2)}
                      >
                        <div className="truncate w-full">{m.blue_player1}</div>
                        <div className="truncate w-full">{m.blue_player2}</div>
                        {bluePen && bluePen !== '0' && <div className="text-[10px] font-bold text-red-500 mt-0.5">패널티 {bluePen}</div>}
                      </div>
                      <button 
                        onClick={() => setWinner(m.id, 'blue')} 
                        className={`w-10 h-10 flex justify-center items-center rounded-full border shrink-0 shadow-sm transition-all ${
                          m.status === 'completed' && m.blue_score > m.white_score 
                            ? 'bg-blue-600 border-blue-600 text-white' 
                            : 'bg-white border-blue-200 text-blue-500 hover:bg-blue-50 dark:bg-gray-800'
                        }`}
                      >
                        <span className="text-xs sm:text-sm font-black leading-none">{m.status === 'completed' && m.blue_score > m.white_score ? 'WIN' : '승'}</span>
                      </button>
                    </div>"""

content = content.replace(old_blue, new_blue)

# Replace White Team container
old_white = """                    {/* 백팀 */}
                    <div className={`p-1.5 flex justify-between items-center flex-1 ${m.status === 'completed' && m.white_score > m.blue_score ? 'bg-gray-100 dark:bg-gray-800' : ''}`}>
                      <div 
                        className="font-bold text-[12px] text-gray-800 dark:text-gray-200 cursor-pointer w-full"
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
                            ? 'bg-gray-800 border-gray-800 text-white dark:bg-gray-200 dark:text-black' 
                            : 'bg-white border-gray-200 text-gray-500 dark:bg-gray-800'
                        }`}
                      >
                        <span className="text-[10px] font-black leading-none">{m.status === 'completed' && m.white_score > m.blue_score ? 'WIN' : '승'}</span>
                      </button>
                    </div>"""

new_white = """                    {/* 백팀 */}
                    <div className={`p-3 flex justify-between items-center flex-1 ${m.status === 'completed' && m.white_score > m.blue_score ? 'bg-gray-100 dark:bg-gray-800' : ''}`}>
                      <div 
                        className="font-black text-sm sm:text-base text-gray-700 dark:text-gray-300 cursor-pointer w-full flex flex-col justify-center min-w-0 pr-2"
                        onClick={() => editPlayers(m.id, 'white', m.white_player1, m.white_player2)}
                      >
                        <div className="truncate w-full">{m.white_player1}</div>
                        <div className="truncate w-full">{m.white_player2}</div>
                        {whitePen && whitePen !== '0' && <div className="text-[10px] font-bold text-red-500 mt-0.5">패널티 {whitePen}</div>}
                      </div>
                      <button 
                        onClick={() => setWinner(m.id, 'white')} 
                        className={`w-10 h-10 flex justify-center items-center rounded-full border shrink-0 shadow-sm transition-all ${
                          m.status === 'completed' && m.white_score > m.blue_score 
                            ? 'bg-gray-700 border-gray-700 text-white dark:bg-gray-200 dark:text-black' 
                            : 'bg-white border-gray-300 text-gray-600 hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-400'
                        }`}
                      >
                        <span className="text-xs sm:text-sm font-black leading-none">{m.status === 'completed' && m.white_score > m.blue_score ? 'WIN' : '승'}</span>
                      </button>
                    </div>"""

content = content.replace(old_white, new_white)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
