"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";

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

  async function updateScore(id: string, team: 'blue' | 'white', delta: number) {
    const match = matches.find(m => m.id === id);
    if(!match) return;
    const newScore = team === 'blue' ? match.blue_score + delta : match.white_score + delta;
    if(newScore < 0) return;
    
    // UI 낙관적 업데이트
    setMatches(matches.map(m => m.id === id ? { ...m, [`${team}_score`]: newScore } : m));
    
    // DB 업데이트
    await supabase.from('matches').update({ [`${team}_score`]: newScore }).eq('id', id);
  }

  async function addMatch() {
    const round = parseInt(prompt("몇 라운드에 추가할까요?", "1") || "0");
    if (!round) return;
    const court = parseInt(prompt("코트 번호는요?", "1") || "1");
    
    await supabase.from('matches').insert({
      round_num: round,
      court_num: court,
      match_type: 'MD', // 기본값
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

  if (!authed) {
    return (
      <div className="container mx-auto px-4 py-20 flex flex-col items-center">
        <h1 className="text-2xl font-bold mb-4">관리자 로그인</h1>
        <input 
          type="password" 
          value={pwd} 
          onChange={e => setPwd(e.target.value)} 
          className="border p-2 rounded mb-4 text-black"
          placeholder="비밀번호 입력"
        />
        <button 
          onClick={() => { if(pwd === 'techzone123') setAuthed(true); else alert('틀렸습니다!'); }}
          className="bg-blue-600 text-white px-6 py-2 rounded"
        >
          입장하기
        </button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-red-600">관리자 점수판 조작 모드</h1>
        <button onClick={addMatch} className="bg-yellow-500 text-white px-4 py-2 rounded font-bold">
          + 새로운 경기 추가하기
        </button>
      </div>

      <div className="space-y-4">
        {matches.map(m => (
          <div key={m.id} className="bg-white dark:bg-gray-900 border p-4 rounded-xl flex items-center justify-between gap-4">
            <div className="w-20 text-center font-bold">{m.round_num}R - {m.court_num}코트</div>
            
            <div className="flex-1 flex justify-end items-center gap-4">
              <div className="text-right">
                <div className="text-blue-600 font-bold">청팀</div>
                <div className="text-sm">{m.blue_player1}, {m.blue_player2}</div>
              </div>
              <button onClick={() => updateScore(m.id, 'blue', -1)} className="bg-gray-200 px-3 py-1 rounded">-</button>
              <div className="text-2xl font-bold w-12 text-center">{m.blue_score}</div>
              <button onClick={() => updateScore(m.id, 'blue', 1)} className="bg-blue-500 text-white px-3 py-1 rounded">+</button>
            </div>

            <div className="font-bold text-gray-400">VS</div>

            <div className="flex-1 flex justify-start items-center gap-4">
              <button onClick={() => updateScore(m.id, 'white', 1)} className="bg-gray-700 text-white px-3 py-1 rounded">+</button>
              <div className="text-2xl font-bold w-12 text-center">{m.white_score}</div>
              <button onClick={() => updateScore(m.id, 'white', -1)} className="bg-gray-200 px-3 py-1 rounded">-</button>
              <div className="text-left">
                <div className="text-gray-700 font-bold dark:text-gray-300">백팀</div>
                <div className="text-sm">{m.white_player1}, {m.white_player2}</div>
              </div>
            </div>
            
            <div>
              <button 
                onClick={async () => {
                  const newStatus = m.status === 'completed' ? 'pending' : 'completed';
                  await supabase.from('matches').update({ status: newStatus }).eq('id', m.id);
                  fetchMatches();
                }}
                className={`px-3 py-1 rounded text-sm font-bold ${m.status === 'completed' ? 'bg-gray-300' : 'bg-red-500 text-white'}`}
              >
                {m.status === 'completed' ? '종료됨' : '강제종료'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
