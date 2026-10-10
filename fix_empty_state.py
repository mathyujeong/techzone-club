import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# Remove the broken `</>)}`
content = content.replace("                </>\n        )}\n\n        {/* --- 대진표 자동 생성 모달 --- */}", "{/* --- 대진표 자동 생성 모달 --- */}")

# Find the start of `<main...>`
main_start_regex = r'(<main className="flex-1 overflow-y-auto h-screen pb-20">)\s*({/\* 상단 헤더 \*/})'

replacement = r'''\1
        {!selectedTournamentId ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-400 dark:text-gray-600 bg-gray-50/50 dark:bg-gray-950/50">
            <Trophy className="w-16 h-16 mb-4 opacity-20" />
            <p className="font-bold text-lg text-gray-500">왼쪽 목록에서 대회를 선택해주세요.</p>
            <p className="text-sm mt-2">새로운 월례회를 시작하려면 좌측의 [새 대회 추가]를 눌러주세요.</p>
          </div>
        ) : (
          <>
            \2'''

content = re.sub(main_start_regex, replacement, content)

# Now put the `</>)}` back before the modal
modal_start = "{/* --- 대진표 자동 생성 모달 --- */}"
content = content.replace(modal_start, "          </>\n        )}\n\n      " + modal_start)

# Change button text
content = content.replace('새 대회 생성', '새 대회 추가')

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
