import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { checklistSummary, parseWon, checklistError } from '../src/lib/checklists.ts';

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

test('등록 스크립트와 SQL은 탈퇴 회원을 제외한 최신 38명을 유지한다', () => {
  const expected = '강봉선 김기원 김세라 김승현 김여진 김진수 김창수 김태섭 박지윤 박진현 배진희 백숙호 손병근 신나리 양하나 오성환 유반석 유소라 이정훈 이청아 장기철 장상원 장성학 정광종 정규임 정진선 조아라 조유정 주원휘 최진용 현정혜 배형남 박수신 송온유 박미자 전영배 송환희 강민정'.split(' ').sort();
  const seed = readFileSync(new URL('../import_players.js', import.meta.url), 'utf8');
  const sql = readFileSync(new URL('../checklist_setup.sql', import.meta.url), 'utf8');
  assert.deepEqual([...seed.matchAll(/"Name":"([^"]+)"/g)].map(match => match[1]).sort(), expected);
  assert.deepEqual([...sql.matchAll(/\('([^']+)','[SABCDE]',/g)].map(match => match[1]).sort(), expected);
  assert.match(sql, /delete from public\.players where name = '송지은'/);
  assert.doesNotMatch(sql, /(?:delete from|update) public\.matches/i);
});
