import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Add states
state_addition = """
  const [numCourts, setNumCourts] = useState(3);
  const [numRounds, setNumRounds] = useState(5);
"""
content = content.replace('const [isGenerating, setIsGenerating] = useState(false);', 'const [isGenerating, setIsGenerating] = useState(false);\n' + state_addition)

# 2. Modify handleGenerate
handle_gen_old = "const matches = generateMatches(activePlayers, 'TEAM', 7);"
handle_gen_new = "const matches = generateMatches(activePlayers, 'TEAM', numCourts, numRounds);"
content = content.replace(handle_gen_old, handle_gen_new)

# 3. Modify saveTournament
save_t_old = """      round_num: Math.floor(i / 3) + 1,
      court_num: (i % 3) + 1,"""
save_t_new = """      round_num: m.round_num || Math.floor(i / numCourts) + 1,
      court_num: m.court_num || (i % numCourts) + 1,"""
content = content.replace(save_t_old, save_t_new)

# 4. UI: Add settings panel before "알고리즘으로 대진표 짜기"
btn_old = """                <button 
                  onClick={handleGenerate}
                  disabled={isGenerating || selectedPlayerIds.size < 4}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50 transition-all shadow-md"
                >"""

btn_new = """                <div className="flex gap-2">
                  <div className="flex-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-3 flex flex-col justify-center">
                    <label className="text-xs text-gray-500 font-bold mb-1">코트 수</label>
                    <div className="flex items-center gap-2">
                      <input type="number" min="1" max="10" value={numCourts} onChange={e => setNumCourts(parseInt(e.target.value) || 1)} className="w-full bg-transparent font-bold outline-none" />
                      <span className="text-sm text-gray-400">면</span>
                    </div>
                  </div>
                  <div className="flex-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-3 flex flex-col justify-center">
                    <label className="text-xs text-gray-500 font-bold mb-1">총 라운드</label>
                    <div className="flex items-center gap-2">
                      <input type="number" min="1" max="20" value={numRounds} onChange={e => setNumRounds(parseInt(e.target.value) || 1)} className="w-full bg-transparent font-bold outline-none" />
                      <span className="text-sm text-gray-400">R</span>
                    </div>
                  </div>
                </div>

                <button 
                  onClick={handleGenerate}
                  disabled={isGenerating || selectedPlayerIds.size < 4}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50 transition-all shadow-md mt-2"
                >"""
content = content.replace(btn_old, btn_new)


# 5. Fix preview UI to show Round and Court
preview_old = """                          <span className="text-xs font-black text-blue-600 bg-blue-50 px-2 py-1 rounded w-max">청팀</span>"""
preview_new = """                          <span className="text-xs font-black text-gray-500 mb-1">{m.round_num}R - {m.court_num}코트</span>
                          <span className="text-xs font-black text-blue-600 bg-blue-50 px-2 py-1 rounded w-max">청팀</span>"""
content = content.replace(preview_old, preview_new)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
