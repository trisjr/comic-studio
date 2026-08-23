# Cost: 2026-08-23-khoi-tao-tai-lieu-planning-comic-studio

**Số đo thật**, lấy bằng `jq` cộng trường `message.usage` trong `~/.claude/projects/<slug>/<session>.jsonl` (main loop) và `<session>/subagents/agent-*.jsonl`. Không phải ước lượng.

> Snapshot main loop chốt **trước** turn báo cáo cuối — con số thật cao hơn vài nghìn output token. Số subagent là chốt hẳn.

---

## 1. Bảng tổng

| # | Thành phần | Role | Lô | Tool call | Turn | Cache read | Cache write | Output |
|---|---|---|---|---:|---:|---:|---:|---:|
| — | **Main loop (PM)** | product-manager | — | — | **271** | **76.678.003** | 1.740.167 | **599.290** |
| 1 | Inventory kho docs *(kiêm probe Write)* | `context-auditor` | L1 | 25 | 51 | 3.036.639 | 273.905 | 30.301 |
| 2 | Market sizing + đối thủ | `researcher` | L2 | 51 | 84 | 8.166.181 | 521.855 | 36.107 |
| 3 | Charter | `business-analyst` | L3 | 17 | 34 | 2.058.983 | 345.397 | 23.181 |
| 4 | MVP-Scope + Roadmap | `architect` | L4 | 22 | 45 | 4.186.858 | 689.200 | 66.392 |
| 5 | Risk Register | `security-auditor` | L5 | 19 | 39 | 2.820.401 | 485.463 | 39.826 |
| 6 | Research Notes | `business-analyst` #2 | L6 | 14 | 34 | 2.462.436 | 354.625 | 81.479 |
| 7 | OKRs | `product-owner` | L7 | 11 | 27 | 2.291.678 | 479.465 | 31.841 |
| 8 | **Verify 6 deliverable** | `context-auditor` | L8 | 49 | **89** | **14.358.593** | 577.767 | 54.645 |
| | **Tổng 8 subagent** | | | **208** | **403** | **39.381.769** | 3.727.677 | **363.772** |

**Tổng run**: cache read **116,06M** · output **963.062**
**Tỉ lệ**: PM **66,1%** cache read / **62,2%** output · subagent **33,9%** / **37,8%**

---

## 2. Ngân sách tool call

| | |
|---|---|
| Cấp tại gate | 8 lô × 60 = **480** |
| Thực dùng | **208** (43%) |
| **Lô vượt trần** | **KHÔNG CÓ.** Lô cao nhất là `researcher` **51/60** (85%), kế đến verify **49/60** (82%) |
| Số lô thực tế vs plan | **8/8** — đúng plan, không nở thêm lô nào |

Hai lô chạm gần trần đều là lô **đọc nhiều**: `researcher` phải fetch web và nhiều nguồn trả 403/timeout nên phải thử nguồn thay thế; verify phải grep chéo 6 deliverable × 6 tiêu chí. Cả hai đều **báo `DONE`, không phải `PARTIAL`** ⇒ trần 60 đặt đúng chỗ cho lane doc.

⚠️ **Một hệ quả của việc không lô nào chạm trần đáng ghi lại**: `researcher` **tự dừng ở 51 call và bỏ dở câu hỏi 5.e (kênh phân phối thị trường Việt Nam)** với lý do *"hết ngân sách"* — trong khi nó còn **9 call**. Trần không bị chạm, nhưng **cảm giác về trần** đã cắt scope. Lần sau nên nói rõ trong `[TASK]`: *"còn dưới trần thì tiếp tục; chỉ dừng khi thật sự chạm"*.

---

## 3. Điều đáng đọc trong bảng này

### 3.1 Guardrail `Write` của run trước: đã khoanh vùng được chính xác

Run trước kết luận trong `cost.md` mục *"Nếu chạy lại"*: **"Với lane doc trong môi trường này: PM tự viết, không dispatch writer."** Run này **bác bỏ kết luận đó**, và đó là thu hoạch phương pháp lớn nhất.

