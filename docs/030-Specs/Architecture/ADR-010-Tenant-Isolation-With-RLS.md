---
id: ADR-010
type: adr
status: draft
project: comic-studio
created: 2026-08-29
updated: 2026-08-30
---

# ADR-010: Cô lập tenant bằng `tenant_id` toàn cục + Postgres RLS

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

## Context

> [!IMPORTANT]
> ⛔ **Đây là ADR `record-only`.** Mọi quyết định ở mục `Decision` **đã CHỐT ở Phase 1**. ADR này **đóng băng** chúng để một run sau không mở lại, ⛔ **không** quyết thêm điều gì mới.
>
> ⚠️ **Cơ chế bơm tenant context đã được [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) chốt** (`SET LOCAL app.current_tenant`, DB role `app_worker`, khoảng hở đúng **một statement** khi worker claim job). ⛔ **ADR-010 KHÔNG đặc tả lại cơ chế đó** — nó chỉ ghi nhận *ràng buộc phải được cơ chế nào đó thoả*.

### Vì sao ràng buộc này là loại nghiêm trọng nhất

Sản phẩm là SaaS multi-tenant thương mại — nền tảng cho **người khác tự upload bản thảo chưa công bố của họ** (`CF-1.1` `[CHỐT]`). Rò rỉ chéo tenant ở đây không phải một bug, nó là **mất sản phẩm**.

Ba dữ kiện bối cảnh làm hình dạng của quyết định:

| Dữ kiện | Hệ quả kiến trúc |
|---|---|
| Đội **1 người**, `bus factor = 1`, **không có code review** (`CF-1.2`) | Không có bước nào chặn một câu query quên `WHERE tenant_id` trước khi nó lên production ⇒ phòng thủ phải ở **tầng DB**, không phải tầng kỷ luật |
| `tenant_id` retrofit vào schema **đã có dữ liệu thật** | *"Một trong những migration đắt nhất tồn tại"* — và `KC-5` ghi thẳng *"không có cách nào xác minh đã sửa hết"* ([MVP-Scope](../../010-Planning/MVP-Scope.md) §6) |
| RLS có **một giới hạn đã biết** | Nguyên văn: *"RLS **không** bảo vệ được join thực hiện phía application — đó là lý do tách 2 database làm mất lớp phòng thủ này"* ([Glossary](../../999-Resources/Glossary.md) mục `RLS`) ⇒ đây chính là lý do [ADR-009](./ADR-009-Modular-Monolith-Three-Schemas.md) giữ **một** database |

### ⭐ Cảnh báo phải đọc trước khi lập kế hoạch triển khai

> [!CAUTION]
> **`tenant_id` trên 8/10 bảng = VẪN RÒ RỈ.**
>
> Nguyên văn từ [Story-Tenant-Id-And-RLS-Everywhere](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) §6 INVEST:
>
> > *"Chạm **100% bảng nghiệp vụ** + 100% composite index + 100% query. Không có sub-slice nào 'xong' mà có nghĩa: `tenant_id` trên 8/10 bảng = **vẫn rò rỉ**. `MVP-Scope` KC-5: 'không có cách nào xác minh đã sửa hết' ⇒ **DoD phải là test rò rỉ chéo tenant PASS (`M1-1`), không phải số bảng đã sửa**."*
>
> ⇒ Đây là một **thuộc tính TOÀN CỤC của hệ thống**, không phải một tính năng đo được bằng phần trăm. ⛔ **Đếm bảng là một chỉ số có thể tăng đều trong khi kết quả cuối vẫn là thất bại** ([Story](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) §6 INVEST).

## Decision

### D1. `tenant_id NOT NULL` trên **MỌI** bảng nghiệp vụ

Cả 3 schema `story` / `comic` / `generation`, và nhóm bảng platform mà [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) đã đặt vào `public`.
Xác minh: script liệt kê toàn bộ bảng nghiệp vụ, **0 bảng thiếu** ràng buộc `NOT NULL` trên `tenant_id` ([Story](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) §4 AC *"Xác minh được"*).

