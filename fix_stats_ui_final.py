import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# Fix the map callbacks for the new stats format
content = content.replace("teamStats.some(([n]) => n === p1)", "teamStats.some(s => s.name === p1)")
content = content.replace("teamStats.some(([n]) => n === p2)", "teamStats.some(s => s.name === p2)")
content = content.replace(".map(([name]) => (", ".map(({name}) => (")


# Fix the UI
old_ui_pattern = r'      <div className="container mx-auto px-4 pt-8">\n        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">\n          <h2 className="text-lg font-bold mb-6 flex items-center gap-2 border-b border-gray-100 dark:border-gray-800 pb-4">\n            <Users className="text-yellow-600 w-5 h-5" />팀 구성 및 선수별 배정 경기 수\n          </h2>\n          <div className="flex flex-col md:flex-row gap-8">\n            <div className="flex-1">\n              <h3 className="text-sm font-bold text-blue-600 dark:text-blue-400 mb-3 flex items-center gap-1">\n                청팀 <span className="bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 text-xs px-2 py-0.5 rounded-full">\{blueTeamStats.length\}명</span>\n              </h3>\n              <div className="flex flex-wrap gap-2">\n                \{blueTeamStats.map\(\(\[name, count\]\) => \(\n                  <span key=\{name\} className="bg-blue-50 border border-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm dark:bg-blue-900/30 dark:border-blue-800 dark:text-blue-300">\n                    \{name\} <span className="font-bold opacity-70">\(\{count\}\)</span>\n                  </span>\n                \)\)\}\n              </div>\n            </div>\n            <div className="hidden md:block w-px bg-gray-200 dark:bg-gray-800"></div>\n            <div className="flex-1">\n              <h3 className="text-sm font-bold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-1">\n                백팀 <span className="bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300 text-xs px-2 py-0.5 rounded-full">\{whiteTeamStats.length\}명</span>\n              </h3>\n              <div className="flex flex-wrap gap-2">\n                \{whiteTeamStats.map\(\(\[name, count\]\) => \(\n                  <span key=\{name\} className="bg-gray-100 border border-gray-200 text-gray-800 px-3 py-1 rounded-full text-sm dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300">\n                    \{name\} <span className="font-bold opacity-70">\(\{count\}\)</span>\n                  </span>\n                \)\)\}\n              </div>\n            </div>\n          </div>'

new_ui = """      <div className="container mx-auto px-4 pt-8">
        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
          <h2 className="text-lg font-bold mb-6 flex items-center gap-2 border-b border-gray-100 dark:border-gray-800 pb-4">
            <Users className="text-yellow-600 w-5 h-5" />
            {isIndividualMode ? '개인별 배정 경기 수 및 승률 (성적순)' : '팀 구성 및 선수별 배정 경기 수'}
          </h2>
          
          {isIndividualMode ? (
            <div className="flex flex-wrap gap-3">
              {individualStats.map(s => (
                <div key={s.name} className="bg-gray-50 border border-gray-200 text-gray-800 px-3 py-2 rounded-xl text-sm dark:bg-gray-800 dark:border-gray-700 dark:text-gray-200 flex flex-col min-w-[100px]">
                  <span className="font-black text-center mb-1 text-base">{s.name}</span>
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>{s.matches}경기</span>
                    <span className="text-blue-600 font-bold">{s.wins}승</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col md:flex-row gap-8">
              <div className="flex-1">
                <h3 className="text-sm font-bold text-blue-600 dark:text-blue-400 mb-3 flex items-center gap-1">
                  청팀 <span className="bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 text-xs px-2 py-0.5 rounded-full">{blueTeamStats.length}명</span>
                </h3>
                <div className="flex flex-wrap gap-2">
                  {blueTeamStats.map(s => (
                    <div key={s.name} className="bg-blue-50 border border-blue-100 text-blue-800 px-3 py-1.5 rounded-xl text-sm dark:bg-blue-900/30 dark:border-blue-800 dark:text-blue-300 flex items-center gap-2">
                      <span className="font-bold">{s.name}</span>
                      <span className="text-xs opacity-70 border-l border-blue-200 pl-2">{s.matches}경기 <span className="font-bold text-blue-700">{s.wins}승</span></span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="hidden md:block w-px bg-gray-200 dark:bg-gray-800"></div>
              <div className="flex-1">
                <h3 className="text-sm font-bold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-1">
                  백팀 <span className="bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300 text-xs px-2 py-0.5 rounded-full">{whiteTeamStats.length}명</span>
                </h3>
                <div className="flex flex-wrap gap-2">
                  {whiteTeamStats.map(s => (
                    <div key={s.name} className="bg-gray-100 border border-gray-200 text-gray-800 px-3 py-1.5 rounded-xl text-sm dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300 flex items-center gap-2">
                      <span className="font-bold">{s.name}</span>
                      <span className="text-xs opacity-70 border-l border-gray-300 pl-2">{s.matches}경기 <span className="font-bold text-gray-700">{s.wins}승</span></span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}"""

content = re.sub(old_ui_pattern, new_ui, content, flags=re.DOTALL)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
