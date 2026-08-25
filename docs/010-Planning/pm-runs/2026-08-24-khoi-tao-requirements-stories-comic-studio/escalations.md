# Escalations: 2026-08-24-khoi-tao-requirements-stories-comic-studio

Không escalation nào phát sinh **tại gate**. Các mục dưới đây phát sinh trong Bước 5 và được PM xử ở **tầng 2** (câu hỏi nằm trong phạm vi `brief.md` ⇒ PM tự quyết, ghi lý do, không hỏi anh).

---

## E-1 — Số hiệu *"Điều 11"* trong tên file `Story-AI-Disclosure-Article-11.md`

| | |
|---|---|
| **Tầng** | 2 — PM tự quyết |
| **Ai nêu** | `product-owner` lô L10 (Epic E–H), nêu trong `SUMMARY`, **không** trả `BLOCKED` |
| **Nội dung nêu** | Tên file được copy nguyên từ `findings/business-analyst.md` §4.7, nhưng writer *"không tìm thấy nơi nào trong repo khẳng định số hiệu Điều 11"* — repo chỉ nói nghĩa vụ *AI disclosure theo Luật TTNT 2025* (`GP-4`, `CF-7.7`). Writer **giữ nguyên tên file** để wave 3 không lệch, và ghi note tường minh trong Epic-G rằng Epic không khẳng định thêm số hiệu nào. |

**Quyết định của PM: tên file ĐÚNG, giữ nguyên. Không sửa gì.**

**Căn cứ** — PM `grep "Điều 11"` toàn `docs/` và số hiệu này **có căn cứ ở năm nơi độc lập**, tất cả đều có trước run này hoặc thuộc wave 1:

| Nguồn | Nội dung |
|---|---|
| `Charter-Comic-Studio.md` §9.1 câu 2 | *"**Khoản 4 Điều 11 Luật TTNT 2025** — nghĩa vụ đánh dấu định dạng máy đọc áp cho *mọi* nội dung AI hay chỉ…"* |
| `Charter-Comic-Studio.md` §4 **R6** | *"Tư vấn luật sư SHTT về Điều 37a và **khoản 4 Điều 11** TRƯỚC khi thương mại hoá"* |
| `MVP-Scope.md` §7.1 câu **Q2** | nguyên văn câu hỏi gate G0 về **khoản 4 Điều 11** |
| `Risk-Register.md` (hàng 2 của bảng câu hỏi pháp lý) | cùng câu hỏi, cùng số hiệu |
| `BRD-007-Legal-And-Compliance.md` (wave 1) | truy tới **`Luật số 134/2025/QH15`** — *"**Điều 11** (minh bạch) · **khoản 4 Điều 11** (gắn nhãn + đánh dấu định dạng máy đọc) · **Điều 8** (chuyển tiếp 12 tháng)"*, nhãn `[OFF]`, nguồn `Analysis §8.4` |

**Vì sao writer không thấy**: nó đọc `MVP-Scope §3 GP-4` và `Glossary.md` — hai chỗ **nói về nghĩa vụ mà không nhắc số hiệu**. Số hiệu nằm ở `Analysis §8.4` và ở `Charter`/`MVP-Scope §7.1`, không thuộc `[CONTEXT]` mà PM cấp cho lô đó.

**Sự thận trọng của writer là ĐÚNG hành vi, không phải lỗi.** Nó gặp một số hiệu điều luật không truy được trong phạm vi nguồn được cấp, và nó **giữ nguyên tên đã đóng băng** thay vì tự sửa (sửa sẽ làm 41 link của wave 3 lệch) **và** từ chối khẳng định thêm. Đó chính xác là hành vi mà `[ANTI-HALLUCINATION]` yêu cầu.

**Bài học cho PM, đáng ghi**: PM cấp `[CONTEXT]` theo *chủ đề* (`MVP-Scope §3` nhóm G, `Glossary`) nhưng tên file lại mã hoá một **số hiệu pháp lý** chỉ tồn tại ở nguồn khác. Khi một tên file chứa một khẳng định sự thật, `[CONTEXT]` của lô đó **phải** gồm nguồn của khẳng định ấy — nếu không, writer buộc phải chọn giữa "bịa" và "báo nghi vấn", và cả hai đều tốn một vòng.