### D2. `tenant_id` là **cột ĐẦU TIÊN** của **MỌI** composite index

⛔ Không phải *"có mặt trong index"* — **phải là cột đầu**. Xác minh bằng catalog Postgres (`pg_index` + `pg_attribute`): **0 index** có `tenant_id` không đứng đầu ([Story](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) §4 AC *"Xác minh được"*).

### D3. Postgres RLS là **lớp phòng thủ thứ hai**, bật trên 100% bảng có `tenant_id`

Điều kiện: `ROW LEVEL SECURITY` bật **và** có **≥1** `CREATE POLICY`. Đo bằng: số bảng xuất hiện trong `pg_policies` phải **bằng đúng** số bảng có cột `tenant_id` ([Story](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) §4 AC *"Xác minh được"*).

### D4. Mô hình **shared database + shared schema**

⛔ **KHÔNG** schema-per-tenant · ⛔ **KHÔNG** database-per-tenant (`SRS-NFR-01` · [Story](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) §4 *"Story này KHÔNG làm"*).

### D5. ⛔ **CẤM** viết tenant isolation thành *"filter `tenant_id` ở tầng ứng dụng"*

Nguyên văn ràng buộc ([SRS §3.E khối `[!WARNING]`](../../020-Requirements/SRS-Comic-Studio.md)):

> *"App-layer filter **sẽ có lúc bị lọt** — một query quên `WHERE tenant_id`. Với 1 dev không có code review, **RLS biến lỗi lập trình thành no-op thay vì rò rỉ dữ liệu chéo tenant**."*

⭐ Phát biểu đúng về giá trị của RLS: nó **không** làm code đúng hơn — nó **đổi hậu quả của code sai** từ *"lộ dữ liệu khách"* thành *"trả 0 row"*.

### D6. `tenant` / `user` / `membership` là **BA entity riêng** ngay từ đầu

- Kể cả khi quan hệ hiện tại là **1:1** (`SRS-FR-01` · `MVP-Scope §3 E2`).
- Mọi dữ liệu nghiệp vụ trỏ **`tenant_id`**, ⛔ **không** trỏ `user_id`.
- Vị trí schema vật lý của ba bảng này: [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) — ⛔ không quyết lại ở đây. Vendor auth sở hữu định danh: [ADR-003](./ADR-003-Auth-And-Billing-Vendor-Selection.md).

### D7. **HAI đường xoá TÁCH BIỆT** — ⛔ không được gộp

| | **Hard-delete tenant** | **Takedown** |
|---|---|---|
| Mã nghiệp vụ | `BR-007-08` ([BRD-007](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md)) · `SRS-NFR-05` · `MVP-Scope §3 GP-5` | `BR-007-04` ([BRD-007](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md)) · `MVP-Scope §3 GP-3` |
| Ngữ nghĩa | **Xoá cứng** toàn bộ dữ liệu tenant, kỷ luật `ON DELETE CASCADE` trên mọi FK | **Soft-delete + disable-access ở cấp PROJECT** |
| Bắt buộc | Đường xoá phải **tồn tại VÀ đã được kiểm thử** | ⛔ **KHÔNG hard delete** |
| Vì sao không gộp | Quyền rút khỏi hệ thống của khách | Xoá cứng **phá mất chính bằng chứng** mà counter-notice cần; provenance ⛔ **không backfill được** ([UC-11](../../020-Requirements/Use-Cases/UC-11-Handle-Takedown-Request.md) khối `[!CAUTION]` *"Gộp hai thứ này là một lỗi"*) |

### D8. ⭐ Definition of Done là một **test nhị phân toàn cục**

**DoD = test rò rỉ chéo tenant PASS (`M1-1`)**: seed 2 tenant A/B; **mọi** câu query chạy dưới session của tenant A trả về **0 row** thuộc tenant B ([Story](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) §4 AC *"Xác minh được"* · §6 INVEST).

