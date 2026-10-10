import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

content = re.sub(r'  const \[hideGrade, setHideGrade\] = useState\(false\);\n', '', content)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
