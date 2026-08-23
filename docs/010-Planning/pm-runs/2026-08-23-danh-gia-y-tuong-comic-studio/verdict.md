# Verdict: 2026-08-23-danh-gia-y-tuong-comic-studio

**Bước 6 — Verification & Close.** Verifier: `context-auditor`, agent **không tham gia** bất kỳ phần nào của run (không viết, không phân tích, không được cấp file nào — read-only tuyệt đối).

| | |
|---|---|
| **STATUS của verifier** | `PASS_WITH_ISSUES` |
| **CRITICAL** | **0** |
| **MAJOR** | 4 — **đã sửa 4/4** |
| **MINOR** | 9 — **đã sửa 8, 1 tự giải quyết** |
| **Quyết định của PM** | **Đóng run.** 0 CRITICAL ⇒ không kích hoạt điều khoản "quay lại Bước 5" của `pm-doc.md`. PM tự vá (harness chặn subagent ghi file — cùng đường đã tạo ra một nửa tài liệu). |
| **Chi phí verify** | 165.877 token, 33 tool call, 13,5 phút |

---

## 1. Bốn tiêu chí

| Tiêu chí | Kết quả | Bằng chứng verifier đưa ra |
|---|---|---|
| **Completeness** | ✅ Đạt | 16/16 mục có mặt, đếm khớp block `CẤU TRÚC CHỐT`. Toàn bộ sub-section khớp 1:1 (3.1–3.3, 4.1–4.4, 5.1–5.7, 6.1–6.4, 8.1–8.5, 9b.1–9b.4). Frontmatter đủ 4 trường bắt buộc. Verifier đi qua **từng dòng** bảng *Ràng buộc bổ sung* và xác nhận không ràng buộc nào bị bỏ. Không mục nào rỗng. |
| **Correctness** | ⚠️ Đạt, 4 issue | **17 phép tính kiểm lại độc lập — đúng toàn bộ tới từng % làm tròn.** 3 citation chịu lực trace 1:1 về findings, **caveat còn nguyên**, không conflate NĐ 134/2026 với Luật 134/2025 ở cả 5 lần xuất hiện. Không tìm được khẳng định định lượng nào không có căn cứ. Bốn issue đều là **thiếu** hoặc **mất nhãn**, không phải sai. |
| **Coherence** | ✅ Đạt | Không mâu thuẫn thực chất. §5↔§6 chỉ có một giao điểm (Layout Score) và tài liệu **tự giải thích** vì sao nó nằm ở cả hai. §3 verdict khớp §12. Thuật ngữ: mỗi khái niệm dùng **đúng một tên** xuyên suốt, không synonym drift. |
| **Connectivity** | ⚠️ Đạt sau close-step | 0 wiki-link `[[...]]` (RULE-001). 4/4 relative link phân giải được. **Orphan tại thời điểm verify** — đã sửa ở close-step. |

---

## 2. Disposition từng issue

### MAJOR

| # | Vấn đề | Disposition |
|---|---|---|
| 1 | Dòng 878: `$8,04` dùng làm số sống, **mất nhãn** "tính ở hệ số 2x đã bị E2 phủ định". Nguồn `architect.md:788,796` **có** nhãn `@2x`. Vi phạm đúng bài học mà chính dòng 794 vừa dạy | ✅ **Đã sửa** — chèn một blockquote `[!NOTE]` gắn nhãn, **cố ý không quy đổi sang N=3** đúng như verifier đề xuất: đoạn ngay dưới đã chứng minh câu hỏi two-pass là moot, quy đổi một phép so sánh đã mất hiệu lực chỉ tạo ấn tượng sai rằng nó còn đáng so |
| 2 | Khuyến nghị **Điều 37b opt-out check** rơi mất hoàn toàn (`grep opt-out` = 0). Chi phí ~0, xoá được một nhánh rủi ro pháp lý | ✅ **Đã sửa** — thêm **item 6** vào checklist §8.3 kèm lập luận điều kiện đầy đủ, **và** một blockquote giải thích vì sao nó **không** xung đột với nghịch lý safe harbour (đọc nhãn tường minh do chủ quyền gắn vào file ≠ tự suy đoán về quyền người khác). Thêm vào §10 MVP1 — đúng chỗ, vì ingest là nơi file user lần đầu vào hệ thống |
| 3 | **Speaker attribution** rơi mất hoàn toàn. Lỗi 30-50% (3+ người) / 40-60% (câu ngắn), và là **một trong HAI** human gate bắt buộc ở MVP2 — tài liệu chỉ phủ gate còn lại | ✅ **Đã sửa** — thêm mục mới **§5.4b** với bảng tỉ lệ lỗi (đánh dấu rõ là **ước lượng**, không phải số đo), bốn tầng khắc phục, và lập luận chi phí lỗi bất đối xứng. Thêm hai human gate tường minh vào §10 MVP2. Bổ sung entry vào Mục lục |
| 4 | Tài liệu **orphan** — `Research-MOC.md` chưa trỏ tới | ✅ **Đã sửa ở close-step** — thêm entry có mô tả vào `Research-MOC.md`, bump `updated`. Nhân thể đánh dấu 2 link chết sẵn có trong MOC (`Competitor-Analysis/`, `User-Interviews/`) là placeholder chưa tồn tại — **không xoá**, đúng guardrail |

