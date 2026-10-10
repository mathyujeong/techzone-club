import re

# 1. Update Admin page
with open('src/app/admin/page.tsx', 'r') as f:
    admin = f.read()

# Pass manualBlue and manualWhite to generateMatches
old_gen_call = "const matches = generateMatches(activePlayers, matchType, numCourts, numRounds, ignoreGrade);"
new_gen_call = """const manualBlue = activePlayers.filter(p => teamAssignments[p.id] !== 'WHITE');
      const manualWhite = activePlayers.filter(p => teamAssignments[p.id] === 'WHITE');
      const matches = generateMatches(activePlayers, matchType, numCourts, numRounds, ignoreGrade, manualBlue, manualWhite);"""
admin = admin.replace(old_gen_call, new_gen_call)

# Add court count warning in generator modal
old_gen_header = '<h3 className="font-bold text-gray-800 dark:text-gray-200">참가자 선택</h3>'
new_gen_header = """<div className="flex flex-col gap-1">
                      <h3 className="font-bold text-gray-800 dark:text-gray-200">참가자 선택</h3>
                      {selectedPlayerIds.size > 0 && selectedPlayerIds.size < numCourts * 4 && (
                        <span className="text-[11px] text-amber-600 dark:text-amber-400 font-medium">
                          ⚠️ {selectedPlayerIds.size}명 선택됨 (코트당 4명 필요하여 최대 {Math.floor(selectedPlayerIds.size / 4)}개 코트만 배정됩니다)
                        </span>
                      )}
                    </div>"""
admin = admin.replace(old_gen_header, new_gen_header)

# Preview Labels: Hide team/group label completely in INDIVIDUAL mode
old_preview_blue = """<span className={`text-[10px] font-black px-2 py-0.5 rounded w-max mb-0.5 ${matchType === 'TEAM' ? 'text-blue-600 bg-blue-50' : 'text-gray-600 bg-gray-100 dark:bg-gray-800'}`}>{matchType === 'TEAM' ? '청팀' : 'A조'}</span>"""
new_preview_blue = """{matchType === 'TEAM' && <span className="text-[10px] font-black px-2 py-0.5 rounded w-max mb-0.5 text-blue-600 bg-blue-50">청팀</span>}"""
admin = admin.replace(old_preview_blue, new_preview_blue)

old_preview_white = """<span className={`text-[10px] font-black px-2 py-0.5 rounded w-max mb-0.5 ${matchType === 'TEAM' ? 'text-gray-600 bg-gray-100 dark:bg-gray-800' : 'text-gray-600 bg-gray-100 dark:bg-gray-800'}`}>{matchType === 'TEAM' ? '백팀' : 'B조'}</span>"""
new_preview_white = """{matchType === 'TEAM' && <span className="text-[10px] font-black px-2 py-0.5 rounded w-max mb-0.5 text-gray-600 bg-gray-100 dark:bg-gray-800">백팀</span>}"""
admin = admin.replace(old_preview_white, new_preview_white)

# Admin Main Match Cards: Hide team/group label in INDIVIDUAL mode
old_admin_blue_header = """<span>{isIndividualMode ? 'A조' : '청팀'} {bluePen && bluePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {bluePen}</span>}</span>"""
new_admin_blue_header = """<span>{!isIndividualMode && '청팀'} {bluePen && bluePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {bluePen}</span>}</span>"""
admin = admin.replace(old_admin_blue_header, new_admin_blue_header)

old_admin_white_header = """<span>{isIndividualMode ? 'B조' : '백팀'} {whitePen && whitePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {whitePen}</span>}</span>"""
new_admin_white_header = """<span>{!isIndividualMode && '백팀'} {whitePen && whitePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {whitePen}</span>}</span>"""
admin = admin.replace(old_admin_white_header, new_admin_white_header)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(admin)

# 2. Update Member page
with open('src/app/tournament/page.tsx', 'r') as f:
    member = f.read()

old_member_blue = """<div className="text-xs font-black text-blue-600 dark:text-blue-400 mb-2 flex justify-center items-center gap-1">{activeTournament?.match_type === 'INDIVIDUAL' ? 'A조' : '청팀'} {bluePen && bluePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {bluePen}</span>}</div>"""
new_member_blue = """<div className="text-xs font-black text-blue-600 dark:text-blue-400 mb-2 flex justify-center items-center gap-1">{activeTournament?.match_type !== 'INDIVIDUAL' && '청팀'} {bluePen && bluePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {bluePen}</span>}</div>"""
member = member.replace(old_member_blue, new_member_blue)

old_member_white = """<div className="text-xs font-black text-gray-600 dark:text-gray-400 mb-2 flex justify-center items-center gap-1">{activeTournament?.match_type === 'INDIVIDUAL' ? 'B조' : '백팀'} {whitePen && whitePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {whitePen}</span>}</div>"""
new_member_white = """<div className="text-xs font-black text-gray-600 dark:text-gray-400 mb-2 flex justify-center items-center gap-1">{activeTournament?.match_type !== 'INDIVIDUAL' && '백팀'} {whitePen && whitePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {whitePen}</span>}</div>"""
member = member.replace(old_member_white, new_member_white)

with open('src/app/tournament/page.tsx', 'w') as f:
    f.write(member)

