"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { Settings, Plus, Minus, Check, Play, Pause, RefreshCw, Trophy, Users, Trash2, ChevronDown } from "lucide-react";

export default function AdminPage() {
  const [authed, setAuthed] = useState(false);
  const [pwd, setPwd] = useState("");
  const [matches, setMatches] = useState<any[]>([]);
  const [editPlayerModal, setEditPlayerModal] = useState<{ id: string, team: 'blue' | 'white', currentP1: string, currentP2: string } | null>(null);
  const [p1Select, setP1Select] = useState("");
  const [p1Input, setP1Input] = useState("");
  const [p2Select, setP2Select] = useState("");
  const [p2Input, setP2Input] = useState("");

  useEffect(() => {
    if (authed) fetchMatches();
  }, [authed]);

  async function fetchMatches() {
    const { data } = await supabase.from('matches').select('*').order('round_num').order('court_num');
    if (data) setMatches(data);
  }

  async function setWinner(id: string, team: 'blue' | 'white') {
    const blueScore = team === 'blue' ? 1 : 0;
    const whiteScore = team === 'white' ? 1 : 0;
    
    setMatches(matches.map(m => m.id === id ? { ...m, blue_score: blueScore, white_score: whiteScore, status: 'completed' } : m));
    
    await supabase.from('matches').update({ 
      blue_score: blueScore, 
      white_score: whiteScore, 
      status: 'completed' 
    }).eq('id', id);
  }

  function editPlayers(id: string, team: 'blue' | 'white', p1: string, p2: string) {
    setEditPlayerModal({ id, team, currentP1: p1, currentP2: p2 });
    
    const teamStats = team === 'blue' ? blueTeamStats : whiteTeamStats;
    const isP1Exist = teamStats.some(([n]) => n === p1);
    const isP2Exist = teamStats.some(([n]) => n === p2);
    
    setP1Select(isP1Exist ? p1 : '직접입력');
    setP1Input(isP1Exist ? '' : p1);
    
    setP2Select(isP2Exist ? p2 : '직접입력');
    setP2Input(isP2Exist ? '' : p2);
  }

  async function savePlayers() {
    if (!editPlayerModal) return;
    const { id, team } = editPlayerModal;
    
    const finalP1 = p1Select === '직접입력' ? p1Input.trim() : p1Select;
    const finalP2 = p2Select === '직접입력' ? p2Input.trim() : p2Select;
    
    if(!finalP1 || !finalP2) {
      alert("선수 이름을 모두 입력해주세요.");
      return;
    }

    const updateData = team === 'blue' 
      ? { blue_player1: finalP1, blue_player2: finalP2 } 
      : { white_player1: finalP1, white_player2: finalP2 };
      
    setMatches(matches.map(m => m.id === id ? { ...m, ...updateData } : m));
    await supabase.from('matches').update(updateData).eq('id', id);
    setEditPlayerModal(null);
  }

  async function editMatchInfo(id: string, currentCourt: number, currentType: string, bluePen: string, whitePen: string) {
    const newCourt = prompt("코트 번호를 입력하세요:", currentCourt.toString());
    if (newCourt === null) return;
    const newType = prompt("경기 종류 (MD: 남복, WD: 여복, XD: 혼복):", currentType);
    if (newType === null) return;
    const newBluePen = prompt("청팀 패널티:", bluePen || "0");
    if (newBluePen === null) return;
    const newWhitePen = prompt("백팀 패널티:", whitePen || "0");
    if (newWhitePen === null) return;

    const match_type = `${newType.toUpperCase()}:${newBluePen}:${newWhitePen}`;
    
    setMatches(matches.map(m => m.id === id ? { ...m, court_num: parseInt(newCourt) || currentCourt, match_type } : m));
    await supabase.from('matches').update({ court_num: parseInt(newCourt) || currentCourt, match_type }).eq('id', id);
  }

  async function addMatch() {
    const round = parseInt(prompt("몇 라운드에 추가할까요?", "1") || "0");
    if (!round) return;
    const court = parseInt(prompt("코트 번호는요?", "1") || "1");
    
    await supabase.from('matches').insert({
      round_num: round,
      court_num: court,
      match_type: 'MD:0:0',
      blue_player1: '선수1',
      blue_player2: '선수2',
      white_player1: '선수3',
      white_player2: '선수4',
      blue_score: 0,
      white_score: 0,
      status: 'pending'
    });
    fetchMatches();
  }

  async function deleteMatch(id: string) {
    if (confirm("정말로 이 경기를 삭제하시겠습니까?")) {
      setMatches(matches.filter(m => m.id !== id));
      await supabase.from('matches').delete().eq('id', id);
    }
  }

  if (!authed) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950">
        <div className="bg-white dark:bg-gray-900 p-8 rounded-2xl shadow-xl w-full max-w-sm text-center border border-gray-200 dark:border-gray-800">
          <Trophy className="w-16 h-16 text-yellow-500 mx-auto mb-6" />
          <h1 className="text-2xl font-black mb-2">관리자 모드</h1>
          <p className="text-gray-500 mb-8 text-sm">경기 점수 조작 및 대진표 관리</p>
          <input 
            type="password" 
            value={pwd} 
            onChange={e => setPwd(e.target.value)} 
            className="w-full border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 p-4 rounded-xl mb-4 text-center font-bold tracking-widest outline-none focus:ring-2 focus:ring-yellow-500 text-black dark:text-white"
            placeholder="비밀번호 입력"
            onKeyDown={e => { if(e.key === 'Enter' && pwd === '0070') setAuthed(true); }}
          />
          <button 
            onClick={() => { if(pwd === '0070') setAuthed(true); else alert('비밀번호가 틀렸습니다!'); }}
            className="w-full bg-black dark:bg-yellow-600 text-white font-bold px-6 py-4 rounded-xl hover:opacity-80 transition"
          >
            입장하기
          </button>
        </div>
      </div>
    );
  }


  const playerStats: Record<string, number> = {};
  matches.forEach(m => {
    [m.blue_player1, m.blue_player2, m.white_player1, m.white_player2].forEach(p => {
      if(p) playerStats[p] = (playerStats[p] || 0) + 1;
    });
  });

  const blueTeamStats = Object.entries(playerStats)
    .filter(([name]) => matches.some(m => m.blue_player1 === name || m.blue_player2 === name))
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
    
  const whiteTeamStats = Object.entries(playerStats)
    .filter(([name]) => matches.some(m => m.white_player1 === name || m.white_player2 === name))
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));

  const roundNums = Array.from(new Set(matches.map(m => m.round_num))).sort((a, b) => a - b);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 pb-20">

      {editPlayerModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4">
          <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-xl w-full max-w-sm p-6 border border-gray-200 dark:border-gray-800">
            <h2 className="text-xl font-bold mb-4">{editPlayerModal.team === 'blue' ? '청팀' : '백팀'} 선수 교체</h2>
            
            <div className="space-y-6 mb-8">
              <div>
                <label className="block text-sm font-bold mb-2 text-gray-800 dark:text-gray-200">첫 번째 선수</label>
                <div className="relative">
                  <select 
                    value={p1Select} 
                    onChange={e => {
                      setP1Select(e.target.value);
                      if(e.target.value !== '직접입력') setP1Input('');
                    }} 
                    className="w-full appearance-none border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-xl px-4 py-3.5 outline-none mb-2 text-gray-900 dark:text-white focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-all font-medium cursor-pointer shadow-sm"
                  >
                    <option value="">-- 선택 --</option>
                    {(editPlayerModal.team === 'blue' ? blueTeamStats : whiteTeamStats).map(([name]) => (
                      <option key={name} value={name}>{name}</option>
                    ))}
                    <option value="직접입력">+ 새 선수/게스트 직접입력</option>
                  </select>
                  <ChevronDown className="absolute right-4 top-4 w-5 h-5 text-gray-400 pointer-events-none" />
                </div>
                {p1Select === '직접입력' && (
                  <input 
                    type="text" 
                    placeholder="선수 이름 입력"
                    value={p1Input}
                    onChange={e => setP1Input(e.target.value)}
                    className="w-full border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 rounded-xl px-4 py-3.5 outline-none text-gray-900 dark:text-white focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-all shadow-sm"
                    autoFocus
                  />
                )}
              </div>

              <div>
                <label className="block text-sm font-bold mb-2 text-gray-800 dark:text-gray-200">두 번째 선수</label>
                <div className="relative">
                  <select 
                    value={p2Select} 
                    onChange={e => {
                      setP2Select(e.target.value);
                      if(e.target.value !== '직접입력') setP2Input('');
                    }} 
                    className="w-full appearance-none border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-xl px-4 py-3.5 outline-none mb-2 text-gray-900 dark:text-white focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-all font-medium cursor-pointer shadow-sm"
                  >
                    <option value="">-- 선택 --</option>
                    {(editPlayerModal.team === 'blue' ? blueTeamStats : whiteTeamStats).map(([name]) => (
                      <option key={name} value={name}>{name}</option>
                    ))}
                    <option value="직접입력">+ 새 선수/게스트 직접입력</option>
                  </select>
                  <ChevronDown className="absolute right-4 top-4 w-5 h-5 text-gray-400 pointer-events-none" />
                </div>
                {p2Select === '직접입력' && (
                  <input 
                    type="text" 
                    placeholder="선수 이름 입력"
                    value={p2Input}
                    onChange={e => setP2Input(e.target.value)}
                    className="w-full border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 rounded-xl px-4 py-3.5 outline-none text-gray-900 dark:text-white focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-all shadow-sm"
                  />
                )}
              </div>
            </div>

            <div className="flex gap-3">
              <button 
                onClick={() => setEditPlayerModal(null)} 
                className="flex-1 bg-gray-200 dark:bg-gray-800 text-gray-800 dark:text-gray-200 py-3 rounded-xl font-bold"
              >
                취소
              </button>
              <button 
                onClick={savePlayers} 
                className="flex-1 bg-yellow-500 text-white py-3 rounded-xl font-bold"
              >
                저장
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 상단 헤더 */}
      <div className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-10 shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl md:text-2xl font-black flex items-center gap-2">
            <Settings className="text-gray-400" />
            점수 관리 보드
          </h1>
          <button onClick={addMatch} className="bg-gray-900 dark:bg-gray-100 text-white dark:text-black px-4 py-2 rounded-lg font-bold text-sm flex items-center gap-1 hover:opacity-80">
            <Plus className="w-4 h-4" /> 경기 추가
          </button>
        </div>
      </div>


      {/* 통계 패널 */}
      <div className="container mx-auto px-4 pt-8">
        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
          <h2 className="text-lg font-bold mb-6 flex items-center gap-2 border-b border-gray-100 dark:border-gray-800 pb-4">
            <Users className="text-yellow-600 w-5 h-5" />팀 구성 및 선수별 배정 경기 수
          </h2>
          <div className="flex flex-col md:flex-row gap-8">
            <div className="flex-1">
              <h3 className="text-sm font-bold text-blue-600 dark:text-blue-400 mb-3">청팀</h3>
              <div className="flex flex-wrap gap-2">
                {blueTeamStats.map(([name, count]) => (
                  <span key={name} className="bg-blue-50 border border-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm dark:bg-blue-900/30 dark:border-blue-800 dark:text-blue-300">
                    {name} <span className="font-bold opacity-70">({count})</span>
                  </span>
                ))}
              </div>
            </div>
            <div className="hidden md:block w-px bg-gray-200 dark:bg-gray-800"></div>
            <div className="flex-1">
              <h3 className="text-sm font-bold text-gray-700 dark:text-gray-300 mb-3">백팀</h3>
              <div className="flex flex-wrap gap-2">
                {whiteTeamStats.map(([name, count]) => (
                  <span key={name} className="bg-gray-100 border border-gray-200 text-gray-800 px-3 py-1 rounded-full text-sm dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300">
                    {name} <span className="font-bold opacity-70">({count})</span>
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8 space-y-12">
        {roundNums.map(roundNum => {
          const roundMatches = matches.filter(m => m.round_num === roundNum);
          return (
            <div key={roundNum} className="space-y-4">
              <h2 className="text-2xl font-black flex items-center gap-2 text-gray-800 dark:text-gray-200">
                <span className="bg-yellow-500 text-white px-3 py-1 rounded-lg text-lg">{roundNum}R</span>
              </h2>
              
              <div className="grid grid-cols-3 gap-2 md:gap-4">
                {roundMatches.map(m => {
                  const [actualType, bluePen, whitePen] = (m.match_type || '').split(':');
                  return (
                  <div key={m.id} className={`flex flex-col bg-white dark:bg-gray-900 rounded-lg shadow-sm border overflow-hidden text-xs ${m.status === 'completed' ? 'border-gray-200 opacity-60' : 'border-blue-100 dark:border-blue-900/30'}`}>
                    {/* 코트 번호 헤더 */}
                    <div className="bg-gray-100 dark:bg-gray-800 p-1.5 flex flex-col lg:flex-row justify-between items-center text-center gap-1">
                      <span 
                        className="font-bold text-gray-700 dark:text-gray-300 text-[10px] cursor-pointer hover:underline truncate w-full lg:w-auto"
                        onClick={() => editMatchInfo(m.id, m.court_num, actualType, bluePen, whitePen)}
                      >
                        코트 {m.court_num} <span className="hidden lg:inline">({actualType})</span>
                      </span>
                      <div className="flex items-center gap-1">
                        <button 
                          onClick={async () => {
                            const newStatus = m.status === 'completed' ? 'pending' : 'completed';
                            await supabase.from('matches').update({ status: newStatus }).eq('id', m.id);
                            fetchMatches();
                          }}
                          className={`px-1.5 py-0.5 rounded text-[9px] font-bold ${m.status === 'completed' ? 'bg-gray-300 text-gray-700' : 'bg-red-500 text-white'}`}
                        >
                          {m.status === 'completed' ? '재개' : '종료'}
                        </button>
                        <button onClick={() => deleteMatch(m.id)} className="text-gray-400 hover:text-red-500 p-0.5" title="경기 삭제">
                          <Trash2 className="w-3 h-3" />
                        </button>
                      </div>
                    </div>
                    
                    <div className="flex flex-col flex-1 divide-y divide-gray-100 dark:divide-gray-800">
                      {/* 청팀 */}
                      <div className={`p-1.5 flex flex-col flex-1 justify-center gap-1 ${m.status === 'completed' && m.blue_score > m.white_score ? 'bg-blue-50 dark:bg-blue-900/30' : ''}`}>
                        <div className="text-[10px] font-bold text-blue-600 dark:text-blue-400 text-center mb-0.5">
                          청팀 {bluePen && bluePen !== '0' && <span className="text-[9px] opacity-70">(-{bluePen})</span>}
                        </div>
                        <div className="flex flex-row items-center justify-between gap-1 w-full">
                          <div 
                            className="font-medium cursor-pointer hover:underline leading-tight text-left flex-1 break-keep"
                            onClick={() => editPlayers(m.id, 'blue', m.blue_player1, m.blue_player2)}
                          >
                            {m.blue_player1}<br/>{m.blue_player2}
                          </div>
                          <button 
                            onClick={() => setWinner(m.id, 'blue')} 
                            className={`shrink-0 px-2 py-1.5 rounded text-[10px] font-black ${m.status === 'completed' && m.blue_score > m.white_score ? 'bg-blue-600 text-white shadow-sm' : 'bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300'}`}
                          >
                            {m.status === 'completed' && m.blue_score > m.white_score ? '승리' : '승'}
                          </button>
                        </div>
                      </div>

                      {/* 백팀 */}
                      <div className={`p-1.5 flex flex-col flex-1 justify-center gap-1 ${m.status === 'completed' && m.white_score > m.blue_score ? 'bg-gray-100 dark:bg-gray-800' : ''}`}>
                        <div className="text-[10px] font-bold text-gray-700 dark:text-gray-300 text-center mb-0.5">
                          백팀 {whitePen && whitePen !== '0' && <span className="text-[9px] opacity-70">(-{whitePen})</span>}
                        </div>
                        <div className="flex flex-row items-center justify-between gap-1 w-full">
                          <div 
                            className="font-medium cursor-pointer hover:underline leading-tight text-left text-gray-800 dark:text-gray-200 flex-1 break-keep"
                            onClick={() => editPlayers(m.id, 'white', m.white_player1, m.white_player2)}
                          >
                            {m.white_player1}<br/>{m.white_player2}
                          </div>
                          <button 
                            onClick={() => setWinner(m.id, 'white')} 
                            className={`shrink-0 px-2 py-1.5 rounded text-[10px] font-black ${m.status === 'completed' && m.white_score > m.blue_score ? 'bg-gray-800 text-white dark:bg-gray-200 dark:text-black shadow-sm' : 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300'}`}
                          >
                            {m.status === 'completed' && m.white_score > m.blue_score ? '승리' : '승'}
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                )})}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
