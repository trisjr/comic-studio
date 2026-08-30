# PM Core — Phần lõi dùng chung của `/pm-code` và `/pm-doc`

> [!IMPORTANT]
> File này **không phải slash command**. Nó là phần lõi bất biến được cả hai lane nạp vào.
> Lane code: `.claude/commands/pm-code.md`. Lane tài liệu: `.claude/commands/pm-doc.md`.
>
> Sửa quy tắc điều phối → sửa **tại đây**, không sửa trong từng command. Đó là lý do file này tồn tại.

Hai command chia nhau đúng bộ xương 6 bước: **Intake & Triage → Analysis fan-out → GATE → Planning artifacts → Implementation → Verification & Close**. Chúng chỉ khác nhau ở Bước 1 (ngữ nghĩa triage), Bước 4 (loại artifact sinh ra), Bước 5 (roster agent) và Bước 6 (cách đóng run). Mọi thứ dưới đây áp dụng cho cả hai, không có ngoại lệ.

---

## Nguyên tắc bất biến (đọc trước khi chạy Bước 1)

Bốn ràng buộc dưới đây xuất phát từ giới hạn thật của runtime. Vi phạm là workflow chết giữa chừng.

1. **BẠN là PM.** Vai trò Product Manager do chính main loop đảm nhiệm, KHÔNG được delegate cho subagent `product-manager`. Lý do: subagent đó chỉ có `Read, Glob, Grep, Edit, Write, SendMessage` — không có `Task` nên không spawn được ai, không có `Bash` nên không chạy được lệnh nào. Nạp persona PM từ `.agent/roles/product-manager.md` và role memory tại `knowledge-base/45-Role-Memory/product-manager/` trước khi bắt đầu.

2. **Subagent không spawn được subagent.** Không agent nào trong `.claude/agents/` khai tool `Task`. Mọi việc dispatch đều do BẠN thực hiện. Không viết prompt kiểu "hãy spawn thêm agent để…".

3. **Không dựa vào SendMessage hai chiều.** Worker báo cáo về BẠN bằng **structured verdict trong final message** (xem *Worker Contract*). Khi worker `BLOCKED`, BẠN quyết định rồi **dispatch worker MỚI** kèm câu trả lời — không cố trả lời ngược vào một agent đang chạy. SendMessage chỉ là tiện ích bổ sung, không phải cơ chế phụ thuộc.

4. **Đúng MỘT gate phê duyệt.** Đặt ở Bước 3, trước mọi thao tác ghi vào vùng deliverable. Việc anh gọi `/pm-code` hoặc `/pm-doc` đã bao hàm sự cho phép ghi **run-state** dưới `docs/010-Planning/pm-runs/<run-id>/` — đó là sổ tay làm việc của PM, không phải sản phẩm. Ngoài vùng đó, không ghi gì trước khi qua gate.

---

## Run-state

Cả hai lane dùng chung một gốc: `docs/010-Planning/pm-runs/<run-id>/`, với `run-id` = `<YYYY-MM-DD>-<slug-kebab-case-của-yêu-cầu>`. Lấy ngày bằng `date +%F`, không tự nhớ.

Schema đầy đủ từng file nằm ở `docs/010-Planning/pm-runs/README.md` — đọc nó trước khi ghi file đầu tiên.

Ghi thêm vào `brief.md` một dòng **`Lane: code | doc`** ngay dưới phần Triage. Về sau đọc lại run cũ mà không biết nó chạy bằng command nào thì run-state mất giá trị truy vết.

---

## Triage — khung chung

Chấm **4 câu hỏi**, mỗi câu trả lời Có (1 điểm) hoặc Không (0 điểm). Ghi rõ lý do từng câu vào `brief.md` — không chấm ngầm. Nội dung cụ thể của Q1–Q4 do từng lane định nghĩa.

| Điểm | Tier | Đặc trưng |
|------|------|-----------|
| 0 | **T0** | PM tự làm, 0 spawn. Bỏ qua Bước 2 và 4. |
| 1 | **T1** | 1 worker duy nhất. Bỏ qua Bước 2. |
| 2 | **T2** | Analysis fan-out → thực thi → verify bởi agent khác. Đủ 6 bước. |
| 3–4 | **T3** | Full path: đủ 6 bước + artifact mở rộng + close-step đầy đủ. |

