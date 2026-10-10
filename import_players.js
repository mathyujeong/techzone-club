require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);

const players = [
  {"Name":"강민정","Grade":"E"}, {"Name":"강봉선","Grade":"S"}, {"Name":"김기원","Grade":"B"},
  {"Name":"김세라","Grade":"A"}, {"Name":"김승현","Grade":"E"}, {"Name":"김여진","Grade":"A"},
  {"Name":"김진수","Grade":"D"}, {"Name":"김창수","Grade":"A"}, {"Name":"김태섭","Grade":"A"},
  {"Name":"박미자","Grade":"C"}, {"Name":"박수신","Grade":"E"}, {"Name":"박지윤","Grade":"S"},
  {"Name":"박진현","Grade":"A"}, {"Name":"배진희","Grade":"E"}, {"Name":"배형남","Grade":"E"},
  {"Name":"백숙호","Grade":"D"}, {"Name":"손병근","Grade":"E"}, {"Name":"송온유","Grade":"D"},
  {"Name":"송지은","Grade":"E"}, {"Name":"송환희","Grade":"D"}, {"Name":"신나리","Grade":"S"},
  {"Name":"양하나","Grade":"A"}, {"Name":"오성환","Grade":"E"}, {"Name":"유반석","Grade":"B"},
  {"Name":"유소라","Grade":"A"}, {"Name":"이정훈","Grade":"B"}, {"Name":"이청아","Grade":"C"},
  {"Name":"장상원","Grade":"E"}, {"Name":"장성학","Grade":"A"}, {"Name":"전영배","Grade":"E"},
  {"Name":"정광종","Grade":"A"}, {"Name":"정규임","Grade":"D"}, {"Name":"정진선","Grade":"S"},
  {"Name":"조아라","Grade":"D"}, {"Name":"조유정","Grade":"D"}, {"Name":"주원휘","Grade":"E"},
  {"Name":"최진용","Grade":"A"}, {"Name":"현정혜","Grade":"B"}, {"Name":"장기철","Grade":"E"}
];

async function run() {
  for (const p of players) {
    const { data, error } = await supabase.from('players').upsert(
      { name: p.Name, grade: p.Grade },
      { onConflict: 'name' }
    );
    if (error) {
      console.error('Error inserting', p.Name, error);
    }
  }
  console.log('Finished inserting 39 players.');
}

run();
