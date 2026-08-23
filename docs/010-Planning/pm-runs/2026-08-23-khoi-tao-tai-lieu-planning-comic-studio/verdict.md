# Verdict: 2026-08-23-khoi-tao-tai-lieu-planning-comic-studio

**Bước 6 — Verification & Close.** Verifier: `context-auditor`, **instance mới, context sạch**, không viết deliverable nào trong run. Báo cáo đầy đủ: [findings/verify-report.md](./findings/verify-report.md).

| | |
|---|---|
| **STATUS của verifier** | `DONE` |
| **CRITICAL** | **0** |
| **MAJOR** | 4 — **đã sửa 4/4** |
| **MINOR** | 5 — **đã sửa 2, chấp nhận 3** |
| **Quyết định của PM** | ✅ **Đóng run.** 0 CRITICAL ⇒ không kích hoạt điều khoản *"quay lại Bước 5"* của `pm-doc.md`. Bốn MAJOR tổng cộng ~12 dòng edit cục bộ, PM tự vá tại close-step. |
| **Chi phí verify** | 89 turn · 14,36M cache read · 54.645 output · **49/60 tool call** |

---

## 1. Sáu tiêu chí

Run này dùng **sáu** tiêu chí thay vì bốn: bốn tiêu chí chuẩn của lane doc, cộng **hai tiêu chí đặc thù** được thêm vì run song song hoá bốn writer trên các tài liệu ghép chặt.

| # | Tiêu chí | Kết quả | Bằng chứng |
|---|---|---|---|
| 1 | **Completeness** | ✅ **Đạt tuyệt đối** | Mọi ngưỡng định lượng đều **vượt**: Risk Register 23 rủi ro (yêu cầu ≥16) · Research Notes 41 URL (≥25) · OKRs 8 anti-goal (≥4) · Charter RACI 9×5 (≥8×5). ⭐ **Hai file sửa stub KHÔNG dính failure mode ghi đè** — `Roadmap.md` và `OKRs.md` đều giữ đúng `id` và `created: 2026-02-04`, có `updated: 2026-08-23` |
| 2 | **Correctness** | ⚠️ Đạt, 2 issue | Mọi khẳng định định lượng trace được về CF hoặc nguồn. Hai issue đều là **mất nhãn**, không phải sai số |
| 3 | **Coherence** | ⚠️ Đạt, 2 issue | Research Notes **không trùng lặp** với `Analysis-Comic-Studio-Concept` — link sang đúng như yêu cầu. Hai issue là xung đột con số giữa hai tài liệu |
| 4 | **Connectivity** | ✅ **Sạch** | **0 link chết · 0 wiki-link `[[...]]` · 0 file orphan** trên toàn bộ 6 deliverable |
| 5 | ⭐ **Cross-doc consistency** | ✅ **Đạt** | **10 con số CF dùng chung khớp giá trị VÀ giữ nhãn ở mọi nơi.** Cả **hai cạm bẫy đã biết đều bị chặn bằng lệnh cấm tường minh**, không phải nhờ may |
| 6 | ⭐ **Sweep khuyến nghị bị rơi** | ✅ **0 khuyến nghị bị rơi** | Quét cơ học: Risk Register **17/17** mục bắt buộc · OKRs **4/4** anti-goal bắt buộc · Research Notes **23/23** khoảng trống đủ 5 nhóm **gồm cả 5.e Việt Nam** · Charter đủ **CHÍN** điều kiện · MVP-Scope §6 và §8 đầy đủ · 7/7 khuyến nghị §B của `researcher.md` đều landed |

### Vì sao tiêu chí 5 và 6 xứng đáng tồn tại

**Tiêu chí 6 là bài học trực tiếp từ run trước**, nơi **2 lỗi MAJOR** đều là *khuyến nghị có trong findings nhưng rơi mất khỏi deliverable* — và chúng chỉ bị bắt vì verifier **tự chủ động** đi tìm. Bốn tiêu chí chuẩn được định nghĩa để bắt cái **THỪA** (khẳng định vô căn cứ), **không bắt được cái THIẾU**. Run này biến hành vi tự phát đó thành **yêu cầu tường minh trong prompt dispatch**, và kết quả là **0 khuyến nghị bị rơi**.

