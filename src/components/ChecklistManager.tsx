"use client";

import { useEffect, useRef, useState, type FormEvent, type ReactNode } from "react";
import { Archive, ArrowLeft, ClipboardList, LoaderCircle, Plus, RefreshCw, Search, Users, X } from "lucide-react";
import { supabase } from "@/lib/supabase";
import { checklistError, checklistSummary, parseWon, type ChecklistEntry, type ClubChecklist } from "@/lib/checklists";
import type { Player } from "@/lib/types";

const inputClass = "w-full rounded-xl border border-gray-300 bg-white px-3 py-2.5 text-sm outline-none focus:border-yellow-500 focus:ring-2 focus:ring-yellow-500/20 dark:border-gray-700 dark:bg-gray-900";
const buttonClass = "inline-flex items-center justify-center gap-2 rounded-xl border border-gray-200 bg-white px-4 py-2.5 text-sm font-bold hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-700 dark:bg-gray-900 dark:hover:bg-gray-800";
const primaryClass = "inline-flex items-center justify-center gap-2 rounded-xl bg-yellow-600 px-4 py-2.5 text-sm font-bold text-white hover:bg-yellow-700 disabled:cursor-not-allowed disabled:opacity-50";
const won = (amount: number) => `${amount.toLocaleString("ko-KR")}원`;
type Notice = { kind: "success" | "error"; message: string } | null;

function Dialog({ title, onClose, busy, children }: { title: string; onClose: () => void; busy: boolean; children: ReactNode }) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    const dialog = ref.current;
    dialog?.showModal();
    return () => dialog?.close();
  }, []);
  return (
    <dialog ref={ref} aria-label={title} onCancel={event => { event.preventDefault(); if (!busy) onClose(); }} className="m-auto max-h-[90dvh] w-[calc(100%-2rem)] max-w-xl overflow-y-auto rounded-2xl border border-gray-200 bg-white p-0 text-gray-900 shadow-2xl backdrop:bg-black/50 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100">
      <div className="sticky top-0 z-10 flex items-center justify-between border-b border-gray-200 bg-white p-5 dark:border-gray-700 dark:bg-gray-900">
        <h2 className="text-lg font-black">{title}</h2>
        <button type="button" aria-label="닫기" disabled={busy} onClick={onClose} className="rounded-lg p-2 hover:bg-gray-100 disabled:opacity-50 dark:hover:bg-gray-800"><X className="h-5 w-5" /></button>
      </div>
      {children}
    </dialog>
  );
}

function MemberPicker({ players, selected, onChange }: { players: Player[]; selected: string[]; onChange: (ids: string[]) => void }) {
  const [search, setSearch] = useState("");
  const visible = players.filter(player => player.name.includes(search.trim()));
  return (
    <fieldset className="space-y-3">
      <legend className="mb-2 text-sm font-bold">대상 회원 <span className="text-yellow-700 dark:text-yellow-400">{selected.length}명 선택</span></legend>
      <div className="flex items-center gap-2">
        <input aria-label="회원 찾기" placeholder="회원 이름 검색" value={search} onChange={event => setSearch(event.target.value)} className={inputClass} />
        <button type="button" onClick={() => onChange(players.map(player => player.id))} className="shrink-0 text-xs font-bold text-yellow-700 dark:text-yellow-400">전체 선택</button>
        <button type="button" onClick={() => onChange([])} className="shrink-0 text-xs text-gray-500">해제</button>
      </div>
      <div className="grid max-h-52 grid-cols-2 gap-2 overflow-y-auto rounded-xl border border-gray-200 p-3 sm:grid-cols-3 dark:border-gray-700">
        {visible.map(player => (
          <label key={player.id} className={`flex cursor-pointer items-center gap-2 rounded-lg border px-2 py-2.5 text-sm ${selected.includes(player.id) ? "border-yellow-300 bg-yellow-50 dark:border-yellow-800 dark:bg-yellow-950/40" : "border-transparent hover:bg-gray-50 dark:hover:bg-gray-800"}`}>
            <input type="checkbox" checked={selected.includes(player.id)} onChange={event => onChange(event.target.checked ? [...selected, player.id] : selected.filter(id => id !== player.id))} className="h-4 w-4 accent-yellow-600" />
            {player.name}
          </label>
        ))}
        {!visible.length && <p className="col-span-full py-3 text-center text-sm text-gray-500">해당하는 회원이 없어요.</p>}
      </div>
    </fieldset>
  );
}

