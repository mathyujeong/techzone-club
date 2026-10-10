with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# Add handleAddNewTournament
new_func = """  const handleAddNewTournament = async () => {
    const { data, error } = await supabase.from('tournaments').insert({ title: '새 월례회' }).select().single();
    if (data) {
      setTournaments([data, ...tournaments]);
      setSelectedTournamentId(data.id);
      setEditingTournamentId(data.id);
      setEditingTournamentName(data.title);
      setEditingTournamentDate(new Date(data.created_at).toISOString().split('T')[0]);
    } else {
      alert('대회 추가 실패: ' + (error?.message || ''));
    }
  };"""

if 'const handleAddNewTournament =' not in content:
    content = content.replace("  // --- Tournament Renaming ---", new_func + "\n\n  // --- Tournament Renaming ---")

# Replace sidebar button
old_btn = """<button onClick={() => { setGeneratedBracket([]); setIsGeneratorModalOpen(true); }} className="w-full bg-blue-600 text-white px-4 py-3 rounded-xl font-bold text-sm flex justify-center items-center gap-2 hover:bg-blue-700 shadow-sm transition-colors">
            <RefreshCw className="w-4 h-4" /> 새 대회 추가
          </button>"""
new_btn = """<button onClick={handleAddNewTournament} className="w-full bg-blue-600 text-white px-4 py-3 rounded-xl font-bold text-sm flex justify-center items-center gap-2 hover:bg-blue-700 shadow-sm transition-colors">
            <RefreshCw className="w-4 h-4" /> 새 대회 추가
          </button>"""
content = content.replace(old_btn, new_btn)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
