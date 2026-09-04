# PM Evidence — Số đo đằng sau các guardrail

> [!IMPORTANT]
> File này **không phải slash command** và **không có bản mirror** ở `.claude/commands/`. Nó là đích của một lệnh Read, chỉ nạp trong hai tình huống:
> 1. **Close-step**, khi số đo của run mới lệch đáng kể so với hằng số đang dùng và cần cập nhật.
> 2. Khi ai đó — anh, hoặc chính BẠN — **chất vấn một con số** trong `pm-core.md` / `pm-orca.md`.
>
> Không đọc file này ở đầu run. Hằng số cần dùng đã nằm sẵn trong hai file kia.

Mọi số dưới đây là số **đo được từ transcript thật**, không phải ước lượng. Mục này tồn tại vì thiếu nó: con số overhead spawn **"5–6k"** từng sống rất lâu trong `pm-core.md` trước khi phát hiện nó **sai gần 4 lần**. Hằng số trần trụi, không nguồn, là thứ người sau sẽ "tối ưu" đi mất.

---

## Overhead một lần spawn — ~23.6k token

Trung vị context turn đầu của **60 subagent transcript**. Main loop khởi điểm ~63k.

Con số gồm: system prompt + tool schema + global/project `CLAUDE.md` + `.claude/rules/*.md` + agent definition + prompt dispatch.

**Cảnh báo về độ tươi**: đo **trước** đợt rút rule khỏi auto-load ngày `2026-08-22` (`clickup-mcp-formatting`, `learning-loop`, nửa meta của `mindset` → `.agent/rules/`; xem Rule Index trong `CLAUDE.md`), nên dự đoán lúc đó là thực tế sẽ **thấp hơn ~1.5k**.

**Đo lại run `2026-09-03` — dự đoán đó SAI, con số đi theo chiều ngược lại**: hai `software-engineer` khởi điểm **26,721** và **28,613** token, tức **cao hơn** mốc 23.6k khoảng 15%, dù rule auto-load đã bị rút bớt. Việc rút rule tiết kiệm được ít hơn phần mà system prompt + tool schema phình thêm. **Mốc dùng hiện nay: ~27k.**

Bài học phương pháp: một hiệu chỉnh *suy ra* ("rút rule ⇒ nhẹ hơn ~1.5k") không phải một phép đo, và ở đây nó lệch cả về dấu. Đừng ghi hiệu chỉnh suy diễn vào file này mà không đo.

Đo lại bằng `cache_read` + `cache_creation` của turn đầu trong `~/.claude/projects/<slug>/<session>/subagents/*.jsonl`.

→ Đây là lý do **T0** tồn tại: phần việc nhỏ hơn ~27k thì spawn là lỗ.

## Chi phí tăng siêu tuyến tính theo turn — `turns^1.74`

Đo trên **142 subagent transcript**:

| turns trung bình | cache_read trung bình / agent |
|---|---|
| 33 | 1.5M |
| 144 | 18.4M |
| 382 | 90.9M |
| 621 | 252.8M |

Lý do: context của agent tự phình theo từng turn, và **mỗi turn phải trả tiền cho toàn bộ context đã tích luỹ**. Một agent 621 turns đắt gấp **165 lần** một agent 33 turns, dù chỉ chạy dài gấp 19 lần.

**Hệ quả — số học của việc cắt lô**: 1 worker × 382 turns ≈ 90.9M, so với 4 worker × ~95 turns ≈ 38M — **rẻ hơn 58%**, đổi lại chỉ tốn thêm 3 × 23.6k overhead spawn (0.07M, không đáng kể).

**Hệ quả cho triage**: overhead spawn chỉ đắt khi so với việc *ngắn*. Càng về sau một run dài, một turn inline của PM (context đã phình) càng đắt hơn một turn của worker mới (context sạch) — đừng viện "tiết kiệm spawn" để PM tự ôm việc dài.

## Vì sao ngân sách là 60 tool call, không phải 50