**Quy tắc phân vân**: nếu lưỡng lự giữa hai tier, chọn tier **thấp hơn**. Escalate lên giữa chừng rẻ hơn nhiều so với chạy thừa cả full path. Ghi lại việc đã chọn thấp vào `brief.md` để lát nữa còn biết đường mà escalate.

Nếu yêu cầu mơ hồ tới mức không chấm nổi Q1–Q4, dùng **AskUserQuestion** làm rõ ngay tại Bước 1. Đây là điểm duy nhất được phép hỏi trước gate.

---

## GATE (Bước 3 — bắt buộc, đúng một lần)

Viết `docs/010-Planning/pm-runs/<run-id>/run-plan.md`, rồi trình bày gọn cho anh **trong một lượt duy nhất**:

- **Lane** + **Tier** đã chấm + điểm Q1–Q4 + lý do.
- **Tóm tắt phân tích** (nếu có Bước 2) — tối đa 5 dòng, kèm mâu thuẫn chưa phân xử nếu có.
- **Run plan**: danh sách phase, agent nào làm gì, phase nào song song.
- **File ownership map**: mỗi worker sở hữu tập file/thư mục nào. Các tập phải **rời nhau tuyệt đối (disjoint)**. Nếu không cắt được rời nhau → chỉ dùng 1 worker, nhưng vẫn cắt việc của nó thành nhiều **lô dispatch tuần tự** theo trần ở mục Guardrails.
- **Kế hoạch dispatch theo lô**: liệt kê từng lô — lô nào, gồm file/task nào, worker nào chạy, tuần tự hay song song, và **ngân sách tool call cấp cho lô đó** (60 + 15/spec mutation-test). Một lô vượt ~3–5 file là dấu hiệu cắt chưa đủ nhỏ. Kể cả lô verify read-only cũng phải có ngân sách. Đây là mục anh nhìn vào để biết run này sẽ tốn bao nhiêu — cộng tổng ngân sách các lô lại là ước lượng thô của cả run.
- **Danh sách artifact sắp tạo/sửa** ngoài vùng run-state.
- **Assumptions** BẠN đang đi theo, và điều gì sẽ sai nếu assumption đó sai.

Dùng **AskUserQuestion** để chốt. Sau khi anh duyệt, chạy thẳng tới hết — không hỏi lại trừ khi rơi vào *Escalation Protocol*.

---

## Worker Contract

Mọi agent được dispatch BẮT BUỘC kết thúc final message bằng đúng khối này. Nêu rõ yêu cầu đó trong prompt dispatch.

```
STATUS: DONE | BLOCKED | PARTIAL
FILES_TOUCHED: <danh sách đường dẫn — phải nằm trong ownership được cấp; ghi "none" nếu read-only>
SUMMARY: <3-5 dòng, kết quả thực tế đã làm được>
QUESTION: <chỉ điền khi BLOCKED — câu hỏi cụ thể, một vấn đề một câu>
OPTIONS: <chỉ khi BLOCKED — A / B / C kèm trade-off mỗi phương án>
RECOMMEND: <chỉ khi BLOCKED — chọn một, kèm lý do>
```

`PARTIAL` = làm được một phần, phần còn lại có lý do rõ ràng. Worker **không được** tự bịa để lấp chỗ thiếu — thiếu thì báo `BLOCKED` hoặc `PARTIAL`.

### Ngân sách mỗi dispatch

Worker tự đếm **số tool call** của chính mình. Ngân sách = **60 tool call cơ bản, cộng 15 cho mỗi spec phải mutation-test** (`.claude/rules/mindset.md`: backup → revert → chạy → restore → xác nhận ≈ 10–15 turn/spec). PM nêu con số cụ thể của lô đó ngay trong `[TASK]`.

