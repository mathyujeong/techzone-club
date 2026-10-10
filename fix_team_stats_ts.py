import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# Fix 1: isP1Exist
content = content.replace("teamStats.some(([n]) => n === p1)", "teamStats.some(s => s.name === p1)")
content = content.replace("teamStats.some(([n]) => n === p2)", "teamStats.some(s => s.name === p2)")

# Fix 2: editPlayerModal.map
content = content.replace(".map(([name]) => (", ".map(s => (")
# wait, there's <option key={name} value={name}>{name}</option> inside the map.
# If I changed `([name])` to `s`, I need to change `{name}` to `{s.name}`.
# Let's just use `.map(({name}) => (` !

content = content.replace(".map(([name]) => (", ".map(({name}) => (")

# Wait, there are errors in 749 and 762. But my previous python script ALREADY replaced that part of the UI!
# Why did it error on 749?
# Oh! The old_ui replacement might have failed, so the old UI was still there!
# Let me check if `old_ui` failed to replace.
