import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { checklistSummary, parseWon, checklistError, groupChecklistPayments, formatPaymentRoster } from '../src/lib/checklists.ts';

test('금액은 원 단위의 0 이상 정수만 허용한다', () => {
  assert.equal(parseWon('0'), 0);
  assert.equal(parseWon('20000'), 20000);
  assert.equal(parseWon('2147483647'), 2147483647);
  for (const value of ['', ' ', '-1', '1.5', '1e3', '10,000', 'NaN', '2147483648']) {
    assert.equal(parseWon(value), null, value);
  }
});

test('납부 상태와 회원별로 다른 금액을 기준으로 합산한다', () => {
  const entries = [
    { amount: 20000, is_paid: true },
    { amount: 40000, is_paid: false },
    { amount: 0, is_paid: true },
  ];
  assert.deepEqual(checklistSummary(entries), { count: 3, paidCount: 2, totalAmount: 60000, paidAmount: 20000 });
  entries[1].is_paid = true;
  assert.equal(checklistSummary(entries).paidAmount, 60000);
  entries[0].is_paid = false;
  assert.deepEqual(checklistSummary(entries), { count: 3, paidCount: 2, totalAmount: 60000, paidAmount: 40000 });
  assert.deepEqual(checklistSummary([]), { count: 0, paidCount: 0, totalAmount: 0, paidAmount: 0 });
});

test('테이블이나 생성 함수가 없으면 DB 설정 안내를 표시한다', () => {
  for (const code of ['42P01', '42883', 'PGRST202', 'PGRST205']) {
    assert.match(checklistError({ code, message: 'missing' }), /checklist_setup\.sql/);
  }
  assert.match(checklistError({ code: '42501', message: 'permission denied' }), /permission denied/);
});

test('납부 여부로 명단을 나누고 원래 순서를 바꾸지 않는다', () => {
  const entries = [
    { id: '1', player_name: '최진용', is_paid: true, amount: 20000 },
    { id: '2', player_name: '김세라', is_paid: false, amount: 0 },
    { id: '3', player_name: '강봉선', is_paid: true, amount: 40000 },
  ];
  const groups = groupChecklistPayments(entries);
  assert.deepEqual(groups.paid.map(entry => entry.player_name), ['강봉선', '최진용']);
  assert.deepEqual(groups.unpaid.map(entry => entry.player_name), ['김세라']);
  assert.deepEqual(entries.map(entry => entry.id), ['1', '2', '3']);
  entries[1].is_paid = true;
  assert.equal(groupChecklistPayments(entries).paid.length, 3);
  assert.equal(groupChecklistPayments(entries).unpaid.length, 0);
  assert.deepEqual(groupChecklistPayments([]), { paid: [], unpaid: [] });
});

test('복사할 명단은 제목, 납부 구분, 인원과 가나다순 이름을 포함한다', () => {
  const entries = [{ player_name: '최진용' }, { player_name: '강봉선' }];
  assert.equal(formatPaymentRoster('단체티 주문', '납부', entries), '[단체티 주문]\n납부 명단 (2명)\n강봉선, 최진용');
  assert.equal(formatPaymentRoster('음식 주문', '미납', []), '[음식 주문]\n미납 명단 (0명)\n없음');
});

test('등록 스크립트와 SQL은 탈퇴 회원을 제외한 최신 38명을 유지한다', () => {
  const expected = '강봉선 김기원 김세라 김승현 김여진 김진수 김창수 김태섭 박지윤 박진현 배진희 백숙호 손병근 신나리 양하나 오성환 유반석 유소라 이정훈 이청아 장기철 장상원 장성학 정광종 정규임 정진선 조아라 조유정 주원휘 최진용 현정혜 배형남 박수신 송온유 박미자 전영배 송환희 강민정'.split(' ').sort();
  const seed = readFileSync(new URL('../import_players.js', import.meta.url), 'utf8');
  const sql = readFileSync(new URL('../checklist_setup.sql', import.meta.url), 'utf8');
  assert.deepEqual([...seed.matchAll(/"Name":"([^"]+)"/g)].map(match => match[1]).sort(), expected);
  assert.deepEqual([...sql.matchAll(/\('([^']+)','[SABCDE]',/g)].map(match => match[1]).sort(), expected);
  assert.match(sql, /delete from public\.players where name = '송지은'/);
  assert.doesNotMatch(sql, /(?:delete from|update) public\.matches/i);
});
