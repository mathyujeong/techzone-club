import { Trophy, Clock, Swords, Users } from "lucide-react";
import scheduleData from "@/data/tournament.json";

export default function TournamentPage() {
  const rounds = [1, 2, 3, 4, 5, 6, 7].map(r => ({
    roundNum: r,
    matches: scheduleData.filter((m: any) => m.round === r)
  }));

  // 선수별 경기 수 계산
  const playerStats: Record<string, number> = {};
  scheduleData.forEach((match: any) => {
    match.blue_team.forEach((p: string) => {
      playerStats[p] = (playerStats[p] || 0) + 1;
    });
    match.white_team.forEach((p: string) => {
      playerStats[p] = (playerStats[p] || 0) + 1;
    });
  });

  // 팀별로 분리 및 정렬 (게임 수 내림차순, 이름 오름차순)
  const blueTeamStats = Object.entries(playerStats)
    .filter(([name]) => scheduleData.some((m: any) => m.blue_team.includes(name)))
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  
  const whiteTeamStats = Object.entries(playerStats)
    .filter(([name]) => scheduleData.some((m: any) => m.white_team.includes(name)))
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="mb-12 text-center">
        <h1 className="text-3xl md:text-4xl font-bold flex items-center justify-center gap-3 mb-4">
          <Trophy className="w-8 h-8 text-yellow-500" />
          제 1회 월례회 대진표
        </h1>
        <p className="text-gray-600 dark:text-gray-400 font-medium">
          총 24명 참가 (청팀 12명 vs 백팀 12명)
        </p>
        <p className="text-sm text-gray-500 mt-2">
          남복 7경기 | 여복 9경기 | 혼복 4경기 (총 20경기, 코트 3개 운영)
        </p>
      </div>

      <div className="flex flex-col xl:flex-row-reverse gap-8 items-start">
        
        {/* 사이드바 - 개인별 배정 경기 수 (모바일: 상단, PC: 우측 고정) */}
        <div className="w-full xl:w-1/4 bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm xl:sticky xl:top-24">
          <h2 className="text-lg font-bold mb-6 flex items-center justify-center xl:justify-start gap-2 border-b border-gray-100 dark:border-gray-800 pb-4">
            <Users className="text-yellow-600 w-5 h-5" />
            개인별 배정 경기 수
          </h2>
          
          <div className="flex gap-4">
            {/* 청팀 통계 */}
            <div className="flex-1">
              <h3 className="text-sm font-bold text-blue-600 dark:text-blue-400 mb-3 text-center">청팀</h3>
              <ul className="space-y-2">
                {blueTeamStats.map(([name, count]) => (
                  <li key={name} className="flex justify-between items-center text-sm">
                    <span className="text-gray-700 dark:text-gray-300 truncate font-medium" title={name}>{name.split('(')[0]}</span>
                    <span className="bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 px-2 py-0.5 rounded font-bold text-xs">
                      {count}게임
                    </span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="w-px bg-gray-200 dark:bg-gray-800"></div>
            
            {/* 백팀 통계 */}
            <div className="flex-1">
              <h3 className="text-sm font-bold text-gray-700 dark:text-gray-300 mb-3 text-center">백팀</h3>
              <ul className="space-y-2">
                {whiteTeamStats.map(([name, count]) => (
                  <li key={name} className="flex justify-between items-center text-sm">
                    <span className="text-gray-700 dark:text-gray-300 truncate font-medium" title={name}>{name.split('(')[0]}</span>
                    <span className={`px-2 py-0.5 rounded font-bold text-xs ${name.includes('조유정') ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'}`}>
                      {count}게임
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          
          <p className="text-xs text-gray-500 mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 text-center xl:text-left">
            * 전원 3~4게임 배정 완료 (조유정님 3게임 고정)
          </p>
        </div>

        {/* 메인 대진표 */}
        <div className="w-full xl:w-3/4 space-y-8">
          {rounds.map((round) => (
            <div key={round.roundNum} className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2 border-b border-gray-100 dark:border-gray-800 pb-4">
                <Clock className="text-yellow-600 w-6 h-6" />
                {round.roundNum}라운드
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {round.matches.map((match: any, idx: number) => (
                  <div key={idx} className="bg-gray-50 dark:bg-gray-950 rounded-xl p-4 border border-gray-200 dark:border-gray-800">
                    <div className="flex justify-between items-center mb-4">
                      <span className="bg-yellow-100 text-yellow-800 text-xs font-bold px-2 py-1 rounded dark:bg-yellow-900 dark:text-yellow-300">
                        코트 {match.court}
                      </span>
                      <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">
                        {match.type === 'MD' ? '남자 복식' : match.type === 'WD' ? '여자 복식' : '혼합 복식'}
                      </span>
                    </div>
                    
                    <div className="flex justify-between items-center gap-2">
                      {/* 청팀 */}
                      <div className="flex-1 text-center bg-blue-50 dark:bg-blue-900/20 py-3 px-1 rounded-lg border border-blue-100 dark:border-blue-800/50">
                        <div className="text-xs font-bold text-blue-600 dark:text-blue-400 mb-1">청팀 ({match.blue_score})</div>
                        <div className="font-semibold text-sm text-gray-900 dark:text-gray-100">{match.blue_team[0]}</div>
                        <div className="font-semibold text-sm text-gray-900 dark:text-gray-100">{match.blue_team[1]}</div>
                      </div>
                      
                      <div className="text-gray-400 flex-shrink-0">
                        <Swords className="w-4 h-4" />
                      </div>
                      
                      {/* 백팀 */}
                      <div className="flex-1 text-center bg-white dark:bg-gray-800 py-3 px-1 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
                        <div className="text-xs font-bold text-gray-600 dark:text-gray-400 mb-1">백팀 ({match.white_score})</div>
                        <div className="font-semibold text-sm text-gray-900 dark:text-gray-100">{match.white_team[0]}</div>
                        <div className="font-semibold text-sm text-gray-900 dark:text-gray-100">{match.white_team[1]}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}
