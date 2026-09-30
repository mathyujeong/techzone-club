const { createClient } = require('@supabase/supabase-js');
const dotenv = require('dotenv');
dotenv.config({ path: './.env.local' });

const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY);

const grades = {
  '김태섭': 'A', '유반석': 'B', '전영배': 'E', '주원희': 'E', '강봉선': 'S', '백숙호': 'D',
  '양하나': 'A', '유소라': 'A', '현정혜': 'B', '이청아': 'C', '정규임': 'D', '배진희': 'E', '정진선': 'S',
  '김창수': 'A', '최진용': 'A', '이정훈': 'B', '송온유': 'D', '정광종': 'A', '장상원': 'E',
  '김세라': 'A', '김기원': 'B', '조유정': 'D', '강민정': 'E', '박지윤': 'S', '신나리': 'S'
};

function addGrade(name) {
  if (!name || name.includes('(')) return name;
  const g = grades[name];
  if (g) return `${name}(${g})`;
  return name;
}

async function run() {
  const { data: matches, error } = await supabase.from('matches').select('*');
  if (error) { console.error(error); return; }
  
  for (const m of matches) {
    const b1 = addGrade(m.blue_player1);
    const b2 = addGrade(m.blue_player2);
    const w1 = addGrade(m.white_player1);
    const w2 = addGrade(m.white_player2);
    
    if (b1 !== m.blue_player1 || b2 !== m.blue_player2 || w1 !== m.white_player1 || w2 !== m.white_player2) {
      await supabase.from('matches').update({
        blue_player1: b1,
        blue_player2: b2,
        white_player1: w1,
        white_player2: w2
      }).eq('id', m.id);
    }
  }
  console.log("Updated all names with grades!");
}

run();