> ⚠️ **Chuyển cho verify L21/L23**: BRD-007 phân biệt **hai văn bản cùng số 134** — `NĐ 134/2026/NĐ-CP` (Điều 5a / 37a / 37b, hiệu lực 09/04/2026) **khác** `Luật số 134/2025/QH15` (khoản 4 Điều 11, hiệu lực 01/03/2026). Verify phải kiểm **mọi** tài liệu của run có trộn lẫn hai số hiệu này không. Đây là loại lỗi mà một người đọc không tinh sẽ không bao giờ phát hiện.

---

## E-2 — Xung đột rule: RULE-001 quy tắc #4 (writer cập nhật MOC) vs ownership map (PM giữ MOC)

| | |
|---|---|
| **Tầng** | 2 — PM tự quyết |
| **Ai nêu** | **Ba** writer độc lập: `security-auditor` (L5a), `product-designer` (L7), và `product-owner` gián tiếp qua DoD **D5** |
| **Nội dung nêu** | RULE-001 quy tắc #4 ghi *"**BẮT BUỘC** cập nhật file MOC tương ứng sau khi tạo tài liệu mới"*, và Validation Checklist của nó cũng có dòng đó. Nhưng `outline.md` §5 + ownership map giao MOC cho PM và **cấm writer chạm**. Cả ba writer đều tuân ownership và **báo lại thay vì im lặng**. |

**Quyết định của PM: ownership THẮNG. Writer không chạm MOC. PM cập nhật ở close-step.**

**Căn cứ**: `pm-doc.md` Guardrails lane doc ghi tường minh — *"**File MOC và `000-Index.md` không bao giờ cấp cho worker.** PM giữ độc quyền — đây là điểm hội tụ của mọi writer."* Với run này có **20 lô writer**, cấp `Requirements-MOC.md` cho cả 8 lô của tầng 020 là cầm chắc ghi đè lẫn nhau. RULE-001 quy tắc #4 nói *"phải được cập nhật"* — nó **không** nói *"writer của tài liệu phải là người cập nhật"*. Không có xung đột thật; chỉ là quy tắc #4 mặc định một người làm cả hai việc, còn ở đây hai việc thuộc hai chủ.

**Hành vi của ba writer là ĐÚNG**: tuân ràng buộc hẹp hơn, rồi **báo lại** để PM route. Đây là lý do khối `SUMMARY` của Worker Contract tồn tại.

> ✅ **Nghĩa vụ này KHÔNG bị rơi** — nó nằm ở `outline.md` §5 (5 file PM phải cập nhật) và có một lô verify riêng (**L24**) nhắm đúng vào nó, vì `cost.md` run trước bài học #5: lỗi MAJOR `M-1` của run đó **do PM tự sửa file ở close-step sau khi verify đã chạy**.

---

## E-3 — Bốn lô wave 1 bị terminate do session limit, mất khối Worker Contract

| | |
|---|---|
| **Tầng** | 2 — PM tự quyết |
| **Nguyên nhân** | API error `You've hit your session limit · resets 2:50am (Asia/Saigon)` — **hạ tầng, không phải lỗi worker** |
| **Ảnh hưởng** | L1 (PRD), L2 (SRS), L4 (BRD-004…006), L5b (BRD-008) bị cắt **sau khi đã ghi file**, ở bước tự-verify ⇒ **không lô nào trả khối `STATUS`/`FILES_TOUCHED`/`SUMMARY`** |

**Quyết định của PM: tick 6 file đó bằng CHECK CƠ HỌC, ghi rõ nguồn gốc của việc tick, KHÔNG coi như đã có Worker Contract.**

Guardrail `pm-core.md` — *"Không tick `outline.md` thay worker khi chưa đọc `FILES_TOUCHED`"* — tồn tại để chặn PM **giả định** worker đã làm đúng. Nó không có nghĩa "file không được tick khi worker chết vì hạ tầng"; nó có nghĩa **PM phải có bằng chứng thay thế**. Năm check PM đã chạy:

