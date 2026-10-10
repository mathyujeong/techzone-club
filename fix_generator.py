import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Fix saveGuest to NOT save to DB
old_save_guest = """  const saveGuest = async () => {
    if (!guestName.trim()) return;
    const { data, error } = await supabase.from('players').insert({ name: guestName.trim(), grade: guestGrade, gender: guestGender }).select().single();
    if (data) {
      setDbPlayers([...dbPlayers, data].sort((a, b) => a.grade.localeCompare(b.grade)));
      const newSet = new Set(selectedPlayerIds);
      newSet.add(data.id);
      setSelectedPlayerIds(newSet);
      setIsGuestModalOpen(false);
    } else {
      alert('추가 실패: ' + (error?.message || '알 수 없는 오류'));
    }
  };"""

new_save_guest = """  const saveGuest = async () => {
    if (!guestName.trim()) return;
    
    const fakeGuest = {
      id: `guest_${Date.now()}`,
      name: `${guestName.trim()}(게스트)`,
      grade: guestGrade,
      gender: guestGender,
      default_penalty: 0,
      created_at: new Date().toISOString()
    };
    
    setDbPlayers([...dbPlayers, fakeGuest].sort((a, b) => a.grade.localeCompare(b.grade)));
    const newSet = new Set(selectedPlayerIds);
    newSet.add(fakeGuest.id);
    setSelectedPlayerIds(newSet);
    setIsGuestModalOpen(false);
  };"""

content = content.replace(old_save_guest, new_save_guest)

# 2. Fix Admin Match Cards to show 'A조 / B조' for INDIVIDUAL matches
old_match_blue_admin = """<div className="text-xs font-black text-blue-600 dark:text-blue-400 mb-2 flex justify-between items-center w-full">
                        <span>청팀 {bluePen && bluePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {bluePen}</span>}</span>"""
new_match_blue_admin = """<div className="text-xs font-black text-blue-600 dark:text-blue-400 mb-2 flex justify-between items-center w-full">
                        <span>{isIndividualMode ? 'A조' : '청팀'} {bluePen && bluePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {bluePen}</span>}</span>"""
content = content.replace(old_match_blue_admin, new_match_blue_admin)

old_match_white_admin = """<div className="text-xs font-black text-gray-600 dark:text-gray-400 mb-2 flex justify-between items-center w-full">
                        <span>백팀 {whitePen && whitePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {whitePen}</span>}</span>"""
new_match_white_admin = """<div className="text-xs font-black text-gray-600 dark:text-gray-400 mb-2 flex justify-between items-center w-full">
                        <span>{isIndividualMode ? 'B조' : '백팀'} {whitePen && whitePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {whitePen}</span>}</span>"""
content = content.replace(old_match_white_admin, new_match_white_admin)

# 3. Fix Stats Panel to include ALL dbPlayers so nobody is missing
old_stats = """  const playerStatsMap: Record<string, { matches: number, wins: number, team: 'BLUE' | 'WHITE' | 'MIXED' }> = {};
  currentMatches.forEach(m => {"""
new_stats = """  const playerStatsMap: Record<string, { matches: number, wins: number, team: 'BLUE' | 'WHITE' | 'MIXED' }> = {};
  dbPlayers.forEach(p => {
    playerStatsMap[p.name] = { matches: 0, wins: 0, team: 'MIXED' }; // initialize everyone
  });
  
  currentMatches.forEach(m => {"""
content = content.replace(old_stats, new_stats)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)

