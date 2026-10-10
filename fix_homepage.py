import re

# 1. Update Homepage
with open('src/app/page.tsx', 'r') as f:
    page = f.read()

page = page.replace("제 1회 테크존 클럽 월례회 개최!", "🔥 우리들의 경기 (실시간 대진표)")
page = page.replace("이번 월례회 대진표를 확인하고 결과를 실시간으로 공유해보세요.", "새롭게 짜여진 대진표를 확인하고 경기 결과를 실시간으로 공유해보세요.")

with open('src/app/page.tsx', 'w') as f:
    f.write(page)

# 2. Update Navigation
with open('src/components/Navigation.tsx', 'r') as f:
    nav = f.read()

nav = nav.replace('name: "제1회 월례회"', 'name: "실시간 대진표"')

with open('src/components/Navigation.tsx', 'w') as f:
    f.write(nav)
