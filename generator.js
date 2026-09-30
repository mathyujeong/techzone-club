const { createClient } = require('@supabase/supabase-js');
const dotenv = require('dotenv');

dotenv.config({ path: './.env.local' });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

const blueMen = [
  { name: '김태섭', pen: 4, type: 'A' },
  { name: '유반석', pen: 3, type: 'B' },
  { name: '전영배', pen: 0, type: 'E' },
  { name: '주원희', pen: 0, type: 'E' },
  { name: '강봉선', pen: 8, type: 'S' },
  { name: '백숙호', pen: 1, type: 'D' },
];
const blueWomen = [
  { name: '양하나', pen: 4, type: 'A' },
  { name: '유소라', pen: 4, type: 'A' },
  { name: '현정혜', pen: 3, type: 'B' },
  { name: '이청아', pen: 2, type: 'C' },
  { name: '정규임', pen: 1, type: 'D' },
  { name: '배진희', pen: 0, type: 'E' },
  { name: '정진선', pen: 5, type: 'S' },
];
const whiteMen = [
  { name: '김창수', pen: 4, type: 'A' },
  { name: '최진용', pen: 4, type: 'A' },
  { name: '이정훈', pen: 3, type: 'B' },
  { name: '송온유', pen: 1, type: 'D' },
  { name: '정광종', pen: 4, type: 'A' },
  { name: '장상원', pen: 0, type: 'E' },
];
const whiteWomen = [
  { name: '김세라', pen: 4, type: 'A' },
  { name: '김기원', pen: 3, type: 'B' },
  { name: '조유정', pen: 1, type: 'D' },
  { name: '강민정', pen: 0, type: 'E' },
  { name: '박지윤', pen: 5, type: 'S' },
  { name: '신나리', pen: 5, type: 'S' },
];

