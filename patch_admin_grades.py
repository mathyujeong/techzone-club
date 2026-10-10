with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. State
state_old = """  const [numCourts, setNumCourts] = useState(3);
  const [numRounds, setNumRounds] = useState(5);"""

state_new = """  const [numCourts, setNumCourts] = useState(3);
  const [numRounds, setNumRounds] = useState(5);
  const [ignoreGrade, setIgnoreGrade] = useState(false);
  const [hideGrade, setHideGrade] = useState(false);"""
content = content.replace(state_old, state_new)

# 2. Call
content = content.replace("generateMatches(activePlayers, 'TEAM', numCourts, numRounds);", "generateMatches(activePlayers, 'TEAM', numCourts, numRounds, ignoreGrade);")

# 3. Checkboxes UI
btn_old = """                <button 
                  onClick={handleGenerate}
                  disabled={isGenerating || selectedPlayerIds.size < 4}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50 transition-all shadow-md mt-2"
                >"""

btn_new = """                <div className="flex gap-4 mt-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-3">
                  <label className="flex items-center gap-2 text-xs font-bold text-gray-700 dark:text-gray-300 cursor-pointer">
                    <input type="checkbox" checked={ignoreGrade} onChange={e => setIgnoreGrade(e.target.checked)} className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500" />
                    급수 무관 (랜덤 편성)
                  </label>
                  <label className="flex items-center gap-2 text-xs font-bold text-gray-700 dark:text-gray-300 cursor-pointer">
                    <input type="checkbox" checked={hideGrade} onChange={e => setHideGrade(e.target.checked)} className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500" />
                    대진표 급수 숨기기
                  </label>
                </div>
                <button 
                  onClick={handleGenerate}
                  disabled={isGenerating || selectedPlayerIds.size < 4}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50 transition-all shadow-md mt-2"
                >"""
content = content.replace(btn_old, btn_new)

# 4. Preview modification
preview_grades = [
    "{m.blue_team[0].grade}</span>",
    "{m.blue_team[1].grade}</span>",
    "{m.white_team[0].grade}</span>",
    "{m.white_team[1].grade}</span>",
]

for g in preview_grades:
    old_span = f'<span className="text-xs font-normal text-gray-400 ml-1">{g}'
    new_span = f'{{!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{g}}}'
    content = content.replace(old_span, new_span)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
