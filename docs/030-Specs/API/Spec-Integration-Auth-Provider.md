---
id: SPEC-INT-AUTH-PROVIDER
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Spec Integration: Auth Provider

Serves: [Story-Buy-Authentication-Provider](../../022-User-Stories/Backlog/Story-Buy-Authentication-Provider.md) · [Story-Tenant-User-Membership-As-Three-Entities](../../022-User-Stories/Backlog/Story-Tenant-User-Membership-As-Three-Entities.md)
Decided in: [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) · [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-010](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md)

> [!CAUTION]
> ⭐⛔ **Câu quan trọng nhất của file này**: **vendor auth ⛔ KHÔNG sở hữu `tenant_id`.**
> `public.tenant` / `public."user"` / `public.membership` là **nguồn sự thật duy nhất** của `tenant_id` mà RLS neo vào ([ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 1, 2, 4).
> ⛔ **Không seam nào trong file này được thiết kế theo hướng biến vendor thành nguồn sự thật của tenancy** — kể cả khi vendor cho sẵn tính năng đó.

## Mục lục

- [1. Mục đích](#1-mục-đích)
- [2. Cái gì đã CHỐT](#2-cái-gì-đã-chốt)
- [3. Cái gì còn MỞ](#3-cái-gì-còn-mở)
- [4. Interface / seam](#4-interface--seam)
- [5. Retry & error taxonomy](#5-retry--error-taxonomy)
- [6. Chi phí](#6-chi-phí)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## 1. Mục đích

File này đặc tả **bề mặt tiếp xúc giữa hệ thống và vendor auth**: cái gì đi qua ranh giới đó, cái gì ⛔ tuyệt đối không được đi qua, và hệ thống hành xử thế nào khi ranh giới đó hỏng.

⚠️ **Phạm vi**: đây là spec **integration**, ⛔ không phải ADR. Quyết định *"mua, ⛔ không tự viết"* và toàn bộ 8 điều của seam đã đóng ở [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md); cơ chế bơm tenant context đã đóng ở [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md). ⛔ File này **không quyết lại**, chỉ **kéo chúng xuống mức thi hành được** và bổ sung phần chưa ai viết: **error taxonomy** và **hành vi retry**.

**Vì sao integration này chặn mọi thứ khác**: `E4` = `✅ auth` từ **MVP1** ([MVP-Scope](../../010-Planning/MVP-Scope.md) §3). ⛔ Không có nó thì ⛔ không có `tenant_id` trong context, mà ⛔ không có `tenant_id` thì **mọi** truy vấn dưới RLS trả **0 row** ([SDD §6.1](../Architecture/SDD-Comic-Studio.md)).

---

## 2. Cái gì đã CHỐT

### 2.1 Ranh giới sở hữu — bảng phải thuộc lòng

| Thứ | Ai sở hữu | Neo |
|---|---|---|
| Identity, credential, phiên đăng nhập, phương thức đăng nhập | **Vendor** | [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 1 |
| ⭐ `tenant`, `membership`, **mọi** quyết định authorization | ⭐ **CỦA TA** | `D-11` · `SRS-FR-01` |
| ⭐ `tenant_id` mà RLS neo vào | ⭐ **CỦA TA** — tra từ `public.membership` **ở mỗi request** | [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 4 · [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |
| Ánh xạ tới định danh vendor | Cột **duy nhất** `public."user".external_auth_id` (`UNIQUE`) | [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md) |

### 2.2 Tám ràng buộc CHỐT của bề mặt này

| # | Ràng buộc | Neo |
|:--:|---|---|
| `AU-1` | **Mua, ⛔ không tự viết.** ⛔ Không lưu mật khẩu, ⛔ không tự phát session, ⛔ không dùng auth library self-host *"cho tiện"* — [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) `Alternatives` mục B đã loại tường minh | `D-12` · `SRS-FR-03` |
| `AU-2` | ⭐ **Custom claim của vendor ⛔ KHÔNG BAO GIỜ là nguồn sự thật cho `tenant_id` hay role.** Token chỉ cung cấp `sub`. **Lý do bảo mật, ⛔ không phải thẩm mỹ**: token là **bản sao đã ký của quá khứ**; membership bị thu hồi mà token chưa hết hạn thì bản sao đó **vẫn mở được dữ liệu** | [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 4 |
| `AU-3` | **Backend chỉ chấp nhận JWT verify qua JWKS chuẩn OIDC.** ⛔ Không SDK vendor trong đường xử lý request. SDK chỉ được xuất hiện ở **hai chỗ**: (a) frontend, (b) một adapter webhook | [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 3 |
| `AU-4` | ⛔ **Không FK nghiệp vụ nào trỏ vào định danh của vendor.** Mọi FK nội bộ trỏ `public."user".id`; mọi dữ liệu nghiệp vụ trỏ `tenant_id` | `D-11` · [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md) |
| `AU-5` | **Worker ⛔ không có HTTP request ⇒ ⛔ không có token.** Job mang `tenant_id` từ **chính dòng `job`**. ⛔ Worker ⛔ không được gọi vendor auth để lấy ngữ cảnh | [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 5 · [ADR-006 `D4`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |
| `AU-6` | **Webhook của vendor là nguồn SỰ KIỆN, ⛔ không phải nguồn SỰ THẬT**: verify chữ ký → ghi **inbox** có khoá idempotency → xử lý bất đồng bộ. Nhận trùng ⛔ không được tạo hai hệ quả | [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 6 |
| `AU-7` | **Cache kết quả tra `membership`: trong phạm vi MỘT request thì được; ⛔ CẤM cache xuyên request** cho tới khi có cơ chế vô hiệu hoá — nếu không là tự tạo lại đúng lỗ hổng mà `AU-2` vừa tránh | [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) `Consequences` |
| `AU-8` | ⭐ **Bơm `tenant_id` vào session DB SAU bước tra `membership`, ⛔ không trước.** Cơ chế: [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) — ⛔ file này ⛔ không đặc tả lại | [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |

### 2.3 Vendor mặc định và thang đường lui — đã có, nhưng **chưa phải quyết định cuối**

**Mặc định: Clerk.** **Thang đường lui**: `1.` Auth0 · `2.` Supabase Auth hoặc WorkOS · `3.` self-host Keycloak/Ory (chỉ khi ràng buộc lưu trữ dữ liệu trong nước buộc như vậy). **Ba tiêu chí nghiệm thu spike** (trượt một ⇒ chuyển bậc): JWT verify được bằng **JWKS chuẩn** ⛔ không cần SDK backend · **SPA + PKCE** hoàn chỉnh · có đường **xuất dữ liệu user** khi rời đi. Chi tiết và lý do: [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md).

> [!WARNING]
> ⚠️ **File này ⛔ KHÔNG xác nhận thay việc verify, và ⛔ không dán giá.** Xem [§3](#3-cái-gì-còn-mở).

### 2.4 Ba ràng buộc xuyên suốt áp cho bề mặt này

| Mã | Nội dung | Nguồn duy nhất |
|:--:|---|---|
| `C-4` | ⛔ **Token vendor, client secret và signing key ⛔ không được lọt vào `stdout`/`stderr`.** Cưỡng chế bằng test CI grep log | [Spec-Security-Threat-Model §4.2](../Security/Spec-Security-Threat-Model.md) |
| `C-5` | Thông báo lỗi ⛔ **không được** phân biệt *"không tồn tại"* với *"không thuộc về bạn"* | [Spec-Security-Threat-Model §4.2](../Security/Spec-Security-Threat-Model.md) |
| `C-9` | Điều khoản dữ liệu của vendor (*"không dùng dữ liệu khách để train"*, vị trí lưu trữ) **phải verify bằng văn bản khi mua** | [Spec-Security-Threat-Model §4.2](../Security/Spec-Security-Threat-Model.md) |

### 2.5 ⛔ `SRS-NFR-15` áp cho **mọi** integration, kể cả bề mặt này

⛔ **Bề mặt này ⛔ không được gọi bất kỳ dịch vụ copyright / plagiarism / similarity detection nào.** Bề mặt auth ⛔ không tiêu thụ nội dung người dùng, nên lệnh cấm **nghe như không liên quan** — nó được ghi ra ở đây để một lô sau ⛔ không nhét một phép *"kiểm tra danh tiếng vi phạm bản quyền của người đăng ký"* vào bước đăng ký. Lý do đầy đủ: [Spec-Security-Legal-Compliance §5](../Security/Spec-Security-Legal-Compliance.md) — ⛔ file này ⛔ không lặp lại.

---

## 3. Cái gì còn MỞ

> ⛔ **Mục này ⛔ không đóng hàng nào**, chỉ ghi **ai đóng** và **khi nào**. ⛔ Tuyệt đối không tự chọn vendor thay chỗ Phase 1 để `TBD`.

| # | `TBD` | Nội dung | Ai đóng | Khi nào |
|:--:|---|---|---|---|
| 1 | `SRS-NFR-08` | **Vendor auth cuối cùng.** Clerk là **mặc định**, ⛔ không phải đã mua. Phải chạy spike ba tiêu chí ở [§2.3](#23-vendor-mặc-định-và-thang-đường-lui--đã-có-nhưng-chưa-phải-quyết-định-cuối) | **Dev** | **Kickoff MVP1**, spike **tối đa 1 ngày** |
| 2 | — | **Danh sách trường đồng bộ từ vendor** (email, tên hiển thị, avatar…). ⛔ **Không tự thêm cột `email`** vào `public."user"` — thêm một cột dữ liệu cá nhân là tạo nghĩa vụ mà ⛔ chưa ai xác định (`T-24`) | **PM + Architect** | Khi chốt vendor |
| 3 | — | **TTL của phiên đăng nhập.** ⛔ Chưa nguồn nào chốt. ⚠️ Đây là **đầu vào chặn** của `T-7`: [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) chốt *"TTL signed URL phải NGẮN HƠN TTL phiên đăng nhập"* ⇒ ⛔ không đóng được `T-7` trước hàng này | **Dev đề xuất, Founder duyệt** | **MVP1**, cùng gói với `T-7` |
| 4 | — | ⭐ **Bảng inbox webhook ⛔ chưa có chỗ trong closed list.** [ADR-005 `Q1`](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) liệt kê **12** bảng `public` và `G-2` chốt đó là **closed list** — ⛔ **không có** bảng inbox nào trong đó, trong khi `AU-6` bắt buộc phải có. ⛔ **File này ⛔ không tạo và ⛔ không đặt tên bảng.** ⚠️ Thêm bảng ⇒ **phải sửa ADR-005 trước** | **Architect** (sửa ADR-005) | Trước khi tiêu thụ webhook vendor **đầu tiên** |
| 5 | — | ⚠️ **Có cần webhook auth ở MVP1 hay không — cũng còn mở.** Đường thay thế là **JIT provisioning**: tạo dòng `user` ở request đã xác thực đầu tiên (`AUTH-E3`), ⛔ không cần webhook. ⛔ **File này ⛔ không chọn** — chọn sai hướng làm hàng #4 hoặc trở nên bắt buộc, hoặc trở nên thừa | **Architect + dev** | Khi chốt vendor |
| 6 | — | **Luồng tạo `tenant` + `membership` lần đầu (onboarding).** ⛔ Không tài liệu nguồn nào chốt: `SRS-FR-32` nhắc *"onboarding"* nhưng **chỉ** trong ngữ cảnh ba tầng giá. ⇒ `AUTH-E4` **fail-closed** cho tới khi hàng này đóng | **Lô API (`Endpoint-*`) + PM** | Trước endpoint đăng nhập đầu tiên |
| 7 | `T-16` (`b-1`) | **Lưu / xoay secret của vendor** (client secret, signing key, JWKS cache config) | **Dev** | Sau khi **platform được mua** |
| 8 | `T-27` (`b-2`) | ⚠️ **BYOK — lưu / mã hoá / THU HỒI API key của KHÁCH.** ⛔ **Ngoài phạm vi run này**: đóng đúng nghĩa cần **một ADR mới**. ⇒ **nợ kỹ thuật**. ⛔ **Cấm** ghi credential của khách vào DB hoặc log trước khi hàng này đóng (`C-12`). ⛔ Và ⛔ **tuyệt đối không** cắm key BYOK vào metadata của vendor auth *"cho tiện"* | **Architect + Founder** (theo PM run-state `E22`) | Trước khi **BYOK bật** (MVP4) |

---

## 4. Interface / seam

### 4.1 Ba bề mặt — và chỉ ba

| Bề mặt | Ở đâu | Được dùng SDK vendor? |
|---|---|:--:|
| Đăng nhập / đăng ký / quên mật khẩu | **Frontend** (SPA + PKCE) | ✅ Có |
| Verify token trên đường request | **Backend, một middleware duy nhất** | ⛔ **KHÔNG** — chỉ JWKS chuẩn |
| Nhận sự kiện vendor | **Một adapter webhook** | ✅ Có (nếu hàng #5 của [§3](#3-cái-gì-còn-mở) chốt là *cần*) |

### 4.2 Cổng vào duy nhất — hình dạng hàm

> ⭐ **Toàn bộ tri thức về vendor bị nhốt sau một hàm**: nhận access token, trả **duy nhất** `external_auth_id` (chính là `sub`).
> ⛔ **Hàm này ⛔ không được trả về `tenant_id`, ⛔ không trả role, ⛔ không trả bất kỳ claim nào được dùng cho quyết định authorization** — nếu nó trả, `AU-2` bị phá ngay tại chữ ký hàm.

**Trình tự trên đường request** — cơ chế thuộc [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md), ⛔ file này ⛔ không đặc tả lại; bảng dưới chỉ ghi **ai sở hữu bước nào**:

| Bước | Nội dung | Sở hữu |
|:--:|---|---|
| 1 | Verify token → `external_auth_id` | ⭐ **Integration này** |
| 2 | `external_auth_id` → `public."user".id` → `tenant_id` qua `public.membership` | Data model của ta ([`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md)) |
| 3–6 | `BEGIN` → bơm tenant context → chạy handler → `COMMIT` | [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |

⚠️ **Bước 2 chứa một vòng lặp đã được giải ở ADR-006**: để đọc `membership` cần tenant context, mà phải đọc `membership` mới biết tenant. Lời giải là **đúng một** hàm `SECURITY DEFINER` hẹp — và đó là **một trong ba bề mặt đặc quyền cố định** (`C-11`, [Spec-Security-Threat-Model §4.2](../Security/Spec-Security-Threat-Model.md)) phải được review **như code bảo mật**. ⛔ File này ⛔ không nới chữ ký hàm đó.

### 4.3 Đổi vendor đụng vào đâu — bảng chi phí đã được giới hạn TRƯỚC

| Điểm chạm | Việc phải làm |
|---|---|
| Cấu hình JWKS / issuer | Đổi biến môi trường |
| `public."user".external_auth_id` | **Remap đúng MỘT cột** — ⛔ mọi FK nghiệp vụ không đổi |
| Frontend | Đổi SDK |
| Adapter webhook | Viết lại **một** adapter |

### 4.4 ⛔ Bốn anti-seam — ⛔ CẤM, kèm lý do

| ⛔ Cấm | Vì sao |
|---|---|
| ⛔ Dùng **"Organizations"** của vendor làm `tenant` | ⚠️ **Đây là chỗ hấp dẫn nhất và là chỗ một dev sẽ làm ngược theo bản năng.** Ba lý do độc lập ở [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) `Alternatives` mục F — tóm tắt: RLS ⛔ mất thứ để neo, và vendor từ *"đổi được bằng một cột"* thành *"⛔ không đổi được"* |
| ⛔ Đọc `tenant_id` hoặc role **từ claim** | `AU-2`. Token là bản sao đã ký của quá khứ |
| ⛔ Cache `tenant_id` **xuyên request** | `AU-7`. Tạo lại đúng cửa sổ không nhất quán vừa tránh |
| ⛔ Cho worker gọi vendor auth để *"lấy ngữ cảnh"* | `AU-5`. Worker ⛔ không có request, và job đã mang sẵn `tenant_id` |

---

## 5. Retry & error taxonomy

> ⭐ **Quy tắc phân loại — áp cho mọi hàng dưới**: chỉ lỗi **transient** mới được retry. Lỗi **permanent** và lỗi **security** ⛔ **không bao giờ** retry. ⛔ **Không có hàng nào fail-open.**

| Mã | Tình huống | Loại | Hành vi bắt buộc | ⛔ Cấm |
|:--:|---|:--:|---|---|
| `AUTH-E1` | Token thiếu / sai chữ ký / hết hạn | permanent | Trả **401**. ⛔ Server ⛔ không retry. **Client** làm mới token qua vendor rồi thử lại **đúng một lần** — cùng khuôn với signed URL hết hạn ([ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 5) | ⛔ Không coi *"hết hạn"* là lỗi hệ thống |
| `AUTH-E2` | ⭐ JWKS ⛔ không lấy được, hoặc `kid` lạ | transient | JWKS được cache theo cấu hình. Miss ⇒ **retry có backoff, số lần CÓ TRẦN**; hết trần ⇒ **503 fail-closed** | ⛔⛔ **TUYỆT ĐỐI không fail-open** (*"⛔ không verify được thì cho qua"*). Đây là lỗ hổng đắt nhất của cả bề mặt |
| `AUTH-E3` | Verify OK nhưng ⛔ chưa có dòng `public."user"` | bình thường | Tạo dòng **idempotent** dựa trên `UNIQUE(external_auth_id)`: hai request đồng thời ⇒ một thắng, một **bắt lỗi unique rồi đọc lại** | ⛔ Không *"check-rồi-insert"* — đó là race condition |
| `AUTH-E4` | Có `user` nhưng ⛔ **không có** `membership` | permanent | **403 fail-closed** | ⛔ **Không tự tạo `tenant` im lặng** — luồng onboarding là hàng #6 của [§3](#3-cái-gì-còn-mở) |
| `AUTH-E5` | Tra `membership` ra **nhiều hơn một** `tenant_id` | permanent | ⭐ **Lỗi fail-closed.** Ở horizon này quan hệ là **1:1** (`D-08` hoãn team nhiều thành viên) và hàm phân giải trả **đúng một** `tenant_id` | ⛔ **Không tự chọn dòng đầu tiên** — chọn bừa tenant là **rò rỉ chéo tenant** |
| `AUTH-E6` | Vendor auth **sập** | transient (ngoài tầm) | Đăng nhập **mới** thất bại. Request có token còn hạn vẫn verify được nhờ JWKS cache. ⭐ **Job đang chạy ở worker vẫn chạy** — hệ quả sẵn có của `AU-5` | ⛔ **Không dựng "chế độ khẩn cấp bỏ qua auth"** dưới bất kỳ tên gọi nào |
| `AUTH-E7` | Webhook: **chữ ký sai** | security | **Từ chối**, ghi sự kiện bảo mật, ⛔ không xử lý | ⛔ Không retry, ⛔ không *"xử lý tạm rồi verify sau"* |
| `AUTH-E8` | Webhook: **nhận trùng** | bình thường | **No-op** nhờ khoá idempotency ở inbox (`AU-6`) | ⛔ Không tạo hai hệ quả |
| `AUTH-E9` | Webhook: **loại sự kiện lạ** | bình thường | Lưu thô vào inbox, ⛔ **không hành động** | ⛔ Không đoán ngữ nghĩa |

⚠️ **Ba quy tắc bao trùm bảng trên:**
1. Mọi phản hồi lỗi ra ngoài tuân `C-5` — ⛔ không biến *"không thuộc về bạn"* thành một mã lỗi khác *"không tồn tại"*.
2. ⛔ Token, chữ ký và secret ⛔ không bao giờ vào log (`C-4`).
3. ⚠️ `AUTH-E2` và `AUTH-E4` cùng có một cám dỗ: **nới ra cho hết lỗi**. Cả hai là **fail-closed có chủ ý** — cùng tinh thần với [ADR-006 `D4.3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md): `0 row` là **fail-closed**, ⛔ không phải *"không có dữ liệu"*.

---

## 6. Chi phí

> ⛔ **Không dán giá, phí hay hạn mức nào vào file này** ([ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md)). Mọi con số phải tra **tại thời điểm mua**.

| Loại | Nội dung |
|---|---|
| **Chi phí vendor** | Mô hình giá của lớp vendor này thường tính theo **người dùng hoạt động**. **Tiêu chí bắt buộc**, ⛔ không phải con số: phải có gói dùng được ở mức **doanh thu bằng 0** |
| **Chi phí ẩn 1 — mỗi request tốn thêm một truy vấn `membership`** | Đây là **cái giá có chủ ý** của việc ⛔ không tin claim (`AU-2`). ⛔ Không được "tối ưu" bằng cache xuyên request (`AU-7`) |
| **Chi phí ẩn 2 — một adapter + một bảng chỉ để nhận webhook** | Chỉ phát sinh nếu hàng #5 của [§3](#3-cái-gì-còn-mở) chốt là *cần*. ⚠️ Bảng đó ⛔ chưa có chỗ trong closed list (hàng #4) |
| **Chi phí ẩn 3 — ta tự viết phần quản lý thành viên** | Chưa tới ở horizon này vì `D-08` **hoãn** team nhiều thành viên có role. ⛔ Không trả trước bằng cách mua tầng enterprise |
| **Chi phí đổi vendor** | ⭐ **Đã được giới hạn TRƯỚC khi biết chọn đúng hay sai** — xem [§4.3](#43-đổi-vendor-đụng-vào-đâu--bảng-chi-phí-đã-được-giới-hạn-trước) |
| ⛔ **Không thuộc COGS mỗi chapter** | Bề mặt này ⛔ **không** sinh `usage_event` và ⛔ **không** nằm trong chuỗi chi phí sinh ảnh. Ghi ra để lô sau ⛔ không trộn hai loại chi phí vào một con số |

---

## Tài liệu tham khảo

**Tầng 020 — Requirements**
- [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) — `SRS-FR-01` (`D-11`) · `SRS-FR-03` (`D-12`) · `SRS-NFR-01` (`D-09`) · `SRS-NFR-08` (vendor `TBD`) · `SRS-NFR-15` · `SRS-NFR-26` (`D-08`) · §5.2 hàng `b-1`, `b-2`, `b-4`

**Tầng 022 — User Stories**
- [Story-Buy-Authentication-Provider](../../022-User-Stories/Backlog/Story-Buy-Authentication-Provider.md)
- [Story-Tenant-User-Membership-As-Three-Entities](../../022-User-Stories/Backlog/Story-Tenant-User-Membership-As-Three-Entities.md)

**Tầng 030 — Architecture** *(chỉ đọc, ⛔ không sửa)*
- [ADR-003 — Auth & billing vendor](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) — ⭐ nguồn duy nhất của 8 điều seam
- [ADR-004 — Object storage & signed URL](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) — ràng buộc *"TTL ngắn hơn phiên đăng nhập"*
- [ADR-005 — Vị trí schema nhóm bảng platform](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) — `Q1`, `G-2` closed list
- [ADR-006 — Bơm tenant context cho RLS](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) — `D3`, `D4`
- [ADR-010 — Cô lập tenant bằng RLS](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md)
- [SDD-Comic-Studio](../Architecture/SDD-Comic-Studio.md) — §6.1, §7.4

**Tầng 030 — Schema**
- [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md) — `public.tenant` / `public."user"` / `public.membership`

**Tầng 030 — Security** *(⛔ không lặp lại nội dung)*
- [Spec-Security-Threat-Model](../Security/Spec-Security-Threat-Model.md) — §4.2 `C-4`, `C-5`, `C-9`, `C-11`, `C-12`
- [Spec-Security-Tenant-Isolation](../Security/Spec-Security-Tenant-Isolation.md)
- [Spec-Security-Legal-Compliance](../Security/Spec-Security-Legal-Compliance.md) — §5 (`SRS-NFR-15`), §8 (bảng `TBD`)

**Tầng 010 — Planning**
- [MVP-Scope](../../010-Planning/MVP-Scope.md) — `E4`
- [PM run-state](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md) — `E22` (chủ của `T-27`)

**Spec anh em**
- [Spec-Integration-Billing-Provider](./Spec-Integration-Billing-Provider.md) — cùng khuôn seam vendor (điều 6, 7, 8 của ADR-003), khác vòng đời; ⚠️ **hàng inbox webhook được ghi ở cả hai file** vì nó chạm cả hai
- *(⛔ chưa tồn tại tại thời điểm viết — nêu bằng plain text, ⛔ cố ý không tạo link)*: `Endpoint-*.md` của lô API.
