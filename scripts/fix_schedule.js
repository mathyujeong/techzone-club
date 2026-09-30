const { createClient } = require('@supabase/supabase-js');
const dotenv = require('dotenv');
dotenv.config({ path: './.env.local' });

const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY);

function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

async function run() {
  const { data: matches, error } = await supabase.from('matches').select('*').order('round_num').order('court_num');
  if (error) { console.error(error); return; }

  // Extracted matchups
  const mList = matches.map(m => {
    return {
      id: m.id,
      players: [m.blue_player1, m.blue_player2, m.white_player1, m.white_player2].filter(Boolean)
    };
  });

  let bestSchedule = null;
  let bestScore = 999999; // lower is better (penalty)

  for (let attempt = 0; attempt < 50000; attempt++) {
    const indices = shuffle(Array.from({length: 21}, (_, i) => i));
    
    let rounds = [[], [], [], [], [], [], []];
    let valid = true;
    
    for (let i = 0; i < 21; i++) {
      const matchIdx = indices[i];
      const match = mList[matchIdx];
      
      let placed = false;
      for (let r = 0; r < 7; r++) {
        if (rounds[r].length >= 3) continue;
        
        let conflict = false;
        for (const existingMatch of rounds[r]) {
          for (const p of match.players) {
            if (existingMatch.players.includes(p)) {
              conflict = true;
              break;
            }
          }
          if (conflict) break;
        }
        
        if (!conflict) {
          rounds[r].push(match);
          placed = true;
          break;
        }
      }
      if (!placed) {
        valid = false;
        break;
      }
    }
    
    if (valid) {
      // Calculate penalty (consecutive games)
      let playerRounds = {};
      rounds.forEach((roundMatches, r) => {
        roundMatches.forEach(m => {
          m.players.forEach(p => {
            if (!playerRounds[p]) playerRounds[p] = [];
            playerRounds[p].push(r);
          });
        });
      });
      
      let penalty = 0;
      for (const [p, rList] of Object.entries(playerRounds)) {
        rList.sort((a, b) => a - b);
        let cons = 1;
        for (let i = 1; i < rList.length; i++) {
          if (rList[i] === rList[i-1] + 1) {
            cons++;
          } else {
            if (cons >= 3) penalty += Math.pow(10, cons); // heavily penalize 3 or 4 consecutive
            if (cons === 2) penalty += 1;
            cons = 1;
          }
        }
        if (cons >= 3) penalty += Math.pow(10, cons);
        if (cons === 2) penalty += 1;
      }
      
      if (penalty < bestScore) {
        bestScore = penalty;
        bestSchedule = rounds;
        if (penalty === 0) break; // perfect!
      }
    }
  }

  if (bestSchedule) {
    console.log("Found a valid arrangement with penalty score:", bestScore);
    
    let updates = [];
    bestSchedule.forEach((roundMatches, r) => {
      roundMatches.forEach((m, c) => {
        updates.push({
          id: m.id,
          round_num: r + 1,
          court_num: c + 1
        });
      });
    });

    console.log(JSON.stringify(updates, null, 2));
    
    // We can execute updates if requested
    for (const u of updates) {
       await supabase.from('matches').update({ round_num: u.round_num, court_num: u.court_num }).eq('id', u.id);
    }
    console.log("Updated database successfully!");
  } else {
    console.log("Could not find a valid arrangement.");
  }
}

run();
