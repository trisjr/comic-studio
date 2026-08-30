---
id: SPEC-API-TENANCY
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Endpoint: Tenancy

Bề mặt API của ba entity định danh — `public.tenant`, `public."user"`, `public.membership`. ⭐ **Auth là dịch vụ MUA NGOÀI** ⇒ phần lớn file này là **ánh xạ + callback**, ⛔ **không** phải CRUD tự viết một hệ thống định danh.

**Serves:** [UC-01 — Upload And Ingest Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) (điều kiện tiên quyết: mọi request cần tenant context) · nền tảng cho **toàn bộ 10 UC trong phạm vi**

**Nguồn ràng buộc** (⛔ file này **không** đặc tả lại, chỉ trỏ theo mã):

| Ràng buộc | Nguồn duy nhất |
|---|---|
| Trình tự bơm tenant context, hàm `SECURITY DEFINER` phân giải `user → tenant` | ⭐ [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |
| Policy RLS cụ thể cho ba bảng định danh | [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md) mục RLS Policy |
| Ta chỉ giữ **ánh xạ**, ⛔ không sở hữu định danh | [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) |
| Hành vi fail-closed khi ⛔ không có context | [ADR-010 `D9`](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) |
| `change_log` cùng transaction (`KC-4`) | [ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| Rate limit per tenant cho `upload` và `generate` | [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md) `RL-1`…`RL-4` |

---

## ⭐ Hai bề mặt, ⛔ không phải một

> [!IMPORTANT]
> Bốn endpoint đầu là **đường API có session người dùng** ([ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)). Endpoint thứ năm — **webhook của vendor auth** — ⛔ **không** có session người dùng và ⛔ **không** có tenant context. Hai bề mặt này có **threat model khác nhau**; ⛔ đọc chúng như một là chỗ sinh lỗ hổng.

| Bề mặt | Ai gọi | Xác thực bằng | Tenant context |
|---|---|---|---|
| `E-TN-1`…`E-TN-4` | Trình duyệt của người dùng | Session do vendor auth phát | ✅ có, bơm bằng `SET LOCAL` |
| `E-TN-5` (webhook) | ⭐ **Vendor auth**, server-to-server | **Chữ ký của vendor**, ⛔ không phải session | ⛔ **KHÔNG có** — xem [`API-TN-5`](#invariant-của-resource) |

---

## Danh sách endpoint

| # | Method · Path | Mục đích |
|--:|---|---|
| `E-TN-1` | `GET /v1/me` | ⭐ Endpoint **duy nhất** chạy **trước khi** tenant context tồn tại |
| `E-TN-2` | `GET /v1/tenants/{tenant_id}` | Đọc thông tin tenant hiện tại |
| `E-TN-3` | `GET /v1/tenants/{tenant_id}/members` | Liệt kê thành viên |
| `E-TN-4` | `POST /v1/tenants/{tenant_id}/members` | Tạo một `membership` cho `user` **đã tồn tại** |
| `E-TN-5` | `POST /v1/webhooks/auth` | ⚠️ **CÓ ĐIỀU KIỆN** — callback vendor auth, đồng bộ ánh xạ `external_auth_id → public."user"`. Xem [cảnh báo ở `E-TN-5`](#e-tn-5--post-v1webhooksauth--️-có-điều-kiện) |

---

### `E-TN-1` · `GET /v1/me`

| | |
|---|---|
| **Auth** | Session do vendor auth phát ⇒ có `external_auth_id` |
| **Request** | ⛔ Không param |
| **Response `200`** | `{ user: { id, external_auth_id }, tenant: { id, display_name }, membership: { id, created_at } }` |

> ⭐ **Đây là endpoint duy nhất của hệ thống chạy khi tenant context CHƯA tồn tại.** Vòng lặp *"cần tenant context để đọc `membership`, mà phải đọc `membership` mới biết tenant"* đã có **đúng một** lời giải: hàm `SECURITY DEFINER` hẹp nhận `user_id` và trả **duy nhất** `tenant_id` ([ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)). ⛔ File này **không** đặc tả lại sáu bước của middleware.

- ⛔ **⛔ TUYỆT ĐỐI không giải bằng cách tắt RLS hay cấp `BYPASSRLS`** cho đường đăng nhập. Hàm đó là **một trong ba điểm đặc quyền đếm được** của toàn hệ thống và phải được review như code bảo mật.
- ⛔ Handler ⛔ **không** truy vấn thẳng `public."user"` khi chưa có context — policy của bảng đó dựa trên `membership`, nên truy vấn thẳng sẽ trả `0 row` và bị đọc nhầm thành *"user không tồn tại"*.
- ⛔ **Không có endpoint đổi tenant (`switch tenant`)** ở horizon này: ⛔ không nguồn nào yêu cầu, và quan hệ hiện là 1:1. ⚠️ `membership` tồn tại như entity riêng **từ đầu** chính là để ngày mở gói team ⛔ không phải migrate FK nghiệp vụ.
- `E-TN-1` là **read-only** ⇒ ⛔ không sinh `change_log`.

| Mã lỗi | Khi nào |
|---|---|
| `401` | ⛔ Không có session hợp lệ từ vendor |
| ⚠️ `404` | ⚠️ **CHỈ tồn tại ở nhánh (a) webhook** của [`E-TN-5`](#e-tn-5--post-v1webhooksauth--️-có-điều-kiện): `external_auth_id` hợp lệ nhưng dòng `public."user"` ⛔ **chưa tới**. Client xử lý như *"đang khởi tạo tài khoản"*, ⛔ **không** tự tạo user thay. ⭐ **Ở nhánh (b) JIT provisioning, mã này ⛔ KHÔNG BAO GIỜ phát ra**: `AUTH-E3` chốt tình huống này là **bình thường** ⇒ middleware tạo dòng **idempotent** dựa trên `UNIQUE(external_auth_id)` (hai request đồng thời ⇒ một thắng, một **bắt lỗi unique rồi đọc lại**; ⛔ không *"check-rồi-insert"*) rồi **đi tiếp** |
| ⭐ `409` `no_membership` | ⭐ User tồn tại nhưng ⛔ **không có `membership` nào** ⇒ ⛔ **không phân giải được tenant**. ⚠️ Đây là **trạng thái HỢP LỆ, transient** (`INV-T-4`), ⛔ không phải lỗi hệ thống — ⛔ đừng trả `500` |

---

### `E-TN-2` · `GET /v1/tenants/{tenant_id}`

| | |
|---|---|
| **Auth** | Session + tenant context |
| **Request** | Path: `tenant_id` |
| **Response `200`** | `{ id, display_name, created_at, updated_at }` |

- ⚠️ **⛔ Response ⛔ KHÔNG có `status` / `is_deleted` / `plan` / `tier`** — ⛔ không phải bị lược, mà vì **bảng ⛔ không có các cột đó**: hard-delete là **xoá cứng** (⛔ không có trạng thái *"đã xoá"* để trả), soft-delete là ngữ nghĩa của **takedown ở cấp PROJECT**, và ba tầng giá ⛔ chưa mở (`D-62`).
- ⭐ Truyền `tenant_id` khác tenant hiện tại ⇒ RLS trả `0 row` ⇒ **`404`**, ⛔ không `403`. ⚠️ `0 row` ở đây là **fail-closed**, ⛔ không phải *"không có dữ liệu"*.

| Mã lỗi | Khi nào |
|---|---|
| `404` | `tenant_id` ⛔ không phải tenant hiện tại (hoặc ⛔ không tồn tại) |

---

### `E-TN-3` · `GET /v1/tenants/{tenant_id}/members`

| | |
|---|---|
| **Auth** | Session + tenant context |
| **Request** | Path: `tenant_id` |
| **Response `200`** | `{ members: [ { membership_id, user_id, external_auth_id, created_at } ] }` |

- ⭐ **Mảng rỗng là kết quả HỢP LỆ, ⛔ không phải lỗi** (`INV-T-4`) — một tenant vừa tạo, chưa có membership, là trạng thái transient hợp lệ.
- ⚠️ **⛔ Response ⛔ KHÔNG có `role`** — cột đó ⛔ **không tồn tại** ở horizon này (SSO + team nhiều thành viên có role là hàng `E8`, hoãn tới Full Scope).
- ⚠️ **⛔ Response ⛔ KHÔNG có `email`, tên hiển thị, avatar.** Danh sách trường đồng bộ từ vendor còn `TBD`, và thêm một trường dữ liệu cá nhân là **tạo nghĩa vụ mà ⛔ chưa ai xác định**.
- ⭐ Bảng `public."user"` ⛔ **không có `tenant_id`** ⇒ policy của nó dựa trên `EXISTS(membership)`; ⇒ endpoint này chỉ thấy user **có membership trong tenant hiện tại** — đúng ý định, ⛔ không phải giới hạn cần nới.

| Mã lỗi | Khi nào |
|---|---|
| `404` | `tenant_id` ⛔ không phải tenant hiện tại |

---

### `E-TN-4` · `POST /v1/tenants/{tenant_id}/members`

| | |
|---|---|
| **Auth** | Session + tenant context |
| **Request** | `{ user_id }` — ⭐ khoá **nội bộ** của ta, ⛔ **không** phải `external_auth_id` |
| **Response `201`** | `{ membership_id, user_id, tenant_id, created_at }` |

> [!WARNING]
> ⚠️ **Endpoint này ⛔ KHÔNG phải luồng invite.** [Story-Tenant-User-Membership-As-Three-Entities](../../022-User-Stories/Backlog/Story-Tenant-User-Membership-As-Three-Entities.md) loại **tường minh**: ⛔ *"không xây luồng invite user vào tenant hay đổi role"*. ⇒ Ở horizon này nó là **thao tác tạo ánh xạ cho một `user` ĐÃ TỒN TẠI**, dùng bởi đường onboarding/provisioning — ⛔ **không** gửi email, ⛔ **không** sinh token mời, ⛔ **không** có trạng thái *"đang chờ chấp nhận"*.

- ⛔ **⛔ Không nhận trường `role`** — cột ⛔ không tồn tại. Gửi kèm ⇒ `422`, ⛔ không bỏ qua im lặng.
- ⛔ **⛔ Không nhận `external_auth_id`** để *"tạo user nếu chưa có"*. Tạo dòng `public."user"` là việc của `E-TN-5`. Hai đường tạo cho một entity là hai nguồn sự thật.
- Sinh **một** `public.change_log` row cùng transaction ([ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)) với ⭐ `action_type = 'create_membership'` — giá trị **đã có** trong danh mục đóng ([`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md), lô Schema `L28b`). ⚠️ Mỏ neo của giá trị đó là **chính đường ghi `E-TN-4` này**, ⛔ **không phải** [Story-Tenant-User-Membership-As-Three-Entities](../../022-User-Stories/Backlog/Story-Tenant-User-Membership-As-Three-Entities.md) — Story đó cố ý ⛔ không xây luồng invite. ⛔ Không tái dụng một giá trị của editor.
- ⛔ **Không có `DELETE` member ở horizon này**: ⛔ không nguồn nào yêu cầu, và việc xoá chạm nghĩa vụ dữ liệu cá nhân đang `TBD`.

| Mã lỗi | Khi nào |
|---|---|
| `404` | `tenant_id` ⛔ không phải tenant hiện tại; hoặc `user_id` ⛔ không thấy dưới RLS |
| ⭐ `409` | ⭐ Cặp `(tenant_id, user_id)` **đã có membership** — `UNIQUE (tenant_id, user_id)` (`INV-T-2`). ⚠️ ⛔ **Không** biến thành `UPSERT`: hai dòng trùng bị **DB** từ chối, và đó là AC đo được |
| `422` | Body chứa `role` hoặc `external_auth_id` |

---

### `E-TN-5` · `POST /v1/webhooks/auth` — ⚠️ CÓ ĐIỀU KIỆN

> [!CAUTION]
> ⚠️⭐ **Sự TỒN TẠI của endpoint này ⛔ CHƯA ĐƯỢC CHỐT — và ⛔ lô này ⛔ không chốt thay.**
> [`Spec-Integration-Auth-Provider.md`](./Spec-Integration-Auth-Provider.md) §3 để **mở** câu hỏi *"có cần webhook auth ở MVP1 hay không"*, và nêu **đường thay thế**: **JIT provisioning** — tạo dòng `public."user"` ngay ở **request đã xác thực đầu tiên** (`AUTH-E3`), ⛔ **không cần webhook**.
> ⇒ **Hai nhánh, ⛔ chỉ một được chọn:**
>
> | Nhánh | Hệ quả cho file này |
> |---|---|
> | **(a) Webhook** | `E-TN-5` là endpoint như đặc tả dưới đây. ⚠️ Kéo theo **một bảng inbox webhook** mà [ADR-005 `G-2`](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) **closed list ⛔ chưa có chỗ** ⇒ phải sửa ADR-005 **trước** |
> | ⭐ **(b) JIT provisioning** | ⛔ **`E-TN-5` ⛔ KHÔNG tồn tại như một route.** Việc tạo dòng `user` là **bước nội bộ của middleware auth** (`AUTH-E3`), ⛔ không phải bề mặt HTTP. ⇒ Resource này còn **4 endpoint**, và `404` của `E-TN-1` ⛔ **không bao giờ** xảy ra |
>
> ⛔ **Đặc tả dưới đây chỉ áp dụng cho nhánh (a).** *Ai đóng*: **Architect + dev**, khi chốt vendor.

| | |
|---|---|
| **Auth** | ⭐ **Chữ ký của vendor auth**, xác minh server-to-server. ⛔ **KHÔNG** session người dùng, ⛔ **KHÔNG** tenant context |
| **Request** | Payload do vendor định dạng; ⭐ trường **duy nhất** ta phụ thuộc là **subject** ⇒ ánh xạ vào `external_auth_id` |
| **Response `200`** | `{ received: true }` — ⚠️ trả **nhanh và ngắn**; ⛔ không tiết lộ trạng thái nội bộ |

- ⭐ **Ta chỉ giữ ÁNH XẠ.** Vendor auth **sở hữu** định danh; `public."user"` ⛔ không phải hệ thống định danh của ta ([ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md)). ⇒ ⭐ **Đổi vendor auth = remap đúng MỘT cột** (`external_auth_id`).
- ⭐ **Idempotent theo `external_auth_id`** — `UNIQUE (external_auth_id)` là chốt cuối. Vendor **sẽ** gửi lại cùng một sự kiện; lần thứ hai ⛔ **không** được tạo dòng thứ hai và ⛔ **không** được trả lỗi cho vendor (vendor sẽ retry vô hạn).
- ⚠️ **⛔ KHÔNG lưu trường dữ liệu cá nhân nào** (email, tên, avatar) cho tới khi danh sách trường đồng bộ được chốt. ⛔ *"Lưu sẵn cho tiện"* là tạo nghĩa vụ chưa ai xác định.
- ⛔ **Webhook này ⛔ KHÔNG tạo `tenant` và ⛔ KHÔNG tạo `membership`.** Nó chỉ tạo/cập nhật ánh xạ user. Provisioning tenant là một quyết định sản phẩm, ⛔ không phải hệ quả của một sự kiện auth.
- ⚠️ **Cơ chế đặc quyền của lần ghi này ⛔ CHƯA ĐÓNG** — xem [`API-TN-5`](#invariant-của-resource) và [`TBD` còn lại](#tbd-còn-lại).

| Mã lỗi | Khi nào |
|---|---|
| `401` | ⭐ Chữ ký vendor ⛔ không hợp lệ. ⚠️ ⛔ **Không** xử lý payload trước khi xác minh chữ ký |
| `400` | Payload thiếu subject |
| `503` | Lỗi tạm thời phía ta ⇒ ⭐ **báo cho vendor RETRY**. ⚠️ ⛔ Không trả `200` để *"cho êm"* — trả `200` khi chưa ghi được là **mất vĩnh viễn** một ánh xạ |

---

## Invariant của resource

| # | Invariant | Neo |
|:--:|---|---|
| `API-TN-1` | ⭐ **Mọi bảng nghiệp vụ phân vùng bằng `tenant_id`, ⛔ KHÔNG bằng `user_id`** ⇒ ⛔ không endpoint nào của hệ thống nhận `user_id` làm khoá phạm vi dữ liệu | `D-11` · `INV-T-5` |
| `API-TN-2` | ⭐ **ID ngoài tenant ⇒ `404`, ⛔ không `403`.** `0 row` là **fail-closed**, ⛔ không phải *"không có dữ liệu"* | [ADR-010 `D9`](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) |
| `API-TN-3` | ⭐ **Vòng lặp `user → tenant` giải bằng ĐÚNG MỘT hàm `SECURITY DEFINER`**, ⛔ không `BYPASSRLS`, ⛔ không tắt RLS, ⛔ không role thứ năm | [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |
| `API-TN-4` | ⛔ **Không endpoint nào của file này trả `role`, `email`, `plan`, `tier`, `status`** — các cột đó ⛔ **không tồn tại** ở horizon này | [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md) |
| ⭐ `API-TN-5` | ⚠️ **`E-TN-5` ghi `public."user"` trên một session ⛔ KHÔNG có tenant context.** ⛔ Carve-out `app_public_intake` của [ADR-006 `D6`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) **⛔ KHÔNG phủ** trường hợp này — nó chỉ cho `INSERT` vào `public.takedown_request`. ⇒ ⛔ **File này ⛔ KHÔNG tự phát minh** một đường đặc quyền thứ tư; nó **phát biểu yêu cầu** và route cơ chế | [ADR-006 `D6`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [`TBD` còn lại](#tbd-còn-lại) |
| `API-TN-6` | ⭐ **Rate limit per tenant** áp cho `upload` và `generate`, đếm **SỐ REQUEST** trong một khung thời gian. ⛔ **Đường rate limit ⛔ không đọc `cost_usd`, ⛔ không đếm `usage_event`, ⛔ không chạm bảng `credit_*`** | `RL-b`, `RL-c`, `INV-T-8` |
| `API-TN-7` | ⛔ **Bộ đếm rate limit ⛔ KHÔNG là entity trong data model** ⇒ ⛔ không endpoint nào đọc/ghi nó, ⛔ không endpoint trạng thái quota. Mất bộ đếm ⇒ mặc định **chặn tạm thời**, ⛔ không bao giờ *"cho phép không giới hạn"* | `RL-1`, `RL-2`, `RL-e` |
| `API-TN-8` | ⛔ **Không endpoint nào của file này là async** — ⛔ không job, ⛔ không polling | [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) |

### ⛔ Bốn thứ KHÔNG nằm ở file này

| ⛔ Không ở đây | Ở đâu |
|---|---|
| Ngưỡng số + cửa sổ của rate limit, và **`429`** khi vượt ngưỡng `generate` | ⚠️ `429` phát ở **chính endpoint `generate`** (`Endpoint-Generation.md`), ⛔ không ở file này. Ngưỡng = `TBD` (`RL-f`) |
| Hard-delete tenant (`SRS-NFR-05`) + export hồ sơ trước khi xoá | ⛔ **Không phải endpoint sản phẩm** — đường vận hành có đặc quyền riêng ([ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 8) |
| Soft-delete / disable-access theo takedown | Cấp **PROJECT**, ⛔ không cấp tenant — `Endpoint-Takedown-Public.md` |
| Cơ chế chi tiết của vendor auth (chữ ký, retry, danh sách trường sync) | `Spec-Integration-Auth-Provider.md` (lô L17) |

---

## UC nào tiêu thụ

| UC · bước | Endpoint |
|---|---|
| **Mọi UC trong phạm vi**, bước đầu tiên của **mọi** request | `E-TN-1` — ⭐ ⛔ không có tenant context thì ⛔ không truy vấn nghiệp vụ nào trả về dòng nào |
| [UC-01](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) bước 1 (tạo/chọn tác phẩm) | Điều kiện tiên quyết: `E-TN-1` xác lập tenant; resource `project` ở `Endpoint-Project.md` |
| Nền tảng của `KC-5` (`tenant_id` trên mọi bảng) | `E-TN-2`, `E-TN-3` |
| Onboarding tài khoản mới | `E-TN-5` → `E-TN-4` → `E-TN-1` |

⚠️ **Phạm vi build**: [Story-Tenant-User-Membership-As-Three-Entities](../../022-User-Stories/Backlog/Story-Tenant-User-Membership-As-Three-Entities.md) và [Story-Tenant-Id-And-RLS-Everywhere](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) **nằm trong 24**; luồng invite/role ⛔ **không**.

---

## `TBD` còn lại

| Khoảng trống | Ai đóng | Khi nào |
|---|---|---|
| ⭐⚠️ **Nhánh (a) webhook hay (b) JIT provisioning** — [`Spec-Integration-Auth-Provider.md`](./Spec-Integration-Auth-Provider.md) §3 để **mở**; ⛔ lô này ⛔ không chọn thay. ⚠️ Nhánh (a) còn kéo theo một **bảng inbox webhook** ⛔ chưa có chỗ trong closed list của [ADR-005 `G-2`](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) | **Architect + dev** | Khi chốt vendor |
| ⭐⚠️ **Cơ chế đặc quyền cho lần GHI dòng `public."user"`** — dù đi nhánh (a) hay (b), lần ghi đó xảy ra khi ⛔ **chưa có** tenant context, mà policy của `public."user"` dựa trên `EXISTS(membership)`. ⚠️ [ADR-006 `D6`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) ⛔ **không** phủ trường hợp này (carve-out `app_public_intake` chỉ `INSERT` `takedown_request`), và hàm `SECURITY DEFINER` của `D3` chỉ **ĐỌC** `user → tenant`, ⛔ không ghi. ⛔ File này ⛔ **không** tự mở một điểm đặc quyền thứ tư | ⭐ **Architect** — đối chiếu [`Spec-Integration-Auth-Provider.md`](./Spec-Integration-Auth-Provider.md) `AUTH-E3` với `Spec-Security-Tenant-Isolation.md`; ⚠️ nếu cần sửa ADR-006 thì PM route lại vì tầng Architecture **đã đóng** ở run này | **Trước** request đã xác thực đầu tiên |
| ~~**`action_type` cho `E-TN-4`**~~ ⇒ ✅ **ĐÃ ĐÓNG** bởi lô Schema **`L28b`**: danh mục mở giá trị **RIÊNG** `create_membership`, mỏ neo là chính đường ghi `E-TN-4` + [ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) ([`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md)). ⇒ `E-TN-4` ⛔ không còn bị chặn bởi hàng này | — (đã đóng) | — |
| **Vendor auth** ⛔ chưa chốt ⇒ hình dạng payload của `E-TN-5` và cách xác minh chữ ký ⛔ chưa cố định | **PM + Architect** ([ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md)) | Khi chốt vendor |
| **Danh sách trường đồng bộ** từ vendor vào `public."user"` | **PM + Architect** | Khi chốt vendor |
| **Ngưỡng số + độ dài cửa sổ** của rate limit (`upload`, `generate`) | **PM / Founder**, sau số đo MVP0 | Trước khi bật cưỡng chế thật |
| Xoá dòng ánh xạ `user` khi ⛔ không còn `membership` — chạm nghĩa vụ **dữ liệu cá nhân** | **PM + luật sư** | Trước khi có người dùng ngoài |

---

## Tài liệu tham khảo

- [ADR-003 — Auth And Billing Vendor Selection](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md)
- [ADR-005 — Platform Table Schema Placement](../Architecture/ADR-005-Platform-Table-Schema-Placement.md)
- [ADR-006 — RLS Tenant Context Injection](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)
- [ADR-010 — Tenant Isolation With RLS](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md)
- [ADR-017 — Provenance Chain And One Transaction Boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)
- [SDD — Comic Studio](../Architecture/SDD-Comic-Studio.md) §6.1, §7.4
- [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md) · [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md)
- [Story-Tenant-User-Membership-As-Three-Entities](../../022-User-Stories/Backlog/Story-Tenant-User-Membership-As-Three-Entities.md) · [Story-Minimum-Abuse-Controls](../../022-User-Stories/Backlog/Story-Minimum-Abuse-Controls.md)