**Tiêu chí 5 là rủi ro do chính run này tạo ra** khi song song hoá 4 writer trên 5 tài liệu ghép chặt. Đối sách là bảng **canonical facts** trong `outline.md`. Bằng chứng nó hoạt động:

- `MVP-Scope.md:249` **viết thẳng** rằng phép trừ `50–60% − 20–25%` là sai số học (hai mẫu số khác nhau).
- `Analysis-Market:376-383` có **khối cảnh báo riêng** rằng nói *"23% và 21,1% khớp nhau"* là sai (GRR ≠ payer retention).

Cả hai đều là **lệnh cấm tường minh trong outline** được writer chép vào deliverable. Bảng canonical facts không chỉ cấp số — nó cấp cả **lý do không được làm gì với số đó**, và đó là phần tạo ra hiệu quả.

---

## 2. Disposition từng issue

### MAJOR — đã sửa 4/4

| # | Vấn đề | Disposition |
|---|---|---|
| **M-1** | `Glossary.md:96` — `23% GRR` **mất nhãn `[OFF]` và mất cả ba caveat CF-4.7**, viết thành *"con số ngành là 23%"*. **Đây là nơi DUY NHẤT trong repo con số này đi trần trụi**; cả 4 deliverable đều giữ đủ ba caveat | ✅ **Đã sửa** — thêm nhãn `[OFF]`, ghi rõ nguồn ChartMogul + cỡ mẫu + năm dữ liệu, và chèn blockquote đủ **ba caveat** kèm link tới `Analysis-Market §5.1`. Thêm cả kết luận chịu lực (*"vấn đề không phải AI churn mà là GIÁ"* — cùng dataset, >$250/tháng đạt 70%) |
| **M-2** | `MVP-Scope.md:427,428` — `−141%` và `+40%` dùng **không có nhãn `[EM]`**; dòng 428 còn đặt `+40%` cạnh `50–60%` `[BCN]`. Đối chứng: `Roadmap.md:67` xử lý ca y hệt **đúng cách** ⇒ là bỏ sót, không phải quy ước | ✅ **Đã sửa** — gắn `[EM]` cho cả hai, kèm giải thích chúng là kết quả **reverse-engineer từ giá công bố của ComicInk**, không phải margin đo được của công ty nào. Thêm một cảnh báo nữa: so `[EM]` với `[BCN]` thì kết luận đúng về **hướng** nhưng **không đủ chắc để làm ngưỡng gate** |
| **M-3** | Checklist safe harbour 198b ghi **6 mục** ở `Risk-Register.md:75,189` nhưng **3 mục** ở `OKRs.md:187`. Hai thước cho **cùng một điều kiện rời gate G0** | ✅ **Đã sửa — và PM xác minh nguồn gốc trước khi chọn bên.** Đọc `Analysis §8.3` (dòng 702–712): bảng có **đúng 6 hàng**. CF-7.6 chỉ tóm tắt **3 trong số đó**, và đó chính là nguồn của sai lệch. Risk-Register đúng ⇒ sửa `OKRs.md` thành **6/6 mục**, liệt kê đủ, và **trỏ về `Risk-Register` R-02 làm danh sách chuẩn** để về sau chỉ có một nơi sửa |
| **M-4** | `Charter.md:94-98` đặt ID mục tiêu `G1…G5` **va chạm tên gate** `G0/G1/G2` ở `:238`. Sắc nhất: hàng mang ID **G2** lại trỏ tới *"gate G1"* | ✅ **Đã sửa** — đổi ID mục tiêu thành `MT-1…MT-5`, tách hẳn hai namespace. Thêm một blockquote `[!IMPORTANT]` nói rõ **chúng không ánh xạ 1-1** (`MT-2` và `MT-3` đều lấy ngưỡng từ **gate G1**) để lần sau không ai cố ghép chúng lại |

