with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. State
state_old = """  const [ignoreGrade, setIgnoreGrade] = useState(false);
  const [hideGrade, setHideGrade] = useState(false);"""
state_new = """  const [ignoreGrade, setIgnoreGrade] = useState(false);
  const [hideGrade, setHideGrade] = useState(false);
  const [matchType, setMatchType] = useState<'TEAM' | 'INDIVIDUAL'>('TEAM');"""
content = content.replace(state_old, state_new)

# 2. handleGenerate Call
content = content.replace("generateMatches(activePlayers, 'TEAM', numCourts, numRounds, ignoreGrade);", "generateMatches(activePlayers, matchType, numCourts, numRounds, ignoreGrade);")

# 3. Add UI to the generator modal options
ui_old = """                <div className="flex gap-2 shrink-0">
                  <div className="flex-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-2 flex flex-col justify-center">"""
ui_new = """                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-3 shrink-0">
                  <label className="text-xs text-gray-500 font-bold mb-1 block">경기 방식</label>
                  <select 
                    value={matchType} 
                    onChange={e => setMatchType(e.target.value as 'TEAM' | 'INDIVIDUAL')}
                    className="w-full bg-transparent font-bold outline-none cursor-pointer"
                  >
                    <option value="TEAM">청백전 (팀전)</option>
                    <option value="INDIVIDUAL">개인전 (랜덤 매치)</option>
                  </select>
                </div>
                <div className="flex gap-2 shrink-0">
                  <div className="flex-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-2 flex flex-col justify-center">"""
content = content.replace(ui_old, ui_new)

# 4. Update the preview badges (Blue Team)
blue_old = """<span className="text-xs font-black text-blue-600 bg-blue-50 px-2 py-1 rounded w-max">청팀</span>"""
blue_new = """<span className={`text-xs font-black px-2 py-1 rounded w-max ${matchType === 'TEAM' ? 'text-blue-600 bg-blue-50' : 'text-gray-600 bg-gray-100 dark:bg-gray-800'}`}>{matchType === 'TEAM' ? '청팀' : 'A조'}</span>"""
content = content.replace(blue_old, blue_new)

# Update the preview badges (White Team)
white_old = """<span className="text-xs font-black text-gray-600 bg-gray-100 px-2 py-1 rounded w-max">백팀</span>"""
white_new = """<span className="text-xs font-black text-gray-600 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded w-max">{matchType === 'TEAM' ? '백팀' : 'B조'}</span>"""
content = content.replace(white_old, white_new)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