⛔ **KHÔNG** phải *"đã thêm `tenant_id` cho N/M bảng"*.

### D9. Ba hành vi biên bắt buộc (đã ghi ở Story, giữ nguyên ở đây)

| # | Hành vi | Nguồn |
|:--:|---|---|
| 1 | Insert row nghiệp vụ thiếu `tenant_id` bị **DB từ chối ở tầng constraint**, ⛔ không lọt qua bằng validation tầng ứng dụng | [Story](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) §4 AC *"Đường không hạnh phúc"* |
| 2 | Session **không set** (hoặc set sai) tenant context bị RLS chặn trả **0 row** — **fail-closed**, ⛔ không phải lỗi 500 không kiểm soát | [Story](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) §4 AC *"Đường không hạnh phúc"* |
| 3 | Hai request của hai tenant **tái sử dụng cùng một connection trong pool** ⛔ không được rò context sang nhau | [Story](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) §4 AC *"Đường không hạnh phúc"* |

⇒ **Cách thoả ba hành vi này là nội dung của [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md)** (`SET LOCAL` phạm vi transaction, helper đọc context, đường API vs đường worker, carve-out `public.job` cho role `app_worker`). ⛔ ADR-010 không lặp lại.

### D10. Giới hạn đã biết, ghi tường minh

⚠️ **RLS ⛔ không bảo vệ được join thực hiện phía application.** Đây **không** phải một khiếm khuyết cần vá ở ADR này — nó là **căn cứ** của [ADR-009](./ADR-009-Modular-Monolith-Three-Schemas.md): giữ **một** database để mọi join nằm **trong** phạm vi RLS.

## Alternatives considered

> ⭐ Phần giá trị nhất của ADR record-only. Lý do bác được trích từ nguồn Phase 1; chỗ nào là suy luận, em dán nhãn `[Kiến trúc suy luận]`.

### (a) Chỉ filter `tenant_id` ở **tầng ứng dụng**, ⛔ không bật RLS — BỊ LOẠI

Đây là phương án **rẻ nhất trong ngắn hạn** và vì vậy là phương án **dễ bị mở lại nhất**. Lý do bác có nguyên văn ([SRS §3.E](../../020-Requirements/SRS-Comic-Studio.md) · `Analysis §5.7 #1`):

1. App-layer filter **sẽ có lúc bị lọt** — chỉ cần **một** query quên `WHERE tenant_id`.
2. Bối cảnh làm điều đó thành **chắc chắn xảy ra**, không phải *"có thể"*: **1 dev, không có code review** ⇒ không tồn tại bước nào phát hiện query thiếu điều kiện.
3. Với RLS, cùng một lỗi lập trình đó cho ra **no-op (0 row)** thay vì **rò rỉ chéo tenant**.
4. `C1` ([Charter §7](../../010-Planning/Charter-Comic-Studio.md)): RLS là **lớp phòng thủ bắt buộc, không phải tuỳ chọn** ([Story](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) §4 *"Ràng buộc cứng không được vi phạm"*).

⇒ Xem thêm phương án `(F)` của [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md), nơi cùng phương án này bị bác lần thứ hai ở tầng cơ chế.

### (b) **Schema-per-tenant** — BỊ LOẠI

`SRS-NFR-01` loại tường minh: mô hình là **shared DB + shared schema**, *"**không** schema-per-tenant"*.

`[Kiến trúc suy luận]` — nguồn Phase 1 ghi **kết quả**, không ghi nguyên văn lý do bác từng biến thể. Ràng buộc trong hồ sơ khiến phương án này không tương thích: mỗi migration phải chạy **N lần** (một lần mỗi tenant) và mỗi lần là một cơ hội lệch schema — với `bus factor = 1` (`CF-1.2`) đó là chi phí vận hành thường trực. Đồng thời nhóm bảng cross-cutting ở `public` ([ADR-005](./ADR-005-Platform-Table-Schema-Placement.md)) vẫn phải xuyên tenant, nên phương án này **không loại bỏ** nhu cầu `tenant_id` + RLS mà chỉ **cộng thêm** một chiều phức tạp.