Cắt lô **không miễn phí**. Đo 12 subagent của run `2026-08-22`: **15 turn đầu của mọi agent tốn ~0.37M token**, đồng đều đến mức đáng ngạc nhiên (0.31–0.40M). Đó là giá cố định mỗi lần cắt.

| Tình huống | Tiết kiệm | Phải trả | Kết luận |
|---|---|---|---|
| Cắt lô 171-call thành hai | ~8.8M | 0.37M | lãi đậm |
| Cắt lô 56-call tại mốc 50 | ~0.1M | 0.37M + 1 spawn | **lỗ** |

Break-even nằm quanh **60–70 call**. Đặt 60 vẫn chặn được cả hai runaway đã quan sát (90 và 105 call) mà không cắt oan nhóm giữa.

→ **Hạ con số này xuống dưới 60 là biến trần thành thứ tự nó gây tốn kém.**

## Vì sao đơn vị là tool call, không phải số file

Đo trên **15 subagent** của run `2026-08-22-google-account-set-password`: thứ hạng theo tool call trùng gần khít thứ hạng chi phí.

| tool call | chi phí |
|---:|---|
| 105 | 18.9M |
| 90 | 26.5M |
| 56 | 7.3M |
| 16–46 | 1.1–5.0M |

Trong khi đó lô đắt thứ nhất **chỉ chạm ~3 file** — nằm gọn trong trần *"3–5 file"* cũ mà vẫn đốt 18.9M.

→ Trần tính bằng file **không tương quan** với thứ phải trả tiền. Số file vẫn hữu ích để *cắt* lô; nó chỉ không dùng được để *chặn*.

## Lô verify là chỗ đắt nhất, và lâu nay không có gì chặn

Cùng run `2026-08-22-google-account-set-password`: một lô verify duy nhất chạy **90 tool call / 164 turn / 26.5M token — 19% chi phí toàn run**, đắt hơn mọi lô implementation.

Nguyên nhân: verify read-only nên heuristic *"3–5 file"* rỗng nghĩa với nó. Trần cũ đếm file *được ghi*, mà lô này không ghi file nào.

→ **Ngân sách tool call áp cho mọi dispatch, kể cả read-only.**

## PM main loop chiếm 37–52% tổng chi phí

Run `2026-08-22`: **326 turn × 161k context/turn = 52.4M** → 37% tổng run — đắt hơn bất kỳ subagent nào trong run.

Run `2026-09-03` (T1, chỉ 2 lô): **103 turn × 158k context/turn = 17.03M** → **51.9%** tổng run 32.83M. Tỷ lệ *cao hơn* dù run nhỏ hơn nhiều.

**Vì sao tier thấp lại tệ hơn về tỷ lệ**: ít lô nghĩa là ít cơ hội để luật "checkpoint sau mỗi 4 lô" kích hoạt, nên context PM chạy suốt run mà không bị vứt lần nào. Run 2026-09-03 còn bỏ luôn **checkpoint sau GATE** — vốn là vô điều kiện. Kết luận đưa vào `pm-core.md`: **tier thấp không miễn checkpoint.**

Mục này tồn tại vì nó từng bị bỏ sót: mọi guardrail ban đầu đều nhắm vào subagent. PM viết ra luật rồi tự miễn trừ cho mình.

## Cắt lô sai — số liệu run `2026-09-03`

Bằng chứng trực tiếp cho luật `turns^1.74`, đo trên hai lô cùng role, cùng repo, cùng run:

| Lô | Turns | Tool call | Tổng token | ctx/turn |
|---|---|---|---|---|
| Lô 1 — extract sang `lib/` | 39 | 18 | 2.05M | 46,311 |
| Lô 2 — viết `sync.ts` + đăng ký + README | 109 | 61 | **13.75M** | **121,100** |

Tỷ lệ turn 2.8× → tỷ lệ chi phí **6.7×**. Dự đoán theo `turns^1.74` là 5.98× (exponent thực của run này ≈ **1.85**). Luật giữ đúng về bản chất; không sửa 1.74 vì nó đo trên 142 transcript, n=2 ở đây không đủ để lật.

