---
id: SPEC-SEC-TENANT-ISOLATION
type: security-spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Spec Security: Tenant Isolation — Comic Studio

Threat model of: [SDD-Comic-Studio](../Architecture/SDD-Comic-Studio.md) · [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-010](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) · [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)

> [!CAUTION]
> ⭐ **Câu hỏi của tài liệu này ⛔ KHÔNG phải *"đã bật RLS chưa"*. Nó là: *"đường nào vòng được qua RLS"*.**
> Trả lời *"đã bật RLS"* là trả lời sai câu hỏi. [ADR-010 `D8`](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) đã chốt DoD là **một test nhị phân toàn cục** (`M1-1`), ⛔ **không phải** số bảng đã sửa — nguyên văn: *"`tenant_id` trên 8/10 bảng = **vẫn rò rỉ**"*.
> ⇒ Trọng tâm của file này là [§4 — catalog đường vòng `BP-1`…`BP-17`](#4--catalog-đường-vòng-bp-1bp-17).

> [!IMPORTANT]
> ⛔ **File này ⛔ không quyết lại cơ chế.** Cơ chế bơm tenant context đã CHỐT ở [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md); ràng buộc cô lập đã CHỐT ở [ADR-010](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md). File này **soi** chúng và **liệt kê đường vòng**.
> Mối đe doạ **không thuộc trục cô lập** (prompt injection, compositor, watermark, abuse control, anti-feature `SRS-NFR-15`) nằm ở [Spec-Security-Threat-Model](./Spec-Security-Threat-Model.md), ⛔ không lặp ở đây.

## Mục lục

1. [Câu hỏi chưa có câu trả lời](#1-câu-hỏi-chưa-có-câu-trả-lời)
2. [Tài sản & bề mặt tấn công của trục cô lập](#2-tài-sản--bề-mặt-tấn-công-của-trục-cô-lập)
3. [STRIDE trên bảy luồng `F1`–`F7` — góc cô lập](#3-stride-trên-bảy-luồng-f1f7--góc-cô-lập)
4. [⭐ Catalog đường vòng `BP-1`…`BP-17`](#4--catalog-đường-vòng-bp-1bp-17)
5. [Biện pháp & ma trận cưỡng chế](#5-biện-pháp--ma-trận-cưỡng-chế)
6. [Nghĩa vụ pháp lý — phần thuộc file này](#6-nghĩa-vụ-pháp-lý--phần-thuộc-file-này)
7. [Ma trận `KC-1`…`KC-7`](#7-ma-trận-kc-1kc-7)
8. [Bảng `TBD` của file này](#8-bảng-tbd-của-file-này)
9. [Tài liệu tham khảo](#9-tài-liệu-tham-khảo)

### Quy ước trích dẫn

| Ký hiệu | Nghĩa |
|---|---|
| `BP-n` | **B**ypass **P**ath — đường vòng qua cô lập, [§4](#4--catalog-đường-vòng-bp-1bp-17) |
| `IC-n` | Biện pháp cô lập (**I**solation **C**ontrol), [§5](#5-biện-pháp--ma-trận-cưỡng-chế) |
| `D1`…`D7`, `W-1`…`W-4` | Điều khoản và guardrail của [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |
| `T-n`, `P-n` | Mã `TBD` của [`SDD` §9](../Architecture/SDD-Comic-Studio.md) — ⛔ không đánh mã mới khi `SDD` đã có |
| `M1-1` | Test rò rỉ chéo tenant — **DoD nhị phân toàn cục** |

⛔ Requirement neo bằng **mã** (`SRS-FR-*` / `SRS-NFR-*`), ⛔ không bằng số dòng.

---

## 1. Câu hỏi chưa có câu trả lời

> [!CAUTION]
> ⛔ **Không hàng nào dưới đây được đọc thành *"rủi ro đã đánh giá"* hay thành giấy phép tự chọn số** (`R-5` · [`SRS` §5.2](../../020-Requirements/SRS-Comic-Studio.md)).

### 1.1 Câu hỏi thuộc chính trục cô lập — chủ đã xác định

| # | Câu hỏi | Vì sao nó chặn | Ai đóng | Khi nào |
|---|---|---|---|---|
| ~~`P-3`~~ | ~~Policy RLS cho `public.tenant` / `public."user"` / `public.membership` / `public.takedown_request`~~ | ✅ **ĐÃ ĐÓNG** — [DB-Entity-Tenancy](../Schema/DB-Entity-Tenancy.md) đóng phần ba bảng định danh, [DB-Entity-Compliance-And-Takedown](../Schema/DB-Entity-Compliance-And-Takedown.md) đóng phần `takedown_request`. ⇒ `BP-10`, `BP-14` kết luận được | — | — |
| `P-4` | Chi phí thực thi của hàm helper `public.current_tenant_id()` (có khối xử lý ngoại lệ) | Nếu đắt, đường lui là **validate ở tầng ứng dụng trước `SET LOCAL`** — ⛔ chỉ được làm **sau khi có số đo** và ⛔ không được bỏ test fail-closed | **Engineer** | Khi có bộ test tải đầu tiên (MVP0/MVP1) |
| **`D4.5`** | ⭐ **CTE claim + `set_config` trong MỘT statement** có làm khoảng hở bằng `0` không | ⚠️ **Chưa verify.** Thứ tự đánh giá `set_config` trong CTE ⛔ **không được PostgreSQL đảm bảo**, và ⛔ **một cơ chế bảo mật không được xây trên hành vi không được đảm bảo** ⇒ ⛔ **không được viết code dựa trên giả định nó chạy** | **Engineer** | MVP1, **bằng một test thật** |
| `T-6` | **`N` của `in_flight_per_tenant < N`** | Là ràng buộc **fairness/anti-DoS chéo tenant** nằm trong chính câu CLAIM; ⛔ chưa có `N` ⇒ test `W-2b` ⛔ chưa chạy được | **PM + Architect** | Sau MVP0 đo tải thật |
| **`M1-1` scope** | ⭐ **Danh sách ĐẦY ĐỦ bảng nghiệp vụ để `M1-1` phủ hết** | DoD là **thuộc tính toàn cục** ⇒ danh sách **phải đóng**; một bảng nằm ngoài danh sách là một lỗ ⛔ không ai phát hiện | **Architect**, lô `DB-Entity-*` + [ADR-005](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) cho nhóm bảng platform | Trước khi lô DB Schema được duyệt |
| **queue khác** | Tải chạy **ngoài `public.job`** (rollup `usage_daily`, golden dataset regression, hold reaper) lấy tenant context bằng cách nào: **job per tenant** hay **read carve-out riêng** | ⭐ Gốc của `BP-13`. ⚠️ [DB-Entity-Job-Queue](../Schema/DB-Entity-Job-Queue.md) đã chốt chúng chạy bằng **subcommand của image**, ⛔ **không** qua `public.job` ⇒ ⛔ **không** thừa hưởng trình tự `D4.2` | **Architect, lô DB Schema** | Khi đặc tả các bảng rollup |
| `T-7` | **TTL của signed URL** | Là tham số duy nhất giới hạn thời gian sống của một quyền đọc **đã rời khỏi hệ thống** (`BP-7`) | **Dev đề xuất, Founder duyệt** | MVP1 |
| **pooling** | Chế độ pooling cụ thể (session-mode hay transaction-mode) | ⭐ **⛔ KHÔNG chặn**: `SET LOCAL` an toàn với **cả hai** — ghi ra để một run sau ⛔ không tưởng rằng đây là điều kiện tiên quyết | [ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) | Lô ADR song song |

### 1.2 Câu hỏi CHỜ LUẬT SƯ — ⛔ Security Auditor KHÔNG có thẩm quyền đóng

| # | Câu hỏi | Nó chạm cô lập ở đâu | Ai đóng |
|---|---|---|---|
| `T-22` | **Có nghĩa vụ lưu trữ dữ liệu trong lãnh thổ Việt Nam không?** | Nếu *"phải"* ⇒ [ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) và [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) **mở lại cùng lúc** ⇒ vị trí vật lý của cả DB lẫn object storage đổi | ⭐ **PM + luật sư SHTT** |
| `T-23` | **`b-3` — giữ dữ liệu bao lâu** | ⭐ Quyết định **hard-delete `L-7` có ý nghĩa gì trên backup/PITR** (`BP-15`), và `change_log`/`usage_event` append-only tăng tới đâu | ⭐ **PM + luật sư SHTT** |
| `T-24` | **`b-4` — nghĩa vụ nào áp cho dữ liệu cá nhân** | `public.takedown_request` chứa email + SĐT của người **ngoài hệ thống**; nó nằm ngoài mô hình tenant ⇒ ⛔ không có RLS nào bảo vệ theo `tenant_id` | ⭐ **PM + luật sư SHTT** |
| `T-18`…`T-21`, `CẤM-13` | Bốn câu hỏi Điều 37a/37b/198b/khoản 4 Điều 11 + lệnh cấm viết như thể Điều 37a đã rõ | Không chạm cơ chế cô lập, nhưng ⛔ **không được đóng** ở file này | ⭐ **PM + luật sư SHTT** |

### 1.3 Câu hỏi CHƯA CÓ CHỦ

| # | Hàng | Ghi chú |
|---|---|---|
| `T-27` | `b-2` — lưu / mã hoá / **thu hồi** API key BYOK của khách | ⭐ **owner: Architect + Founder** (PM gán, [`E22`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md)); ⛔ cần **ADR mới** ⇒ **nợ kỹ thuật**. ⚠️ Ở góc cô lập: một key của khách bị lẫn sang tenant khác là **rò rỉ tài sản của bên thứ ba**, ⛔ không chỉ là rò rỉ dữ liệu nội bộ |
| `T-29` | Thông báo cho tenant bị takedown | ⭐ **owner: Founder + luật sư**, PM điều phối (PM gán, [`E22`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md)); ⛔ Security Auditor **từ chối đóng** vì đây là **quyết định pháp lý** — PM **chấp nhận** lời từ chối. Chi tiết ở [Spec-Security-Threat-Model](./Spec-Security-Threat-Model.md) |

---

## 2. Tài sản & bề mặt tấn công của trục cô lập

### 2.1 Cái gì đang được cô lập

| # | Tài sản | Vì sao ranh giới tenant là ranh giới sống-còn |
|---|---|---|
| `A-1` | **Bản thảo chưa công bố + Story Bible dẫn xuất** | Sản phẩm là nền tảng cho **người khác tự upload bản thảo chưa công bố của họ**. ⭐ Rò rỉ chéo tenant ở đây ⛔ **không phải một bug — nó là mất sản phẩm** |
| `A-2` | **Chuỗi provenance** (`change_log`, `field_provenance`, `usage_event`, lineage) | Là **bằng chứng pháp lý của khách**. Trộn bằng chứng giữa hai chủ thể pháp lý là hỏng chính thứ nó tồn tại để chứng minh |
| `A-3` | **Artifact ảnh** ở object storage, key `tenant/{tenant_id}/{sha256}` | ⛔ **KHÔNG dedup chéo tenant** — dedup tạo **một object dùng chung giữa hai chủ thể pháp lý khác nhau**, mâu thuẫn trực tiếp với lập luận bản quyền |
| `A-7` | **`tenant` / `user` / `membership`** | ⭐ Nguồn **duy nhất** của `tenant_id`. Sai ở đây làm **mọi** policy RLS sai theo |
| `A-10` | **Ngân sách gọi provider** | Một tenant chiếm hết worker là **DoS chéo tenant**, ⛔ không phải vấn đề hiệu năng |

### 2.2 Bốn DB role và ba loại session — ranh giới tin cậy thật

| Role | Dùng ở | Đặc quyền đặc thù | Rủi ro đặc trưng |
|---|---|---|---|
| `app_api` | Process `api`, đường đã đăng nhập | Tenant context bơm ở **một** middleware duy nhất | Mở connection thẳng, bỏ qua middleware ⇒ `0 row` **im lặng** (`BP-2`) |
| `app_worker` | Process `worker` | ⭐ **Đúng một cặp policy** trên `public.job`, xuyên tenant; ⛔ **KHÔNG `BYPASSRLS`** | ⭐ Đây là **chỗ duy nhất trên đường TENANT mà một câu `SELECT` nhìn thấy nhiều tenant** (`BP-4`, `BP-5`). ⚠️ ⛔ **Đừng đọc thành *"chỗ duy nhất trong hệ thống"*** — bề mặt operator (`BP-16`) là chỗ thứ hai, và nó ⛔ **không** đi qua `public.job` |
| `app_public_intake` | Đường takedown **công khai** | **Chỉ** `INSERT` vào `public.takedown_request`; ⛔ không `SELECT` bảng nghiệp vụ nào | Bề mặt Internet **không có tenant** (`BP-14`) |
| ⚠️ **`app_operator`** — ⛔ **CHƯA TỒN TẠI** | Đường **operator/quản trị** takedown (`TD-2`/`TD-3` của [Endpoint-Takedown-Public](../API/Endpoint-Takedown-Public.md)) | ⭐ `SELECT`/`UPDATE` **xuyên tenant** trên `public.takedown_request` (bảng ⛔ **không có `tenant_id`**) + `UPDATE` `public.project_access_state` + `INSERT` `public.change_log`; ⛔ **KHÔNG `BYPASSRLS`**, ⛔ không DDL, ⛔ không owner, ⛔ không `SELECT` bảng nghiệp vụ nào | ⭐⭐ **`BP-16`.** ⛔ **DB role CHƯA PIN** và **uỷ quyền tầng ứng dụng CHƯA CÓ CƠ CHẾ**. Phương án chốt + ripple `SDD` §7.4: [Spec-Security-Threat-Model §4.5](./Spec-Security-Threat-Model.md) |
| owner / migration | Chạy migration | Quyền DDL | ⭐ Bảng mới thiếu `tenant_id`/RLS; và **chủ sở hữu bảng** là một đường vòng ngầm của PostgreSQL (`BP-12`). ⛔ **Tuyệt đối ⛔ không dùng làm đường lui cho `app_operator`** — `BP-16` |

**Ba loại session hợp lệ** — cơ chế bơm context ⛔ **không được giả định mọi session DB đều có tenant**: (1) **có tenant**; (2) **không tenant nhưng có carve-out hẹp** (worker lúc claim, intake, ⚠️ **operator**, ⚠️ **lần ghi đầu `public."user"`**); (3) **owner/migration**.

⇒ **Bề mặt đặc quyền của toàn hệ thống rút về NĂM điểm đếm được**, và ⭐ **năm điểm này là danh sách review bảo mật cố định**.

> [!WARNING]
> ⚠️ ⭐ **Danh sách đếm BỀ MẶT, ⛔ không đếm CƠ CHẾ đã hiện thực.** `PS-4` và `PS-5` ⛔ **chưa có cơ chế được pin**, nhưng bề mặt của chúng **đã tồn tại trong đặc tả** ⇒ chúng ⛔ **không được** rơi khỏi danh sách chỉ vì chưa ai chọn cơ chế. Một tài liệu sau viết *"ba bề mặt đặc quyền"* là **lặp lại đúng chỗ hở mà mục này vá**.

| # | Bề mặt đặc quyền | Ràng buộc hình dạng | Trạng thái |
|---|---|---|---|
| **`PS-1`** | Hàm `SECURITY DEFINER` phân giải `user_id → tenant_id` | ⭐ Nhận `user_id`, trả **duy nhất** `tenant_id`; ⛔ không trả gì khác, ⛔ không nhận tham số nào khác. ⚠️ Nó chỉ **ĐỌC** | ✅ CHỐT (`D3`) |
| **`PS-2`** | Cặp policy carve-out trên `public.job` | `SELECT` phủ job **claim được** **VÀ** job **in-flight**; `UPDATE` ⛔ **chỉ** job claim được | ✅ CHỐT (`D4.1`) |
| **`PS-3`** | Role `app_public_intake` | Chỉ `INSERT`, đúng một bảng | ✅ CHỐT (`D6`) |
| ⭐ **`PS-4`** | **Đường operator xuyên tenant** — `SELECT`/`UPDATE` `public.takedown_request` + `UPDATE` `public.project_access_state` + `INSERT` `public.change_log` | ⛔ **KHÔNG `BYPASSRLS`** · ⛔ không `DELETE` · ⛔ không DDL · ⛔ không owner · ⛔ **không `SELECT`** bất kỳ bảng nghiệp vụ nào của `story`/`comic`/`generation`. ⭐ Nửa uỷ quyền nằm ở **tầng ứng dụng** ⇒ `pg_policies` ⛔ **không nhìn thấy nó** | ⛔ **CHƯA PIN** — `BP-16` |
| ⚠️ **`PS-5`** | **Lần GHI đầu tiên dòng `public."user"`** khi ⛔ chưa có tenant context | ⛔ Chỉ được ghi **đúng một** dòng `user` cho **đúng một** `external_auth_id`; ⛔ **không** kèm quyền đọc bảng nào khác; ⛔ **không** được hiện thực bằng cách nới `PS-1` sang chiều GHI | ⛔ **CHƯA PIN** — `BP-17` |

### 2.3 SÁU bề mặt nơi `tenant_id` phải đi qua một ranh giới

| # | Bề mặt | Điều gì mang `tenant_id` qua ranh giới |
|---|---|---|
| `AS-1` | HTTP request đã xác thực | `sub` của JWT → tra `membership` **mỗi request** ⇒ ⭐ token claim ⛔ **không bao giờ** là nguồn sự thật |
| `AS-9` | `public.job` | **Cột `tenant_id` của chính dòng `job`**, được ghi cùng transaction với công việc |
| `AS-4` | Key object storage | Tiền tố `tenant/{tenant_id}/` — ⭐ là thứ làm `L-7` (xoá theo tenant) khả thi, và cũng là thứ ⛔ **không được** để client tự đặt |
| `AS-2` | Endpoint takedown **công khai** (`TD-1`) | ⛔ **Không có** `tenant_id`. ⭐ Ngoại lệ duy nhất **của bề mặt CÔNG KHAI** — ⚠️ ⛔ **không** phải *"ngoại lệ duy nhất của toàn mô hình"*: xem hai hàng dưới |
| ⭐ `AS-13` | **Bề mặt OPERATOR** (`TD-2`/`TD-3`) | ⛔ **Không có** `tenant_id` — và ⭐ đây là bề mặt **XUYÊN tenant** (đọc/ghi dữ liệu của **mọi** tenant), khác hẳn `AS-2` vốn chỉ **ghi mù một dòng**. ⇒ `BP-16` |
| ⚠️ `AS-14` | **Lần ghi đầu tiên `public."user"`** | ⛔ **Chưa có** `tenant_id` **tại thời điểm ghi** — membership chưa tồn tại nên policy `EXISTS(membership)` ⛔ không qua được. ⇒ `BP-17` |

---

## 3. STRIDE trên bảy luồng `F1`–`F7` — góc cô lập

> ⚠️ Chỉ liệt kê mối đe doạ **thuộc trục cô lập**. Mối đe doạ khác của cùng luồng nằm ở [Spec-Security-Threat-Model](./Spec-Security-Threat-Model.md).
> Cột *"Đường vòng"* trỏ tới [§4](#4--catalog-đường-vòng-bp-1bp-17) — đó là nơi mối đe doạ được mổ xẻ.

| Luồng | STRIDE | Mối đe doạ ở trục cô lập | Đường vòng |
|---|:--:|---|---|
| **`F1`** Ingest | **I**, **E** | Object của tenant khác bị ghi đè / đọc nhầm vì key do client đặt; prefix `incoming/{upload_id}` **đoán được**; log opt-out (`story.ingest_check`) thiếu `tenant_id` | `BP-7`, `BP-12` |
| **`F1`** | **I** | ⭐ **Kênh rò rỉ qua dedup**: nếu content-address được làm **toàn cục**, một tenant suy ra được tenant khác **có cùng file** từ phản hồi *"đã tồn tại"* | `BP-8` |
| **`F2`** Extraction | **I** | `resolveState()` join xuyên bảng ở **tầng ứng dụng** — ⚠️ RLS ⛔ **không bảo vệ join phía application** | `BP-8` |
| **`F3`** Director | **T**, **I** | ID nhúng trong `page_layout JSONB` trỏ sang panel/asset của tenant khác — ⛔ **không FK nào kiểm** | `BP-9` |
| **`F4`** Hai gate | **E** | Endpoint ghi `PASS` cho `dialogue_line` của tenant khác bằng ID đoán được ⇒ RLS biến thành `0 row`, nhưng tầng API phải ⛔ **không** phân biệt *"không tồn tại"* với *"không thuộc về bạn"* | `BP-8` |
| **`F5`** Enqueue | **E** | Enqueue ghi `job.tenant_id` khác với tenant của session ⇒ ⛔ cách duy nhất chặn là ghi **cùng transaction đã có context** | `BP-6` |
| **`F5`** Claim | ⭐ **E** | ⭐ **Worker claim job của tenant khác**, hoặc chạy công việc trong **khoảng hở một statement** trước `SET LOCAL`, hoặc bind theo **payload** thay vì theo cột `tenant_id` của dòng job | `BP-3`, `BP-4`, `BP-5`, `BP-6` |
| **`F5`** Claim | **D** | Subquery đếm `in_flight_per_tenant` **luôn trả `0`** vì policy `SELECT` quá hẹp ⇒ fairness **không bao giờ ràng buộc**, và hỏng **im lặng** | `BP-5` |
| **`F5`** Ghi kết quả | **T** | `usage_event` / `change_log` ghi dưới **sai tenant** ⇒ trộn bằng chứng và trộn số liệu đối soát | `BP-3`, `BP-13` |
| **`F6`** Preview/Export | **I** | Endpoint ký URL theo **key do client gửi** ⇒ đọc artifact của tenant khác mà ⛔ không cần chạm DB | ⭐ `BP-7` |
| **`F6`** | **I** | Compositor đọc artifact **ngoài** transaction có context ⇒ hoặc `0 row` im lặng, hoặc phải nới quyền | `BP-2`, `BP-13` |
| **`F7`** Takedown | **E** | Bề mặt công khai được nới quyền *"cho tiện tra cứu"* ⇒ một đường đọc không tenant xuất hiện | `BP-14` |
| **`F7`** | **T** | Takedown thi hành bằng **hard-delete** ⇒ phá bằng chứng; hoặc hard-delete tenant chạy nhầm phạm vi ⇒ xoá dữ liệu tenant khác | `BP-15` |
| ⭐ **`F7`** Operator | ⭐ **E**, **I** | ⭐⭐ **Đường operator đọc/ghi XUYÊN TENANT**: `SELECT` toàn bảng `takedown_request` (⛔ không `tenant_id` ⇒ ⛔ không RLS nào lọc) và `UPDATE access_state` của project **bất kỳ tenant nào**. Đường lui *"cho tiện"* là chạy nó dưới **role owner** ⇒ RLS **im lặng không áp** trên **mọi** bảng | ⭐ `BP-16` |
| ⚠️ **Đăng nhập lần đầu** | **E** | **Ghi dòng `public."user"` khi ⛔ chưa có tenant context**; đường lui bản năng là **nới `PS-1` sang chiều GHI** hoặc thêm một carve-out thứ tư *"cho tiện"* | ⚠️ `BP-17` |
| **Mọi luồng** | **I** | Hai request của hai tenant **dùng lại cùng một connection** trong pool ⇒ rò `app.current_tenant` | ⭐ `BP-1` |
| **Mọi luồng** | **E** | Bảng mới sinh ra thiếu `tenant_id` / thiếu policy / index sai thứ tự cột | `BP-11`, `BP-12` |

---

## 4. ⭐ Catalog đường vòng `BP-1`…`BP-17`

> [!IMPORTANT]
> **Cách đọc**: mỗi đường vòng có bốn phần — *đường vòng là gì* · *vì sao nó vòng được* · *cái gì đang chặn nó (và ai sở hữu cái đó)* · *còn hở gì*.
> ⛔ Một đường vòng **được chặn** chỉ khi cái chặn nó là **thứ máy cưỡng chế được** (`R-1`): ràng buộc/quyền ở tầng DB, lint rule ở CI, hoặc test tự động. ⛔ Không có ngoại lệ, vì đội **1 người, ⛔ không có code review**.

### `BP-1` — Rò `app.current_tenant` qua connection pool

- **Đường vòng**: dùng `SET app.current_tenant` (không có `LOCAL`) hoặc `set_config('app.current_tenant', ..., false)`. Biến sống ở **mức session** ⇒ nó **đi theo connection về pool** và có mặt ở request kế tiếp — **của tenant khác**.
- **Vì sao vòng được**: hai câu SQL đó **trông giống hệt** câu đúng. ⛔ Không có gì trong cú pháp báo động.
- **Đang chặn bởi**: `SET LOCAL` tự hết hiệu lực ở `COMMIT`/`ROLLBACK` ⇒ ⭐ **điểm reset là tự động**, ⛔ không phụ thuộc việc ai đó nhớ gọi `RESET` (`D1`, `D5`). ⛔ **Cấm** hai dạng trên **ở mọi nơi trong codebase**, cưỡng chế bằng **lint/grep rule ở CI**. Test: hai tenant xen kẽ trên cùng pool (`D9` hành vi 3) + `W-4` (sau `COMMIT`, `public.current_tenant_id()` phải trả `NULL`).
- **Còn hở**: ⛔ không, **nếu** lint rule tồn tại. ⚠️ Lint rule đó là hạng mục công việc **thật**, ⛔ không phải ghi chú.

### `BP-2` — Truy vấn ở chế độ autocommit / ngoài transaction tường minh

- **Đường vòng**: mở connection thẳng, hoặc chạy một read đơn lẻ **ngoài** middleware ⇒ ⛔ không có `SET LOCAL` ⇒ ⛔ không có context.
- **Vì sao vòng được**: kết quả ⛔ **không phải lỗi** — nó là **`0 row`**. Với một pipeline, *"không có gì"* rất dễ bị xử lý thành *"bỏ qua"*.
- **Đang chặn bởi**: fail-closed là **thiết kế đã chọn** — thiếu context ⇒ `0 row`, ⛔ không phải exception (`D2`, `D9` hành vi 2). ⭐ Hệ quả bắt buộc: **mọi truy vấn chạm dữ liệu tenant phải nằm trong một transaction tường minh** — ràng buộc lan khắp codebase, ⛔ **không có ngoại lệ**.
- **Còn hở**: ⭐ **Có, và nó là hở nghiêm trọng nhất về mặt PHÁT HIỆN.** Fail-closed ⇒ ⛔ **không có alert**; bug hiện ra dưới dạng *"dữ liệu trống"*. ⚠️ Khả năng phát hiện phụ thuộc `b-7` (observability) — ⛔ **chưa có chủ đóng** (`T-16`, **Dev**, sau khi platform được mua).
- ⛔ **Cách "sửa" bị CẤM**: nới quyền role — xem `BP-4`.

### `BP-3` — Một transaction phục vụ HAI tenant

- **Đường vòng**: một vòng lặp claim **nhiều** job trong **cùng một** transaction, hoặc một job nền xử lý nhiều tenant liên tiếp, rồi gọi `SET LOCAL` lần thứ hai để "đổi tenant". Mọi câu lệnh **trước** lần đổi đã chạy dưới tenant cũ; mọi câu **sau** chạy dưới tenant mới — trong **cùng một** đơn vị nguyên tử. Một lần rollback kéo theo cả hai.
- **Vì sao vòng được**: `SET LOCAL` **cho phép** gọi lại trong cùng transaction. ⛔ Không có gì ở tầng DB ngăn việc đó.
- **Đang chặn bởi**: ⭐ **hệ quả dẫn xuất** của trình tự bắt buộc `D4.2` — `BEGIN` → claim → `SET LOCAL` → **toàn bộ công việc** → `COMMIT`, và *"`SET LOCAL` tự hết hiệu lực ⇒ worker quay lại vòng lặp ở trạng thái **không tenant**, là trạng thái an toàn mặc định"*. ⇒ Trình tự đó ⛔ **không có chỗ** cho tenant thứ hai. Cưỡng chế: `W-3` — hai bước gói trong **đúng một** hàm `claimJobAndBindTenant()` + lint rule chặn mọi truy vấn trực tiếp vào `public.job` ngoài hàm đó.
- **Còn hở**: ⚠️ Với **job nền không đi qua `claimJobAndBindTenant()`** (rollup, export toàn tenant) thì ràng buộc trên ⛔ **chưa được phát biểu** — đó chính là `BP-13`.

### `BP-4` — Khoảng hở một statement giữa CLAIM và `SET LOCAL`

- **Đường vòng**: chèn một câu lệnh nghiệp vụ vào giữa bước claim và bước `SET LOCAL`. Session **đã giữ row `job`** nhưng **chưa có tenant context**.
- **Vì sao vòng được**: khoảng hở **tồn tại thật**, dài **đúng một statement** — và [ADR-006 `D4.3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) gọi tên nó thay vì giấu.
- **Đang chặn bởi**: trong khoảng đó mọi truy vấn nghiệp vụ trả **`0 row`** ⇒ ⭐ **an toàn về rò rỉ**. Bốn guardrail cưỡng chế được: `W-1` (test: truy vấn ngay sau claim phải trả `0 row`) · `W-2` (test CI: `pg_roles.rolbypassrls = false` cho `app_worker`; đối chiếu `pg_policies` với hằng số trong repo) · `W-3` (lint rule) · `W-4` (test reset sau `COMMIT`).
- **Còn hở**: ⭐ **Rủi ro thật ⛔ KHÔNG phải khoảng hở tự nó — mà là PHẢN ỨNG của một dev khi gặp `0 row`**: cách "sửa" theo bản năng là **nới quyền role worker** (`BYPASSRLS`, hoặc thêm policy xuyên tenant cho bảng nghiệp vụ). ⛔ `BYPASSRLS` xoá RLS trên **mọi** bảng, ở đúng process phục vụ **nhiều tenant nhất**. `W-2` tồn tại để làm **CI đỏ** khi ai đó làm vậy. ⚠️ Phương án khoảng-hở-bằng-`0` (`D4.5`) **chưa verify** ⇒ ⛔ không được viết code dựa trên giả định nó chạy.

### `BP-5` — Carve-out trên `public.job` bị nới hoặc bị bóp

- **Đường vòng, hai chiều ngược nhau**:
  - **Nới**: cấp thêm `UPDATE` trên job **in-flight**, hoặc thêm một bảng nghiệp vụ vào carve-out *"cho worker tiện làm việc"* ⇒ worker sửa được job của tenant khác.
  - **Bóp**: policy `SELECT` chỉ lộ row *"claim được"* ⇒ subquery đếm `in_flight_per_tenant` **luôn trả `0`** ⇒ điều kiện fairness **không bao giờ ràng buộc** — và nó hỏng **im lặng**.
- **Vì sao vòng được**: cả hai đều trông như tinh chỉnh vô hại của một policy.
- **Đang chặn bởi**: hình dạng carve-out đã CHỐT ở `D4.1` — `SELECT` phủ **cả** job claim được **và** in-flight (⭐ *"bắt buộc phải gồm cả in-flight"*), `UPDATE` ⛔ **chỉ** job claim được. `app_worker` ⛔ **không** có policy xuyên tenant trên **bất kỳ bảng nghiệp vụ nào**. Cưỡng chế: `W-2` (đối chiếu `pg_policies` với hằng số) + `W-2b` (seed một tenant có `N` job in-flight ⇒ CLAIM phải trả **0 job** của tenant đó).
- **Còn hở**: ⚠️ `W-2b` ⛔ **chưa chạy được** cho tới khi `T-6` (`N`) đóng — **PM + Architect, sau MVP0**.

### `BP-6` — Bind tenant theo PAYLOAD thay vì theo cột `tenant_id` của dòng `job`

- **Đường vòng**: `SET LOCAL app.current_tenant` lấy giá trị từ một trường trong payload JSON của job (hoặc từ một tham số do người gọi truyền) thay vì từ **cột `tenant_id` của chính dòng `job`** vừa claim.
- **Vì sao vòng được**: payload là dữ liệu, ⛔ không phải cột được RLS canh; nếu có một đường nào cho phép ảnh hưởng payload thì đó là **elevation**.
- **Đang chặn bởi**: `D4.2` bước 3 viết rõ giá trị là **`<job.tenant_id>`**; và enqueue (`INSERT generation` + `INSERT job` cùng transaction) chạy **dưới context của chính tenant đó** ⇒ dòng `job` ⛔ không thể mang `tenant_id` lạ mà vẫn `INSERT` được (RLS `WITH CHECK` **từ chối ồn ào** khi ghi sai, khác với đọc sai chỉ trả `0 row`). Worker ⛔ **không được** gọi vendor auth để lấy ngữ cảnh — *"job mang `tenant_id` từ chính dòng `job`"*.
- **Còn hở**: ⛔ không, **nếu** `claimJobAndBindTenant()` là đường duy nhất (`W-3`).

### `BP-7` — Signed URL: bốn đường vòng khác nhau, ⛔ đừng gộp

| # | Đường vòng | Đang chặn bởi | Còn hở |
|---|---|---|---|
| **a** | ⭐ **Endpoint nhận `key` từ client rồi ký** ⇒ ai gửi key của tenant khác cũng lấy được URL hợp lệ. ⚠️ Key là `tenant/{tenant_id}/{sha256}` — **cấu tạo đã biết**, ⛔ không phải bí mật | ⭐ Ràng buộc **dẫn xuất bắt buộc**: URL chỉ được ký cho **key đọc ra từ một dòng DB đã qua RLS trong transaction hiện tại**. ⛔ Không có endpoint *"xin URL cho một key bất kỳ"* — [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 6 đã chốt hình dạng: URL phát **theo lô, kèm ngay trong response của resource**, ⛔ không phải endpoint *"xin URL cho từng ảnh"* | ⚠️ Phải được viết thành ràng buộc tường minh ở **lô API** (`IC-5`) |
| **b** | **URL bị lưu bền** ⇒ tồn tại ngoài phiên: trong DB, trong log, trong file export, trong email/webhook | ⭐ [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 3 — ⛔ **KHÔNG BAO GIỜ** lưu bền; DB **chỉ lưu `key`**. *"Một URL đã ký nằm trong log hoặc trong PDF là một **public bucket thu nhỏ** có thời hạn"* | Cần **test CI grep log** — xem `IC-6` |
| **c** | **TTL quá dài** ⇒ cửa sổ khai thác rộng | Điều 4–5 của ADR-004 làm hệ thống chạy đúng với **TTL bất kỳ**; ràng buộc lên con số đã chốt sẵn | Con số = `T-7`, **Dev + Founder, MVP1** |
| **d** | **`incoming/{upload_id}` đoán được** ⇒ ghi đè upload đang chờ của chính tenant, hoặc đặt dữ liệu chưa kiểm | ⛔ Không object nào trong `incoming/` được coi là dữ liệu hợp lệ; ⛔ không đường đọc nào của sản phẩm trỏ vào prefix đó | ⚠️ Tính **không đoán được** của `upload_id` phải là ràng buộc tường minh ở lô API |

### `BP-8` — RLS ⛔ KHÔNG bảo vệ join phía application

- **Đường vòng**: lấy dữ liệu bằng hai truy vấn rồi **join trong code**; hoặc quên `WHERE tenant_id` và tin rằng RLS đã lo.
- **Vì sao vòng được**: ⚠️ Đây là **giới hạn đã biết và đã ghi tường minh** của RLS, ⛔ không phải khiếm khuyết cần vá: *"RLS **không** bảo vệ được join thực hiện phía application"*.
- **Đang chặn bởi**: (1) ⭐ **RLS là lớp phòng thủ THỨ HAI** — code **vẫn phải** viết `WHERE tenant_id = ...`; đọc thành *"có RLS rồi nên khỏi filter"* là **hiểu ngược**. (2) Giữ **một** database để mọi join nằm **trong** phạm vi RLS — đó là căn cứ của [ADR-009](../Architecture/ADR-009-Modular-Monolith-Three-Schemas.md), và nó làm ràng buộc *"một database"* thành **bắt buộc vĩnh viễn**. (3) `comic` gọi `story` **chỉ qua** `resolveState()` và `getBible()`, cưỡng chế bằng **lint rule** (`B-1`).
- **Còn hở**: ⭐ **Có — về nguyên lý.** Đây là lý do `M1-1` phải là **test toàn cục** chứ không phải kiểm từng bảng. ⚠️ Hệ quả phụ: phản hồi của API ⛔ **không được** phân biệt *"không tồn tại"* với *"không thuộc về bạn"* (`IC-7`), nếu không `0 row` trở thành một **oracle** dò sự tồn tại tài nguyên tenant khác. ⚠️ Cùng cơ chế rò gián tiếp: **dedup chéo tenant** — bị cấm sẵn (`A-3`).

### `BP-9` — Tham chiếu chéo tenant nhúng trong `JSONB`

- **Đường vòng**: ghi một ID của tenant khác vào một trường bên trong `page_layout JSONB`, `conditioning_set`, hoặc `degradations`. ⛔ **Không FK nào kiểm** giá trị nằm trong JSONB.
- **Vì sao vòng được**: RLS canh **row**, FK canh **cột** — ⛔ ⛔ không cơ chế nào canh **ID nằm trong tài liệu JSON**.
- **Đang chặn bởi**: khi **đọc**, ID lạ sẽ resolve ra `0 row` ⇒ ⛔ không lộ dữ liệu. Đó là lớp chặn thật, và nó đủ để chặn **rò rỉ**.
- **Còn hở**: ⭐ **Có, ở hai chỗ**: (1) giá trị lạ **vẫn được ghi vào DB** ⇒ dữ liệu bẩn tồn tại; (2) khi đọc, nó hỏng **im lặng** (`0 row`) đúng kiểu `BP-2`. ⇒ **Ràng buộc**: mọi ID nghiệp vụ trong JSONB phải được **validate theo schema và resolve trong cùng transaction có context** trước khi ghi. ⚠️ Hình dạng cụ thể thuộc **Architect, lô DB Schema**, khi đặc tả các bảng mang JSONB.

### `BP-10` — `tenant_id` đến từ một bản sao đã ký thay vì từ DB

- **Đường vòng**: đọc `tenant_id` (hoặc role) từ **custom claim** trong JWT của vendor auth.
- **Vì sao vòng được**: nó **tiện hơn** — tiết kiệm một truy vấn `membership` mỗi request. ⚠️ Và đây là **phương án hấp dẫn nhất** ở tầng vendor: dùng luôn *"Organizations"* của vendor làm `tenant`.
- **Đang chặn bởi**: ⭐ [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 4 — custom claim ⛔ **KHÔNG BAO GIỜ** là nguồn sự thật; `tenant_id` và role **tra từ `membership` trong DB của ta ở mỗi request**. Lý do là **lý do bảo mật**: *"quyền truy cập phải neo vào trạng thái hiện tại trong DB, ⛔ không neo vào một bản sao đã ký"* — một token phát **trước khi** thu hồi membership vẫn mở được dữ liệu cho tới khi hết hạn. Phương án *"Organizations của vendor làm `tenant`"* đã bị **loại dứt khoát**.
- **Còn hở**: ⛔ không về cơ chế — ⭐ policy cho ba bảng định danh **đã đóng** ([DB-Entity-Tenancy](../Schema/DB-Entity-Tenancy.md), hàng `P-3`), và ⛔ **không** carve-out xuyên tenant nào tồn tại trên ba bảng đó. ⚠️ Phần phải canh vĩnh viễn: `PS-1` (hàm `SECURITY DEFINER`) là **bề mặt đặc quyền duy nhất của đường API ĐÃ ĐĂNG NHẬP của tenant** *(⛔ không phải của toàn tầng HTTP — đường operator `PS-4`/`BP-16` là một bề mặt riêng)* — nới tham số hoặc nới kiểu trả về là mở đường vòng, và đường đăng nhập phải đi qua **đúng hàm đó**, ⛔ không truy vấn thẳng bảng `user` khi chưa có context.

### `BP-11` — ⚠️ Ngoại lệ ĐÃ ĐƯỢC DUYỆT: `generation.visual_vocabulary` không có `tenant_id`

> [!WARNING]
> ⭐ **Đây là ngoại lệ đã được duyệt, ⛔ không phải một lỗ hổng — và cũng ⛔ không phải một tiền lệ.**

- **Bản chất**: `generation.visual_vocabulary` là **dữ liệu do operator soạn offline**, ⛔ không phải dữ liệu của tenant nào ⇒ nó **cố ý không có `tenant_id`**. ⛔ Không có gì để cô lập vì bảng ⛔ không chứa dữ liệu của tenant nào.
- **Guardrail thay thế**: ⭐ **quyền ghi** — `REVOKE INSERT, UPDATE, DELETE` khỏi `app_api` và `app_worker`, hai role ứng dụng **chỉ có `SELECT`** (`V-2` của [DB-Entity-Prompt-Vocabulary](../Schema/DB-Entity-Prompt-Vocabulary.md)). Ghi **chỉ** qua role owner/migration (`D7`).
- ⚠️ **Đừng gộp nhầm với bảng bên cạnh**: `generation.action_pose_cache` chứa **action text của tenant** ⇒ nó **CÓ `tenant_id NOT NULL` + RLS** như mọi bảng nghiệp vụ. Ngoại lệ áp cho **đúng một** bảng, ⛔ không cho cả schema.
- ⭐ **Ràng buộc lên test CI của `SRS-NFR-01`** — ⛔ đây là phần dễ làm sai nhất:

| ✅ Đúng | ⛔ SAI |
|---|---|
| Test **whitelist đúng bảng `generation.visual_vocabulary`**, kèm **comment** trỏ về mục ngoại lệ ở [DB-Entity-Prompt-Vocabulary](../Schema/DB-Entity-Prompt-Vocabulary.md) và nêu guardrail thay thế | ⛔ Nới test thành *"bỏ qua mọi bảng không có `tenant_id`"* / *"`tenant_id` trên hầu hết bảng"* — ⭐ **cách đó biến mọi bảng quên `tenant_id` trong tương lai thành hợp lệ**, tức phá đúng thứ test tồn tại để bắt |

- **Còn hở**: ⛔ không, **nếu** whitelist là **danh sách hằng số một phần tử**. ⭐ **Thêm phần tử thứ hai phải qua ADR, ⛔ không qua PR sửa test.**

### `BP-12` — Bảng mới sinh ra không có ba nghĩa vụ; và **chủ sở hữu bảng**

- **Đường vòng a**: thêm một bảng nghiệp vụ mà quên **một trong ba nghĩa vụ**: cột `tenant_id NOT NULL` · `tenant_id` là **cột ĐẦU TIÊN** của mọi composite index · **một policy RLS**. ⭐ *"`tenant_id` trên 8/10 bảng = **vẫn rò rỉ**"*.
- **Đường vòng b**: ⚠️ **Chủ sở hữu bảng trong PostgreSQL ⛔ không chịu RLS theo mặc định.** Nếu một role ứng dụng trở thành owner của một bảng, policy trên bảng đó **im lặng không áp dụng**.
- **Đang chặn bởi**: (a) Test CI toàn cục — số bảng xuất hiện trong `pg_policies` phải **bằng đúng** số bảng có cột `tenant_id`; catalog check `pg_index` + `pg_attribute` cho **0 index** có `tenant_id` không đứng đầu; script liệt kê **0 bảng** thiếu `NOT NULL`. (b) ⭐ **Hệ quả dẫn xuất của `D7`**: migration chạy dưới **role owner riêng**, ⛔ role ứng dụng **không có DDL** ⇒ role ứng dụng ⛔ **không phải** owner của bảng nào. Điều này ⛔ **phải được kiểm bằng test CI**, ⛔ không phải bằng niềm tin.
- **Còn hở**: ⚠️ Danh sách bảng nghiệp vụ để `M1-1` phủ hết ⛔ **chưa đóng** — **Architect, lô DB Schema**.

### `BP-13` — Job nền chạy NGOÀI request context

- **Đường vòng**: rollup `usage_daily`, golden dataset regression, export toàn bộ dữ liệu tenant, dọn rác `incoming/` — ⛔ **không có HTTP request**, ⛔ không có middleware, ⛔ không đi qua `claimJobAndBindTenant()`. Chúng cần đọc dữ liệu của **nhiều tenant**.
- **Vì sao vòng được**: bản năng khi gặp `0 row` ở một cron là **cấp thêm quyền cho role chạy cron** — và đó là `BYPASSRLS` dưới một cái tên khác.
- **Đang chặn bởi**: hai ràng buộc **hình thức** — cron chỉ được **gọi một subcommand của chính image**, ⛔ không một dòng logic nghiệp vụ nào sống trong cấu hình cron; và ⛔ tuyệt đối không `BYPASSRLS`. ⚠️ **Một dữ kiện đã chốt làm câu hỏi sắc hơn, ⛔ không làm nó biến mất**: [DB-Entity-Job-Queue](../Schema/DB-Entity-Job-Queue.md) ghi rõ rollup `usage_daily`, golden dataset regression và hold reaper ⛔ **KHÔNG đi qua `public.job`** ⇒ chúng ⛔ **không** thừa hưởng trình tự claim của `D4.2`, tức ⛔ **không** có sẵn bước `SET LOCAL` nào.
- **Còn hở**: ⭐ **CÓ — đây là hở lớn nhất còn lại của trục cô lập.** Câu hỏi *"chạy dạng **job per tenant** (⇒ hợp `D4.2` nguyên trạng) hay cần một **read carve-out riêng**"* là hàng `TBD` đã được [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) route đi, và ⛔ **file này ⛔ không chọn giúp**. **Ai đóng: Architect, lô DB Schema**, khi đặc tả các bảng rollup. ⛔ **Không ai được hiện thực cron theo hướng nới quyền trước khi hàng đó đóng** — bản năng *"cấp thêm quyền cho role chạy cron"* chính là `BP-4` dưới một cái tên khác.

### `BP-14` — Bề mặt công khai không có tenant bị nới quyền

- **Đường vòng**: cấp `SELECT` cho `app_public_intake` *"để trang công khai hiển thị trạng thái đơn"*; hoặc cho đường intake bypass RLS *"vì nó không có tenant"*.
- **Đang chặn bởi**: ⛔ Role `app_public_intake` **chỉ** `INSERT` vào `public.takedown_request`; ⛔ ⛔ **không** giải bằng cách cho đường này bypass RLS; ⛔ **không** cho nó `SELECT` bất kỳ bảng nghiệp vụ nào (`D6`).
- **Còn hở**: ⛔ Không về policy — phần `public.takedown_request` của `P-3` **đã đóng** ở [DB-Entity-Compliance-And-Takedown](../Schema/DB-Entity-Compliance-And-Takedown.md). ⚠️ Còn lại **hai hở ngoài kỹ thuật**: bảng này chứa **dữ liệu cá nhân của người ngoài hệ thống** ⇒ nghĩa vụ áp dụng = `T-24` (**PM + luật sư SHTT**); và thông báo cho tenant bị nhắm = `T-29` (⛔ **chưa có chủ**).

### `BP-15` — Hai đường xoá bị gộp; và dữ liệu sống sót ngoài DB

- **Đường vòng a**: dùng **hard-delete** để thi hành takedown ⇒ **phá mất chính bằng chứng** counter-notice cần, và provenance ⛔ **không backfill được**.
- **Đường vòng b**: hard-delete tenant chạy nhưng **bỏ sót** một nhánh — ⚠️ Story Bible là **nhóm bảng nhiều nhất**, nên là chỗ dễ sót nhất — hoặc xoá trong DB mà **quên object storage**.
- **Đường vòng c**: dữ liệu đã xoá vẫn còn trong **backup/PITR** và trong bản export dữ liệu tenant.
- **Đang chặn bởi**: ⭐ **Hai đường xoá TÁCH BIỆT tuyệt đối** (`D7` của [ADR-010](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md)) — takedown = **soft-delete + disable-access cấp project**, ⛔ **KHÔNG hard delete**; hard-delete tenant = kỷ luật `ON DELETE CASCADE` trên **mọi** FK, và đường đó phải **tồn tại VÀ đã được kiểm thử**. Ở object storage: key mang tiền tố `tenant/{tenant_id}/` ⇒ xoá theo prefix **khả thi**; `api`/`worker` ⛔ **không** có quyền `DeleteObject` trên prefix canonical ⇒ xoá **chỉ** đi qua đường riêng có đặc quyền.
- **Còn hở**: ⭐ (c) ⛔ **chưa có câu trả lời**: retention nghiệp vụ = `T-23` (**PM + luật sư SHTT**); RPO/RTO/backup retention = `T-9` (**Founder + dev, sau MVP0**). ⇒ ⛔ **Không được** tuyên bố *"đã xoá hết dữ liệu tenant"* cho tới khi hai hàng đó đóng.

### `BP-16` — ⭐⭐ Đường OPERATOR xuyên tenant trên `public.takedown_request`

> [!CAUTION]
> ⭐ **Đây là bề mặt mà catalog này ⛔ chưa biết cho tới lô L33.** Tầng API sinh ra **sau** ba file Security và nó tạo ra một đường đọc/ghi **xuyên tenant ở tầng HTTP** — thứ mà toàn bộ `BP-1`…`BP-15` **giả định là không tồn tại**.

- **Đường vòng**: `GET /v1/admin/takedown-requests` (`TD-2`) và `PATCH /v1/admin/takedown-requests/{id}` (`TD-3`) của [Endpoint-Takedown-Public](../API/Endpoint-Takedown-Public.md). Chúng **đọc và ghi dữ liệu của MỌI tenant**: `requester_email`, `requester_phone` (`A-9`), `project_id`, và `access_state` của `public.project_access_state`.
- **Vì sao vòng được** — ⭐ **ba lý do độc lập, ⛔ đừng gộp**:
  1. ⭐ `public.takedown_request` ⛔ **không có `tenant_id`** ⇒ ⛔ **không viết được** vị từ `tenant_id = public.current_tenant_id()` ⇒ **RLS ⛔ không lọc gì cả**. Đây ⛔ không phải policy viết sai — bảng **cố ý** nằm ngoài mô hình tenant (`BP-14`).
  2. ⛔ **DB role CHƯA PIN**: `app_public_intake` ⛔ **không** được `SELECT`; `app_api` ⛔ **không** có đường xuyên tenant. ⇒ ⚠️ Cái *"chưa pin"* đó tạo áp lực chọn **role owner** — mà owner ⛔ **không chịu RLS theo mặc định** ⇒ đó là `BP-12b` **dựng lên như thiết kế**, và nó xoá RLS trên **mọi** bảng chứ ⛔ không riêng một bảng.
  3. ⛔ **Uỷ quyền operator ở tầng ứng dụng CHƯA TỒN TẠI**: `membership` ⛔ không có mô hình role/permission. ⇒ ⭐ **Toàn bộ kiểm soát truy cập của hai endpoint này nằm ở một thứ CHƯA CÓ.**
- **Đang chặn bởi**: ⭐ **hiện tại: một CÂU CHỮ, ⛔ không phải một cơ chế.** [Endpoint-Takedown-Public](../API/Endpoint-Takedown-Public.md) ghi `TD-2`/`TD-3` ⛔ **không được triển khai** trước khi `TD-Q1` đóng. Theo `R-1`/`C-2`, một ràng buộc chỉ tồn tại dưới dạng câu chữ thì **coi như không tồn tại** ⇒ ⭐ **cái chặn thật là: endpoint chưa được viết.**
- **Còn hở** — ⭐ **CÓ, mức CAO**:
  - ⚠️ ⭐ **`W-2` (đối chiếu `pg_policies` + `pg_roles` với hằng số repo) ⛔ MÙ với đường vòng này.** Nửa uỷ quyền sống ở **tầng ứng dụng**; một catalog check ở tầng DB ⛔ **không có gì để so sánh**. ⇒ Cần phép kiểm thứ hai — `IC-13`.
  - ⚠️ ⛔ **`M1-1` cũng ⛔ không bắt được**: `M1-1` seed hai tenant A/B rồi khẳng định session A trả `0 row` thuộc B. `takedown_request` ⛔ **không có `tenant_id`** ⇒ ⛔ **không biểu diễn được** *"dòng thuộc B"* ⇒ hàng này nằm **ngoài phạm vi DoD**. ⭐ Ghi ra để ⛔ không ai đọc *"`M1-1` xanh"* thành *"⛔ không còn đường xuyên tenant nào"*.
  - ⭐ **Phương án đã chốt** (role thứ năm `app_operator`, đường owner **bị loại**, hình dạng grant, ràng buộc uỷ quyền): [Spec-Security-Threat-Model §4.5](./Spec-Security-Threat-Model.md). ⚠️ **Nó buộc sửa [`SDD` §7.4](../Architecture/SDD-Comic-Studio.md)** — mà tầng Architecture **đã đóng băng** ⇒ ⛔ **file này ⛔ không sửa**; PM xử ở close-step.
- ⛔ **Ba cách "sửa" bị CẤM tường minh**: ⛔ chạy dưới **owner** (căn cứ ở trên) · ⛔ cấp `BYPASSRLS` cho một role operator *"vì bảng không có `tenant_id`"* (`IC-4`) · ⛔ cấp cho `app_operator` thêm `SELECT` trên `story.project` *"cho tiện hiển thị tiêu đề"* — cách đó biến `TD-2` thành **đường liệt kê tác phẩm của mọi tenant**.

### `BP-17` — ⚠️ Lần GHI ĐẦU TIÊN dòng `public."user"` khi chưa có tenant context

- **Đường vòng**: dòng `public."user"` phải được tạo **trước khi** có `membership`, nhưng policy của bảng đó dựa trên `EXISTS(membership)` ⇒ dưới một session bình thường, `INSERT` đó ⛔ **không qua được**. Bản năng khi gặp bế tắc: **nới hàm `SECURITY DEFINER` của `PS-1` sang chiều GHI**, hoặc mở một carve-out thứ tư *"cho tiện"*, hoặc chạy nó dưới owner.
- **Vì sao vòng được**: ⭐ **cả hai nhánh đã biết đều rơi vào đây, ⛔ không nhánh nào thoát**: (a) **webhook vendor auth** ghi dòng `user` từ một callback ⛔ không có phiên người dùng; (b) **JIT provisioning** tạo dòng ngay ở **request đã xác thực đầu tiên** — cũng là lúc ⛔ chưa có membership. ⇒ Đây ⛔ **không** phải một chi tiết triển khai của một nhánh, nó là **thuộc tính của cả hai**.
- **Đang chặn bởi**: ⛔ **chưa có gì.** [ADR-006 `D6`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) ⛔ **không phủ** trường hợp này — carve-out đó chỉ cho `INSERT` vào `public.takedown_request`; và hàm `SECURITY DEFINER` của `D3` chỉ **ĐỌC** `user → tenant`, ⛔ **không ghi**. [Endpoint-Tenancy](../API/Endpoint-Tenancy.md) (`API-TN-5`) phát biểu yêu cầu rồi **route thẳng sang file này**, và ⛔ **từ chối tự phát minh** một đường đặc quyền thứ tư — ✅ **đúng kỷ luật**.
- **Còn hở** — ⭐ **CÓ**. ⛔ File này ⛔ **cũng không chọn cơ chế**, vì việc chọn kéo theo `ADR-006` (đã đóng băng) và vì nhánh **webhook hay JIT** ⛔ **chưa chốt** (`Spec-Integration-Auth-Provider.md` §3 để mở) — chọn hộ là **đóng hộ một quyết định của Architect**. ⇒ **Ai đóng: Architect**, trước request đã xác thực đầu tiên.
- ⭐ **Ràng buộc hình dạng mà file này SỞ HỮU và CHỐT** — cơ chế nào cũng phải thoả:
  1. ⛔ **KHÔNG nới `PS-1` sang chiều GHI.** `PS-1` là **bề mặt đặc quyền duy nhất của đường API đã đăng nhập**; biến nó thành đọc-ghi là mở rộng đúng điểm nhạy nhất. Nếu cần một hàm `SECURITY DEFINER` để ghi thì đó phải là **một hàm KHÁC, có tên khác**, và nó là `PS-5` — ⛔ không phải một tham số thêm vào `PS-1`.
  2. ⛔ **KHÔNG `BYPASSRLS`**, ⛔ **không** dùng role owner (`IC-4`, `IC-11`).
  3. ⭐ Đặc quyền phải **hẹp tới đúng một bảng và đúng một hành vi**: ghi/upsert **một** dòng `user` theo `external_auth_id`. ⛔ **Không** kèm quyền đọc `membership`, `tenant`, hay bất kỳ bảng nghiệp vụ nào.
  4. ⭐ **Idempotent theo `UNIQUE(external_auth_id)`**, ⛔ không *"check-rồi-insert"* — hai request đồng thời ⇒ một thắng, một bắt lỗi unique rồi **đọc lại**. *(Khuôn này [Endpoint-Tenancy](../API/Endpoint-Tenancy.md) đã viết đúng.)*
  5. ⭐ **Đặc quyền dừng NGAY sau bước đó**: phần còn lại của request phải chạy dưới tenant context bình thường. ⚠️ Một đặc quyền *"sống suốt request"* biến mọi truy vấn tiếp theo thành `BP-3` (một transaction phục vụ hai ngữ cảnh).
  6. ⭐ **Bất kể chọn nhánh nào**, cơ chế được chọn phải vào **danh sách `PS-*`** và chịu `IC-13`.

---

## 5. Biện pháp & ma trận cưỡng chế

### 5.1 Biện pháp

| # | Biện pháp | Nội dung | Đóng đường vòng |
|---|---|---|---|
| **`IC-1`** | **`SET LOCAL` là hình thức DUY NHẤT** | ⛔ Cấm `SET app.current_tenant` và `set_config(..., false)` ở **mọi nơi** trong codebase | `BP-1` |
| **`IC-2`** | **Mọi truy vấn chạm dữ liệu tenant nằm trong transaction tường minh** | Kể cả read đơn lẻ. ⛔ Không ngoại lệ | `BP-2` |
| **`IC-3`** | **Đúng một đường chạm `public.job`** | `claimJobAndBindTenant()`; giữa CLAIM và `SET LOCAL` ⛔ không statement nào khác | `BP-3`, `BP-4`, `BP-6` |
| **`IC-4`** | ⛔ **Không `BYPASSRLS`, không policy xuyên tenant trên bảng nghiệp vụ** | Áp cho **mọi** role ứng dụng, gồm cả role chạy cron | `BP-4`, `BP-5`, `BP-13`, `BP-14` |
| **`IC-5`** | ⭐ **Signed URL chỉ ký cho key ĐỌC RA TỪ DB dưới RLS** | ⛔ Không endpoint nào nhận `key` từ client rồi ký. Kèm điều 3–6 của [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) | `BP-7a`, `BP-7d` |
| **`IC-6`** | **URL/khoá/token ⛔ không lọt vào log** | Cùng quy tắc che với `C-4` của [Spec-Security-Threat-Model](./Spec-Security-Threat-Model.md) | `BP-7b` |
| **`IC-7`** | **Phản hồi ⛔ không phân biệt *"không tồn tại"* với *"không thuộc về bạn"*** | Chặn `0 row` trở thành oracle | `BP-8` |
| **`IC-8`** | **ID nghiệp vụ trong JSONB phải resolve trong cùng transaction có context trước khi ghi** | ⛔ Không tin một ID chỉ vì nó nằm trong tài liệu JSON | `BP-9` |
| **`IC-9`** | **`tenant_id` và role tra từ `membership` mỗi request** | ⛔ Claim của vendor ⛔ không bao giờ là nguồn sự thật | `BP-10` |
| **`IC-10`** | ⚠️ **Whitelist ngoại lệ là danh sách HẰNG SỐ, kèm comment** | Đúng một phần tử `generation.visual_vocabulary`; ⛔ ⛔ **không** nới thành *"bỏ qua bảng không có `tenant_id`"*; ⭐ thêm phần tử thứ hai **phải qua ADR** | `BP-11` |
| **`IC-11`** | **Role ứng dụng ⛔ không có DDL và ⛔ không là owner của bảng nào** | Hệ quả dẫn xuất của `D7`; phải **kiểm bằng test**, ⛔ không bằng niềm tin | `BP-12` |
| **`IC-12`** | **Hai đường xoá tách biệt; xoá object chỉ qua đường đặc quyền** | ⛔ Không gộp takedown với hard-delete | `BP-15` |
| ⭐ **`IC-13`** | ⭐⭐ **Đặc quyền XUYÊN TENANT ở tầng ứng dụng phải là một REGISTRY đếm được** | Sinh ra vì `W-2` (đối chiếu `pg_policies`/`pg_roles`) **MÙ** với đặc quyền sống ở tầng ứng dụng — mà `BP-16` chính là loại đó. (a) Mọi route xuyên tenant đi qua **đúng một** hàm uỷ quyền dùng chung. (b) Danh sách route đó là **hằng số trong repo**, đối chiếu ở CI **HAI CHIỀU**: route trong tiền tố quản trị mà ⛔ không gọi hàm ⇒ **CI đỏ**; route gọi hàm mà ⛔ không có tên trong hằng số ⇒ **CI đỏ**. ⭐ Một chiều chỉ bắt lỗi **quên**, ⛔ không bắt lỗi **thêm lén**. (c) ⛔ Danh tính operator ⛔ **không bao giờ** từ claim vendor (`IC-9`), ⛔ **không** là một cấp của `membership`. Chuẩn tắc đầy đủ = `C-13` của [Spec-Security-Threat-Model](./Spec-Security-Threat-Model.md) | `BP-16` |
| ⚠️ **`IC-14`** | **Đặc quyền của lần ghi đầu `public."user"` là một điểm RIÊNG, hẹp, và DỪNG ngay sau bước đó** | ⛔ **Không** nới `PS-1` sang chiều ghi; ⛔ không `BYPASSRLS`; ⛔ không owner; hẹp tới **một bảng, một hành vi**; idempotent theo `UNIQUE(external_auth_id)`; ⭐ đặc quyền **⛔ không sống tiếp** trong phần còn lại của request | `BP-17` |

### 5.2 Ma trận cưỡng chế — mỗi biện pháp phải quy về DB / lint / test

| Phép kiểm | Loại | Nó bắt gì | Chủ |
|---|---|---|---|
| ⭐ **`M1-1`** — seed 2 tenant A/B; **mọi** query dưới session A trả **0 row** thuộc B | **Test** — ⭐ **DoD nhị phân toàn cục** | Toàn bộ trục cô lập. ⛔ **Không** phải *"đã thêm `tenant_id` cho N/M bảng"* | Engineer; phạm vi bảng do **Architect lô DB Schema** đóng |
| Insert row nghiệp vụ thiếu `tenant_id` ⇒ **DB từ chối ở tầng constraint** | Test | `BP-12` | Engineer |
| Session không set (hoặc set sai) context ⇒ **`0 row`, fail-closed**, ⛔ không lỗi 500 | Test | `BP-2` | Engineer |
| Hai tenant xen kẽ trên cùng pool ⇒ ⛔ không rò context | Test | `BP-1` | Engineer |
| `W-1` — truy vấn nghiệp vụ **ngay sau CLAIM, trước `SET LOCAL`** ⇒ `0 row` | Test | `BP-4` | Engineer |
| `W-2` — `pg_roles.rolbypassrls = false` cho `app_worker`; `pg_policies` **khớp hằng số trong repo** | Test CI | `BP-4`, `BP-5` | Engineer |
| `W-2b` — tenant có `N` job in-flight ⇒ CLAIM trả **0 job** của tenant đó | Test | `BP-5` | ⚠️ Chạy được **sau khi `T-6` đóng** |
| `W-3` — lint rule: ⛔ mọi truy vấn trực tiếp vào `public.job` ngoài `claimJobAndBindTenant()` ⇒ CI đỏ | Lint CI | `BP-3`, `BP-6` | Engineer |
| `W-4` — sau `COMMIT`/`ROLLBACK`, `public.current_tenant_id()` trả `NULL` trên chính connection đó | Test | `BP-1` | Engineer |
| grep/lint: ⛔ ⛔ không có `SET app.current_tenant` và `set_config(..., false)` trong codebase | Lint CI | `BP-1` | Engineer |
| ⭐ Catalog: **`0` bảng CÓ `tenant_id` mà THIẾU policy**, cộng **hai danh sách đóng**: (a) allowlist bảng **có policy mà không có `tenant_id`** (`public.tenant`, `public."user"` — bị bảo vệ **chặt hơn** mức tối thiểu) · (b) whitelist `IC-10` bảng **không `tenant_id` và không policy** (`generation.visual_vocabulary`, guardrail thay thế là quyền ghi) | Test CI | `BP-11`, `BP-12`. ⚠️ Viết phép đo dạng *"số bảng trong `pg_policies` bằng đúng số bảng có `tenant_id`"* sẽ **báo đỏ oan** — cách đọc đúng ở [DB-Entity-Tenancy](../Schema/DB-Entity-Tenancy.md) | Engineer |
| Catalog: **0 index** có `tenant_id` không phải cột đầu | Test CI | `BP-12` | Engineer |
| Catalog: ⛔ **không** role ứng dụng nào là owner của bảng nghiệp vụ; ⛔ không role ứng dụng nào có DDL | Test CI | `BP-12b` | Engineer |
| Catalog: ⛔ không cột kiểu binary nào trong bốn schema (`B-4` của [`SDD` §4.1](../Architecture/SDD-Comic-Studio.md)) | Test CI | Giữ bytes ảnh **ngoài** DB | Engineer |
| grep log của bộ test tích hợp: ⛔ không mẫu signed URL / khoá / token | Test CI | `BP-7b` | ⭐ **Chưa có** — file này chốt yêu cầu |
| Request tài nguyên tenant khác **và** tài nguyên không tồn tại ⇒ **cùng một** phản hồi | Test | `BP-8` | ⭐ **Chưa có** — file này chốt yêu cầu |
| `UPDATE`/`DELETE` trực tiếp một dòng `change_log`/`usage_event` ⇒ **bị từ chối ở tầng DB** | Test | Bảo vệ `A-2` (`GR-3`) | Đã có chủ ở [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) / [ADR-018](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) |
| ⭐ **Registry route xuyên tenant khớp hằng số repo — HAI CHIỀU** (`IC-13b`) | Lint + Test CI | `BP-16` — ⭐ **phần mà `W-2` ⛔ không nhìn thấy** | ⭐ **Chưa có** — file này chốt yêu cầu; ⛔ chạy được **sau khi** PM lands ripple `SDD` §7.4 |
| ⭐ Test: định danh tenant hợp lệ nhưng ⛔ **không** phải operator gọi `TD-2`/`TD-3` ⇒ **`403`**; và operator gọi ⇒ ⛔ **không** thấy bảng nghiệp vụ nào | Test | `BP-16` | ⭐ **Chưa có** |
| ⭐ Test cấu hình: ⛔ ⛔ **không** connection string nào của process `api` trỏ tới **role owner**; `pg_roles.rolbypassrls = false` cho **mọi** role ứng dụng *(gồm `app_operator` khi nó tồn tại)* | Test CI | `BP-16`, `BP-17` — chặn đường lui owner | ⭐ **Chưa có** — mở rộng của `W-2` |
| ⚠️ Test: sau bước ghi dòng `public."user"` đầu tiên, một truy vấn nghiệp vụ trên cùng session ⇒ **`0 row`** *(đặc quyền ⛔ không sống tiếp)* | Test | `BP-17` (`IC-14`) | ⭐ **Chưa có** — ⛔ viết được **sau khi** Architect chốt cơ chế |

> [!WARNING]
> ⚠️ **BỐN điều ⛔ không được nới, dù bảng test đỏ**:
> 1. ⛔ **Không nới quyền role** để làm một test xanh — `BP-4` mô tả chính xác cái bẫy đó.
> 2. ⛔ **Không nới whitelist `IC-10`** thành quy tắc chung — `BP-11`.
> 3. ⛔ **Không chạy đường operator dưới role owner** *"vì nó đã có sẵn quyền"* — `BP-16`.
> 4. ⛔ **Không nới `PS-1` sang chiều GHI** để giải bế tắc lần ghi đầu `public."user"` — `BP-17`.

> [!CAUTION]
> ⭐⭐ **Ranh giới thành thật của `M1-1`, ⛔ phải đọc cùng bảng trên.**
> `M1-1` seed hai tenant A/B rồi khẳng định **mọi** query dưới session A trả **`0 row` thuộc B**. ⇒ Nó chỉ đo được trên **bảng có `tenant_id`**.
> ⚠️ ⛔ `public.takedown_request` ⛔ **không có `tenant_id`** ⇒ `BP-16` nằm **NGOÀI phạm vi của DoD**. ⛔ **Đừng đọc *"`M1-1` xanh"* thành *"⛔ không còn đường xuyên tenant nào"*** — đó đúng là kiểu đọc mà [ADR-010 `D8`](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) dựng `M1-1` lên để chống, chỉ khác chiều.

---

## 6. Nghĩa vụ pháp lý — phần thuộc file này

| # | Nghĩa vụ | Góc cô lập — phần file này sở hữu | Phần thuộc file khác |
|---|---|---|---|
| **`L-1`** | Năm hạng mục provenance trên **mọi** generation | `change_log`, `field_provenance`, `usage_event` **mang `tenant_id` và có RLS** (`GR-5`) ⇒ bằng chứng của hai tenant ⛔ không trộn. ⚠️ Đây cũng là lý do chúng phải nằm **cùng một database** | Hình dạng cột + lineage: [ADR-017 `Q1`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md), lô DB Schema |
| **`L-2`** | Ba bảng bằng chứng commit **cùng một transaction** với artifact | ⭐ Cô lập ⛔ **không được phá `KC-4`**: cả ba `INSERT` nằm **sau** bước `SET LOCAL`, trong **cùng** transaction đã có context ⇒ ⛔ không mâu thuẫn. ⚠️ Và ngược lại: bất kỳ đề xuất tách DB thứ hai nào **phá `KC-4` trước khi phá cô lập** — mà một database cũng chính là điều kiện để RLS còn giá trị | Chuẩn tắc `KC-4`: [ADR-017 `Q4.1`–`Q4.6`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md). ⛔ File này ⛔ không cấp `UPDATE`/`DELETE` cho role ứng dụng trên hai bảng append-only |
| **`L-3`** | Kiểm opt-out Điều 37b tại ingest, log kèm timestamp | Góc cô lập: bảng log opt-out mang `tenant_id`; prefix `incoming/` **thuộc tenant** ⇒ dữ liệu chưa kiểm ⛔ không bao giờ nằm ở vùng dùng chung | Cơ chế stage + bốn kênh: [Spec-Security-Threat-Model](./Spec-Security-Threat-Model.md) `C-1` + `Spec-Security-Legal-Compliance.md` |
| **`L-4`** | Checklist safe harbour Điều 198b | ⭐ Góc cô lập — **HAI** bề mặt ngoài mô hình RLS, ⛔ đừng gộp: **(i)** `AS-2` là ngoại lệ duy nhất của bề mặt **CÔNG KHAI** — role `app_public_intake` chỉ `INSERT` (`BP-14`); **(ii)** ⭐ `AS-13` là bề mặt **OPERATOR xuyên tenant** — cùng một nghĩa vụ `L-4` (đánh giá đơn + thi hành trong 72h) **đẻ ra** nó, và nó ⛔ **chưa có cơ chế** (`BP-16`). ⚠️ Và **disable-access là cờ CẤP PROJECT — nằm BÊN TRONG một tenant**, ⛔ **không** phải một ranh giới tenant: ⛔ đừng nhầm hai lớp | Checklist, đăng ký đầu mối, SLA 72h: [Spec-Security-Legal-Compliance](./Spec-Security-Legal-Compliance.md). ⭐ Phương án `TD-Q1` + ripple `SDD` §7.4: [Spec-Security-Threat-Model §4.5](./Spec-Security-Threat-Model.md) |
| **`L-5`** | Đánh dấu nội dung AI bằng định dạng máy đọc | ⛔ Không thuộc trục cô lập | [Spec-Security-Threat-Model](./Spec-Security-Threat-Model.md) `TM-F6-5` + `Spec-Security-Legal-Compliance.md` |
| **`L-6`** | Cơ chế để user biết đang tương tác với AI | ⛔ Không thuộc trục cô lập | như trên |
| **`L-7`** | ⭐ **Đường hard-delete toàn bộ dữ liệu tenant phải tồn tại và đã kiểm thử** | ⭐ **Đây là nghĩa vụ pháp lý sở hữu bởi file này**: kỷ luật `ON DELETE CASCADE` trên **mọi** FK · xoá object theo **prefix `tenant/{tenant_id}/`** (chính key schema làm việc này khả thi) · đường xoá là **đặc quyền riêng**, `api`/`worker` ⛔ không có `DeleteObject` · ⛔ **tách biệt tuyệt đối** khỏi soft-delete của `L-4`. Chỗ dễ sót nhất: **nhóm bảng Story Bible**. Xem `BP-15` | Retention/purge và dữ liệu trong backup: `T-23` (**PM + luật sư SHTT**), `T-9` (**Founder + dev**) |

> ⭐ **Một ràng buộc pháp lý ẩn trong quyết định kỹ thuật**: ⛔ **KHÔNG dedup chéo tenant** ⛔ không phải để tiết kiệm gì — nó là **lựa chọn có động cơ pháp lý**: dedup tạo một object dùng chung giữa **hai chủ thể pháp lý khác nhau** và mâu thuẫn trực tiếp với lập luận bản quyền. ⚠️ Đây là chỗ **sẽ có người muốn "tối ưu" lại khi nhìn hoá đơn lưu trữ** — hai object, hai key, **hai lần trả tiền** là chi phí **có chủ ý**.

---

## 7. Ma trận `KC-1`…`KC-7`

| `KC` | Neo | Soi ở đâu trong file này | Thuộc file nào (nếu không phải file này) |
|---|---|---|---|
| **`KC-1`** — chuỗi lineage | `SRS-FR-34` | `L-1` — lineage của hai tenant ⛔ không trộn được vì bảng mang `tenant_id` + RLS (`GR-5`) | Hình dạng chuỗi: [ADR-017 `Q1`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md). Mối đe doạ tampering: [Spec-Security-Threat-Model](./Spec-Security-Threat-Model.md) |
| **`KC-2`** — `change_log` mọi hành động | `SRS-FR-35` | `L-1`, `L-2`; và `BP-13` — cron ghi `change_log` **ngoài context** là đường làm bẩn dòng audit | Phạm vi ghi + middleware: [ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| **`KC-3`** — `field_provenance` + `origin` | `SRS-FR-36` | `L-1` — cùng lập luận `GR-5` | [ADR-017 `Q3`, `Q5`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| **`KC-4`** — một-transaction-boundary | `SRS-NFR-13` | `L-2` — ⭐ cô lập và `KC-4` **không mâu thuẫn**: ba `INSERT` nằm **sau** `SET LOCAL` trong cùng transaction. ⛔ File này ⛔ **không** viết *"tầng DB cưỡng chế `KC-4`"* | Chuẩn tắc: [ADR-017 `Q4`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md). Thứ tự vòng đời: `P-7`, lô DB Schema |
| **`KC-5`** — `tenant_id` + RLS mọi bảng | `SRS-NFR-01` | ⭐ **File này SỞ HỮU `KC-5`**: [§2](#2-tài-sản--bề-mặt-tấn-công-của-trục-cô-lập), [§3](#3-stride-trên-bảy-luồng-f1f7--góc-cô-lập), toàn bộ [§4](#4--catalog-đường-vòng-bp-1bp-17), ma trận cưỡng chế [§5.2](#52-ma-trận-cưỡng-chế--mỗi-biện-pháp-phải-quy-về-db--lint--test). DoD = `M1-1` | Danh sách bảng để `M1-1` phủ hết: **Architect, lô DB Schema** |
| **`KC-6`** — opt-out check tại ingest | `SRS-FR-37` | Chỉ góc cô lập: `L-3` — log mang `tenant_id`, prefix `incoming/` thuộc tenant | ⭐ **Sở hữu bởi [Spec-Security-Threat-Model](./Spec-Security-Threat-Model.md)** (`TM-F1-1`, `C-1`) |
| **`KC-7`** — credit ledger + HOLD + reaper | `SRS-FR-28` | Góc cô lập **duy nhất**: bảng ledger là bảng nghiệp vụ ⇒ chịu **đủ ba nghĩa vụ** (`tenant_id NOT NULL` · cột đầu index · RLS) ngay từ khi **reserve chỗ**, ⛔ không retrofit; và `CHECK (available >= 0)` ở tầng DB. ⚠️ `[OoH]` MVP3 ⇒ ⛔ **không HOLD ở MVP1–MVP2** | ⭐ Góc chống lạm dụng chi phí (rate limit **đếm request, ⛔ không đếm tiền**) và `T-25`: [Spec-Security-Threat-Model](./Spec-Security-Threat-Model.md). Ledger/reaper: lô DB Schema + [ADR-018](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) |

---

## 8. Bảng `TBD` của file này

> ⛔ **Mục này ⛔ KHÔNG đóng hàng nào.**

| # | Việc còn mở | Ai đóng | Khi nào |
|---|---|---|---|
| ~~`P-3`~~ | ~~Policy RLS cho `tenant` / `user` / `membership` / `takedown_request`~~ | ✅ **ĐÃ ĐÓNG** — [DB-Entity-Tenancy](../Schema/DB-Entity-Tenancy.md) + [DB-Entity-Compliance-And-Takedown](../Schema/DB-Entity-Compliance-And-Takedown.md) | — |
| `P-4` | Chi phí thực thi hàm helper `public.current_tenant_id()` | **Engineer** | Khi có bộ test tải đầu tiên |
| `D4.5` | Verify CTE + `set_config` một statement (khoảng hở `= 0`) | **Engineer** | MVP1, bằng test thật. ⛔ Chưa PASS ⇒ ⛔ không được giả định |
| `T-6` | `N` của `in_flight_per_tenant` (`BP-5`, `W-2b`) | **PM + Architect** | Sau MVP0 đo tải thật |
| `T-7` | TTL signed URL (`BP-7c`) | **Dev đề xuất, Founder duyệt** | MVP1 |
| **queue khác** | Tải chạy **ngoài `public.job`** (rollup, golden dataset regression, hold reaper) lấy tenant context bằng cách nào (`BP-13`) — ⚠️ ⛔ **không** thừa hưởng `D4.2` vì ⛔ không qua `public.job` | ⭐ **Architect, lô DB Schema** | Khi đặc tả các bảng rollup |
| **`M1-1` scope** | Danh sách đầy đủ bảng nghiệp vụ (`BP-12`) | **Architect, lô DB Schema** + [ADR-005](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) | Trước khi lô DB Schema được duyệt |
| **mới** | Hình dạng ràng buộc cho **ID nghiệp vụ nằm trong JSONB** (`BP-9`, `IC-8`) | **Architect, lô DB Schema** | Khi đặc tả bảng mang `JSONB` |
| **mới** | Ràng buộc *"⛔ không endpoint nào ký URL cho key do client gửi"* + tính không đoán được của `upload_id` (`BP-7a`, `BP-7d`, `IC-5`) | **Architect, lô API** | Trước khi `Endpoint-*` đầu tiên được duyệt |
| `T-9` | RPO/RTO/backup retention (`BP-15c`) | **Founder + dev** | Sau MVP0 |
| `T-23` | `b-3` retention nghiệp vụ (`BP-15c`) | ⭐ **PM + luật sư SHTT** | Cùng gói `SRS-NFR-17` |
| `T-24` | `b-4` dữ liệu cá nhân trong `takedown_request` (`BP-14`) | ⭐ **PM + luật sư SHTT** | Cùng gói `SRS-NFR-17` |
| `T-22` | Nghĩa vụ lưu trữ dữ liệu trong lãnh thổ Việt Nam | ⭐ **PM + luật sư SHTT** | Trước khi có khách trả tiền |
| `T-16` | `b-1` mã hoá + secret · `b-7` observability — ⚠️ ⛔ không có `b-7` thì `BP-2` **không phát hiện được** | **Dev** | Sau khi platform được mua |
| `T-27` | `b-2` BYOK key | ⭐ **Architect + Founder** (PM gán, `E22`) — ⛔ cần **ADR mới**, ngoài phạm vi run Phase 2 ⇒ **nợ kỹ thuật số 1** | Trước khi seam BYOK bật |
| ⭐ **mới** | ⭐⭐ **Ba ripple mở băng Architecture cho `app_operator`** (`BP-16`): [`SDD` §7.4](../Architecture/SDD-Comic-Studio.md) *"bốn DB role"* ⇒ **năm** · [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) thêm carve-out cạnh `D6` · `W-2` mở rộng đối chiếu role mới. ⚠️ ⛔ **Phương án ĐÃ CHỐT** ([Spec-Security-Threat-Model §4.5](./Spec-Security-Threat-Model.md)) nhưng ⛔ **chưa gỡ chặn** | ⭐ **PM** điều phối, **Architect** thực hiện | ⭐ **Trước** khi `TD-2`/`TD-3` được triển khai |
| ⭐ **mới** | **Cơ chế uỷ quyền operator ở tầng ứng dụng** + registry `IC-13` (`BP-16`) | **Architect + Engineer**; ràng buộc hình dạng do file này chốt | Cùng lúc với `app_operator` |
| ⚠️ **mới** | ⛔ **Cơ chế đặc quyền cho lần GHI đầu tiên dòng `public."user"`** (`BP-17`, `IC-14`) — ⛔ **không** phủ bởi `D6`; `D3` chỉ ĐỌC. ⛔ File này ⛔ **không chọn** nhánh webhook hay JIT — đó là quyết định của Architect | ⭐ **Architect**, đối chiếu `Spec-Integration-Auth-Provider.md` `AUTH-E3` với file này | **Trước** request đã xác thực đầu tiên |
| ⭐ **mới** | ⚠️ **`M1-1` ⛔ không phủ `BP-16`** — bảng ⛔ không có `tenant_id` thì DoD ⛔ không biểu diễn được *"dòng thuộc tenant B"*. Cần một phép đo **riêng** cho bề mặt xuyên tenant | **Architect + Engineer**, cùng hàng **`M1-1` scope** | Trước khi lô DB Schema được duyệt |

---

## 9. Tài liệu tham khảo

**Kiến trúc** — [SDD-Comic-Studio](../Architecture/SDD-Comic-Studio.md) (§4.1 bốn đường ranh giới · §4.2 ràng buộc tầng DB · §5 luồng `F1`–`F7` · §6.1 tenant context & RLS · §7.4 bốn DB role · §9 bảng `TBD`) · [ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) · [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) · [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) · [ADR-005](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) · [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-009](../Architecture/ADR-009-Modular-Monolith-Three-Schemas.md) · [ADR-010](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) · [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) · [ADR-018](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md)

**Requirements** — [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) (`SRS-NFR-01`, `SRS-NFR-05`, `SRS-NFR-13`, `SRS-NFR-20`, `SRS-FR-02`, `SRS-FR-25`, `SRS-FR-26`, `SRS-FR-38` · §5.2 hàng `b-1`…`b-7`)

**Security** — [Spec-Security-Threat-Model](./Spec-Security-Threat-Model.md) *(⭐ `§4.5` — câu trả lời `TD-Q1`; `C-11`, `C-13`)* · [Spec-Security-Legal-Compliance](./Spec-Security-Legal-Compliance.md) *(lô L19 — ✅ đã viết xong)*

**API** *(⛔ chỉ đọc — file này ⛔ không sửa một dòng nào của tầng API)* — [Endpoint-Takedown-Public](../API/Endpoint-Takedown-Public.md) (`TD-1`…`TD-3`, `TD-Q1`) · [Endpoint-Tenancy](../API/Endpoint-Tenancy.md) (`API-TN-5` — lần ghi đầu `public."user"`) · [Endpoint-Project](../API/Endpoint-Project.md) (`API-PRJ-4`)

**Schema** — [DB-Entity-Tenancy](../Schema/DB-Entity-Tenancy.md) · [DB-Entity-Compliance-And-Takedown](../Schema/DB-Entity-Compliance-And-Takedown.md) · [DB-Entity-Job-Queue](../Schema/DB-Entity-Job-Queue.md) · [DB-Entity-Prompt-Vocabulary](../Schema/DB-Entity-Prompt-Vocabulary.md)

---

_Created by security-auditor_
_Author: trisjr_
