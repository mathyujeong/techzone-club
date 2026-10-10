import re

with open('src/app/tournament/page.tsx', 'r') as f:
    content = f.read()

content = content.replace("getPlayerGrade(match.blue_player1)", "getPlayerGrade(String(match.blue_player1))")
content = content.replace("getPlayerGrade(match.blue_player2)", "getPlayerGrade(String(match.blue_player2))")
content = content.replace("getPlayerGrade(match.white_player1)", "getPlayerGrade(String(match.white_player1))")
content = content.replace("getPlayerGrade(match.white_player2)", "getPlayerGrade(String(match.white_player2))")

with open('src/app/tournament/page.tsx', 'w') as f:
    f.write(content)
