import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

content = content.replace("grade: guestGrade,", "grade: guestGrade as any,")

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
