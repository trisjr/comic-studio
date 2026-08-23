# Cost: 2026-08-23-danh-gia-y-tuong-comic-studio

**Số đo thật**, lấy từ `~/.claude/projects/<slug>/<session>.jsonl` và `<session>/subagents/agent-*.jsonl` bằng `jq` cộng trường `message.usage`. Không phải ước lượng.

> Snapshot main loop chốt **trước** turn báo cáo cuối cùng — con số thật cao hơn vài nghìn output token. Số subagent là chốt hẳn (đã kết thúc).

---

## 1. Bảng tổng

| Thành phần | Role | Turn | Cache read | Cache write | Output |
|---|---|---|---|---|---|
| **Main loop (PM)** | product-manager | 235 | 39.391.312 | 2.692.507 | **854.175** |
| Lens 1 | `architect` | 36 | 1.708.599 | 720.825 | 59.331 |
| Lens 2 | `senior-ai-engineer` | 23 | 1.191.691 | 263.227 | 52.971 |
| Lens 3 + delta | `researcher` | 125 | 10.622.412 | 1.164.014 | 70.263 |
| Writer §1–§6 | `business-analyst` | 36 | 3.779.409 | 1.697.086 | 43.851 |
| Verify | `context-auditor` | — | — | — | ~165.877 tổng (33 tool call, 13,5 phút) |
| **Tổng 5 subagent** | | 220 | 17.302.111 | 3.845.152 | **226.416** |

---

## 2. Điều đáng đọc trong bảng này

### 2.1 PM tiêu 79% output token của cả run

854k / (854k + 226k) ≈ **79%**. Với một lane doc mà đúng ra writer phải là nơi tiêu output, đây là con số ngược. Nguyên nhân **không** phải PM viết dài, mà là một guardrail của harness:

> `business-analyst` bị **chặn `Write`** với thông báo *"Subagents should return findings as text, not write report files"*.

Hệ quả dây chuyền:
1. Writer trả payload §1–§6 dưới dạng **text** trong phản hồi — PM phải ghi file. Nội dung đó **đi qua context của PM một lần nữa**.
2. PM **không dispatch batch 2** cho §7–§12, vì biết trước cùng guardrail sẽ chặn lần nữa — dispatch chỉ để nhận về text rồi tự ghi thì đắt hơn tự viết. **PM tự viết §7–§12 + Tài liệu tham khảo.**
3. `context-auditor` cũng bị áp cùng ràng buộc từ đầu ⇒ báo cáo verify 165k token đi qua context PM để PM chưng thành `verdict.md`.

**Bài học định lượng:** trong môi trường có guardrail này, mô hình "PM điều phối, worker viết file" của `pm-doc.md` **không thực thi được như thiết kế** cho lane doc. Chi phí thật của một lần dispatch writer = spawn overhead + output của writer + **cùng lượng nội dung đó lần thứ hai qua PM**. Với tài liệu dài, tự viết rẻ hơn dispatch. Đây là điều nên biết **trước** khi lập `run-plan.md`, không phải phát hiện ở giữa run.

### 2.2 `researcher` đắt hơn hẳn ba lens còn lại

125 turn và 10,6M cache read — gấp ~6x `architect`. Hai nguyên nhân, cả hai chính đáng:
- Nó là lens duy nhất có **WebFetch/WebSearch**; mỗi trang fetch về là input token thật, và nhiều lần fetch trả 403/paywall (thuvienphapluat, IAPP) nên phải thử nguồn khác.
- Nó bị **resume qua `SendMessage`** cho vòng delta sau gate, nên jsonl của nó gộp cả hai vòng.

**Và nó là lens trả về giá trị cao nhất.** Nó đảo hai kết luận: phát hiện NĐ 134/2026 Điều 5a khiến PM phải **thu hồi** khuyến nghị cắt `parent_generation`, và phát hiện Luật TTNT 2025 nâng compliance từ "chuyện thị trường Hàn Quốc" thành nghĩa vụ nội địa có deadline. Cả hai nằm **sau knowledge cutoff** — không lens nào không có web access tự đến được. Chi phí web access ở đây là **đắt và đáng**.

