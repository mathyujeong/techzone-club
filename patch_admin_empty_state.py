import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Change button text
content = content.replace('새 대회 생성', '새 대회 추가')

# 2. Remove the auto-select useEffect
auto_select_code = """  // set selected tournament when tournaments load
  useEffect(() => {
    if (tournaments.length > 0 && !selectedTournamentId) {
      // Find IN_PROGRESS first, otherwise first in list
      const active = tournaments.find(t => t.status === 'IN_PROGRESS') || tournaments[0];
      setSelectedTournamentId(active.id);
    }
  }, [tournaments]);"""
content = content.replace(auto_select_code, "")

# 3. Wrap the main content with the empty state logic
# The main content starts at: {/* 상단 헤더 */}
# and ends right before: {/* --- 대진표 자동 생성 모달 --- */}

empty_state = """      {/* Main Content */}
      <main className="flex-1 overflow-y-auto h-screen pb-20">
        {!selectedTournamentId ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-400 dark:text-gray-600 bg-gray-50/50 dark:bg-gray-950/50">
            <Trophy className="w-16 h-16 mb-4 opacity-20" />
            <p className="font-bold text-lg text-gray-500">왼쪽 목록에서 대회를 선택해주세요.</p>
            <p className="text-sm mt-2">새로운 월례회를 시작하려면 좌측의 [새 대회 추가]를 눌러주세요.</p>
          </div>
        ) : (
          <>
            {/* 상단 헤더 */}"""

# We replace the <main> opening and the header comment
content = content.replace('      {/* Main Content */}\n      <main className="flex-1 overflow-y-auto h-screen pb-20">\n      {/* 상단 헤더 */}', empty_state)

# And close the fragment before the modal
close_fragment = """          </>
        )}
      </main>
    </div>
  );
}"""

content = content.replace("      </main>\n    </div>\n  );\n}", close_fragment)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
