# PM Core — Phần lõi dùng chung của `/pm-code` và `/pm-doc`

> [!IMPORTANT]
> Không phải slash command. Cả hai lane nạp file này ở Bước 0. **SSOT là `.agent/workflows/`**; mirror ở `.claude/commands/` chỉ khác cú pháp `/opsx:` thay `/opsx-`. Sửa quy tắc điều phối → sửa **tại đây**, không sửa trong từng lane.
>
> Đọc theo yêu cầu, **không** nạp đầu run: `pm-orca.md` (khi sắp dispatch lô Orca), `pm-evidence.md` (số đo đằng sau mọi hằng số — khi chất vấn hoặc cần cập nhật một con số).

Khung 6 bước chung: **Intake & Triage → Analysis fan-out → GATE → Planning artifacts → Implementation → Verification & Close**. Lane chỉ khác ở ngữ nghĩa triage (Bước 1), loại artifact (Bước 4), roster agent (Bước 5) và cách đóng run (Bước 6).

---

## Nguyên tắc bất biến

1. **BẠN là PM.** Vai trò do main loop đảm nhiệm, không delegate cho subagent `product-manager` (nó không có Agent lẫn Bash). Không cần nạp role file hay role memory — việc ở đây là điều phối.
2. **Subagent không spawn được subagent.** Mọi dispatch do BẠN làm; không viết prompt kiểu "hãy spawn thêm agent".
3. **Kênh hai chiều là `SendMessage`.** Worker báo bằng *Worker Contract* trong final message. Worker `BLOCKED` → BẠN quyết rồi `SendMessage` trả lời **đúng agent đó** — context của nó giữ nguyên, không respawn. Chỉ dispatch worker MỚI kèm handoff note khi worker đã trả `PARTIAL` vì chạm trần: lúc đó context của nó chính là phần đắt.
4. **Đúng MỘT gate phê duyệt** (Bước 3), trước mọi thao tác ghi ngoài run-state. Gọi `/pm-code` hoặc `/pm-doc` đã bao hàm phép ghi vào `docs/010-Planning/pm-runs/<run-id>/`.

**Runtime dispatch** mặc định là **Agent tool** (subagent in-process, chạy nền — đợi notification, không đoán kết quả). Có `ORCA_TERMINAL_HANDLE` trong env, `orca status --json` trả ready, **và** anh muốn dùng → đọc `pm-orca.md` trước lô Orca đầu tiên. Không thoả → im lặng dùng Agent, không cần báo.

---

## Run-state

`docs/010-Planning/pm-runs/<run-id>/`, với `run-id` = `$(date +%F)-<slug-kebab-case>`. Schema từng file: `docs/010-Planning/pm-runs/README.md` — đọc trước khi ghi file đầu tiên.

| File | Khi nào | Ai ghi |
|---|---|---|
| `brief.md` | Mọi tier | PM |
| `run-plan.md` | Từ T1 | PM |
| `tasks.md` (code, trong `openspec/`) / `outline.md` (doc) | Từ T1 | **PM độc quyền tick** |
| `findings/<role>.md` | T2, T3 | Mỗi lens tự ghi file của mình |
| `escalations.md` | Khi có escalation đầu tiên | PM, append-only |
| `verdict.md` (+ `verdict-<pass>.md`) | Từ T1 | Pass verify ghi, PM tổng hợp |
| `cost.md` | Từ T1 | PM |

`brief.md` ghi ngay dưới Triage: **`Lane: code | doc`** và **`Runtime: agent | orca`** (chính sách mặc định của run; runtime thật từng lô nằm ở cột `Runtime` của `run-plan.md`). Lô Orca ghi thêm `Model`, `run_id`, `Worktree` theo `pm-orca.md`.

---

## Triage — khung chung

Chấm **4 câu hỏi**, mỗi câu Có = 1 điểm, ghi lý do từng câu vào `brief.md`. Nội dung Q1–Q4 do lane định nghĩa.

**Q4 là tie-breaker, không phải câu độc lập**: chỉ tính điểm khi Q1 hoặc Q2 = Có. Khối lượng lớn gói trong một domain và không đổi contract là việc *nhiều*, không phải *phức tạp* — cần một worker làm lâu, không cần fan-out. Vẫn ghi đáp án thật kèm "không tính điểm".

| Điểm | Tier | Đường đi |
|---|---|---|
| 0 | **T0** | PM tự làm, 0 spawn. Bỏ Bước 2 và 4. |
| 1 | **T1** | 1 worker. Bỏ Bước 2. |
| 2 | **T2** | Fan-out → thực thi → verify bởi agent khác. Đủ 6 bước. |
| 3–4 | **T3** | Full path + artifact mở rộng + close-step đầy đủ. |