### (c) **Database-per-tenant** — BỊ LOẠI

Cùng hàng nguồn với (b). ⭐ Ngoài ra nó va thẳng vào ràng buộc số một của [ADR-009](./ADR-009-Modular-Monolith-Three-Schemas.md): nhiều database ⇒ **mất một transaction boundary duy nhất** cho `KC-4` ([MVP-Scope](../../010-Planning/MVP-Scope.md) §6 `KC-4` · `SRS-NFR-13`). Tức phương án này bị **hai** ràng buộc độc lập loại, không phải một.

### (d) Thêm `tenant_id` **sau**, khi đã có khách thật — BỊ LOẠI

- `KC-5` ([MVP-Scope](../../010-Planning/MVP-Scope.md) §6): retrofit vào schema đã có dữ liệu thật là *"một trong những migration đắt nhất tồn tại"*, và **"không có cách nào xác minh đã sửa hết"**.
- [Glossary](../../999-Resources/Glossary.md) mục `tenant_id`, nguyên văn: *"Phải là **cột đầu tiên** của mọi composite index, `NOT NULL`, **có từ ngày đầu**. Thêm sau là một cuộc migration xuyên toàn bộ schema."*
- ⇒ `E1` = `✅` từ **MVP1 — ngày đầu** ([MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `E1`).

### (e) `tenant_id` có mặt trong composite index nhưng **không phải cột đầu** — BỊ LOẠI

`SRS-NFR-01` và [Glossary](../../999-Resources/Glossary.md) đều phát biểu ràng buộc ở dạng **vị trí**, không phải dạng **hiện diện**. `[Kiến trúc suy luận]` — trong mô hình shared-schema, `tenant_id` là điều kiện có tính chọn lọc cao nhất và xuất hiện ở **mọi** truy vấn; đặt nó ở vị trí khác cột đầu làm index mất tác dụng cho chính hình dạng query phổ biến nhất của hệ thống.

### (f) Gộp `user` và `tenant` thành **một** entity (vì hiện tại 1:1) — BỊ LOẠI

`SRS-FR-01` loại tường minh: ba entity riêng *"**kể cả khi** quan hệ là 1:1"*. `[Kiến trúc suy luận]` — điều làm phương án gộp trở nên nguy hiểm không phải hôm nay mà là hệ quả của nó: mọi FK nghiệp vụ sẽ trỏ `user_id`, và ngày đầu tiên một tenant có người thứ hai thì **toàn bộ** FK đó phải migrate. Đây cùng loại chi phí với (d), khác chỗ nó tới sớm hơn.

### (g) Một đường xoá **dùng chung** cho takedown và hard-delete tenant — BỊ LOẠI

[UC-11](../../020-Requirements/Use-Cases/UC-11-Handle-Takedown-Request.md) khối `[!CAUTION]` *"Gộp hai thứ này là một lỗi"* ghi thẳng: `BR-007-04` phát biểu takedown là *"**KHÔNG** hard delete"*. Thực hiện takedown bằng xoá cứng **phá mất chính bằng chứng** mà counter-notice cần, và dữ liệu provenance thì **không backfill được** (`CF-7.3`). Hai cơ chế phục vụ hai mục đích trái chiều ⇒ ⛔ không được gộp ([Story-ToS-User-Warrant-And-Tenant-Hard-Delete](../../022-User-Stories/Backlog/Story-ToS-User-Warrant-And-Tenant-Hard-Delete.md) §3 Bối cảnh & nguồn · §4 *"Story này KHÔNG làm"*).

### (h) Cấp `BYPASSRLS` cho role ứng dụng / worker — ⛔ ĐÃ BỊ [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) BÁC

Ghi ở đây **chỉ để chặn việc mở lại**, ⛔ không lặp lại lập luận: `BYPASSRLS` xoá RLS trên **mọi** bảng, ở đúng process phục vụ nhiều tenant nhất. Xem phương án `(E)` của [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md).

## Consequences

### Tích cực

- ⭐ Lỗi lập trình phổ biến nhất (quên `WHERE tenant_id`) có hậu quả **0 row**, ⛔ không phải lộ dữ liệu khách. Đây là điều duy nhất làm cho mô hình *"1 dev, không code review"* còn chấp nhận được về mặt rủi ro.
- Tiêu chí *"xong"* là **một test chạy được** (`M1-1`), ⛔ không phải một bản tự đánh giá — kiểm chứng được bởi người ngoài.
- `tenant_id` là cột đầu mọi composite index ⇒ hình dạng query phổ biến nhất được index phục vụ đúng ngay từ migration đầu.
- Ba entity `tenant`/`user`/`membership` tách sẵn ⇒ mở team nhiều thành viên về sau **không** đụng tới FK nghiệp vụ (`E8` hoãn SSO/team-role vẫn nằm ngoài horizon, [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `E8`).
- Hai đường xoá tách biệt ⇒ nghĩa vụ **giữ bằng chứng** (takedown) và **quyền rút dữ liệu** (hard-delete) không triệt tiêu nhau.

### Tiêu cực — chi phí thật

- ⭐ **Story vỡ `I` và `S` ở mức nặng nhất của cả backlog.** `E_build ≈ 24h` `[EM]` — **vượt trần 16h** và ⛔ **không được split**: *"split một Story mà DoD là một test nhị phân toàn cục chỉ tạo ra ảo giác tiến độ"* ([Story](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) §5 Ước lượng · §6 INVEST).
- **Mọi bảng mới sinh ra ba nghĩa vụ mới**: cột `tenant_id NOT NULL`, thứ tự cột index, và một RLS policy. Không có bảng nào được miễn ⇒ chi phí biên của mỗi feature tăng vĩnh viễn.
- **Multi-tenancy ăn 15–25% effort** `[EM]` (`CF-6.9`) — và `R-16` ([BRD-005](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md)) ghi rằng nó *"không có trong `Request.md` một dòng nào"*, tức đây là chi phí **không nằm trong kỳ vọng ban đầu**.
- **RLS ⛔ không bảo vệ join phía application** ⇒ ràng buộc *"một database"* của [ADR-009](./ADR-009-Modular-Monolith-Three-Schemas.md) trở thành **bắt buộc vĩnh viễn**, không phải một lựa chọn có thể đảo lại khi quy mô đổi.
- **Bề mặt không có tenant vẫn tồn tại**: công cụ tiếp nhận takedown là **công khai, không cần tài khoản** (`BR-007-04`) ⇒ có ít nhất một đường vào hệ thống không mang tenant context. Cách xử lý thuộc `D6` của [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md).

### Việc còn để `TBD` — ⛔ không được bịa

| Khoảng trống | Ai đóng | Khi nào |
|---|---|---|
| Danh sách đầy đủ **bảng nghiệp vụ** để test `M1-1` phủ hết (DoD là toàn cục ⇒ danh sách phải đóng) | Lô `docs/030-Specs/Schema/DB-Entity-*.md` (architect) + [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) cho nhóm P | Trước khi viết test `M1-1` — tức trước **migration số 1** |
| **Thông báo cho tenant bị takedown** — `TBD` trong nguồn | PM / `security-auditor`; xem [findings/architect §7 G10](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) — *"Thông báo cho tenant bị takedown là `TBD`"* | Trước khi `Story-Safe-Harbour-Checklist-Article-198b` vào Active Sprint (SLA **72 giờ** phải có người nhận) |
| **Vendor auth** sở hữu định danh `user` (`SRS-NFR-08`) | [ADR-003](./ADR-003-Auth-And-Billing-Vendor-Selection.md) | `ADR-003` nay `accepted`, nhưng Clerk mới ở mức **MẶC ĐỊNH, ⛔ chưa mua** ⇒ điều kiện còn lại là **spike verify ba tiêu chí nghiệm thu** của `ADR-003` — kickoff MVP1 (`E4` = `✅ auth` từ MVP1) |

## Đã quyết ở đâu

> Bảng truy vết. Mọi nguồn được đọc trực tiếp tại thời điểm viết, ⛔ không sao chép từ tài liệu trung gian. ⭐ Neo bằng **mã requirement / tên mục**, ⛔ **không dùng số dòng** — số dòng mục ngay khi file nguồn đổi một ký tự.

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|:--:|---|
| `tenant_id NOT NULL` trên **MỌI** bảng nghiệp vụ · **cột ĐẦU TIÊN** của mọi composite index · **Postgres RLS** là lớp phòng thủ thứ hai · **shared DB + shared schema** (⛔ không schema-per-tenant, ⛔ không db-per-tenant) | `D-09` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E `SRS-NFR-01` · [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `E1`, §6 `KC-5` · [BRD-005](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md) `BR-005-01` |
| ⛔ **CẤM** tenant isolation bằng filter tầng ứng dụng; RLS biến lỗi lập trình thành **no-op thay vì rò rỉ**; ⚠️ RLS ⛔ không bảo vệ join phía application | `D-10` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E khối `[!WARNING]` · [Glossary](../../999-Resources/Glossary.md) mục `RLS` · `C1` [Charter §7](../../010-Planning/Charter-Comic-Studio.md) |
| `tenant` / `user` / `membership` là **BA entity riêng** ngay từ đầu, kể cả khi 1:1; dữ liệu nghiệp vụ trỏ `tenant_id`, ⛔ không trỏ `user_id` | `D-11` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E `SRS-FR-01` · [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `E2` |
| Kỷ luật `ON DELETE CASCADE` + **một đường hard-delete tenant đã kiểm thử**, **TÁCH BIỆT** khỏi soft-delete của takedown | `D-14` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E `SRS-NFR-05` · [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `GP-5` · [BRD-007](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md) `BR-007-08` |
| Takedown = **soft-delete + disable-access cấp project**, ⛔ **KHÔNG hard delete** (giữ bằng chứng cho counter-notice) | `D-54` | [BRD-007](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md) `BR-007-04` · [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `GP-3` · [UC-11](../../020-Requirements/Use-Cases/UC-11-Handle-Takedown-Request.md) khối `[!CAUTION]` *"Gộp hai thứ này là một lỗi"* |
| ⭐ **DoD = test rò rỉ chéo tenant PASS (`M1-1`)**, ⛔ không phải số bảng đã sửa; *"`tenant_id` trên 8/10 bảng = **vẫn rò rỉ**"* | — | [Story-Tenant-Id-And-RLS-Everywhere](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) §4 AC *"Xác minh được"* · §6 INVEST · [Roadmap §2](../../010-Planning/Roadmap.md) `M1-1` |
| Ba hành vi biên: từ chối insert thiếu `tenant_id` ở tầng constraint · session không có context ⇒ **fail-closed 0 row** · ⛔ không rò context qua connection pool | — | [Story-Tenant-Id-And-RLS-Everywhere](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) §4 AC *"Đường không hạnh phúc"* |
| **Cơ chế** bơm tenant context (`SET LOCAL app.current_tenant`, role `app_worker`, khoảng hở 1 statement khi claim job) — ⛔ ADR-010 không đặc tả lại | — | [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) |
| **Vị trí schema** của `tenant`/`user`/`membership` và nhóm bảng platform — ⛔ ADR-010 không quyết lại | — | [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) |
| Một database duy nhất (điều kiện để RLS còn giá trị) | `D-01`, `D-05` | [ADR-009](./ADR-009-Modular-Monolith-Three-Schemas.md) · [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-02`, `SRS-NFR-21` |
| Nhiệm vụ *"đóng băng, không mở lại"* của ADR-010 và danh sách `D-09`/`D-10`/`D-11`/`D-14` | — | [findings/architect §2.2](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) · §1.2 |

---

_Created by architect_
_Author: trisjr_