> **Vì sao 60 chứ không phải 50.** Cắt lô không miễn phí: đo 12 subagent của run `2026-08-22`, **15 turn đầu của mọi agent tốn ~0.37M token**, đồng đều đến mức đáng ngạc nhiên (0.31–0.40M). Đó là giá cố định mỗi lần cắt. Cắt lô 171-call thành hai tiết kiệm ~8.8M — lãi đậm. Nhưng cắt một lô 56-call tại mốc 50 thì chỉ còn 6 call nữa là xong, tiết kiệm ~0.1M mà trả 0.37M + một spawn — **lỗ**. Break-even nằm quanh 60–70 call. Đặt 60 vẫn chặn được cả hai runaway đã quan sát (90 và 105) mà không cắt oan nhóm giữa. Hạ con số này xuống dưới 60 là biến trần thành thứ tự nó gây tốn kém.

Chạm trần mà việc chưa xong → trả `STATUS: PARTIAL` kèm **handoff note**: đã xong tới đâu, đã ghi file nào, **working tree đang ở trạng thái nào**, bước kế tiếp là gì, cạm bẫy nào phát hiện được. Không cố làm nốt. PM dispatch worker MỚI với handoff note đó dán nguyên văn vào `[SCENE]`.

> [!WARNING]
> **Ngân sách KHÔNG BAO GIỜ là lý do hạ chuẩn.** Chạm trần thì **dừng và báo `PARTIAL`** — tuyệt đối không cắt bớt kiểm chứng, không bỏ mutation test, không báo `DONE` cho kịp trần. Một worker bỏ verify để lọt ngân sách gây thiệt hại lớn hơn nhiều lần số token nó tiết kiệm: nó biến một lô đắt thành một lô **sai mà trông như đúng**. `PARTIAL` là kết quả hợp lệ và được mong đợi; `DONE` chưa kiểm chứng thì không.

**Ba stop rule cứng** — hai cái đầu là đường dẫn tới runaway đã quan sát được, cái thứ ba chặn một rủi ro đúng-sai do chính trần này sinh ra:

- **Full test suite tối đa MỘT lần mỗi dispatch.** Mọi lần chạy khác dùng `jest <path>` nhắm đúng file. Chạy cả suite là nạp hàng chục KB output vào context, rồi mỗi turn còn lại của worker đều phải trả tiền cho nó.
    - Cái giá phải trả của luật này: worker có thể làm hỏng một suite không liên quan mà không biết. **PM bù bằng cách chạy full suite giữa các lô, ngay TRƯỚC checkpoint `/compact`** — output to đùng đó bị vứt đi ngay khi compact, nên gần như miễn phí.
- **Hai lần sửa hỏng liên tiếp trên cùng một test → `BLOCKED`, không có lần thứ ba.** Vòng lặp sửa-thử-sửa là nơi turn count phát nổ mà tiến độ đứng yên.
- **TUYỆT ĐỐI không trả `PARTIAL` khi đang ở giữa một mutation test.** Protocol là backup → revert → chạy → **restore** → xác nhận. Dừng lại giữa `revert` và `restore` để lại working tree **đang cố tình hỏng**, và worker kế tiếp thừa hưởng nó như thể đó là code thật — đường ngắn nhất để ship code hỏng. Chạm trần giữa protocol thì **restore trước đã, rồi mới `PARTIAL`**; ngân sách luôn chừa 3 call cho việc đó. Handoff note phải nói rõ đã restore và đã `grep` xác nhận.

> **Vì sao đơn vị là tool call, không phải file.** Đo trên 15 subagent của run `2026-08-22-google-account-set-password`: thứ hạng theo tool call trùng gần khít thứ hạng chi phí (105 call → 18.9M; 90 → 26.5M; 56 → 7.3M; nhóm 16–46 call → 1.1–5.0M). Trong khi đó lô đắt thứ nhất chỉ chạm ~3 file — **nằm gọn trong trần "3–5 file" cũ mà vẫn đốt 18.9M**. Trần tính bằng file không tương quan với thứ phải trả tiền. Số file vẫn hữu ích để *cắt* lô; nó chỉ không dùng được để *chặn*.

## Dispatch Prompt Template

