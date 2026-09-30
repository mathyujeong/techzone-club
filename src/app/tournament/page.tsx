import { Trophy, Clock, Swords } from "lucide-react";
import scheduleData from "@/data/tournament.json";

export default function TournamentPage() {
  const rounds = [1, 2, 3, 4, 5, 6, 7].map(r => ({
    roundNum: r,
    matches: scheduleData.filter((m: any) => m.round === r)
  }));

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

      <div className="space-y-8">
        {rounds.map((round) => (
          <div key={round.roundNum} className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-2 border-b border-gray-100 dark:border-gray-800 pb-4">
              <Clock className="text-yellow-600 w-6 h-6" />
              {round.roundNum}라운드
            </h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
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
                      <div className="font-semibold text-gray-900 dark:text-gray-100">{match.blue_team[0]}</div>
                      <div className="font-semibold text-gray-900 dark:text-gray-100">{match.blue_team[1]}</div>
                    </div>
                    
                    <div className="text-gray-400 flex-shrink-0">
                      <Swords className="w-5 h-5" />
                    </div>
                    
                    {/* 백팀 */}
                    <div className="flex-1 text-center bg-white dark:bg-gray-800 py-3 px-1 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
                      <div className="text-xs font-bold text-gray-600 dark:text-gray-400 mb-1">백팀 ({match.white_score})</div>
                      <div className="font-semibold text-gray-900 dark:text-gray-100">{match.white_team[0]}</div>
                      <div className="font-semibold text-gray-900 dark:text-gray-100">{match.white_team[1]}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
