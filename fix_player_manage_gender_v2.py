import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

old_ui = """                    <span className="text-xs text-gray-400">급수 변경:</span>
                    <select 
                      value={p.grade}
                      onChange={(e) => updatePlayerGrade(p.id, e.target.value)}
                      className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg px-2 py-1 font-bold outline-none cursor-pointer"
                    >
                      <option value="S">S급</option>
                      <option value="A">A급</option>
                      <option value="B">B급</option>
                      <option value="C">C급</option>
                      <option value="D">D급</option>
                      <option value="E">E급</option>
                    </select>"""

new_ui = """                    <span className="text-xs text-gray-400">성별/급수:</span>
                    <div className="flex gap-1">
                      <select 
                        value={p.gender || 'M'} 
                        onChange={(e) => updatePlayer(p.id, { gender: e.target.value })}
                        className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg px-2 py-1 font-bold outline-none cursor-pointer text-blue-600 dark:text-blue-400"
                      >
                        <option value="M">남</option>
                        <option value="F">여</option>
                      </select>
                      <select 
                        value={p.grade} 
                        onChange={(e) => updatePlayer(p.id, { grade: e.target.value })}
                        className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg px-2 py-1 font-bold outline-none cursor-pointer"
                      >
                        <option value="S">S급</option>
                        <option value="A">A급</option>
                        <option value="B">B급</option>
                        <option value="C">C급</option>
                        <option value="D">D급</option>
                        <option value="E">E급</option>
                      </select>
                    </div>"""
content = content.replace(old_ui, new_ui)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
