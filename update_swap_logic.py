import re

with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# 1. Update the handleSwapGenerated function to take the targetPlayer directly instead of prompting
old_func = """  const handleSwapGenerated = (matchIndex: number, team: 'blue' | 'white', playerIndex: 0 | 1) => {
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
  };"""

new_func = """  const handleSwapGenerated = (matchIndex: number, team: 'blue' | 'white', playerIndex: 0 | 1, targetPlayerName: string) => {
    const targetPlayer = dbPlayers.find(p => p.name === targetPlayerName);
    if (!targetPlayer) return;

    const newBracket = [...generatedBracket];
    
    // Check if target player is already in THIS round. If so, do a 2-way swap!
    const roundNum = newBracket[matchIndex].round_num;
    const currentOccupant = team === 'blue' ? newBracket[matchIndex].blue_team[playerIndex] : newBracket[matchIndex].white_team[playerIndex];
    
    let foundAndSwapped = false;
    for (let i = 0; i < newBracket.length; i++) {
      if (newBracket[i].round_num === roundNum) {
        if (newBracket[i].blue_team[0].name === targetPlayer.name) { newBracket[i].blue_team[0] = currentOccupant; foundAndSwapped = true; break; }
        if (newBracket[i].blue_team[1].name === targetPlayer.name) { newBracket[i].blue_team[1] = currentOccupant; foundAndSwapped = true; break; }
        if (newBracket[i].white_team[0].name === targetPlayer.name) { newBracket[i].white_team[0] = currentOccupant; foundAndSwapped = true; break; }
        if (newBracket[i].white_team[1].name === targetPlayer.name) { newBracket[i].white_team[1] = currentOccupant; foundAndSwapped = true; break; }
      }
    }

    if (team === 'blue') {
      newBracket[matchIndex].blue_team[playerIndex] = targetPlayer;
    } else {
      newBracket[matchIndex].white_team[playerIndex] = targetPlayer;
    }
    
    setGeneratedBracket(newBracket);
  };"""

content = content.replace(old_func, new_func)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
