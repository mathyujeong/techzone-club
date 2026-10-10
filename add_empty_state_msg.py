import re

# 1. Admin page
with open('src/app/admin/page.tsx', 'r') as f:
    admin = f.read()

old_admin_grid = """          {isIndividualMode ? (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
              {individualStats.map(s => ("""

new_admin_grid = """          {isIndividualMode ? (
            individualStats.length === 0 ? (
              <div className="text-center py-8 text-gray-400 text-sm font-medium">
                아직 생성된 경기가 없습니다. 상단의 [새 대진표 자동생성] 버튼을 누르면 출전 선수별 성적이 여기에 표시됩니다.
              </div>
            ) : (
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
                {individualStats.map(s => ("""

admin = admin.replace(old_admin_grid, new_admin_grid)
admin = admin.replace("              ))}\n            </div>\n          ) : (", "              ))}\n            </div>\n            )\n          ) : (")

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(admin)

# 2. Member page
with open('src/app/tournament/page.tsx', 'r') as f:
    member = f.read()

old_member_grid = """          {isIndividualMode ? (
            <div className="flex flex-col gap-2">
              {individualStats.map(s => {"""

new_member_grid = """          {isIndividualMode ? (
            individualStats.length === 0 ? (
              <div className="text-center py-6 text-gray-400 text-xs font-medium">
                아직 생성된 경기가 없습니다.
              </div>
            ) : (
              <div className="flex flex-col gap-2">
                {individualStats.map(s => {"""

member = member.replace(old_member_grid, new_member_grid)
member = member.replace("              })}\n            </div>\n          ) : (", "              })}\n            </div>\n            )\n          ) : (")

with open('src/app/tournament/page.tsx', 'w') as f:
    f.write(member)