**Đường cắt đã nằm ngay trước mắt mà PM bỏ qua**: `tasks.md` vốn chia lô 2 thành ba nhóm (quét/dựng kế hoạch — thi hành/trình bày — tài liệu). PM gộp cả ba vào một dispatch. `ctx/turn` xác nhận chẩn đoán: lô 2 phình từ 46k lên 121k mỗi turn, tức mỗi turn về sau phải trả tiền cho mọi file đã đọc và mọi output test đã chạy trước đó.

→ **Heuristic bổ sung**: nếu `tasks.md` đã tự chia phần việc thành nhóm, coi ranh giới nhóm là đường cắt lô mặc định. Gộp nhóm lại phải có lý do, và lý do "chúng liên quan nhau" là không đủ.

**Hệ quả**: cùng một việc kiểm chứng, 20 turn × 40k của worker mới rẻ hơn 20 turn × 161k của PM cuối run **gấp 4 lần**. Đó là lý do PM đọc `SUMMARY`/`FILES_TOUCHED` thay vì đọc lại file, và dispatch verify pass context sạch thay vì tự đọc.

**Checkpoint `/compact` là cơ chế đã kiểm chứng, không phải đề xuất trên giấy**: run `2026-08-22` compact giữa chừng rồi resume sạch, vì mọi trạng thái cần thiết đã nằm trong `docs/010-Planning/pm-runs/<run-id>/` chứ không nằm trong đầu PM. Run-state có giá trị đúng ở chỗ đó — nó làm cho context của PM trở thành thứ vứt đi được.

## Lane doc có hệ số chi phí riêng — run `2026-09-04-onboarding-step6-social-connect`

Đây là run làm phát sinh toàn bộ mục *Trần lane doc*, *Verify theo tier* và trần fix round trong `pm-doc.md`.

**Deliverable: MỘT file spec, 569 dòng (~20KB). Chi phí: 72.37M token.**

| Thành phần | Tool call | Turns | Token | % run |
|---|---:|---:|---:|---:|
| PM main loop | 55 | 110 | 19.36M | 26.8% |
| L1 writer `architect` — tạo spec | 63 | 101 | 14.17M | 19.6% |
| L2b verify **Correctness** | 29 | 71 | 7.48M | 10.3% |
| L2c verify **Coherence** | 27 | 66 | 6.55M | 9.1% |
| L2a verify **Completeness** | 24 | 59 | 4.02M | 5.6% |
| **L3 fix round 1** `architect` | 60 | 125 | **17.73M** | **24.5%** |
| L4 re-verify | 12 | 30 | 2.23M | 3.1% |
| L5 fix round 2 | 5 | 13 | 0.83M | 1.1% |
| **Tổng** | **275** | **575** | **72.37M** | 100% |

Phân bổ theo mục đích: **viết deliverable 19.6% · verify 28.0% · rework 25.6% · PM điều phối 26.8%**.
→ **Verify + rework = 53.6%, gấp 2.7× chi phí viết ra thứ mà anh đặt hàng.**

### Hệ số quy đổi: lane doc ~0.25M/call, gần gấp đôi lane code

| Lane | Run | M token / tool call |
|---|---|---|
| code | `2026-09-03` lô 1 (18 call / 2.05M) | 0.114 |
| code | `2026-09-03` lô 2 (61 call / 13.75M) | 0.225 |
| **doc** | writer (63 call / 14.17M) | **0.225** |
| **doc** | fix round 1 (60 call / 17.73M) | **0.296** |
| **doc** | verify (24–29 call / 4.02–7.48M) | **0.168–0.258** |

Nguyên nhân: một tool call lane doc là `Read`/`Write` markdown vài trăm dòng, hoặc `Read` một vùng code để xác minh khẳng định. Một tool call lane code thường là `grep`, `jest <path>`, hay một `Edit` nhỏ. Ở 60 call, lô lane doc = **14–18M**.