### 2.3 Quyết định resume thay vì re-run fan-out — tiết kiệm được bao nhiêu

Khi gate đổi giả định A1 (công cụ cá nhân → SaaS thương mại, user tự upload truyện), phương án đúng sách là chạy lại phase 2. PM chọn **resume 2 lens qua `SendMessage`** thay vì spawn mới (ghi ở `escalations.md` E1, kèm rủi ro của lựa chọn đó).

Cận dưới của phần tiết kiệm: spawn mới 2 lens = 2 × ~23,6k overhead + phải nạp lại toàn bộ `Request.md` (894 dòng) và tự khám phá lại repo. Resume giữ nguyên context đã prime ⇒ delta chỉ trả tiền cho **phần suy luận mới**. Nhìn vào bảng: `researcher` chạy 2 vòng mà cache write chỉ 1,16M — thấp hơn `business-analyst` chạy 1 vòng (1,70M), vì vòng 2 gần như toàn bộ là **cache read**.

### 2.4 Cache read chiếm ~91% tổng input

39,4M / 43,2M. Cache đang làm đúng việc của nó. Cache write 2,69M ở main loop tương ứng với các mốc context thay đổi thật: nạp `pm-core.md` + RULE-001, đọc `Request.md`, mỗi lần findings mới về, hai lần compact.

---

## 3. Cấu hình run

| | |
|---|---|
| Lane / Shape / Tier | `doc` / **A** (authoring) / **T2** — 2/4 câu triage trả lời Có |
| Spawn | **5** (3 lens + 1 writer + 1 verifier). Không lens nào spawn con — đúng invariant `pm-core.md`. |
| Gate | **Đúng một lần**, 4 câu qua `AskUserQuestion` |
| Escalation | 2 — **E1** (gate làm mất hiệu lực 4 kết luận), **E2** (PM tự sửa lỗi số học của chính mình: 2x → 3x, +50%) |
| Deliverable | 1 tài liệu, ~1.150 dòng, 16 mục, 0 wiki-link |
| Ngân sách tool call/dispatch | 60 cho lens & writer, 50 cho verify — **không dispatch nào chạm trần**; verify dùng 33/50 |
| Trần bị chạm | Không có. Nhưng **guardrail Write** chặn 2/5 subagent — xem §2.1 |

---

## 4. Nếu chạy lại run này

1. **Với lane doc trong môi trường này: PM tự viết, không dispatch writer.** Dispatch writer chỉ đáng khi worker thực sự **ghi được file**. Nếu guardrail còn, hãy đặt writer làm *lens soạn thảo* (trả outline chi tiết + các đoạn khó) chứ đừng đặt nó làm người sản xuất toàn văn.
2. **Chốt A1 (bản chất sản phẩm) ở gate TRƯỚC khi dispatch lens**, không sau. Đây là nguồn duy nhất của E1 và của toàn bộ vòng delta. Một câu hỏi thêm ở `brief.md` rẻ hơn một vòng delta.
3. **Cấp WebFetch cho ít nhất một lens là bắt buộc, không tuỳ chọn** — với domain có pháp lý hoặc benchmark, lens không có web access sẽ tự tin sai. Bằng chứng: hai lần lens có web access đảo kết luận của lens không có (§6.4 và §8.4 của deliverable).
4. **Thêm một yêu cầu tường minh vào dispatch prompt của verify**: *"liệt kê khuyến nghị có trong findings mà KHÔNG có trong deliverable"*. Bốn tiêu chí Bước 6 bắt **thừa** chứ không bắt **thiếu** — hai MAJOR của run này chỉ bị bắt vì `context-auditor` tự chủ động làm việc đó. Xem `verdict.md` §3.
5. **Khi một con số đi qua phép nhân, nhãn của nó phải đi cùng.** Bài học của E2, và nó tái diễn thêm một lần ở dòng 878 (verifier bắt được). Không phải lỗi cẩu thả một lần — là **failure mode có tính hệ thống** của việc tổng hợp nhiều lens.

---

Xem thêm: [verdict.md](./verdict.md) · [escalations.md](./escalations.md) · [outline.md](./outline.md) · [brief.md](./brief.md)
