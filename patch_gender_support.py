import re

# 1. Update types.ts
with open('src/lib/types.ts', 'r') as f:
    types_content = f.read()

types_content = types_content.replace(
    "default_penalty?: number;",
    "default_penalty?: number;\n  gender?: 'M' | 'F';"
).replace(
    "default_penalty: number;",
    "default_penalty: number;\n  gender?: 'M' | 'F';"
)

with open('src/lib/types.ts', 'w') as f:
    f.write(types_content)

# 2. Update matchMaker.ts
with open('src/lib/matchMaker.ts', 'r') as f:
    mm_content = f.read()

helper_func = """export const getGradeValue = (grade: string): number => {"""
new_helper = """export const getMatchTypeLabel = (team1: Player[], team2: Player[]) => {
  const allPlayers = [...team1, ...team2];
  const mCount = allPlayers.filter(p => p.gender === 'M' || !p.gender).length;
  const fCount = allPlayers.filter(p => p.gender === 'F').length;
  
  if (fCount === 0) return 'MD';
  if (mCount === 0) return 'WD';
  return 'XD';
};

export const getGradeValue = (grade: string): number => {"""
mm_content = mm_content.replace(helper_func, new_helper)

mm_content = mm_content.replace(
    "match_type: 'MD',",
    "match_type: getMatchTypeLabel(bluePairs[i], whitePairs[i]),"
)

with open('src/lib/matchMaker.ts', 'w') as f:
    f.write(mm_content)

# 3. Update admin/page.tsx
with open('src/app/admin/page.tsx', 'r') as f:
    admin_content = f.read()

# 3.1 State for guest
admin_content = admin_content.replace(
    'const [guestGrade, setGuestGrade] = useState("E");',
    'const [guestGrade, setGuestGrade] = useState("E");\n  const [guestGender, setGuestGender] = useState<"M"|"F">("M");'
)

admin_content = admin_content.replace(
    'setGuestGrade("E");',
    'setGuestGrade("E");\n    setGuestGender("M");'
)

admin_content = admin_content.replace(
    'insert({ name: guestName.trim(), grade: guestGrade })',
    'insert({ name: guestName.trim(), grade: guestGrade, gender: guestGender })'
)

# 3.2 Update Player function
old_update_grade = """  const updatePlayerGrade = async (id: string, newGrade: string) => {
    await supabase.from('players').update({ grade: newGrade }).eq('id', id);
    setDbPlayers(dbPlayers.map(p => p.id === id ? { ...p, grade: newGrade } : p).sort((a, b) => a.grade.localeCompare(b.grade)));
  };"""

new_update_player = """  const updatePlayer = async (id: string, updates: Partial<Player>) => {
    await supabase.from('players').update(updates).eq('id', id);
    setDbPlayers(dbPlayers.map(p => p.id === id ? { ...p, ...updates } : p).sort((a, b) => a.grade.localeCompare(b.grade)));
  };"""
admin_content = admin_content.replace(old_update_grade, new_update_player)

# 3.3 Player Manage UI
old_player_row = """                      <select 
                        value={p.grade} 
                        onChange={(e) => updatePlayerGrade(p.id, e.target.value)}
                        className="bg-gray-100 dark:bg-gray-800 text-sm font-bold px-2 py-1 rounded outline-none border border-transparent focus:border-blue-500"
                      >"""

new_player_row = """                      <div className="flex gap-2">
                        <select 
                          value={p.gender || 'M'} 
                          onChange={(e) => updatePlayer(p.id, { gender: e.target.value as 'M'|'F' })}
                          className="bg-gray-100 dark:bg-gray-800 text-sm font-bold px-2 py-1 rounded outline-none border border-transparent focus:border-blue-500"
                        >
                          <option value="M">남</option>
                          <option value="F">여</option>
                        </select>
                        <select 
                          value={p.grade} 
                          onChange={(e) => updatePlayer(p.id, { grade: e.target.value })}
                          className="bg-gray-100 dark:bg-gray-800 text-sm font-bold px-2 py-1 rounded outline-none border border-transparent focus:border-blue-500"
                        >"""
admin_content = admin_content.replace(old_player_row, new_player_row)
# Close the div
admin_content = admin_content.replace(
    '</select>\n                    </div>\n                  </div>',
    '</select>\n                      </div>\n                    </div>\n                  </div>'
)

# 3.4 Guest Add UI
old_guest_grade = """              <div className="relative">
                <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">급수</label>
                <select 
                  value={guestGrade} 
                  onChange={(e) => setGuestGrade(e.target.value)}"""

new_guest_grade = """              <div className="flex gap-4">
                <div className="flex-1 relative">
                  <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">성별</label>
                  <select 
                    value={guestGender} 
                    onChange={(e) => setGuestGender(e.target.value as 'M'|'F')}
                    className="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all font-medium cursor-pointer appearance-none"
                  >
                    <option value="M">남성</option>
                    <option value="F">여성</option>
                  </select>
                  <ChevronDown className="absolute right-4 top-10 w-5 h-5 text-gray-400 pointer-events-none" />
                </div>
                <div className="flex-1 relative">
                  <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">급수</label>
                  <select 
                    value={guestGrade} 
                    onChange={(e) => setGuestGrade(e.target.value)}"""
admin_content = admin_content.replace(old_guest_grade, new_guest_grade)

admin_content = admin_content.replace(
    '</select>\n                <ChevronDown className="absolute right-4 top-10 w-5 h-5 text-gray-400 pointer-events-none" />\n              </div>\n            </div>\n            <button',
    '</select>\n                  <ChevronDown className="absolute right-4 top-10 w-5 h-5 text-gray-400 pointer-events-none" />\n                </div>\n              </div>\n            </div>\n            <button'
)


with open('src/app/admin/page.tsx', 'w') as f:
    f.write(admin_content)