### MINOR — sửa 2, chấp nhận 3

| # | Vấn đề | Disposition |
|---|---|---|
| m-1 | `MVP-Scope.md:289` — KC-4 ghi *"cả **bốn** mục KC-1…KC-3"*, nhưng KC-1→KC-3 là **ba** mục | ✅ **Đã sửa** — "cả **ba** mục KC-1, KC-2, KC-3" |
| m-2 | Phân bổ thành phần editor **lệch ba chiều**: `MVP-Scope:136` (D1) ↔ `MVP-Scope:259-263` (§5) ↔ `Roadmap:105` | ✅ **Đã sửa** — đồng bộ hàng D1 theo **§5** (nguồn chi tiết nhất): MVP1 = #5 · MVP2 = #3, #4, **bắt đầu** #2 · MVP3 = hoàn tất #2 + thêm #1. Roadmap:105 vốn đã khớp §5 |
| m-3 | Tổng năm thành phần editor cộng ra **20–30%**, nhưng con số tổng ghi **~20–25%** | ✅ **Đã xử lý theo cách khác — không sửa số, mà phơi bày chênh lệch.** PM truy về nguồn: `Analysis §6.1` đưa **cả** năm khoảng thành phần **và** con số tổng *"~20-25%"*, và **hai thứ đó vốn đã không khớp ở biên trên**. Sửa một trong hai là âm thầm chọn bên trên một dữ liệu mà nguồn không phân xử. ⇒ Giữ `~20–25%` của CF-6.7 làm số chuẩn (để mọi tài liệu trích cùng một giá trị), **thêm blockquote ghi lại chênh lệch** và khuyến nghị dùng **30%** khi lập ngân sách thời gian thận trọng |
| m-4 | Đề xuất bổ sung **6 term** vào Glossary | ⏸️ **Chấp nhận, không làm trong run này.** Glossary đã tăng từ 40 → **54 term** ở close-step (nhóm mới *Planning, thị trường & quản trị*, 14 term). Sáu term còn lại là đề xuất tốt nhưng thuộc run dọn dẹp — thêm nữa sẽ vượt scope đã duyệt tại gate |
| m-5 | Ba nghi ngờ verifier **không xác minh được bằng quy tắc có sẵn**, xếp riêng vào mục *cần PM tự kiểm* | 📋 **PM đã xử lý — xem mục 3.** Verifier làm đúng khi **không** đẩy chúng lên MAJOR |

> ⭐ **Đáng ghi nhận về chất lượng verify**: verifier **không** đẩy ba nghi ngờ chưa xác minh được lên MAJOR mà tách riêng thành mục *cần PM tự kiểm*, đúng như prompt yêu cầu (*"một false positive ở tiêu chí 5 tốn của PM một vòng sửa vô ích"*). Và với M-2, nó **tự tìm đối chứng** (`Roadmap.md:67` xử lý ca y hệt đúng cách) để phân biệt **bỏ sót** với **quy ước có chủ đích** — đó là bước mà một verifier cẩu thả sẽ bỏ, và nó quyết định issue này đáng sửa hay không.

---

## 3. Ba điểm verifier chuyển cho PM tự kiểm

