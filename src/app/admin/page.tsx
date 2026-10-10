/* eslint-disable */
"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";

import { generateMatches } from '@/lib/matchMaker';
import { Player } from '@/lib/types';
import { Save, X, Lock, Edit2, UserPlus, CheckSquare, Square, Users as UsersIcon } from 'lucide-react';
import { Settings, Plus, Minus, Check, Play, Pause, RefreshCw, Trophy, Users, Trash2, ChevronDown } from "lucide-react";

export default function AdminPage() {
  const [authed, setAuthed] = useState(false);
  const [pwd, setPwd] = useState("");
  const [matches, setMatches] = useState<any[]>([]);
  const [editPlayerModal, setEditPlayerModal] = useState<{ id: string, team: 'blue' | 'white', currentP1: string, currentP2: string } | null>(null);
  const [p1Select, setP1Select] = useState("");
  const [p1Input, setP1Input] = useState("");
  const [p2Select, setP2Select] = useState("");
  const [p2Input, setP2Input] = useState("");
  const [editMatchModal, setEditMatchModal] = useState<{ id: string, round: number, court: number, type: string, bluePen: number, whitePen: number } | null>(null);

  // --- New Bracket Generator State ---
  const [isGeneratorModalOpen, setIsGeneratorModalOpen] = useState(false);
  const [dbPlayers, setDbPlayers] = useState<Player[]>([]);
  const [selectedPlayerIds, setSelectedPlayerIds] = useState<Set<string>>(new Set());
  const [generatedBracket, setGeneratedBracket] = useState<any[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);

  const [numCourts, setNumCourts] = useState(3);
  const [numRounds, setNumRounds] = useState(5);
  const [ignoreGrade, setIgnoreGrade] = useState(false);
  const [hideGrade, setHideGrade] = useState(false);
  const [matchType, setMatchType] = useState<'TEAM' | 'INDIVIDUAL'>('TEAM');

  const [tournaments, setTournaments] = useState<any[]>([]);

  const [isPlayerManageModalOpen, setIsPlayerManageModalOpen] = useState(false);
  const [isGuestModalOpen, setIsGuestModalOpen] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState<{type: 'tournament'|'match', id: string} | null>(null);
  const [deleteCode, setDeleteCode] = useState("");
  const [guestName, setGuestName] = useState("");
  const [guestGrade, setGuestGrade] = useState("E");
  const [editingTournamentId, setEditingTournamentId] = useState<string | null>(null);
  const [editingTournamentName, setEditingTournamentName] = useState("");
  const [editingTournamentDate, setEditingTournamentDate] = useState("");


  const [selectedTournamentId, setSelectedTournamentId] = useState<string | null>(null);




  
  const handleAddNewTournament = async () => {
    const { data, error } = await supabase.from('tournaments').insert({ title: '새 월례회' }).select().single();
    if (data) {
      setTournaments([data, ...tournaments]);
      setSelectedTournamentId(data.id);
      setEditingTournamentId(data.id);
      setEditingTournamentName(data.title);
      setEditingTournamentDate(new Date(data.created_at).toISOString().split('T')[0]);
    } else {
      alert('대회 추가 실패: ' + (error?.message || ''));
    }
  };

  const executeDelete = async () => {
    if (deleteCode !== '0000') {
      alert('코드가 일치하지 않습니다.');
      return;
    }
    if (deleteConfirm?.type === 'tournament') {
      await supabase.from('tournaments').delete().eq('id', deleteConfirm.id);
      setTournaments(tournaments.filter(t => t.id !== deleteConfirm.id));
      if (selectedTournamentId === deleteConfirm.id) setSelectedTournamentId(null);
      setEditingTournamentId(null);
    } else if (deleteConfirm?.type === 'match') {
      setMatches(matches.filter(m => m.id !== deleteConfirm.id));
      await supabase.from('matches').delete().eq('id', deleteConfirm.id);
      setEditMatchModal(null);
      fetchPlayersAndTournaments();
    }
    setDeleteConfirm(null);
  };

  const deleteTournament = (id: string) => {
    setDeleteCode("");
    setDeleteConfirm({ type: 'tournament', id });
  };



  // --- Tournament Renaming ---
  const saveTournamentData = async (id: string) => {
    if(!editingTournamentName.trim() || !editingTournamentDate) return;
    const newDate = new Date(editingTournamentDate).toISOString();
    await supabase.from('tournaments').update({ title: editingTournamentName, created_at: newDate }).eq('id', id);
    setTournaments(tournaments.map(t => t.id === id ? { ...t, title: editingTournamentName, created_at: newDate } : t));
    setEditingTournamentId(null);
  };

  // --- Player Management ---
  const openGuestModal = () => {
    setGuestName("");
    setGuestGrade("E");
    setIsGuestModalOpen(true);
  };

  const saveGuest = async () => {
    if (!guestName.trim()) return;
    const { data, error } = await supabase.from('players').insert({ name: guestName.trim(), grade: guestGrade }).select().single();
    if (data) {
      setDbPlayers([...dbPlayers, data].sort((a, b) => a.grade.localeCompare(b.grade)));
      const newSet = new Set(selectedPlayerIds);
      newSet.add(data.id);
      setSelectedPlayerIds(newSet);
      setIsGuestModalOpen(false);
    } else {
      alert('추가 실패: ' + (error?.message || '알 수 없는 오류'));
    }
  };

  const updatePlayerGrade = async (id: string, newGrade: string) => {
    await supabase.from('players').update({ grade: newGrade as any }).eq('id', id);
    setDbPlayers(dbPlayers.map(p => p.id === id ? { ...p, grade: newGrade as any } : p));
  };

  async function fetchPlayersAndTournaments() {
    const { data: tData } = await supabase.from('tournaments').select('*').order('created_at', { ascending: false });
    if (tData) setTournaments(tData);

    const { data: pData } = await supabase.from('players').select('*').order('grade', { ascending: true });
    if (pData) {
      setDbPlayers(pData);
      setSelectedPlayerIds(new Set(pData.map(p => p.id)));
    }
  }

  useEffect(() => {
    if (authed) fetchPlayersAndTournaments();
  }, [authed]);

  const handleGenerate = () => {
    setIsGenerating(true);
    setTimeout(() => {
      const activePlayers = dbPlayers.filter(p => selectedPlayerIds.has(p.id));
      const matches = generateMatches(activePlayers, matchType, numCourts, numRounds, ignoreGrade);
      setGeneratedBracket(matches);
      setIsGenerating(false);
    }, 600);
  };

  const saveTournament = async () => {
    const { data: tData, error: tErr } = await supabase.from('tournaments').insert({
      title: `${new Date().getMonth() + 1}월 월례회`,
      match_type: 'TEAM',
      display_mode: 'SCORE',
      status: 'IN_PROGRESS'
    }).select().single();

    if (tErr || !tData) return alert('대회 생성 실패!');

    const matchInserts = generatedBracket.map((m, i) => ({
      tournament_id: tData.id,
      round_num: m.round_num || Math.floor(i / numCourts) + 1,
      court_num: m.court_num || (i % numCourts) + 1,
      match_type: m.match_type + ':0:0',
      blue_player1: m.blue_team[0].name,
      blue_player2: m.blue_team[1].name,
      white_player1: m.white_team[0].name,
      white_player2: m.white_team[1].name,
      blue_score: 0,
      white_score: 0,
      status: 'pending'
    }));

    await supabase.from('matches').insert(matchInserts);
    setIsGeneratorModalOpen(false);
    fetchMatches();
    alert('새 대진표가 성공적으로 적용되었습니다!');
  };

  const handleSwapGenerated = (matchIndex: number, team: 'blue' | 'white', playerIndex: 0 | 1) => {
    const targetName = prompt('누구와 교체하시겠습니까? (정확한 이름 입력)');
    if (!targetName) return;
    
    const targetPlayer = dbPlayers.find(p => p.name === targetName);
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


  async function fetchMatches() {
    const { data } = await supabase.from('matches').select('*').order('round_num').order('court_num');
    if (data) setMatches(data);
  }

  useEffect(() => {
    if (authed) fetchMatches();
  }, [authed]);

  async function setWinner(id: string, team: 'blue' | 'white') {
    const blueScore = team === 'blue' ? 1 : 0;
    const whiteScore = team === 'white' ? 1 : 0;
    
    setMatches(matches.map(m => m.id === id ? { ...m, blue_score: blueScore, white_score: whiteScore, status: 'completed' } : m));
    
    await supabase.from('matches').update({ 
      blue_score: blueScore, 
      white_score: whiteScore, 
      status: 'completed' 
    }).eq('id', id);
  }

  function editPlayers(id: string, team: 'blue' | 'white', p1: string, p2: string) {
    setEditPlayerModal({ id, team, currentP1: p1, currentP2: p2 });
    
    const teamStats = team === 'blue' ? blueTeamStats : whiteTeamStats;
    const isP1Exist = teamStats.some(([n]) => n === p1);
    const isP2Exist = teamStats.some(([n]) => n === p2);
    
    setP1Select(isP1Exist ? p1 : '직접입력');
    setP1Input(isP1Exist ? '' : p1);
    
    setP2Select(isP2Exist ? p2 : '직접입력');
    setP2Input(isP2Exist ? '' : p2);
  }

  async function savePlayers() {
    if (!editPlayerModal) return;
    const { id, team } = editPlayerModal;
    
    const finalP1 = p1Select === '직접입력' ? p1Input.trim() : p1Select;
    const finalP2 = p2Select === '직접입력' ? p2Input.trim() : p2Select;
    
    if(!finalP1 || !finalP2) {
      alert("선수 이름을 모두 입력해주세요.");
      return;
    }

    const updateData: Record<string, string> = team === 'blue' 
      ? { blue_player1: finalP1, blue_player2: finalP2 } 
      : { white_player1: finalP1, white_player2: finalP2 };

    const m = matches.find(m => m.id === id);
    if (m) {
      const b1 = team === 'blue' ? finalP1 : m.blue_player1;
      const b2 = team === 'blue' ? finalP2 : m.blue_player2;
      const w1 = team === 'white' ? finalP1 : m.white_player1;
      const w2 = team === 'white' ? finalP2 : m.white_player2;
      
      const PLAYER_PENALTY: Record<string, number> = {
        '김태섭(A)': 4, '유반석(B)': 3, '전영배(E)': 0, '주원희(E)': 0, '강봉선(S)': 8, '백숙호(D)': 1,
        '양하나(A)': 4, '유소라(A)': 4, '현정혜(B)': 3, '이청아(C)': 2, '정규임(D)': 1, '배진희(E)': 0, '정진선(S)': 5,
        '김창수(A)': 4, '최진용(A)': 4, '이정훈(B)': 3, '송온유(D)': 1, '정광종(A)': 4, '장상원(E)': 0,
        '김세라(A)': 4, '김기원(B)': 3, '조유정(D)': 1, '강민정(E)': 0, '박지윤(S)': 5, '신나리(S)': 5
      };

      const bp1Pen = PLAYER_PENALTY[b1];
      const bp2Pen = PLAYER_PENALTY[b2];
      const wp1Pen = PLAYER_PENALTY[w1];
      const wp2Pen = PLAYER_PENALTY[w2];

      if (bp1Pen !== undefined && bp2Pen !== undefined && wp1Pen !== undefined && wp2Pen !== undefined) {
        const bPenTotal = bp1Pen + bp2Pen;
        const wPenTotal = wp1Pen + wp2Pen;
        let finalBluePen = 0;
        let finalWhitePen = 0;
        if (bPenTotal > wPenTotal) finalBluePen = bPenTotal - wPenTotal;
        else if (wPenTotal > bPenTotal) finalWhitePen = wPenTotal - bPenTotal;

        const [actualType] = (m.match_type || 'MD:0:0').split(':');
        updateData.match_type = `${actualType}:${finalBluePen}:${finalWhitePen}`;
      }
    }
      
    setMatches(matches.map(m => m.id === id ? { ...m, ...updateData } : m));
    await supabase.from('matches').update(updateData).eq('id', id);
    setEditPlayerModal(null);
  }

  function openEditMatch(id: string, round: number, court: number, actualType: string, bluePen: string, whitePen: string) {
    setEditMatchModal({
      id,
      round: round || 1,
      court: court || 1,
      type: actualType || 'MD',
      bluePen: parseInt(bluePen) || 0,
      whitePen: parseInt(whitePen) || 0,
    });
  }

  async function saveMatchInfo() {
    if (!editMatchModal) return;
    const { id, round, court, type, bluePen, whitePen } = editMatchModal;
    const match_type = `${type}:${bluePen}:${whitePen}`;
    
    setMatches(matches.map(m => m.id === id ? { ...m, round_num: round, court_num: court, match_type } : m));
    await supabase.from('matches').update({ round_num: round, court_num: court, match_type }).eq('id', id);
    setEditMatchModal(null);
  }

  async function addMatch() {
    const round = parseInt(prompt("몇 라운드에 추가할까요?", "1") || "0");
    if (!round) return;
    const court = parseInt(prompt("코트 번호는요?", "1") || "1");
    
    await supabase.from('matches').insert({
      round_num: round,
      court_num: court,
      match_type: 'MD:0:0',
      blue_player1: '선수1',
      blue_player2: '선수2',
      white_player1: '선수3',
      white_player2: '선수4',
      blue_score: 0,
      white_score: 0,
      status: 'pending'
    });
    fetchMatches();
  }

  const deleteMatch = (id: string) => {
    setDeleteCode("");
    setDeleteConfirm({ type: 'match', id });
  };

  if (!authed) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950">
        <div className="bg-white dark:bg-gray-900 p-8 rounded-2xl shadow-xl w-full max-w-sm text-center border border-gray-200 dark:border-gray-800">
          <Trophy className="w-16 h-16 text-yellow-500 mx-auto mb-6" />
          <h1 className="text-2xl font-black mb-2">관리자 모드</h1>
          <p className="text-gray-500 mb-8 text-sm">경기 점수 조작 및 대진표 관리</p>
          <input 
            type="password" 
            value={pwd} 
            onChange={e => setPwd(e.target.value)} 
            className="w-full border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 p-4 rounded-xl mb-4 text-center font-bold tracking-widest outline-none focus:ring-2 focus:ring-yellow-500 text-black dark:text-white"
            placeholder="비밀번호 입력"
            onKeyDown={e => { if(e.key === 'Enter' && pwd === '0070') setAuthed(true); }}
          />
          <button 
            onClick={() => { if(pwd === '0070') setAuthed(true); else alert('비밀번호가 틀렸습니다!'); }}
            className="w-full bg-black dark:bg-yellow-600 text-white font-bold px-6 py-4 rounded-xl hover:opacity-80 transition"
          >
            입장하기
          </button>
        </div>
      </div>
    );
  }


  
  const endTournament = async () => {
    if(!selectedTournamentId) return;
    if(confirm('정말로 이 대회를 최종 종료하시겠습니까? 종료 후에는 기록 보관소로 이동합니다.')) {
      await supabase.from('tournaments').update({ status: 'COMPLETED' }).eq('id', selectedTournamentId);
      setTournaments(tournaments.map(t => t.id === selectedTournamentId ? { ...t, status: 'COMPLETED' } : t));
      alert('대회가 종료되었습니다.');
    }
  };

  const currentMatches = matches.filter(m => m.tournament_id === selectedTournamentId);
  const activeTournament = tournaments.find(t => t.id === selectedTournamentId);

  // We need to override the matches logic for stats to only use currentMatches
  const playerStats: Record<string, number> = {};
  currentMatches.forEach(m => {
    [m.blue_player1, m.blue_player2, m.white_player1, m.white_player2].forEach(p => {
      if(p) playerStats[p] = (playerStats[p] || 0) + 1;
    });
  });

  const blueTeamStats = Object.entries(playerStats)
    .filter(([name]) => currentMatches.some(m => m.blue_player1 === name || m.blue_player2 === name))
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
    
  const whiteTeamStats = Object.entries(playerStats)
    .filter(([name]) => currentMatches.some(m => m.white_player1 === name || m.white_player2 === name))
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));

  const roundNums = Array.from(new Set(currentMatches.map(m => m.round_num))).sort((a, b) => a - b);


  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex flex-col md:flex-row">
      {/* Sidebar */}
      <aside className="w-full md:w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col shrink-0">
        <div className="p-4 border-b border-gray-200 dark:border-gray-800">
          <h1 className="text-xl font-black flex items-center gap-2 mb-4">
            <Settings className="text-gray-400" />
            관리자 메뉴
          </h1>
          <button onClick={handleAddNewTournament} className="w-full bg-blue-600 text-white px-4 py-3 rounded-xl font-bold text-sm flex justify-center items-center gap-2 hover:bg-blue-700 shadow-sm transition-colors">
            <RefreshCw className="w-4 h-4" /> 새 대회 추가
          </button>
        </div>
        
        <div className="p-4 border-b border-gray-200 dark:border-gray-800 pt-0">
          <button onClick={() => setIsPlayerManageModalOpen(true)} className="w-full bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 px-4 py-3 rounded-xl font-bold text-sm flex justify-center items-center gap-2 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
            <UsersIcon className="w-4 h-4" /> 회원 명단 관리
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          <h2 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 ml-1">누적 대회 목록</h2>
          {tournaments.map(t => (
            <button 
              key={t.id}
              onClick={() => setSelectedTournamentId(t.id)}
              className={`w-full text-left p-3 rounded-xl transition-colors flex flex-col gap-1 ${selectedTournamentId === t.id ? 'bg-yellow-50 dark:bg-yellow-900/30 border border-yellow-200 dark:border-yellow-700/50' : 'hover:bg-gray-50 dark:hover:bg-gray-800 border border-transparent'}`}
            >
              <div className="flex flex-col gap-1 w-full">
                <div className="flex items-center justify-between w-full">
                  {editingTournamentId === t.id ? (
                    <input 
                      type="text" 
                      value={editingTournamentName}
                      onChange={e => setEditingTournamentName(e.target.value)}
                      onKeyDown={e => e.key === 'Enter' && saveTournamentData(t.id)}
                      autoFocus
                      className="flex-1 text-sm font-bold border border-blue-400 rounded px-1 py-0.5 w-full bg-white dark:bg-gray-800 text-black dark:text-white mb-1"
                      onClick={(e) => e.stopPropagation()}
                    />
                  ) : (
                    <span className={`font-bold text-sm flex-1 ${selectedTournamentId === t.id ? 'text-yellow-700 dark:text-yellow-400' : 'text-gray-700 dark:text-gray-300'}`}>{t.title}</span>
                  )}
                  <div className="flex items-center gap-2 shrink-0">
                    {editingTournamentId === t.id ? (
                      <button onClick={(e) => { e.stopPropagation(); saveTournamentData(t.id); }} className="p-1 bg-blue-100 text-blue-600 rounded">
                        <Check className="w-3 h-3" />
                      </button>
                    ) : (
                      <button 
                        onClick={(e) => { e.stopPropagation(); setEditingTournamentId(t.id); setEditingTournamentName(t.title); setEditingTournamentDate(new Date(t.created_at).toISOString().split('T')[0]); }} 
                        className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded text-gray-400 hover:text-gray-600"
                      >
                        <Edit2 className="w-3 h-3" />
                      </button>
                    )}
                    <div className={`w-2 h-2 rounded-full ${t.status === 'IN_PROGRESS' ? 'bg-green-500' : 'bg-gray-300'}`} />
                    {editingTournamentId !== t.id && (
                      <button 
                        onClick={(e) => { e.stopPropagation(); deleteTournament(t.id); }} 
                        className="p-1 hover:bg-red-100 dark:hover:bg-red-900/30 rounded text-red-400 hover:text-red-600 transition-colors"
                      >
                        <Trash2 className="w-3 h-3" />
                      </button>
                    )}
                  </div>
                </div>
                {editingTournamentId === t.id ? (
                  <input
                    type="date"
                    value={editingTournamentDate}
                    onChange={e => setEditingTournamentDate(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && saveTournamentData(t.id)}
                    className="text-[10px] border border-blue-400 rounded px-1 py-0.5 w-max bg-white dark:bg-gray-800 text-black dark:text-white"
                    onClick={(e) => e.stopPropagation()}
                  />
                ) : (
                  <span className="text-[10px] text-gray-400">{new Date(t.created_at).toLocaleDateString()}</span>
                )}
              </div>
            </button>
          ))}
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto h-screen pb-20">

            {editMatchModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4">
          <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-xl w-full max-w-sm p-6 border border-gray-200 dark:border-gray-800">
            <h2 className="text-xl font-bold mb-6 text-gray-800 dark:text-gray-200">경기 정보 수정</h2>
            
            <div className="space-y-4 mb-8">
              <div className="flex gap-4">
                <div className="flex-1">
                  <label className="block text-sm font-bold mb-2 text-gray-700 dark:text-gray-300">라운드</label>
                  <div className="relative">
                    <select 
                      value={editMatchModal.round} 
                      onChange={e => setEditMatchModal({...editMatchModal, round: parseInt(e.target.value)})} 
                      className="w-full appearance-none border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-xl px-4 py-3 outline-none text-gray-900 dark:text-white focus:ring-2 focus:ring-yellow-500 transition-all font-medium cursor-pointer shadow-sm"
                    >
                      {[...Array(15)].map((_, i) => <option key={i+1} value={i+1}>{i+1} 라운드</option>)}
                    </select>
                    <ChevronDown className="absolute right-3 top-3.5 w-5 h-5 text-gray-400 pointer-events-none" />
                  </div>
                </div>
                
                <div className="flex-1">
                  <label className="block text-sm font-bold mb-2 text-gray-700 dark:text-gray-300">코트 번호</label>
                  <div className="relative">
                    <select 
                      value={editMatchModal.court} 
                      onChange={e => setEditMatchModal({...editMatchModal, court: parseInt(e.target.value)})} 
                      className="w-full appearance-none border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-xl px-4 py-3 outline-none text-gray-900 dark:text-white focus:ring-2 focus:ring-yellow-500 transition-all font-medium cursor-pointer shadow-sm"
                    >
                      {[...Array(10)].map((_, i) => <option key={i+1} value={i+1}>{i+1} 코트</option>)}
                    </select>
                    <ChevronDown className="absolute right-3 top-3.5 w-5 h-5 text-gray-400 pointer-events-none" />
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-sm font-bold mb-2 text-gray-700 dark:text-gray-300">종목</label>
                <div className="relative">
                  <select 
                    value={editMatchModal.type} 
                    onChange={e => setEditMatchModal({...editMatchModal, type: e.target.value})} 
                    className="w-full appearance-none border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-xl px-4 py-3 outline-none text-gray-900 dark:text-white focus:ring-2 focus:ring-yellow-500 transition-all font-medium cursor-pointer shadow-sm"
                  >
                    <option value="MD">남자 복식 (남복)</option>
                    <option value="WD">여자 복식 (여복)</option>
                    <option value="XD">혼합 복식 (혼복)</option>
                  </select>
                  <ChevronDown className="absolute right-3 top-3.5 w-5 h-5 text-gray-400 pointer-events-none" />
                </div>
              </div>

              <div className="flex gap-4">
                <div className="flex-1">
                  <label className="block text-sm font-bold mb-2 text-blue-600 dark:text-blue-400">청팀 패널티</label>
                  <div className="relative">
                    <select 
                      value={editMatchModal.bluePen} 
                      onChange={e => setEditMatchModal({...editMatchModal, bluePen: parseInt(e.target.value)})} 
                      className="w-full appearance-none border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-xl px-4 py-3 outline-none text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 transition-all font-medium cursor-pointer shadow-sm"
                    >
                      {[...Array(21)].map((_, i) => <option key={i} value={i}>{i}</option>)}
                    </select>
                    <ChevronDown className="absolute right-3 top-3.5 w-5 h-5 text-gray-400 pointer-events-none" />
                  </div>
                </div>
                
                <div className="flex-1">
                  <label className="block text-sm font-bold mb-2 text-gray-600 dark:text-gray-400">백팀 패널티</label>
                  <div className="relative">
                    <select 
                      value={editMatchModal.whitePen} 
                      onChange={e => setEditMatchModal({...editMatchModal, whitePen: parseInt(e.target.value)})} 
                      className="w-full appearance-none border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-xl px-4 py-3 outline-none text-gray-900 dark:text-white focus:ring-2 focus:ring-gray-500 transition-all font-medium cursor-pointer shadow-sm"
                    >
                      {[...Array(21)].map((_, i) => <option key={i} value={i}>{i}</option>)}
                    </select>
                    <ChevronDown className="absolute right-3 top-3.5 w-5 h-5 text-gray-400 pointer-events-none" />
                  </div>
                </div>
              </div>
            </div>

            <div className="flex flex-col gap-3">
              <div className="flex gap-3">
                <button 
                  onClick={() => setEditMatchModal(null)} 
                  className="flex-1 bg-gray-200 dark:bg-gray-800 text-gray-800 dark:text-gray-200 py-3.5 rounded-xl font-bold"
                >
                  취소
                </button>
                <button 
                  onClick={saveMatchInfo} 
                  className="flex-1 bg-yellow-500 text-white py-3.5 rounded-xl font-bold"
                >
                  저장
                </button>
              </div>
              <button 
                onClick={() => deleteMatch(editMatchModal.id)} 
                className="w-full bg-red-50 text-red-600 dark:bg-red-900/20 dark:text-red-400 py-3 rounded-xl font-bold text-sm hover:bg-red-100 dark:hover:bg-red-900/40 transition-colors flex items-center justify-center gap-2"
              >
                <Trash2 className="w-4 h-4" /> 이 경기 완전 삭제
              </button>
            </div>
          </div>
        </div>
      )}

      {editPlayerModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4">
          <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-xl w-full max-w-sm p-6 border border-gray-200 dark:border-gray-800">
            <h2 className="text-xl font-bold mb-4">{editPlayerModal.team === 'blue' ? '청팀' : '백팀'} 선수 교체</h2>
            
            <div className="space-y-6 mb-8">
              <div>
                <label className="block text-sm font-bold mb-2 text-gray-800 dark:text-gray-200">첫 번째 선수</label>
                <div className="relative">
                  <select 
                    value={p1Select} 
                    onChange={e => {
                      setP1Select(e.target.value);
                      if(e.target.value !== '직접입력') setP1Input('');
                    }} 
                    className="w-full appearance-none border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-xl px-4 py-3.5 outline-none mb-2 text-gray-900 dark:text-white focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-all font-medium cursor-pointer shadow-sm"
                  >
                    <option value="">-- 선택 --</option>
                    {(editPlayerModal.team === 'blue' ? blueTeamStats : whiteTeamStats).map(([name]) => (
                      <option key={name} value={name}>{name}</option>
                    ))}
                    <option value="직접입력">+ 새 선수/게스트 직접입력</option>
                  </select>
                  <ChevronDown className="absolute right-4 top-4 w-5 h-5 text-gray-400 pointer-events-none" />
                </div>
                {p1Select === '직접입력' && (
                  <input 
                    type="text" 
                    placeholder="선수 이름 입력"
                    value={p1Input}
                    onChange={e => setP1Input(e.target.value)}
                    className="w-full border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 rounded-xl px-4 py-3.5 outline-none text-gray-900 dark:text-white focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-all shadow-sm"
                    autoFocus
                  />
                )}
              </div>

              <div>
                <label className="block text-sm font-bold mb-2 text-gray-800 dark:text-gray-200">두 번째 선수</label>
                <div className="relative">
                  <select 
                    value={p2Select} 
                    onChange={e => {
                      setP2Select(e.target.value);
                      if(e.target.value !== '직접입력') setP2Input('');
                    }} 
                    className="w-full appearance-none border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-xl px-4 py-3.5 outline-none mb-2 text-gray-900 dark:text-white focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-all font-medium cursor-pointer shadow-sm"
                  >
                    <option value="">-- 선택 --</option>
                    {(editPlayerModal.team === 'blue' ? blueTeamStats : whiteTeamStats).map(([name]) => (
                      <option key={name} value={name}>{name}</option>
                    ))}
                    <option value="직접입력">+ 새 선수/게스트 직접입력</option>
                  </select>
                  <ChevronDown className="absolute right-4 top-4 w-5 h-5 text-gray-400 pointer-events-none" />
                </div>
                {p2Select === '직접입력' && (
                  <input 
                    type="text" 
                    placeholder="선수 이름 입력"
                    value={p2Input}
                    onChange={e => setP2Input(e.target.value)}
                    className="w-full border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 rounded-xl px-4 py-3.5 outline-none text-gray-900 dark:text-white focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-all shadow-sm"
                  />
                )}
              </div>
            </div>

            <div className="flex gap-3">
              <button 
                onClick={() => setEditPlayerModal(null)} 
                className="flex-1 bg-gray-200 dark:bg-gray-800 text-gray-800 dark:text-gray-200 py-3 rounded-xl font-bold"
              >
                취소
              </button>
              <button 
                onClick={savePlayers} 
                className="flex-1 bg-yellow-500 text-white py-3 rounded-xl font-bold"
              >
                저장
              </button>
            </div>
          </div>
        </div>
      )}


        {!selectedTournamentId ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-400 dark:text-gray-600 bg-gray-50/50 dark:bg-gray-950/50 py-32">
            <Trophy className="w-16 h-16 mb-4 opacity-20" />
            <p className="font-bold text-lg text-gray-500">왼쪽 목록에서 대회를 선택해주세요.</p>
            <p className="text-sm mt-2">새로운 월례회를 시작하려면 좌측의 [새 대회 추가]를 눌러주세요.</p>
          </div>
        ) : (
          <>
      {/* 상단 헤더 */}
      <div className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-10 shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          
          <h1 className="text-xl md:text-2xl font-black flex items-center gap-2">
            <Settings className="text-gray-400" />
            점수 관리 보드
          </h1>
          <div className="flex gap-2">
            <button onClick={() => { setGeneratedBracket([]); setIsGeneratorModalOpen(true); }} className="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold text-sm flex items-center gap-1 hover:bg-blue-700 shadow-sm">
              <RefreshCw className="w-4 h-4" /> 새 대진표 자동생성
            </button>
            <button onClick={addMatch} className="bg-gray-900 dark:bg-gray-100 text-white dark:text-black px-4 py-2 rounded-lg font-bold text-sm flex items-center gap-1 hover:opacity-80">
              <Plus className="w-4 h-4" /> 빈 경기 추가
            </button>
          </div>

        </div>
      </div>


      {/* 통계 패널 */}
      <div className="container mx-auto px-4 pt-8">
        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
          <h2 className="text-lg font-bold mb-6 flex items-center gap-2 border-b border-gray-100 dark:border-gray-800 pb-4">
            <Users className="text-yellow-600 w-5 h-5" />팀 구성 및 선수별 배정 경기 수
          </h2>
          <div className="flex flex-col md:flex-row gap-8">
            <div className="flex-1">
              <h3 className="text-sm font-bold text-blue-600 dark:text-blue-400 mb-3 flex items-center gap-1">
                청팀 <span className="bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 text-xs px-2 py-0.5 rounded-full">{blueTeamStats.length}명</span>
              </h3>
              <div className="flex flex-wrap gap-2">
                {blueTeamStats.map(([name, count]) => (
                  <span key={name} className="bg-blue-50 border border-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm dark:bg-blue-900/30 dark:border-blue-800 dark:text-blue-300">
                    {name} <span className="font-bold opacity-70">({count})</span>
                  </span>
                ))}
              </div>
            </div>
            <div className="hidden md:block w-px bg-gray-200 dark:bg-gray-800"></div>
            <div className="flex-1">
              <h3 className="text-sm font-bold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-1">
                백팀 <span className="bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300 text-xs px-2 py-0.5 rounded-full">{whiteTeamStats.length}명</span>
              </h3>
              <div className="flex flex-wrap gap-2">
                {whiteTeamStats.map(([name, count]) => (
                  <span key={name} className="bg-gray-100 border border-gray-200 text-gray-800 px-3 py-1 rounded-full text-sm dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300">
                    {name} <span className="font-bold opacity-70">({count})</span>
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="mt-6 pt-6 border-t border-gray-100 dark:border-gray-800">
            <h3 className="text-sm font-bold text-gray-800 dark:text-gray-200 mb-3 flex items-center justify-center gap-1">
              <Trophy className="w-4 h-4 text-yellow-500" />
              종목별 경기 통계
            </h3>
            <div className="flex gap-2 text-center text-sm font-bold">
              <div className="flex-1 bg-blue-50 border border-blue-100 text-blue-700 dark:bg-blue-900/20 dark:border-blue-800/50 dark:text-blue-300 py-2 rounded-xl">
                남복 <span className="text-lg font-black ml-1">{currentMatches.filter(m => (m.match_type || '').startsWith('MD')).length}</span>
              </div>
              <div className="flex-1 bg-pink-50 border border-pink-100 text-pink-700 dark:bg-pink-900/20 dark:border-pink-800/50 dark:text-pink-300 py-2 rounded-xl">
                여복 <span className="text-lg font-black ml-1">{currentMatches.filter(m => (m.match_type || '').startsWith('WD')).length}</span>
              </div>
              <div className="flex-1 bg-purple-50 border border-purple-100 text-purple-700 dark:bg-purple-900/20 dark:border-purple-800/50 dark:text-purple-300 py-2 rounded-xl">
                혼복 <span className="text-lg font-black ml-1">{currentMatches.filter(m => (m.match_type || '').startsWith('XD')).length}</span>
              </div>
              <div className="flex-1 bg-gray-100 border border-gray-200 text-gray-800 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-200 py-2 rounded-xl">
                총 <span className="text-lg font-black ml-1">{currentMatches.length}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8 space-y-12">
        {roundNums.map(roundNum => {
          const roundMatches = currentMatches.filter(m => m.round_num === roundNum);
          return (
            <div key={roundNum} className="space-y-4">
              <h2 className="text-2xl font-black flex items-center gap-2 text-gray-800 dark:text-gray-200">
                <span className="bg-yellow-500 text-white px-3 py-1 rounded-lg text-lg">{roundNum}R</span>
              </h2>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 md:gap-4">
                {roundMatches.map(m => {
                  const [actualType, bluePen, whitePen] = (m.match_type || '').split(':');
                  const tName = actualType === 'MD' ? '남복' : actualType === 'WD' ? '여복' : actualType === 'XD' ? '혼복' : actualType;
                  return (
                  <div key={m.id} className={`flex flex-col bg-white dark:bg-gray-900 rounded-lg shadow-sm border overflow-hidden ${m.status === 'completed' ? 'border-gray-200 opacity-70' : 'border-blue-200 dark:border-blue-900/50'}`}>
                    {/* 코트 번호 헤더 */}
                    <div className="bg-gray-100 dark:bg-gray-800 p-2 flex justify-between items-center border-b border-gray-200 dark:border-gray-700 whitespace-nowrap">
                      <div 
                        className="font-bold text-gray-800 dark:text-gray-200 text-[11px] cursor-pointer"
                        onClick={() => openEditMatch(m.id, m.round_num, m.court_num, actualType, bluePen, whitePen)}
                      >
                        {m.court_num}코트 <span className="text-gray-500 font-normal">({tName})</span>
                      </div>
                      <button onClick={() => deleteMatch(m.id)} className="text-gray-400 hover:text-red-500 p-1 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-all ml-1 shrink-0" title="경기 삭제">
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                    
                    {/* 청팀 */}
                    <div className={`p-2 md:p-3 flex justify-between items-center border-b border-gray-100 dark:border-gray-800 flex-1 ${m.status === 'completed' && m.blue_score > m.white_score ? 'bg-blue-50 dark:bg-blue-900/30' : ''}`}>
                      <div 
                        className="font-black text-sm sm:text-base md:text-lg text-blue-700 dark:text-blue-400 cursor-pointer w-full flex flex-col justify-center min-w-0 pr-2"
                        onClick={() => editPlayers(m.id, 'blue', m.blue_player1, m.blue_player2)}
                      >
                        <div className="truncate w-full">{m.blue_player1}</div>
                        <div className="truncate w-full">{m.blue_player2}</div>
                        {bluePen && bluePen !== '0' && <div className="text-[10px] md:text-xs font-bold text-red-500 mt-0.5">패널티 {bluePen}</div>}
                      </div>
                      <button 
                        onClick={() => setWinner(m.id, 'blue')} 
                        className={`w-9 h-9 md:w-11 md:h-11 flex justify-center items-center rounded-full border shrink-0 shadow-sm transition-all ${
                          m.status === 'completed' && m.blue_score > m.white_score 
                            ? 'bg-blue-600 border-blue-600 text-white' 
                            : 'bg-white border-blue-200 text-blue-500 hover:bg-blue-50 dark:bg-gray-800'
                        }`}
                      >
                        <span className="text-xs md:text-sm font-black leading-none">{m.status === 'completed' && m.blue_score > m.white_score ? 'WIN' : '승'}</span>
                      </button>
                    </div>

                    {/* 백팀 */}
                    <div className={`p-1.5 flex justify-between items-center flex-1 ${m.status === 'completed' && m.white_score > m.blue_score ? 'bg-gray-100 dark:bg-gray-800' : ''}`}>
                      <div 
                        className="font-bold text-[12px] text-gray-800 dark:text-gray-200 cursor-pointer w-full"
                        onClick={() => editPlayers(m.id, 'white', m.white_player1, m.white_player2)}
                      >
                        <div className="truncate w-full">{m.white_player1}</div>
                        <div className="truncate w-full">{m.white_player2}</div>
                        {whitePen && whitePen !== '0' && <div className="text-[9px] text-red-500">패널티 {whitePen}</div>}
                      </div>
                      <button 
                        onClick={() => setWinner(m.id, 'white')} 
                        className={`w-7 h-7 flex justify-center items-center rounded-full border shrink-0 ml-1 shadow-sm ${
                          m.status === 'completed' && m.white_score > m.blue_score 
                            ? 'bg-gray-800 border-gray-800 text-white dark:bg-gray-200 dark:text-black' 
                            : 'bg-white border-gray-200 text-gray-500 dark:bg-gray-800'
                        }`}
                      >
                        <span className="text-[10px] font-black leading-none">{m.status === 'completed' && m.white_score > m.blue_score ? 'WIN' : '승'}</span>
                      </button>
                    </div>

                    {/* 하단 제어 영역 (재개/종료) */}
                    <button 
                      onClick={async () => {
                        const newStatus = m.status === 'completed' ? 'pending' : 'completed';
                        setMatches(matches.map(match => match.id === m.id ? { ...match, status: newStatus } : match));
                        await supabase.from('matches').update({ status: newStatus }).eq('id', m.id);
                      }}
                      className={`w-full text-center py-2 text-[10px] font-bold transition-all border-t border-gray-200 dark:border-gray-700 ${
                        m.status === 'completed' 
                          ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-400 hover:bg-amber-200' 
                          : 'bg-gray-100 text-gray-600 dark:bg-gray-800/80 dark:text-gray-400 hover:bg-gray-200'
                      }`}
                    >
                      {m.status === 'completed' ? '↺ 경기 재개' : '■ 경기 종료'}
                    </button>
                  </div>
                )})}
              </div>
            </div>
          );
        })}
      </div>
    
          </>
        )}

      {/* --- 대진표 자동 생성 모달 --- */}
      {isGeneratorModalOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white dark:bg-gray-900 rounded-3xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col shadow-2xl">
            <div className="p-6 border-b border-gray-100 dark:border-gray-800 flex items-center justify-between">
              <h2 className="text-xl font-bold flex items-center gap-2">
                <RefreshCw className="text-blue-600" /> 대진표 자동 생성기
              </h2>
              <button onClick={() => setIsGeneratorModalOpen(false)} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 flex-1 overflow-y-auto flex flex-col md:flex-row gap-8 bg-gray-50 dark:bg-gray-950">
              <div className="w-full md:w-1/3 flex flex-col gap-3 h-full max-h-[70vh]">
                <div className="flex justify-between items-center">
                  <h3 className="font-bold text-gray-800 dark:text-gray-200">참가자 선택</h3>
                  <div className="flex gap-2">
                    <span className="text-sm text-blue-600 font-bold bg-blue-50 px-2 py-1 rounded-md">{selectedPlayerIds.size}명 선택됨</span>
                  </div>
                </div>
                <div className="flex justify-between gap-1 shrink-0">
                  <button onClick={() => setSelectedPlayerIds(new Set(dbPlayers.map(p => p.id)))} className="flex-1 text-xs bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 px-2 py-1.5 rounded flex items-center justify-center gap-1 font-bold">
                    <CheckSquare className="w-3 h-3" /> 전체선택
                  </button>
                  <button onClick={() => setSelectedPlayerIds(new Set())} className="flex-1 text-xs bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 px-2 py-1.5 rounded flex items-center justify-center gap-1 font-bold">
                    <Square className="w-3 h-3" /> 전체해제
                  </button>
                  <button onClick={openGuestModal} className="flex-1 text-xs bg-blue-100 text-blue-700 hover:bg-blue-200 px-2 py-1.5 rounded flex items-center justify-center gap-1 font-bold">
                    <UserPlus className="w-3 h-3" /> 게스트/추가
                  </button>
                </div>
                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-3 flex-1 overflow-y-auto space-y-2 min-h-0">
                  {dbPlayers.map(p => (
                    <label key={p.id} className="flex items-center gap-3 p-2 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg cursor-pointer">
                      <input 
                        type="checkbox" 
                        className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500 border-gray-300"
                        checked={selectedPlayerIds.has(p.id)}
                        onChange={(e) => {
                          const next = new Set(selectedPlayerIds);
                          if (e.target.checked) next.add(p.id);
                          else next.delete(p.id);
                          setSelectedPlayerIds(next);
                        }}
                      />
                      <span className="font-medium text-sm text-gray-800 dark:text-gray-200">{p.name}</span>
                      <span className="text-xs font-bold text-gray-500 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded-md">{p.grade}급</span>
                    </label>
                  ))}
                </div>
                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-3 shrink-0">
                  <label className="text-xs text-gray-500 font-bold mb-1 block">경기 방식</label>
                  <select 
                    value={matchType} 
                    onChange={e => setMatchType(e.target.value as 'TEAM' | 'INDIVIDUAL')}
                    className="w-full bg-transparent font-bold outline-none cursor-pointer"
                  >
                    <option value="TEAM">청백전 (팀전)</option>
                    <option value="INDIVIDUAL">개인전 (랜덤 매치)</option>
                  </select>
                </div>
                <div className="flex gap-2 shrink-0">
                  <div className="flex-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-2 flex flex-col justify-center">
                    <label className="text-xs text-gray-500 font-bold mb-1">코트 수</label>
                    <div className="flex items-center gap-2">
                      <input type="number" min="1" max="10" value={numCourts} onChange={e => setNumCourts(parseInt(e.target.value) || 1)} className="w-full bg-transparent font-bold outline-none" />
                      <span className="text-sm text-gray-400">면</span>
                    </div>
                  </div>
                  <div className="flex-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-2 flex flex-col justify-center">
                    <label className="text-xs text-gray-500 font-bold mb-1">총 라운드</label>
                    <div className="flex items-center gap-2">
                      <input type="number" min="1" max="20" value={numRounds} onChange={e => setNumRounds(parseInt(e.target.value) || 1)} className="w-full bg-transparent font-bold outline-none" />
                      <span className="text-sm text-gray-400">R</span>
                    </div>
                  </div>
                </div>

                <div className="flex flex-col gap-2 shrink-0 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-3">
                  <label className="flex items-center gap-2 text-xs font-bold text-gray-700 dark:text-gray-300 cursor-pointer">
                    <input type="checkbox" checked={ignoreGrade} onChange={e => setIgnoreGrade(e.target.checked)} className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500" />
                    급수 무관 (랜덤 편성)
                  </label>
                  <label className="flex items-center gap-2 text-xs font-bold text-gray-700 dark:text-gray-300 cursor-pointer">
                    <input type="checkbox" checked={hideGrade} onChange={e => setHideGrade(e.target.checked)} className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500" />
                    대진표 급수 숨기기
                  </label>
                </div>
                <button 
                  onClick={handleGenerate}
                  disabled={isGenerating || selectedPlayerIds.size < 4}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50 transition-all shadow-md shrink-0"
                >
                  <RefreshCw className={`w-5 h-5 ${isGenerating ? 'animate-spin' : ''}`} />
                  알고리즘으로 대진표 짜기
                </button>
              </div>

              <div className="w-full md:w-2/3">
                <h3 className="font-bold mb-4 text-gray-800 dark:text-gray-200">대진표 미리보기 <span className="text-sm font-normal text-gray-500 ml-2">(이름을 클릭하여 수동 교체)</span></h3>
                {generatedBracket.length === 0 ? (
                  <div className="h-64 flex flex-col items-center justify-center text-gray-400 border-2 border-dashed border-gray-200 dark:border-gray-800 rounded-2xl bg-white dark:bg-gray-900">
                    <Trophy className="w-12 h-12 mb-3 opacity-30 text-blue-500" />
                    <p className="font-medium">좌측에서 생성 버튼을 눌러주세요</p>
                  </div>
                ) : (
                  <div className="space-y-3 max-h-[50vh] overflow-y-auto pr-2">
                    {generatedBracket.map((m, idx) => (
                      <div key={idx} className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-4 flex shadow-sm hover:border-blue-300 transition-colors">
                        <div className="flex-1 flex flex-col justify-center gap-2 border-r border-gray-100 dark:border-gray-800 pr-4">
                          <span className="text-xs font-black text-gray-500 mb-1">{m.round_num}R - {m.court_num}코트</span>
                          <span className={`text-xs font-black px-2 py-1 rounded w-max ${matchType === 'TEAM' ? 'text-blue-600 bg-blue-50' : 'text-gray-600 bg-gray-100 dark:bg-gray-800'}`}>{matchType === 'TEAM' ? '청팀' : 'A조'}</span>
                          <div className="flex gap-2">
                            <button onClick={() => handleSwapGenerated(idx, 'blue', 0)} className="text-sm md:text-base bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-blue-200 transition-all min-w-0">{m.blue_team[0].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.blue_team[0].grade}</span>}</button>
                            <button onClick={() => handleSwapGenerated(idx, 'blue', 1)} className="text-sm md:text-base bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-blue-200 transition-all min-w-0">{m.blue_team[1].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.blue_team[1].grade}</span>}</button>
                          </div>
                        </div>
                        <div className="px-5 flex items-center justify-center font-black text-gray-300 italic text-lg">VS</div>
                        <div className="flex-1 flex flex-col justify-center gap-2 pl-4">
                          <span className="text-xs font-black text-gray-600 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded w-max">{matchType === 'TEAM' ? '백팀' : 'B조'}</span>
                          <div className="flex gap-2">
                            <button onClick={() => handleSwapGenerated(idx, 'white', 0)} className="text-sm md:text-base bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-gray-300 transition-all min-w-0">{m.white_team[0].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.white_team[0].grade}</span>}</button>
                            <button onClick={() => handleSwapGenerated(idx, 'white', 1)} className="text-sm md:text-base bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 p-2 rounded-lg font-bold w-full text-left truncate border border-transparent hover:border-gray-300 transition-all min-w-0">{m.white_team[1].name} {!hideGrade && <span className="text-xs font-normal text-gray-400 ml-1">{m.white_team[1].grade}</span>}</button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            <div className="p-5 border-t border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-900 flex justify-end gap-3">
              <button onClick={() => setIsGeneratorModalOpen(false)} className="px-6 py-3 font-bold text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-xl transition-colors">취소</button>
              <button 
                onClick={saveTournament}
                disabled={generatedBracket.length === 0}
                className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl flex items-center gap-2 disabled:opacity-50 transition-all shadow-md"
              >
                <Save className="w-5 h-5" />
                이 대진표로 실제 경기 생성하기
              </button>
            </div>
          </div>
        </div>
      )}


      {/* --- 회원 명단 관리 모달 --- */}
      {isPlayerManageModalOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white dark:bg-gray-900 rounded-3xl w-full max-w-xl max-h-[80vh] overflow-hidden flex flex-col shadow-2xl">
            <div className="p-6 border-b border-gray-100 dark:border-gray-800 flex items-center justify-between">
              <h2 className="text-xl font-bold flex items-center gap-2">
                <UsersIcon className="text-blue-600" /> 회원 명단 및 급수 관리
              </h2>
              <button onClick={() => setIsPlayerManageModalOpen(false)} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full">
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="p-6 flex-1 overflow-y-auto space-y-3 bg-gray-50 dark:bg-gray-950">
              <div className="flex justify-between items-center mb-4">
                <h3 className="font-bold">총 {dbPlayers.length}명</h3>
                <button onClick={openGuestModal} className="bg-blue-600 text-white text-sm px-3 py-1.5 rounded-lg font-bold flex items-center gap-1 hover:bg-blue-700">
                  <UserPlus className="w-4 h-4" /> 새 회원 등록
                </button>
              </div>

              {dbPlayers.map(p => (
                <div key={p.id} className="flex items-center justify-between bg-white dark:bg-gray-900 p-3 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800">
                  <span className="font-bold">{p.name}</span>
                  <div className="flex items-center gap-3">
                    <span className="text-xs text-gray-400">급수 변경:</span>
                    <select 
                      value={p.grade}
                      onChange={(e) => updatePlayerGrade(p.id, e.target.value)}
                      className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg px-2 py-1 font-bold outline-none cursor-pointer"
                    >
                      <option value="S">S급</option>
                      <option value="A">A급</option>
                      <option value="B">B급</option>
                      <option value="C">C급</option>
                      <option value="D">D급</option>
                      <option value="E">E급</option>
                    </select>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}


      {/* --- 게스트 추가 모달 --- */}
      {isGuestModalOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[60] flex items-center justify-center p-4">
          <div className="bg-white dark:bg-gray-900 rounded-3xl w-full max-w-sm p-6 shadow-2xl border border-gray-100 dark:border-gray-800">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold flex items-center gap-2 text-gray-800 dark:text-white">
                <UserPlus className="text-blue-600 w-6 h-6" /> 새 게스트 추가
              </h2>
              <button onClick={() => setIsGuestModalOpen(false)} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full">
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">이름</label>
                <input 
                  type="text" 
                  value={guestName} 
                  onChange={(e) => setGuestName(e.target.value)} 
                  placeholder="홍길동"
                  autoFocus
                  className="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all font-medium"
                  onKeyDown={(e) => e.key === 'Enter' && saveGuest()}
                />
              </div>
              <div className="relative">
                <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">급수</label>
                <select 
                  value={guestGrade} 
                  onChange={(e) => setGuestGrade(e.target.value)}
                  className="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all font-medium cursor-pointer appearance-none"
                >
                  <option value="S">S급</option>
                  <option value="A">A급</option>
                  <option value="B">B급</option>
                  <option value="C">C급</option>
                  <option value="D">D급</option>
                  <option value="E">E급 (초심)</option>
                </select>
                <ChevronDown className="absolute right-4 top-10 w-5 h-5 text-gray-400 pointer-events-none" />
              </div>
            </div>
            <button 
              onClick={saveGuest}
              disabled={!guestName.trim()}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50 transition-all shadow-md"
            >
              추가하기
            </button>
          </div>
        </div>
      )}

      {/* --- 안전 삭제 모달 --- */}
      {deleteConfirm && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[70] flex items-center justify-center p-4">
          <div className="bg-white dark:bg-gray-900 rounded-3xl w-full max-w-sm p-6 shadow-2xl border border-red-100 dark:border-red-900/30">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold flex items-center gap-2 text-red-600 dark:text-red-500">
                <Trash2 className="w-6 h-6" /> 영구 삭제 확인
              </h2>
              <button onClick={() => setDeleteConfirm(null)} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full">
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-6 font-medium leading-relaxed">
              {deleteConfirm.type === 'tournament' 
                ? '이 대회와 관련된 모든 경기 기록이 완전히 삭제되며 복구할 수 없습니다.' 
                : '선택하신 경기가 완전히 삭제되며 복구할 수 없습니다.'}
              <br /><br />
              정말로 삭제하시려면 아래에 <strong className="text-red-500">0000</strong> 을 입력해주세요.
            </p>

            <div className="space-y-4">
              <input 
                type="text" 
                value={deleteCode} 
                onChange={(e) => setDeleteCode(e.target.value)} 
                placeholder="0000"
                maxLength={4}
                autoFocus
                className="w-full bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-900/50 rounded-xl px-4 py-4 outline-none focus:border-red-500 focus:ring-2 focus:ring-red-200 transition-all font-black text-center text-2xl tracking-[0.5em] text-red-600 placeholder-red-300"
                onKeyDown={(e) => e.key === 'Enter' && executeDelete()}
              />
              <button 
                onClick={executeDelete}
                disabled={deleteCode !== '0000'}
                className="w-full bg-red-600 hover:bg-red-700 text-white py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50 transition-all shadow-md"
              >
                <Trash2 className="w-5 h-5" /> 완전히 삭제하기
              </button>
            </div>
          </div>
        </div>
      )}
      </main>
    </div>
  );
}
