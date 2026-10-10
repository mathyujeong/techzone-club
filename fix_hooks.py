import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# The hooks I incorrectly injected lower down
hooks_code = """
  const [selectedTournamentId, setSelectedTournamentId] = useState<string | null>(null);

  // set selected tournament when tournaments load
  useEffect(() => {
    if (tournaments.length > 0 && !selectedTournamentId) {
      // Find IN_PROGRESS first, otherwise first in list
      const active = tournaments.find(t => t.status === 'IN_PROGRESS') || tournaments[0];
      setSelectedTournamentId(active.id);
    }
  }, [tournaments]);
"""

# Remove from the lower part
content = content.replace(hooks_code, "")

# Insert right after `const [tournaments, setTournaments] = useState<any[]>([]);`
insert_target = "const [tournaments, setTournaments] = useState<any[]>([]);"
content = content.replace(insert_target, insert_target + "\n" + hooks_code)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
