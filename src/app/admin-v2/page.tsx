'use client';

import React, { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { Trophy, Plus, Calendar, Settings, Users, ChevronRight, Activity, X, RefreshCw, Save } from 'lucide-react';
import { generateMatches } from '@/lib/matchMaker';
import { Player } from '@/lib/types';

export default function AdminDashboard() {
  const [tournaments, setTournaments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Modal state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [players, setPlayers] = useState<Player[]>([]);
  const [selectedPlayerIds, setSelectedPlayerIds] = useState<Set<string>>(new Set());
  
  // Bracket generation state
  const [generatedBracket, setGeneratedBracket] = useState<any[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    fetchTournaments();
    fetchPlayers();
  }, []);

  const fetchTournaments = async () => {
    const { data } = await supabase.from('tournaments').select('*').order('created_at', { ascending: false });
    if (data) setTournaments(data);
    setLoading(false);
  };

  const fetchPlayers = async () => {
    const { data } = await supabase.from('players').select('*').order('grade', { ascending: true });
    if (data) {
      setPlayers(data);
      // default select all for demo
      setSelectedPlayerIds(new Set(data.map(p => p.id)));
    }
  };

  const handleGenerate = () => {
    setIsGenerating(true);
    setTimeout(() => {
      const activePlayers = players.filter(p => selectedPlayerIds.has(p.id));
      const matches = generateMatches(activePlayers, 'TEAM', 7);
      setGeneratedBracket(matches);
      setIsGenerating(false);
    }, 600); // fake loading for effect
  };

  const handleSwap = (matchIndex: number, team: 'blue' | 'white', playerIndex: 0 | 1) => {
    // Simple prompt for now - could be a dropdown in a real UI
    const targetName = prompt('누구와 교체하시겠습니까? (이름 입력)');
    if (!targetName) return;
    
    const targetPlayer = players.find(p => p.name === targetName);
    if (!targetPlayer) {
      alert('존재하지 않는 회원입니다.');
      return;
    }

    const newBracket = [...generatedBracket];
    if (team === 'blue') {
      newBracket[matchIndex].blue_team[playerIndex] = targetPlayer;
    } else {
      newBracket[matchIndex].white_team[playerIndex] = targetPlayer;
    }
    setGeneratedBracket(newBracket);
  };

  const saveTournament = async () => {
    // 1. Create Tournament
    const { data: tData, error: tErr } = await supabase.from('tournaments').insert({
      title: `${new Date().getMonth() + 1}월 자동생성 월례회`,
      match_type: 'TEAM',
      display_mode: 'SCORE',
      status: 'IN_PROGRESS'
    }).select().single();

    if (tErr || !tData) return alert('생성 실패!');

    // 2. Insert Matches
    const matchInserts = generatedBracket.map((m, i) => ({
      tournament_id: tData.id,
      round_num: Math.floor(i / 3) + 1,
      court_num: (i % 3) + 1,
      match_type: m.match_type,
      blue_player1: m.blue_team[0].name,
      blue_player2: m.blue_team[1].name,
      white_player1: m.white_team[0].name,
      white_player2: m.white_team[1].name,
      blue_score: 0,
      white_score: 0,
      blue_handicap: m.blue_handicap,
      white_handicap: m.white_handicap,
      status: 'pending'
    }));

    await supabase.from('matches').insert(matchInserts);
    setIsModalOpen(false);
    fetchTournaments();
    alert('대진표가 성공적으로 저장되었습니다!');
  };

  return (
    <div className="min-h-screen bg-[#F9FAFB] dark:bg-gray-950 pb-20">
      <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-10">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-blue-600 p-2 rounded-xl text-white shadow-sm">
              <Trophy className="w-5 h-5" />
            </div>
            <h1 className="text-xl font-bold text-gray-900 dark:text-white tracking-tight">
              클럽 관리자 v2
            </h1>
          </div>
          <button 
            onClick={() => {
              setGeneratedBracket([]);
              setIsModalOpen(true);
            }}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-full font-medium text-sm transition-colors flex items-center gap-2 shadow-sm"
          >
            <Plus className="w-4 h-4" />
            새 대회 생성
          </button>
        </div>
      </header>

      <main className="container mx-auto px-4 mt-8 max-w-4xl space-y-8">
        {/* Dashboard Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: '진행중인 대회', value: tournaments.filter(t => t.status === 'IN_PROGRESS').length, icon: Activity, color: 'text-green-600', bg: 'bg-green-100 dark:bg-green-900/30' },
            { label: '누적 대회', value: tournaments.length, icon: Calendar, color: 'text-blue-600', bg: 'bg-blue-100 dark:bg-blue-900/30' },
            { label: '등록 회원', value: players.length, icon: Users, color: 'text-purple-600', bg: 'bg-purple-100 dark:bg-purple-900/30' },
            { label: '시스템 설정', value: '⚙️', icon: Settings, color: 'text-gray-600', bg: 'bg-gray-100 dark:bg-gray-800' },
          ].map((stat, i) => (
            <div key={i} className="bg-white dark:bg-gray-900 p-4 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm flex flex-col gap-3">
              <div className={`w-8 h-8 rounded-full ${stat.bg} ${stat.color} flex items-center justify-center`}>
                <stat.icon className="w-4 h-4" />
              </div>
              <div>
                <div className="text-2xl font-black text-gray-900 dark:text-white">{stat.value}</div>
                <div className="text-xs font-medium text-gray-500">{stat.label}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Tournament List */}
        <div>
          <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4">대회 목록</h2>
          <div className="bg-white dark:bg-gray-900 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm overflow-hidden">
            {tournaments.map((t, idx) => (
              <div key={t.id} className={`p-5 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-800/50 cursor-pointer ${idx !== tournaments.length - 1 ? 'border-b border-gray-100 dark:border-gray-800' : ''}`}>
                <div className="flex items-center gap-4">
                  <div className={`w-2 h-2 rounded-full ${t.status === 'IN_PROGRESS' ? 'bg-green-500 animate-pulse' : t.status === 'COMPLETED' ? 'bg-gray-300' : 'bg-amber-400'}`} />
                  <div>
                    <h3 className="font-bold text-gray-900 dark:text-white text-base">{t.title}</h3>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-xs font-medium text-gray-500 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-md">
                        {t.match_type === 'TEAM' ? '청백전' : '개인복식'}
                      </span>
                      <span className="text-[10px] text-gray-400">
                        {new Date(t.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="text-gray-400 flex items-center gap-2">
                  <span className="text-sm font-medium">{t.status === 'IN_PROGRESS' ? '관리하기' : '기록보기'}</span>
                  <ChevronRight className="w-5 h-5" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Generation Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white dark:bg-gray-900 rounded-3xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col shadow-2xl">
            
            <div className="p-6 border-b border-gray-100 dark:border-gray-800 flex items-center justify-between">
              <h2 className="text-xl font-bold">대진표 자동 생성기</h2>
              <button onClick={() => setIsModalOpen(false)} className="p-2 hover:bg-gray-100 rounded-full">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 flex-1 overflow-y-auto flex flex-col md:flex-row gap-8 bg-gray-50 dark:bg-gray-950">
              {/* Left: Player Selection */}
              <div className="w-full md:w-1/3 space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="font-bold">참가자 선택</h3>
                  <span className="text-sm text-blue-600 font-bold">{selectedPlayerIds.size}명 선택됨</span>
                </div>
                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-4 max-h-[50vh] overflow-y-auto space-y-2">
                  {players.map(p => (
                    <label key={p.id} className="flex items-center gap-3 p-2 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg cursor-pointer">
                      <input 
                        type="checkbox" 
                        className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500"
                        checked={selectedPlayerIds.has(p.id)}
                        onChange={(e) => {
                          const next = new Set(selectedPlayerIds);
                          if (e.target.checked) next.add(p.id);
                          else next.delete(p.id);
                          setSelectedPlayerIds(next);
                        }}
                      />
                      <span className="font-medium text-sm">{p.name}</span>
                      <span className="text-xs text-gray-500 bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded">{p.grade}급</span>
                    </label>
                  ))}
                </div>
                <button 
                  onClick={handleGenerate}
                  disabled={isGenerating || selectedPlayerIds.size < 4}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  <RefreshCw className={`w-5 h-5 ${isGenerating ? 'animate-spin' : ''}`} />
                  대진표 무작위 생성
                </button>
              </div>

              {/* Right: Bracket Preview */}
              <div className="w-full md:w-2/3">
                <h3 className="font-bold mb-4">대진표 미리보기 (클릭하여 수동 교체)</h3>
                
                {generatedBracket.length === 0 ? (
                  <div className="h-64 flex flex-col items-center justify-center text-gray-400 border-2 border-dashed border-gray-200 dark:border-gray-800 rounded-2xl">
                    <Trophy className="w-12 h-12 mb-2 opacity-50" />
                    <p>좌측에서 생성 버튼을 눌러주세요</p>
                  </div>
                ) : (
                  <div className="space-y-3 max-h-[50vh] overflow-y-auto pr-2">
                    {generatedBracket.map((m, idx) => (
                      <div key={idx} className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-3 flex shadow-sm">
                        
                        {/* Blue Team */}
                        <div className="flex-1 flex flex-col justify-center gap-1 border-r border-gray-100 dark:border-gray-800 pr-3">
                          <span className="text-xs font-bold text-blue-600 mb-1">청팀</span>
                          <div className="flex gap-2">
                            <button onClick={() => handleSwap(idx, 'blue', 0)} className="text-sm bg-gray-50 hover:bg-gray-100 p-1 rounded font-medium w-full text-left truncate border border-transparent hover:border-gray-200">{m.blue_team[0].name} <span className="text-xs text-gray-400">{m.blue_team[0].grade}</span></button>
                            <button onClick={() => handleSwap(idx, 'blue', 1)} className="text-sm bg-gray-50 hover:bg-gray-100 p-1 rounded font-medium w-full text-left truncate border border-transparent hover:border-gray-200">{m.blue_team[1].name} <span className="text-xs text-gray-400">{m.blue_team[1].grade}</span></button>
                          </div>
                        </div>

                        {/* VS */}
                        <div className="px-4 flex items-center justify-center font-black text-gray-300 italic">VS</div>

                        {/* White Team */}
                        <div className="flex-1 flex flex-col justify-center gap-1 pl-3">
                          <span className="text-xs font-bold text-gray-600 mb-1">백팀</span>
                          <div className="flex gap-2">
                            <button onClick={() => handleSwap(idx, 'white', 0)} className="text-sm bg-gray-50 hover:bg-gray-100 p-1 rounded font-medium w-full text-left truncate border border-transparent hover:border-gray-200">{m.white_team[0].name} <span className="text-xs text-gray-400">{m.white_team[0].grade}</span></button>
                            <button onClick={() => handleSwap(idx, 'white', 1)} className="text-sm bg-gray-50 hover:bg-gray-100 p-1 rounded font-medium w-full text-left truncate border border-transparent hover:border-gray-200">{m.white_team[1].name} <span className="text-xs text-gray-400">{m.white_team[1].grade}</span></button>
                          </div>
                        </div>

                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Footer */}
            <div className="p-4 border-t border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-900 flex justify-end gap-3">
              <button onClick={() => setIsModalOpen(false)} className="px-5 py-2 font-medium text-gray-600 hover:bg-gray-100 rounded-xl">취소</button>
              <button 
                onClick={saveTournament}
                disabled={generatedBracket.length === 0}
                className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl flex items-center gap-2 disabled:opacity-50"
              >
                <Save className="w-4 h-4" />
                이 대진표로 저장하기
              </button>
            </div>
            
          </div>
        </div>
      )}
    </div>
  );
}