→ **Break-even 60–70 call vẫn đúng và không bị lật.** Nó trả lời *khi nào nên cắt lô*, không trả lời *trần đặt ở đâu*. Trần lane doc thấp hơn (30/20/20) là vì hệ số quy đổi khác, và nó chỉ hoạt động khi đi kèm hai thứ làm việc nhỏ lại thật: `Độ dài đích` và `Mức neo code = neo file`. Hạ trần đơn lẻ chỉ sinh ra chuỗi `PARTIAL`.

### Mỗi pass verify bắt được gì — cơ sở để bỏ nhóm máy móc

Bảng này là lý do `pm-doc.md` chia tiêu chí verify thành **nhóm máy móc** (không dispatch) và **nhóm judgment** (đáng trả tiền cho agent).

| Pass | Chi phí | Phán quyết | CRITICAL thật | Rule đầu vào ngăn được? |
|---|---:|---|---|---|
| L2a Completeness | 4.02M | PASS-WITH-WARNINGS | **0** | Phần lớn có |
| L2c Coherence + Connectivity | 6.55M | PASS-WITH-WARNINGS | **0** | Connectivity: có · Coherence: không |
| L2b Correctness | 7.48M | **FAIL** | **C1** (+ C2 ở mức WARNING, PM nâng) | **Không** |

**C1 — tầng NỘI DUNG của Correctness, judgment thật.** Spec viết *"`:29`/`:33`/`:38`/`:43` cần `false` để con số mới khớp bảng trên"*. Auditor mở `onboarding-progress.ts:74-77`, đọc logic, tính ra: `:38` (`canUse: true`, kỳ vọng `.toBe(1)`) với `false` cho ra **2** → đổ; `:43` tương tự → đổ. **Hai bài test sẽ đổ nếu SE gõ theo spec.**
Không rule nào ngăn được — đây không phải lỗi tuân thủ quy tắc mà là **lỗi lập luận**. Không `grep` nào bắt được — cần hiểu ngữ nghĩa của hàm.

**C2 — hygiene, `grep` một call.** Hai dòng `</content>` và `</invoke>` ở cuối deliverable (dòng 593–594), dấu vết tool-call từ vòng `Write` cuối của writer — hệ quả trực tiếp của vòng "viết dài rồi cắt" (697→594, xem mục *Độ dài deliverable*). Prompt writer khi đó đã 16KB đầy ràng buộc tường minh mà vẫn lọt: **đây không phải thứ agent cố ý vi phạm, nó là tai nạn cơ chế.**

→ Ba kết luận vào `pm-doc.md`:
1. **Nhóm máy móc** (Completeness / Connectivity / Correctness-neo / Hygiene) → rule ở prompt writer + **PM pre-check bằng `grep`, ~2–3 call**. 4.02M cho 0 CRITICAL là giá không đáng trả cho một agent.
2. **Không bỏ hẳn phần kiểm máy móc.** Rule giảm lỗi, `grep` bắt phần còn lại với chi phí gần bằng 0. C2 là bằng chứng rằng chỉ nhắc rule là chưa đủ.
3. **Correctness phải tách hai tầng.** Neo (`grep` được) ≠ nội dung (judgment). Gộp lại thì hoặc trả tiền cho agent làm việc của `grep`, hoặc kết luận sai rằng "Correctness là máy móc" rồi bỏ mất chỗ C1 sinh ra.

### Cắt pass verify ở tier thấp thì NHÂN chi phí, không chia

Triage run này chấm **0/4 → T0**. PM khai T1 tại gate. Thực tế: **7 dispatch**.

Ba pass verify song song trên một deliverable duy nhất → 18.05M, rồi ba verdict đó sinh ra **20.79M rework**. Mỗi pass phải trả lại overhead spawn (~27k), đọc lại cùng deliverable, và sinh thêm một verdict cho PM đọc.

