---
id: STORY-G-03
type: story
status: draft
created: 2026-08-24
---

# Story-Opt-Out-Check-At-Ingest

## 1. Story

> Là Founder (operator), tôi muốn **kiểm opt-out signal Điều 37b ngay tại bước ingest**, để **hệ thống không xử lý nội dung có opt-out trước khi biết**.

## 2. Part of

| Quan hệ | Tài liệu |
|---|---|
| **Epic cha** | [Epic-Legal-And-Compliance](../Epics/Epic-Legal-And-Compliance.md) — hàng 3/6 mục 3 |
| **BRD cha** | [BRD-007-Legal-And-Compliance](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md) — `BR-007-03`, `KC-6` §4.1 |
| **Use Case liên quan** | [UC-01 — Upload And Ingest Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) — bước ingest là nơi **DUY NHẤT** file của user lần đầu vào hệ thống |

## 3. Bối cảnh & nguồn

- **Hạng mục MVP-Scope**: [MVP-Scope §3 GP-2](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope) — `❌` ở MVP0 → `✅` ở MVP1. [MVP-Scope §6 KC-6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng).
- **Exit criterion Roadmap**: [Roadmap §2 — M1-4](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) — *"100% file upload đi qua bước kiểm opt-out Điều 37b"*.
- **Căn cứ pháp lý**: **NĐ 134/2026/NĐ-CP, Điều 37b** `[OFF]` **tóm tắt** (CF-7.5) — bốn kênh bảo lưu quyền: metadata · biện pháp bảo vệ công nghệ · thông tin quản lý quyền dạng máy đọc · thông báo công khai từ tổ chức quản lý tập thể ([BRD-007 §3 BR-007-03](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md#3-yêu-cầu-nghiệp-vụ)). ⚠️ Nhãn `[OFF]` này là **bản tóm tắt**, không phải nguyên văn — nguồn gốc trả 403/paywall (CF-7.4, `KT-5`).
- **`Valuable-I`**: đây là nơi duy nhất file của user lần đầu đi vào hệ thống — kiểm ở chỗ khác nghĩa là **đã xử lý nội dung có opt-out trước khi biết**, và một lần xử lý sai là *"một vi phạm đã xảy ra, không sửa hồi tố được"* ([Risk-Register R-06](../../010-Planning/Risk-Register.md)).
- ⛔ **CẤM-13** ([BRD-007 §4.5](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md#45-ràng-buộc-về-chất-lượng-nguồn--bắt-buộc-mang-theo)): cấm viết requirement như thể phạm vi **Điều 37a** (TDM, câu hỏi Q1 của gate G0) đã rõ. Story này chỉ kiểm **opt-out (Điều 37b)**, không mở rộng sang diễn giải phạm vi Điều 37a.
- ⚠️ **Anti-feature liền kề** ([BRD-007 §5.2](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md#52-không-xây-bộ-phát-hiện-bản-quyền-chủ-động--đây-là-anti-feature) · [Risk-Register R-04](../../010-Planning/Risk-Register.md)): đọc **opt-out signal do chính chủ quyền gắn vào file** là dữ kiện khách quan, **khác** với việc chủ động phát hiện bản quyền — ranh giới này phải được giữ khi implement Story này.

## 4. Acceptance Criteria

### Xác minh được

- [ ] **100%** file upload (đo trên tổng số file đi qua endpoint ingest trong một cửa sổ thời gian bất kỳ) có một bản ghi log kết quả kiểm opt-out — đo bằng đếm số file upload so với số dòng log kiểm tra tương ứng, kỳ vọng bằng nhau.
- [ ] Mỗi lần kiểm opt-out ghi log kèm **timestamp** và kết quả (`có signal` / `không có signal`) — đo bằng đọc trực tiếp một dòng log mẫu, xác nhận có đủ hai trường.
- [ ] File có ít nhất một trong bốn kênh bảo lưu quyền (metadata / biện pháp bảo vệ công nghệ / rights-management-info dạng máy đọc / thông báo công khai từ tổ chức quản lý tập thể đã biết) bị **chặn xử lý tiếp** ở bước ingest — đo bằng: upload một file test có gắn metadata opt-out, kỳ vọng pipeline dừng lại trước bước extraction, không tạo ra `generation` hay `usage_event` nào từ file đó.
- [ ] Bước kiểm opt-out chạy **trước** mọi bước xử lý nội dung khác trong pipeline ingest (text clean, extraction) — đo bằng kiểm tra thứ tự bước trong code pipeline hoặc trace log.

### Đường không hạnh phúc (unhappy path)

- [ ] File có metadata bị hỏng hoặc không đọc được (corrupt) phải được xử lý theo hướng **an toàn** (log kết quả `không đọc được` và chặn, hoặc route sang hàng đợi kiểm tay) — **không** được coi mặc định là `không có signal` rồi cho qua.
- [ ] File có nhiều kênh bảo lưu quyền mâu thuẫn nhau (ví dụ metadata nói không opt-out nhưng công cụ bảo vệ công nghệ báo có) phải bị chặn (fail-safe theo hướng bảo thủ hơn), không được ưu tiên kênh cho phép xử lý.
- [ ] Batch upload nhiều file cùng lúc mà một file giữa batch có opt-out signal: chỉ file đó bị chặn, các file khác trong cùng batch không có signal vẫn được xử lý bình thường — đo bằng test batch hỗn hợp.

### Ràng buộc cứng không được vi phạm

- `KC-6` — kiểm opt-out signal Điều 37b ngay trong bước ingest, bắt buộc từ MVP1, chi phí giữ ~0.

### Story này KHÔNG làm

- [ ] **KHÔNG** xây bộ phát hiện bản quyền chủ động (`copyright detection`, `plagiarism check`, `similarity scan`) — đây là **anti-feature** có thể phá chính miễn trừ Điều 198b ([Risk-Register R-04](../../010-Planning/Risk-Register.md)). Story này **chỉ** đọc tín hiệu khách quan do chính chủ quyền gắn vào file.
- [ ] **KHÔNG** diễn giải hay khẳng định phạm vi Điều 37a (TDM) — đó là câu hỏi Q1 của gate G0, thuộc luật sư, không thuộc Story này (`CẤM-13`).
- [ ] **KHÔNG** xử lý yêu cầu takedown từ bên ngoài — đó là phạm vi `Story-Safe-Harbour-Checklist-Article-198b` (`GP-3`).

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | `TBD` | Không có ước lượng bottom-up trong repo. `MVP-Scope §6 KC-6` ghi chi phí giữ là **~0** (CF-7.5 `[OFF]` tóm tắt) — đây là ước lượng chi phí **vận hành**, không phải giờ-người xây dựng. **Điều kiện escalate**: nếu ước lượng thực tế lúc nhặt Story lên vượt **16 giờ-người**, phải split Story (Story này **không** nằm trong danh sách vỡ Independent/Small của §4.10, nên split là lựa chọn hợp lệ) hoặc ghi lý do vượt trần thành văn. |
| `E_hitl` | `0` giờ-người/chapter | Cơ chế kiểm là tự động (đọc metadata + log + chặn), không tạo bước xác nhận thủ công theo chapter. Trường hợp file không đọc được metadata cần route sang hàng đợi kiểm tay (xem AC-2) là **ngoại lệ vận hành**, chưa có số đo tần suất — nếu tần suất này đáng kể trên thực tế, đó là tín hiệu escalate. |

## 6. INVEST

| Tiêu chuẩn | Đánh giá |
|---|---|
| Independent | ✅ Không nằm trong danh sách vỡ Independent của [`findings/business-analyst.md` §4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md#410-bảy-story-sẽ-vỡ-khi-cắt-lô--pm-cần-biết-trước). §4.7 chấm `I = ✅`. |
| Negotiable | ⚠️ **Bị giới hạn** — Story chạm `KC-6`, một trong bảy mục không mở ra thương lượng scope. |
| Valuable | `Valuable-I` — xem mục 3: xử lý sai một lần là vi phạm không sửa hồi tố được. |
| Estimable | Estimable bằng giờ-người, hiện `TBD` — xem mục 5. |
| Small | ✅ §4.7 chấm `S = ✅`. Không có dòng nào trong §4.10 nêu lý do vỡ cho Story này — phù hợp với chấm điểm ✅. |
| Testable | Testable bằng checklist assertion nhị phân — xem mục 4 AC-1/AC-2. |

> **Kết luận mục 6**: `I` và `S` đều `✅` theo §4.7 — không cần nhãn `⚠️` hay `[Security suy luận]` cho Story này.
