---
id: STORY-G-04
type: story
status: draft
created: 2026-08-24
---

# Story-ToS-User-Warrant-And-Tenant-Hard-Delete

## 1. Story

> Là khách hàng SaaS, tôi muốn **có đường xoá cứng toàn bộ dữ liệu tenant của tôi đã được kiểm thử**, để **quyền rút khỏi hệ thống là quyền thực thi được, không phải lời hứa**.

## 2. Part of

| Quan hệ | Tài liệu |
|---|---|
| **Epic cha** | [Epic-Legal-And-Compliance](../Epics/Epic-Legal-And-Compliance.md) — hàng 4/6 mục 3 |
| **BRD cha** | [BRD-007-Legal-And-Compliance](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md) — `BR-007-07`, `BR-007-08`, `BR-007-09`, `GP-5` §2 |
| **Use Case liên quan** | [UC-01 — Upload And Ingest Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) — nơi gắn checkbox **user warrant** ở bước upload (`BR-007-07`) |

## 3. Bối cảnh & nguồn

- **Hạng mục MVP-Scope**: [MVP-Scope §3 GP-5](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope) — `❌` ở MVP0 → `✅` ở MVP1: *"ToS + user warrant + `ON DELETE CASCADE` + đường hard-delete tenant đã kiểm thử"*.
- **Exit criterion Roadmap**: ⚠️ **[Security suy luận]** — không có exit criterion `M1-x`/`M2-x` nào của [Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) nêu tên hard-delete tenant tường minh (đã grep, không có kết quả). Anchor gần nhất được suy luận: **M1-1** — *"`tenant_id NOT NULL` trên 100% bảng nghiệp vụ; RLS policy bật trên 100% bảng có `tenant_id`; test rò rỉ chéo tenant PASS"*. Lý do dùng suy luận này: cả hai đều xác minh **cùng một ranh giới tenant** — M1-1 xác minh ranh giới đó qua **đọc** (query không rò dữ liệu), Story này xác minh qua **xoá** (xoá một tenant không để sót dữ liệu ở tenant khác/của chính nó). ⛔ Đây **không phải** một exit criterion đã được Roadmap đặt tên cho hard-delete — ghi rõ để không ai đọc nhầm thành đã có nguồn trực tiếp.
- **Căn cứ nghiệp vụ trực tiếp hơn**: [MVP-Scope §8.2](../../010-Planning/MVP-Scope.md#82-nghĩa-vụ-khi-kill--dừng-có-trật-tự) — *"Đây là lý do E3 và GP-5 (`ON DELETE CASCADE` + đường hard-delete đã kiểm thử) phải có từ MVP1: đường thoát phải được xây cùng lúc với đường vào"*. Khi KILL (K3/K4/K5), phải xuất **cả `change_log` + `field_provenance`** cho từng tenant vì đó là hồ sơ chứng minh quyền tác giả **của khách**.
- **`Valuable-I`**: Analysis §5.7 #5, nguyên văn trích tại [BRD-007 BR-007-08](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md#3-yêu-cầu-nghiệp-vụ): *"FK lỏng thì xoá một tenant biến thành khảo cổ học thủ công, và sót dữ liệu là rủi ro pháp lý"*. Không xây và kiểm thử đường hard-delete từ MVP1 nghĩa là khi cần xoá thật (takedown, yêu cầu người dùng, hoặc KILL), không có cách nào xác minh đã xoá hết — hậu quả tương tự cấp độ với `KC-5` dù không nằm trong bảy `KC-x`.
- **Phân biệt bắt buộc**: đường hard-delete tenant (`BR-007-08`) **tách biệt** với đường soft-delete/disable-access dùng cho takedown Điều 198b (`BR-007-04`, thuộc `Story-Safe-Harbour-Checklist-Article-198b`) — hai cơ chế phục vụ hai mục đích khác nhau, không được gộp.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Mọi bảng nghiệp vụ có FK trỏ về `tenant` sử dụng `ON DELETE CASCADE` — đo bằng: đọc schema migration, đếm số FK tới `tenant.id` và xác nhận 100% dùng `ON DELETE CASCADE`.
- [ ] Có một thao tác vận hành (script/lệnh/API nội bộ) xoá cứng toàn bộ dữ liệu của một `tenant_id` cụ thể — đo bằng: chạy thao tác đó trên một tenant test, sau đó query **mọi** bảng nghiệp vụ với `tenant_id` đó, kỳ vọng **0 dòng** ở tất cả các bảng.
- [ ] Đường hard-delete này đã được **kiểm thử tự động** (test suite), không chỉ chạy tay một lần — đo bằng: tồn tại một test case cụ thể chạy hard-delete và assert 0 dòng còn lại.
- [ ] Trước khi hard-delete, tồn tại đường **xuất dữ liệu đầy đủ** cho tenant đó — bao gồm Story Bible, Comic IR, mọi ảnh, **và cả `change_log` + `field_provenance`** — đo bằng: chạy export cho một tenant test, xác nhận file export chứa đủ 5 loại dữ liệu trên.
- [ ] Có checkbox **user warrant + indemnify** gắn vào bước upload (không chỉ nằm ở trang ToS) — đo bằng: kiểm tra UI/API upload yêu cầu xác nhận checkbox này trước khi chấp nhận file.

### Đường không hạnh phúc (unhappy path)

- [ ] Hard-delete một tenant **không** được xoá nhầm dữ liệu của tenant khác — đo bằng test: tạo 2 tenant, hard-delete tenant A, xác nhận **100%** dữ liệu tenant B còn nguyên vẹn.
- [ ] Nếu hard-delete bị gián đoạn giữa chừng (crash, timeout), tenant đó phải ở một trong hai trạng thái xác định được (chưa xoá / đã xoá hoàn toàn) — **không** được để lại trạng thái xoá dở dang mà không có cách phát hiện.
- [ ] Yêu cầu hard-delete một tenant **đang có dữ liệu được tenant khác tham chiếu gián tiếp** (nếu có cơ chế chia sẻ nào trong tương lai) phải được từ chối hoặc cảnh báo rõ ràng, không được âm thầm xoá và phá vỡ tham chiếu của tenant khác.
- [ ] Checkbox user warrant bị bỏ qua (do lỗi client, request trực tiếp vào API) phải bị **API tầng server chặn**, không được tin tưởng riêng validation phía client.

### Ràng buộc cứng không được vi phạm

—

> `GP-5` không có mã `KC-x` tương ứng trong bảy mục [MVP-Scope §6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) (chỉ `KC-1`, `KC-2`, `KC-3`, `KC-4`, `KC-6` thuộc BRD-007; `KC-5`, `KC-7` thuộc BRD khác). Ràng buộc thực tế của Story này là nghĩa vụ **`GP-5`** ([MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope)) và nghĩa vụ khi KILL ([MVP-Scope §8.2](../../010-Planning/MVP-Scope.md#82-nghĩa-vụ-khi-kill--dừng-có-trật-tự)), không phải một `KC-x`/`C-x`/`AG-x` trong enum chuẩn.

### Story này KHÔNG làm

- [ ] **KHÔNG** phải đường soft-delete/disable-access dùng cho xử lý takedown Điều 198b — đó là `BR-007-04`, thuộc `Story-Safe-Harbour-Checklist-Article-198b`. Hai đường xoá **tách biệt**, không được gộp.
- [ ] **KHÔNG** thực hiện thông báo trước ≥30 ngày hay ngừng thu tiền khi KILL — đó là quy trình vận hành ở [MVP-Scope §8.2](../../010-Planning/MVP-Scope.md#82-nghĩa-vụ-khi-kill--dừng-có-trật-tự), Story này chỉ cung cấp **cơ chế** xuất dữ liệu + xoá cứng đã kiểm thử.
- [ ] **KHÔNG** đăng ký DMCA designated agent với US Copyright Office — đó là điều kiện **chỉ khi** nhắm thị trường Mỹ ([BRD-007 BR-007-07](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md#3-yêu-cầu-nghiệp-vụ)), `TBD` cho tới khi có quyết định thị trường.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | `TBD` | Không có ước lượng bottom-up trong repo. **Điều kiện escalate**: nếu ước lượng thực tế lúc nhặt Story lên vượt **16 giờ-người**, split Story (ví dụ tách phần "checkbox + ToS text" khỏi phần "hard-delete + export kiểm thử") hoặc ghi lý do vượt trần thành văn — Story này không nằm trong danh sách vỡ Independent của §4.10 nên split là lựa chọn hợp lệ cho phần `I = ✅`. |
| `E_hitl` | `0` giờ-người/chapter | Hard-delete là thao tác vận hành theo **sự kiện tenant** (rời đi, KILL), không theo chu kỳ chapter. Không tạo nghĩa vụ giờ-người lặp lại mỗi chapter. |

## 6. INVEST

| Tiêu chuẩn | Đánh giá |
|---|---|
| Independent | ✅ Không nằm trong danh sách vỡ Independent của §4.10. §4.7 chấm `I = ✅`. |
| Negotiable | Negotiable trong phạm vi triển khai (cách viết ToS, UI checkbox), nhưng **không negotiable** ở việc phải tồn tại đường hard-delete đã kiểm thử (`GP-5` là nghĩa vụ bắt buộc, dù không mang mã `KC-x`). |
| Valuable | `Valuable-I` — xem mục 3: không có đường thoát kiểm thử được ⇒ quyền rút khỏi hệ thống chỉ là lời hứa, không phải quyền thực thi được. |
| Estimable | Estimable bằng giờ-người, hiện `TBD` — xem mục 5. |
| Small | ⚠️ [Security suy luận] — §4.7 chấm `S = ⚠️` nhưng không có dòng nào trong §4.10 giải thích lý do. Suy luận: Story này gộp **ba yêu cầu nghiệp vụ khác nhau** (`BR-007-07` ToS/checkbox, `BR-007-08` hard-delete kiểm thử, `BR-007-09` export khi KILL) dưới một tên Story — kích thước thực tế phụ thuộc vào **số bảng có FK tới `tenant`** tại thời điểm build (tương tự lý do `Story-Tenant-Id-And-RLS-Everywhere` vỡ `I`/`S` ở BRD khác: kiểm thử "đã xoá hết" đòi phủ hết mọi bảng nghiệp vụ hiện có, và có thể phình khi thêm bảng mới). |
| Testable | Testable bằng checklist assertion nhị phân — xem mục 4 AC-1/AC-2. |

> **Kết luận mục 6**: `I = ✅` theo §4.7, không có mâu thuẫn. `S = ⚠️` theo §4.7 nhưng không có dòng §4.10 tương ứng ⇒ lý do trên mang nhãn `[Security suy luận]`, không phải trích dẫn có sẵn.
