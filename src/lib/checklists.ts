export interface ClubChecklist {
  id: string;
  title: string;
  description: string;
  input_label: string;
  default_amount: number;
  archived: boolean;
  created_at: string;
}

export interface ChecklistEntry {
  id: string;
  checklist_id: string;
  player_id: string | null;
  player_name: string;
  content: string;
  memo: string;
  amount: number;
  is_paid: boolean;
  paid_at: string | null;
}

export function checklistSummary(entries: ChecklistEntry[]) {
  return entries.reduce(
    (summary, entry) => ({
      count: summary.count + 1,
      paidCount: summary.paidCount + Number(entry.is_paid),
      totalAmount: summary.totalAmount + entry.amount,
      paidAmount: summary.paidAmount + (entry.is_paid ? entry.amount : 0),
    }),
    { count: 0, paidCount: 0, totalAmount: 0, paidAmount: 0 },
  );
}

export function parseWon(value: string): number | null {
  if (!/^\d+$/.test(value)) return null;
  const amount = Number(value);
  return Number.isSafeInteger(amount) && amount <= 2147483647 ? amount : null;
}

export function checklistError(error: { message: string; code?: string }): string {
  if (["42P01", "42883", "PGRST202", "PGRST205"].includes(error.code || "")) {
    return "체크리스트 기능의 DB 설정이 아직 적용되지 않았어요. Supabase에서 checklist_setup.sql을 실행한 뒤 다시 불러와주세요.";
  }
  return `저장하거나 불러오지 못했어요. ${error.message}`;
}
