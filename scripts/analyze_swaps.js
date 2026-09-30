const { createClient } = require('@supabase/supabase-js');
const dotenv = require('dotenv');
dotenv.config({ path: './.env.local' });

const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY);

async function run() {
  const { data: matches, error } = await supabase.from('matches').select('*').order('round_num').order('court_num');
  if (error) { console.error(error); return; }

  matches.forEach(m => {
    console.log(`[R${m.round_num} C${m.court_num}] ${m.blue_player1}, ${m.blue_player2} VS ${m.white_player1}, ${m.white_player2} (${m.match_type})`);
  });
}

run();
