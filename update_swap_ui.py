import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Add activePlayers at the top of the render logic
if "const activePlayersForDropdown =" not in content:
    content = content.replace("const handleGenerate = () => {", """const activePlayersForDropdown = dbPlayers.filter(p => selectedPlayerIds.has(p.id)).sort((a,b) => a.name.localeCompare(b.name));\n  const handleGenerate = () => {""")

# 2. Replace the buttons with <select>

old_blue0 = """<button onClick={() => handleSwapGenerated(idx, 'blue', 0)} className="flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-800 hover:bg-blue-50 hover:text-blue-600 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent transition-all group min-w-0">
                              <span className="truncate">{m.blue_team[0].name}</span>
                              {<span className="text-[10px] font-black text-gray-400 group-hover:text-blue-400 ml-1 shrink-0">{m.blue_team[0].grade}</span>}
                            </button>"""
new_blue0 = """<select 
                              value={m.blue_team[0].name} 
                              onChange={e => handleSwapGenerated(idx, 'blue', 0, e.target.value)} 
                              className="appearance-none cursor-pointer flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-800 hover:bg-blue-50 hover:text-blue-600 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent transition-all group min-w-0 outline-none"
                            >
                              <option value={m.blue_team[0].name}>{m.blue_team[0].name} ({m.blue_team[0].grade})</option>
                              <optgroup label="교체 대상 선택">
                                {activePlayersForDropdown.filter(p => p.name !== m.blue_team[0].name).map(p => (
                                  <option key={p.id} value={p.name}>{p.name} ({p.grade})</option>
                                ))}
                              </optgroup>
                            </select>"""
content = content.replace(old_blue0, new_blue0)

old_blue1 = """<button onClick={() => handleSwapGenerated(idx, 'blue', 1)} className="flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-800 hover:bg-blue-50 hover:text-blue-600 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent transition-all group min-w-0">
                              <span className="truncate">{m.blue_team[1].name}</span>
                              {<span className="text-[10px] font-black text-gray-400 group-hover:text-blue-400 ml-1 shrink-0">{m.blue_team[1].grade}</span>}
                            </button>"""
new_blue1 = """<select 
                              value={m.blue_team[1].name} 
                              onChange={e => handleSwapGenerated(idx, 'blue', 1, e.target.value)} 
                              className="appearance-none cursor-pointer flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-800 hover:bg-blue-50 hover:text-blue-600 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent transition-all group min-w-0 outline-none"
                            >
                              <option value={m.blue_team[1].name}>{m.blue_team[1].name} ({m.blue_team[1].grade})</option>
                              <optgroup label="교체 대상 선택">
                                {activePlayersForDropdown.filter(p => p.name !== m.blue_team[1].name).map(p => (
                                  <option key={p.id} value={p.name}>{p.name} ({p.grade})</option>
                                ))}
                              </optgroup>
                            </select>"""
content = content.replace(old_blue1, new_blue1)


old_white0 = """<button onClick={() => handleSwapGenerated(idx, 'white', 0)} className="flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 hover:text-gray-800 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent transition-all group min-w-0">
                              <span className="truncate">{m.white_team[0].name}</span>
                              {<span className="text-[10px] font-black text-gray-400 group-hover:text-gray-500 ml-1 shrink-0">{m.white_team[0].grade}</span>}
                            </button>"""
new_white0 = """<select 
                              value={m.white_team[0].name} 
                              onChange={e => handleSwapGenerated(idx, 'white', 0, e.target.value)} 
                              className="appearance-none cursor-pointer flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 hover:text-gray-800 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent transition-all group min-w-0 outline-none"
                            >
                              <option value={m.white_team[0].name}>{m.white_team[0].name} ({m.white_team[0].grade})</option>
                              <optgroup label="교체 대상 선택">
                                {activePlayersForDropdown.filter(p => p.name !== m.white_team[0].name).map(p => (
                                  <option key={p.id} value={p.name}>{p.name} ({p.grade})</option>
                                ))}
                              </optgroup>
                            </select>"""
content = content.replace(old_white0, new_white0)

old_white1 = """<button onClick={() => handleSwapGenerated(idx, 'white', 1)} className="flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 hover:text-gray-800 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent transition-all group min-w-0">
                              <span className="truncate">{m.white_team[1].name}</span>
                              {<span className="text-[10px] font-black text-gray-400 group-hover:text-gray-500 ml-1 shrink-0">{m.white_team[1].grade}</span>}
                            </button>"""
new_white1 = """<select 
                              value={m.white_team[1].name} 
                              onChange={e => handleSwapGenerated(idx, 'white', 1, e.target.value)} 
                              className="appearance-none cursor-pointer flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 hover:text-gray-800 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent transition-all group min-w-0 outline-none"
                            >
                              <option value={m.white_team[1].name}>{m.white_team[1].name} ({m.white_team[1].grade})</option>
                              <optgroup label="교체 대상 선택">
                                {activePlayersForDropdown.filter(p => p.name !== m.white_team[1].name).map(p => (
                                  <option key={p.id} value={p.name}>{p.name} ({p.grade})</option>
                                ))}
                              </optgroup>
                            </select>"""
content = content.replace(old_white1, new_white1)


with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
