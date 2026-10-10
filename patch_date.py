import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. State addition
content = content.replace('const [editingTournamentName, setEditingTournamentName] = useState("");', 'const [editingTournamentName, setEditingTournamentName] = useState("");\n  const [editingTournamentDate, setEditingTournamentDate] = useState("");')

# 2. Function replacement
old_func = """  const saveTournamentName = async (id: string) => {
    if(!editingTournamentName.trim()) return;
    await supabase.from('tournaments').update({ title: editingTournamentName }).eq('id', id);
    setTournaments(tournaments.map(t => t.id === id ? { ...t, title: editingTournamentName } : t));
    setEditingTournamentId(null);
  };"""

new_func = """  const saveTournamentData = async (id: string) => {
    if(!editingTournamentName.trim() || !editingTournamentDate) return;
    const newDate = new Date(editingTournamentDate).toISOString();
    await supabase.from('tournaments').update({ title: editingTournamentName, created_at: newDate }).eq('id', id);
    setTournaments(tournaments.map(t => t.id === id ? { ...t, title: editingTournamentName, created_at: newDate } : t));
    setEditingTournamentId(null);
  };"""

content = content.replace(old_func, new_func)

# 3. UI Replacement
# Find the exact button element logic in the map
old_ui = """              <div className="flex items-center justify-between w-full">
                {editingTournamentId === t.id ? (
                  <input 
                    type="text" 
                    value={editingTournamentName}
                    onChange={e => setEditingTournamentName(e.target.value)}
                    onBlur={() => saveTournamentName(t.id)}
                    onKeyDown={e => e.key === 'Enter' && saveTournamentName(t.id)}
                    autoFocus
                    className="flex-1 text-sm font-bold border border-blue-400 rounded px-1 py-0.5 w-full bg-white dark:bg-gray-800 text-black dark:text-white"
                    onClick={(e) => e.stopPropagation()}
                  />
                ) : (
                  <span className={`font-bold text-sm flex-1 ${selectedTournamentId === t.id ? 'text-yellow-700 dark:text-yellow-400' : 'text-gray-700 dark:text-gray-300'}`}>{t.title}</span>
                )}
                <div className="flex items-center gap-2 shrink-0">
                  {editingTournamentId !== t.id && (
                    <button 
                      onClick={(e) => { e.stopPropagation(); setEditingTournamentId(t.id); setEditingTournamentName(t.title); }} 
                      className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded text-gray-400 hover:text-gray-600"
                    >
                      <Edit2 className="w-3 h-3" />
                    </button>
                  )}
                  <div className={`w-2 h-2 rounded-full ${t.status === 'IN_PROGRESS' ? 'bg-green-500' : 'bg-gray-300'}`} />
                </div>
              </div>
              <span className="text-[10px] text-gray-400">{new Date(t.created_at).toLocaleDateString()}</span>"""

new_ui = """              <div className="flex flex-col gap-1 w-full">
                <div className="flex items-center justify-between w-full">
                  {editingTournamentId === t.id ? (
                    <input 
                      type="text" 
                      value={editingTournamentName}
                      onChange={e => setEditingTournamentName(e.target.value)}
                      onKeyDown={e => e.key === 'Enter' && saveTournamentData(t.id)}
                      autoFocus
                      className="flex-1 text-sm font-bold border border-blue-400 rounded px-1 py-0.5 w-full bg-white dark:bg-gray-800 text-black dark:text-white mb-1"
                      onClick={(e) => e.stopPropagation()}
                    />
                  ) : (
                    <span className={`font-bold text-sm flex-1 ${selectedTournamentId === t.id ? 'text-yellow-700 dark:text-yellow-400' : 'text-gray-700 dark:text-gray-300'}`}>{t.title}</span>
                  )}
                  <div className="flex items-center gap-2 shrink-0">
                    {editingTournamentId === t.id ? (
                      <button onClick={(e) => { e.stopPropagation(); saveTournamentData(t.id); }} className="p-1 bg-blue-100 text-blue-600 rounded">
                        <Check className="w-3 h-3" />
                      </button>
                    ) : (
                      <button 
                        onClick={(e) => { e.stopPropagation(); setEditingTournamentId(t.id); setEditingTournamentName(t.title); setEditingTournamentDate(new Date(t.created_at).toISOString().split('T')[0]); }} 
                        className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded text-gray-400 hover:text-gray-600"
                      >
                        <Edit2 className="w-3 h-3" />
                      </button>
                    )}
                    <div className={`w-2 h-2 rounded-full ${t.status === 'IN_PROGRESS' ? 'bg-green-500' : 'bg-gray-300'}`} />
                  </div>
                </div>
                {editingTournamentId === t.id ? (
                  <input
                    type="date"
                    value={editingTournamentDate}
                    onChange={e => setEditingTournamentDate(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && saveTournamentData(t.id)}
                    className="text-[10px] border border-blue-400 rounded px-1 py-0.5 w-max bg-white dark:bg-gray-800 text-black dark:text-white"
                    onClick={(e) => e.stopPropagation()}
                  />
                ) : (
                  <span className="text-[10px] text-gray-400">{new Date(t.created_at).toLocaleDateString()}</span>
                )}
              </div>"""

content = content.replace(old_ui, new_ui)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