Phân vân giữa hai tier → chọn **thấp hơn**, ghi điều kiện escalate vào `brief.md`. Yêu cầu mơ hồ tới mức không chấm nổi → **AskUserQuestion** ngay tại Bước 1 — điểm duy nhất được hỏi trước gate.

---

## Bước 2 — Analysis fan-out (T2, T3) — khung chung

- Chọn lens theo bảng tín hiệu của lane; **chỉ lens thực sự cần** — mỗi lens thừa là một lần nạp lại toàn bộ context.
- **Dispatch tất cả lens trong MỘT message.** Mỗi lens sở hữu **đúng một file** `findings/<role>.md`; ngoài file đó read-only tuyệt đối (không chạm deliverable, `brief.md`, findings của lens khác).
- Lens tự ghi mục *Kết luận của worker*. PM **không transcribe**, chỉ append *PM đọc được gì* + *Mâu thuẫn với lens khác*.
- Hai lens mâu thuẫn → PM phân xử, ghi `brief.md` §Assumptions; không đủ cơ sở → đưa lên gate cho anh quyết.

---

## GATE (Bước 3 — bắt buộc, đúng một lần)

Viết `run-plan.md`, rồi trình anh **trong một lượt** và chốt bằng **AskUserQuestion**:

- **Lane, Tier**, điểm Q1–Q4 + lý do.
- **Runtime** mặc định. Có lô Orca: model + worktree đã pin, runtime từng lô, đã chạy *Precondition checklist* của `pm-orca.md`.
- **Model từng lô** — cột `Model` của `run-plan.md` (mục *Chọn model cho từng lô*).
- **Tóm tắt phân tích** ≤5 dòng + mâu thuẫn chưa phân xử (nếu có Bước 2).
- **Run plan**: phase, agent nào làm gì, phase nào song song.
- **File ownership map**: các tập **rời nhau tuyệt đối**. Không cắt rời được → 1 worker, nhưng vẫn cắt việc thành nhiều lô tuần tự.
- **Kế hoạch dispatch theo lô**: mỗi lô gồm gì, worker nào, tuần tự/song song, **ngân sách tool call** — kể cả lô verify read-only. Lô vượt ~3–5 file là dấu hiệu cắt chưa đủ nhỏ.
- **Ước lượng token — bắt buộc, một dòng, quy ra % session**:

  ```
  Ước lượng: Σ(ngân sách lô × hệ số lane) = <N>M token ≈ <X>% session 5h
  Hệ số: lane code 0.11–0.23M/call · lane doc 0.25M/call (pm-evidence.md)
  + chi phí PM (~30–50% run) + dự phòng 1 fix round
  ```

  Tool call là đơn vị để *chặn* worker; token quy ra % session là đơn vị duy nhất anh *quyết định* được. Lệch thực tế >50% → ghi lý do vào `cost.md`.
- **Artifact sắp tạo/sửa** ngoài run-state.
- **Assumptions** đang đi theo, và điều gì hỏng nếu sai.

Anh duyệt → chạy thẳng tới hết, không hỏi lại trừ *Escalation* tầng 3. Run-state trên đĩa là điểm resume: anh có thể gõ `/compact` ngay sau gate mà không mất gì.

---

## Chọn model cho từng lô

Quota session tính theo model → chọn model là quyết định chi phí thật, hiện ở cột `Model` của `run-plan.md` và truyền vào param `model` của Agent tool. Chọn theo **cách phần việc có thể sai**, không theo "việc nhỏ thì model nhỏ" (model yếu cần nhiều turn hơn cho việc cần judgment → vừa đắt hơn vừa tệ hơn):

| Phần việc có thể sai vì… | Model |
|---|---|
| Bỏ sót một mục trong danh sách: inventory, bảng call-site, sweep có pattern rõ, áp template | `haiku` |
| Prose khi outline + *Nguồn sự thật* đã chốt; verify theo checklist tường minh | `sonnet` |
| Suy luận lệch: kiến trúc, đổi contract/schema/taxonomy, phân xử mâu thuẫn, Coherence, Correctness-nội-dung | `opus` |

- Default nằm ở `.claude/agents/<role>.md` (`model:`). Role không khai thì **thừa hưởng model của PM** — mặc định im lặng và đắt. Quyết định per-dispatch ghi ở `run-plan.md`; cố ý dùng mặc định thì ghi `default`, không để trắng.
- Đổi model giảm giá mỗi token, **không giảm số token**. Trần tool call và `Độ dài đích` mới là thứ cắt token.