**Verdict artifact: 111KB cho deliverable 20KB — 5.5×.** (`verdict-correctness` 36KB, `verdict-round2` 34.5KB, `verdict-coherence` 22.9KB, `verdict-completeness` 17.6KB.) PM đọc trọn chỗ đó ở 167k ctx/turn.

→ Kết luận vào `pm-core.md`: **cắt pass áp từ T2; ngân sách áp mọi tier.** Và verdict phải mở đầu bằng bảng tóm tắt ≤20 dòng.

### Vòng fix không có trần là runaway đắt nhất của lane doc

Fix round 1: **17.73M / 60 call / 125 turn — đắt hơn cả việc viết ra tài liệu (14.17M / 101 turn)**. Hai nguyên nhân, cả hai đều là lỗi thiết kế:

1. **Prompt nhồi cả 3 verdict** (14.2KB) thay vì chỉ các mục `CRITICAL`.
2. **Không phân mức finding** — `WARNING` và `SUGGESTION` được xử ngang `CRITICAL`, nên phạm vi fix gần bằng viết lại.

Rồi nó sinh tiếp re-verify (2.23M) + fix round 2 (0.83M). → Trần: **1 vòng, chỉ `CRITICAL`, 20 call**; re-verify chỉ soát mục đã sửa, 10 call; vòng 2 phải qua AskUserQuestion.

### Model mặc định im lặng — hai role đắt nhất run đều chạy Opus 5

**Quota session tính theo model** — anh xác nhận `2026-09-04`. Nên model là một đòn bẩy chi phí độc lập với token, và nó bị bỏ quên hoàn toàn cho tới run này.

Kiểm `.claude/agents/*.md`: **8/12 agent không khai `model:`**, tức thừa hưởng model của PM (Opus 5). Trong đó có đúng hai role đắt nhất của run:

| Role | Chi phí trong run | Khai `model:`? |
|---|---:|---|
| `architect` (writer 14.17M + fix 17.73M + 0.83M) | **32.7M** | không → Opus 5 |
| `context-auditor` (3 verify pass + re-verify) | **20.3M** | không → Opus 5 |

→ `context-auditor` đặt default **`sonnet`** (remit của nó là liệt kê và đối chiếu). `architect` **giữ Opus** vì nó là role judgment — cùng run đó nó sửa lại hai khẳng định sai của PM (E1, E2) và tìm thêm 3 ripple point PM bỏ sót; đó chính là thứ mất đi khi hạ model. Quyết định per-lô vào cột `Model` của `run-plan.md`.

**Cảnh báo phương pháp**: đổi model **không giảm số token**, nó giảm giá mỗi token. Và model yếu hơn có thể cần nhiều turn hơn cho cùng việc — với `turns^1.74`, hạ model sai chỗ thì vừa đắt hơn vừa tệ hơn. Chọn theo *tính quyết định được của phần việc*, không theo kích cỡ. Bảng chọn: `pm-core.md` §*Chọn model cho từng lô*.

**Chưa đo**: chưa có run nào so `sonnet` với `opus` trên cùng phần việc verify. Run kế tiếp đổi **hai** biến một lúc (trần mới + model mới) nên số liệu sẽ bị nhiễu — ghi rõ điều đó vào `cost.md` thay vì gán toàn bộ phần giảm cho một nguyên nhân.

### Gate hiện tool call thì anh không thấy giá

`run-plan.md` trình ra gate: *"Tổng ngân sách ước lượng: 145 tool call"* — và được duyệt. 145 call × 0.25M ≈ **36M**, cộng PM và rework thành **72.37M**. Không mục nào ở gate nói ra con số đó.

Thực tế 220 call subagent so với 145 kế hoạch (**+52%**), và **toàn bộ phần vượt là fix/re-verify không có trong plan**.

→ Kết luận vào `pm-core.md` §GATE: **ước lượng token quy ra % session là bắt buộc**. Tool call là đơn vị để chặn worker; token là đơn vị duy nhất anh quyết định được bằng.

### Độ dài deliverable là biến nhân, và nó bị đặt sai nguồn

