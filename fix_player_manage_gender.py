import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Update updatePlayerGrade to updatePlayer
old_func = """  const updatePlayerGrade = async (id: string, newGrade: string) => {
    await supabase.from('players').update({ grade: newGrade as any }).eq('id', id);
    setDbPlayers(dbPlayers.map(p => p.id === id ? { ...p, grade: newGrade as any } : p));
  };"""

new_func = """  const updatePlayer = async (id: string, updates: any) => {
    await supabase.from('players').update(updates).eq('id', id);
    setDbPlayers(dbPlayers.map(p => p.id === id ? { ...p, ...updates } : p).sort((a, b) => a.grade.localeCompare(b.grade)));
  };"""
content = content.replace(old_func, new_func)


# 2. Update the UI in the player list
old_ui = """                      <select 
                        value={p.grade} 
                        onChange={(e) => updatePlayerGrade(p.id, e.target.value)}
                        className="bg-gray-100 dark:bg-gray-800 text-sm font-bold px-2 py-1 rounded outline-none border border-transparent focus:border-blue-500"
                      >
                        <option value="S">S급</option>
                        <option value="A">A급</option>
                        <option value="B">B급</option>
                        <option value="C">C급</option>
                        <option value="D">D급</option>
                        <option value="E">E급</option>
                      </select>
                    </div>
                  </div>"""

new_ui = """                      <div className="flex gap-2">
                        <select 
                          value={p.gender || 'M'} 
                          onChange={(e) => updatePlayer(p.id, { gender: e.target.value })}
                          className="bg-gray-100 dark:bg-gray-800 text-sm font-bold px-2 py-1 rounded outline-none border border-transparent focus:border-blue-500 cursor-pointer"
                        >
                          <option value="M">남</option>
                          <option value="F">여</option>
                        </select>
                        <select 
                          value={p.grade} 
                          onChange={(e) => updatePlayer(p.id, { grade: e.target.value })}
                          className="bg-gray-100 dark:bg-gray-800 text-sm font-bold px-2 py-1 rounded outline-none border border-transparent focus:border-blue-500 cursor-pointer"
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
                  </div>"""
content = content.replace(old_ui, new_ui)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
