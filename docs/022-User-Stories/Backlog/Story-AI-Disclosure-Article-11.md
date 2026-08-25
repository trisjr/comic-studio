---
id: STORY-G-06
type: story
status: draft
created: 2026-08-24
---

# Story-AI-Disclosure-Article-11

## 1. Story

> Là **độc giả / cơ quan quản lý**, tôi muốn **nội dung do AI tạo được đánh dấu**, để **nền tảng tuân thủ Luật TTNT 2025 trước deadline ~01/03/2027**.

## 2. Part of

| Quan hệ | Tài liệu |
|---|---|
| **Epic cha** | [Epic-Legal-And-Compliance](../Epics/Epic-Legal-And-Compliance.md) — hàng 6/6 mục 3 |
| **BRD cha** | [BRD-007-Legal-And-Compliance](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md) — `BR-007-05`, `BR-007-06`, `GP-4` §2 và §3.1 |
| **Use Case liên quan** | ⚠️ Không có Use Case nào trong ba UC đã tạo của run này (`UC-01`, `UC-06`, `UC-11`) được [Epic-Legal-And-Compliance §6.2](../Epics/Epic-Legal-And-Compliance.md#62-use-case-liên-quan) gán riêng cho nghĩa vụ AI disclosure. Không tự gán một UC không có căn cứ — xem [BRD-007 §7.2](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md#72-use-case-liên-quan) để xác nhận. |

## 3. Bối cảnh & nguồn

- **Hạng mục MVP-Scope**: [MVP-Scope §3 GP-4](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope) — `❌` ở MVP0 → `🟡` ở MVP1 và MVP2 → `✅` ở MVP3 (**NGOÀI HORIZON**). Theo quy ước `QC-3` của run này (cờ gán theo mốc **đầu tiên** hạng mục được giao), Story này là `[TRONG HORIZON]` vì bắt đầu ở MVP1.
- **Exit criterion Roadmap**: ⚠️ **[Security suy luận]** — không có exit criterion `M1-x`/`M2-x` nào của [Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) nêu tên AI disclosure/watermark tường minh (đã grep, không có kết quả). Anchor gần nhất được suy luận: **P-1** ([Roadmap §2 Pre-cycle](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) — *"3/3 câu CF-7.8 đã gửi tới một luật sư SHTT VN có tên, có xác nhận đã nhận"*). Lý do dùng suy luận này: câu **Q2** trong bộ ba câu hỏi CF-7.8 chính là câu hỏi xác định **phạm vi thật** của nghĩa vụ đánh dấu ở Story này (*"khoản 4 Điều 11 áp cho mọi nội dung AI, hay chỉ nội dung mô phỏng người thật?"*) — P-1 là exit criterion sở hữu việc gửi câu hỏi đó đi. ⛔ Đây **không phải** một exit criterion đo trực tiếp cơ chế đánh dấu, chỉ đo việc câu hỏi quyết định phạm vi đã được gửi đi.
- **Căn cứ pháp lý — HAI văn bản số `134` KHÁC NHAU, không được trộn**:

  | Văn bản | Điều khoản dùng ở Story này | Hiệu lực | Nhãn |
  |---|---|---|---|
  | **LUẬT TRÍ TUỆ NHÂN TẠO 2025 — Luật số 134/2025/QH15** | **Điều 11** (minh bạch) · **khoản 4 Điều 11** (gắn nhãn + đánh dấu định dạng máy đọc) · **Điều 8** (chuyển tiếp 12 tháng) | thông qua **10/12/2025**, **hiệu lực 01/03/2026** ⇒ deadline tuân thủ của comic-studio **~01/03/2027** | `[OFF]` — ⚠️ **hai nguồn mô tả phạm vi khoản 4 Điều 11 KHÁC NHAU** |

  > ⚠️ **Đây KHÔNG phải Nghị định 134/2026/NĐ-CP** (Điều 5a/37a/37b, hiệu lực 09/04/2026, thuộc `Story-Provenance-Chain-Parent-Generation` và `Story-Opt-Out-Check-At-Ingest`). Hai văn bản, hai số hiệu na ná nhau, hai nghĩa vụ khác nhau — Story này **chỉ** dùng Luật số 134/2025/QH15.

- **Mâu thuẫn phạm vi — ghi cả hai, không chọn một** ([BRD-007 §3.1](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md#31-gp-4--hai-cách-đọc-trong-repo-mâu-thuẫn-về-phạm-vi)):

  | Cách đọc | Phát biểu | Hệ quả kỹ thuật nếu đúng |
  |---|---|---|
  | **HẸP** | Nghĩa vụ gắn nhãn chỉ áp cho nội dung AI tạo/chỉnh sửa nhằm *"mô phỏng người thật hoặc sự kiện thực tế"* | Gần như là một dòng metadata |
  | **RỘNG** | Nhà cung cấp phải đảm bảo nội dung do hệ thống AI tạo ra được đánh dấu bằng định dạng máy đọc, **không** giới hạn ở "mô phỏng người thật" | Một hạng mục kỹ thuật ở export path + provenance field cấp page/panel |

- **Cách xử lý đã chốt** ([Charter §7 C4](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints)): *"Vì phạm vi chưa rõ, phải **thiết kế theo diễn giải rộng** (mọi nội dung AI) **cho tới khi luật sư chốt**."* ⇒ Story này implement **cơ chế** theo diễn giải rộng; **phạm vi thật vẫn là `TBD`** và là câu **Q2 của gate G0**.
- ⚠️ **`TBD` không giả định**: **SynthID** (đã nhúng sẵn trong Nano Banana Pro) có thoả nghĩa vụ đánh dấu hay không — *"phải verify, không giả định"* (Analysis §8.4, [BRD-007 BR-007-06](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md#3-yêu-cầu-nghiệp-vụ)).
- **`Valuable-I`**: deadline **~01/03/2027** nằm ngay sau horizon (09/2026–02/2027) — không xây cơ chế đánh dấu từ trong horizon nghĩa là chạy vào deadline mà không có nền tảng kỹ thuật đã sẵn sàng ([Charter §7 C4](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints)).
- **Ràng buộc positioning liên quan**: [Charter §7 C5](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints) — *"disclosure-first, nhắm writer KHÔNG nhắm artist"*; disclosure không phải chi phí tuân thủ mà là **ràng buộc phân phối** (`Glossary.md` term *disclosure-first positioning*).

## 4. Acceptance Criteria

### Xác minh được

- [ ] Có **cơ chế trong sản phẩm để người dùng nhận biết đang tương tác với hệ thống AI** (Điều 11, minh bạch) — đo bằng: xác nhận tồn tại một chỉ dẫn/thông báo hiển thị cho người dùng tại điểm tương tác với tính năng AI (ví dụ tại bước generate/pick variant), không phải chỉ ghi trong ToS.
- [ ] Mỗi nội dung do AI tạo mang một **provenance field ở cấp page/panel** xác định nguồn gốc AI (dựa trên `generation.origin` đã có từ `Story-Provenance-Chain-Parent-Generation`) — đo bằng: truy vấn một page/panel bất kỳ, xác nhận field này tồn tại và có giá trị.
- [ ] **Export path nhúng được machine-readable watermark/marker** cho nội dung do AI tạo — đo bằng: export một chapter chứa nội dung AI, kiểm tra file export có marker đọc được bằng công cụ (ví dụ đọc metadata nhúng), không chỉ đọc được bằng mắt.
- [ ] Cơ chế đánh dấu áp dụng theo **diễn giải RỘNG** (mọi nội dung AI, không giới hạn ở "mô phỏng người thật") đúng như quyết định `Charter §7 C4` — đo bằng: kiểm tra một nội dung AI **không** mô phỏng người thật (ví dụ nhân vật hư cấu hoàn toàn) vẫn được đánh dấu.

### Đường không hạnh phúc (unhappy path)

- [ ] Nội dung **hỗn hợp** (một phần AI, một phần con người chỉnh sửa nặng — `origin = 'ai_edited'`) phải có cách đánh dấu phản ánh đúng bản chất hỗn hợp, không được mặc định gắn nhãn "hoàn toàn con người" hoặc "hoàn toàn AI" một cách sai lệch.
- [ ] Nếu export path bị lỗi và không nhúng được marker (ví dụ định dạng export không hỗ trợ metadata), quá trình export phải **thất bại rõ ràng hoặc cảnh báo**, không được xuất ra file thiếu marker mà coi như thành công.
- [ ] Marker bị người dùng cuối (không phải chủ tenant) cố tình strip khỏi file export (ví dụ qua công cụ bên ngoài) là **ngoài phạm vi kiểm soát kỹ thuật** của Story này — ghi nhận đây là giới hạn đã biết, không phải lỗi của Story.

### Ràng buộc cứng không được vi phạm

- `C4` — deadline pháp lý ~01/03/2027, hai nguồn mô tả phạm vi khác nhau ⇒ phải thiết kế theo diễn giải RỘNG cho tới khi luật sư chốt ([Charter §7](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints)).
- `C5` — positioning bắt buộc disclosure-first, nhắm writer không nhắm artist ([Charter §7](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints)).

### Story này KHÔNG làm

- [ ] **KHÔNG** chọn một trong hai cách đọc phạm vi khoản 4 Điều 11 rồi trình bày như sự thật đã chốt — phạm vi thật giữ nguyên `TBD`, là câu Q2 của gate G0, chờ luật sư SHTT.
- [ ] **KHÔNG** khẳng định SynthID (hoặc watermark của bất kỳ model provider nào) thoả hay không thoả nghĩa vụ đánh dấu — phải verify riêng, không giả định trong Story này.
- [ ] **KHÔNG** marketing hay truyền thông vào cộng đồng hoạ sĩ dựa trên cơ chế đánh dấu này — đó là vi phạm `C5`/anti-goal `AG-2` ([OKRs §6](../../010-Planning/OKRs.md#6-anti-goals)), nằm ngoài phạm vi kỹ thuật của Story.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | `TBD` | Không có ước lượng bottom-up trong repo. **Điều kiện escalate**: nếu ước lượng thực tế lúc nhặt Story lên vượt **16 giờ-người**, split Story (ví dụ tách "thông báo minh bạch trong UI" khỏi "watermark ở export path") hoặc ghi lý do vượt trần thành văn — chi phí thật phụ thuộc câu trả lời `TBD` của Q2/SynthID nên biến động là dự kiến trước, không phải ước lượng sai. |
| `E_hitl` | `0` giờ-người/chapter | Cơ chế đánh dấu được thiết kế để tự động (thông báo UI cố định + nhúng marker ở export path), không tạo bước xác nhận thủ công theo từng chapter. |

## 6. INVEST

| Tiêu chuẩn | Đánh giá |
|---|---|
| Independent | ✅ Không nằm trong danh sách vỡ Independent của [`findings/business-analyst.md` §4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md#410-bảy-story-sẽ-vỡ-khi-cắt-lô--pm-cần-biết-trước). §4.7 chấm `I = ✅`. |
| Negotiable | ⚠️ **Bị giới hạn ở cơ chế** (phải tồn tại provenance field + export marker theo diễn giải rộng), nhưng **negotiable ở tham số** — phạm vi hẹp/rộng và việc SynthID có đủ hay không đều là `TBD` chờ luật sư, không phải quyết định cứng của Story. |
| Valuable | `Valuable-I` — xem mục 3: deadline pháp lý nằm ngay sau horizon; không xây nền trong horizon là rủi ro chạy vào deadline mà chưa có cơ chế. |
| Estimable | Estimable bằng giờ-người, hiện `TBD` — xem mục 5. |
| Small | ⚠️ [Security suy luận] — §4.7 chấm `S = ⚠️` nhưng không có dòng nào trong §4.10 giải thích lý do. Suy luận: kích thước thực tế của Story phụ thuộc vào một biến chưa biết — **phạm vi hẹp hay rộng** của khoản 4 Điều 11 và **SynthID có thoả hay không** (CF-7.7 ⚠️ hai nguồn mô tả khác nhau; Analysis §8.4 *"phải verify, không giả định"*). Nếu SynthID thoả và phạm vi đọc hẹp, chi phí gần bằng một dòng metadata; nếu ngược lại, chi phí là một hạng mục kỹ thuật đầy đủ ở export path — biên độ dao động lớn này tự nó là một lý do `Small` khó chấm chắc trước khi có câu trả lời Q2. |
| Testable | Testable bằng checklist assertion nhị phân — xem mục 4 AC-1/AC-2. |

> **Kết luận mục 6**: `I = ✅` theo §4.7. `S = ⚠️` theo §4.7 nhưng không có dòng §4.10 tương ứng ⇒ lý do trên mang nhãn `[Security suy luận]`, gắn trực tiếp với khoảng trống `TBD` đã nêu ở mục 3.
