require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);

async function run() {
  await supabase.from('matches').update({ blue_player1: '주원휘' }).eq('blue_player1', '주원희');
  await supabase.from('matches').update({ blue_player2: '주원휘' }).eq('blue_player2', '주원희');
  await supabase.from('matches').update({ white_player1: '주원휘' }).eq('white_player1', '주원희');
  await supabase.from('matches').update({ white_player2: '주원휘' }).eq('white_player2', '주원희');
  console.log('Updated matches successfully.');
}

run();
