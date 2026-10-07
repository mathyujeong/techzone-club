"use client";

import { useEffect, useState } from "react";
import { Download } from "lucide-react";

export default function AddToHomeButton() {
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null);
  const [isIOS, setIsIOS] = useState(false);
  const [isStandalone, setIsStandalone] = useState(true); // 기본적으로는 안보이게 처리 (서버사이드 방지)

  useEffect(() => {
    // PWA로 이미 설치되어 있는지 확인
    const isPwa = window.matchMedia("(display-mode: standalone)").matches || (window.navigator as any).standalone;
    setIsStandalone(isPwa);

    const isIosDevice = /iPad|iPhone|iPod/.test(navigator.userAgent) && !(window as any).MSStream;
    setIsIOS(isIosDevice);

    const handleBeforeInstallPrompt = (e: any) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setIsStandalone(false); // 설치 가능 상태이므로 버튼 표시
    };

    window.addEventListener("beforeinstallprompt", handleBeforeInstallPrompt);

    // iOS는 설치 프롬프트가 없으므로 무조건 보여줌 (단, 이미 설치된 상태가 아니라면)
    if (isIosDevice && !isPwa) {
      setIsStandalone(false);
    }

    return () => {
      window.removeEventListener("beforeinstallprompt", handleBeforeInstallPrompt);
    };
  }, []);

  const handleInstallClick = () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then((choiceResult: any) => {
        setDeferredPrompt(null);
      });
    } else if (isIOS) {
      alert("Safari 하단 메뉴에서 '공유' 아이콘(네모 위로 화살표)을 누른 후 '홈 화면에 추가'를 선택해주세요.");
    } else {
      alert("브라우저 메뉴(⋮)에서 '홈 화면에 추가' 또는 '앱 설치'를 선택해주세요.");
    }
  };

  if (isStandalone) return null;

  return (
    <button
      onClick={handleInstallClick}
      className="mt-16 flex items-center justify-center gap-1.5 px-4 py-2 text-xs font-medium text-gray-500 bg-gray-50 border border-gray-200 rounded-full hover:bg-gray-100 hover:text-gray-700 transition-all dark:bg-gray-900 dark:border-gray-800 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-gray-300 shadow-sm"
    >
      <Download className="w-3.5 h-3.5" />
      <span>홈 화면에 추가</span>
    </button>
  );
}