function CreateDialog({ players, onClose, onCreated }: { players: Player[]; onClose: () => void; onCreated: (id: string) => void }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [inputLabel, setInputLabel] = useState("주문 내용");
  const [amount, setAmount] = useState("0");
  const [selected, setSelected] = useState(players.map(player => player.id));
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  async function submit(event: FormEvent) {
    event.preventDefault();
    if (busy) return;
    const parsed = parseWon(amount);
    if (parsed === null) { setError("금액은 0 이상의 정수로 입력해주세요."); return; }
    if (!title.trim() || !inputLabel.trim() || !selected.length) { setError("제목과 입력칸 이름을 입력하고 회원을 선택해주세요."); return; }
    setBusy(true);
    setError("");
    const { data, error: resultError } = await supabase.rpc("create_club_checklist", {
      p_title: title.trim(), p_description: description.trim(), p_input_label: inputLabel.trim(),
      p_default_amount: parsed, p_player_ids: selected,
    });
    if (resultError || !data) {
      setError(resultError ? checklistError(resultError) : "생성 결과를 확인하지 못했어요. 목록을 새로 불러와주세요.");
      setBusy(false);
      return;
    }
    onCreated(data as string);
  }
  return (
    <Dialog title="체크리스트 만들기" onClose={onClose} busy={busy}>
      <form onSubmit={submit} className="space-y-5 p-5">
        <label className="block space-y-2 text-sm font-bold">제목<input autoFocus required maxLength={100} value={title} onChange={event => setTitle(event.target.value)} placeholder="예: 2026 단체티 주문" className={inputClass} /></label>
        <label className="block space-y-2 text-sm font-bold">설명 <span className="font-normal text-gray-400">선택</span><textarea maxLength={2000} value={description} onChange={event => setDescription(event.target.value)} placeholder="마감일이나 안내 내용을 적어주세요." rows={2} className={inputClass} /></label>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <label className="block space-y-2 text-sm font-bold">입력칸 이름<input required maxLength={40} value={inputLabel} onChange={event => setInputLabel(event.target.value)} placeholder="예: 사이즈 / 주문 메뉴" className={inputClass} /></label>
          <label className="block space-y-2 text-sm font-bold">1인 기본 금액 (원)<input required type="number" min="0" max="2147483647" step="1" value={amount} onChange={event => setAmount(event.target.value)} className={inputClass} /></label>
        </div>
        <p className="text-xs leading-relaxed text-gray-500">금액이 없으면 0원으로 두세요. 생성 후 회원별로 금액을 바꿀 수 있어요.</p>
        <MemberPicker players={players} selected={selected} onChange={setSelected} />
        {error && <p role="alert" className="rounded-xl bg-red-50 p-3 text-sm text-red-700 dark:bg-red-950/40 dark:text-red-300">{error}</p>}
        <div className="flex justify-end gap-2 border-t border-gray-100 pt-4 dark:border-gray-800">
          <button type="button" disabled={busy} onClick={onClose} className={buttonClass}>취소</button>
          <button disabled={busy || !selected.length} className={primaryClass}>{busy ? <LoaderCircle className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />}{busy ? "생성 중…" : `${selected.length}명으로 만들기`}</button>
        </div>
      </form>
    </Dialog>
  );
}