```
[SCENE] Bối cảnh: <yêu cầu gốc 2-3 dòng> — <tại sao phần việc này tồn tại, nó khớp vào đâu>
[ROLE] Em đóng vai <role>. Nạp .agent/roles/<role>.md.
[TASK] <TOÀN VĂN phần việc — không phải con trỏ tới file plan>
[OWNERSHIP] Em CHỈ được ghi: <danh sách file/thư mục>. Ngoài phạm vi này → báo BLOCKED.
[CONTEXT] Đọc tham chiếu: <đường dẫn artifact lớn — chỉ phần này mới dùng path>
[CONSTRAINTS] <ràng buộc: read-only?, không đổi contract?, phải theo pattern nào?>
[CONTRACT] Kết thúc bằng khối STATUS/FILES_TOUCHED/SUMMARY (+ QUESTION/OPTIONS/RECOMMEND nếu BLOCKED).
[ANTI-HALLUCINATION] Không đoán nội dung file hay API. Verify bằng Read/Grep trước khi khẳng định.
  Không rõ → báo BLOCKED, tuyệt đối không tự bịa giả định rồi đi tiếp.
```

## Escalation Protocol — 3 tầng

| Tầng | Điều kiện | Hành động |
|------|-----------|-----------|
| 1 | Worker gặp vướng | Trả `STATUS: BLOCKED` kèm QUESTION + OPTIONS + RECOMMEND. Dừng, không tự quyết. |
| 2 | Câu hỏi nằm trong phạm vi `brief.md` | PM tự quyết, ghi quyết định + lý do vào `escalations.md`, dispatch worker MỚI kèm câu trả lời inline. |
| 3 | Câu hỏi vượt brief (đổi scope, đổi ưu tiên, đánh đổi business) | PM hỏi anh bằng **AskUserQuestion**, kèm OPTIONS và khuyến nghị của PM. Ghi vào `escalations.md`. |

Đây là ngoại lệ hợp lệ duy nhất của quy tắc một gate.

---

## Guardrails

- **Không spawn khi phần việc nhỏ hơn overhead nạp context của agent đó.** Overhead một spawn = **~23.6k token** (đo thật, trung vị context turn đầu của 60 subagent transcript; main loop khởi điểm ~63k). Con số này đo **trước** đợt rút rule khỏi auto-load ngày 2026-08-22 (`clickup-mcp-formatting`, `learning-loop`, nửa meta của `mindset` → `.agent/rules/`, xem Rule Index trong `CLAUDE.md`), nên thực tế hiện nay thấp hơn ~1.5k. Đo lại bằng `cache_read` của turn đầu trong `~/.claude/projects/<slug>/<session>/subagents/*.jsonl` thay vì nhớ theo con số. Con số này gồm system prompt + tool schema + global/project CLAUDE.md + `.claude/rules/*.md` + agent definition + prompt dispatch. Đây là lý do T0 tồn tại. Đừng dùng lại con số "5–6k" từng ghi ở đây — nó sai gần 4 lần.
- **Chi phí một agent tăng theo số turn nó chạy, không theo số spawn — nhưng số mũ phụ thuộc việc trần có được thi hành hay không.** Đây là **hai chế độ**, đừng trích một cái rồi bỏ cái kia.

  **Chế độ A — trần KHÔNG được thi hành ⇒ siêu tuyến tính `turns^1.74`.** Đo trên 142 subagent transcript (run lane code, agent chạy tới 621 turn):

  | turns trung bình | cache_read trung bình / agent |
    |---|---|
  | 33 | 1.5M |
  | 144 | 18.4M |
  | 382 | 90.9M |
  | 621 | 252.8M |

  Lý do: context của agent tự phình theo từng turn, và **mỗi turn phải trả tiền cho toàn bộ context đã tích luỹ**. Một agent 621 turns đắt gấp 165 lần một agent 33 turns, dù chỉ chạy dài gấp 19 lần.

  **Chế độ B — lô ĐƯỢC CẮT NGẮN ⇒ gần TUYẾN TÍNH.** Đo trên 46 subagent của run `2026-08-28-phase-2-architecture-design-comic-studio` (lane doc): hồi quy log-log cho **`k = 0.94`, `R² = 0.50`** (bỏ outlier: `k = 0.92`). Chi phí mỗi turn **gần như hằng số** qua mọi nhóm kích thước:

  | nhóm | số lô | $ / turn |
  |---|--:|--:|
  | < 50 turns | 4 | 0.119 |
  | 50–89 | 26 | 0.122 |
  | 90–129 | 13 | 0.110 |
  | ≥ 130 | 3 | 0.110 |

  ⭐ **Cơ chế là VIỆC CẮT LÔ, ⛔ không phải việc thi hành trần** — phân biệt này quan trọng, đừng đọc lướt. Lô kết thúc trước khi context kịp phình quá ~200k (`p50` 106k, `p90` 199k), nên mỗi turn trả tiền cho một context nhỏ và gần như không đổi. ⚠️ **Bằng chứng quyết định**: cả **3 lô của nhóm ≥130 turn đều VƯỢT trần** (77, 77, 160 tool call) mà `$/turn` vẫn **thấp nhất bảng** (0.110). Tuyến tính giữ được **ngay cả trong các lô phá trần** ⇒ trần chỉ là **tín hiệu dừng**; thứ thực sự bẻ đường cong là **cắt lô**.

  `R² = 0.50` nghĩa là **turns chỉ giải thích một nửa biến thiên** — nửa còn lại là kích thước file worker phải đọc. ⛔ Đừng dùng `turns^1.74` để ước lượng một lô đã được cắt ngắn; nó vống lên nhiều lần. Và ⛔ đừng đọc ngược lại thành *"cấp trần là an toàn"* — xem bullet ngay dưới.

