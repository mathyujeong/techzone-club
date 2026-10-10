import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

old_gen_list = """                  {dbPlayers.map(p => (
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
                  ))}"""

new_gen_list = """                  {dbPlayers.map(p => (
                    <div key={p.id} className="flex items-center justify-between p-1.5 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg group transition-colors">
                      <label className="flex items-center gap-2 cursor-pointer flex-1">
                        <input 
                          type="checkbox" 
                          className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500 border-gray-300 cursor-pointer"
                          checked={selectedPlayerIds.has(p.id)}
                          onChange={(e) => {
                            const next = new Set(selectedPlayerIds);
                            if (e.target.checked) next.add(p.id);
                            else next.delete(p.id);
                            setSelectedPlayerIds(next);
                          }}
                        />
                        <span className="font-bold text-sm text-gray-800 dark:text-gray-200">{p.name}</span>
                      </label>
                      <div className="flex gap-1 items-center bg-white dark:bg-gray-900 rounded-md border border-gray-200 dark:border-gray-700 p-0.5">
                        <select 
                          value={p.gender || 'M'} 
                          onChange={(e) => updatePlayer(p.id, { gender: e.target.value })}
                          className="bg-transparent text-xs font-bold text-blue-600 dark:text-blue-400 outline-none cursor-pointer px-1 py-0.5 appearance-none text-center"
                        >
                          <option value="M">남</option>
                          <option value="F">여</option>
                        </select>
                        <div className="w-px h-3 bg-gray-200 dark:bg-gray-700"></div>
                        <select 
                          value={p.grade} 
                          onChange={(e) => updatePlayer(p.id, { grade: e.target.value })}
                          className="bg-transparent text-xs font-bold text-gray-600 dark:text-gray-400 outline-none cursor-pointer px-1 py-0.5 appearance-none text-center"
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
                  ))}"""

content = content.replace(old_gen_list, new_gen_list)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