function EntryDialog({ entry, checklist, onClose, onSaved }: { entry: ChecklistEntry; checklist: ClubChecklist; onClose: () => void; onSaved: (entry: ChecklistEntry) => void }) {
  const [content, setContent] = useState(entry.content);
  const [memo, setMemo] = useState(entry.memo);
  const [amount, setAmount] = useState(String(entry.amount));
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  async function submit(event: FormEvent) {
    event.preventDefault();
    if (busy) return;
    const parsed = parseWon(amount);
    if (parsed === null) { setError("금액은 0 이상의 정수로 입력해주세요."); return; }
    setBusy(true);
    const { data, error: resultError } = await supabase.from("club_checklist_entries")
      .update({ content: content.trim(), memo: memo.trim(), amount: parsed }).eq("id", entry.id).select().single();
    if (resultError) { setError(checklistError(resultError)); setBusy(false); return; }
    onSaved(data as ChecklistEntry);
  }
  return (
    <Dialog title={`${entry.player_name} · 주문 정보`} onClose={onClose} busy={busy}>
      <form onSubmit={submit} className="space-y-5 p-5">
        <label className="block space-y-2 text-sm font-bold">{checklist.input_label}<input autoFocus maxLength={500} value={content} onChange={event => setContent(event.target.value)} placeholder={`${checklist.input_label} 입력`} className={inputClass} /></label>
        <label className="block space-y-2 text-sm font-bold">받을 금액 (원)<input required type="number" min="0" max="2147483647" step="1" value={amount} onChange={event => setAmount(event.target.value)} className={inputClass} /></label>
        <label className="block space-y-2 text-sm font-bold">메모<textarea maxLength={1000} rows={3} value={memo} onChange={event => setMemo(event.target.value)} placeholder="수량, 수령 여부 등" className={inputClass} /></label>
        {error && <p role="alert" className="text-sm text-red-600 dark:text-red-400">{error}</p>}
        <div className="flex justify-end gap-2"><button type="button" disabled={busy} onClick={onClose} className={buttonClass}>취소</button><button disabled={busy} className={primaryClass}>{busy ? "저장 중…" : "저장"}</button></div>
      </form>
    </Dialog>
  );
}

function AddMembersDialog({ players, checklistId, onClose, onSaved }: { players: Player[]; checklistId: string; onClose: () => void; onSaved: () => void }) {
  const [selected, setSelected] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  async function submit(event: FormEvent) {
    event.preventDefault();
    if (busy || !selected.length) return;
    setBusy(true);
    const { error: resultError } = await supabase.rpc("add_club_checklist_members", { p_checklist_id: checklistId, p_player_ids: selected });
    if (resultError) { setError(checklistError(resultError)); setBusy(false); return; }
    onSaved();
  }
  return (
    <Dialog title="대상 회원 추가" onClose={onClose} busy={busy}>
      <form onSubmit={submit} className="space-y-5 p-5">
        <MemberPicker players={players} selected={selected} onChange={setSelected} />
        {error && <p role="alert" className="text-sm text-red-600 dark:text-red-400">{error}</p>}
        <div className="flex justify-end gap-2"><button type="button" disabled={busy} onClick={onClose} className={buttonClass}>취소</button><button disabled={busy || !selected.length} className={primaryClass}>{busy ? "추가 중…" : `${selected.length}명 추가`}</button></div>
      </form>
    </Dialog>
  );
}

function PaidButton({ entry, disabled, saving, onClick }: { entry: ChecklistEntry; disabled: boolean; saving: boolean; onClick: () => void }) {
  return <button aria-label={`${entry.player_name} 납부 ${entry.is_paid ? "O" : "X"}`} aria-pressed={entry.is_paid} disabled={disabled} onClick={onClick} className={`flex min-h-11 min-w-16 items-center justify-center gap-1 rounded-xl border px-3 py-2 font-black disabled:cursor-not-allowed disabled:opacity-60 ${entry.is_paid ? "border-green-200 bg-green-50 text-green-700 dark:border-green-900 dark:bg-green-950/40 dark:text-green-400" : "border-gray-200 bg-gray-100 text-gray-600 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300"}`}>{saving ? <LoaderCircle className="h-4 w-4 animate-spin" /> : entry.is_paid ? "O" : "X"}</button>;
}

