/* eslint-disable */
"use client";

import { useEffect, useState } from "react";
import { Trophy, Clock, Swords, Users } from "lucide-react";
import { supabase } from "@/lib/supabase";

export default function TournamentPage() {
  const [tournaments, setTournaments] = useState<any[]>([]);
  const [activeTournament, setActiveTournament] = useState<any>(null);
  const [matches, setMatches] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPlayer, setSelectedPlayer] = useState<string | null>(null);
  const [dbPlayers, setDbPlayers] = useState<any[]>([]);
  const [showGrades, setShowGrades] = useState(false);
  
  const getPlayerGrade = (name: string) => {
    const p = dbPlayers.find(player => player.name === name);
    return p ? p.grade : '';
  };

  async function fetchAllData() {
    const { data: tData } = await supabase
      .from('tournaments')
      .select('*')
      .order('created_at', { ascending: false });
      
    if (tData && tData.length > 0) {
      setTournaments(tData);
      if (!activeTournament) {
        setActiveTournament(tData[0]);
        fetchMatches(tData[0].id);
      }
    } else {
      setLoading(false);
    }
  }

  async function fetchMatches(tournamentId: string) {
    setLoading(true);
    const { data, error } = await supabase
      .from('matches')
      .select('*')
      .eq('tournament_id', tournamentId)
      .order('round_num', { ascending: true })
      .order('court_num', { ascending: true });
      
    if (data) setMatches(data);
    setLoading(false);
  }

  const handleTournamentChange = (id: string) => {
    const t = tournaments.find(x => x.id === id);
    if (t) {
      setActiveTournament(t);
      setSelectedPlayer(null); // Reset player filter on tournament change
      fetchMatches(t.id);
    }
  };

  useEffect(() => {
    fetchAllData();

    const subscription = supabase
      .channel('matches_changes')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'matches' }, payload => {
        if (activeTournament) fetchMatches(activeTournament.id);
      })
      .subscribe();

    return () => {
      supabase.removeChannel(subscription);
    };
  }, [activeTournament?.id]);

  // 라운드별로 그룹화
  const roundNums = Array.from(new Set(matches.map(m => m.round_num))).sort((a, b) => a - b);
  const rounds = roundNums.map(r => ({
    roundNum: r,
    matches: matches.filter(m => m.round_num === r)
  }));

  // 선수별 통계
  const isIndividualMode = activeTournament?.match_type === 'INDIVIDUAL';
  const playerStatsMap: Record<string, { matches: number, wins: number, team: 'BLUE' | 'WHITE' | 'MIXED' }> = {};
  
  dbPlayers.forEach(p => {
    playerStatsMap[p.name] = { matches: 0, wins: 0, team: 'MIXED' };
  });

  matches.forEach(m => {
    const isCompleted = m.status === 'completed';
    const blueWon = isCompleted && m.blue_score > m.white_score;
    const whiteWon = isCompleted && m.white_score > m.blue_score;
    
    const addStat = (pName: string, isBlue: boolean) => {
      if (!pName) return;
      if (!playerStatsMap[pName]) playerStatsMap[pName] = { matches: 0, wins: 0, team: isBlue ? 'BLUE' : 'WHITE' };
      
      playerStatsMap[pName].matches++;
      if (playerStatsMap[pName].team !== (isBlue ? 'BLUE' : 'WHITE')) {
        playerStatsMap[pName].team = 'MIXED';
      }
      
      if (isBlue && blueWon) playerStatsMap[pName].wins++;
      if (!isBlue && whiteWon) playerStatsMap[pName].wins++;
    };

    addStat(String(m.blue_player1), true);
    addStat(String(m.blue_player2), true);
    addStat(String(m.white_player1), false);
    addStat(String(m.white_player2), false);
  });

  const allStats = Object.entries(playerStatsMap)
    .map(([name, data]) => ({ name, ...data }))
    ; // Only show people who actually played (optional, but requested by user?)
    // Actually, user complained people were missing!
    // But if they didn't play at all, it's fine. Wait, user said "어떤 회원은 아예 리스트에도 없는거지?". I should NOT filter out matches=0 if it's the ADMIN panel, but for member view, keeping everyone who was selected might be good.
    // Wait, in member view, we don't know who was "selected", we only know `dbPlayers`. Showing 40 people with 0 matches is bad. Let's just filter `matches > 0`.
    // Wait, Admin mode has `activePlayersForDropdown`, so it knows. Member mode doesn't.
    // Let's filter `matches > 0` for Member mode.
  
  const blueTeamStats = allStats.filter(s => s.team === 'BLUE').sort((a, b) => b.matches - a.matches || b.wins - a.wins);
  const whiteTeamStats = allStats.filter(s => s.team === 'WHITE').sort((a, b) => b.matches - a.matches || b.wins - a.wins);
  const individualStats = [...allStats].sort((a, b) => b.wins - a.wins || b.matches - a.matches);

  const totalBlueWins = matches.filter(m => m.status === 'completed' && m.blue_score > m.white_score).length;
  const totalWhiteWins = matches.filter(m => m.status === 'completed' && m.white_score > m.blue_score).length;

  if (loading) {
    return <div className="text-center py-20 text-gray-500 animate-pulse">대진표와 실시간 점수를 불러오는 중입니다...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="mb-12 text-center">
        <div className="flex flex-col items-center justify-center mb-8 space-y-4">
          <div className="flex items-center justify-center gap-3">
            <Trophy className="w-10 h-10 text-yellow-500" />
            <h1 className="text-3xl md:text-4xl font-black">
              대진표 및 실시간 점수
            </h1>
          </div>
          
          {tournaments.length > 0 && (
            <div className="relative inline-block w-full max-w-xs mt-4">
              <select 
                value={activeTournament?.id || ''} 
                onChange={(e) => handleTournamentChange(e.target.value)}
                className="w-full appearance-none bg-white dark:bg-gray-900 border-2 border-yellow-400 dark:border-yellow-600 rounded-2xl px-6 py-4 outline-none text-gray-900 dark:text-white focus:ring-4 focus:ring-yellow-500/20 transition-all font-bold text-center cursor-pointer shadow-md text-lg"
              >
                {tournaments.map(t => (
                  <option key={t.id} value={t.id}>{t.title}</option>
                ))}
              </select>
              <div className="absolute inset-y-0 right-4 flex items-center pointer-events-none">
                <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M19 9l-7 7-7-7" /></svg>
              </div>
            </div>
          )}
        </div>
        
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
            <Users className="text-yellow-600 w-5 h-5" />{isIndividualMode ? '개인별 배정 경기 수 및 승률 (성적순)' : '개인별 배정 경기 수'}
          </h2>
          
          {isIndividualMode ? (
            <div className="flex flex-col gap-2">
              {individualStats.map(s => {
                const isSelected = selectedPlayer === s.name;
                return (
                  <div key={s.name} onClick={() => setSelectedPlayer(isSelected ? null : s.name)} className={`flex justify-between items-center text-sm cursor-pointer p-2 -mx-2 rounded-lg transition-all ${isSelected ? 'bg-yellow-50 dark:bg-yellow-900/30 ring-1 ring-yellow-400' : 'hover:bg-gray-50 dark:hover:bg-gray-800'}`}>
                    <span className={`font-bold ${isSelected ? 'text-yellow-700 dark:text-yellow-400' : 'text-gray-800 dark:text-gray-200'}`}>{s.name}</span>
                    <div className="flex gap-2 text-xs">
                      <span className="text-gray-500">{s.matches}경기</span>
                      <span className="text-blue-600 font-black">{s.wins}승</span>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="flex gap-4">
              <div className="flex-1">
                <h3 className="text-sm font-bold text-blue-600 dark:text-blue-400 mb-3 text-center flex items-center justify-center gap-1">
                  청팀 <span className="bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 text-xs px-2 py-0.5 rounded-full">{blueTeamStats.length}명</span>
                </h3>
                <ul className="space-y-2">
                  {blueTeamStats.map(s => {
                    const isSelected = selectedPlayer === s.name;
                    return (
                      <li 
                        key={s.name} 
                        onClick={() => setSelectedPlayer(isSelected ? null : s.name)}
                        className={`flex justify-between items-center text-sm cursor-pointer p-2 -mx-2 rounded-lg transition-all ${isSelected ? 'bg-blue-100 dark:bg-blue-900/40 ring-1 ring-blue-300 dark:ring-blue-800' : 'hover:bg-gray-50 dark:hover:bg-gray-800/50'}`}
                      >
                        <span className={`truncate ${isSelected ? 'text-blue-700 dark:text-blue-300 font-bold' : 'text-gray-700 dark:text-gray-300 font-medium'}`}>{s.name}</span>
                        <span className={`${isSelected ? 'bg-blue-200 dark:bg-blue-800/50 text-blue-800 dark:text-blue-200' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'} px-2 py-0.5 rounded font-bold text-xs transition-colors`}>{s.matches}게임</span>
                      </li>
                    );
                  })}
                </ul>
              </div>
              <div className="w-px bg-gray-200 dark:bg-gray-800"></div>
              <div className="flex-1">
                <h3 className="text-sm font-bold text-gray-700 dark:text-gray-300 mb-3 text-center flex items-center justify-center gap-1">
                  백팀 <span className="bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 text-xs px-2 py-0.5 rounded-full">{whiteTeamStats.length}명</span>
                </h3>
                <ul className="space-y-2">
                  {whiteTeamStats.map(s => {
                    const isSelected = selectedPlayer === s.name;
                    return (
                      <li 
                        key={s.name} 
                        onClick={() => setSelectedPlayer(isSelected ? null : s.name)}
                        className={`flex justify-between items-center text-sm cursor-pointer p-2 -mx-2 rounded-lg transition-all ${isSelected ? 'bg-gray-200 dark:bg-gray-700/50 ring-1 ring-gray-300 dark:ring-gray-600' : 'hover:bg-gray-50 dark:hover:bg-gray-800/50'}`}
                      >
                        <span className={`truncate ${isSelected ? 'text-gray-900 dark:text-gray-100 font-bold' : 'text-gray-700 dark:text-gray-300 font-medium'}`}>{s.name}</span>
                        <span className={`${isSelected ? 'bg-gray-300 dark:bg-gray-600 text-gray-900 dark:text-gray-100' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'} px-2 py-0.5 rounded font-bold text-xs transition-colors`}>{s.matches}게임</span>
                      </li>
                    );
                  })}
                </ul>
              </div>
            </div>
          )}
          <div className="mt-6 pt-6 border-t border-gray-100 dark:border-gray-800">
            <h3 className="text-sm font-bold text-gray-800 dark:text-gray-200 mb-3 flex items-center justify-center gap-1">
              <Trophy className="w-4 h-4 text-yellow-500" />
              종목별 통계
            </h3>
            <div className="grid grid-cols-2 gap-2 mb-2 text-center text-sm font-bold">
              <div className="bg-blue-50 border border-blue-100 text-blue-700 dark:bg-blue-900/20 dark:border-blue-800/50 dark:text-blue-300 py-1.5 rounded-lg">
                남복 <span className="text-base font-black ml-1">{matches.filter(m => (m.match_type || '').startsWith('MD')).length}</span>
              </div>
              <div className="bg-pink-50 border border-pink-100 text-pink-700 dark:bg-pink-900/20 dark:border-pink-800/50 dark:text-pink-300 py-1.5 rounded-lg">
                여복 <span className="text-base font-black ml-1">{matches.filter(m => (m.match_type || '').startsWith('WD')).length}</span>
              </div>
              <div className="bg-purple-50 border border-purple-100 text-purple-700 dark:bg-purple-900/20 dark:border-purple-800/50 dark:text-purple-300 py-1.5 rounded-lg">
                혼복 <span className="text-base font-black ml-1">{matches.filter(m => (m.match_type || '').startsWith('XD')).length}</span>
              </div>
              <div className="bg-gray-100 border border-gray-200 text-gray-800 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-200 py-1.5 rounded-lg">
                총 <span className="text-base font-black ml-1">{matches.length}</span>
              </div>
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-4 pt-4 border-t border-gray-100 dark:border-gray-800 text-center xl:text-left">
            * 참가자 전원 경기 배정 완료
          </p>
        </div>

        {/* 메인 대진표 */}
        <div className="w-full xl:w-3/4 space-y-8">
          {rounds.map((round) => (
            <div key={round.roundNum} className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2 border-b border-gray-100 dark:border-gray-800 pb-4">
                <Clock className="text-yellow-600 w-6 h-6" />{round.roundNum}라운드
                <span className="text-sm font-medium text-gray-500 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full ml-2">
                  {(() => {
                    const totalMinutes = 580 + (round.roundNum - 1) * 20;
                    const hours = Math.floor(totalMinutes / 60);
                    const minutes = totalMinutes % 60;
                    return `${hours}:${minutes.toString().padStart(2, '0')}`;
                  })()}
                </span>
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {round.matches.map((match: Record<string, string | number>, idx: number) => {
                  const [actualType, bluePen, whitePen] = (String(match.match_type) || '').split(':');
                  const hasSelectedPlayer = selectedPlayer && [match.blue_player1, match.blue_player2, match.white_player1, match.white_player2].includes(selectedPlayer);
                  const isDimmed = selectedPlayer && !hasSelectedPlayer;
                  
                  return (
                  <div key={idx} className={`rounded-2xl p-5 border shadow-sm transition-all duration-300 ${
                    isDimmed ? 'opacity-30 grayscale-[50%] scale-95 border-transparent bg-gray-50 dark:bg-gray-950' : 
                    hasSelectedPlayer ? 'ring-4 ring-yellow-400 dark:ring-yellow-500 shadow-xl scale-[1.02] bg-white dark:bg-gray-900 border-yellow-400 dark:border-yellow-500 z-10 relative' : 
                    (match.status === 'completed' ? 'bg-white border-gray-200 dark:bg-gray-900 dark:border-gray-800' : 'bg-gray-50 border-gray-200 dark:bg-gray-950 dark:border-gray-800 hover:shadow-md')
                  }`}>
                    <div className="flex justify-between items-center mb-5">
                      <span className="bg-yellow-400 text-yellow-950 text-xs font-black px-3 py-1.5 rounded-lg dark:bg-yellow-500 dark:text-yellow-950 shadow-sm">
                        {match.court_num}코트
                      </span>
                      <span className="text-sm font-bold text-gray-500 dark:text-gray-400">
                        {actualType === 'MD' ? '남복' : actualType === 'WD' ? '여복' : actualType === 'XD' ? '혼복' : actualType}
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
                        <div className="text-xs font-black text-blue-600 dark:text-blue-400 mb-2 flex justify-center items-center gap-1">{activeTournament?.match_type !== 'INDIVIDUAL' && '청팀'} {bluePen && bluePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {bluePen}</span>}</div>
                        <div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed flex items-center gap-2"><span>{match.blue_player1}</span> {showGrades && <span className="text-[10px] font-black opacity-50 bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded">{getPlayerGrade(String(match.blue_player1))}</span>}</div>
                        <div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed flex items-center gap-2"><span>{match.blue_player2}</span> {showGrades && <span className="text-[10px] font-black opacity-50 bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded">{getPlayerGrade(String(match.blue_player2))}</span>}</div>
                        
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
                        <div className="text-xs font-black text-gray-600 dark:text-gray-400 mb-2 flex justify-center items-center gap-1">{activeTournament?.match_type !== 'INDIVIDUAL' && '백팀'} {whitePen && whitePen !== '0' && <span className="text-[10px] bg-red-100 text-red-600 px-1.5 rounded-full">패널티 {whitePen}</span>}</div>
                        <div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed flex items-center gap-2"><span>{match.white_player1}</span> {showGrades && <span className="text-[10px] font-black opacity-50 bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded">{getPlayerGrade(String(match.white_player1))}</span>}</div>
                        <div className="font-bold text-base text-gray-900 dark:text-gray-100 leading-relaxed flex items-center gap-2"><span>{match.white_player2}</span> {showGrades && <span className="text-[10px] font-black opacity-50 bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded">{getPlayerGrade(String(match.white_player2))}</span>}</div>
                        
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