| # | Check | Kết quả |
|---|---|---|
| 1 | `git status --short` | đúng 10 file mới, **0 file bị modify**, 0 vi phạm ownership |
| 2 | `tail -3` từng file | cả 10 kết thúc bằng block signature đầy đủ ⇒ **0 file bị cắt giữa** |
| 3 | `grep "\[\["` | **0 wiki-link** |
| 4 | `grep "](.*030-Specs"` | **0 link tới tầng rỗng** |
| 5 | frontmatter | 10/10 đủ `id`/`type`/`status: draft`/`created`, id đúng dãy `PRD-001`, `SRS-001`, `BRD-001…008` |

**Cái check cơ học KHÔNG thay thế được, và vì thế trở thành nghĩa vụ của verify:**
- Không có `SUMMARY` tự báo ⇒ **PM không biết 4 lô đó có tự phát hiện `PARTIAL` nào không**. Cụ thể L1 (PRD) được ràng buộc **phải** báo `PARTIAL` vì khoảng trống persona `KT-1`. PM đã xác minh §3.3 *có* mục `TBD` đúng yêu cầu, nhưng **nợ này phải được L21 khẳng định lại**, không coi là đã đóng.
- Không có xác nhận *"mọi hàng `MVP-Scope §3` của module đều có mặt"* từ chính L4 và L5b (L3 và L5a có xác nhận đó trong `SUMMARY`). ⇒ **L21 phải tự đếm** cho `BRD-004…006` và `BRD-008`.

**Thay đổi quy trình PM áp dụng ngay từ wave 2**: mọi prompt dispatch thêm một dòng — *"**GHI FILE NGAY SAU KHI VIẾT XONG TỪNG FILE**, không giữ nháp trong context rồi ghi một lượt cuối."* Wave 1 chứng minh giá trị của nó: cả 4 agent bị cắt đều đã ghi xong file, nên **0 công việc bị mất**. Nếu chúng giữ nháp thì mất 6 file.

---

## E-4 — File Epic KHÔNG có id tường minh cho từng Story, writer phải tự suy `STORY-{X}-nn`

| | |
|---|---|
| **Tầng** | 2 — PM tự quyết |
| **Ai nêu** | **Ba** writer độc lập trong cùng một wave: `product-owner` L11, L12, L14. L11 nói thẳng *"đề nghị PM chuẩn hoá cách đánh số này xuyên các lô L11–L18"* |
| **Nội dung nêu** | `outline.md` §2.6 và prompt dispatch đều yêu cầu frontmatter `id: STORY-{X}-nn` và nói *"`nn` đúng theo Epic cha"*, nhưng **8 file Epic của wave 2 không chứa cột id nào** — mục 3 của Epic chỉ liệt kê tên file Story theo hàng. Không writer nào có nguồn để đọc ra `nn`. |

**Quyết định của PM: `nn` = thứ tự hàng Story trong mục 3 của Epic cha, đánh số từ `01`. Không sửa file Epic để thêm cột id.**

**Căn cứ**: ba writer, làm việc song song và không thấy nhau, **suy ra cùng một quy ước** và đều **khai rằng đó là suy luận** thay vì trình bày như thể đọc được từ nguồn. Sự hội tụ đó là bằng chứng quy ước này là cách đọc tự nhiên duy nhất của cấu trúc mục 3. Thêm cột id vào 8 file Epic đã commit sẽ mở lại deliverable của wave 2 để lấy một thứ có thể suy ra không nhập nhằng — đổi một sửa chữa thật lấy một tiện lợi.

**Lỗi này thuộc PM, không thuộc writer.** `outline.md` §2.6 viết *"`nn` đúng theo Epic cha"* như thể Epic có sẵn con số đó. PM chưa bao giờ kiểm rằng nó có. Cụm chữ ấy mô tả một thứ không tồn tại trong suốt 4 lô đầu của wave 3.