export default function ChecklistManager({ players }: { players: Player[] }) {
  const [checklists, setChecklists] = useState<ClubChecklist[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [entries, setEntries] = useState<ChecklistEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState(false);
  const [notice, setNotice] = useState<Notice>(null);
  const [scope, setScope] = useState<"active" | "archived">("active");
  const [filter, setFilter] = useState<"all" | "unpaid" | "paid">("all");
  const [search, setSearch] = useState("");
  const [createOpen, setCreateOpen] = useState(false);
  const [addOpen, setAddOpen] = useState(false);
  const [editing, setEditing] = useState<ChecklistEntry | null>(null);
  const [busyIds, setBusyIds] = useState<Set<string>>(new Set());
  const locks = useRef(new Set<string>());
  const detailRequest = useRef(0);
  const roster = players.filter(player => !player.id.startsWith("guest_")).sort((a, b) => a.name.localeCompare(b.name, "ko"));
  const selected = checklists.find(checklist => checklist.id === selectedId);
  const busy = busyIds.size > 0;

  async function loadLists() {
    setLoading(true);
    const { data, error } = await supabase.from("club_checklists").select("*").order("created_at", { ascending: false });
    if (error) { setNotice({ kind: "error", message: checklistError(error) }); setLoading(false); return false; }
    setChecklists(data as ClubChecklist[]);
    setLoading(false);
    return true;
  }

  async function loadEntries(id: string) {
    const request = ++detailRequest.current;
    setDetailLoading(true);
    setDetailError(false);
    setEntries([]);
    const { data, error } = await supabase.from("club_checklist_entries").select("*").eq("checklist_id", id).order("player_name");
    if (request !== detailRequest.current) return;
    if (error) { setDetailError(true); setNotice({ kind: "error", message: checklistError(error) }); }
    else setEntries((data as ChecklistEntry[]).sort((a, b) => a.player_name.localeCompare(b.player_name, "ko")));
    setDetailLoading(false);
  }

  useEffect(() => {
    let alive = true;
    const requests = detailRequest;
    supabase.from("club_checklists").select("*").order("created_at", { ascending: false }).then(({ data, error }) => {
      if (!alive) return;
      if (error) setNotice({ kind: "error", message: checklistError(error) });
      else setChecklists(data as ClubChecklist[]);
      setLoading(false);
    });
    return () => { alive = false; requests.current++; };
  }, []);

  function acquire(id: string) {
    if (locks.current.has(id)) return false;
    locks.current.add(id);
    setBusyIds(new Set(locks.current));
    return true;
  }
  function release(id: string) {
    locks.current.delete(id);
    setBusyIds(new Set(locks.current));
  }
  function openList(id: string) {
    if (locks.current.size) return;
    setSelectedId(id);
    setFilter("all");
    setSearch("");
    setNotice(null);
    void loadEntries(id);
  }
  function replaceEntry(entry: ChecklistEntry) {
    setEntries(current => current.map(item => item.id === entry.id ? entry : item));
  }
  async function togglePaid(entry: ChecklistEntry) {
    if (!selected || selected.archived || !acquire(entry.id)) return;
    setNotice(null);
    const { data, error } = await supabase.from("club_checklist_entries").update({ is_paid: !entry.is_paid }).eq("id", entry.id).select().single();
    if (error) setNotice({ kind: "error", message: checklistError(error) });
    else { replaceEntry(data as ChecklistEntry); setNotice({ kind: "success", message: `${entry.player_name} 님의 납부 상태를 저장했어요.` }); }
    release(entry.id);
  }
  async function toggleArchive() {
    if (!selected || locks.current.size || !acquire(selected.id)) return;
    setNotice(null);
    const { data, error } = await supabase.from("club_checklists").update({ archived: !selected.archived }).eq("id", selected.id).select().single();
    if (error) setNotice({ kind: "error", message: checklistError(error) });
    else {
      const result = data as ClubChecklist;
      setChecklists(current => current.map(item => item.id === result.id ? result : item));
      setScope(result.archived ? "archived" : "active");
      setNotice({ kind: "success", message: result.archived ? "체크리스트를 보관했어요. 기록은 그대로 남아 있어요." : "체크리스트를 다시 열었어요." });
    }
    release(selected.id);
  }

  const summary = checklistSummary(entries);
  const visible = entries.filter(entry => entry.player_name.includes(search.trim()) && (filter === "all" || (filter === "paid" ? entry.is_paid : !entry.is_paid)));
  const available = roster.filter(player => !entries.some(entry => entry.player_id === player.id || entry.player_name === player.name));

  return (
    <section className="mx-auto max-w-6xl space-y-6 p-4 md:p-8">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="mb-1 text-xs font-bold tracking-wider text-yellow-700 dark:text-yellow-400">클럽 운영</p>
          <h1 className="flex items-center gap-2 text-2xl font-black"><ClipboardList className="h-6 w-6 text-yellow-600" />체크리스트 관리</h1>
          <p className="mt-2 text-sm text-gray-500">단체티, 음식 주문과 납부 내역을 한곳에서 관리하세요.</p>
        </div>
        <button disabled={loading || busy || !roster.length} onClick={() => setCreateOpen(true)} className={primaryClass}><Plus className="h-4 w-4" />체크리스트 만들기</button>
      </div>

      {notice && <p role={notice.kind === "error" ? "alert" : "status"} className={`rounded-xl border p-4 text-sm ${notice.kind === "error" ? "border-red-200 bg-red-50 text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300" : "border-green-200 bg-green-50 text-green-800 dark:border-green-900 dark:bg-green-950/30 dark:text-green-300"}`}>{notice.message}</p>}

      {!selectedId ? (
        <>
          <div className="flex items-center justify-between gap-3">
            <div className="flex rounded-xl bg-gray-100 p-1 dark:bg-gray-800">
              {([['active', '진행 중'], ['archived', '보관함']] as const).map(([value, label]) => <button key={value} onClick={() => setScope(value)} className={`rounded-lg px-4 py-2 text-sm font-bold ${scope === value ? "bg-white shadow-sm dark:bg-gray-700" : "text-gray-500"}`}>{label} {checklists.filter(item => item.archived === (value === "archived")).length}</button>)}
            </div>
            <button aria-label="체크리스트 새로고침" onClick={() => { setNotice(null); void loadLists(); }} disabled={loading} className={buttonClass}><RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} /><span className="hidden sm:inline">새로고침</span></button>
          </div>
          {loading ? <p role="status" className="py-16 text-center text-gray-500">체크리스트를 불러오는 중…</p> : (
            <div className="grid gap-4 md:grid-cols-2">
              {checklists.filter(item => item.archived === (scope === "archived")).map(item => (
                <button key={item.id} onClick={() => openList(item.id)} className="flex min-h-36 flex-col items-start rounded-2xl border border-gray-200 bg-white p-5 text-left shadow-sm transition hover:border-yellow-400 hover:shadow-md dark:border-gray-800 dark:bg-gray-900">
                  <span className="mb-3 rounded-md bg-gray-100 px-2 py-1 text-xs text-gray-500 dark:bg-gray-800">{item.archived ? "보관됨" : "진행 중"} · {new Date(item.created_at).toLocaleDateString("ko-KR", { timeZone: "Asia/Seoul" })}</span>
                  <h2 className="break-all text-lg font-bold">{item.title}</h2>
                  <p className="mt-2 line-clamp-2 whitespace-pre-wrap break-all text-sm text-gray-500">{item.description || `${item.input_label} · 납부 O/X 관리`}</p>
                </button>
              ))}
              {!checklists.some(item => item.archived === (scope === "archived")) && <div className="col-span-full rounded-2xl border-2 border-dashed border-gray-200 py-16 text-center dark:border-gray-800"><ClipboardList className="mx-auto mb-3 h-10 w-10 text-gray-300" /><p className="font-bold">{scope === "archived" ? "보관한 체크리스트가 없어요." : "첫 체크리스트를 만들어보세요."}</p><p className="mt-2 text-sm text-gray-500">{scope === "archived" ? "완료한 목록은 기록을 보관할 수 있어요." : `등록된 회원 ${roster.length}명을 불러와 바로 시작할 수 있어요.`}</p></div>}
            </div>
          )}
        </>
      ) : selected ? (
        <>
          <div className="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900">
            <button disabled={busy} onClick={() => { detailRequest.current++; setSelectedId(null); setNotice(null); }} className="mb-4 flex items-center gap-1 text-sm text-gray-500 disabled:opacity-50"><ArrowLeft className="h-4 w-4" />목록으로</button>
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h2 className="break-all text-xl font-black">{selected.title}</h2>
              <button disabled={busy || detailLoading || detailError} onClick={toggleArchive} className={buttonClass}>{selected.archived ? <RefreshCw className="h-4 w-4" /> : <Archive className="h-4 w-4" />}{selected.archived ? "다시 열기" : "완료하고 보관"}</button>
            </div>
            {selected.description && <p className="mt-3 whitespace-pre-wrap break-all text-sm text-gray-500">{selected.description}</p>}
            {selected.archived && <p className="mt-3 rounded-lg bg-amber-50 p-3 text-sm text-amber-800 dark:bg-amber-950/30 dark:text-amber-300">보관된 기록이에요. 수정하려면 ‘다시 열기’를 눌러주세요.</p>}
          </div>
          {detailLoading ? <p role="status" className="py-16 text-center text-gray-500">회원 기록을 불러오는 중…</p> : detailError ? <button onClick={() => { setNotice(null); void loadEntries(selected.id); }} className={buttonClass}><RefreshCw className="h-4 w-4" />다시 불러오기</button> : (
            <>
              <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
                {[
                  { label: "대상 회원", value: `${summary.count}명`, hint: `납부 ${summary.paidCount}명 · 미납 ${summary.count - summary.paidCount}명` },
                  { label: "받을 총금액", value: won(summary.totalAmount), hint: "전체 대상 회원 기준" },
                  { label: "받은 금액", value: won(summary.paidAmount), hint: "납부 O 회원 합계" },
                  { label: "미납 금액", value: won(summary.totalAmount - summary.paidAmount), hint: "납부 X 회원 합계" },
                ].map(item => <div key={item.label} className="rounded-xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-gray-900"><p className="text-xs text-gray-500">{item.label}</p><p className="mt-2 break-all text-xl font-black">{item.value}</p><p className="mt-1 text-xs text-gray-500">{item.hint}</p></div>)}
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <div className="relative min-w-36 flex-1"><Search className="absolute top-3 left-3 h-4 w-4 text-gray-400" /><input aria-label="체크리스트 회원 검색" placeholder="이름 검색" value={search} onChange={event => setSearch(event.target.value)} className={`${inputClass} pl-9`} /></div>
                <select aria-label="납부 상태 필터" value={filter} onChange={event => setFilter(event.target.value as typeof filter)} className={inputClass.replace("w-full", "w-28 shrink-0")}><option value="all">전체</option><option value="unpaid">미납 X</option><option value="paid">납부 O</option></select>
                <button aria-label="회원 기록 새로고침" disabled={busy} onClick={() => { setNotice(null); void loadEntries(selected.id); }} className={buttonClass}><RefreshCw className="h-4 w-4" /></button>
                {!selected.archived && <button disabled={busy || !available.length} onClick={() => setAddOpen(true)} className={buttonClass}><Users className="h-4 w-4" />회원 추가</button>}
              </div>
              <p className="text-xs text-gray-500">{visible.length}명 표시 · 납부 O/X를 누르면 바로 저장돼요. 주문 내용은 ‘수정’에서 입력하세요.</p>
              <div className="divide-y divide-gray-100 overflow-hidden rounded-2xl border border-gray-200 bg-white md:hidden dark:divide-gray-800 dark:border-gray-800 dark:bg-gray-900">
                {visible.map(entry => <article key={entry.id} aria-label={`${entry.player_name} 주문 내역`} className="space-y-3 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <div><h3 className="font-bold">{entry.player_name}</h3><p className="mt-1 text-sm tabular-nums text-gray-500">{won(entry.amount)}</p></div>
                    <div className="flex items-center gap-2"><span className="text-xs text-gray-500">납부</span><PaidButton entry={entry} disabled={selected.archived || busyIds.has(entry.id) || busyIds.has(selected.id)} saving={busyIds.has(entry.id)} onClick={() => void togglePaid(entry)} /></div>
                  </div>
                  <div className="flex items-center justify-between gap-3 border-t border-gray-100 pt-3 dark:border-gray-800">
                    <div className="min-w-0"><p className="break-all text-xs text-gray-500">{selected.input_label}</p><p className="mt-1 whitespace-pre-wrap break-all text-sm">{entry.content || <span className="text-gray-400">미입력</span>}</p></div>
                    <button aria-label={`${entry.player_name} 주문 정보 수정`} disabled={selected.archived || busy} onClick={() => setEditing(entry)} className="min-h-11 shrink-0 rounded-lg px-3 py-2 text-sm font-bold text-yellow-700 hover:bg-yellow-50 disabled:text-gray-400 disabled:opacity-50 dark:text-yellow-400 dark:hover:bg-yellow-950/30">수정</button>
                  </div>
                  {entry.memo && <p className="whitespace-pre-wrap break-all rounded-lg bg-gray-50 p-2 text-xs text-gray-500 dark:bg-gray-800">{entry.memo}</p>}
                </article>)}
                {!visible.length && <p className="py-12 text-center text-sm text-gray-500">조건에 맞는 회원이 없어요.</p>}
              </div>
              <div className="hidden overflow-x-auto rounded-2xl border border-gray-200 bg-white md:block dark:border-gray-800 dark:bg-gray-900">
                <table className="w-full min-w-[660px] text-left text-sm">
                  <caption className="sr-only">{selected.title} 회원별 주문 및 납부 내역</caption>
                  <thead className="border-b border-gray-200 bg-gray-50 text-xs text-gray-500 dark:border-gray-800 dark:bg-gray-800/60"><tr><th scope="col" className="px-4 py-3">회원</th><th scope="col" className="max-w-48 break-all px-4 py-3">{selected.input_label}</th><th scope="col" className="px-4 py-3">금액</th><th scope="col" className="px-4 py-3">납부</th><th scope="col" className="px-4 py-3">메모</th><th scope="col" className="px-4 py-3"><span className="sr-only">수정</span></th></tr></thead>
                  <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
                    {visible.map(entry => <tr key={entry.id} className="hover:bg-gray-50/70 dark:hover:bg-gray-800/40">
                      <th scope="row" className="whitespace-nowrap px-4 py-3 font-bold">{entry.player_name}</th>
                      <td className="max-w-64 whitespace-pre-wrap break-all px-4 py-3">{entry.content || <span className="text-gray-400">미입력</span>}</td>
                      <td className="whitespace-nowrap px-4 py-3 tabular-nums">{won(entry.amount)}</td>
                      <td className="px-4 py-3"><PaidButton entry={entry} disabled={selected.archived || busyIds.has(entry.id) || busyIds.has(selected.id)} saving={busyIds.has(entry.id)} onClick={() => void togglePaid(entry)} /></td>
                      <td className="max-w-52 whitespace-pre-wrap break-all px-4 py-3 text-gray-500">{entry.memo || "—"}</td>
                      <td className="px-4 py-3"><button aria-label={`${entry.player_name} 주문 정보 수정`} disabled={selected.archived || busy} onClick={() => setEditing(entry)} className="whitespace-nowrap rounded-lg px-3 py-2 font-bold text-yellow-700 hover:bg-yellow-50 disabled:text-gray-400 disabled:opacity-50 dark:text-yellow-400 dark:hover:bg-yellow-950/30">수정</button></td>
                    </tr>)}
                    {!visible.length && <tr><td colSpan={6} className="py-12 text-center text-gray-500">조건에 맞는 회원이 없어요.</td></tr>}
                  </tbody>
                </table>
              </div>
            </>
          )}
        </>
      ) : <div className="space-y-3"><p>목록 정보를 불러오지 못했어요.</p><button className={buttonClass} onClick={() => setSelectedId(null)}>목록으로 돌아가기</button></div>}

      {createOpen && <CreateDialog players={roster} onClose={() => setCreateOpen(false)} onCreated={async id => {
        setCreateOpen(false);
        setScope("active");
        const loaded = await loadLists();
        if (loaded) { openList(id); setNotice({ kind: "success", message: "체크리스트를 만들었어요." }); }
      }} />}
      {editing && selected && <EntryDialog entry={editing} checklist={selected} onClose={() => setEditing(null)} onSaved={entry => { replaceEntry(entry); setEditing(null); setNotice({ kind: "success", message: `${entry.player_name} 님의 주문 정보를 저장했어요.` }); }} />}
      {addOpen && selected && <AddMembersDialog players={available} checklistId={selected.id} onClose={() => setAddOpen(false)} onSaved={() => { setAddOpen(false); void loadEntries(selected.id); setNotice({ kind: "success", message: "대상 회원을 추가했어요." }); }} />}
    </section>
  );
}
