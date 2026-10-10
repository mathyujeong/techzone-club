require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);

async function run() {
  const { data, error } = await supabase.from('players').select('name').order('name');
  console.log('Total players:', data.length);
  console.log(data.map(d => d.name));
}

run();
