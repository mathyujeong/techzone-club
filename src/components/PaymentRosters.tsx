"use client";

import { useEffect, useRef, useState } from "react";
import { ArrowDown, Check, Copy } from "lucide-react";
import { formatPaymentRoster, groupChecklistPayments, type ChecklistEntry } from "@/lib/checklists";

type PaymentFilter = "paid" | "unpaid";

function RosterCard({ title, label, members, busy, onView }: {
  title: string;
  label: "납부" | "미납";
  members: ChecklistEntry[];
  busy: boolean;
  onView: () => void;
}) {
  const [copiedText, setCopiedText] = useState<string | null>(null);
  const [manualCopy, setManualCopy] = useState(false);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const text = formatPaymentRoster(title, label, members);
  const copied = copiedText === text;
  const amount = members.reduce((total, member) => total + member.amount, 0);

  useEffect(() => () => { if (timer.current) clearTimeout(timer.current); }, []);

  async function copyNames() {
    try {
      await navigator.clipboard.writeText(text);
      setManualCopy(false);
      setCopiedText(text);
      if (timer.current) clearTimeout(timer.current);
      timer.current = setTimeout(() => setCopiedText(null), 2000);
    } catch {
      setManualCopy(true);
    }
  }

  return (
    <section aria-label={`${label} 명단`} className="min-w-0 rounded-2xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-gray-900">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h3 className="flex items-center gap-2 text-sm font-bold">{label} 명단<span className="rounded-md bg-gray-100 px-2 py-1 text-xs text-gray-600 dark:bg-gray-800 dark:text-gray-300">{members.length}명</span></h3>
        <button type="button" aria-label={`${label} 명단 복사`} disabled={busy || !members.length} onClick={() => void copyNames()} className="inline-flex min-h-10 items-center justify-center gap-1.5 rounded-lg px-2 py-2 text-xs font-bold text-gray-600 hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-40 dark:text-gray-300 dark:hover:bg-gray-800">
          {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}{copied ? "복사됨" : "명단 복사"}
        </button>
      </div>
      {members.length ? (
        <ul aria-label={`${label}자 이름`} className="mt-3 flex max-h-44 flex-wrap gap-2 overflow-y-auto">
          {members.map(member => <li key={member.id} className="rounded-lg bg-gray-50 px-3 py-2 text-sm dark:bg-gray-800">{member.player_name}</li>)}
        </ul>
      ) : <p className="py-5 text-sm text-gray-500">{label === "미납" ? "미납자가 없어요." : "아직 납부한 회원이 없어요."}</p>}
      <div className="mt-4 flex flex-wrap items-center justify-between gap-2 border-t border-gray-100 pt-3 dark:border-gray-800">
        <p className="text-xs text-gray-500">{label} 금액 <span className="font-bold tabular-nums text-gray-700 dark:text-gray-200">{amount.toLocaleString("ko-KR")}원</span></p>
        <button type="button" disabled={!members.length} onClick={onView} className="inline-flex min-h-10 items-center gap-1 text-xs font-bold text-yellow-700 disabled:opacity-40 dark:text-yellow-400">{label}자만 보기<ArrowDown className="h-3.5 w-3.5" /></button>
      </div>
      {manualCopy && <div className="mt-3 space-y-2">
        <p className="text-xs text-gray-500">자동 복사가 안 되는 환경이에요. 아래 명단을 선택해 복사해주세요.</p>
        <textarea aria-label={`${label} 명단 복사용 텍스트`} readOnly autoFocus onFocus={event => event.currentTarget.select()} value={text} rows={4} className="w-full rounded-xl border border-gray-300 bg-gray-50 p-3 text-sm outline-none focus:border-yellow-500 dark:border-gray-700 dark:bg-gray-800" />
      </div>}
    </section>
  );
}

export default function PaymentRosters({ title, entries, busy, onFilter }: {
  title: string;
  entries: ChecklistEntry[];
  busy: boolean;
  onFilter: (filter: PaymentFilter) => void;
}) {
  const groups = groupChecklistPayments(entries);
  return (
    <section aria-label="납부 현황 명단" className="space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-2"><h2 className="text-base font-bold">납부 현황 명단</h2><p className="text-xs text-gray-500">전체 대상 회원 기준 · 가나다순</p></div>
      <div className="grid gap-3 md:grid-cols-2">
        <RosterCard title={title} label="미납" members={groups.unpaid} busy={busy} onView={() => onFilter("unpaid")} />
        <RosterCard title={title} label="납부" members={groups.paid} busy={busy} onView={() => onFilter("paid")} />
      </div>
    </section>
  );
}
