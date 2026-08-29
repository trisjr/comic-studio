---
id: SPEC-API-TAKEDOWN-PUBLIC
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Endpoint: Takedown (public intake + operator triage)

Đặc tả **ba endpoint** của resource `takedown_request` — bề mặt tiếp nhận yêu cầu hạ nội dung theo **Điều 198b** và đường xử lý của operator.

> [!CAUTION]
> ⭐⭐ **Đây là bề mặt nguy hiểm nhất hệ thống, và ⛔ KHÔNG phải vì lý do kỹ thuật.**
> Một lỗi ở đây ⛔ không làm hỏng một tính năng — nó làm **mất điều kiện miễn trừ trách nhiệm** của cả nền tảng. Ba cách hỏng, cả ba đều **im lặng**:
>
> 1. Từ chối một đơn **hợp lệ** ở tầng validate ⇒ ⭐ **đồng hồ SLA 72 giờ ⛔ không bao giờ bắt đầu** — và ⛔ không có log nào của một đơn chưa từng được ghi.
> 2. Nhận `received_at` từ client ⇒ **bằng chứng SLA do bên ngoài đặt**.
> 3. Thêm một phép "kiểm tra chủ động" nghe có trách nhiệm ⇒ **tự phá miễn trừ Điều 198b** (`SRS-NFR-15`).

## Mục lục

