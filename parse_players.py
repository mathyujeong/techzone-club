import json

blue_men = [{"id": "BM1", "name": "강봉선", "grade": "S", "score": -8}, {"id": "BM2", "name": "김태섭", "grade": "A", "score": -4}, {"id": "BM3", "name": "유반석", "grade": "B", "score": -3}, {"id": "BM4", "name": "전영배", "grade": "E", "score": 0}, {"id": "BM5", "name": "주원희", "grade": "E", "score": 0}]
blue_women = [{"id": "BW1", "name": "정진선", "grade": "S", "score": -5}, {"id": "BW2", "name": "양하나", "grade": "A", "score": -4}, {"id": "BW3", "name": "유소라", "grade": "A", "score": -4}, {"id": "BW4", "name": "현정혜", "grade": "B", "score": -3}, {"id": "BW5", "name": "이청아", "grade": "C", "score": -2}, {"id": "BW6", "name": "정규임", "grade": "D", "score": -1}, {"id": "BW7", "name": "배진희", "grade": "E", "score": 0}]
white_men = [{"id": "WM1", "name": "최진용", "grade": "A", "score": -4}, {"id": "WM2", "name": "김창수", "grade": "A", "score": -4}, {"id": "WM3", "name": "이정훈", "grade": "B", "score": -3}, {"id": "WM4", "name": "송온유", "grade": "D", "score": -1}, {"id": "WM5", "name": "백숙호", "grade": "D", "score": -1}, {"id": "WM6", "name": "장상원", "grade": "E", "score": 0}]
white_women = [{"id": "WW1", "name": "박지윤", "grade": "S", "score": -5}, {"id": "WW2", "name": "신나리", "grade": "S", "score": -5}, {"id": "WW3", "name": "김세라", "grade": "A", "score": -4}, {"id": "WW4", "name": "김기원", "grade": "B", "score": -3}, {"id": "WW5", "name": "조유정", "grade": "D", "score": -1}, {"id": "WW6", "name": "강민정", "grade": "E", "score": 0}]

all_players = blue_men + blue_women + white_men + white_women
for p in all_players:
    print(f"('{p['name']}', '{p['grade']}', {p['score']}),")
