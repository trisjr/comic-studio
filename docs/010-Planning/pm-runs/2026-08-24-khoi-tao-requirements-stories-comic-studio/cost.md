# Cost: 2026-08-24-khoi-tao-requirements-stories-comic-studio

> **Trạng thái file**: bảng số thô của wave 3 được ghi **ngay khi các lô báo về**, trước khi phần bài học được viết. Lý do: số liệu per-batch chỉ tồn tại trong text của notification; một lần compaction context là mất vĩnh viễn, và `cost.md` là close-step **bắt buộc** của lane doc. Ghi số trước, đúc kết sau.

## 1. Số đo per-batch — wave 3 (41 Story + 2 hạng mục cuối)

| Lô | Vai | Deliverable | Output token | Tool call | Thời gian (s) | Token / file |
|----|-----|-------------|-------------:|----------:|--------------:|-------------:|
| L11 | `product-owner` | 5 Story (Epic-A) | 200.186 | 30 | 852 | 40.037 |
| L12 | `product-owner` | 4 Story (Epic-B) | 177.647 | 30 | 603 | 44.412 |
| L13 | `product-owner` | 7 Story (Epic-C) | 169.400 | 31 | 702 | **24.200** |
| L14 | `product-owner` | 5 Story (Epic-D) | 164.449 | 25 | 624 | 32.890 |
| L15 | `architect` | 5 Story (Epic-E) | 207.063 | 38 | 632 | 41.413 |
| L16 | `product-owner` | 3 Story (Epic-F) | 185.117 | 35 | 500 | **61.706** |
| L17 | `security-auditor` | 6 Story (Epic-G) | 224.921 | 53 | 999 | 37.487 |
| L18 | `quality-assurance` | 6 Story (Epic-H) | 221.194 | 32 | 909 | 36.866 |
| **Tổng wave 3 (Story)** | | **41 Story** | **1.549.977** | **274** | — | **37.804** |
| L19 | `product-owner` | `Backlog-Priority.md` | 249.212 | **66** ⚠️ | 1.267 | — |
| L20 | `business-analyst` | `Glossary.md` (+15 term) | 163.919 | 34 | 560 | — |
| **Tổng wave 3 (đủ)** | | **41 Story + 2 hạng mục** | **1.963.108** | **374** | — | — |

### Bốn lô verify

| Lô | Vai | Phạm vi | Output token | Tool call | Thời gian (s) | Kết quả |
|----|-----|---------|-------------:|----------:|--------------:|---------|
| L21 | `context-auditor` | tầng 020 — 21 tài liệu | 188.518 | 54 | 325 | **0 defect** |
| L22 | `context-auditor` | tầng 022 — 50 tài liệu | 217.491 | 43 | 512 | 0 MAJOR · 1 MINOR · 2 NOTE |
| L23 | `context-auditor` | xuyên tầng — 72 file (tiêu chí 4/5/6) | 187.231 | 45 | 752 | **2 MAJOR** · 1 NOTE |
| L24 | `context-auditor` | close-step của PM — 5 file | 120.560 | 41 | 603 | **1 MAJOR** · 2 MINOR · 2 NOTE |
| **Tổng verify** | | | **713.800** | **183** | — | **3 MAJOR** |

> **Verify tốn 713.800 token — bằng 36% chi phí ghi (1.963.108) — và tìm ra 3 MAJOR mà không check cơ học nào của PM bắt được.** Con số này là câu trả lời cho câu hỏi *"verify có đáng không"*: ba MAJOR đó gồm **một số hiệu pháp lý gán sai văn bản trong PRD** (sẽ được copy xuống code), **10 link chết trong 8 Epic**, và **một mục tài liệu bị PM xoá im lặng** (không còn ở đâu trong repo). Không lỗi nào trong ba lỗi ấy lộ ra qua `grep`.
>
> ⚠️ **L19 vượt trần budget: 66/60 tool call.** Nguyên nhân đọc được và **chi tiêu đúng chỗ**: writer đối chiếu **65/65** link character-exact bằng `Glob` thật thay vì tin tên file trong findings — chính nó tạo ra kết quả `diff` rỗng khi PM kiểm lại 41 link.

