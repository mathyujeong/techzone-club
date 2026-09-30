import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Navigation } from "@/components/Navigation";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "테크존 배드민턴 클럽",
  description: "테크존 클럽 공식 웹사이트 및 대진표",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className={`${inter.className} bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-gray-50 antialiased min-h-screen flex flex-col`}>
        <Navigation />
        <main className="flex-1">
          {children}
        </main>
        <footer className="border-t border-gray-200 dark:border-gray-800 py-8 text-center text-sm text-gray-500 dark:text-gray-400">
          © {new Date().getFullYear()} TechZone Badminton Club. All rights reserved.
        </footer>
      </body>
    </html>
  );
}