| Writer | File đích | `Write` |
|---|---|---|
| `context-auditor` | `findings/inventory.md` | ✅ |
| `business-analyst` #1 | `Charter-Comic-Studio.md` | ✅ |
| `security-auditor` | `Risk-Register.md` | ✅ |
| `architect` | `MVP-Scope.md`, `Roadmap.md` | ✅ |
| `context-auditor` | `findings/verify-report.md` | ✅ |
| `business-analyst` #2 | **`Analysis-Market-Competitor-Landscape.md`** | ❌ **chặn 2 lần, deterministic** |

⇒ **Guardrail bám theo MẪU TÊN FILE** (*"report/analysis .md file"*), **không** theo loại agent và **không** theo worktree. 5/6 writer ghi được bình thường.

**Kết luận của run trước là tổng quát hoá quá mức từ một mẫu** — nó quan sát đúng một writer bị chặn (cũng là writer viết một tài liệu **Analysis**) rồi suy ra cả lane. Chi phí của sai lầm đó có thể đo được: nếu run này tin theo, PM sẽ tự viết cả 6 tài liệu và cộng thêm khoảng **300k output token** vào phần vốn đã là 599k.

**Quy tắc thay thế, hẹp và dự đoán được**: dispatch writer bình thường; riêng file có tên khớp `Analysis-*` / `*-report.md` thì dispatch để **soạn nội dung**, PM ghi file. Chi phí: nội dung đi qua context PM một lần.

### 3.2 PM vẫn chiếm 62% output — nhưng vì lý do khác run trước

| | Run trước | Run này |
|---|---:|---:|
| PM output | 854.175 | **599.290** (−30%) |
| PM turn | 235 | 271 |
| PM cache read | 39,39M | **76,68M** (+95%) |
| **PM context/turn** | ~168k | **~283k** (+68%) |
| Deliverable | 1 tài liệu | **6 tài liệu + 32 thư mục + `000-Index` + 3 MOC + Glossary + RULE-001** |

PM viết **ít hơn** dù giao gấp sáu lần deliverable — mô hình dispatch hoạt động. Nhưng **context mỗi turn của PM tăng 68%**, và đó là chỗ tiền thật sự đi.

Ba nguồn phình, xếp theo mức đóng góp:
1. **Ghi `findings/researcher.md` (~8k token) và `Analysis-Market-Competitor-Landscape.md` (~700 dòng)** — cả hai đi qua context PM vì worker không ghi được file (một do không có tool `Write`, một do guardrail tên file).
2. **`outline.md` với bảng canonical facts** — PM phải giữ toàn bộ CF trong đầu để dựng nó, và nó ở lại trong context tới hết run.
3. **Nạp trước**: `pm-core.md` + RULE-001 + 5 file run-state của run trước + các mục trích từ Analysis 1.148 dòng.

**Điểm 1 là chi phí bắt buộc; điểm 2 là chi phí đáng tiêu** (nó mua được 0 lỗi cross-doc trên 4 writer song song). **Điểm 3 là chỗ có thể cắt** — PM đọc `§4.1, §10, §11, §9b, §6.1` của Analysis bằng `sed` thay vì đọc cả file là đúng, nhưng vẫn có thể đẩy phần lớn việc đó sang một lens đọc-và-tóm-tắt.

### 3.3 Verify là subagent đắt nhất — và điều đó là đúng

`context-auditor` verify: **89 turn · 14,36M cache read**, tức **37% toàn bộ chi phí subagent**, gấp 1,8 lần lens đắt thứ nhì.

**Đây không phải lãng phí.** Nó được giao **6 tiêu chí trên 6 tài liệu** (hơn 1.900 dòng), trong đó hai tiêu chí đòi **quét chéo cơ học**: đối chiếu 10 con số CF dùng chung ở mọi nơi chúng xuất hiện, và sweep từng khuyến nghị trong outline + findings xem có landed không. Kết quả: **4 MAJOR bắt được, 0 CRITICAL, 0 khuyến nghị bị rơi**. Trong đó **M-1** (`Glossary.md` mất ba caveat của con số 23% GRR) là lỗi **PM tự tạo ra ở close-step** — không tiêu chí nào của bốn tiêu chí chuẩn nhắm vào file đó, và không ai khác trong run có thể bắt được nó.