**Hành động đã áp**: từ L15 trở đi, prompt cấp quy ước **thành văn** ở khối *"BA QUYẾT ĐỊNH PM ĐÃ CHỐT — áp dụng, không cần suy lại"*, nên L15–L18 không phải suy lần nữa. PM đã kiểm cơ học 21 file của L11–L14: `A-01…05` · `B-01…04` · `C-01…07` · `D-01…05` — **liên tục, không trùng, không nhảy số**.

> ⚠️ ~~**Chuyển cho verify + L19**: `Backlog-Priority.md` sẽ tham chiếu chính 41 id này. Verify phải kiểm **cả 41** id liên tục trong từng Epic và **khớp thứ tự hàng của Epic cha** — không chỉ kiểm chúng tồn tại. Một id lệch thứ tự sẽ làm `Backlog-Priority` trỏ sai Story mà không có link nào chết để lộ ra.~~
>
> ❌ **NGHĨA VỤ NÀY DỰA TRÊN TIỀN ĐỀ SAI — đã sửa sau khi L19 về.** PM giả định `Backlog-Priority.md` định danh Story bằng id. **Nó không.** Schema 15 cột ở `findings/product-owner.md` §3.2/§3.3 định danh Story bằng **link tới file**; `grep 'STORY-[A-H]-[0-9][0-9]'` trên `Backlog-Priority.md` trả về **0**.
>
> ⇒ **Rủi ro PM lo không tồn tại, và thiết kế thật MẠNH HƠN giả định của PM**: mọi tham chiếu sai trong `Backlog-Priority` **là** một link chết, phát hiện được bằng máy. PM đã kiểm: `diff` giữa danh sách link (`grep -o` + `sed`) và `ls docs/022-User-Stories/Backlog/` = **rỗng**, tức **41/41 khớp character-exact**; 8/8 link Epic cũng khớp.
>
> ⇒ **Nghĩa vụ verify được THU HẸP, không xoá**: vẫn kiểm 41 id trong frontmatter Story là đúng và liên tục — chúng sẽ được dùng về sau (sprint planning, tham chiếu chéo). Nhưng **bỏ** phần *"kiểm khớp thứ tự hàng vì `Backlog-Priority` phụ thuộc"*: không có phụ thuộc đó.
>
> **Bài học cho PM, cùng loại với chính lỗi E-4**: PM viết một nghĩa vụ verify dựa trên một giả định về **schema của một file chưa được viết**, thay vì đọc schema đã có sẵn trong `findings/product-owner.md` §3.2. Đây là lần thứ **hai** trong cùng escalation này PM khẳng định một thứ về cấu trúc mà không kiểm — lần đầu là *"`nn` đúng theo Epic cha"*. Cả hai lần chi phí thấp vì writer khai báo suy luận thay vì im lặng. Nhưng cái sửa được là **PM kiểm cấu trúc trước khi viết ràng buộc về cấu trúc**, không phải trông vào writer bắt lỗi hộ.

---

## E-5 — Khối `[!WARNING]` trong file Epic lệch với bảng `findings` §4.10

| | |
|---|---|
| **Tầng** | 2 — PM tự quyết |
| **Ai nêu** | `product-owner` L13 (Epic-C), trong `SUMMARY`, **không** trả `BLOCKED` — nó chọn một hướng, ghi rõ vì sao chọn, rồi tiếp tục |
| **Nội dung nêu** | Hai lệch cụ thể: (a) khối `[!WARNING]` của `Epic-Comic-Director-And-Layout` gán `Story-Comic-IR-Panel-Specification` vào §4.10, nhưng **bảng §4.10 gốc không có hàng đó**; (b) hàng gate trong §4.10 chỉ ghi vỡ ở `I`, còn §4.3 **và** bảng mục 3 của Epic cha đánh dấu **cả `I` và `S`** là ⚠️. |

**Quyết định của PM: bảng `findings` §4.x + bảng mục 3 của Epic cha THẮNG khối `[!NOTE]`/`[!WARNING]` trong Epic, khi lệch nhãn `I`/`S`.**

