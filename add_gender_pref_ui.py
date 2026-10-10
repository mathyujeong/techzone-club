import re

with open('src/app/admin/page.tsx', 'r') as f:
    admin = f.read()

# 1. Add state
old_state = "const [matchType, setMatchType] = useState<'TEAM' | 'INDIVIDUAL'>('TEAM');"
new_state = """const [matchType, setMatchType] = useState<'TEAM' | 'INDIVIDUAL'>('TEAM');
  const [genderPref, setGenderPref] = useState<'SAME_GENDER' | 'MIXED'>('SAME_GENDER');"""
admin = admin.replace(old_state, new_state)

# 2. Update handleGenerate call
old_gen_call = "const matches = generateMatches(activePlayers, matchType, numCourts, numRounds, ignoreGrade, manualBlue, manualWhite);"
new_gen_call = "const matches = generateMatches(activePlayers, matchType, numCourts, numRounds, ignoreGrade, manualBlue, manualWhite, genderPref === 'SAME_GENDER');"
admin = admin.replace(old_gen_call, new_gen_call)

# 3. Add Dropdown UI in top settings panel of Generator Modal
old_settings_panel = """                  <div className="w-full sm:w-auto">
                    <label className="text-xs text-gray-500 font-bold mb-1 block">경기 방식</label>
                    <select 
                      value={matchType} 
                      onChange={e => setMatchType(e.target.value as 'TEAM' | 'INDIVIDUAL')}
                      className="w-full sm:w-auto bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-3 py-2 rounded-xl font-bold outline-none cursor-pointer"
                    >
                      <option value="TEAM">청백전 (팀전)</option>
                      <option value="INDIVIDUAL">개인전 (랜덤 매치)</option>
                    </select>
                  </div>"""

new_settings_panel = """                  <div className="w-full sm:w-auto">
                    <label className="text-xs text-gray-500 font-bold mb-1 block">경기 방식</label>
                    <select 
                      value={matchType} 
                      onChange={e => setMatchType(e.target.value as 'TEAM' | 'INDIVIDUAL')}
                      className="w-full sm:w-auto bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-3 py-2 rounded-xl font-bold outline-none cursor-pointer"
                    >
                      <option value="TEAM">청백전 (팀전)</option>
                      <option value="INDIVIDUAL">개인전 (랜덤 매치)</option>
                    </select>
                  </div>

                  <div className="w-full sm:w-auto">
                    <label className="text-xs text-gray-500 font-bold mb-1 block">종목 선호</label>
                    <select 
                      value={genderPref} 
                      onChange={e => setGenderPref(e.target.value as 'SAME_GENDER' | 'MIXED')}
                      className="w-full sm:w-auto bg-indigo-50 dark:bg-indigo-950/50 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 px-3 py-2 rounded-xl font-bold outline-none cursor-pointer"
                    >
                      <option value="SAME_GENDER">남복/여복 우선 (추천)</option>
                      <option value="MIXED">혼복 포함 (랜덤)</option>
                    </select>
                  </div>"""

admin = admin.replace(old_settings_panel, new_settings_panel)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(admin)