> **Bài học ngân sách**: run trước cấp verify **50** call và nó dùng 33. Run này cấp **60** và nó dùng 49 — cho một phạm vi lớn gấp sáu. **Đừng cắt ngân sách verify theo tỉ lệ với số deliverable**; chi phí verify tăng theo **số cặp tài liệu phải đối chiếu**, không theo số tài liệu.

### 3.4 Overhead spawn — đo lại: **~25,5k**, không phải 23,6k

Đo `cache_creation_input_tokens` ở **turn đầu tiên** của ba subagent (turn đầu có `cache_read = 0`, nên toàn bộ context khởi tạo nằm ở `cache_write`):

| Subagent | Turn đầu — cache write |
|---|---:|
| `context-auditor` (inventory) | **24.854** |
| `business-analyst` (Charter) | **25.697** |
| `product-owner` (OKRs) | **26.078** |

⇒ **Trung vị ~25,7k.** Cao hơn con số **23,6k** trong `pm-core.md` khoảng **9%**, dù `pm-core.md` dự đoán con số này sẽ **giảm ~1,5k** sau đợt rút rule khỏi auto-load.

**Nguyên nhân gần như chắc chắn: prompt dispatch của run này dài.** Mỗi prompt chứa toàn văn outline của tài liệu đó, danh sách ràng buộc, tiêu chí xong và ownership map — ước lượng 2–4k token/prompt. Đây là **đánh đổi có chủ đích**: prompt dài mua được 0 lỗi cross-doc và 0 vi phạm ownership trên 8 dispatch.

⇒ **Không sửa con số trong `pm-core.md` thành 25,7k.** Overhead spawn là **hàm của độ dài prompt**, không phải hằng số của môi trường. Cách ghi đúng: **~23–24k nền + độ dài prompt dispatch**.

### 3.5 Đường cong `turns^1.74` khớp về hình dạng, lệch về hằng số

| Subagent | Turn | Cache read | Cache read/turn |
|---|---:|---:|---:|
| `product-owner` | 27 | 2,29M | 85k |
| `business-analyst` (Charter) | 34 | 2,06M | 61k |
| `architect` | 45 | 4,19M | 93k |
| `researcher` | 84 | 8,17M | 97k |
| `context-auditor` (verify) | 89 | 14,36M | 161k |

Bảng trong `pm-core.md` ghi **33 turn → 1,5M**. Run này ở 34 turn cho **2,06M** — cao hơn **37%**. Ở 89 turn, đường cong dự đoán ~8,4M nhưng thực đo **14,36M**, cao hơn **70%**.

**Hình dạng siêu tuyến tính vẫn đúng** (context/turn tăng từ 61k lên 161k khi turn tăng 34 → 89), nhưng **hằng số phụ thuộc kích thước context khởi tạo**. Agent của run này khởi động với prompt dài và phải đọc bảng canonical facts ~300 dòng ⇒ mọi turn sau đều trả tiền cho phần nền đó.

⇒ **Đề xuất sửa `pm-core.md`**: ghi rõ bảng `turns^1.74` là **đường cong hình dạng, không phải bảng tra chi phí tuyệt đối**. Muốn ước lượng thật thì nhân thêm hệ số theo context khởi tạo. Nếu chỉ nhớ con số tuyệt đối, sẽ **ước thấp khoảng 40–70%** cho các run có prompt dispatch dài.

---

## 4. Guardrail cần cập nhật trong `pm-core.md`