**Căn cứ**: hai nguồn thắng là hai nguồn **đã được verify character-exact** — L10 tự `grep` đối chiếu 26/26 tên file Story với §4.5–§4.8, và L9/L10 dựng bảng mục 3 từ chính §4.x. Khối `[!WARNING]` là **văn xuôi diễn giải** mà writer wave 2 thêm vào để cảnh báo người đọc; nó hữu ích nhưng nó là tầng thứ hai, không phải nguồn. Khi một bảng đã verify lệch với một đoạn văn diễn giải, bảng thắng.

**Trường hợp (a) là dấu hiệu tốt, không phải lỗi**: writer wave 2 nhận ra `Comic-IR` **thực sự** vỡ `Independent`/`Small` và cảnh báo, dù lens chưa đưa nó vào §4.10. Nhận định đó có lý — `Comic-IR` là `[MVP0]`, `E_build ~20h` vượt trần. Nhưng **INVEST không áp cho Story `[MVP0]`** ngay từ đầu, nên việc nó có nằm trong §4.10 hay không **không đổi nội dung file**: mục 6 vẫn ghi `INVEST không áp` + DoD 5 tiêu chí gate G1. Lệch này vô hại về đầu ra, chỉ đáng ghi vì nó cho thấy §4.10 chưa phủ hết.

**Hành động đã áp**: L15–L18 nhận quy tắc ưu tiên nguồn này thành văn, **kèm** hướng xử lý cho trường hợp còn lại — Story có `⚠️` ở §4.x nhưng **không** có hàng chi tiết §4.10 thì writer tự suy lý do và **gắn nhãn** `[PO suy luận]` / `[Kiến trúc suy luận]` / `[Security suy luận]` / `[QA suy luận]` ngay tại chỗ. Nhãn đó tồn tại để verify **grep được** ra mọi chỗ suy luận thay vì phải đọc tay 41 file.

> ⚠️ **Chuyển cho verify**: `grep` mọi nhãn `[* suy luận]` trong 41 Story. Mỗi chỗ phải (a) là Story thật sự có `⚠️` ở §4.x, và (b) có lý do đọc được, không phải câu rỗng. Đây là **nợ có chủ đích** — nó hợp lệ vì được đánh dấu, không phải vì nó đúng.

---

## Không phải escalation — ghi lại để không ai đi tìm

- **`Story-Change-Log-On-Every-Editor-Action` giữ ở CẢ HAI chỗ** (một Story riêng trong Epic-D mục 3 **và** một mục DoD cấp Epic). Lens đề xuất chuyển hẳn thành DoD; PM bác vì nó là `KC-2` trong danh sách *"không được cắt"*, và một ràng buộc chỉ tồn tại trong DoD thì **không có ai tick nó**. Quyết định đã ghi ở `outline.md` §2.5, writer đã thực hiện đúng.
- **Epic-D KHÔNG tách.** Lens cảnh báo nó có thể vỡ (5 thành phần UI độc lập trải 3 mốc); writer L9 khuyến nghị **chưa tách** với lý do PM chấp nhận: quan hệ ba tầng đang là **1:1:1** (module PRD ↔ BRD ↔ Epic), tách sẽ biến traceability từ **một link** thành **một ma trận** — đúng cái mà trục module A–H được chọn để tránh. Đường tách tự nhiên (theo thành phần #1–#5, **không** theo mốc) đã ghi trong Epic-D mục 5 để dùng về sau.
- **Hai lỗi gán nhãn exit criterion do writer L9 TỰ phát hiện và TỰ sửa**: `M1-7` (thực ra là `usage_daily` p50/p90 — thuộc Epic-F, không phải job queue của Epic-A) và `M1-3` (thuộc Epic-B, không phải Story Bible editor của Epic-D). Cả hai đổi thành *"không có exit criterion `M-x` riêng, nằm ở cột Deliverable"*. Đây đúng loại lỗi **tách số khỏi nhãn** mà run này đang policing — writer bắt được nó là dấu hiệu ràng buộc canonical facts đang hoạt động.