> **Số của wave 1 và wave 2 KHÔNG có trong file này.** Chúng nằm trong notification của các lô L1–L10, và context PM đã bị compaction **hai lần** trước khi `cost.md` được khởi tạo. Đây là **mất dữ liệu thật, không phải bỏ sót** — và nó chính là lý do bảng trên được ghi sớm thay vì để tới cuối run. Bài học đã có ngay: **khởi tạo `cost.md` cùng lúc với `outline.md`, không phải ở close-step.**

## 2. Hai quan sát đọc được ngay từ bảng

**2.1 `token / file` biến động 2,5 lần và KHÔNG tương quan với số file.**
`L13` viết **7 file** với **24.200 token/file** — rẻ nhất. `L16` viết **3 file** với **61.706 token/file** — đắt nhất, gấp **2,55×**. Nếu chi phí bám số file thì quan hệ phải ngược lại.

Nguyên nhân đọc được từ chính nội dung hai lô: `L16` là module `F` — **module dày số nhất của run**, và prompt của nó yêu cầu *"dùng budget dư để rà lại nhãn nguồn của **mọi** con số"*. Nó rà thật: giữ nguyên **cả hai** con số mâu thuẫn của Anifusion, giữ caveat *"SÀN không phải trần"* của `C7`. `L13` ngược lại — 7 Story cùng một domain (layout/comic-director), chia sẻ gần như cùng một tập anchor, nên chi phí đọc nguồn được **khấu hao trên 7 file**.

⇒ **Chi phí một lô bám vào "số nguồn khác nhau phải đọc", không bám vào "số file phải ghi".** Cắt lô theo Epic (cùng domain ⇒ cùng anchor) đã đúng; cắt lô theo số file sẽ sai.

**2.2 Tool call là chỉ báo tốt hơn token về độ khó xác minh.**
`L17` (pháp lý) dùng **53 tool call** — cao nhất, gấp **2,1×** `L14` (25 call). Nó không viết nhiều file hơn (6 vs 5). Nó **xác minh nhiều hơn**: `grep` để chứng minh hai văn bản cùng số 134 không bị trộn, `grep` để chứng minh Roadmap **không** có exit criterion cho hard-delete tenant (0 kết quả — một grep tốn tiền để chứng minh một sự vắng mặt).

⇒ Lô nào có ràng buộc *"không được bịa số hiệu"* thì **tool call tăng, không phải token tăng**. Khi ước lượng ngân sách cho lô kiểu này, nới **trần tool call** mới đúng chỗ; nới token là nới sai trục.

## 3. Bài học

### #1 — Khởi tạo `cost.md` cùng lúc `outline.md`, không phải ở close-step

**Số của wave 1 và wave 2 đã MẤT.** Chúng chỉ tồn tại trong text của notification, và context PM bị compaction **hai lần** trước khi `cost.md` được tạo. Không cách nào lấy lại.

Đây là bài học **rẻ nhất và cụ thể nhất** của run: một file rỗng tạo ở Bước 4 với đúng một bảng trống sẽ cứu được toàn bộ dữ liệu ấy. Run trước không gặp vì nó ngắn hơn và không bị compaction.

### #2 — Chi phí một lô bám vào *số nguồn phải đọc*, không bám vào *số file phải ghi*

`L13` viết **7 file** với **24.200 token/file**; `L16` viết **3 file** với **61.706 token/file** — gấp **2,55×**. Nếu chi phí bám số file thì quan hệ phải ngược lại.

7 Story của `L13` cùng một domain nên chia nhau cùng một tập anchor; `L16` là module dày số nhất và phải rà nhãn nguồn từng con số. ⇒ **Cắt lô theo Epic (cùng domain ⇒ cùng anchor) là đúng trục.** Cắt theo số file sẽ sai.

### #3 — Với lô có ràng buộc *"không được bịa"*, nới TRẦN TOOL CALL, đừng nới token