| # | Mục | Số cũ | Đo được ở run này | Đề xuất |
|---|---|---|---|---|
| 1 | Overhead spawn | ~23,6k | **~25,7k** (trung vị 3 mẫu) | **Không đổi con số.** Ghi lại thành *"~23–24k nền + độ dài prompt dispatch"* — nó là hàm, không phải hằng số |
| 2 | Bảng `turns^1.74` | 33 turn → 1,5M | 34 turn → **2,06M**; 89 turn → **14,36M** (dự đoán ~8,4M) | Ghi rõ đây là **đường cong hình dạng**, không phải bảng tra tuyệt đối. Cảnh báo ước thấp 40–70% khi prompt dispatch dài |
| 3 | *"Lane doc: PM tự viết, không dispatch writer"* (`cost.md` run trước) | Áp cho cả lane | **Sai** — 5/6 writer ghi được | **Thu hẹp**: guardrail bám **mẫu tên file** (`Analysis-*`, `*-report.md`), không bám loại agent |
| 4 | Ngân sách verify | 50–60 call | Dùng **49/60** cho phạm vi gấp 6 lần run trước | Giữ 60. Thêm ghi chú: chi phí verify tăng theo **số cặp tài liệu phải đối chiếu**, không theo số tài liệu |
| 5 | Cách diễn đạt trần | "Ngân sách 60 tool call" | `researcher` **tự cắt scope ở 51/60** vì *"hết ngân sách"* | Thêm vào Dispatch Prompt Template: *"còn dưới trần thì tiếp tục; chỉ dừng khi thật sự chạm trần"* |

---

## 5. Cấu hình run

| | |
|---|---|
| Lane / Shape / Tier | `doc` / **A** (authoring) / **T3** — 3/4 câu triage trả lời Có |
| Spawn | **8** (2 lens + 5 writer + 1 verifier). Không lens nào spawn con — đúng invariant `pm-core.md` |
| Gate | **Đúng một lần**, 3 câu qua `AskUserQuestion`, duyệt như plan |
| Escalation | **0** — không tạo `escalations.md` |
| Deliverable | 6 tài liệu (~1.900 dòng) + 32 thư mục Dewey + `000-Index.md` + 3 MOC + Glossary 40→54 term + 1 hàng RULE-001 |
| Verdict | 0 CRITICAL · 4 MAJOR (sửa 4/4) · 5 MINOR (sửa 2, chấp nhận 3) |
| Vi phạm ownership | **0** — `git status` xác nhận đúng 2 file bị sửa (2 stub đã dự kiến) |

---

## 6. Nếu chạy lại run này

1. **Đẩy phần "PM đọc Analysis" sang một lens.** PM đọc `sed` từng mục là đúng hướng, nhưng ~250 dòng trích dẫn vẫn nằm trong context tới hết run. Một lens đọc-và-trả-bảng-CF sẽ rẻ hơn, và bảng CF là thứ duy nhất PM thật sự cần giữ.
2. **Cấp cho `researcher` một câu tường minh về trần**: nó bỏ dở một câu hỏi khi còn 9 call. Trần là để chặn runaway, không phải để worker tự cắt scope sớm.
3. **Bảng canonical facts là thứ đáng giữ nhất của run này.** 4 writer song song, 10 con số dùng chung, **0 lệch giá trị và 0 mất nhãn giữa các deliverable**. Nó không chỉ cấp số — nó cấp cả **lệnh cấm tường minh** (*"cấm trừ CF-6.8 cho CF-6.7"*, *"cấm gộp CF-4.6 với CF-4.8"*), và chính hai lệnh cấm đó xuất hiện nguyên văn trong deliverable.
4. **Tiêu chí verify thứ 6 (sweep khuyến nghị bị rơi) phải thành mặc định.** Run trước bắt được 2 MAJOR nhờ verifier **tự phát**; run này biến nó thành yêu cầu tường minh và kết quả là **0 khuyến nghị bị rơi**. Đây là thay đổi rẻ nhất có tỉ suất cao nhất của cả hai run.
5. **Đừng để PM viết vào file mà không có ai verify.** M-1 (`Glossary.md` mất ba caveat) là lỗi PM tạo ra ở close-step, sau khi verify đã chạy trên deliverable. May là verifier tự mở rộng phạm vi. **Close-step của PM cũng cần nằm trong phạm vi verify**, hoặc phải chạy một verify pass ngắn sau close-step.

---

Xem thêm: [verdict.md](./verdict.md) · [brief.md](./brief.md) · [run-plan.md](./run-plan.md) · [outline.md](./outline.md)