### MINOR

| # | Vấn đề | Disposition |
|---|---|---|
| 5 | §1 nói "bảy điều kiện", §4.1 thêm "hai điều kiện cùng mức bắt buộc" ⇒ thực tế **9** | ✅ **Sửa cả hai đầu** — §1 nói rõ "bảy + hai = chín"; §4.1 thêm blockquote `[!IMPORTANT]` giải thích vì sao tiêu đề giữ chữ "BẢY" (là số của một lens cụ thể, truy vết được) nhưng số phải thoả là chín. Đánh số (8) và (9) cho hai điều kiện kỹ thuật |
| 6 | MVP0: hàng *Model* ghi "batch API" nhưng hàng *Chi phí* tính ở giá standard | ✅ **Đã sửa** — tách thành hàng riêng *Giá dùng để tính*: ~$12 ở standard $0.134, ~$6 nếu batch; nói rõ lấy số cao làm **trần an toàn** và vì sao (cần vòng lặp nhanh thì batch không dùng được) |
| 7 | Mất con số độ phủ checker **40-60% số panel** + chỉ thị *"nói rõ với user, đừng để họ hiểu là đã được bảo vệ toàn diện"* | ✅ **Đã sửa** — thêm block ⚠️ vào §5.2 nêu độ phủ và biến nó thành **yêu cầu giao tiếp sản phẩm**, nối vào đúng cơ chế tự sát của checker đã mô tả ở lập luận (c) |
| 8 | *"tám ngày sau ngày viết"* — từ 23/08 tới 01/09/2026 là **chín** ngày | ✅ **Đã sửa** |
| 9 | Dòng 1008 khẳng định run-state chứa `verdict.md`, `cost.md` — chưa tồn tại | ✅ **Tự giải quyết** — cả hai file được tạo ở close-step này |
| 10 | `id: ANALYSIS-001` nhưng `type: research`; RULE-001 quy định `id: {TYPE}-{NNN}` | ✅ **Đã sửa** — grep toàn repo trước khi đổi: chỉ 2 chỗ tham chiếu, **cả hai là file của run này**. Đổi thành `id: RESEARCH-001` ở cả deliverable và `outline.md`. Giữ `type: research` vì khớp Document Type Mapping của thư mục `050-Research/` |
| 11 | ToC thiếu 6 heading H3 có thật | ✅ **Đã sửa** — bổ sung 2 H3 của §10, 4 H3 của §11, và §5.4b mới. §Tài liệu tham khảo khai tường minh là "chỉ liệt kê tới cấp mục" |
| 12 | `Comic IR` dùng 8 lần, **chưa bao giờ** expand acronym | ✅ **Đã sửa** — expand ở lần dùng đầu tiên (§3.3) |
| 13 | Bảng CogCanvas: UNO có `19.60` ở **cả hai** hàng 3 và 4 — bất thường thống kê. Verifier **không có WebFetch** nên không kiểm được nguyên văn | ✅ **Đã verify bằng nguồn gốc** — PM fetch trực tiếp Table 2 của [arXiv 2606.15867](https://arxiv.org/html/2606.15867v1): cặp `19.60/19.60` (ID-Sim) và cặp `14.65/14.65` (Attr-VQA) **đúng như in trong paper**. Nhãn cột cũng đối chiếu: paper đánh theo group size **N=2..5**, khớp cột 2-5 của tài liệu — **không lệch một bậc**. Thêm blockquote ghi lại việc xác minh để người đọc sau không nghi ngờ nhầm |

---

## 3. Nguyên nhân gốc — và nó đã được sửa ở đâu

Verifier quy trách chính xác, và điểm này quan trọng hơn bản thân hai issue:

> *"cả (1) và (2) **không** có trong bảng ràng buộc của block `CẤU TRÚC CHỐT`. Writer tuân thủ contract đúng; chỗ rơi nằm ở **bước lập outline**, không phải ở writer."*

MAJOR #2 và #3 **không phải writer deviation**. Vá deliverable mà không sửa `outline.md` là chữa triệu chứng — lần dispatch sau sẽ rơi lại đúng chỗ đó. Vì vậy cùng lượt vá này:

- Bảng *Ràng buộc bổ sung* trong `outline.md` đã được cập nhật: thêm hàng **§5.4b**, sửa §8.3 từ "checklist 5 điểm" thành **6 điểm** kèm nội dung item 6, sửa §4.1 (bảy → nói rõ tổng chín), bổ sung §10.
- `outline.md` có thêm block **`# BÀI HỌC GỐC — vì sao hai khuyến nghị bị rơi`**, phân tích cơ chế lỗi: PM lập bảng ràng buộc bằng cách trích những điểm **sắc nhất** (gây tranh luận, đảo kết luận, có con số gây sốc) — và **bộ lọc "sắc" không phải bộ lọc "quan trọng"**. Cả hai khuyến nghị bị rơi đều rẻ và không gây tranh cãi, tức là loại dễ rơi nhất và cũng đáng làm nhất.
- Kèm đề xuất sửa quy trình: sau khi trích điểm sắc, chạy thêm **một lượt quét cơ học** qua từng heading của từng findings, đánh dấu heading nào chưa xuất hiện trong bảng ràng buộc.

**Một hạn chế của chính `pm-doc.md` cần ghi lại:** bốn tiêu chí Bước 6 **không** bắt loại lỗi này một cách hiển nhiên — *Correctness* được định nghĩa là "nội dung khớp Nguồn sự thật, không có khẳng định không có căn cứ", tức là bắt **thừa**, không bắt **thiếu**. `context-auditor` bắt được vì nó **tự chủ động** grep findings tìm khuyến nghị không xuất hiện trong doc. Hành vi đó nên trở thành yêu cầu tường minh trong mọi dispatch verify sau: *"liệt kê khuyến nghị có trong findings mà KHÔNG có trong deliverable"*.

---

## 4. Close-step — RULE-001 Validation Checklist

| Hạng mục | Trạng thái |
|---|---|
| Đúng thư mục theo Document Type Mapping | ✅ `docs/050-Research/Analysis-{Topic}.md` |
| Naming convention | ✅ |
| Frontmatter `id / type / status / created` | ✅ + `updated: 2026-08-23` sau vòng vá |
| Standard markdown link, **không** wiki-link | ✅ 0 occurrence `[[` |
| Link phân giải được | ✅ 4/4 trong deliverable; link mới trong Glossary đã sửa đường dẫn RULE-001 sang `knowledge-base/` sau khi `ls` xác nhận nó không nằm trong `docs/999-Resources/Templates/` |
| MOC thư mục cha đã cập nhật | ✅ `Research-MOC.md`, `updated` bumped |
| Glossary | ✅ **~40 term domain** thêm vào `docs/999-Resources/Glossary.md`, chia 7 nhóm, giữ nguyên 3 term OTP cũ, `updated` bumped. Vượt danh sách P1 (5 term) của verifier — đã lấy hết P1+P2 và phần lớn P3 |
| `docs/000-Index.md` | ⛔ **Không tạo.** File **không tồn tại** trong repo dù RULE-001 ghi "BẮT BUỘC phải có". Hai lý do không tạo trong run này: (a) `pm-doc.md` chỉ yêu cầu cập nhật nó cho **tài liệu lớn** (PRD, SDD, MTP, Roadmap) — Analysis là `type: research`, không thuộc danh sách; (b) `brief.md` §*Nợ kỹ thuật NGOÀI scope* đã ghi nhận nó **trước** run. Tạo một index toàn repo là việc của một run riêng, không phải phần đuôi của một run phân tích |
| Tài liệu bị thay thế → `090-Archive/` | — không có |

---

## 5. Ba điểm verifier chủ động ghi nhận là tốt

Trích lại vì chúng là tiêu chí chất lượng đáng giữ cho các run sau, không phải lời khen:

1. **Mọi caveat "không có dữ liệu" đều sống sót** từ findings sang deliverable — *kể cả những caveat làm yếu chính luận điểm của deliverable*. Verifier kiểm riêng điểm này và không tìm được chỗ nào một khoảng trống bị phát biểu thành số chắc chắn.
2. **§9b.1 tự khai lỗi tính của PM** thay vì im lặng sửa. Verifier đánh giá điều này *"làm tăng độ tin cậy của toàn bộ phần kinh tế"*.
3. **§6.1 và §6.4 trình bày tranh luận có kết luận và tự thu hồi khuyến nghị**, giữ lại dấu vết quyết định — *"đúng thứ mà một tài liệu quyết-định-build cần, và là thứ khó nhất để một writer chịu viết"*.

---

## 6. Kết luận

**Run đóng.** Deliverable ở `status: draft` — đúng trạng thái đích đã khai trong `outline.md`, và đúng bản chất: tài liệu này kết luận rằng **ba việc phải làm trước dòng code đầu tiên**, trong đó có việc mang ba câu hỏi §8.5 tới luật sư SHTT Việt Nam. Nó chuyển sang `status: approved` khi anh đã quyết định build / không build, không phải khi nó được viết xong.

Xem thêm: [outline.md](./outline.md) · [escalations.md](./escalations.md) · [cost.md](./cost.md) · [brief.md](./brief.md) · deliverable: [Analysis-Comic-Studio-Concept](../../../050-Research/Analysis-Comic-Studio-Concept.md)