`L17` (pháp lý) dùng **53 call** — gấp **2,1×** `L14` — mà không viết nhiều file hơn. Nó **xác minh** nhiều hơn: `grep` để chứng minh hai văn bản cùng số 134 không bị trộn, và `grep` để chứng minh `Roadmap` **không** có exit criterion cho hard-delete tenant (0 kết quả — một grep tốn tiền để chứng minh một **sự vắng mặt**).

`L19` vượt trần (**66/60**) vì cùng lý do: nó `Glob` đối chiếu **65/65** link character-exact. Chính chi tiêu đó tạo ra kết quả `diff` rỗng khi PM kiểm lại. ⇒ Vượt trần vì **xác minh** là chi tiêu đúng; vượt trần vì viết dài là chi tiêu sai. Trần nên phân biệt hai loại.

### #4 — Verify tốn 36% chi phí ghi và tìm ra 3 MAJOR mà không `grep` nào của PM bắt được

**713.800 token verify** trên **1.963.108 token ghi**. Ba MAJOR: một **số hiệu pháp lý gán sai văn bản trong PRD** (`Điều 198b` gán cho `NĐ 134/2026` — sẽ được copy xuống code), **10 link chết trong 8 Epic**, và **một mục tài liệu PM xoá im lặng** (không còn ở đâu trong repo).

**Không lỗi nào trong ba lỗi ấy lộ ra qua check cơ học.** PM đã chạy 5 loại `grep` và tuyên bố sạch. Lỗi PRD nằm ở vùng PM **tuyên bố đã quét mà chỉ quét một phần** (`Backlog/`, không phải cả 72 file) — xem bài học #6.

### #5 — Lô verify nhắm riêng vào close-step của PM đã trả đủ tiền vé ngay lần đầu

`L24` tồn tại vì bài học #5 của run trước (`M-1`: PM sửa Glossary sau khi verify chạy). Lần này nó bắt được **`M-3`**: PM **xoá im lặng** mục *"Quy Trình Làm Việc (BA Workflow)"* khỏi `Requirements-MOC.md` khi ghi lại toàn file.

Điều làm lỗi này đáng ghi hơn bản thân nó: **trong cùng commit đó PM ghi chú tường minh cho 3 link chết mình gỡ** (`> ⚠️ Link chết đã gỡ...`). PM áp guardrail *"không xoá im lặng"* cho ba dòng link, rồi vi phạm chính nó với một mục 9 dòng. **Không lô nào khác có phạm vi để thấy điều đó** — L21/L22 kiểm deliverable, L23 kiểm xuyên tầng theo tiêu chí. Bỏ L24 để tiết kiệm ⇒ mục đó biến mất khỏi repo mà không ai biết.

### #6 — `grep` một phần rồi tuyên bố sạch là tệ hơn không grep

PM quét bẫy số hiệu 134 **riêng thư mục `Backlog/`**, thấy sạch, và **ghi kết quả đó vào `outline.md`**. Nghĩa vụ E-1 nói *"kiểm **mọi** tài liệu của run"*. `L23` quét cả 72 file và tìm ra lỗi ở **PRD** — tầng cao nhất của cây requirement.

Một kết quả *"đã kiểm, sạch"* trên phạm vi hẹp hơn nghĩa vụ **tạo ra cảm giác an toàn giả** và làm người đọc sau không kiểm lại. Nếu PM ghi *"đã kiểm `Backlog/`, còn nợ 51 file"* thì thông tin trung thực. ⇒ **Ghi phạm vi thật của mỗi check, không ghi kết luận trần.**

### #7 — Quy ước của PM hẹp hơn thực tế writer gặp — ba lần trong một run

| Lần | PM viết | Thực tế |
|---|---|---|
| E-4 | *"`nn` đúng theo Epic cha"* | 8 file Epic **không có** cột id nào |
| E-4 phụ lục | *"`Backlog-Priority` tham chiếu 41 id"* | Schema §3.2 định danh Story bằng **link tới file** |
| E-5b | nhãn `[* suy luận]` chỉ cho `I`/`S` vỡ | 3 lô dùng nó cho **anchor không truy được** |

