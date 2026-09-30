const { createClient } = require('@supabase/supabase-js');
const dotenv = require('dotenv');
dotenv.config({ path: './.env.local' });

const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY);

async function run() {
  const { data: matches, error } = await supabase.from('matches').select('*').order('round_num').order('court_num');
  if (error) { console.error(error); return; }

  // 1. Check duplicate player in the same round
  const roundPlayers = {};
  const duplicatesInRound = [];
  
  // 2. Check back-to-back games
  const playerRounds = {};
  
  // 3. Check duplicate partnerships
  const partnerships = {};
  const duplicatePartners = [];

  matches.forEach(m => {
    const r = m.round_num;
    if (!roundPlayers[r]) roundPlayers[r] = [];
    
    const players = [m.blue_player1, m.blue_player2, m.white_player1, m.white_player2].filter(Boolean);
    
    // Check partnerships
    if (m.blue_player1 && m.blue_player2) {
      const pair = [m.blue_player1, m.blue_player2].sort().join(' & ');
      partnerships[pair] = (partnerships[pair] || 0) + 1;
      if (partnerships[pair] === 2) duplicatePartners.push(pair);
    }
    if (m.white_player1 && m.white_player2) {
      const pair = [m.white_player1, m.white_player2].sort().join(' & ');
      partnerships[pair] = (partnerships[pair] || 0) + 1;
      if (partnerships[pair] === 2) duplicatePartners.push(pair);
    }

    players.forEach(p => {
      // 1. Same round check
      if (roundPlayers[r].includes(p)) {
        duplicatesInRound.push({ round: r, player: p });
      } else {
        roundPlayers[r].push(p);
      }
      
      // 2. Collect rounds for back-to-back check
      if (!playerRounds[p]) playerRounds[p] = [];
      playerRounds[p].push(r);
    });
  });

  // Check back-to-back
  const backToBackIssues = [];
  for (const [p, rounds] of Object.entries(playerRounds)) {
    rounds.sort((a, b) => a - b);
    let consecutive = 1;
    let maxConsecutive = 1;
    for (let i = 1; i < rounds.length; i++) {
      if (rounds[i] === rounds[i-1] + 1) {
        consecutive++;
        if (consecutive > maxConsecutive) maxConsecutive = consecutive;
      } else if (rounds[i] !== rounds[i-1]) {
        consecutive = 1;
      }
    }
    if (maxConsecutive >= 3) {
      backToBackIssues.push({ player: p, consecutive: maxConsecutive, rounds: rounds });
    }
  }
  
  // Game counts
  const gameCounts = Object.entries(playerRounds).map(([p, r]) => ({ player: p, count: r.length }));
  
  console.log("=== 검증 결과 ===");
  console.log("\n1. 같은 라운드 중복 출전 (에러):");
  if (duplicatesInRound.length === 0) console.log(" -> 없음! 완벽합니다.");
  else duplicatesInRound.forEach(d => console.log(` -> ${d.player} 님이 ${d.round}라운드에 2번 들어갔습니다!`));

  console.log("\n2. 연속 3게임 이상 출전 (체력 부담):");
  if (backToBackIssues.length === 0) console.log(" -> 3게임 연속 출전하는 사람은 없습니다.");
  else backToBackIssues.forEach(b => console.log(` -> ${b.player} 님: ${b.consecutive}게임 연속 출전 (출전 라운드: ${b.rounds.join(', ')})`));

  console.log("\n3. 똑같은 파트너와 2번 이상 치는 케이스:");
  if (duplicatePartners.length === 0) console.log(" -> 없음! 모두 다양한 파트너와 칩니다.");
  else duplicatePartners.forEach(p => console.log(` -> 파트너 중복: ${p}`));
  
  console.log("\n4. 인당 게임 수 통계:");
  const countStats = {};
  gameCounts.forEach(g => {
    countStats[g.count] = (countStats[g.count] || 0) + 1;
  });
  for (const [count, ppl] of Object.entries(countStats)) {
    console.log(` -> ${count}게임 치는 사람: ${ppl}명`);
  }
}

run();
