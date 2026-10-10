import re

# Admin mode
with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()
# Wait, admin mode didn't have filter?
# Let's check:
content = content.replace(".filter(s => s.matches > 0);", ";")
with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)

# Member mode
with open('src/app/tournament/page.tsx', 'r') as f:
    content = f.read()
content = content.replace(".filter(s => s.matches > 0);", ";")
with open('src/app/tournament/page.tsx', 'w') as f:
    f.write(content)
