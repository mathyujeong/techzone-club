"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { Settings, Plus, Minus, Check, Play, Pause, RefreshCw, Trophy, Users, Trash2 } from "lucide-react";

export default function AdminPage() {
  const [authed, setAuthed] = useState(false);
  const [pwd, setPwd] = useState("");
  const [matches, setMatches] = useState<any[]>([]);

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

  async function editPlayers(id: string, team: 'blue' | 'white', p1: string, p2: string) {
    const newP1 = prompt(`${team === 'blue' ? '청팀' : '백팀'} 첫 번째 선수 이름:`, p1);
    if (newP1 === null) return;
    const newP2 = prompt(`${team === 'blue' ? '청팀' : '백팀'} 두 번째 선수 이름:`, p2);
    if (newP2 === null) return;

    const updateData = team === 'blue' 
      ? { blue_player1: newP1, blue_player2: newP2 } 
      : { white_player1: newP1, white_player2: newP2 };
      
    setMatches(matches.map(m => m.id === id ? { ...m, ...updateData } : m));
    await supabase.from('matches').update(updateData).eq('id', id);
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

  const roundNums = Array.from(new Set(matches.map(m => m.round_num))).sort((a, b) => a - b);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 pb-20">
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

      <div className="container mx-auto px-4 py-8 space-y-12">
        {roundNums.map(roundNum => {
          const roundMatches = matches.filter(m => m.round_num === roundNum);
          return (
            <div key={roundNum} className="space-y-4">
              <h2 className="text-2xl font-black flex items-center gap-2 text-gray-800 dark:text-gray-200">
                <span className="bg-yellow-500 text-white px-3 py-1 rounded-lg text-lg">{roundNum}R</span>
              </h2>
              
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                {roundMatches.map(m => {
                  const [actualType, bluePen, whitePen] = (m.match_type || '').split(':');
                  return (
                  <div key={m.id} className={`bg-white dark:bg-gray-900 rounded-2xl shadow-sm border overflow-hidden ${m.status === 'completed' ? 'border-gray-200 opacity-60' : 'border-blue-100 dark:border-blue-900/30'}`}>
                    {/* 코트 번호 헤더 */}
                    <div className="bg-gray-100 dark:bg-gray-800 px-4 py-2 flex justify-between items-center">
                      <span 
                        className="font-black text-gray-700 dark:text-gray-300 cursor-pointer hover:underline"
                        onClick={() => editMatchInfo(m.id, m.court_num, actualType, bluePen, whitePen)}
                      >
                        코트 {m.court_num} ({actualType === 'MD' ? '남복' : actualType === 'WD' ? '여복' : actualType === 'XD' ? '혼복' : actualType})
                      </span>
                      <div className="flex items-center gap-2">
                        <button 
                          onClick={async () => {
                            const newStatus = m.status === 'completed' ? 'pending' : 'completed';
                            await supabase.from('matches').update({ status: newStatus }).eq('id', m.id);
                            fetchMatches();
                          }}
                          className={`px-3 py-1 rounded-md text-xs font-bold ${m.status === 'completed' ? 'bg-gray-300 text-gray-700' : 'bg-red-500 text-white'}`}
                        >
                          {m.status === 'completed' ? '경기 재개' : '경기 종료'}
                        </button>
                        <button onClick={() => deleteMatch(m.id)} className="text-gray-400 hover:text-red-500 transition-colors p-1" title="경기 삭제">
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                    
                    <div className="p-4 flex flex-col md:flex-row gap-4">
                      {/* 청팀 컨트롤 */}
                      <div className="flex-1 bg-blue-50 dark:bg-blue-900/10 rounded-xl p-4 border border-blue-100 dark:border-blue-800/50 flex flex-col items-center">
                        <div className="text-blue-600 dark:text-blue-400 font-black mb-2 text-lg flex items-center gap-2">
                          청팀 {bluePen && bluePen !== '0' && <span className="bg-blue-200 dark:bg-blue-800 text-blue-800 dark:text-blue-100 text-xs px-2 py-1 rounded-full">패널티 {bluePen}</span>}
                        </div>
                        <div 
                          className="text-gray-700 dark:text-gray-300 font-medium mb-4 text-center h-12 cursor-pointer hover:underline"
                          onClick={() => editPlayers(m.id, 'blue', m.blue_player1, m.blue_player2)}
                        >
                          {m.blue_player1}<br/>{m.blue_player2}
                        </div>
                        <div className="flex items-center w-full justify-center mt-2">
                          <button 
                            onClick={() => setWinner(m.id, 'blue')} 
                            className={`w-full py-3 rounded-xl font-black text-lg ${m.status === 'completed' && m.blue_score > m.white_score ? 'bg-blue-600 text-white shadow-md' : 'bg-white dark:bg-gray-800 text-blue-600 border border-blue-200 dark:border-blue-800 hover:bg-blue-50 dark:hover:bg-blue-900/20'}`}
                          >
                            {m.status === 'completed' && m.blue_score > m.white_score ? '승리' : '승리 처리'}
                          </button>
                        </div>
                      </div>

                      {/* VS 중앙 */}
                      <div className="flex items-center justify-center py-2 md:py-0">
                        <span className="text-gray-300 dark:text-gray-700 font-black text-xl italic">VS</span>
                      </div>

                      {/* 백팀 컨트롤 */}
                      <div className="flex-1 bg-gray-50 dark:bg-gray-800/30 rounded-xl p-4 border border-gray-200 dark:border-gray-800 flex flex-col items-center">
                        <div className="text-gray-700 dark:text-gray-300 font-black mb-2 text-lg flex items-center gap-2">
                          백팀 {whitePen && whitePen !== '0' && <span className="bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 text-xs px-2 py-1 rounded-full">패널티 {whitePen}</span>}
                        </div>
                        <div 
                          className="text-gray-700 dark:text-gray-300 font-medium mb-4 text-center h-12 cursor-pointer hover:underline"
                          onClick={() => editPlayers(m.id, 'white', m.white_player1, m.white_player2)}
                        >
                          {m.white_player1}<br/>{m.white_player2}
                        </div>
                        <div className="flex items-center w-full justify-center mt-2">
                          <button 
                            onClick={() => setWinner(m.id, 'white')} 
                            className={`w-full py-3 rounded-xl font-black text-lg ${m.status === 'completed' && m.white_score > m.blue_score ? 'bg-gray-800 dark:bg-gray-200 text-white dark:text-black shadow-md' : 'bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700'}`}
                          >
                            {m.status === 'completed' && m.white_score > m.blue_score ? '승리' : '승리 처리'}
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
