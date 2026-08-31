# Findings — business-analyst

## Kết luận của worker

> **Lens**: nghiệp vụ. Câu hỏi em trả lời là *"sản phẩm này có những bề mặt UI nào, lấy từ Use Case và Story đã viết"* — ⛔ không phải *"một Design System thường có gì"*.
>
> **Kỷ luật áp cho toàn bộ tài liệu này**: mọi hàng đều có cột nguồn trỏ về một UC + mã flow (`EXC-n` / `EX-n` / `EF-n` / `AF-n` / `ALT-n`) hoặc một mã requirement (`SRS-FR-nn` / `SRS-NFR-nn`). Hàng không truy được nguồn nằm riêng ở [§1.4](#14-suy-luận-chưa-có-nguồn--đọc-riêng-đừng-trộn-vào-bảng-trên) và được dán nhãn **suy luận**.
>
> ⚠️ **Copy số thì copy cả nhãn** (`CẤM-15`): `[OFF]` paper/văn bản gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` thứ cấp · `[EM]` **ước lượng, không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.

### Mục lục

1. [Bảng bề mặt UI (UI surface inventory)](#1-bảng-bề-mặt-ui-ui-surface-inventory)
2. [Component inventory tối thiểu](#2-component-inventory-tối-thiểu)
3. [NFR và requirement chạm trực tiếp vào UI](#3-nfr-và-requirement-chạm-trực-tiếp-vào-ui)
4. [Khoảng trống persona](#4-khoảng-trống-persona--nói-thẳng-không-lấp)
5. [Vấn đề phát hiện trong tài liệu nguồn (report-only)](#5-vấn-đề-phát-hiện-trong-tài-liệu-nguồn--report-only-em-không-sửa)
6. [Handoff cho PM](#6-handoff-cho-pm)
7. [Tài liệu tham khảo](#7-tài-liệu-tham-khảo)

---

## 1. Bảng bề mặt UI (UI surface inventory)

**Đã đọc đủ 11/11 UC, cả Main flow, Alternative flow và Exception flow.** Xác nhận nhận định của `000-Index.md`: **không UC nào có Exception flow rỗng** — tổng cộng **67 nhánh ngoại lệ** trên 11 UC (UC-01: 6 · UC-02: 7 · UC-03: 6 · UC-04: 7 · UC-05: 6 · UC-06: 7 · UC-07: 8 · UC-08: 7 · UC-09: 5 · UC-10: 6 · UC-11: 5).

> ⭐ **Phát hiện quan trọng nhất của lens này**: nguồn của trạng thái UI trong repo này **không nằm ở Main flow**. Main flow của 11 UC hầu như chỉ mô tả happy path một chiều; **toàn bộ** trạng thái `error` / `empty` / `blocked` / `pending` / `partial` nằm ở Exception flow. Một Design System viết từ Main flow sẽ thiếu đúng phần đắt nhất.

### 1.1 Bảng chi tiết theo Use Case

| Surface | UC nguồn | Actor | Component chính cần có | Trạng thái phải có |
|---|---|---|---|---|
| **S-01** — Chọn / tạo tác phẩm | `UC-01` Main flow b1 | Tác giả truyện chữ | List tác phẩm · nút tạo mới | ⚠️ **UC không mô tả** trạng thái nào cho bề mặt này (chỉ một dòng *"chọn tác phẩm hoặc tạo tác phẩm mới"*) |
| **S-02** — Upload chapter | `UC-01` b2, b3 · `ALT-2` · `EXC-2`, `EXC-3`, `EXC-5` · `SRS-FR-41` | Tác giả truyện chữ | **File input** + **paste text** (hai đường nạp, `ALT-2`) · form khai `timeline_id` + `story_order` · ⭐ **checkbox cam kết quyền (*user warrant*) gắn vào BƯỚC UPLOAD, không chỉ ở trang ToS** | `form-invalid / blocked`: chưa tick checkbox ⇒ **upload không được nhận** (`EXC-2`) · `error`: file không đọc được / sai định dạng / rỗng sau `text clean`, **báo lý do cụ thể** (`EXC-3`) · `conflict`: trùng `timeline_id`+`story_order` ⇒ **bắt chọn** *thay thế* hay *huỷ*, ⛔ **không âm thầm ghi đè** (`EXC-5`) |
| **S-03** — Kết quả ingest | `UC-01` b9, b10 · `EXC-1`, `EXC-4` · `ALT-3` | Tác giả truyện chữ · Hệ thống | Panel tóm tắt **những gì `text clean` đã loại bỏ** (bắt buộc hiển thị, `EXC-4`) · kết quả phép kiểm opt-out · nút chấp nhận / từ chối | `loading`: pipeline b4–b8 chạy · ⛔ `hard-block`: phát hiện opt-out signal Điều 37b ⇒ **hệ thống CHẶN**, thông báo nêu rõ nội dung có bảo lưu quyền, **không có đường cấu hình bỏ qua** (`EXC-1`, `KC-6`) · `rejected-by-user` ⇒ quay lại b2 (`ALT-3`) |
| **S-04** — Story Bible editor | `UC-02` b5–b8, b11 · `BR-004-01` · `MVP-Scope §5.2` #5 | Tác giả truyện chữ | ⛔ **form + list, KHÔNG canvas, KHÔNG graph editor** (ràng buộc tường minh) · list nhân vật / trang phục / địa điểm · viewer state-theo-event · **truy vấn theo thời điểm** (*"tại chương 40, X mặc gì"*) · **provenance badge mức field** (`field_provenance`, `KC-3`, b4) | `empty`: extraction rỗng ⇒ hiển thị **danh sách rỗng**, ⛔ **cấm tạo entity rác để "có gì đó hiển thị"** (`EXC-1`) · `error + retry` hoặc fallback khai tay (`EXC-1`, `ALT-2`) · `conflict-must-resolve`: hai event mâu thuẫn ⇒ **buộc tác giả chọn**, `resolveState()` **không được đoán** (`EXC-4`) · `warning-not-dismissible`: sửa `story_order` của event đã có panel ⇒ cảnh báo **phải hiện, không được ẩn** (`EXC-5`, `R-15`) · `rollback`: ghi `change_log` fail ⇒ transaction rollback, field **không** được sửa (`EXC-6`) · `destructive-confirm`: xoá toàn bộ dữ liệu tác phẩm (`EXC-7`) |
| **S-05** — Panel script reviewer (Comic IR) | `UC-03` b8, b9 · `ALT-3` | Tác giả truyện chữ | View theo **page**: thứ tự đọc · kích cỡ tương đối panel · nhân vật có mặt · camera · control sửa: đổi nhân vật / camera / gộp-tách panel / đổi `beat_type` · phạm vi thao tác **một page** cũng hợp lệ (`ALT-3`) | ⛔ `db-reject`: sửa panel thành ≥4 nhân vật ⇒ **tầng DB TỪ CHỐI**, ⚠️ **KHÔNG phải cảnh báo rồi cho qua**; kèm gợi ý đường giải hợp lệ **shot xa / silhouette / crop** (`EXC-1`, `M2-2`, `BR-003-07`) · `error + retry` hoặc fallback viết tay, ⛔ **không sinh panel script rỗng** (`EXC-2`) · `blocked-downstream`: thiếu `text_safe_zone` ⇒ panel **không được đi tiếp** sang typeset (`EXC-3`) · `silent-wrong`: state sai vì khoá thời gian sai — **không crash, chỉ sai âm thầm**, chỉ phát hiện bằng mắt ở b8 (`EXC-4`) · `quota-exhausted`: emphasis quota cạn ⇒ **buộc hạ một panel khác xuống** (`EXC-5`) · `rollback` (`EXC-6`) |
| **S-06** — Human gate #1: speaker attribution | `UC-04` b3–b8 · `SRS-FR-14` · `MVP-Scope §3 C7` | Tác giả truyện chữ | List dòng thoại + speaker được LLM **đề xuất** · control *xác nhận* / *gán lại* · ⭐ **counter số dòng còn `chưa xác nhận`** (b7) · cờ `speaker_confidence` thấp (`SRS-FR-14`) · giá trị `UNKNOWN` là **hợp lệ** | ⭐ `unconfirmed` là **trạng thái mặc định của MỌI dòng** — ⛔ *"đã xác nhận"* **không bao giờ là mặc định** (b3) · `no-suggestion`: LLM không gán được ⇒ hiển thị **không có đề xuất**, buộc gán tay, **không có đường bỏ trống** (`EXC-1`) · `high-risk-flagged`: câu ngắn/thán từ ⇒ đánh dấu rủi ro cao + hiện **ngữ cảnh trước/sau** (`EXC-2`) · ⛔ `publish-rejected`: cố xuất bản khi còn dòng chưa xác nhận ⇒ **TỪ CHỐI ở tầng pipeline, không phải cảnh báo ở tầng UI**; page giữ `pending` (`EXC-3`) · `invalidated`: panel script bị sửa sau khi đã xác nhận ⇒ dòng thoại **quay về `chưa xác nhận`** kèm lý do (`EXC-4`) · `pending`: rời giữa chừng ⇒ **không timeout, không auto-approve** (`EXC-5`) · `rollback` (`EXC-6`) · ⭐ `partial`: trạng thái đúng để hiển thị là ***"gate 1/2 đã xong"***, ⛔ **không phải *"đã sẵn sàng xuất bản"*** (`EXC-7`) |
| **S-07** — Human gate #2: dialogue condensation | `UC-05` b5–b10 · `BR-003-11` | Tác giả truyện chữ | ⭐ **Diff / side-by-side từng cặp `gốc → nén`** theo thứ tự đọc · ba control loại trừ nhau: *chấp nhận* / *sửa tay* / *yêu cầu nén lại* · cờ dòng **vẫn vượt `text_budget`** sau khi nén · chỉ báo gate `OPEN` / `PASS` | `over-budget-reject`: bản nén hoặc bản sửa tay vẫn vượt `text_budget` ⇒ **từ chối đánh dấu đã quyết**, **nêu rõ mức vượt** (`EX-1`) · `rejected-meaning`: mất nghĩa ⇒ ⛔ **không auto-accept sau n lần reject, không hạ tiêu chuẩn, không đề nghị "tạm chấp nhận và sửa sau"** (`EX-2`) · `llm-error + retry`, ⛔ **không có nhánh "LLM lỗi nên bỏ qua gate"** (`EX-3`) · ⭐ `gate-reset-to-OPEN`: layout đổi ⇒ `text_budget` đổi ⇒ **reset gate về OPEN** cho panel bị ảnh hưởng (`EX-4`) · `gate-reset` khi thoại bị sửa ở `UC-07` (`EX-5`) · `session-interrupted`: dòng đã quyết giữ, dòng chưa quyết vẫn chưa quyết, **không timeout dẫn tới auto-approve** (`EX-6`) · `empty-pass`: trang không có dòng thoại ⇒ PASS hợp lệ do **tập rỗng** (`AF-4`) |
| **S-08** — Panel card | `UC-06` b1 · `BR-004-05` · `MVP-Scope §5.2` #1 | Tác giả truyện chữ | Form `Panel Specification` + preview + nút `Generate` / `Regenerate` · ⭐ **hiển thị chi phí TRƯỚC khi tiêu**: hold **3 credit/panel** (`KC-7`, b4) | `loading` dài: generation *"mất hàng chục giây"* (`SRS-NFR-06` — polling **2 giây**) · `insufficient-credit`: **TỪ CHỐI enqueue, không gọi provider**, nêu rõ còn thiếu bao nhiêu (`EX-2` · `UC-10` `EF-1`) · `spec-invalid`: panel 4 nhân vật **không tới được bước 1** — bị DB từ chối (`EX-3`) · ⭐ `irreversible-warning`: **không có undo qua generation**, `Regenerate` **tiêu tiền thật, không hoàn lại** — *"UX phải nói rõ điều này, không để actor suy đoán"* (`EX-6`, `BR-004-08`) |
| **S-09** — Variant picker | `UC-06` b7–b9 · `AF-2` · `MVP-Scope §5.2` #1 · **MVP3** | Tác giả truyện chữ · VLM (đề xuất) | ⭐ **3 candidate hiển thị cùng lúc** (N=3 là mặc định cho **mọi** panel, `CF-3.1` `[OFF]`) · **preselect của VLM** phân biệt được với **lựa chọn của người** · control override · ⭐ *"hành động CHỌN là `authorship`"* | `candidate-failed`: candidate lỗi/timeout/bị provider từ chối ⇒ **retry đúng lời gọi đã lỗi**, mục tiêu vẫn là **đủ 3** (`EX-1`) · `candidate-invalid`: candidate **có chữ nướng vào pixel** ⇒ coi là FAIL, **không được đưa lên picker** (`EX-4`, `G1-e`) · `regenerate-cost-warning`: lượt mới **hold thêm 3 credit**, tiêu tiền thật (`AF-3`) |
| **S-10** — Bubble / text overlay editor (trong **MỘT** panel) | `UC-07` b2–b6 · `MVP-Scope §5.2` #2 · `SRS-FR-16` | Tác giả truyện chữ | Ảnh panel **không chữ** làm nền + **`typeset layer` tách rời** phía trên · **hiển thị `text_safe_zone`** như vùng giữ trống · 4 thao tác (và **chỉ** 4): kéo bubble · sửa thoại · chọn kiểu bubble · kéo đuôi trỏ (tail) · undo **cục bộ** | `warning`: bubble đè ra ngoài `text_safe_zone` / che mặt ⇒ **cảnh báo + chỉ rõ vùng vi phạm**, actor có quyền chấp nhận có ý thức — ⚠️ **đây là CẢNH BÁO (`M2-3`, ≥95% `[EM]`), ⛔ không nhầm với TỪ CHỐI ở tầng DB (`M2-2`)** (`EX-1`) · `over-budget`: báo **mức vượt** + **ba đường xử lý** (`EX-2`) · `refused`: undo qua generation ⇒ **từ chối**, nói rõ lý do (`EX-3`) · `refused`: sửa pixel / inpainting ⇒ **không có công cụ nào làm được** (`EX-4`, D5 hoãn) · `boundary-constraint`: kéo bubble ra ngoài khung ⇒ **giới hạn trong khung panel đang mở** (`EX-5`, D2 hoãn) · `gate-reset` khi sửa nội dung thoại (b10, `EX-6`) · `db-reject` khi thêm nhân vật thứ 4 (`EX-7`) · ⚠️ `TBD`: ảnh panel bị thay sau khi đặt bubble ⇒ **nguồn KHÔNG phát biểu hành vi hệ thống** (`EX-8`) |
| **S-11** — Page layout editor | `UC-08` b1–b9 · `BR-004-02`, `BR-004-07` · `MVP-Scope §5.2` #3 | Tác giả truyện chữ · Layout Director | **Template picker** · ⭐ **swap / reorder RỜI RẠC giữa các ô** — *"chọn ô, không phải kéo hình học liên tục"* · hiển thị thứ tự đọc · đề xuất diện tích theo **rubric `beat_type` + emphasis quota** · ⛔ **không có điểm số thực nào được tính, hiển thị hay lưu** (`SRS-NFR-22`, `C4` cắt hẳn) | `template-reject`: template không đủ ô ⇒ **từ chối áp**, **nêu rõ số ô so với số panel**, ⛔ không tự nhồi 2 panel vào 1 ô, không tự bỏ panel (`EX-1`) · ⭐ `gate-reset`: đổi layout sau khi gate #2 PASS ⇒ **reset gate #2 về OPEN** (`EX-2`) · `refused`: hình học tự do / xoay / chồng lấn / zoom-pan chapter (`EX-3`, D2 hoãn) · `refused`: yêu cầu điểm số layout (`EX-4`) · `spec-error`: panel thiếu `text_safe_zone` ⇒ **trang không được coi là đã sắp xong** (`EX-5`) · `db-reject` (`EX-6`) · `quota-exhausted`: emphasis quota chapter hết ⇒ đổi chỗ hoặc giữ bố cục đều (`AF-2`) · ⚠️ `no-change-no-evidence`: giữ nguyên đề xuất Director ⇒ **không sinh `change_log`** ⇒ trang đó **không có bằng chứng đóng góp** của actor (`AF-1`) |
| **S-12** — Preview trang / chapter | `UC-08` b10–b13 · `AF-3`, `AF-6` · `BR-004-03` | Tác giả truyện chữ · compositor | Viewer **composite server-side, READ-ONLY** (PNG/PDF) · phạm vi **trang** hoặc **cả chapter** (`AF-3`) · dùng **chung compositor với export** (`H4`) | ⭐ `empty-slot`: panel **chưa có ảnh** ⇒ hiện dạng **ô trống**, preview vẫn render được (`AF-6`) — *đây là empty state duy nhất trong repo được mô tả tường minh ở mức hiển thị* · `error + retry`: render preview lỗi/timeout ⇒ **read-only nên không hỏng dữ liệu**, ⛔ không có nhánh *"coi như đã xem và cho xuất bản"* (`EX-7`) · ⭐ `preview ≠ publishable`: **preview KHÔNG mở đường xuất bản** ⇒ phải phân biệt được hai trạng thái này trên UI (b13, `M2-4`) |
| **S-13** — Export chapter | `UC-09` b1–b10 · `BR-008-11`, `BR-008-12` | Tác giả truyện chữ | List **định dạng khả dụng theo mốc**: MVP2 = PDF · **CBZ / webtoon hiển thị là *chưa có*** — ⚠️ **không phải lỗi** (b4, `EF-2`) · nút xác nhận export · trả file tải về | ⭐ `blocked-by-gate` (**nhánh load-bearing của cả UC**): còn ≥1 page chưa qua đủ **hai** gate ⇒ **TỪ CHỐI**, **liệt kê page nào thiếu gate nào**, **điều hướng về `UC-04`/`UC-05`**; ⛔ không có cờ *"export nháp"*, *"bỏ qua kiểm tra"*, không quyền admin nào vượt được (`EF-1`, `M2-4`) · `unavailable-format` (`EF-2`) · `blocked-by-takedown`: project ở trạng thái `disable-access` ⇒ từ chối + ghi lại lần từ chối (`EF-3`) · `incomplete-data`: panel thiếu `approved_generation_id` ⇒ **báo rõ page/panel nào**, không trả file một phần (`EF-4`) · `composite-failed`: **không trả file dở** (`EF-5`); ⚠️ SLA/uptime của export là **`TBD`** (`BRD-008` `TBD-4`) · ⚠️ `TBD`: export **từng phần** (chỉ page đã qua gate) — **repo KHÔNG trả lời** (`AF-4`) |
| **S-14** — Quản lý credit ⚠️ **NGOÀI HORIZON** | `UC-10` b1, b2, b12 · `BR-006-01`, `BR-006-03` · **MVP3** | Tác giả truyện chữ | ⭐ **BA số tách bạch**: credit `available` · credit **đang bị HOLD** · mức tiêu theo `usage_daily`. ⛔ **Không gộp `available` với credit đang hold** — *"đó chính là nguồn của cảm giác **có credit mà không generate được**"* | `insufficient-balance`: **TỪ CHỐI trước enqueue**, nêu rõ cần thêm bao nhiêu (`EF-1`) · `hold-stuck`: hold treo do thiếu reaper ⇒ **loại lỗi khó chẩn đoán nhất** (`EF-3`) · ⚠️ `credit-lost`: reaper thu hồi hold của job còn sống ⇒ *"user mất credit oan"* — cơ chế phân biệt và chu kỳ reaper là **`TBD`** (`EF-5`) |
| **S-15** — Mua credit pack ⚠️ **NGOÀI HORIZON** | `UC-10` b3–b6 · `MVP-Scope §3 E4` | Tác giả truyện chữ · Vendor billing (**hệ thống ngoài**) | ⛔ **Bề mặt thanh toán do VENDOR sở hữu** — `E4` = *"mua billing, không tự viết"* ⇒ Design System **không** đặc tả màn hình thanh toán, chỉ đặc tả **điểm bàn giao** và cách giữ nhất quán thương hiệu qua ranh giới đó | `payment-failed`: **không ghi dòng nạp nào** vào ledger (append-only ⇒ ghi sai không xoá được) (`EF-6`) |
| **S-16** — Bật BYOK ⚠️ **NGOÀI HORIZON (MVP4)** | `UC-10` `AF-1`, `EF-4` · `BR-006-05` · `CF-2.4` `[CHỐT]` | Tác giả truyện chữ (power user) | Nhập API key của provider · ⛔ **là đường MỞ KHOÁ, KHÔNG phải cửa vào, KHÔNG phải điều kiện dùng sản phẩm** ⇒ vị trí trong information architecture phải phản ánh điều đó | ⭐ `byok-failed`: key sai / hết hiệu lực / hết quota ⇒ thông điệp lỗi phải **nêu rõ đây là giới hạn của key của user, KHÔNG phải lỗi truyện của họ**, và **đưa đường lui về Tầng 2 hoặc Tầng 1** (`EF-4`). ⚠️ *Onboarding BYOK là **rủi ro sản phẩm số 1** với người dùng non-technical* (`Glossary` *BYOK*); ⛔ độ lớn ma sát **không đo được** (`G-08`) ⇒ **không gán tỉ lệ drop-off** |
| **S-17** — Công cụ tiếp nhận takedown (**CÔNG KHAI**) | `UC-11` b2 · `BR-007-04` (a) · `SRS-FR-38` | ⚠️ **Chủ sở hữu quyền — BÊN NGOÀI HỆ THỐNG** | ⭐ **Form công khai + email `copyright@`** · ⛔ **không đăng ký tài khoản, không đăng nhập, không tenant context** ⇒ đây là **shell khác** với toàn bộ sản phẩm; *"phải công khai và dùng được bởi người chưa từng biết sản phẩm"* | `request-incomplete`: thông tin không đủ ⇒ yêu cầu bổ sung. ⚠️ **`TBD` hai thứ**: (a) **danh sách trường bắt buộc** của yêu cầu hợp lệ; (b) **`SLA 72 giờ` có tạm dừng khi chờ bổ sung hay không** — *"không nguồn nào trong repo nói, không tự phân xử"* (`EF-1`) |
| **S-18** — Xác nhận đã nhận takedown | `UC-11` b3, b4, b10 · `BR-007-04` (a) | Hệ thống → chủ sở hữu quyền | Xác nhận gửi về địa chỉ liên hệ + ⭐ **timestamp tiếp nhận** (mốc bắt đầu đếm SLA **72 giờ** `[OFF]` **tóm tắt**) — *"công cụ tiếp nhận phải là một đường hai chiều, không phải một hộp thư đen"* | ⚠️ `over-SLA`: quá 72 giờ ⇒ điều kiện miễn trừ Điều 198b có nguy cơ không thoả; **bus factor = 1**, không có người thứ hai (`EF-2`, `R-02`) · `content-already-hard-deleted` (`EF-3`) |
| **S-19** — Bề mặt operator của Founder | `UC-01` `EXC-1` (rà log opt-out) · `UC-09` `AF-2` (export hồ sơ tenant khi KILL) · `UC-10` `AF-3`, `AF-4`, `EF-3`, `EF-5` (hold reaper, hard quota, đo `G2-d`) · `UC-11` b5–b9 (đánh giá, soft-delete, phản hồi) | Founder ở vai **operator** | ⚠️ **KHÔNG UC NÀO MÔ TẢ MÀN HÌNH OPERATOR.** Sáu UC gọi tên **hành động** của operator nhưng không UC nào nói bề mặt đó trông thế nào, ở đâu, hay có phải một app riêng không | ⛔ **Anti-feature bắt buộc**: hệ thống **KHÔNG quét, KHÔNG flag, KHÔNG chấm điểm nghi vấn** bản quyền (`UC-11` `EF-4`, `SRS-NFR-15`, `R-04`) — đây là một **negative requirement lên UI**: một dashboard *"nội dung khả nghi"* sẽ **phá miễn trừ Điều 198b**. ⚠️ Counter-notice: **thủ tục là `TBD`** ⇒ ⛔ **không thiết kế màn hình counter-notice** (`AF-1`) |

### 1.2 Bề mặt xuyên suốt — không thuộc riêng UC nào, nhưng mọi UC đều chạm

| Surface | Nguồn | Component chính cần có | Trạng thái phải có |
|---|---|---|---|
| **X-1** — Chỉ báo trạng thái job | `SRS-NFR-06` · `SRS §4.1` | Cập nhật bằng **polling 2 giây**, ⛔ không WebSocket | Nhịp 2s là ràng buộc thiết kế thật: loading pattern **phải chịu được re-render mỗi 2 giây** mà không nhấp nháy |
| **X-2** — Chỉ báo AI disclosure | ⭐ `SRS-FR-40` · `Story-AI-Disclosure-Article-11` AC-1 | *"Chỉ dẫn/thông báo hiển thị cho người dùng **tại điểm tương tác với tính năng AI** (ví dụ tại bước generate/pick variant), **không phải chỉ ghi trong ToS**"* | Xem [§3.3](#33--ai-disclosure-có-buộc-phải-có-bề-mặt-ui--câu-trả-lời-là-có) — đây là bề mặt **bắt buộc có, nhưng KHÔNG có UC nào phủ** |
| **X-3** — Công bố độ phủ checker | ⭐ `SRS-FR-22` | Hiển thị tường minh: *"đã kiểm **N/M** panel, **M−N** panel không kiểm được vì có nhiều nhân vật"* | `SRS-FR-22` được đánh dấu là **FR minh bạch, KHÔNG phải chỉ tiêu chất lượng**; số **40–60%** (`CF-6.11` `[EM]`) là *"chỉ tiêu **PHẢI CÔNG BỐ cho user**"* |
| **X-4** — Side-by-side hai version | `SRS-FR-21` | Giữ **cả hai** version, hiển thị side-by-side, ⭐ **NGƯỜI chọn, không bao giờ tự áp dụng** · `unclear` là câu trả lời **hợp lệ hạng nhất** | ⛔ `[Fix automatically]` **đã cắt hẳn** |
| **X-5** — Provenance / origin | `SRS-FR-36` (`generation.origin ENUM('ai','ai_edited','human')`) · `UC-02` b4 · `UC-06` b10 · `UC-07` b9 | Badge mức **field** (`field_provenance`) và mức **generation** (`origin`) | Ba giá trị phân biệt được: `ai` · `ai_edited` · `human`. `Story-AI-Disclosure` unhappy path: nội dung **hỗn hợp** phải đánh dấu đúng bản chất hỗn hợp, ⛔ không mặc định về một trong hai cực |
| **X-6** — `change_log` mọi hành động | `SRS-FR-35` · `KC-2` · `MVP-Scope §5.2` callout | ⚠️ **Ranh giới cần giữ**: repo bắt buộc **GHI** một `change_log` row cho mọi hành động — **không** bắt buộc **HIỂN THỊ** nó. Và `SRS-NFR-23` **cắt hẳn UI duyệt cây generation** (tree/diff/branch-merge) | ⛔ Design System **không** được suy ra một *"history panel"* từ `KC-2`. Cắt UI ≠ cắt cột dữ liệu (`CẤM-09`) |

### 1.3 Nhóm màn hình — **12 nhóm**

Số nhóm là **12**, không ép về con số tròn. Cột *Mốc* dùng để PM cắt lô theo `UNLOCK-ORDER` của `Backlog-Priority.md`.

| # | Nhóm màn hình | Surface | Mốc sớm nhất | Trong horizon 09/2026–02/2027? |
|---|---|---|---|---|
| 1 | **Workspace / tenant shell + danh sách tác phẩm** | S-01 | MVP1 | ✅ |
| 2 | **Khu vực ingest** | S-02, S-03 | MVP1 (`B1`, `GP-2`) | ✅ |
| 3 | **Khu vực review Story Bible** | S-04 | MVP1 (`MVP-Scope §5.2` #5) | ✅ |
| 4 | **Khu vực review panel script (Comic IR)** | S-05 | MVP0 (YAML tay) → MVP2 (UI) | ✅ |
| 5 | ⭐ **Khu vực human gate** (hai gate — *"chỉ xong CÙNG NHAU"*) | S-06, S-07 | MVP2 (`C7`) | ✅ |
| 6 | **Panel card + variant picker** | S-08, S-09 | MVP0 (script) → **MVP3** (UI) | ⚠️ **UI ngoài horizon** |
| 7 | **Editor panel / typeset** | S-10 | MVP0 (thô) → MVP2 → MVP3 | ⚠️ **Bắt đầu MVP2, hoàn tất MVP3** |
| 8 | **Editor trang + preview** | S-11, S-12 | MVP2 (`MVP-Scope §5.2` #3, #4) | ✅ |
| 9 | **Khu vực export** | S-13 | MVP2 (PDF) → MVP3 (đủ định dạng) | ✅ (chỉ PDF) |
| 10 | **Khu vực credit / billing / BYOK** | S-14, S-15, S-16 | MVP3 / MVP4 | ⛔ **NGOÀI HORIZON** |
| 11 | ⭐ **Khu vực takedown công khai** (shell riêng, **không đăng nhập**) | S-17, S-18 | MVP2 hoặc **sớm hơn nếu trigger `X-a` đến sớm hơn** | ✅ |
| 12 | ⚠️ **Khu vực operator (Founder)** | S-19 | rải rác MVP1→MVP4 | ⚠️ **Không UC nào mô tả màn hình** |

> **Hai nhóm cần PM chú ý vì chúng phá giả định "một hệ thiết kế cho cả sản phẩm"**:
> - **Nhóm 11** có actor **ngoài hệ thống, không có tài khoản, có thể không bao giờ trở thành khách hàng**. Nó không nằm trong workspace, không có tenant context. Brand Guidelines phải quyết: bề mặt này mang cùng brand, hay là một trang pháp lý tối giản riêng?
> - **Nhóm 10** giao một phần bề mặt cho **vendor billing** (`E4` = *mua, không tự viết*). Có một ranh giới thương hiệu mà Design System **không kiểm soát được**.

### 1.4 Suy luận, chưa có nguồn — đọc riêng, đừng trộn vào bảng trên

Những bề mặt dưới đây **một sản phẩm SaaS bình thường sẽ có**, nhưng **không UC nào và không requirement nào trong repo mô tả chúng**. Em liệt kê để PM biết đây là chỗ Design System sẽ bị cám dỗ tự bịa.

| Bề mặt | Trạng thái nguồn | Mảnh gần nhất repo có |
|---|---|---|
| Màn hình **đăng nhập / đăng ký** | ⚠️ **Suy luận** — không UC nào mô tả | `SRS-FR-03`: *"**Mua** auth và billing, **không tự viết**"* ⇒ bề mặt này **do vendor sở hữu**, giống S-15 |
| **Navigation / app shell** (sidebar, breadcrumb, header) | ⚠️ **Suy luận** — không có nguồn nào | Chỉ có ba câu *"mở … trong workspace của tenant mình"* (`UC-01` b1, `UC-09` b1, `UC-10` b1) |
| **Toast / notification system** | ⚠️ **Suy luận** — repo nói *"báo cho tác giả"* nhưng **không nói bằng cơ chế gì** | `UC-01` b9 *"Báo cho tác giả"*; `UC-11` b4 xác nhận đã nhận là **email**, không phải in-app |
| **Onboarding flow** | ⚠️ **Suy luận** ở phần UI | `SRS-FR-32` chỉ nói *"kiến trúc billing + credit ledger + **onboarding** phải đỡ được ba tầng, không retrofit"* — kiến trúc, không phải màn hình |
| **Settings / profile / team management** | ⚠️ **Suy luận** — không có nguồn | `SRS-FR-01`: `tenant` / `user` / `membership` là **ba entity riêng** — là data model, không phải UI |
| **Dark mode** | ⚠️ **Không có một dòng nào trong toàn `docs/020-Requirements/`** (đã grep) | — |
| **Danh mục kiểu bubble** | ⛔ **`TBD` tường minh** | `UC-07` b6 ghi nguyên văn: *"nguồn chỉ ghi 'chọn kiểu'; **danh mục kiểu bubble cụ thể chưa được định nghĩa ở đâu trong repo**"*. `AF-6`: SFX / narration box / caption cũng `TBD` ⇒ ⛔ **Design System KHÔNG được tự đặt danh mục này** |

---

## 2. Component inventory tối thiểu

**Quy tắc phân lô** (theo yêu cầu của PM — *thứ tự ưu tiên quan trọng hơn độ đầy đủ*): dùng ở **≥3 surface** ⇒ **component nền, phải spec kỹ**. Dùng ở **1–2 surface** ⇒ có thể hoãn sang run sau, **trừ** khi nó mang một ràng buộc pháp lý/nghiệp vụ cứng.

### 2.1 Lô 1 — Component nền (≥3 surface), spec kỹ ở run này

| # | Component | Dùng ở surface | Tần suất | Vì sao phải spec kỹ |
|---|---|---|---|---|
| **C-01** ⭐⭐ | **Alert / Callout — BA MỨC phân biệt được** | S-02, S-03, S-04, S-05, S-06, S-07, S-08, S-09, S-10, S-11, S-13, S-14, S-16 | **13** | ⭐ **Component quan trọng nhất của cả Design System này.** Repo phân biệt **ba mức** và trộn chúng là **lỗi nghiệp vụ, không phải lỗi thẩm mỹ**: (a) ⛔ **TỪ CHỐI ở tầng DB/pipeline** — `M2-2` *"bị từ chối, **KHÔNG PHẢI** bị cảnh báo"* (`UC-03` `EXC-1`, `UC-07` `EX-7`, `UC-08` `EX-6`), `M2-4` từ chối export (`UC-09` `EF-1`), chặn opt-out (`UC-01` `EXC-1`); (b) ⚠️ **CẢNH BÁO cho qua được** — `M2-3` bubble đè vùng mặt (`UC-07` `EX-1`), sửa `story_order` (`UC-02` `EXC-5`); (c) ℹ️ **thông tin không phải lỗi** — CBZ/webtoon *"chưa có"* (`UC-09` `EF-2`). Nếu ba mức trông giống nhau, người dùng sẽ học cách bỏ qua cả ba |
| **C-02** | **Error state có LÝ DO CỤ THỂ + ĐƯỜNG XỬ LÝ** | S-02, S-03, S-04, S-05, S-07, S-08, S-12, S-13, S-14, S-16 | **10** | Không UC nào chấp nhận error message chung chung. Mẫu lặp lại: *"báo **lý do cụ thể**"* (`UC-01` `EXC-3`), *"nêu rõ **mức vượt**"* (`UC-05` `EX-1`), *"nêu rõ cần thêm **bao nhiêu** credit"* (`UC-10` `EF-1`), *"liệt kê **các page còn thiếu gate nào**"* (`UC-09` `EF-1`), *"báo rõ **page/panel nào** thiếu"* (`UC-09` `EF-4`). ⭐ `UC-10` `EF-4` còn quy định **nội dung** thông điệp: *"nêu rõ đây là giới hạn của **key của user**, không phải lỗi truyện của họ"* |
| **C-03** | **Status badge / state chip** | S-02, S-03, S-05, S-06, S-07, S-11, S-12, S-13, S-14 | **9** | Tập trạng thái nghiệp vụ đã đặt tên trong repo: `chưa xác nhận` / `đã xác nhận` · gate `OPEN` / `PASS` · `pending` · `gate 1/2 đã xong` · `superseded` · `disable-access` · *"chưa có ở mốc hiện tại"* · `available` / `hold`. **Không được gộp** — mỗi cái mang một hệ quả pháp lý hoặc kinh tế khác nhau |
| **C-04** | **Loading / long-running job** | S-03, S-04, S-05, S-07, S-08, S-12, S-13 | **7** | Mọi chặng máy đều async: ingest · extraction · Director · condenser · **generation *"mất hàng chục giây"*** · preview composite · export composite. Ràng buộc cứng: cập nhật bằng **polling 2 giây** (`SRS-NFR-06`), ⛔ không WebSocket. ⚠️ **`TBD`**: latency mục tiêu và p50/p95 của một panel đều chưa có số |
| **C-05** | **Form + field-level control** (input · select · textarea · numeric) | S-02, S-04, S-05, S-08, S-10, S-16 | **6** | Ràng buộc tường minh: Story Bible editor là **form + list, ⛔ KHÔNG canvas, KHÔNG graph editor** (`BR-004-01`). Cần **field-level provenance** và **field-level lock** (`SRS-FR-12`: edit của người **phải khoá lại** khỏi bị re-run ghi đè) |
| **C-06** | **Data list / table có hàng chọn được** | S-01, S-04, S-05, S-06, S-07, S-13 | **6** | Đơn vị công việc của người dùng luôn là **một hàng**: một entity · một panel · một dòng thoại · một cặp gốc→nén · một page. Cần hỗ trợ **thao tác theo hàng có trạng thái riêng** và **định vị "hàng chưa quyết đầu tiên"** (`UC-04` `ALT-5`) |
| **C-07** | **Confirm dialog cho hành động không đảo ngược được** | S-02, S-04, S-08, S-09, S-13, S-17 | **6** | Repo có **bốn** loại hành động không rút lại: `Regenerate` **tiêu tiền thật** (`BR-004-08` — *"UX **phải nói rõ**, không để actor suy đoán"*) · hard-delete tenant (`UC-02` `EXC-7`) · export ra ngoài (*"artifact đã export thì **không thu hồi được**"*) · takedown soft-delete. Đây là component có **hệ quả tài chính và pháp lý**, không phải một dialog trang trí |
| **C-08** | **Empty state** | S-04, S-07, S-10, S-12 | **4** | ⭐ Chỉ **một** empty state được mô tả ở mức hiển thị (`UC-08` `AF-6`: panel chưa có ảnh ⇒ **ô trống**). Ba cái còn lại chỉ được mô tả bằng **điều cấm**: `UC-02` `EXC-1` ⛔ *"không tự tạo entity rác để **có gì đó hiển thị**"*; `UC-03` `EXC-2` ⛔ *"không sinh panel script rỗng"*. ⇒ Empty state ở sản phẩm này là **một quyết định nghiệp vụ**: thà rỗng còn hơn giả |
| **C-09** | **Provenance / origin indicator** | S-04, S-08, S-09, S-10 | **4** | `field_provenance` mức field (`KC-3`) + `generation.origin ENUM('ai','ai_edited','human')` (`SRS-FR-36`). Phải phân biệt được **ba** giá trị, kể cả trạng thái **hỗn hợp** `ai_edited` |
| **C-10** | **AI disclosure indicator** | S-04, S-05, S-06, S-07, S-08/S-09 | **5** (mọi điểm chạm AI) | Bắt buộc bởi `SRS-FR-40` + AC-1 của `Story-AI-Disclosure-Article-11`. Xem [§3.3](#33--ai-disclosure-có-buộc-phải-có-bề-mặt-ui--câu-trả-lời-là-có) |
| **C-11** | **Budget / quota / ngưỡng — mức hiện tại + trần + hệ quả khi vượt** | S-05 (emphasis quota) · S-07, S-10 (`text_budget`) · S-08, S-14 (credit hold) | **5** | Ba khái niệm khác nhau nhưng **cùng một pattern**: có một trần rời rạc, có mức hiện tại, và **vượt thì bị chặn chứ không co giãn**. `UC-03` `EXC-5`: *"nếu mọi panel đều được nhấn thì **không panel nào được nhấn**"* ⇒ quota cạn thì **buộc đánh đổi**, không nới |
| **C-12** | **Diff / side-by-side có người quyết** | S-07 (gốc→nén) · S-09 (3 candidate) · X-4 (`SRS-FR-21`) | **3** | Ràng buộc cứng chung: **giữ cả hai/cả ba phương án, NGƯỜI chọn, ⛔ không bao giờ tự áp dụng**. `unclear` / `UNKNOWN` là câu trả lời **hợp lệ hạng nhất** — cần một trạng thái thứ ba, không phải nhị phân |
| **C-13** | **Counter / progress theo đơn vị công việc còn lại** | S-06 (*"còn N dòng chưa xác nhận"*) · X-3 (*"đã kiểm N/M panel"*) · S-13 (page thiếu gate) | **3** | Đơn vị đo của một HITL gate là **giờ-người**, không phải token (`Glossary` *HITL gate*) ⇒ counter là thứ cho người dùng biết **còn bao nhiêu công**, không phải một thanh trang trí |

### 2.2 Lô 2 — Dùng 1–2 chỗ nhưng **KHÔNG được hoãn** (ràng buộc cứng)

| # | Component | Surface | Tần suất | Vì sao không hoãn được |
|---|---|---|---|---|
| **C-14** ⭐ | **Consent checkbox — cam kết quyền tại bước upload** | S-02 | **1** | `SRS-FR-41` + `BR-007-07`: checkbox **phải gắn vào BƯỚC UPLOAD, không chỉ ở trang ToS**. Không tick ⇒ **upload không được nhận** (`UC-01` `EXC-2`). Đây là *"phòng tuyến hợp đồng của nền tảng"* — một component 1-chỗ nhưng là điều kiện pháp lý |
| **C-15** ⭐ | **Public form không cần đăng nhập** | S-17 | **1** | `BR-007-04` (a): điều kiện giữ **miễn trừ Điều 198b**. Actor **không có tài khoản** ⇒ component này không dùng lại được bất cứ pattern nào của app đã đăng nhập |
| **C-16** | **Read-only composite viewer** | S-12, S-13 | **2** | Preview và export **dùng CHUNG compositor** (`H4`, `CF-9.1` — ⛔ *"không viết renderer từ đầu"*). Hai surface nhưng một implementation ⇒ spec một lần, dùng hai chỗ |

### 2.3 Lô 3 — Có thể hoãn sang run sau

| # | Component | Surface | Tần suất | Ghi chú |
|---|---|---|---|---|
| C-17 | Dual input: file upload **+** paste text | S-02 | 1 | `UC-01` b2 + `ALT-2` |
| C-18 | Template picker | S-11 | 1 | `UC-08` b4 |
| C-19 | Swap / reorder **rời rạc** giữa các ô | S-11 | 1 | ⚠️ **rời rạc**, ⛔ không phải drag-drop hình học liên tục (`BR-004-02`) ⇒ rẻ hơn nhiều so với vẻ ngoài |
| C-20 | Drag trong khung giới hạn (bubble + tail) | S-10 | 1 | ⛔ **KHÔNG** infinite canvas (D2 hoãn) — *"canvas bị giới hạn trong một khung"* |
| C-21 | Conflict resolution buộc chọn | S-04 | 1 | `UC-02` `EXC-4` |
| C-22 | Hiển thị ba số credit tách bạch | S-14 | 1 | ⛔ **NGOÀI HORIZON** (MVP3) |
| C-23 | API key input (BYOK) | S-16 | 1 | ⛔ **NGOÀI HORIZON** (MVP4). ⚠️ `b-2` — cách lưu/bảo vệ key là **`TBD`** |
| C-24 | Format availability list ("chưa có ở mốc này") | S-13 | 1 | `UC-09` `EF-2` |

> ⛔ **Component KHÔNG được đặc tả ở run này** (đã bị cắt hoặc chưa có nguồn):
> - **Tree view / diff view / branch-merge của generation** — `SRS-NFR-23`, `D6` **cắt hẳn**. ⚠️ Cắt **UI**, ⛔ **không** cắt cột `parent_generation_id` (`CẤM-09`).
> - **Layout Score / bất kỳ hiển thị điểm số layout nào** — `SRS-NFR-22`, `C4` = ❌ ở **mọi** cột kể cả Full Scope. ⛔ *"Không có điểm số thực nào được tính, hiển thị hay lưu"*.
> - **Inpainting brush / drawing tools** — D5 hoãn (`UC-07` `EX-4`).
> - **Infinite canvas** — D2 hoãn (`UC-07` `EX-5`, `UC-08` `EX-3`).
> - **Bất kỳ dashboard "nội dung khả nghi" / copyright detection nào** — `SRS-NFR-15` **anti-feature**: nó **phá** miễn trừ Điều 198b (`UC-11` `EF-4`, `R-04`).
> - **Danh mục kiểu bubble cụ thể** — `TBD` tường minh (`UC-07` b6).
> - **Màn hình counter-notice** — thủ tục là `TBD`, *"UC này KHÔNG phát minh thời hạn hay bước phục hồi"* (`UC-11` `AF-1`).

---

## 3. NFR và requirement chạm trực tiếp vào UI

### 3.0 ⚠️ Đính chính con số trong prompt của run

Prompt giao việc ghi *"SRS có 17 NFR có số + 14 NFR `TBD`"*. Em đo lại trên file thật và thấy **ba con số khác nhau, ba nghĩa khác nhau** — PM cần dùng đúng cái:

| Con số | Nghĩa | Vị trí |
|---|---|---|
| **17** ✅ khớp | Số hàng của bảng *"NFR có chỉ tiêu đo được"* | `SRS §5.1`, 17 hàng |
| **21** ⚠️ **không phải 14** | Số hàng của bảng *"NFR chưa có chỉ tiêu — `TBD`"*. Callout ngay trên bảng ghi nguyên văn: *"**Hai mươi mốt hàng** dưới đây ở lại `TBD`"* | `SRS §5.2`, 21 hàng |
| **7** | Số **requirement row** có mức độ rắn *"CHƯA QUYẾT → `TBD`"*: thuần 4 (`SRS-NFR-07`, `SRS-NFR-08`, `SRS-NFR-09`, `SRS-NFR-16`) + lai 3 (`SRS-FR-26`, `SRS-NFR-20`, `SRS-NFR-17`) | `SRS §3.9` |

⇒ Không có con số **14** nào trong SRS. Em **không sửa file nguồn**; PM chọn con số đúng khi viết prompt cho writer.

### 3.1 NFR **có số** chạm trực tiếp vào UI — Design System được phép dùng, **kèm nguyên nhãn**

| Chỉ tiêu | Số | Nhãn | Mã requirement | Hệ quả lên Design System |
|---|---|---|---|---|
| **Polling interval trạng thái job** | **2 giây** | quyết định kỹ thuật của lens `architect` | `SRS-NFR-06` — **MẶC ĐỊNH**, có đường lui | Loading/progress pattern phải chịu được refresh mỗi 2s. ⛔ Không WebSocket ⇒ không có realtime streaming state |
| **best-of-N** | **N = 3** candidate/panel, mặc định **mọi** panel | `[OFF]` arXiv 2604.13452 | `SRS-FR-20` | Variant picker luôn có **đúng 3 ô** — không phải grid co giãn. ⛔ `CẤM-03`: N=3 **không phải** retry-on-failure |
| **Trần nhân vật/panel** | **≤ 3** | `[OFF]` arXiv 2606.15867 (ID-Sim 42.33→27.21→2.67→0.52) | `SRS-FR-08` · `M2-2` | Quyết định **loại alert**: `db-reject`, ⛔ **không phải** warning. ⚠️ Nếu gate `G1-d` không đạt, trần siết xuống **≤2** trong schema |
| **Độ phủ Continuity Checker** | **40–60%** số panel | ⚠️ `[EM]` `CF-6.11` | `SRS-FR-22` | ⭐ *"đây là chỉ tiêu **PHẢI CÔNG BỐ cho user**, KHÔNG phải mục tiêu chất lượng để đạt"* ⇒ **bắt buộc có bề mặt hiển thị** (X-3) |
| **Typeset không đè vùng mặt** | **≥ 95%** panel | ⚠️ `[EM]` — *"ngưỡng do em định nghĩa"* | `M2-3` · `BR-003-09` | Quyết định **loại alert**: `warning` cho qua được, ⛔ không phải reject |
| **Extraction khớp Story Bible tay** | **≥ 80%** entity | ⚠️ `[EM]` — *"ngưỡng do em định nghĩa"* | `M1-3` | Đo *"công sức còn lại của con người"* ở S-04, không đo *"chất lượng AI"* |
| **Emphasis budget/chapter** | tối đa **1 full page + 2–3 large panel** | `[EM]` — đề xuất của lens | `SRS-FR-09` | Quota meter ở S-05/S-11 là **rời rạc**, ⛔ không phải thanh co giãn |
| **Hold reserve** | **3 credit/panel**, ⛔ **không phải 1** | dẫn xuất từ `[OFF]` `CF-3.1` | `SRS-FR-28` · `KC-7` | Cost disclosure ở S-08 hiển thị **3**, không phải 1 |
| **Takedown SLA** | **72 giờ** | ⚠️ `[OFF]` **TÓM TẮT, không phải nguyên văn điều luật** | `SRS-FR-38` | S-18 phải hiển thị **timestamp tiếp nhận do hệ thống ghi**, không phải ký ức của Founder |
| **Deadline AI disclosure** | **~01/03/2027** | ⚠️ `[OFF]` — **hai nguồn mô tả phạm vi KHÁC NHAU** | `SRS-FR-39`, `SRS-FR-40` | Nằm **ngay sau** horizon ⇒ cơ chế phải có nền trong horizon |
| **Ngưỡng phân tuyến Tầng 2/3** | **~125 ảnh/tháng** | `[TC]` vendor blog, *"cần đo lại bằng dữ liệu thật"* | `SRS-FR-32` | Chỉ chạm S-14/S-16 — **ngoài horizon** |

### 3.2 NFR **`TBD`** — Design System **PHẢI để `TBD`**, ⛔ không tự điền số

| NFR chưa có chỉ tiêu | Mã | Vì sao nó chạm Design System |
|---|---|---|
| **Latency / response time của API** | `TBD` (không mã riêng) | Không có ngưỡng ⇒ ⛔ **không được viết** *"loading spinner hiện sau 300ms"* hay bất kỳ ngưỡng thời gian nào vào token/motion spec |
| **Thời gian sinh một panel end-to-end (p50/p95)** | `SRS-NFR-11` | Quyết định pattern của C-04 (spinner vs progress vs background job) — **không có số để quyết** |
| **Uptime / availability SLA** | `SRS-NFR-03` | Ràng buộc gần nhất chỉ **định tính**: *"worker chết mà API vẫn sống"*. `UC-09` `EF-5` nhắc lại `BRD-008` `TBD-4`: *"Không nguồn nào trong repo đặt con số này. **Không tự gán**"* |
| ⭐ **`b-6` — i18n / l10n** | `SRS-FR-16`, `SRS-NFR-09` | ⭐ **Hàng quan trọng nhất cho Typography spec.** Nguyên văn: *"Artifact duy nhất là `SRS-FR-16` — một FR về **typesetting**, **không phải NFR ngôn ngữ**. Nội dung đa ngôn ngữ hiện là **giả định vận hành**, chưa bao giờ được phát biểu thành requirement. Ảnh hưởng **font** / collation / FTS config"*. ⇒ Design System **được** spec font render tiếng Việt (có `SRS-FR-16`), ⛔ **không được** spec chiến lược i18n cho UI |
| **Ngôn ngữ / framework frontend** | `SRS-NFR-09` | ⚠️ **Xung đột cross-layer — xem [§5](#5-vấn-đề-phát-hiện-trong-tài-liệu-nguồn--report-only-em-không-sửa) mục 3** |
| **Rate limit per tenant · giới hạn dung lượng/số file upload** | `SRS-NFR-20` (**LAI** — cơ chế CHỐT, ngưỡng `TBD`) | S-02 cần một thông điệp lỗi *"vượt giới hạn upload"* ⇒ **có component, không có số** ⇒ copy viết dạng tham số, không hardcode |
| **Thời hạn signed URL** | `SRS-FR-02` | Ảnh trong S-09/S-12 phát hành qua signed URL **có hạn**; hết hạn giữa phiên là một trạng thái lỗi thật — **không có số** |
| **`b-1` — mã hoá dữ liệu / secret** · **`b-2` — lưu API key BYOK** | `SRS-NFR-07`, `SRS-NFR-08`, `SRS-FR-32` | Chạm C-23 (input API key). ⛔ Không viết copy kiểu *"key của bạn được mã hoá an toàn"* — **chưa ai quyết cơ chế** |
| **`b-4` — bảo vệ dữ liệu cá nhân** | `SRS-FR-38`, `SRS-NFR-17` | S-17 **bắt buộc thu email + số điện thoại** của người **ngoài hệ thống**. ⛔ *"Không nêu tên văn bản cụ thể"* ⇒ Design System **không** viết privacy copy |
| **SynthID có thoả nghĩa vụ đánh dấu không** | `SRS-NFR-16` | ⛔ *"phải verify, không giả định"* ⇒ C-10 spec **cơ chế**, ⛔ không khẳng định nguồn watermark |
| **Ba câu hỏi luật sư SHTT** | `SRS-NFR-17` (**LAI**) | Q2 quyết **phạm vi thật** của nghĩa vụ đánh dấu ⇒ phạm vi hiển thị của C-10 là `TBD` |
| ⭐ **PRD §5 trục 6 — Usability** | PRD `§5` hàng 6 | Nguyên văn: *"⚠️ **`TBD`** — không có ngưỡng nào do người ngoài đặt, vì mục 3.3 chưa đóng. **Mọi ngưỡng UX trong tầng này là ngưỡng tự đặt và phải mang nhãn `[EM]`**"* ⇒ ⭐ **mọi con số UX trong Design System phải mang nhãn `[EM]`** |
| ⭐ **PRD §5 trục 5 — Chất lượng typeset tiếng Việt** | PRD `§5` hàng 5 | Nguyên văn: *"không có benchmark định lượng render tiếng Việt có dấu cho **bất kỳ image model nào**; đặc biệt thiếu số cho **chữ chồng hai dấu** (*ế*, *ữ*, *ượ*)"* ⇒ Typography spec ⛔ **không được hứa một mức chất lượng render tiếng Việt** |

### 3.3 ⭐ AI disclosure: có buộc phải có bề mặt UI? — **Câu trả lời là CÓ**

**Có, và nó là ràng buộc mạnh nhất mà lens này tìm được cho Design System.**

| Điều | Nội dung | Nguồn |
|---|---|---|
| **Requirement bắt buộc** | `SRS-FR-40` — *"Cơ chế để **user nhận biết đang tương tác với hệ thống AI**"* (Điều 11 Luật TTNT 2025 — **Luật số 134/2025/QH15**). Mức độ rắn: **CHỐT** | `SRS §3.G` |
| **AC đo được, nói thẳng nó là UI** | *"Xác nhận tồn tại một **chỉ dẫn/thông báo hiển thị cho người dùng tại điểm tương tác với tính năng AI** (ví dụ tại bước generate/pick variant), **không phải chỉ ghi trong ToS**"* | `Story-AI-Disclosure-Article-11` §4 AC-1 |
| **Requirement thứ hai** | `SRS-FR-39` — provenance field cấp **page/panel** + export path nhúng được **machine-readable watermark**. **CHỐT** | `SRS §3.G` |
| **Phạm vi thật** | ⚠️ **`TBD`** — hai cách đọc khoản 4 Điều 11 (HẸP vs RỘNG), là câu **Q2** của gate `G0` | `BRD-007 §3.1` |
| **Quy tắc tạm thời — ĐÃ QUYẾT, không phải `TBD`** | ⭐ *"Vì phạm vi chưa rõ, phải **thiết kế theo diễn giải RỘNG (mọi nội dung AI)** cho tới khi luật sư chốt"* | `Charter §7 C4` · `SRS-FR-39` ghi rõ: *"quy tắc tạm thời 'diễn giải rộng' **là một quyết định**, không phải một `TBD`"* |

**Nó xuất hiện ở surface nào** — suy ra từ *"điểm tương tác với tính năng AI"*, mỗi điểm có UC chứng minh:

| Surface | Tính năng AI tại đó | UC nguồn |
|---|---|---|
| **S-04** Story Bible editor | LLM extraction rút entity + phát event | `UC-02` b2 |
| **S-05** Panel script reviewer | LLM đề xuất phân chia scene → page → panel | `UC-03` b3 |
| **S-06** Human gate #1 | LLM **đề xuất** người nói | `UC-04` b2 |
| **S-07** Human gate #2 | **LLM condenser** nén thoại | `UC-05` b4 |
| **S-08 / S-09** Panel card + variant picker | Image provider sinh 3 candidate · **VLM chấm và đề xuất** | `UC-06` b6, b7 — ⭐ **chính là ví dụ mà AC-1 nêu đích danh** |
| **S-13** Export | Nhúng **machine-readable marker** vào export path | `UC-09` `AF-3` · `SRS-FR-39` |

> ⚠️ **Cảnh báo phải chuyển cho PM**: `Story-AI-Disclosure-Article-11` §2 ghi nguyên văn — ***"Không có Use Case nào… được gán riêng cho nghĩa vụ AI disclosure. Không tự gán một UC không có căn cứ."***
> ⇒ Đây là một **bề mặt UI bắt buộc mà tầng Use Case không phủ**. Bảng ánh xạ ở trên là **em suy ra từ *"điểm tương tác với tính năng AI"* của AC-1**, mỗi hàng có UC chứng minh chỗ AI được gọi — nhưng ⛔ **không UC nào nói *"ở đây phải hiển thị disclosure"***. PM cần biết chỗ này để writer không viết như thể nó đã được chốt ở tầng 020.
>
> **Ràng buộc positioning đi kèm**, ảnh hưởng trực tiếp Brand Guidelines: `Charter §7 C5` — ***disclosure-first, nhắm writer KHÔNG nhắm artist***. `Glossary` gọi đây là *disclosure-first positioning*: disclosure **không phải chi phí tuân thủ mà là ràng buộc phân phối**. ⛔ `AG-2` (`OKRs §6`): **cấm marketing vào cộng đồng hoạ sĩ** dựa trên cơ chế đánh dấu này.

### 3.4 ⛔ Khoảng trống tuyệt đối: accessibility & responsive — **KHÔNG PHẢI `TBD`, mà là CHƯA AI TỪNG NHẮC**

Em grep toàn thư mục `docs/020-Requirements/` (PRD + SRS + 8 BRD + 11 UC) với pattern:

`accessibility|a11y|WCAG|contrast|tương phản|keyboard|bàn phím|screen reader|responsive|mobile|di động|desktop|dark mode`

**Kết quả: 0 hit liên quan.** (Chỉ có hit của `onboarding` — và đều là onboarding **kiến trúc billing 3 tầng**, không phải onboarding UI.)

> ⭐ **Phân biệt phải giữ, vì nó đổi cách xử lý**:
> - Một hàng **`TBD` đã khai** (ví dụ `SRS-NFR-09`, `b-6`) là **một quyết định có ý thức**: ai đó đã nhìn thấy khoảng trống và cố ý không lấp. Design System **giữ nguyên `TBD`**.
> - **Accessibility / responsive / thiết bị đích** là loại khác: **chưa ai từng nêu vấn đề**, nên nó **không có cả một hàng `TBD`** để giữ. Đây là **khoảng trống chưa được thừa nhận**.
>
> ⇒ **Khuyến nghị cho gate**: Design System phải **khai đây là một khoảng trống MỚI** và đưa lên anh quyết, ⛔ **không** được im lặng chọn một chuẩn (WCAG AA, breakpoint set, contrast ratio) rồi trình bày như thể nó đã có căn cứ trong repo. Một `contrast ratio ≥ 4.5:1` viết vào token spec **trông như** có nguồn, nhưng nguồn đó **không tồn tại ở tầng 020** — và nó sẽ **trôi thẳng** vào tầng QA làm chuẩn nghiệm thu.
>
> **Mảnh gần nhất repo có** (không thay thế được cho requirement): `SRS-FR-11` — *"cùng dữ liệu render được **thumbnail** và **bản in 300 DPI**"*. Đó là ràng buộc về **output ảnh comic**, ⛔ **không phải** ràng buộc responsive của giao diện editor.

### 3.5 ⭐ Ràng buộc dễ bị bỏ sót nhất: **hai hệ font, không phải một**

| | Font **UI** (giao diện editor) | Font **render vào ảnh comic** (typeset layer) |
|---|---|---|
| **Nguồn** | ⚠️ **Không có requirement nào** — xem §3.4 | `SRS-FR-16` (**CHỐT**) · `SRS-FR-11` · `SRS-FR-13` |
| **Ràng buộc** | — | *"Wrap tiếng Việt phải dùng **thư viện hiểu Unicode combining marks**"* · auto-placement bubble **phải tự build** (heuristic: gần speaker, tránh vùng có mặt, thứ tự đọc) + **cho user kéo tay** |
| **Chất lượng** | — | ⚠️ **`TBD`** — không có benchmark render tiếng Việt có dấu cho bất kỳ image model nào (PRD §5 trục 5) |
| **Xuất hiện ở** | mọi surface | S-10 (editor), S-12 (preview), S-13 (export) — **cùng một compositor** |

⇒ Typography spec **bắt buộc tách hai hệ này**. Gộp làm một là vi phạm ngay ở tầng thiết kế, và ⚠️ **lỗi chỉ lộ ra sau khi đã sinh ảnh** — tức sau khi đã tiêu tiền thật.

---

## 4. Khoảng trống persona — nói thẳng, không lấp

### 4.1 Xác nhận bằng grep thật

| Điều cần verify | Kết quả | Bằng chứng |
|---|---|---|
| `PRD-Comic-Studio.md` mục *Người dùng & vấn đề* mở bằng `TBD` | ✅ **Đúng** | PRD `L20`: *"Tài liệu này còn một khoảng trống đã biết và được thừa nhận tường minh: mục 3 chưa có persona / JTBD / định nghĩa 'đủ tốt', **vì toàn repo không có**"*. PRD `L148`: `### 3.3 ⭐ TBD — persona, JTBD và định nghĩa "đủ tốt"` |
| `docs/000-Index.md` xác nhận repo không có persona/JTBD | ✅ **Đúng** | `000-Index.md` `L76`: *"⚠️ Mục *Người dùng & vấn đề* mở bằng `TBD` — repo **không có persona/JTBD**"* |
| Không có user interview nào | ✅ **Đúng** | PRD `TBD-4`: `docs/050-Research/User-Interviews/` **rỗng** · `Charter §6`: Design partner *"**chưa có ai**"* |

**Năm khoảng trống được khai tường minh** (PRD §3.3): `TBD-1` persona · `TBD-2` JTBD · `TBD-3` định nghĩa *"đủ tốt"* · `TBD-4` không Design partner, 0 user interview · `TBD-5` không willingness-to-pay study.

### 4.2 Actor **CÓ CĂN CỨ** trong repo — và chỉ những actor này

⛔ **Đây KHÔNG phải persona.** Đây là danh sách *"ai đã xuất hiện trong một tài liệu có thật, kèm anchor"*.

| # | Actor | Loại | UC / tài liệu chứng minh | Nhãn |
|---|---|---|---|---|
| **A-1** | ⭐ **Tác giả truyện chữ (writer) KHÔNG biết vẽ** | **Primary actor** của mọi UC người dùng | Primary actor ở **`UC-01` … `UC-10`** (10/11 UC). PRD §3.1, §3.2 | `[CHỐT]` `CF-1.5`. ⛔ `CẤM-17`: **cấm đặt requirement cho phân khúc hoạ sĩ** |
| **A-2** | **Founder ở vai operator** (và vai architect) | **Secondary actor** — vận hành | `UC-01` `EXC-1` (rà log opt-out) · `UC-02` `ALT-1` · `UC-03` `ALT-1` · `UC-06` `AF-1` · `UC-09` `AF-2` · `UC-10` `AF-3`, `AF-4`, `EF-3`, `EF-5` · `UC-11` **secondary actor chính**, b5–b9 | `Charter §6 RACI`: **A ở cả 9 nhóm hoạt động** ⇒ `bus factor = 1`. `[CHỐT]` `CF-1.2` (đội 1 người + AI assist, **không có code review**) |
| **A-3** | ⭐ **Chủ sở hữu quyền — BÊN NGOÀI HỆ THỐNG** | **Primary actor** của đúng **1 UC** | `UC-11` — *"UC DUY NHẤT có primary actor là người ngoài hệ thống"*: **chưa từng đăng ký tài khoản**, **có thể không bao giờ đăng ký**, không thuộc tenant nào | `MVP-Scope §3 GP-3` · `CF-7.6` `[OFF]` **tóm tắt** · `Charter BLOCKER-02` |
| **A-4** | **Độc giả / cơ quan quản lý** | ⚠️ **KHÔNG tương tác trực tiếp với hệ thống** | Actor của `Story-AI-Disclosure-Article-11` §1 (*"Là **độc giả / cơ quan quản lý**, tôi muốn nội dung do AI tạo được đánh dấu…"*). PRD §3.2 hàng 4 | `MVP-Scope §3 GP-4` · `[OFF]` `CF-7.7` · `Charter C4`. ⇒ **Không có surface riêng**; nó là **lý do tồn tại** của C-10, không phải người dùng của C-10 |

**Ba thứ KHÔNG được đếm là actor** — ghi ra vì chúng trông giống actor:

| Không phải actor | Vì sao | Nguồn |
|---|---|---|
| ⚠️ **"Power user"** | *"**không phải một persona mới**… Nó là **một trạng thái sử dụng** — người vượt ngưỡng ~125 ảnh/tháng"* `[TC]` | `UC-10` §1 |
| **Vendor billing** | *"là **hệ thống ngoài**, không phải actor người"* — `E4` = mua billing, không tự viết | `UC-10` §1 |
| **Model provider** (Google / BFL) | *"**không phải participant**… là ràng buộc ngoài, không đàm phán được"* | `Charter §6` cảnh báo 3 |

**Hai cột RACI đang RỖNG trong thực tế** (`Charter §6` cảnh báo 2 — *"Chữ **C** ở đó là **nghĩa vụ chưa thực hiện**, không phải năng lực đang có"*): **Luật sư SHTT** (chưa engage) và ⭐ **Design partner** (chưa có ai).

### 4.3 Thiếu **chính xác những gì** để một actor thành persona thật

`PRD §3.1` liệt kê **đích danh sáu thứ** mà *"tác giả truyện chữ không biết vẽ"* **không** trả lời được — em trích nguyên, không thêm bớt:

> *"Nó **không** trả lời: người đó **bao nhiêu tuổi**, **viết trên nền tảng nào**, **đã trả tiền cho công cụ gì**, **một chương của họ dài bao nhiêu**, **họ chấp nhận bỏ bao nhiêu phút cho một trang**, và **họ gọi cái gì là 'đủ tốt'**. Bốn thứ sau là **đầu vào bắt buộc của Acceptance Criteria** — và repo không có."*

Cộng thêm: **0 user interview** (`TBD-4`), **0 willingness-to-pay study** (`TBD-5`), **0 Design partner** (`Charter §6`).

**Cơ chế đã được thiết kế sẵn để đóng khoảng trống này**: **KR4.3** (`OKRs §3`) — **20 cuộc trò chuyện 1-1 có ghi chép** với tác giả trước **31/12/2026**. *"Đầu ra của KR4.3 là đầu vào để viết lại mục 3."*

**Proxy duy nhất repo có** cho định nghĩa *"đủ tốt"* — và nó **không** đóng `TBD-1/2/3`:

> Cạnh **mọi** metric kỹ thuật phải có **đúng một câu người trả lời**: ***"trang này đọc có ổn không?"*** — ghi lại **từ MVP0**. (`CF-10.10` · `SRS-NFR-18`)

⚠️ PRD nói thẳng: *"Proxy này **KHÔNG phải persona**. Nó là một ngưỡng chấp nhận do **chính người build** đưa ra."*

### 4.4 Hệ quả trực tiếp lên Brand Guidelines — đọc trước khi viết một dòng nào

| # | Được phép neo vào | Ví dụ |
|---|---|---|
| 1 | **Phân khúc đã chốt** | *"Tác giả truyện chữ **không biết vẽ**"* — `[CHỐT]` `CF-1.5` |
| 2 | **Loại trừ đã chốt** | ⛔ **không nhắm hoạ sĩ** — `CẤM-17`, `NG-1`, và `AG-2` cấm marketing vào cộng đồng hoạ sĩ |
| 3 | **Positioning đã chốt** | ⭐ **disclosure-first** — `Charter §7 C5`; *"không phải chi phí tuân thủ mà là **ràng buộc phân phối**"* |
| 4 | **Bốn actor có anchor** | A-1 … A-4 ở §4.2 |
| 5 | **Điều kiện đội ngũ** | 1 người + AI assist, `bus factor = 1` — `[CHỐT]` `CF-1.2` ⇒ Design System phải **rẻ để duy trì**, không phải đẹp để trình bày |

| # | ⛔ **KHÔNG** được neo vào | Vì sao |
|---|---|---|
| 1 | Tuổi · giới tính · thu nhập · vị trí địa lý của người dùng | `TBD-1` — **không tồn tại trong repo** |
| 2 | *"Người dùng của chúng ta thích phong cách X"* | `TBD-3` — không ngưỡng nào do **người ngoài** đặt |
| 3 | *"Người dùng chấp nhận chờ Y giây"* | `PRD §3.3` hệ quả 1 nêu đích danh câu này là câu **không có căn cứ để viết** |
| 4 | Bất kỳ tone-of-voice nào suy ra từ một chân dung người dùng | Sẽ tạo **nguồn sự thật giả ở tầng 040 mà tầng 020 không có** |

> ⭐ **Rủi ro cụ thể mà em muốn PM nhìn thẳng**: Brand Guidelines là tài liệu **dễ bịa persona nhất** trong toàn bộ SDLC, vì nó *cần* một audience để neo và một audience bịa ra **đọc rất trôi chảy**. Nếu run này sinh ra một persona, nó sẽ thành **nền móng giả cho cả tầng 040** — và mọi Wireframe / User Flow / UI Spec ở run sau sẽ neo vào nó mà **không ai kiểm chứng lại nguồn**. Đường đúng là: khai `TBD` ở mọi chỗ cần persona thật, và ghi rõ **KR4.3 là cơ chế đóng nó**.

---

## 5. Vấn đề phát hiện trong tài liệu nguồn — report-only, em KHÔNG sửa

| # | Vấn đề | Vị trí | Mức |
|---|---|---|---|
| 1 | ⚠️ **Ba file UC có tag XML của tool call lọt vào nội dung file** — `UC-09` kết thúc bằng `</content>` + `</invoke>` (sau dòng 166); `UC-10` kết thúc bằng `</content>` (sau dòng 189); `UC-11` kết thúc bằng `</content>` (sau dòng 205). Đây là **rác artifact**, không phải nội dung tài liệu | `UC-09`, `UC-10`, `UC-11` — cuối file | **Nên sửa** (nhưng ⛔ ngoài ownership của em) |
| 2 | **Số hàng `TBD` trong prompt của run sai** — prompt ghi 14, SRS §5.2 ghi **21**, SRS §3.9 ghi **7** (nghĩa khác) | prompt run · `SRS §5.2`, `§3.9` | **PM xử lý** — xem [§3.0](#30--đính-chính-con-số-trong-prompt-của-run) |
| 3 | ⭐ **Xung đột cross-layer về stack frontend** — `SRS-NFR-09` (tầng 020, mức độ rắn **CHƯA QUYẾT → `TBD`**) ghi: *"Ngôn ngữ / framework backend & frontend… Không anchor được"*. Trong khi `ADR-001` (tầng 030, ⚠️ **chưa commit**) đã chốt Vite + React + TS + **shadcn/ui + Tailwind**. Design System neo token vào ADR-001 ⇒ đang neo vào một quyết định mà **SRS chưa được cập nhật để phản ánh** | `SRS-NFR-09` vs `ADR-001` | ⭐ **Phải nêu ở gate** — trùng với `Q-C` của brief |
| 4 | **Bề mặt UI bắt buộc mà không UC nào phủ** — AI disclosure (`SRS-FR-40`) có requirement **CHỐT** và AC đo được, nhưng `Story-AI-Disclosure-Article-11` §2 xác nhận **không UC nào được gán cho nó** | `SRS-FR-40` · `Story-AI-Disclosure` §2 | **Khoảng trống traceability** |
| 5 | **Bề mặt operator không được mô tả ở đâu** — 6 UC gọi tên hành động của Founder-operator, không UC nào mô tả màn hình | S-19, §1.1 | **Khoảng trống** |
| 6 | ⭐ **Không một dòng nào về accessibility / responsive / thiết bị đích trong toàn `docs/020-Requirements/`** | grep 0 hit | ⭐ **Phải nêu ở gate** — xem [§3.4](#34--khoảng-trống-tuyệt-đối-accessibility--responsive--không-phải-tbd-mà-là-chưa-ai-từng-nhắc) |
| 7 | **`TBD` cấp component chưa ai đóng** — danh mục kiểu bubble (`UC-07` b6) · SFX/narration/caption (`UC-07` `AF-6`) · hành vi khi ảnh panel bị thay (`UC-07` `EX-8`) · tách một dòng thoại thành hai bubble (`UC-05` `AF-5`) · export từng phần (`UC-09` `AF-4`) · thủ tục counter-notice (`UC-11` `AF-1`) | 6 chỗ | ⛔ **Design System giữ nguyên `TBD`** |

---

## 6. Handoff cho PM

### 6.1 Thứ tự cắt lô writer — đề xuất theo mật độ nguồn, không theo `UNLOCK-ORDER` của code

`Backlog-Priority.md` xếp theo `UNLOCK-ORDER` cho **thứ tự build**. Với **thứ tự viết Design System**, ràng buộc khác: viết trước cái **có nhiều nguồn nhất** và **bị dùng lại nhiều nhất**.

| Lô | Nội dung | Vì sao ở lô này |
|---|---|---|
| **Lô 1** | **C-01** (alert ba mức) · **C-02** (error state) · **C-03** (status badge) · **C-04** (loading) | 13 / 10 / 9 / 7 surface. C-01 là chỗ **sai một lần là sai xuyên 13 màn hình** |
| **Lô 2** | **C-05** · **C-06** · **C-07** · **C-08** · **C-09** · **C-10** · **C-11** · **C-12** · **C-13** | Component nền còn lại (3–6 surface) |
| **Lô 3** | **C-14** · **C-15** · **C-16** | 1–2 surface nhưng **ràng buộc pháp lý cứng**, không hoãn được |
| **Lô 4** | C-17 … C-21, C-24 | Hoãn được sang run sau |
| ⛔ **Không làm** | C-22, C-23 (nhóm 10 — **ngoài horizon**) · toàn bộ danh sách cấm ở §2.3 | — |

### 6.2 Ba câu phải mang lên gate cho anh

| # | Câu hỏi | Vì sao agent không tự quyết được |
|---|---|---|
| **Q-BA-1** ⭐ | **Accessibility & thiết bị đích**: repo **không có một dòng nào**. Chọn một chuẩn (ví dụ WCAG 2.1 AA) và một breakpoint set là **quyết định mới ở tầng 040 mà tầng 020 không có căn cứ**. Anh chốt một chuẩn, hay Design System khai `TBD` + `PARTIAL`? | Không có nguồn để suy ra. Bịa ra sẽ thành chuẩn nghiệm thu của tầng QA |
| **Q-BA-2** | **Nhóm 11 (takedown công khai)** có mang cùng brand với sản phẩm không? Actor là **người ngoài, không tài khoản, có thể không bao giờ là khách hàng**; nghĩa vụ pháp lý ≠ trải nghiệm sản phẩm | Quyết định thương hiệu, thuộc Tầng 3 Escalation |
| **Q-BA-3** | **Nhóm 12 (operator)** có nằm trong scope Design System không? Không UC nào mô tả nó, `bus factor = 1` ⇒ có thể nó không cần một hệ thiết kế nào cả | Quyết định phạm vi của PM/Founder |

### 6.3 Ba điều writer **KHÔNG** được làm khi viết Design System

1. ⛔ **Không tự điền số cho bất kỳ hàng nào ở [§3.2](#32-nfr-tbd--design-system-phải-để-tbd--không-tự-điền-số).** Nguyên văn `SRS §5.2`: *"**Bịa một con số performance là lỗi nghiêm trọng hơn để trống nó** — vì con số bịa sẽ được tầng design và tầng QA dùng làm chuẩn nghiệm thu."*
2. ⛔ **Không viết persona.** Chỉ được neo vào [§4.4](#44-hệ-quả-trực-tiếp-lên-brand-guidelines--đọc-trước-khi-viết-một-dòng-nào) cột *được phép*.
3. ⛔ **Không gộp font UI với font render vào ảnh** ([§3.5](#35--ràng-buộc-dễ-bị-bỏ-sót-nhất-hai-hệ-font-không-phải-một)) — lỗi này chỉ lộ ra sau khi đã sinh ảnh, tức sau khi đã tiêu tiền thật.

---

## 7. Tài liệu tham khảo

| Tài liệu | Phần được dùng |
|---|---|
| `docs/020-Requirements/Use-Cases/UC-01` … `UC-11` | **Đọc đủ 11/11 file**, cả Main flow · Alternative flow · Exception flow. Trục chính của §1 và §2 |
| `docs/020-Requirements/SRS-Comic-Studio.md` | §3.C, §3.D, §3.E, §3.G · §3.9 audit đếm hàng · §4.1 User Interfaces · §4.3, §4.4 · **§5.1** (17 hàng có số), **§5.2** (21 hàng `TBD`) · §6.1 negative requirements |
| `docs/020-Requirements/PRD-Comic-Studio.md` | §3.1 phân khúc · §3.2 bốn actor · **§3.3** `TBD-1`…`TBD-5` · §5 bảy trục NFR (trục 5, 6 = `TBD`) |
| `docs/010-Planning/Charter-Comic-Studio.md` | **§6 Stakeholder Matrix (RACI)** + ba lỗ hổng · §7 `C1`, `C2`, `C4`, `C5` · §9 blocker |
| `docs/022-User-Stories/Backlog-Priority.md` | §2 framework `UNLOCK-ORDER` · §3.1 Pre-cycle/MVP0 (8) · §3.2 MVP1 (21) · §3.3 MVP2 (12) · §5 Story chưa xếp được (10, ngoài horizon) |
| `docs/022-User-Stories/Backlog/Story-AI-Disclosure-Article-11.md` | §1 actor · §2 (⚠️ không UC nào phủ) · §3 hai cách đọc phạm vi · **§4 AC** · §5, §6 |
| `docs/000-Index.md` | `L76` — xác nhận repo **không có persona/JTBD** |
| `docs/010-Planning/pm-runs/2026-08-30-…/brief.md` | Phạm vi run, Assumptions 2–4, Open questions `Q-A`…`Q-E` |
| `knowledge-base/45-Role-Memory/business-analyst/000-Core-Memory.md` | Traceability matrix · kỷ luật *"Unhappy Path"* rõ rệt |

> ⚠️ **Quy ước nhãn nguồn số liệu** — kế thừa nguyên vẹn: `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` thứ cấp · `[EM]` **ước lượng, không phải số đo** · `[CHỐT]` quyết định của Founder tại gate. **Copy một con số sang tài liệu khác thì copy cả nhãn** (`CẤM-15`).

---

_Findings by TNMCORE-OS — role `business-analyst`_
_Author: trisjr_