---

## Worker Contract

Mọi worker kết thúc final message bằng đúng khối này (nêu yêu cầu trong prompt):

```
STATUS: DONE | BLOCKED | PARTIAL
FILES_TOUCHED: <đường dẫn — phải nằm trong ownership; "none" nếu read-only>
SUMMARY: <3-5 dòng kết quả thực tế>
QUESTION / OPTIONS (A/B/C + trade-off) / RECOMMEND: <chỉ khi BLOCKED>
```

`PARTIAL` = xong một phần, kèm **handoff note**: đã xong tới đâu, đã ghi file nào, working tree đang ở trạng thái nào, bước kế, cạm bẫy đã thấy. Thiếu dữ liệu → `BLOCKED`/`PARTIAL`, **không bịa để lấp**. Lô Orca dùng contract khác — `pm-orca.md`.

### Ngân sách mỗi dispatch

Worker tự đếm **tool call** của mình. Lane code: **60 + 15 cho mỗi spec phải mutation-test**. Lane doc: bảng *Trần lane doc* trong `pm-doc.md` — một call lane doc đắt ~2× lane code, **không bê 60 sang**. PM ghi con số vào `[BUDGET]`. Chạm trần mà chưa xong → `PARTIAL` + handoff note; PM dispatch worker mới với note đó dán vào `[SCENE]`.

> [!WARNING]
> **Ngân sách không bao giờ là lý do hạ chuẩn.** Chạm trần thì dừng và `PARTIAL` — không cắt kiểm chứng, không bỏ mutation test, không `DONE` cho kịp trần. `PARTIAL` là kết quả hợp lệ; `DONE` chưa kiểm chứng thì không.

Ba stop rule cứng, nêu trong `[TASK]`:

- **Full test suite tối đa 1 lần mỗi dispatch**; mọi lần khác `jest <path>`. PM bù bằng cách chạy full suite giữa các lô — luôn `2>&1 | tail -n 40` (hoặc summary reporter) để output không nằm lại trong context PM.
- **Hai lần sửa hỏng liên tiếp cùng một test → `BLOCKED`**, không có lần ba.
- **Không `PARTIAL` giữa một mutation test.** Restore trước, `grep` xác nhận, rồi mới `PARTIAL`; ngân sách luôn chừa 3 call cho việc đó.

### Verify cũng phải cắt lô

Áp cả hai lane. **Ngân sách áp mọi tier; cắt pass chỉ từ T2.** T0/T1 có tối đa một lô verify (xem từng lane) nên không có gì để cắt — cắt pass trên deliverable nhỏ thì *nhân* chi phí (mỗi pass trả lại overhead spawn + đọc lại cùng deliverable).

- Mỗi pass một dispatch, ngân sách riêng, **thật sự rời nhau** — hai pass cùng đọc lại một bộ file là nhân đôi, không phải cắt. Read-only → dispatch song song trong một message.
- Mỗi pass sở hữu đúng một file `verdict-<pass>.md`; PM tổng hợp thành `verdict.md`.
- **Verdict mở đầu bằng bảng tóm tắt ≤20 dòng** (pass · tiêu chí · PASS/FAIL/WARNING · một dòng lý do). PM chỉ đọc bảng, đọc xuống thân cho mục `CRITICAL`. Nêu yêu cầu này trong `[TASK]`.
- Full test suite chạy **một lần cho cả Bước 6**, PM chạy rồi dán kết quả vào `[CONTEXT]`.

---

## Dispatch Prompt Template

```
[SCENE] <yêu cầu gốc 2-3 dòng> — phần việc này khớp vào đâu
[TASK] <TOÀN VĂN phần việc của đúng lô này — không phải con trỏ tới plan, không kèm lô khác>
[OWNERSHIP] Em CHỈ được ghi: <file/thư mục>. Ngoài phạm vi → BLOCKED.
[CONTEXT] Đọc tham chiếu: <đường dẫn artifact lớn — chỉ phần này dùng path>
[CONSTRAINTS] <read-only? không đổi contract? pattern nào? rule tình huống nào — nêu tên file, không dán nguyên văn>
[BUDGET] <N> tool call. Chạm trần → PARTIAL + handoff note. Ngân sách không phải lý do hạ chuẩn.
[CONTRACT] Kết thúc bằng khối STATUS / FILES_TOUCHED / SUMMARY (+ QUESTION/OPTIONS/RECOMMEND nếu BLOCKED).
```

