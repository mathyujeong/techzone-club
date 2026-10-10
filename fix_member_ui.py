import re

with open('src/app/tournament/page.tsx', 'r') as f:
    content = f.read()

# Make sure we know if it's INDIVIDUAL mode.
# In Member mode, `activeTournament` is the currently selected tournament.
old_match_blue_member = """<div className="text-xs font-black text-blue-600 dark:text-blue-400 mb-2 flex justify-center items-center gap-1">청팀 {bluePen && bluePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {bluePen}</span>}</div>"""
new_match_blue_member = """<div className="text-xs font-black text-blue-600 dark:text-blue-400 mb-2 flex justify-center items-center gap-1">{activeTournament?.match_type === 'INDIVIDUAL' ? 'A조' : '청팀'} {bluePen && bluePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {bluePen}</span>}</div>"""
content = content.replace(old_match_blue_member, new_match_blue_member)

old_match_white_member = """<div className="text-xs font-black text-gray-600 dark:text-gray-400 mb-2 flex justify-center items-center gap-1">백팀 {whitePen && whitePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {whitePen}</span>}</div>"""
new_match_white_member = """<div className="text-xs font-black text-gray-600 dark:text-gray-400 mb-2 flex justify-center items-center gap-1">{activeTournament?.match_type === 'INDIVIDUAL' ? 'B조' : '백팀'} {whitePen && whitePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {whitePen}</span>}</div>"""
content = content.replace(old_match_white_member, new_match_white_member)

with open('src/app/tournament/page.tsx', 'w') as f:
    f.write(content)