function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function generateMatches() {
  const TOTAL_MATCHES = 24;
  let bestSchedule = null;
  let bestScore = -9999;
  
  for (let attempt = 0; attempt < 500000; attempt++) {
    const matchCounts = {};
    const allPlayers = [...blueMen, ...blueWomen, ...whiteMen, ...whiteWomen];
    allPlayers.forEach(p => matchCounts[p.name] = 0);
    
    let matches = [];
    
    // e.g., 9 MD, 9 WD, 6 XD = 24.
    // That means 36 M slots, 36 F slots for MD/WD + 12 M + 12 F for XD = 48 M slots, 48 F slots.
    // We have 13 Blue (6M, 7F), 12 White (6M, 6F).
    // Total Blue slots: 24 * 2 = 48 slots. 6M + 7F = 13 players.
    // For 48 slots, M avg = 48/2 = 24 slots. Wait.
    // MD uses 2M. WD uses 2F. XD uses 1M, 1F.
    // 9 MD -> 18 M from Blue? No, 9 MD means 2 M from Blue and 2 M from White per match. So 18 M from Blue.
    // Wait, 18 M slots for Blue. 6 XD -> 6 M slots for Blue. Total M slots = 24.
    // 24 M slots for Blue Men (6 players). 24 / 6 = 4 games exactly! Perfect.
    // 9 WD -> 18 F slots for Blue. 6 XD -> 6 F slots for Blue. Total F slots = 24.
    // 24 F slots for Blue Women (7 players). 24 / 7 = 3.42 games. So 4 players get 3 games, 3 players get 4 games. Perfect.
    // White Team: 6 Men, 6 Women. Total 12.
    // 24 M slots for White Men (6 players). 24 / 6 = 4 games exactly! Perfect.
    // 24 F slots for White Women (6 players). 24 / 6 = 4 games exactly! Perfect.
    // So everyone will play 3-4 games! Exactly as required.

    const targetMD = 9;
    const targetWD = 9;
    const targetXD = 6;
    
    let poolMD = [];
    let poolWD = [];
    let poolXD = [];
    
    for (let i = 0; i < targetMD; i++) poolMD.push('MD');
    for (let i = 0; i < targetWD; i++) poolWD.push('WD');
    for (let i = 0; i < targetXD; i++) poolXD.push('XD');
    
    let types = shuffle([...poolMD, ...poolWD, ...poolXD]);
    let valid = true;
    
    let roundNum = 1;
    let courtNum = 1;
    
    for (let i = 0; i < TOTAL_MATCHES; i++) {
      const type = types[i];
      let bp1, bp2, wp1, wp2;
      
      let tries = 0;
      let found = false;
      while (tries < 100) {
        tries++;
        if (type === 'MD') {
          bp1 = blueMen[Math.floor(Math.random() * blueMen.length)];
          bp2 = blueMen[Math.floor(Math.random() * blueMen.length)];
          wp1 = whiteMen[Math.floor(Math.random() * whiteMen.length)];
          wp2 = whiteMen[Math.floor(Math.random() * whiteMen.length)];
        } else if (type === 'WD') {
          bp1 = blueWomen[Math.floor(Math.random() * blueWomen.length)];
          bp2 = blueWomen[Math.floor(Math.random() * blueWomen.length)];
          wp1 = whiteWomen[Math.floor(Math.random() * whiteWomen.length)];
          wp2 = whiteWomen[Math.floor(Math.random() * whiteWomen.length)];
        } else {
          bp1 = blueMen[Math.floor(Math.random() * blueMen.length)];
          bp2 = blueWomen[Math.floor(Math.random() * blueWomen.length)];
          wp1 = whiteMen[Math.floor(Math.random() * whiteMen.length)];
          wp2 = whiteWomen[Math.floor(Math.random() * whiteWomen.length)];
        }
        
        if (bp1.name === bp2.name || wp1.name === wp2.name) continue;
        
        const bCombo = [bp1.type, bp2.type].sort().join('');
        const wCombo = [wp1.type, wp2.type].sort().join('');
        // Disallow S + E vs D + D, etc. Just ban ES vs DD.
        if (bCombo === 'ES' && wCombo === 'DD') continue;
        if (wCombo === 'ES' && bCombo === 'DD') continue;
        // Don't pair S with E against anyone, it's safer.
        if (bCombo === 'ES' || wCombo === 'ES') continue;
        
        const bPen = bp1.pen + bp2.pen;
        const wPen = wp1.pen + wp2.pen;
        // Penalty diff <= 3
        if (Math.abs(bPen - wPen) > 2) continue; // tightening to 2 for better balance
        
        if (matchCounts[bp1.name] >= 4 || matchCounts[bp2.name] >= 4 || matchCounts[wp1.name] >= 4 || matchCounts[wp2.name] >= 4) {
          continue;
        }
        
        found = true;
        break;
      }
      
      if (!found) {
        valid = false;
        break;
      }
      
      const bPen = bp1.pen + bp2.pen;
      const wPen = wp1.pen + wp2.pen;
      let finalBluePen = 0;
      let finalWhitePen = 0;
      if (bPen > wPen) finalBluePen = bPen - wPen;
      else if (wPen > bPen) finalWhitePen = wPen - bPen;
      
      matches.push({
        round: roundNum,
        court: courtNum,
        type: type,
        actual_type: `${type}:${finalBluePen}:${finalWhitePen}`,
        b1: bp1.name,
        b2: bp2.name,
        w1: wp1.name,
        w2: wp2.name
      });
      
      matchCounts[bp1.name]++;
      matchCounts[bp2.name]++;
      matchCounts[wp1.name]++;
      matchCounts[wp2.name]++;
      
      courtNum++;
      if (courtNum > 2) {
        courtNum = 1;
        roundNum++;
      }
    }
    
    if (valid) {
      const counts = Object.values(matchCounts);
      const minGames = Math.min(...counts);
      const maxGames = Math.max(...counts);
      if (minGames >= 3 && maxGames <= 4) {
        return matches;
      }
    }
  }
  
  return null;
}

async function run() {
  const schedule = generateMatches();
  if (!schedule) {
    console.log("Failed to generate schedule.");
    return;
  }
  console.log("Found valid schedule with 24 matches!");
  
  console.log("Clearing old matches...");
  const { error: delErr } = await supabase.from('matches').delete().neq('id', '00000000-0000-0000-0000-000000000000');
  if (delErr) {
    console.error("Delete error", delErr);
    return;
  }
  
  const insertData = schedule.map(m => ({
    round_num: m.round,
    court_num: m.court,
    match_type: m.actual_type,
    blue_player1: m.b1,
    blue_player2: m.b2,
    white_player1: m.w1,
    white_player2: m.w2,
    status: 'pending'
  }));
  
  const { error: insErr } = await supabase.from('matches').insert(insertData);
  if (insErr) {
    console.error("Insert error", insErr);
  } else {
    console.log("Successfully inserted new schedule!");
  }
}

run();