- **Cắt nhỏ dispatch — mỗi worker một lô việc, không phải cả feature.** Đây là đòn bẩy token lớn nhất của cả hai lane, lớn hơn mọi tối ưu context khác cộng lại.
    - **Trần chặn là ngân sách tool call ở mục *Ngân sách mỗi dispatch*** (60 + 15/spec mutation-test) — đó là thứ có hiệu lực. Còn **~3–5 file, hoặc một nhóm task gắn kết trong `tasks.md` / một tài liệu trong `outline.md`, là heuristic để CẮT lô**, không phải để chặn. Một lô đúng 3 file vẫn có thể vượt ngân sách; khi đó cắt tiếp, không giao thêm cho worker đang chạy.
    - **Read-only không miễn trần.** Lô verify không ghi file nào nên heuristic "3–5 file" rỗng nghĩa với nó — và đó chính là chỗ agent đắt nhất run 2026-08-22 chui lọt (26.5M, 19% toàn run). Ngân sách tool call áp cho **mọi** dispatch, kể cả read-only.
    - ⛔ **Cấp trần ≠ thi hành trần. PM phải ĐO lại sau run.** Run `2026-08-28-phase-2-architecture-design` có ngân sách trong **46/46 dispatch prompt** (đã grep, ⛔ không phải trí nhớ), vậy mà **8/46 lô vượt trần** (63→160 tool call) và tiêu **$102 = 24% chi phí subagent** mà ⛔ không lô nào bị chặn hay báo `PARTIAL`. ⭐ Trần có mặt trong **100%** prompt vẫn ⛔ không tự thi hành — nó là câu chữ cho tới khi close-step đối chiếu số thật. Trần chỉ là một dòng chữ trong prompt cho tới khi close-step đối chiếu số thật. Lô vượt xa nhất (160 call, 202 turn, **$24** — đắt nhất run) là một **lô quét cơ học**: loại lô dễ vượt trần nhất vì mỗi file sửa tốn 1–2 call, và ⛔ không có tín hiệu tự nhiên nào bảo nó dừng.
    - **Lô quét cơ học phải cắt theo SỐ CHỖ SỬA, không theo số file.** 217 chỗ trên 10 file là **một lô quá to**, dù "10 file" nghe vừa tầm. Đếm chỗ sửa trước bằng `grep -c`, chia sao cho mỗi lô ≲ 50 chỗ.
    - Worker xong lô của mình thì **trả về ngay** kèm Worker Contract. PM tick tiến độ rồi dispatch worker MỚI cho lô kế tiếp.
    - Số học biện minh cho việc này: 1 worker × 382 turns ≈ 90.9M, so với 4 worker × ~95 turns ≈ 38M — **rẻ hơn 58%**, đổi lại chỉ tốn thêm 3 × 23.6k overhead spawn (0.07M, không đáng kể).
    - **Hệ quả cho triage:** overhead spawn chỉ đắt khi so với việc *ngắn*. Càng về sau một run dài, một turn inline của PM (context đã phình) càng đắt hơn một turn của worker mới (context sạch) — nên đừng viện "tiết kiệm spawn" để PM tự ôm việc dài.