Persona đã nằm trong `.claude/agents/<role>.md`, anti-hallucination đã nằm trong `.claude/rules/` (auto-load vào mọi subagent) — **không lặp lại trong prompt**. Biến thể Orca (thêm `[ACCEPT]`, bỏ `[CONTRACT]`): `pm-orca.md`.

---

## Escalation Protocol — 3 tầng

| Tầng | Điều kiện | Hành động |
|---|---|---|
| 1 | Worker vướng | Trả `BLOCKED` + QUESTION/OPTIONS/RECOMMEND, rồi kết thúc. |
| 2 | Câu hỏi trong phạm vi `brief.md` | PM tự quyết, ghi `escalations.md`, **`SendMessage` trả lời đúng agent đó**. |
| 3 | Vượt brief (đổi scope, ưu tiên, đánh đổi business) | **AskUserQuestion** kèm OPTIONS + khuyến nghị của PM. Ghi `escalations.md`. |

Đây là ngoại lệ hợp lệ duy nhất của quy tắc một gate. Lane Orca dùng `ask`/`reply` native cho tầng 1–2 — `pm-orca.md`.

---

## Guardrails

- **Không spawn khi việc nhỏ hơn overhead spawn (~27k token)** — lý do T0 tồn tại. Nhưng càng về sau run, một turn inline của PM (context đã phình) đắt hơn một turn của worker mới — không viện "tiết kiệm spawn" để PM ôm việc dài.
- **Chi phí một agent tăng siêu tuyến tính theo số turn (~`turns^1.74`)** → cắt lô là đòn bẩy token lớn nhất: mỗi worker một lô, không phải cả feature. Worker xong lô thì trả về; lô kế là worker mới.
- **PM cũng bị luật đó** — PM đã đo chiếm 37–52% chi phí run. PM đọc `SUMMARY` + `FILES_TOUCHED`, không đọc lại file worker vừa ghi; cần kiểm độc lập → dispatch verify pass context sạch (ngoại lệ: deliverable nhỏ T0 lane doc — `pm-doc.md`). Không dùng `fork` làm worker: nó kéo theo toàn bộ context PM.
- **Không dispatch song song hai worker có giao file ownership.** Không cắt rời được thì một worker.
- **File theo dõi tiến độ do PM độc quyền tick**, và **chỉ tick sau khi đối chiếu `FILES_TOUCHED`** với ownership đã cấp. File lạ → vi phạm, ghi `escalations.md`, đánh giá tác động trước khi đi tiếp.
- **Đã delegate thì không tự làm lại song song.** Đợi notification; không đoán kết quả của agent đang chạy.
- **Verify phải do agent KHÁC agent đã thực thi.**
- **Không tuyên bố xong khi verdict còn CRITICAL.** Báo trung thực phần chưa xong.
- **Không nhảy tier ngầm** — đổi tier: ghi `escalations.md` + báo anh. **Không đổi lane giữa chừng** — sai lane: dừng, báo anh, chạy lại bằng command đúng; run-state cũ giữ làm dấu vết.

---

## Close-step — `cost.md` (từ T1)

Bảng, không narrative. Số cộng từ `.message.usage` trong `~/.claude/projects/<slug>/<session>.jsonl` (main loop) và `<session>/subagents/*.jsonl` — đo, không nhớ:

- PM main loop: turns, `cache_read`, ctx/turn.
- Mỗi lô: tool call, turns, `cache_read` — xếp giảm dần.
- Tổng run, tỷ lệ PM / subagent; lô vượt ngân sách (bao nhiêu, vì sao); số lô thực tế vs plan; **ước lượng ở gate vs thực tế**.

Hằng số lệch đáng kể so với giá trị đang dùng → cập nhật trong cùng run, cả chỗ dùng lẫn `pm-evidence.md` kèm ghi chú run. Run có lô Orca: nguồn số theo `pm-orca.md`.

---

## Output — báo cáo kết thúc run

- **Run**: `<run-id>` — lane, runtime, tier, số agent spawn, số escalation.
- **Đã làm**: deliverable kèm đường dẫn.
- **Verdict**: kết quả, WARNING/SUGGESTION còn nợ.
- **Chi phí**: tổng, PM / subagent, lô vượt ngân sách, ước lượng vs thực tế → `cost.md`. Có lô Orca: token Claude worker tiêu thụ, số lô đạt lần đầu / làm lại / fallback.
- **Nợ lại**: phần cắt scope hoặc hoãn, kèm lý do.
- **Run-state**: `docs/010-Planning/pm-runs/<run-id>/`.
