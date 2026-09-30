import json
import random

blue_men = [{"id": "BM1", "name": "강봉선", "grade": "S", "score": -5}, {"id": "BM2", "name": "김태섭", "grade": "A", "score": -4}, {"id": "BM3", "name": "유반석", "grade": "B", "score": -3}, {"id": "BM4", "name": "전영배", "grade": "E", "score": 0}, {"id": "BM5", "name": "주원희", "grade": "E", "score": 0}]
blue_women = [{"id": "BW1", "name": "정진선", "grade": "S", "score": -5}, {"id": "BW2", "name": "양하나", "grade": "A", "score": -4}, {"id": "BW3", "name": "유소라", "grade": "A", "score": -4}, {"id": "BW4", "name": "김기원", "grade": "B", "score": -3}, {"id": "BW5", "name": "현정혜", "grade": "B", "score": -3}, {"id": "BW6", "name": "강민정", "grade": "E", "score": 0}, {"id": "BW7", "name": "배진희", "grade": "E", "score": 0}]
white_men = [{"id": "WM1", "name": "최진용", "grade": "A", "score": -4}, {"id": "WM2", "name": "김창수", "grade": "A", "score": -4}, {"id": "WM3", "name": "이정훈", "grade": "B", "score": -3}, {"id": "WM4", "name": "송온유", "grade": "D", "score": -1}, {"id": "WM5", "name": "백숙호", "grade": "D", "score": -1}, {"id": "WM6", "name": "장상원", "grade": "E", "score": 0}]
white_women = [{"id": "WW1", "name": "박지윤", "grade": "S", "score": -5}, {"id": "WW2", "name": "신나리", "grade": "S", "score": -5}, {"id": "WW3", "name": "김세라", "grade": "A", "score": -4}, {"id": "WW4", "name": "이청아", "grade": "C", "score": -2}, {"id": "WW5", "name": "정규임", "grade": "D", "score": -1}, {"id": "WW6", "name": "조유정", "grade": "D", "score": -1}]

def get_grade_val(g):
    return {'S':5, 'A':4, 'B':3, 'C':2, 'D':1, 'E':0}[g]

def evaluate_match(t1, t2):
    s1 = sum(p['score'] for p in t1)
    s2 = sum(p['score'] for p in t2)
    diff = abs(s1 - s2)
    
    pen = 0
    if len(t1) == 2:
        d1 = abs(get_grade_val(t1[0]['grade']) - get_grade_val(t1[1]['grade']))
        if d1 >= 4: pen += 100
        elif d1 == 3: pen += 20
        d2 = abs(get_grade_val(t2[0]['grade']) - get_grade_val(t2[1]['grade']))
        if d2 >= 4: pen += 100
        elif d2 == 3: pen += 20
    return diff * 10 + pen

best_schedule = None
best_cost = 999999

for _ in range(20000):
    bm_counts = [3]*5; bm_counts[0]+=1; bm_counts[1]+=1; bm_counts[2]+=1
    wm_counts = [3]*6
    bw_counts = [3]*7; bw_counts[0]+=1
    ww_counts = [4,4,4,4,3,3] # ww6 (Yujeong) is 3
    
    random.shuffle(bm_counts)
    random.shuffle(bw_counts)
    random.shuffle(ww_counts) # wait, Yujeong must be 3
    ww_rest = [4,4,4,4,3]
    random.shuffle(ww_rest)
    ww_counts = ww_rest + [3]
    
    bm_pool = []
    for p, c in zip(blue_men, bm_counts): bm_pool.extend([p]*c)
    wm_pool = []
    for p, c in zip(white_men, wm_counts): wm_pool.extend([p]*c)
    bw_pool = []
    for p, c in zip(blue_women, bw_counts): bw_pool.extend([p]*c)
    ww_pool = []
    for p, c in zip(white_women, ww_counts): ww_pool.extend([p]*c)
    
    random.shuffle(bm_pool)
    random.shuffle(wm_pool)
    random.shuffle(bw_pool)
    random.shuffle(ww_pool)
    
    valid = True
    matches = []
    cost = 0
    
    # 4 XD
    xd_bm = bm_pool[:4]; bm_pool = bm_pool[4:]
    xd_wm = wm_pool[:4]; wm_pool = wm_pool[4:]
    xd_bw = bw_pool[:4]; bw_pool = bw_pool[4:]
    xd_ww = ww_pool[:4]; ww_pool = ww_pool[4:]
    
    for i in range(4):
        matches.append(("XD", [xd_bm[i], xd_bw[i]], [xd_wm[i], xd_ww[i]]))
        cost += evaluate_match([xd_bm[i], xd_bw[i]], [xd_wm[i], xd_ww[i]])
        
    # 7 MD
    for i in range(7):
        t1 = bm_pool[i*2:i*2+2]
        t2 = wm_pool[i*2:i*2+2]
        if t1[0]['id'] == t1[1]['id'] or t2[0]['id'] == t2[1]['id']:
            valid = False; break
        matches.append(("MD", t1, t2))
        cost += evaluate_match(t1, t2)
        
    if not valid: continue
    
    # 9 WD
    for i in range(9):
        t1 = bw_pool[i*2:i*2+2]
        t2 = ww_pool[i*2:i*2+2]
        if t1[0]['id'] == t1[1]['id'] or t2[0]['id'] == t2[1]['id']:
            valid = False; break
        matches.append(("WD", t1, t2))
        cost += evaluate_match(t1, t2)
        
    if valid and cost < best_cost:
        best_cost = cost
        best_schedule = matches

print("Best cost:", best_cost)
rounds = []
unassigned = best_schedule[:]
for r in range(7):
    round_matches = []
    playing = set()
    random.shuffle(unassigned)
    to_rem = []
    for m in unassigned:
        m_type, t1, t2 = m
        pids = [p['id'] for p in t1] + [p['id'] for p in t2]
        if not any(pid in playing for pid in pids):
            round_matches.append(m)
            playing.update(pids)
            to_rem.append(m)
            if len(round_matches) == 3: break
    for m in to_rem: unassigned.remove(m)
    rounds.append(round_matches)

for m in unassigned: rounds[-1].append(m)

out = []
for i, r in enumerate(rounds):
    for j, m in enumerate(r):
        out.append({
            "round": i+1, "court": j+1, "type": m[0],
            "blue_team": [f"{p['name']}({p['grade']})" for p in m[1]],
            "white_team": [f"{p['name']}({p['grade']})" for p in m[2]],
            "blue_score": sum(p['score'] for p in m[1]),
            "white_score": sum(p['score'] for p in m[2])
        })
with open('src/data/tournament.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
