import re

with open('src/app/admin/page.tsx', 'r') as f:
    text = f.read()

# Remove the broken `</>)}` tags that were floating
text = text.replace("          </>\n        )}\n\n      {/* --- 대진표 자동 생성 모달 --- */}", "{/* --- 대진표 자동 생성 모달 --- */}")
text = text.replace("                </>\n        )}\n\n        {/* --- 대진표 자동 생성 모달 --- */}", "{/* --- 대진표 자동 생성 모달 --- */}")
text = text.replace("                </>\n        )}", "")
text = text.replace("          </>\n        )}", "")
text = text.replace("          </>\n        )}\n", "")

# Now text is clean. Let's insert the ternary logic.

empty_state = """
        {!selectedTournamentId ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-400 dark:text-gray-600 bg-gray-50/50 dark:bg-gray-950/50 py-32">
            <Trophy className="w-16 h-16 mb-4 opacity-20" />
            <p className="font-bold text-lg text-gray-500">왼쪽 목록에서 대회를 선택해주세요.</p>
            <p className="text-sm mt-2">새로운 월례회를 시작하려면 좌측의 [새 대회 추가]를 눌러주세요.</p>
          </div>
        ) : (
          <>
      {/* 상단 헤더 */}"""

text = text.replace("      {/* 상단 헤더 */}", empty_state)

# Close it before the modal
modal_comment = "{/* --- 대진표 자동 생성 모달 --- */}"
text = text.replace(modal_comment, "          </>\n        )}\n\n      " + modal_comment)

# Remove the auto-select if it exists
auto_select_code1 = """  // set selected tournament when tournaments load
  useEffect(() => {
    if (tournaments.length > 0 && !selectedTournamentId) {
      // Find IN_PROGRESS first, otherwise first in list
      const active = tournaments.find(t => t.status === 'IN_PROGRESS') || tournaments[0];
      setSelectedTournamentId(active.id);
    }
  }, [tournaments]);"""
text = text.replace(auto_select_code1, "")

# rename button
text = text.replace('새 대회 생성', '새 대회 추가')

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(text)
