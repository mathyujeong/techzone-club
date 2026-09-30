import { createClient } from '@supabase/supabase-js';
import fs from 'fs';
import dotenv from 'dotenv';
dotenv.config({ path: '.env.local' });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseUrl.startsWith('http')) {
  console.error('❌ .env.local 파일에 NEXT_PUBLIC_SUPABASE_URL을 올바르게 입력해주세요!');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);
const rawData = fs.readFileSync('src/data/tournament.json', 'utf-8');
const schedule = JSON.parse(rawData);

async function upload() {
  console.log('🚀 Supabase로 대진표 데이터 업로드 시작...');
  
  // 기존 데이터 삭제 (RLS 에러 날 수 있으니 확인)
  const { error: delErr } = await supabase.from('matches').delete().neq('round_num', -1);
  if (delErr) console.warn('⚠️ 삭제 실패 (새로 추가됩니다):', delErr.message);
  
  const insertData = schedule.map(m => ({
    round_num: m.round,
    court_num: m.court,
    match_type: `${m.type}:${m.blue_score}:${m.white_score}`, // type:blue_penalty:white_penalty
    blue_player1: m.blue_team[0],
    blue_player2: m.blue_team[1],
    white_player1: m.white_team[0],
    white_player2: m.white_team[1],
    blue_score: 0,
    white_score: 0,
    status: 'pending'
  }));

  const { error } = await supabase.from('matches').insert(insertData);
  if (error) {
    console.error('❌ 업로드 실패:', error.message);
  } else {
    console.log('✅ 대진표 20경기 업로드 성공! 이제 실시간 점수판이 동작합니다.');
  }
}
upload();