**Mẫu chung: PM viết ràng buộc từ HÌNH DUNG về nguồn, không từ nguồn.** Cả ba lần chi phí thấp **chỉ vì** writer khai báo suy luận thay vì im lặng. Cái sửa được không phải *"trông vào writer bắt lỗi hộ"* mà là **PM đọc cấu trúc trước khi viết ràng buộc về cấu trúc** — `grep` một file Epic mất 1 tool call.

### #8 — `grep` từ bị cấm phải đọc DÒNG, không đọc SỐ ĐẾM

Xảy ra **hai lần** trong run, cùng một hình dạng: `grep -i 'phase 0|spike|PoC'` trả **5 file**, nhưng **4 là false positive** — chúng là **văn bản trích chính lệnh cấm** (``⛔ Glossary cấm "spike"``). Đúng **1** vi phạm thật: `Story-Golden-Dataset-For-Regression` dùng *"kỷ luật spike"* trong một dòng AC-1, ở **cùng file** có dòng trích lệnh cấm đó.

Wave 2 gặp y hệt với `grep '\[\['` (4 hit, cả 4 nằm trong code span mô tả lệnh cấm wiki-link). ⇒ **Một tài liệu tốt chứa chính lệnh cấm mà nó tuân thủ**, nên `grep -c` trên tài liệu tốt **luôn** dương. Con số đếm không phân biệt được *"vi phạm"* với *"trích dẫn lệnh cấm"*.

### #9 — Ràng buộc *"ghi file ngay sau khi viết xong từng file"* đã cứu 6 file, và nên là mặc định

Wave 1: **4 lô bị session limit terminate** giữa bước tự-verify. Cả 4 đã ghi xong file ⇒ **0 công việc mất**. Nếu chúng giữ nháp trong context rồi ghi một lượt cuối thì mất **6 file** và phải chạy lại 4 lô.

Ràng buộc này được thêm vào **sau** sự cố. Nó nên nằm trong Dispatch Prompt Template mặc định — chi phí bằng **một dòng**, và nó bảo hiểm cho một lỗi hạ tầng mà PM không kiểm soát được.

### #10 — Writer khai báo suy luận là cơ chế đắt giá nhất của run này

Đếm được: **22 nhãn `[* suy luận]` trên 11 file** · `Story-H-02` khai *"thêm một dòng DoD ngoài G1"* kèm lý do · `L13` khai *"§4.10 không có hàng này, tôi chọn theo §4.3 vì…"* · `L16` giữ **cả hai** số mâu thuẫn của Anifusion thay vì dọn gọn · `L19` khai *"tie-break T4 không dùng được, tôi dùng quy ước đọc"* · `L20` khai *"tôi không có Bash nên không tự `git diff` được, đề nghị PM xác minh"*.

**Cái cuối là ví dụ sạch nhất.** `business-analyst` không có Bash. Nó **không** đọc mắt rồi tuyên bố *"54 term nguyên vẹn"* — nó nói ra giới hạn của mình và chuyển nghĩa vụ. PM chạy `git diff`: **30 thêm / 1 xoá**. Nghĩa vụ được đóng bằng **bằng chứng**, không bằng lời.

⇒ Thứ làm điều này hoạt động là **prompt cho writer một cách hợp lệ để nói "tôi không biết"**: khối `SUMMARY`, nhãn `[* suy luận]`, `TBD` + điều kiện escalate, `PARTIAL`. Không có những lối ra đó, writer chỉ còn hai chọn lựa — **bịa** hoặc **im lặng** — và cả hai đều đắt hơn nhiều.

## 4. Tài liệu liên quan

- [Brief](./brief.md) · [Run plan](./run-plan.md) · [Outline](./outline.md) · [Escalations](./escalations.md)
- [cost.md của run trước](../2026-08-23-khoi-tao-tai-lieu-planning-comic-studio/cost.md) — nguồn của 5 bài học đã áp vào run này