- [0. Ba ràng buộc xuyên-endpoint — TRỎ, ⛔ không lặp](#0-ba-ràng-buộc-xuyên-endpoint--trỏ--không-lặp)
- [1. Resource](#1-resource)
- [2. ⭐ Bề mặt KHÔNG auth, KHÔNG tenant context — RLS ⛔ không áp được, và cái gì thay thế](#2--bề-mặt-không-auth-không-tenant-context--rls--không-áp-được-và-cái-gì-thay-thế)
- [3. Danh sách endpoint](#3-danh-sách-endpoint)
- [4. Invariant của resource](#4-invariant-của-resource)
- [5. `TBD` chặn — ⛔ file này không đóng hàng nào](#5-tbd-chặn---file-này-không-đóng-hàng-nào)
- [6. UC nào tiêu thụ](#6-uc-nào-tiêu-thụ)
- [7. Tài liệu tham khảo](#7-tài-liệu-tham-khảo)

---

## 0. Ba ràng buộc xuyên-endpoint — TRỎ, ⛔ không lặp

> ⛔ **File này ⛔ KHÔNG đặc tả lại bốn ràng buộc xuyên-endpoint.** Trỏ theo mã:

| Mã | Nguồn duy nhất | Áp ở đâu trong file này |
|---|---|---|
| `SDD-HG-01` | [SDD §6.3](../Architecture/SDD-Comic-Studio.md) | ⭐ Vế **disable-access** của `SDD-HG-01.4` là **hệ quả** của [`TD-3`](#td-3--patch-v1admintakedown-requestsid). ⛔ File này ⛔ không đặc tả lại điều kiện chặn export |
| `ADR-015` (queue + polling **2 giây**) | [ADR-015 `Q6`](../Architecture/ADR-015-Job-Queue-In-Postgres.md) | ⛔ **Không endpoint nào trong file này là async** — xem [`INV-API-TD-8`](#4-invariant-của-resource) |
| `ADR-017` (`KC-4`, mã `Q4.x`) | [ADR-017 `Q2` + `Q4.3` `P-2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) | ⭐ [`TD-3`](#td-3--patch-v1admintakedown-requestsid) là endpoint ghi ⇒ tuân hợp đồng trích dẫn `Q4.7`. ⚠️ [`TD-1`](#td-1--post-v1publictakedown-requests) là **ngoại lệ có lý do** — xem [`INV-API-TD-6`](#4-invariant-của-resource) |
| `ADR-006` (RLS) | [ADR-006 `D6`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) | ⭐ Toàn bộ [mục 2](#2--bề-mặt-không-auth-không-tenant-context--rls--không-áp-được-và-cái-gì-thay-thế) |

> [!CAUTION]
> ⛔⛔ **`SRS-NFR-15` — ⛔ TUYỆT ĐỐI không endpoint nào trong file này gọi copyright / plagiarism / similarity detection.**
> ⛔ Không endpoint nào **quét**, **gắn cờ**, **chấm điểm nghi vấn**, hay **đối chiếu nội dung** để tự tìm ra *"đơn này có đúng không"* / *"nội dung nào trong hệ thống giống tác phẩm được nêu"*.
> **Lý do là pháp lý, ⛔ không phải kỹ thuật** — nguồn: [Spec-Security-Legal-Compliance §5](../Security/Spec-Security-Legal-Compliance.md) và [Spec-Security-Threat-Model §5](../Security/Spec-Security-Threat-Model.md). ⛔ **File này ⛔ không lập luận lại.**
> ⚠️ ⭐ **Đây đúng chỗ phản xạ nghề nghiệp làm ngược**: viết một endpoint takedown mà ⛔ **không** có bước "đối chiếu" cảm giác như thiếu sót. Nó ⛔ **không** thiếu sót — nó là **thiết kế**. Bước xác định nội dung bị khiếu nại là **người** làm ([`TM-F7-1`](../Security/Spec-Security-Threat-Model.md)), dựa trên `target_description` do người gửi mô tả.
> ⚠️ **Ranh giới ⛔ không được đọc quá** (Legal-Compliance §5.2 hàng 5): quy tắc này ⛔ **không** cấm rate limit, ⛔ không cấm giới hạn kích thước body, ⛔ không cấm validate định dạng JSON.

---

## 1. Resource

| Hạng mục | Nội dung |
|---|---|
| **Bảng nguồn** | ⭐ [`public.takedown_request`](../Schema/DB-Entity-Compliance-And-Takedown.md) — ⛔ **không có `tenant_id`** · [`public.project_access_state`](../Schema/DB-Entity-Compliance-And-Takedown.md) — **có** `tenant_id` |
| **Kênh tiếp nhận** | **Hai** (`SRS-FR-38`): (a) form công khai ⇒ [`TD-1`](#td-1--post-v1publictakedown-requests), `channel='web_form'`; (b) hộp thư `copyright@` ⇒ ⛔ **không phải HTTP endpoint** — xem [ranh giới kênh email](#ranh-giới--kênh-email-copyright--không-thuộc-file-này) |
| **Số endpoint** | **3** — đúng resource #15 của [findings/architect §4.1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) |
| ⭐ **Vì sao là file riêng** | Bề mặt **công khai, ⛔ không cần tài khoản** ⇒ **security posture khác hẳn** phần còn lại. findings §4.2 ghi thẳng: *"Gộp vào file khác là mời một lỗ hổng"* |
| **Nghĩa vụ nguồn** | `L-4` — checklist safe harbour Điều 198b ([findings/business-analyst §3.1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/business-analyst.md)) · `SRS-FR-38` · `BLOCKER-02` |

### Ranh giới — kênh email `copyright@` ⛔ không thuộc file này

⚠️ `channel='email'` là giá trị **hợp lệ** của bảng, nhưng đường nạp nó là **integration**, ⛔ không phải endpoint ⇒ thuộc `Spec-Integration-Takedown-Intake.md` (lô `L16`–`L17`).

⭐ **Ràng buộc file này SỞ HỮU và gửi sang lô đó** — `CO-TD-1`: đường email **phải ghi qua cùng một intake service** với [`TD-1`](#td-1--post-v1publictakedown-requests), để `received_at` giữ nguyên ngữ nghĩa *"thời điểm HỆ THỐNG nhận"*. ⛔ **Không** đường nào được lấy timestamp từ **header của email** — header do người gửi đặt, và đó đúng là lỗi mà [`INV-API-TD-2`](#4-invariant-của-resource) chặn ở đường HTTP.

---

## 2. ⭐ Bề mặt KHÔNG auth, KHÔNG tenant context — RLS ⛔ không áp được, và cái gì thay thế

> [!IMPORTANT]
> ⭐ **Phát biểu thẳng: ở [`TD-1`](#td-1--post-v1publictakedown-requests), tại thời điểm `INSERT`, hệ thống ⛔ KHÔNG có tenant nào để bơm vào session ⇒ ⛔ KHÔNG viết được vị từ `tenant_id = public.current_tenant_id()` ⇒ RLS ⛔ KHÔNG áp được theo tenant.**
> Đây là **ngoại lệ duy nhất** của mô hình RLS trong toàn hệ thống — đã được lường trước ở [ADR-010](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) Consequences và chốt cách xử lý ở [ADR-006 `D6`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md). ⛔ **File này ⛔ không quyết lại, và ⛔ không phát minh cơ chế mới.**
> ⚠️ Nó ⛔ **không phải một lỗ hổng** — nó là **hình dạng bắt buộc của nghĩa vụ pháp lý**: bắt người gửi đăng ký tài khoản để nộp đơn takedown là **tự bỏ điều kiện (a) của `L-4`**.

⭐ **Sáu thứ thay thế RLS trên bề mặt này** — ⛔ không cái nào một mình đủ, phải có **cả sáu**:

| # | Thay thế | Cơ chế | Nguồn |
|:--:|---|---|---|
| **1** | ⭐ **Đặc quyền cực tiểu ở tầng DB role** | [`TD-1`](#td-1--post-v1publictakedown-requests) chạy dưới role **`app_public_intake`**, quyền **CHỈ `INSERT`** vào `public.takedown_request`. ⛔ Không `SELECT` **bất kỳ** bảng nghiệp vụ nào. ⛔ **Không giải bằng `BYPASSRLS`** | [ADR-006 `D6`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [SDD §7.4](../Architecture/SDD-Comic-Studio.md) |
| **2** | ⭐ **Fail-closed mặc định trên chính bảng** | RLS vẫn **BẬT** + `FORCE`, với **đúng một** policy `FOR INSERT`. ⛔ Không policy `SELECT` nào ⇒ mọi câu query lạc trả **0 dòng** | [DB-Entity-Compliance-And-Takedown §RLS Policy](../Schema/DB-Entity-Compliance-And-Takedown.md) |
| **3** | ⭐ **⛔ Không tồn tại đường đọc công khai** | ⛔ **Không có** `GET /public/takedown-requests/{id}`, ⛔ không endpoint tra cứu trạng thái, ⛔ không "check my request". Xác nhận tiếp nhận **chỉ** là body của `201` — xem [`INV-API-TD-5`](#4-invariant-của-resource) | Story-Safe-Harbour mục 4 |
| **4** | **Bề mặt đặc quyền là danh sách review CỐ ĐỊNH** | Role `app_public_intake` nằm trong ba bề mặt của `C-11`; mọi thay đổi chạm nó **review như code bảo mật** + đối chiếu `pg_policies` với hằng số trong repo ở CI | [Spec-Security-Threat-Model `C-11`](../Security/Spec-Security-Threat-Model.md) |
| **5** | **Abuse control** — cơ chế CHỐT, ⛔ ngưỡng số MỞ | Rate limit trên [`TD-1`](#td-1--post-v1publictakedown-requests) (`SRS-NFR-20`). ⚠️ ⭐ **Ràng buộc ngược, ⛔ không được quên**: ngưỡng ⛔ **không được** chặt tới mức làm **mất một đơn hợp lệ** — mất đơn là mất chính điều kiện miễn trừ | [`C-6`, `TM-F7-2`](../Security/Spec-Security-Threat-Model.md) · ngưỡng = `T-10` |
| **6** | ⚠️ **Uỷ quyền operator ở tầng ứng dụng** cho [`TD-2`](#td-2--get-v1admintakedown-requests)/[`TD-3`](#td-3--patch-v1admintakedown-requestsid) | ⛔⛔ **CHƯA CÓ CƠ CHẾ** — xem [hàng `TD-Q1`](#5-tbd-chặn---file-này-không-đóng-hàng-nào). ⛔ **File này ⛔ không tự phát minh role thứ năm** | [DB-Entity-Compliance-And-Takedown §RLS Policy](../Schema/DB-Entity-Compliance-And-Takedown.md) |

### ⚠️ Hệ quả ⛔ không được bỏ qua: hai endpoint admin cũng **xuyên tenant**

⭐ `public.takedown_request` ⛔ **không có `tenant_id`** ⇒ [`TD-2`](#td-2--get-v1admintakedown-requests) và [`TD-3`](#td-3--patch-v1admintakedown-requestsid) đọc/ghi một bảng **⛔ không phân vùng theo tenant**.

⇒ ⛔ **Không được** viết chúng theo khuôn *"đã có RLS lo"* như 13 file `Endpoint-*` còn lại. Toàn bộ kiểm soát truy cập của hai endpoint này nằm ở **hàng 6** của bảng trên — tức là ở **thứ chưa tồn tại**. Đó là lý do [`TD-Q1`](#5-tbd-chặn---file-này-không-đóng-hàng-nào) là hàng **chặn triển khai**, ⛔ không phải ghi chú.

⚠️ **Ngoại lệ này phải nằm trong allowlist của phép đo `M1-1`/`D3`** cùng `public.tenant` và `public."user"` — allowlist là **một danh sách hợp nhất ba tên**, ⛔ không phải ba danh sách rời.

---

## 3. Danh sách endpoint

> ⚠️ **Quy ước tiền tố path**: file này dùng `/v1/public/…` cho bề mặt công khai và `/v1/admin/…` cho bề mặt operator. ⛔ **Chưa có quy ước tiền tố chung** cho 14 file `Endpoint-*` — xem [`TD-Q4`](#5-tbd-chặn---file-này-không-đóng-hàng-nào).

### `TD-1` — `POST /v1/public/takedown-requests`

⭐ **Endpoint quan trọng nhất của file.** Tiếp nhận yêu cầu hạ nội dung từ **actor ngoài mọi tenant**.

| Hạng mục | Nội dung |
|---|---|
| **Method · Path** | `POST /v1/public/takedown-requests` |
| ⭐ **Auth** | ⛔ **KHÔNG** — ⛔ không token, ⛔ không API key, ⛔ không tenant context. Cố ý, theo `L-4(a)` |
| **DB role** | `app_public_intake` — **CHỈ `INSERT`** |
| **Idempotency** | ⛔ **KHÔNG** — xem [`INV-API-TD-4`](#4-invariant-của-resource) |
| **Rate limit** | ✅ Có (cơ chế CHỐT) · ngưỡng `T-10` `TBD` · ⚠️ ràng buộc ngược ở [mục 2 hàng 5](#2--bề-mặt-không-auth-không-tenant-context--rls--không-áp-được-và-cái-gì-thay-thế) |

**Request body** — ⭐ **mọi trường đều OPTIONAL ở tầng API**:

| Trường | Kiểu | Bắt buộc? | Ghi chú |
|---|---|:--:|---|
| `requester_name` | `string` | ⛔ | |
| `requester_email` | `string` | ⛔ | ⚠️ **Dữ liệu cá nhân của người NGOÀI hệ thống** — [`TD-Q2`](#5-tbd-chặn---file-này-không-đóng-hàng-nào) |
| `requester_phone` | `string` | ⛔ | ⚠️ Như trên |
| `claimed_work` | `string` | ⛔ | Tác phẩm người gửi **tuyên bố** sở hữu quyền |
| `target_description` | `string` | ⛔ | ⭐ Mô tả nội dung bị khiếu nại **bằng lời của người ngoài**. ⛔ **KHÔNG** phải khoá nội bộ — họ ⛔ không biết `project_id` của ta |

> [!CAUTION]
> ⛔⛔ **⛔ KHÔNG có `422 Unprocessable Entity` cho "thiếu trường bắt buộc" — và đây là điều khoản quan trọng nhất của endpoint này.**
> **Danh sách trường bắt buộc của một yêu cầu takedown HỢP LỆ là `TBD`** (`EF-1(a)`): nguyên văn NĐ 17/2023 và NĐ 134/2026 ⛔ **chưa đọc được** (403/paywall, `KT-5`), và cả `SRS-FR-38` lẫn `BRD-007` đều ⛔ **không** liệt kê trường bắt buộc.
> ⇒ Đặt validation *"thiếu email ⇒ 422"* là **bịa một nghĩa vụ pháp lý rồi cưỡng chế nó ở tầng API**. Hậu quả chính xác: ⭐ **một đơn THẬT, HỢP LỆ theo luật, bị từ chối ở cổng vào — và đồng hồ SLA 72 giờ ⛔ không bao giờ bắt đầu.** ⛔ Không log nào ghi lại một đơn chưa từng được nhận.
> ⇒ ⭐ **Nguyên tắc: NHẬN-VÀ-GHI. Tính hợp lệ đánh giá ở tầng nghiệp vụ** bằng `status='needs_more_info'` ([`TD-3`](#td-3--patch-v1admintakedown-requestsid)), ⛔ **không ở tầng validate**. Cùng lập luận với `INV-TR-2` của tầng schema.
> ⚠️ ⛔ Cũng ⛔ **không** trả `422` cho **trường lạ** — đường email và form tương lai có thể mang thêm field; **bỏ qua field lạ**, ⛔ không từ chối cả đơn.

**Response `201 Created`** — ⭐ **đúng hai trường, ⛔ không hơn**:

```json
{ "id": "uuid", "received_at": "2026-08-29T04:15:22.481Z" }
```

| Trường | Ý nghĩa |
|---|---|
| `id` | ⭐ **Chính là ID xác nhận tiếp nhận** trả cho người gửi (PK của `takedown_request`) |
| ⭐ `received_at` | ⭐⭐ **MỐC ĐẾM SLA 72 GIỜ — thuộc tính PHÁP LÝ, ⛔ KHÔNG phải metadata vận hành.** Xem [`INV-API-TD-2`](#4-invariant-của-resource) |

**Mã lỗi**:

| Mã | Khi nào | ⚠️ Ràng buộc |
|:--:|---|---|
| `400` | ⭐ **CHỈ** khi body ⛔ không parse được thành JSON, hoặc content-type sai | ⛔ **Không** dùng cho *"thiếu trường"* |
| `413` | Body vượt trần kích thước | Cơ chế CHỐT (`C-6(b)`), ngưỡng `T-10` |
| `429` | Vượt rate limit | ⚠️ **Ngưỡng ⛔ không được chặt tới mức làm mất một đơn hợp lệ** (`TM-F7-2`) |
| `500` | Lỗi hệ thống | ⭐ **Response ⛔ không được nói *"đơn của bạn đã được ghi nhận"* khi transaction chưa commit** — người gửi sẽ tin rằng đồng hồ đã chạy |

| Mã ⛔ **KHÔNG tồn tại** | Vì sao |
|:--:|---|
| ⛔ `401` / `403` | ⛔ Không có xác thực để mà từ chối. Có `401` ở đây nghĩa là ai đó đã thêm auth vào bề mặt phải công khai ⇒ **phá `L-4(a)`** |
| ⛔ `404` | ⛔ **Không có tra cứu tài nguyên nào ở đường công khai** ⇒ ⛔ không có `404` để làm oracle |
| ⛔ `409` | ⛔ Không dedup — [`INV-API-TD-4`](#4-invariant-của-resource) |
| ⛔ `422` | Xem khối `CAUTION` ở trên |

> [!WARNING]
> ⚠️ ⭐ **Oracle rò rỉ — vì sao endpoint này MIỄN NHIỄM theo CẤU TRÚC, ⛔ không nhờ cẩn thận.**
> Quy tắc `C-5` (*thông báo lỗi ⛔ không được phân biệt "không tồn tại" với "không thuộc về bạn"*) tồn tại vì các endpoint khác nhận **ID tài nguyên**. ⭐ Ở đây **⛔ KHÔNG có tham số ID nào của hệ thống trong request** — người gửi mô tả nội dung bằng **văn xuôi** (`target_description`), ⛔ không bằng `project_id`.
> ⇒ ⛔ **Không có phép tra cứu nào để trả lời *"thứ này có tồn tại không"*** ⇒ ⛔ không có oracle.
> ⇒ ⛔⛔ **CẤM tuyệt đối** hai "cải tiến" sẽ tạo ra oracle: (a) nhận `project_id`/URL rồi **validate nó tồn tại** — biến endpoint công khai thành **máy dò project của tenant khác**; (b) trả về *"đã tìm thấy nội dung khớp"* — vừa là oracle, vừa vi phạm `SRS-NFR-15`.

---

### `TD-2` — `GET /v1/admin/takedown-requests`

Danh sách yêu cầu cho **operator** (Founder ở vai operator) đánh giá — bước 3 của `UC-11`.

| Hạng mục | Nội dung |
|---|---|
| **Method · Path** | `GET /v1/admin/takedown-requests` |
| ⚠️ **Auth** | **Bắt buộc — nhưng cơ chế uỷ quyền operator là [`TD-Q1`](#5-tbd-chặn---file-này-không-đóng-hàng-nào), ⛔ CHƯA CÓ.** ⛔ Endpoint này ⛔ **không được triển khai** trước khi hàng đó đóng |
| ⭐ **Phạm vi** | ⭐ **XUYÊN TENANT** — bảng ⛔ không có `tenant_id`. ⛔ **Không** lọc theo `current_tenant_id()` (⛔ không có gì để lọc) |
| **DB role** | ⛔ **CHƯA PIN** — `app_public_intake` ⛔ **không** được `SELECT`. Xem [`TD-Q1`](#5-tbd-chặn---file-này-không-đóng-hàng-nào) |

**Query params**:

| Param | Kiểu | Ghi chú |
|---|---|---|
| `status` | `enum` | `received` \| `needs_more_info` \| `rejected` \| `actioned` — danh mục **đóng** của schema |
| `received_before` · `received_after` | `timestamptz` | Cửa sổ thời gian trên `received_at` |
| `order_by` | `enum` | `received_at_asc` (**mặc định**) — đơn cũ nhất trước |
| `limit` · `cursor` | | Phân trang |

> [!IMPORTANT]
> ⭐⭐ **Endpoint này là NỬA API của cơ chế đếm ngược SLA 72 giờ (`R-02`) — ⛔ không phải một màn hình list cho tiện.**
> Tầng schema đã pin index `ix_takedown_sla` trên `(status, received_at)` và **route cơ chế đếm ngược/cảnh báo sang "lô API + vận hành"**. ⇒ ⭐ **Nghĩa vụ file này nhận**: bộ `status` + `received_before` + `order_by=received_at_asc` phải làm cho câu hỏi ***"đơn nào đã quá 72 giờ mà chưa xử lý"*** trở thành **một truy vấn chạy được**, ⛔ không phải một việc rà tay.
> ⚠️ **Phần ⛔ KHÔNG thuộc file này**: **cảnh báo/alerting** (ai được báo, qua kênh nào, sau bao lâu) là **vận hành** — vẫn `TBD`, xem [`TD-Q3`](#5-tbd-chặn---file-này-không-đóng-hàng-nào).
> ⚠️ ⛔ **Và ⛔ không kết luận hệ quả pháp lý của việc trễ SLA** — câu đó thuộc luật sư.

**Response `200 OK`**: mảng dòng `takedown_request` + `next_cursor`. ⭐ Mỗi dòng **bắt buộc** mang `id`, `received_at`, `status`, `channel`, `project_id` (có thể `null`), `resolved_at`.

⚠️ **Dữ liệu cá nhân của người gửi** (`requester_email`, `requester_phone`) **có** trong response — vì operator cần nó để phản hồi. ⇒ Kéo theo hai nghĩa vụ, ⛔ không được quên: (a) `C-4` — ⛔ **cấm** để lọt các trường này vào `stdout`/`stderr`; (b) chính sách lưu giữ/xoá = [`TD-Q2`](#5-tbd-chặn---file-này-không-đóng-hàng-nào).

**Mã lỗi**:

| Mã | Khi nào |
|:--:|---|
| `400` | Query param sai kiểu / `status` ngoài danh mục đóng |
| `401` | ⛔ Không có định danh |
| `403` | Có định danh nhưng ⛔ không phải operator — ⚠️ **điều kiện của `403` chính là [`TD-Q1`](#5-tbd-chặn---file-này-không-đóng-hàng-nào)** |
| `500` | |

⭐ `C-5` **⛔ không áp cho endpoint này** và ⚠️ **phải nói rõ vì sao, ⛔ không để người đọc tự suy**: `C-5` chống oracle **xuyên tenant** trên tài nguyên **có** tenant. Bảng này ⛔ không có tenant, và người gọi là operator toàn hệ thống ⇒ ⛔ không có ranh giới tenant nào để rò. ⚠️ Nhưng nó ⛔ **không** cho phép nới `403` thành `200`.

---

### `TD-3` — `PATCH /v1/admin/takedown-requests/{id}`

⭐ **Endpoint xử lý** — bước 4 của `UC-11`: chuyển trạng thái đơn, và **khi `actioned`** thì **đồng thời** thực hiện disable-access cấp project.

| Hạng mục | Nội dung |
|---|---|
| **Method · Path** | `PATCH /v1/admin/takedown-requests/{id}` |
| ⚠️ **Auth** | Như [`TD-2`](#td-2--get-v1admintakedown-requests) — chặn bởi [`TD-Q1`](#5-tbd-chặn---file-này-không-đóng-hàng-nào) |
| ⭐ **Transaction** | ⭐ **MỘT transaction** cho: `UPDATE takedown_request` + `UPDATE project_access_state` + `INSERT change_log`. Chuẩn tắc: [ADR-017 `Q2` + `Q4.3` `P-2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md). ⛔ **File này ⛔ không đặc tả lại `KC-4`** |

**Request body**:

| Trường | Kiểu | Ghi chú |
|---|---|---|
| `status` | `enum` | `needs_more_info` \| `rejected` \| `actioned` |
| `project_id` | `uuid` \| `null` | ⭐ **Do OPERATOR xác định sau khi đánh giá**, ⛔ **không** do người gửi cung cấp ([`INV-API-TD-3`](#4-invariant-của-resource)) |
| `note` | `string` | Ghi chú xử lý — đi vào `change_log`, ⛔ không vào bảng `takedown_request` |

⛔ **Trường ⛔ KHÔNG được nhận**: `received_at` (xem [`INV-API-TD-2`](#4-invariant-của-resource)) · `resolved_at` (⭐ **server ghi** khi vào `actioned`/`rejected`) · ⛔ bất kỳ trường nào đặt trực tiếp `access_state`.

**Ngữ nghĩa của `status='actioned'`** — bốn mệnh đề, đọc **cùng nhau**:

| # | Mệnh đề | Neo |
|:--:|---|---|
| **1** | ⭐ **Disable-access là `UPDATE` dòng `project_access_state` ĐÃ TỒN TẠI, ⛔ KHÔNG phải `INSERT`.** `INV-PAS-5` bảo đảm mọi project có sẵn đúng một dòng ngay từ transaction tạo project ⇒ endpoint này **⛔ không bao giờ** phải tạo dòng, và ⛔ **không được** diễn giải *"thiếu dòng"* thành bất cứ điều gì — thiếu dòng là **lỗi**, ⛔ không phải `'active'` | `INV-PAS-3`, `INV-PAS-5` |
| **2** | ⭐ **⛔ KHÔNG hard-delete. Cơ chế DUY NHẤT là đổi `access_state`.** Dữ liệu **phải giữ** cho counter-notice. ⛔ Endpoint này ⛔ không có nhánh nào gọi `DELETE` | `INV-TR-3` · [ADR-010 `D7`](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) |
| **3** | ⭐ **`actioned` HỢP LỆ ngay cả khi `project_id IS NULL`** — `EF-3` của `UC-11`: project **đã bị hard-delete bởi chính tenant** trước khi đơn đến. Nội dung ⛔ không còn tồn tại ⇒ ⛔ **không có** disable-access nào để làm, nhưng đơn thì **đã được tiếp nhận và phải được đóng**. ⛔ Endpoint ⛔ **không được** trả `404`/`409` ở tình huống này | `UC-11 EF-3` · FK `ON DELETE SET NULL` |
| **4** | ⛔ **⛔ KHÔNG có action "thông báo cho tenant" trong contract này** — xem khối dưới | [`TD-Q3`](#5-tbd-chặn---file-này-không-đóng-hàng-nào) |

> [!CAUTION]
> ⚠️⛔ **`T-29` — nội dung / hình thức / thời hạn THÔNG BÁO cho tenant bị takedown vẫn CÒN MỞ. ⛔ File này ⛔ KHÔNG được tự quyết.** ⭐ **Chủ đã được PM gán** (xem cuối khối) — thứ còn thiếu là **nội dung**, ⛔ không phải chủ sở hữu.
> ⭐ Lý do ⛔ không phải thủ tục: **chính bước thông báo là điều kiện tối thiểu để counter-notice tồn tại**, và counter-notice gắn trực tiếp vào **điều kiện miễn trừ Điều 198b**. Chọn sai *"thông báo cái gì"* (ví dụ: chuyển nguyên `requester_email` + `requester_phone` cho tenant) còn chạm thẳng vào `TM-F7-6` — **lộ dữ liệu cá nhân của người nộp đơn**.
> ⇒ ⭐ **Quyết định của file này: [`TD-3`](#td-3--patch-v1admintakedown-requestsid) ⛔ KHÔNG có field, ⛔ không có side-effect, ⛔ không có endpoint anh em nào gửi thông báo.** Thêm nó khi chưa có nội dung được duyệt là **tự viết một văn bản pháp lý**.
> **Ai đóng**: ⭐ **Founder + luật sư, PM điều phối** — PM **đã gán** ở [run-state `E22`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md). ⚠️ Đây là **quyết định pháp lý**, ⛔ không phải quyết định bảo mật hay kiến trúc (`security-auditor` **từ chối nhận việc**, PM **chấp nhận** lời từ chối). **Khi nào**: trước `BLOCKER-02`.

**Response `200 OK`**: dòng `takedown_request` sau cập nhật + `project_access_state` liên quan (nếu có), gồm `disabled_at`.

**Mã lỗi**:

| Mã | Khi nào |
|:--:|---|
| `400` | `status` ngoài danh mục đóng · body sai kiểu |
| `401` / `403` | Như [`TD-2`](#td-2--get-v1admintakedown-requests) |
| `404` | ⭐ **CHỈ** khi `{id}` ⛔ không phải một `takedown_request` tồn tại. ⚠️ ⛔ **Không** dùng `404` cho trường hợp `project_id` trỏ tới project đã biến mất — đó là mệnh đề **3** ở trên |
| `409` | ⭐ **CHỈ** khi đơn **đã ở** `actioned`/`rejected` mà cố chuyển tiếp — ⛔ để tránh ghi đè `resolved_at` im lặng |
| `500` | ⭐ Transaction rollback ⇒ ⛔ **không có** thay đổi bộ phận nào: ⛔ không có `access_state` bị đổi mà thiếu `change_log`, và ngược lại |

> [!WARNING]
> ⚠️ ⭐ **Đồ thị chuyển trạng thái đầy đủ ⛔ CHƯA đóng được — và file này ⛔ không tự đóng.**
> Nguồn **chỉ** pin bốn giá trị của `CHECK`, ⛔ **không** pin đường đi giữa chúng. Câu chưa có đáp án: ***đồng hồ SLA 72 giờ có TẠM DỪNG khi đơn ở `needs_more_info` chờ bổ sung thông tin không*** (`EF-1(b)`) — mà chính nó quyết định `needs_more_info → received` là hợp lệ hay không, và `received_at` có ý nghĩa gì sau đó.
> ⇒ ⛔ **Không hard-code đồ thị chuyển trạng thái trước khi `EF-1(b)` có đáp án.** **Ai đóng**: **luật sư SHTT → PM**, gate `G0`.

---

## 4. Invariant của resource

| Mã | Invariant | Cưỡng chế bằng |
|:--:|---|---|
| **`INV-API-TD-1`** | ⭐⭐ **NHẬN-VÀ-GHI**: [`TD-1`](#td-1--post-v1publictakedown-requests) ⛔ **không bao giờ** từ chối một đơn vì *"thiếu trường"*. Mọi request parse được ⇒ **một dòng `takedown_request`** | Test: `POST` với body `{}` ⇒ **`201`** + có dòng trong DB. ⭐ Test này là **bằng chứng chống lại lỗi đắt nhất của bề mặt** |
| **`INV-API-TD-2`** | ⭐⭐ **`received_at` DO HỆ THỐNG GHI.** ⛔ Không endpoint nào nhận nó từ client — kể cả `TD-1`, `TD-3`, kể cả header của email. Trường lạ trùng tên bị **bỏ qua**, ⛔ không dùng, ⛔ không gây lỗi | `DEFAULT now()` ở DB + role `app_public_intake` ⛔ không có quyền ghi cột này + test gửi `received_at` giả ⇒ giá trị lưu là **giờ server**. ⚠️ Đây là **bằng chứng SLA**; nhận từ ngoài = để người khác đặt lại đồng hồ nghĩa vụ của mình |
| **`INV-API-TD-3`** | ⛔ **`project_id` ⛔ KHÔNG bao giờ đến từ người gửi** — chỉ operator ghi ở [`TD-3`](#td-3--patch-v1admintakedown-requestsid) | Schema request của `TD-1` ⛔ không có trường này; test gửi thừa ⇒ bị bỏ qua. ⚠️ Nhận nó ở đường công khai = **tạo oracle dò project** |
| **`INV-API-TD-4`** | ⛔ **⛔ KHÔNG dedup ở intake**, ⛔ không idempotency key, ⛔ không `409` | ⭐ **Lý do**: dedup buộc phải **đoán** hai đơn có "cùng nội dung" không ⇒ nguy cơ **nuốt một đơn khác biệt hợp lệ** — vi phạm `INV-API-TD-1`. ⚠️ **Trùng lặp ⛔ không phải vấn đề**: `PK (project_id)` của `project_access_state` làm **N đơn → đúng MỘT** trạng thái disable ⇒ *"chồng chéo trạng thái"* là thứ ⛔ **không biểu diễn được**. ⛔ Lập luận này neo vào `INV-TR-2` + SLA, ⛔ **không** neo vào `SRS-NFR-15` |
| **`INV-API-TD-5`** | ⛔ **⛔ Không đường đọc công khai nào tồn tại.** Người gửi ⛔ không tra cứu lại được đơn của mình qua HTTP hay DB | Chỉ có 3 endpoint; 2 endpoint đọc/ghi đều **admin-only**. Xác nhận = body `201` |
| **`INV-API-TD-6`** | ⚠️ **Bất đối xứng `change_log`**: [`TD-3`](#td-3--patch-v1admintakedown-requestsid) sinh `change_log` cùng transaction (`M9 → M8`, [SDD §6.2](../Architecture/SDD-Comic-Studio.md)); ⭐ [`TD-1`](#td-1--post-v1publictakedown-requests) **⛔ KHÔNG** | ⭐ **⛔ Không phải thiếu sót**: `change_log` ghi **hành động người dùng**, mà người gửi đơn ⛔ **không phải người dùng** — ⛔ không tenant, ⛔ không `user_id`. Và `app_public_intake` ⛔ **không** có grant trên `change_log` (`C-11`, đặc quyền cực tiểu). ⇒ **Chính dòng `takedown_request` LÀ bản ghi của sự kiện đó** |
| **`INV-API-TD-7`** | ⛔ **⛔ Không endpoint nào quét / gắn cờ / chấm điểm / đối chiếu nội dung.** Đánh giá là việc **của người** | `SRS-NFR-15`; nguồn lập luận: [Legal-Compliance §5](../Security/Spec-Security-Legal-Compliance.md), [Threat-Model §5](../Security/Spec-Security-Threat-Model.md). Cưỡng chế: **từ chối tại review**, ⛔ không thương lượng phạm vi |
| **`INV-API-TD-8`** | ⛔ **⛔ Không endpoint nào của file này là async** — ⛔ không job, ⛔ không polling | ⭐ Contract `CT-POLL-2S` ([ADR-015 `Q6`](../Architecture/ADR-015-Job-Queue-In-Postgres.md), độ rắn `MẶC ĐỊNH`) áp cho tác vụ async; ⛔ **không** áp ở đây. ⚠️ Lý do phải nói rõ: đẩy disable-access sang một job **nới ranh giới transaction của `KC-4`** và làm `disabled_at` ⛔ không còn là **vế thứ hai đáng tin của phép đo SLA** |
| **`INV-API-TD-9`** | ⛔ **⛔ Không endpoint nào ngoài [`TD-3`](#td-3--patch-v1admintakedown-requestsid) được đổi `access_state`** | ⭐ `INV-PAS-2` bắt mọi disable **truy được về một `takedown_request`**. ⇒ Một `PATCH /projects/{id}` cho phép set `access_state` sẽ tạo disable **⛔ không có căn cứ** — xem `RIPPLE` trong báo cáo lô |
| **`INV-API-TD-10`** | ⚠️ **`deleted_at` của project ⛔ KHÔNG BAO GIỜ được đọc thành trạng thái takedown** | ⭐ `CO-2` của tầng schema: hai cột đọc **độc lập**. Soft-delete của **tác giả** ≠ disable-access do **người ngoài**. ⛔ Gộp hai khái niệm là mất nguồn sự thật của câu *"project này có đang bị takedown không"* |

---

## 5. `TBD` chặn — ⛔ file này không đóng hàng nào

| Mã | Nội dung | Ai đóng | Khi nào |
|:--:|---|---|---|
| **`TD-Q1`** ⭐ | **Quyền `SELECT`/`UPDATE` `public.takedown_request` cho đường operator** — role thứ **năm** `app_operator` (⚠️ **sửa [SDD §7.4](../Architecture/SDD-Comic-Studio.md)**) hay đi đường **owner/vận hành** đã có. ⚠️ Kèm theo: **cơ chế uỷ quyền operator ở tầng ứng dụng** — `membership` hiện ⛔ **chưa có** mô hình role/permission nào | **`Spec-Security-*` + [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) / [SDD §7.4](../Architecture/SDD-Comic-Studio.md)** | ⭐ **CHẶN triển khai [`TD-2`](#td-2--get-v1admintakedown-requests) + [`TD-3`](#td-3--patch-v1admintakedown-requestsid)** — trước `BLOCKER-02` |
| **`TD-Q2`** | **Retention / xoá dữ liệu cá nhân của người gửi takedown** (`b-4` / `T-24`). ⚠️ `SRS-FR-38` **bắt buộc thu email + SĐT** của người **⛔ không có tài khoản, ⛔ không tenant, ⛔ không nằm trong mô hình `KC-5`**; và dòng `takedown_request` **sống lâu hơn** tenant liên quan. ⛔ **Không nêu tên văn bản pháp luật cụ thể** (`CẤM-13`) | ⭐ **Luật sư** (+ PM) | Trước khi mở cho người ngoài upload |
| **`TD-Q3`** | ⭐ **`T-29`** — nội dung / hình thức / thời hạn **thông báo cho tenant bị takedown**. ⛔ **Vẫn MỞ** — chỉ **chủ sở hữu** đã được chốt | ⭐ **Founder + luật sư, PM điều phối** — theo PM run-state [`E22`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md). ⚠️ Quyết định **pháp lý**, ⛔ không phải bảo mật/kiến trúc | Chặn tính đầy đủ của luồng counter-notice |
| **`TD-Q4`** | Đồ thị chuyển trạng thái đầy đủ + **SLA có tạm dừng ở `needs_more_info` không** (`EF-1(b)`) · danh sách **trường bắt buộc** của đơn hợp lệ (`EF-1(a)`) · **thủ tục counter-notice** (`AF-1`) | **Luật sư SHTT → PM** | Gate `G0` |
| **`TD-Q5`** | **Ngưỡng** rate limit / trần kích thước body cho [`TD-1`](#td-1--post-v1publictakedown-requests) (`T-10`) · **cảnh báo/alerting** SLA 72h (nửa **vận hành** của `R-02`) · **quy ước tiền tố path** chung cho 14 file `Endpoint-*` | **PM + Architect** (ngưỡng) · **PM** (path) | Trước khi công cụ takedown chạy thật |

---

## 6. UC nào tiêu thụ

| Endpoint | UC · bước nghiệp vụ | Ghi chú ràng buộc |
|---|---|---|
| [`TD-1`](#td-1--post-v1publictakedown-requests) | ⭐ **`UC-11` bước 1** (endpoint tiếp nhận **công khai** — ⛔ không tài khoản, ⛔ không tenant context) + ⭐ **bước 2** (ghi nhận kèm **timestamp tiếp nhận**) | 🔒 Bước 2 **phải đứng TRƯỚC** bước hạ nội dung: *"SLA 72 giờ chỉ chứng minh được nếu có một timestamp tiếp nhận được ghi bởi hệ thống"* |
| [`TD-2`](#td-2--get-v1admintakedown-requests) | **`UC-11` bước 3** (Founder đánh giá yêu cầu) | ⭐ Cũng là **nửa API của cơ chế SLA** (`R-02`) |
| [`TD-3`](#td-3--patch-v1admintakedown-requestsid) | ⭐ **`UC-11` bước 4** (soft-delete + disable-access **cấp project**) | 🔒 ⛔ **KHÔNG hard delete.** `AF-4`/`EF-3` phủ nhánh project đã biến mất |
| ⛔ **⛔ Không endpoint nào** | **`UC-11` bước 5** — phản hồi người yêu cầu trong 72h | ⚠️ **Có chủ đích**: phản hồi đi qua **email** (`copyright@`), ⛔ không qua HTTP — người gửi ⛔ không có tài khoản để nhận response. Thuộc `Spec-Integration-Takedown-Intake.md` |

⭐ **Hai đường ĐỌC `project_access_state` ⛔ KHÔNG thuộc file này** — ghi ra để ⛔ không ai tưởng đã phủ:

| Đường | Thuộc file nào |
|---|---|
| Kiểm disable-access ở **đường export** (`UC-09` bước 3, `SDD-HG-01.4`) | `Endpoint-Preview-Export.md` |
| ⭐ **Đóng DANH SÁCH "mọi đường đọc"** phải kiểm cờ disable-access (`C-3`, `TM-F7-7`) | ⚠️ **Nghĩa vụ của LÔ API nói chung**, ⛔ không của riêng file này. ⭐ Điều file này sở hữu là chiều **GHI**: [`INV-API-TD-9`](#4-invariant-của-resource) |

---

## 7. Tài liệu tham khảo

| Tài liệu | Dùng cho phần nào |
|---|---|
| [DB-Entity-Compliance-And-Takedown](../Schema/DB-Entity-Compliance-And-Takedown.md) | ⭐ **Nguồn chuẩn của bảng, cột, `INV-TR-*`, `INV-PAS-*`, `CO-2`, RLS policy** |
| [Spec-Security-Legal-Compliance §5, §6](../Security/Spec-Security-Legal-Compliance.md) | ⭐ Lập luận `SRS-NFR-15` · bề mặt takedown không auth · `L-4` · `T-24`, `T-29` — ⛔ file này **trỏ**, ⛔ không viết lại |
| [Spec-Security-Threat-Model §3.7, §4.2, §5](../Security/Spec-Security-Threat-Model.md) | `TM-F7-1`…`TM-F7-7` · `C-3`, `C-4`, `C-5`, `C-6`, `C-11` |
| [SDD-Comic-Studio](../Architecture/SDD-Comic-Studio.md) | §6.2 (`M9 → M8`) · §6.3 `SDD-HG-01.4` · §7.4 bốn DB role |
| [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-010](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) | `D6` bề mặt không tenant · `D7` hai đường xoá tách biệt |
| [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) · [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) | `Q6` `CT-POLL-2S` (ranh giới) · `Q2` + `Q4.3` `P-2` + `Q4.7` |
| [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) | `SRS-FR-38` · ⛔ `SRS-NFR-15` · `SRS-NFR-20` · `SRS-NFR-17` |
| [UC-11 — Handle Takedown Request](../../020-Requirements/Use-Cases/UC-11-Handle-Takedown-Request.md) | Bước 1–5 · `AF-1`, `AF-4` · `EF-1`…`EF-5` |
| [Story-Safe-Harbour-Checklist-Article-198b](../../022-User-Stories/Backlog/Story-Safe-Harbour-Checklist-Article-198b.md) | Xác nhận tiếp nhận · N đơn → 1 disable |
| [findings/architect §4.1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) · [findings/business-analyst §1.4, §3.1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/business-analyst.md) | Resource #15 · bước nghiệp vụ `UC-11` · `L-4` |

---

_Created by architect_
_Author: trisjr_