- **Chi phí của chính PM cũng bị chặn — và PM là chỗ DUY NHẤT luật siêu tuyến tính còn hiệu lực, vì PM ⛔ không có trần nào.** Mục này tồn tại vì nó từng bị bỏ sót: mọi guardrail phía trên đều nhắm vào subagent, trong khi đo run `2026-08-22-google-account-set-password` cho thấy **PM main loop chiếm 37% tổng chi phí** — 326 turn × 161k context/turn = 52.4M, đắt hơn bất kỳ subagent nào trong run. PM viết ra luật rồi tự miễn trừ cho mình.

    ⚠️ **Tái phạm ở run `2026-08-28-phase-2-architecture-design`, nhẹ hơn nhưng cùng hình dạng** — PM chiếm **27%** ($194/$710):

    | | turns | context `p50` | context `p90` | **$ / turn** |
    |---|--:|--:|--:|--:|
    | PM main loop | 613 | **272k** | 428k | **0.316** |
    | 46 worker | 3.705 | 106k | 199k | 0.115 |

    ⭐ **PM đắt gấp 2,75 lần worker trên mỗi turn.** Và PM tự làm **210 tool call tay chân** (129 `Bash`, 53 `Edit`, 28 `Read`) so với chỉ 46 `Agent` — ước **$67** chỉ để tự `grep`/`Edit`. Mỗi lần PM `grep` một chuỗi ở `p50` tốn ~$0.14; cùng việc đó trong worker context sạch tốn ~$0.01.
    - **Checkpoint `/compact` sau GATE, và sau mỗi 4 lô dispatch.** Đây là cơ chế đã được kiểm chứng chứ không phải đề xuất trên giấy: run 2026-08-22 compact giữa chừng rồi resume sạch, vì mọi trạng thái cần thiết đã nằm trong `docs/010-Planning/pm-runs/<run-id>/` chứ không nằm trong đầu PM. Run-state có giá trị đúng ở chỗ đó — nó làm cho context của PM trở thành thứ vứt đi được.
    - **PM đọc `SUMMARY` + `FILES_TOUCHED`, không đọc lại toàn bộ file worker vừa ghi.** Cần kiểm chứng độc lập một khẳng định của worker (và điều đó thường là đúng đắn) thì **dispatch một verify pass context sạch**, đừng tự đọc: cùng một việc, 20 turn × 40k của worker mới rẻ hơn 20 turn × 161k của PM cuối run gấp 4 lần.
    - **Không tự implement khi đã đi sâu vào run.** T0 tồn tại cho việc nhỏ ở *đầu* run, khi context PM còn sạch. Cũng phần việc đó, làm inline ở lô thứ mười thì đắt hơn spawn một worker mới.

- **Không nhồi rule tình huống vào prompt dispatch.** Worker đã có rule index; cần rule nào thì nêu tên file trong `[CONSTRAINTS]` cho nó tự đọc, đừng dán nguyên văn rule vào prompt.
- **`advisor` cấp theo chính sách, ⛔ không mặc định cho mọi lô.** Run `2026-08-28` gọi **93 lần** (89 từ worker) = **$84,91 ≈ 12% tổng chi phí**, ~$0,91 mỗi lần vì nó forward **toàn bộ** context của agent gọi. Cấp cho **lô ra quyết định** (thiết kế, phân xử hợp đồng, đóng escalation); ⛔ cắt ở **lô quét cơ học** — ở đó nó tư vấn cho một việc đã có lời giải đúng-sai rõ ràng. Nêu thẳng trong `[CONSTRAINTS]` là lô này có gọi `advisor` hay không.
- **Không bao giờ dispatch song song hai worker có giao file ownership.** Không cắt rời được thì dùng một worker.
- ⛔ **Không dispatch lô ĐỌC một nguồn khi lô SỬA chính nguồn đó chưa đóng — kể cả khi ⛔ không giao file ownership.** Giao file rời nhau **⛔ không đủ**: worker đọc `SRS` bản cũ sinh ra trích dẫn theo **hệ toạ độ đã chết**. Run `2026-08-28` để `L0` (sửa `SRS`) chạy cùng `L1`/`L2` (đọc `SRS`) ⇒ **ba hệ toạ độ số dòng** ⇒ **8 lô dọn, ~$90 = 21% chi phí subagent**, cho một lỗi lập lịch mất 10 giây để tránh.
    - ⚠️ **Và lô dọn đầu tiên phải đo lại phạm vi, nếu không phải dọn hai lần.** Đợt một (7 lô) xác định phạm vi bằng một `grep` chỉ bắt `SRS`, bỏ sót trích dẫn tới `MVP-Scope` và file khác; một lô audit sau đó đếm ra **217 chỗ trên 10 file** còn sót, phải chạy đợt hai — **lô đắt nhất run**. Đây là `Nguyên tắc bất biến` về `grep -i` + đủ biến thể, áp vào chính việc dọn.
