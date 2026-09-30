import { Trophy } from "lucide-react";

export default function TournamentPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="mb-12 text-center">
        <h1 className="text-3xl md:text-4xl font-bold flex items-center justify-center gap-3 mb-4">
          <Trophy className="w-8 h-8 text-yellow-500" />
          제 1회 월례회 대진표
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          경기 일정 및 실시간 결과를 확인할 수 있습니다.
        </p>
      </div>

      {/* 대진표 플레이스홀더 */}
      <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-8 shadow-sm min-h-[500px] flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
            <Trophy className="w-8 h-8 text-gray-400" />
          </div>
          <h2 className="text-xl font-semibold mb-2">대진표 준비 중</h2>
          <p className="text-gray-500 dark:text-gray-400 max-w-sm">
            경기 방식과 참가 인원이 확정되면 이곳에 멋진 실시간 대진표가 생성될 예정입니다.
          </p>
        </div>
      </div>
    </div>
  );
}