| # | Nghi ngờ | Phân xử của PM |
|---|---|---|
| 1 | Deliverable link thẳng vào `pm-runs/**` | **Chấp nhận, không sửa.** `pm-runs/` là run-state nhưng **không phải khu vực cấm đọc** — nó được `Planning-MOC.md` trỏ tới hợp lệ và `README.md` của nó là tài liệu công khai. Guardrail cấm **sửa** run-state, không cấm **trỏ tới** nó. Một link tới `findings/researcher.md` từ tài liệu Research là truy vết đúng, không phải rò rỉ sổ tay nội bộ |
| 2 | `outline.md` trích `findings/researcher.md §A.5` nhưng file đó **không có heading `§A.5`** | ✅ **Đúng, và là lỗi của PM.** File dùng `## Câu 5 — Kênh phân phối...` chứ không đánh số `A.5`; tiền tố `A.` là do PM bọc toàn văn báo cáo vào *"Mục A"* rồi trích theo hệ đánh số không tồn tại. **Không sửa `outline.md`** (nó là run-state, đã đóng vai trò contract của run này và writer vẫn tìm đúng mục). Ghi lại làm bài học: **trích một tài liệu bằng hệ đánh số mà chính tài liệu đó không dùng** thì writer phải đoán — lần này đoán đúng, lần sau chưa chắc |
| 3 | Cách đếm thư mục | ✅ **Đã tự kiểm.** `find docs -type d` khớp **100%** khối *Required Folder Structure* của RULE-001; 32 thư mục mới, 32 `.gitkeep`. Con số 32 của inventory chính xác |

---

## 4. Close-step — RULE-001 Validation Checklist

| Hạng mục | Trạng thái |
|---|---|
| Đúng thư mục theo Document Type Mapping | ✅ 6/6 |
| Naming convention | ✅ 6/6 |
| Frontmatter `id / type / status / created` | ✅ 6/6 · **2 file sửa stub giữ đúng `id` + `created`, có `updated`** |
| Standard markdown link, **không** wiki-link | ✅ **0 occurrence `[[`** trên toàn bộ deliverable |
| Link phân giải được | ✅ 0 link chết |
| MOC thư mục cha đã cập nhật | ✅ `Planning-MOC.md` (viết lại, 5 tài liệu + sửa dòng ghi sai `/pm-run`) · `Research-MOC.md` · `Resources-MOC.md` (liệt kê đủ 13 template, lần đầu tiên) |
| `docs/000-Index.md` | ✅ **ĐÃ TẠO** — RULE-001 ghi *"BẮT BUỘC phải có"*, trước run này **không tồn tại**. Đóng luôn 2 link chết trỏ tới nó |
| Cấu trúc Dewey | ✅ **32 thư mục + 32 `.gitkeep`**, `find` khớp 100% |
| Glossary | ✅ **40 → 54 term**, nhóm mới *Planning, thị trường & quản trị* |
| RULE-001 amendment | ✅ Thêm **một hàng** `MVP Scope`, bump `updated`, kèm changelog nêu rõ là **additive** và được duyệt tại gate nào |
| Tài liệu bị thay thế → `090-Archive/` | — không có. Thư mục đã được tạo, đang rỗng |

---

## 5. Kết luận

**Run đóng.** Sáu deliverable ở `status: draft` — đúng trạng thái đích đã khai trong `outline.md`, và đúng bản chất của chúng: cả bộ tài liệu này kết luận rằng **ba việc phải xong trước dòng code đầu tiên**, trong đó có việc mang ba câu hỏi pháp lý tới luật sư SHTT Việt Nam. Chúng chuyển `approved` khi anh ra quyết định Go/No-Go tại gate **G0**, không phải khi chúng được viết xong.

**Điều đáng nói nhất của run này không nằm ở số issue, mà ở việc issue nào KHÔNG xảy ra.** Bốn writer chạy song song trên năm tài liệu ghép chặt — kịch bản mà lỗi mặc định là *"mỗi tài liệu một bộ số"*. Kết quả: 10 con số dùng chung khớp ở mọi nơi, cả hai cạm bẫy số học đã biết đều bị chặn, và 0 khuyến nghị bị rơi. Bốn MAJOR còn lại đều là **mất nhãn hoặc va chạm tên**, không cái nào là **sai nội dung**.

Xem thêm: [brief.md](./brief.md) · [run-plan.md](./run-plan.md) · [outline.md](./outline.md) · [findings/verify-report.md](./findings/verify-report.md) · [cost.md](./cost.md)