- **File theo dõi tiến độ do PM độc quyền chỉnh sửa** (`tasks.md` bên lane code, `outline.md` bên lane doc). Worker báo task nào xong trong `FILES_TOUCHED` và `SUMMARY`; BẠN tick checkbox. Đây là chốt chặn chống ghi đè.
- **Không tick thay worker khi chưa đọc `FILES_TOUCHED`.** Sau mỗi worker trả về, đối chiếu `FILES_TOUCHED` với ownership đã cấp. Có file lạ → coi như vi phạm, ghi vào `escalations.md`, đánh giá tác động trước khi đi tiếp.
- **Verify phải do agent KHÁC agent đã thực thi.** Verify bởi chính người vừa làm là nghi thức rỗng — nó đọc đúng bộ context nó vừa tạo ra.
- **Không tuyên bố xong khi verdict còn CRITICAL.** Báo cáo trung thực phần chưa xong và lý do.
- **Không nhảy tier ngầm.** Muốn đổi tier giữa chừng → ghi vào `escalations.md` và báo anh biết.
- **Không đổi lane giữa chừng.** Phát hiện yêu cầu thực ra thuộc lane kia → dừng, báo anh, chạy lại bằng command đúng. Run-state cũ giữ nguyên làm dấu vết.

## Close-step — đo chi phí thật (BẮT BUỘC)

Mọi con số trong mục *Guardrails* đều là số **đo được**, và chúng chỉ giữ được độ chính xác nếu mỗi run đóng lại bằng một phép đo mới. Bước này tồn tại vì thiếu nó: con số overhead spawn "5–6k" từng sống rất lâu trong file này trước khi phát hiện nó sai gần 4 lần.

Trước khi viết báo cáo, ghi `docs/010-Planning/pm-runs/<run-id>/cost.md` gồm:

- **PM main loop**: turns, tổng `cache_read`, và `cache_read/turns` (context trung bình mỗi turn).
- **Từng subagent**: số tool call, turns, tổng `cache_read`. Xếp giảm dần theo chi phí.
- **Tổng run**, và tỷ lệ PM / subagent.
- **Lô nào vượt ngân sách tool call đã cấp ở gate**, vượt bao nhiêu, và vì sao.
- **Số lô thực tế so với plan.** Vượt plan >50% thì ghi hẳn một dòng kèm lý do — *không* coi đó là lỗi. Lô nở thêm để khoá một requirement chưa có test là chi phí của tính đúng đắn, đáng tiêu. Điều cần tránh là nó tăng mà không ai nhìn thấy.
- **Phân bổ chi phí theo NHÓM MỤC ĐÍCH**, ⛔ không chỉ theo lô: *sản xuất · dọn dẹp · rework · verify*. Đây là bảng duy nhất trả lời được "tiền đi đâu". Ở run `2026-08-28`: sản xuất $214 (49,7%) · dọn dẹp **$90 (20,9%)** · rework $99 (22,9%) · verify $28 (6,5%).
    - ⚠️ **Ghi rõ verify là khoản SINH LỜI, ⛔ không phải overhead.** $28 của run đó tìm ra lỗ `C-3` (nội dung đã takedown vẫn đọc được theo đặc tả) và bề mặt operator xuyên tenant. Một `cost.md` trình bày verify lẫn trong "51% không sinh nội dung mới" là một tài liệu **gây hại** — nó dụ run sau cắt đúng thứ rẻ nhất và đáng giá nhất.

