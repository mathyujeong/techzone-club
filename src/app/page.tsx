import Link from "next/link";
import Image from "next/image";
import { ArrowRight, Trophy } from "lucide-react";
import AddToHomeButton from "@/components/AddToHomeButton";

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-20 flex flex-col items-center justify-center text-center">
      <div className="mb-8 relative w-48 h-48 md:w-64 md:h-64 rounded-full overflow-hidden shadow-2xl border-4 border-yellow-500/20">
        <Image src="/logo.jpg" alt="TechZone Club Logo" fill className="object-cover" priority />
      </div>

      <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-yellow-50 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400 text-sm font-medium mb-8 border border-yellow-200 dark:border-yellow-800/50">
        <Trophy className="w-4 h-4" />
        <span>제 1회 테크존 클럽 월례회 개최!</span>
      </div>
      
      <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6">
        TECHZONE<br />
        <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-600 to-yellow-400">
          BADMINTON CLUB
        </span>
      </h1>
      
      <p className="text-lg md:text-xl text-gray-600 dark:text-gray-400 mb-10 max-w-2xl">
        SINCE 2026. 실력에 상관없이 누구나 즐겁게 운동할 수 있는 열린 모임입니다. 
        이번 월례회 대진표를 확인하고 결과를 실시간으로 공유해보세요.
      </p>
      
      <div className="flex flex-col sm:flex-row gap-4">
        <Link 
          href="/tournament" 
          className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-yellow-600 text-white rounded-xl font-semibold hover:bg-yellow-700 transition-colors shadow-lg shadow-yellow-600/30"
        >
          대진표 확인하기
          <ArrowRight className="w-5 h-5" />
        </Link>
        <Link 
          href="/about" 
          className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white text-gray-900 border border-gray-200 rounded-xl font-semibold hover:bg-gray-50 transition-colors dark:bg-gray-900 dark:text-white dark:border-gray-800 dark:hover:bg-gray-800"
        >
          클럽 소개
        </Link>
      </div>

      <AddToHomeButton />
    </div>
  );
}

