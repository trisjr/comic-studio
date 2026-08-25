---
id: STORY-G-05
type: story
status: draft
created: 2026-08-24
---

# Story-Safe-Harbour-Checklist-Article-198b

## 1. Story

> Là **chủ sở hữu quyền (bên ngoài)**, tôi muốn **có công cụ takedown và một đầu mối đã đăng ký với Bộ VHTTDL, xử lý trong SLA 72 giờ**, để **yêu cầu của tôi được xử lý theo luật**.

## 2. Part of

| Quan hệ | Tài liệu |
|---|---|
| **Epic cha** | [Epic-Legal-And-Compliance](../Epics/Epic-Legal-And-Compliance.md) — hàng 5/6 mục 3 |
| **BRD cha** | [BRD-007-Legal-And-Compliance](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md) — `BR-007-04`, `GP-3` §2 |
| **Use Case liên quan** | [UC-11 — Handle Takedown Request](../../020-Requirements/Use-Cases/UC-11-Handle-Takedown-Request.md) — luồng chính của Story này; **primary actor là chủ sở hữu quyền, một actor NGOÀI hệ thống** |
| **Điều kiện chặn liên quan** | `BLOCKER-02` ([Charter §9.3](../../010-Planning/Charter-Comic-Studio.md#93-ba-điều-kiện-chặn-phụ)) — chặn **mở cho người ngoài upload** (không chặn dùng nội bộ) |

## 3. Bối cảnh & nguồn

- **Hạng mục MVP-Scope**: [MVP-Scope §3 GP-3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope) — `❌` ở MVP0 → `🟡` ở MVP1 → `✅` ở MVP2.
- **Exit criterion Roadmap**: [Roadmap §2 — M2-6](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) — *"checklist safe harbour Điều 198b hoàn thành nếu trigger 'mở cho người ngoài upload' đã đến"*. Neo **TRIGGER**, không neo ngày: [Roadmap §4 X-a](../../010-Planning/Roadmap.md#4-ba-việc-xen-ngang) — *"Trước lần đầu mở cho NGƯỜI NGOÀI upload"*, đặt ở **MVP2** hoặc **sớm hơn nếu trigger đến sớm hơn**.
- **Căn cứ pháp lý**: **Luật Sở hữu trí tuệ sửa đổi 2022 — Luật 07/2022/QH15, Điều 198b** `[OFF]` **tóm tắt** (CF-7.6) — miễn trừ trách nhiệm cho *"doanh nghiệp cung cấp dịch vụ trung gian"*, có điều kiện, không tự động. Kèm **Nghị định 17/2023/NĐ-CP** — nghĩa vụ notice-and-takedown, đầu mối liên hệ với **Bộ Văn hoá, Thể thao và Du lịch**.
- **Checklist đủ 6/6 mục** ([Epic-Legal-And-Compliance mục 3](../Epics/Epic-Legal-And-Compliance.md#3-story-trong-horizon)): (a) công cụ takedown, (b) đầu mối đăng ký Bộ VHTTDL, (c) SLA 72 giờ, (d) **KHÔNG chủ động rà soát nội dung**, (e) user warrant + indemnify trong ToS, (f) kiểm opt-out trước khi xử lý.
- **`Valuable-I`**: [Roadmap §4 X-a](../../010-Planning/Roadmap.md#4-ba-việc-xen-ngang) — *"Một lần upload của người ngoài mà chưa có đường takedown là đã tạo ra nghĩa vụ pháp lý không rút lại được. Rẻ để làm trước, không sửa được sau."*
- ⚠️ **Nghịch lý safe harbour** ([BRD-007 §5.2](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md#52-không-xây-bộ-phát-hiện-bản-quyền-chủ-động--đây-là-anti-feature), [Risk-Register R-04](../../010-Planning/Risk-Register.md)): điều kiện miễn trừ (a) của Điều 198b là *"không biết"* nội dung đó xâm phạm quyền. Xây bộ phát hiện bản quyền chủ động **PHÁ chính miễn trừ này**.
- ⚠️ **Khoảng trống chưa trả lời** ([BRD-007 §5.1 Q3](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md#51-brd-này-không-trả-lời-ba-câu-hỏi-luật-sư)): nền tảng có được coi là *"doanh nghiệp cung cấp dịch vụ trung gian"* khi nó **xử lý/biến đổi** nội dung (không chỉ hosting) hay không — `TBD`, là câu Q3 của gate G0, **không** được Story này tự trả lời.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Tồn tại **công cụ tiếp nhận takedown** hoạt động được — form và/hoặc email `copyright@` — đo bằng: gửi một yêu cầu takedown test qua kênh đó, xác nhận yêu cầu được ghi nhận (có ID/timestamp).
- [ ] **Đầu mối liên hệ (email + số điện thoại) đã đăng ký với Bộ Văn hoá, Thể thao và Du lịch** — đo bằng: tồn tại bằng chứng đăng ký (xác nhận từ Bộ, hoặc hồ sơ đăng ký đã gửi có timestamp).
- [ ] Yêu cầu takedown hợp lệ được xử lý trong **SLA 72 giờ** bằng **soft-delete + disable-access ở cấp project**, **KHÔNG hard delete** — đo bằng: từ timestamp nhận yêu cầu tới timestamp nội dung bị disable-access, chênh lệch ≤ 72 giờ, và dữ liệu vẫn tồn tại ở trạng thái ẩn (không bị xoá cứng) để phục vụ counter-notice.
- [ ] Checkbox **user warrant + indemnify** hiện diện tại bước upload (tái sử dụng cơ chế của `Story-ToS-User-Warrant-And-Tenant-Hard-Delete`) — đo bằng kiểm tra UI/API upload.
- [ ] Bước **kiểm opt-out Điều 37b** chạy trước khi nội dung được xử lý (tái sử dụng cơ chế của `Story-Opt-Out-Check-At-Ingest`) — đo bằng đối chiếu log kiểm opt-out tồn tại cho mọi nội dung đã qua takedown flow.
- [ ] Checklist 6/6 mục có thể được liệt kê và đánh dấu hoàn thành trước khi tính năng "mở cho người ngoài upload" được bật — đo bằng: tồn tại một tài liệu/config checklist với 6 dòng, mỗi dòng có trạng thái hoàn thành xác định được.

### Đường không hạnh phúc (unhappy path)

- [ ] Yêu cầu takedown **không hợp lệ** (thiếu thông tin xác định chủ sở hữu quyền, hoặc không mô tả được nội dung vi phạm) phải có đường phản hồi từ chối rõ ràng, không được âm thầm bỏ qua và không được tự động thực hiện disable-access.
- [ ] Yêu cầu takedown **quá 72 giờ chưa xử lý** phải được phát hiện được (có cơ chế cảnh báo/đếm ngược), không được để trôi qua mà không ai biết — vì SLA vi phạm làm mất điều kiện miễn trừ.
- [ ] Sau khi disable-access, nếu tenant bị ảnh hưởng gửi **counter-notice**, phải có đường tiếp nhận counter-notice — nội dung **không** được hard-delete trong lúc chờ xử lý counter-notice.
- [ ] Nhiều yêu cầu takedown trùng lặp cho cùng một nội dung (từ nhiều chủ thể khác nhau, hoặc gửi lại nhiều lần) không được tạo ra nhiều lần disable-access chồng chéo gây nhầm lẫn trạng thái.

### Ràng buộc cứng không được vi phạm

- `C1` — đội 1 người + AI assist, không funding ([Charter §7](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints)): checklist phải **chia được cho một người** — đây là lý do chọn *form + email `copyright@`* thay vì một hệ thống ticket phức tạp (Analysis §8.3 item 1, [BRD-007 §4.2](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md#42-c-x--ràng-buộc-charter-7-mà-module-này-chịu)).

> `GP-3` không có mã `KC-x` riêng trong bảy mục [MVP-Scope §6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng). Điều kiện chặn thực tế là `BLOCKER-02` ([Charter §9.3](../../010-Planning/Charter-Comic-Studio.md#93-ba-điều-kiện-chặn-phụ)) — ghi ra để tường minh dù không khớp enum `KC-x`/`C-x`/`AG-x`.

### Story này KHÔNG làm

- [ ] **KHÔNG** xây bộ phát hiện bản quyền chủ động dưới bất kỳ tên nào (`copyright detection`, `plagiarism check`, `flag nội dung khả nghi`, `similarity scan`) — đây là **anti-feature** có thể phá chính miễn trừ Điều 198b, cấm tường minh cho tới khi có xác nhận của luật sư ([Risk-Register R-04](../../010-Planning/Risk-Register.md)).
- [ ] **KHÔNG** tự khẳng định nền tảng được hưởng miễn trừ Điều 198b — đó là câu hỏi Q3 của gate G0, `TBD`, thuộc thẩm quyền luật sư.
- [ ] **KHÔNG** hard-delete nội dung khi xử lý takedown — chỉ soft-delete + disable-access; đường hard-delete tenant là cơ chế **tách biệt**, thuộc `Story-ToS-User-Warrant-And-Tenant-Hard-Delete`.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | `TBD` | Không có ước lượng bottom-up trong repo. **Điều kiện escalate**: nếu ước lượng thực tế lúc nhặt Story lên vượt **16 giờ-người**, split Story (ví dụ tách "đăng ký đầu mối Bộ VHTTDL" — một hoạt động hành chính — khỏi "công cụ takedown + SLA" — một cấu phần kỹ thuật) hoặc ghi lý do vượt trần thành văn. |
| `E_hitl` | `0` giờ-người/chapter | Nghĩa vụ SLA 72 giờ phát sinh **theo từng yêu cầu takedown** (tần suất không xác định trước, phụ thuộc bên ngoài), **không** theo chu kỳ chapter — nên không quy đổi được thành giờ-người/chapter mà không bịa số. Đây là một nghĩa vụ vận hành lặp lại theo sự kiện, cần theo dõi riêng ngoài khung `E_hitl`, không phải một chi phí bằng 0 tuyệt đối. |

## 6. INVEST

| Tiêu chuẩn | Đánh giá |
|---|---|
| Independent | ✅ Không nằm trong danh sách vỡ Independent của §4.10. §4.7 chấm `I = ✅`. |
| Negotiable | Negotiable ở cách triển khai công cụ (form/email), nhưng **không negotiable** ở việc phải đủ 6/6 mục checklist trước trigger "mở cho người ngoài upload" (`BLOCKER-02`). |
| Valuable | `Valuable-I` — xem mục 3: một lần upload của người ngoài mà chưa có đường takedown tạo nghĩa vụ pháp lý không rút lại được. |
| Estimable | Estimable bằng giờ-người, hiện `TBD` — xem mục 5. |
| Small | ⚠️ [Security suy luận] — §4.7 chấm `S = ⚠️` nhưng không có dòng nào trong §4.10 giải thích lý do. Suy luận: Story này gộp một hoạt động **kỹ thuật** (form/email, soft-delete, SLA timer) với một hoạt động **hành chính bên ngoài hệ thống** (đăng ký đầu mối với Bộ VHTTDL) và một **ràng buộc thiết kế** (checkbox user warrant + kiểm opt-out tái dùng từ hai Story khác) — ba loại công việc khác bản chất trong cùng một Story làm kích thước khó giữ nhỏ và khó đo bằng giờ-người thuần kỹ thuật. |
| Testable | Testable bằng checklist assertion nhị phân — xem mục 4 AC-1/AC-2. |

> **Kết luận mục 6**: `I = ✅` theo §4.7. `S = ⚠️` theo §4.7 nhưng không có dòng §4.10 tương ứng ⇒ lý do trên mang nhãn `[Security suy luận]`.