### Lấy số — chạy đúng đoạn này, ⛔ đừng nhớ theo con số

> ⛔ **`cost-state` trong transcript ⛔ KHÔNG bao gồm subagent.** Ở run `2026-08-28` nó ghi `totalCostUSD: 278.85`, khớp **chính xác** main loop + `advisor` — trong khi 46 subagent tốn thêm **≈ $431**, tức **61% chi phí thật nằm ngoài con số đó**. Luôn cộng tay thư mục `subagents/`.

```bash
SLUG=~/.claude/projects/<slug>; SID=<session-id>
# 1) Main loop
jq -s '[.[]|select(.type=="assistant")|.message.usage|select(.!=null)] as $u
 | {turns:($u|length), cache_read:($u|map(.cache_read_input_tokens//0)|add),
    cache_create:($u|map(.cache_creation_input_tokens//0)|add),
    output:($u|map(.output_tokens//0)|add)}' $SLUG/$SID.jsonl
# 2) Từng subagent, xếp giảm dần theo chi phí (đơn giá Opus: cr .5 / out 25 / cc 6.25 per MTok)
for f in $SLUG/$SID/subagents/*.jsonl; do b=$(basename $f .jsonl)
  tc=$(jq -r 'select(.type=="assistant")|.message.content[]?|select(.type=="tool_use")|.name' $f|wc -l|tr -d ' ')
  jq -s --arg d "$(jq -r .description $SLUG/$SID/subagents/$b.meta.json)" --arg tc "$tc" -r \
   '[.[]|select(.type=="assistant")|.message.usage|select(.!=null)] as $u
    | [($u|length), $tc,
       ((($u|map(.cache_read_input_tokens//0)|add)/1e6*0.5)
       +(($u|map(.output_tokens//0)|add)/1e6*25)
       +(($u|map(.cache_creation_input_tokens//0)|add)/1e6*6.25)|.*100|round/100), $d]|@tsv' $f
done | sort -t$'\t' -k3 -rn
```

- **Hiệu chuẩn đơn giá ngược từ `cost-state`** thay vì tra bảng giá: giải `costUSD` đã ghi theo 4 thành phần `usage`. Ở run `2026-08-28`, bộ `$5/$25/$0,5/$6,25` cho dư **2,3%** — đủ tốt, và ghi rõ trong `cost.md` rằng số subagent là **ước lượng**, ⛔ không phải số đo.
- **`cache_create` đắt gấp 12,5 lần `cache_read`.** 25M `cache_create` của run đó tốn $156, gần bằng 415M `cache_read` ($208). ⛔ Đừng chỉ báo cáo `cache_read`.

Số nào lệch đáng kể so với bảng trong *Guardrails* thì **cập nhật bảng đó ngay trong cùng run**, kèm ghi chú đo ở run nào. ⭐ Run `2026-08-28` là ví dụ: nó **phủ định** `turns^1.74` cho lane doc có trần (`k = 0.94`) và buộc mục đó tách thành hai chế độ.

> ⚠️ **Bước này bị bỏ ở run `2026-08-28`** — `cost.md` đóng lại ⛔ không có một con số token nào, phải dựng lại toàn bộ từ transcript ở một session sau. Nguyên nhân gốc: file `pm-core.md` bị xoá nhầm ở commit `90a990f`, PM nạp lại bằng `git show` nhưng ⛔ không chạy mục này. **Close-step ⛔ không phải phần tuỳ chọn của run.**

## Output — báo cáo kết thúc run

- **Run**: `<run-id>` — lane, tier, số agent đã spawn, số vòng escalation.
- **Đã làm**: danh sách deliverable kèm đường dẫn.
- **Verdict**: kết quả verification, còn WARNING/SUGGESTION nào chưa xử lý.
- **Chi phí**: tổng run, tỷ lệ PM / subagent, lô nào vượt ngân sách. Trỏ tới `cost.md`.
- **Nợ lại**: phần bị cắt scope hoặc hoãn, kèm lý do. Có thì nói thẳng, không giấu.
- **Run-state**: `docs/010-Planning/pm-runs/<run-id>/`.
