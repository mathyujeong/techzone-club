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

  if (loading) {
    return <div className="text-center py-20 text-gray-500 animate-pulse">대진표와 실시간 점수를 불러오는 중입니다...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="mb-12 text-center">
        <h1 className="text-3xl md:text-4xl font-bold flex items-center justify-center gap-3 mb-4">
          <Trophy className="w-8 h-8 text-yellow-500" />
          제 1회 월례회 대진표
        </h1>
        <p className="text-gray-600 dark:text-gray-400 font-medium">실시간 경기 결과</p>
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
                  <div key={idx} className={`rounded-xl p-4 border ${match.status === 'completed' ? 'bg-gray-100 border-gray-300 opacity-60 dark:bg-gray-900 dark:border-gray-800' : 'bg-gray-50 border-gray-200 dark:bg-gray-950 dark:border-gray-800'}`}>
                    <div className="flex justify-between items-center mb-4">
                      <span className="bg-yellow-100 text-yellow-800 text-xs font-bold px-2 py-1 rounded dark:bg-yellow-900 dark:text-yellow-300">
                        코트 {match.court_num}
                      </span>
                      <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">
                        {actualType === 'MD' ? '남자 복식' : actualType === 'WD' ? '여자 복식' : '혼합 복식'}
                      </span>
                    </div>
                    
                    <div className="flex justify-between items-center gap-2">
                      <div className={`flex-1 text-center py-3 px-1 rounded-lg border ${match.status === 'completed' && match.blue_score > match.white_score ? 'bg-blue-100 border-blue-300 dark:bg-blue-900/40 dark:border-blue-700' : 'bg-blue-50 border-blue-100 dark:bg-blue-900/20 dark:border-blue-800/50'}`}>
                        <div className="text-xs font-bold text-blue-600 dark:text-blue-400 mb-1 flex justify-center items-center gap-1">청팀 {bluePen && bluePen !== '0' && <span className="text-[10px] bg-blue-200/50 px-1 rounded text-blue-800">패널티 {bluePen}</span>}</div>
                        <div className="font-semibold text-sm text-gray-900 dark:text-gray-100">{match.blue_player1}</div>
                        <div className="font-semibold text-sm text-gray-900 dark:text-gray-100">{match.blue_player2}</div>
                        <div className="mt-2 h-6 flex items-center justify-center">
                          {match.status === 'completed' && match.blue_score > match.white_score && (
                            <span className="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full shadow-sm">승리</span>
                          )}
                        </div>
                      </div>
                      
                      <div className="text-gray-400 flex-shrink-0">
                        <span className="text-gray-300 dark:text-gray-600 font-black italic text-sm">VS</span>
                      </div>
                      
                      <div className={`flex-1 text-center py-3 px-1 rounded-lg border ${match.status === 'completed' && match.white_score > match.blue_score ? 'bg-gray-200 border-gray-400 dark:bg-gray-800/80 dark:border-gray-600' : 'bg-white border-gray-200 dark:bg-gray-800 dark:border-gray-700'} shadow-sm`}>
                        <div className="text-xs font-bold text-gray-600 dark:text-gray-400 mb-1 flex justify-center items-center gap-1">백팀 {whitePen && whitePen !== '0' && <span className="text-[10px] bg-gray-200/50 px-1 rounded text-gray-800">패널티 {whitePen}</span>}</div>
                        <div className="font-semibold text-sm text-gray-900 dark:text-gray-100">{match.white_player1}</div>
                        <div className="font-semibold text-sm text-gray-900 dark:text-gray-100">{match.white_player2}</div>
                        <div className="mt-2 h-6 flex items-center justify-center">
                          {match.status === 'completed' && match.white_score > match.blue_score && (
                            <span className="bg-gray-800 dark:bg-gray-200 text-white dark:text-black text-xs font-bold px-3 py-1 rounded-full shadow-sm">승리</span>
                          )}
                        </div>
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
