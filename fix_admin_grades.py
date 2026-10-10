import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Add getPlayerGrade helper just before the render return
if "const getPlayerGrade =" not in content:
    helper_code = """
  const getPlayerGrade = (name: string) => {
    const p = dbPlayers.find(player => player.name === name);
    return p ? p.grade : '';
  };

  return (
"""
    content = content.replace("  return (\n", helper_code)

# 2. Replace the blue player rendering
old_blue_render = """<div className="truncate w-full">{m.blue_player1}</div>
                        <div className="truncate w-full">{m.blue_player2}</div>"""

new_blue_render = """<div className="truncate w-full flex justify-between items-center">
                          <span>{m.blue_player1}</span>
                          <span className="text-[10px] font-black opacity-50 ml-1">{getPlayerGrade(m.blue_player1)}</span>
                        </div>
                        <div className="truncate w-full flex justify-between items-center">
                          <span>{m.blue_player2}</span>
                          <span className="text-[10px] font-black opacity-50 ml-1">{getPlayerGrade(m.blue_player2)}</span>
                        </div>"""

content = content.replace(old_blue_render, new_blue_render)

# 3. Replace the white player rendering
old_white_render = """<div className="truncate w-full">{m.white_player1}</div>
                        <div className="truncate w-full">{m.white_player2}</div>"""

new_white_render = """<div className="truncate w-full flex justify-between items-center">
                          <span>{m.white_player1}</span>
                          <span className="text-[10px] font-black opacity-50 ml-1">{getPlayerGrade(m.white_player1)}</span>
                        </div>
                        <div className="truncate w-full flex justify-between items-center">
                          <span>{m.white_player2}</span>
                          <span className="text-[10px] font-black opacity-50 ml-1">{getPlayerGrade(m.white_player2)}</span>
                        </div>"""

content = content.replace(old_white_render, new_white_render)

# 4. Remove hideGrade checkbox and related logic from the generator Modal
# The user said "저 버튼을 만든 의미가 없는데" so we'll remove it, and ALWAYS show grades in the Generator Modal preview!
checkbox_block = """                    <label className="flex items-center gap-2 text-xs font-bold text-gray-700 dark:text-gray-300 cursor-pointer">
                      <input type="checkbox" checked={hideGrade} onChange={e => setHideGrade(e.target.checked)} className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500" />
                      대진표 급수 숨기기
                    </label>"""
content = content.replace(checkbox_block, "")

# Remove `!hideGrade &&` from the preview
content = content.replace("{!hideGrade && <span", "{<span")

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