`outline.md` đặt target **350–550 dòng** vì tiền lệ cùng loại tài liệu ra **739 dòng** — trong khi anh yêu cầu nguyên văn *"nội dung chỉ cần đầy đủ để xây dựng, không cần quá chi tiết"*.

Writer viết **697 dòng rồi tự cắt còn 594** (chốt 569). Riêng vòng cắt ~20 tool call, và nó là phần làm lô vượt trần (63/60).

→ Hai kết luận: target suy từ **mức chi tiết anh yêu cầu**, không từ tiền lệ; và writer **viết đúng target ngay**, vì "viết dài rồi cắt" là trả tiền hai lần cho phần bị xoá.

### Ước lượng sau khi áp trần mới — CHƯA ĐO, cần run kế xác nhận

Cùng deliverable, áp: `Độ dài đích` 200 dòng · `neo file` · writer 30 call · **nhóm máy móc thành rule + PM pre-check** · 1 verify pass judgment 20 call · ≤1 fix round 20 call · re-verify PM-inline · PM compact sau GATE và sau verdict.

| Thành phần | Ước lượng | Cơ sở |
|---|---:|---|
| Writer | ~4.2M | 30 call ≈ 50 turn; 14.17M × (50/101)^1.74 |
| PM pre-check (nhóm máy móc) | ~0.5M | 2–3 tool call inline, thay cho 4.02M của một pass Completeness |
| Verify judgment (1 pass) | ~2.2M | Correctness-nội-dung + Coherence trên doc 200 dòng |
| Fix round (nếu có) | ~1.5M | 20 call, chỉ `CRITICAL` |
| Subagent cộng lại | ~7.9M | |
| PM (2 checkpoint + pre-check) | ~8M | **~50% tổng** — nằm trong biên đo được 37–52%; chưa dám hạ thấp hơn vì chưa có run nào đo PM *sau khi* compact đúng quy định |
| **Tổng** | **~16M** | **giảm ~78%** |

**Đây là ước lượng ngoại suy từ `turns^1.74`, không phải phép đo** — đúng loại suy diễn mà mục *Overhead một lần spawn* ở trên cảnh báo. Run `/pm-doc` kế tiếp phải đo lại và ghi số thật vào đây.

---

## Số riêng của lane Orca

### Subagent chiếm 63% tổng chi phí run

Đo run `2026-08-22`. Đây là **toàn bộ lý do lane Orca tồn tại**: đẩy 63% đó sang provider khác là đòn bẩy lớn hơn mọi tối ưu context cộng lại.

### Worker Orca `--agent claude` khởi động với 62.7k

`cache_read` 31.5k + `cache_creation` 31.2k — gấp **2.66×** subagent (~23.6k), vì nó là session CLI đầy đủ chứ không phải subagent bị cắt tool.

**Con số này chỉ có ý nghĩa khi worker là Claude.** Worker provider khác thì chi phí Claude bằng 0 và phép so này không dùng để quyết định gì.

### Chất lượng model — CHƯA ĐO

`google-antigravity/gemini-3.8-flash-high` mới chỉ được kiểm chứng ở mức **đường ống**: dispatch vào được, `ask`/`reply` chạy, `worker_done` settle, file ghi được. **Chất lượng output chưa có một phép đo nào.**

Đây là lý do vòng nghiệm thu + trần 1 redo trong `pm-orca.md` là bắt buộc, và lý do mọi pass verify ở lại lane Agent. Bảng *Nghiệm thu accounting* trong `cost.md` là chỗ số liệu này sẽ tích lại — sau vài run mới có cơ sở nới hay siết phạm vi Orca.

---

## Cập nhật file này

Close-step của mỗi run đo lại. Số nào lệch đáng kể so với hằng số đang dùng thì:

1. Sửa hằng số trong `pm-core.md` / `pm-orca.md`.
2. Sửa mục tương ứng ở đây, **ghi rõ đo ở run nào**.

Không sửa một chỗ mà quên chỗ kia — hằng số mất nguồn là hằng số sắp bị "tối ưu" sai.
