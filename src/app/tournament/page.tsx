"use client";

import { useEffect, useState } from "react";
import { Trophy, Clock, Swords, Users } from "lucide-react";
import { supabase } from "@/lib/supabase";

export default function TournamentPage() {
  const [matches, setMatches] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMatches();

    // 실시간 점수 반영 구독
    const subscription = supabase
      .channel('matches_changes')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'matches' }, payload => {
        fetchMatches(); // 데이터가 변경되면 즉시 다시 불러오기
      })
      .subscribe();

    return () => {
      supabase.removeChannel(subscription);
    };
  }, []);

  async function fetchMatches() {
    const { data, error } = await supabase
      .from('matches')
      .select('*')
      .order('round_num', { ascending: true })
      .order('court_num', { ascending: true });
    
    if (data) setMatches(data);
    setLoading(false);
  }

  // 라운드별로 그룹화
  const roundNums = Array.from(new Set(matches.map(m => m.round_num))).sort((a, b) => a - b);
  const rounds = roundNums.map(r => ({
    roundNum: r,
    matches: matches.filter(m => m.round_num === r)
  }));

  // 선수별 통계
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

  const totalBlueWins = matches.filter(m => m.status === 'completed' && m.blue_score > m.white_score).length;
  const totalWhiteWins = matches.filter(m => m.status === 'completed' && m.white_score > m.blue_score).length;

  if (loading) {
    return <div className="text-center py-20 text-gray-500 animate-pulse">대진표와 실시간 점수를 불러오는 중입니다...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="mb-12 text-center">
        <h1 className="text-3xl md:text-4xl font-black flex items-center justify-center gap-3 mb-8">
          <Trophy className="w-10 h-10 text-yellow-500" />
          제 1회 월례회 대진표
        </h1>
        
        {/* 상단 스코어 보드 */}
        <div className="flex justify-center items-center gap-4 md:gap-12 mb-6 max-w-2xl mx-auto bg-white dark:bg-gray-900 rounded-[2rem] p-8 shadow-xl border-4 border-gray-50 dark:border-gray-800">
          <div className="flex-1 text-center">
            <h2 className="text-lg md:text-xl font-bold text-blue-600 dark:text-blue-400 mb-2">청팀</h2>
            <div className="text-6xl md:text-8xl font-black text-blue-600 dark:text-blue-400 tracking-tighter">{totalBlueWins}</div>
          </div>
          
          <div className="text-gray-300 dark:text-gray-700 font-black text-3xl md:text-5xl italic px-4">VS</div>
          
          <div className="flex-1 text-center">
            <h2 className="text-lg md:text-xl font-bold text-gray-800 dark:text-gray-200 mb-2">백팀</h2>
            <div className="text-6xl md:text-8xl font-black text-gray-800 dark:text-gray-200 tracking-tighter">{totalWhiteWins}</div>
          </div>
        </div>
        
        <p className="text-gray-500 dark:text-gray-400 font-bold text-sm tracking-widest uppercase">Live Scoreboard</p>
      </div>

      <div className="flex flex-col xl:flex-row-reverse gap-8 items-start">
        {/* 사이드바 - 통계 */}
        <div className="w-full xl:w-1/4 bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm xl:sticky xl:top-24">
          <h2 className="text-lg font-bold mb-6 flex items-center justify-center xl:justify-start gap-2 border-b border-gray-100 dark:border-gray-800 pb-4">
            <Users className="text-yellow-600 w-5 h-5" />개인별 배정 경기 수
          </h2>
          <div className="flex gap-4">
            <div className="flex-1">
              <h3 className="text-sm font-bold text-blue-600 dark:text-blue-400 mb-3 text-center">청팀</h3>
              <ul className="space-y-2">
                {blueTeamStats.map(([name, count]) => (
                  <li key={name} className="flex justify-between items-center text-sm">
                    <span className="text-gray-700 dark:text-gray-300 truncate font-medium">{name.split('(')[0]}</span>
                    <span className="bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 px-2 py-0.5 rounded font-bold text-xs">{count}게임</span>
                  </li>
                ))}
              </ul>
            </div>
            <div className="w-px bg-gray-200 dark:bg-gray-800"></div>
            <div className="flex-1">
              <h3 className="text-sm font-bold text-gray-700 dark:text-gray-300 mb-3 text-center">백팀</h3>
              <ul className="space-y-2">
                {whiteTeamStats.map(([name, count]) => (
                  <li key={name} className="flex justify-between items-center text-sm">
                    <span className="text-gray-700 dark:text-gray-300 truncate font-medium">{name.split('(')[0]}</span>
                    <span className="bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 px-2 py-0.5 rounded font-bold text-xs">{count}게임</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 text-center xl:text-left">
            * 참가자 전원 경기 배정 완료
          </p>
        </div>

        {/* 메인 대진표 */}
        <div className="w-full xl:w-3/4 space-y-8">
          {rounds.map((round) => (
            <div key={round.roundNum} className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2 border-b border-gray-100 dark:border-gray-800 pb-4">
                <Clock className="text-yellow-600 w-6 h-6" />{round.roundNum}라운드
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {round.matches.map((match: any, idx: number) => {
                  const [actualType, bluePen, whitePen] = (match.match_type || '').split(':');
                  return (
                  <div key={idx} className={`rounded-2xl p-5 border shadow-sm transition-all ${match.status === 'completed' ? 'bg-white border-gray-200 dark:bg-gray-900 dark:border-gray-800' : 'bg-gray-50 border-gray-200 dark:bg-gray-950 dark:border-gray-800 hover:shadow-md'}`}>
                    <div className="flex justify-between items-center mb-5">
                      <span className="bg-yellow-400 text-yellow-950 text-xs font-black px-3 py-1.5 rounded-lg dark:bg-yellow-500 dark:text-yellow-950 shadow-sm">
                        코트 {match.court_num}
                      </span>
                      <span className="text-sm font-bold text-gray-500 dark:text-gray-400">
                        {actualType === 'MD' ? '남자 복식' : actualType === 'WD' ? '여자 복식' : '혼합 복식'}
                      </span>
                    </div>
                    
                    <div className="flex justify-between items-center gap-3">
                      <div className={`flex-1 text-center py-5 px-2 rounded-xl border-2 transition-all relative ${
                        match.status === 'completed' && match.blue_score > match.white_score 
                          ? 'bg-blue-50 border-blue-500 shadow-lg scale-105 z-10 dark:bg-blue-900/40 dark:border-blue-400' 
                          : match.status === 'completed' 
                            ? 'bg-gray-50 border-gray-100 opacity-40 grayscale dark:bg-gray-900/20 dark:border-gray-800' 
                            : 'bg-blue-50/50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-800/50'
                      }`}>
                        <div className="text-xs font-black text-blue-600 dark:text-blue-400 mb-2 flex justify-center items-center gap-1">청팀 {bluePen && bluePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {bluePen}</span>}</div>
                        <div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed">{match.blue_player1}</div>
                        <div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed">{match.blue_player2}</div>
                        
                        {match.status === 'completed' && match.blue_score > match.white_score && (
                          <div className="absolute -top-3 -right-3">
                            <span className="bg-blue-600 text-white text-[10px] font-black px-2 py-1 rounded-full shadow-md border-2 border-white dark:border-gray-900">WIN</span>
                          </div>
                        )}
                      </div>
                      
                      <div className="text-gray-300 flex-shrink-0 flex flex-col justify-center">
                        <span className="text-gray-300 dark:text-gray-600 font-black italic text-base">VS</span>
                      </div>
                      
                      <div className={`flex-1 text-center py-5 px-2 rounded-xl border-2 transition-all relative ${
                        match.status === 'completed' && match.white_score > match.blue_score 
                          ? 'bg-gray-100 border-gray-800 shadow-lg scale-105 z-10 dark:bg-gray-800 dark:border-gray-300' 
                          : match.status === 'completed' 
                            ? 'bg-gray-50 border-gray-100 opacity-40 grayscale dark:bg-gray-900/20 dark:border-gray-800' 
                            : 'bg-white border-gray-200 dark:bg-gray-800 dark:border-gray-700'
                      }`}>
                        <div className="text-xs font-black text-gray-600 dark:text-gray-400 mb-2 flex justify-center items-center gap-1">백팀 {whitePen && whitePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {whitePen}</span>}</div>
                        <div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed">{match.white_player1}</div>
                        <div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed">{match.white_player2}</div>
                        
                        {match.status === 'completed' && match.white_score > match.blue_score && (
                          <div className="absolute -top-3 -right-3">
                            <span className="bg-gray-800 dark:bg-gray-200 text-white dark:text-black text-[10px] font-black px-2 py-1 rounded-full shadow-md border-2 border-white dark:border-gray-900">WIN</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )})}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
