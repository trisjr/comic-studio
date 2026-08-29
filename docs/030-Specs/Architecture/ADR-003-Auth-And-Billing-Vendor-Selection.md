---
id: ADR-003
type: adr
status: draft
project: comic-studio
created: 2026-08-29
---

# ADR-003: Chọn vendor auth & billing và thiết kế seam để đổi vendor

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

## Context

> [!CAUTION]
> ⛔ **ADR này KHÔNG mở lại câu hỏi build-vs-buy.** *"Mua auth và billing, không tự viết"* đã **CHỐT** ở `D-12` — [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-03`, với lý do nguyên văn: *"tự viết auth là cách nhanh nhất để một dev đốt hai tháng và vẫn có lỗ hổng"*.
> ADR này chỉ làm **hai việc**: (1) chọn vendor, (2) thiết kế **seam để đổi vendor**.

Cái còn mở là `SRS-NFR-08` — *"Vendor cụ thể của auth / billing / object storage"* — **`CHƯA QUYẾT` → `TBD`** (`SRS` §3.E): *"Tên vendor không xuất hiện ở bất kỳ tài liệu nào"*. Phần **object storage** của `SRS-NFR-08` được xử lý ở [ADR-004](./ADR-004-Object-Storage-Vendor-And-Signed-URL.md); ADR này lo hai phần còn lại.

### Vì sao phải quyết bây giờ — hai mốc khác nhau, một seam duy nhất

| Năng lực | Mốc cần | Nguồn |
|---|---|---|
| **Auth** | **MVP1** — `E4` = `✅ auth` từ MVP1 | `MVP-Scope` §3 `E4` · findings §5 #4 |
| **Billing** | **MVP3** — ngoài horizon MVP0–MVP2 | `MVP-Scope` §3 `E4` · findings §5 #6 |

Billing là `[OoH]` nên ADR này chỉ **reserve chỗ** cho nó. Nhưng chỗ đó **phải được reserve ngay bây giờ**, vì `D-62` cấm retrofit: *"kiến trúc billing + ledger + onboarding phải đỡ được **ba tầng ngay từ đầu**"* (`SRS` `SRS-FR-32`) — tầng 1 không image gen, tầng 2 credit pack không hết hạn, tầng 3 BYOK là tuỳ chọn **mở khoá**.

### Ràng buộc kế thừa định hình seam (⛔ không mở lại)

| Ràng buộc | Mã | Hệ quả cho seam |
|---|---|---|
| `tenant` / `user` / `membership` là **BA entity riêng** ngay từ đầu; mọi dữ liệu nghiệp vụ trỏ `tenant_id`, **⛔ không trỏ `user_id`** | `D-11` | Mô hình authorization là **của ta**, ⛔ không phải của vendor |
| `tenant_id NOT NULL` mọi bảng + **RLS** là lớp phòng thủ thứ hai | `D-09` | `tenant_id` phải đến từ dữ liệu **ta kiểm soát** |
| ⛔ Cấm tenant isolation kiểu app-layer filter | `D-10` | Không được để một claim trong token quyết định phạm vi truy cập |
| **Credit ledger append-only + HOLD trước enqueue** + `CHECK (available >= 0)` ở tầng DB | `D-60` | **Entitlement là của ta**, ⛔ không phải của vendor billing |
| Ba tầng giá **⛔ không retrofit** | `D-62` | Seam billing phải tồn tại trước khi có billing |
| **Hoãn** SSO/SAML, team nhiều role | `D-08` | ⛔ Không mua tầng enterprise bây giờ; ⛔ cũng không tự viết RBAC phức tạp |
| ⛔ Không tự viết luồng thanh toán | `D-12` · `UC-10` b4 | ⛔ Không bao giờ chạm dữ liệu thẻ |
| Frontend là **SPA thuần, không SSR** | [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) điều 5 | Vendor **bắt buộc** hỗ trợ SPA + PKCE |

## Decision

### Tầng CHỐT — seam, đúng với MỌI vendor, ⛔ không đổi mà không viết ADR mới

1. **Vendor auth chỉ sở hữu: identity, credential, phiên đăng nhập, và các phương thức đăng nhập.** ⛔ Vendor **không** sở hữu `tenant`, `membership`, hay bất kỳ quyết định authorization nào (`D-11`).
2. **Bảng `user` của ta có cột `external_auth_id`** (subject do vendor phát) với ràng buộc `UNIQUE`. ⛔ **Không FK nghiệp vụ nào trỏ vào định danh của vendor.** ⇒ **Đổi vendor auth = remap đúng MỘT cột**, mọi khoá ngoại còn lại không đổi.
3. **Backend chỉ chấp nhận JWT xác thực qua JWKS theo chuẩn OIDC.** ⛔ Không SDK của vendor trong đường xử lý request. SDK vendor chỉ được xuất hiện ở **hai chỗ**: (a) frontend, (b) một adapter webhook.
4. ⭐ **Custom claim của vendor ⛔ KHÔNG BAO GIỜ là nguồn sự thật cho `tenant_id` hay role.** Token chỉ cung cấp `sub`; `tenant_id` và role được **tra từ bảng `membership` trong DB của ta** ở mỗi request.
   Lý do (và đây là lý do bảo mật, không phải thẩm mỹ): RLS (`D-09`) neo vào `tenant_id`; nếu `tenant_id` đến từ một claim đã ký, thì một token phát trước khi ta thu hồi membership **vẫn mở được dữ liệu** cho tới khi hết hạn. `D-10` nói đúng nguy cơ này ở một tầng khác — nguyên tắc giống nhau: **quyền truy cập phải neo vào trạng thái hiện tại trong DB, không neo vào một bản sao đã ký.**
5. **Worker không có HTTP request ⇒ không có token.** Job mang `tenant_id` từ **chính dòng `job`** trong DB (`D-03` bảo đảm dòng đó được ghi cùng transaction với công việc). ⛔ Worker **không được** gọi vendor auth để lấy ngữ cảnh. Ràng buộc này chuyển xuống **ADR-006**.
6. **Webhook của vendor là nguồn SỰ KIỆN, ⛔ không phải nguồn SỰ THẬT.** Mọi webhook phải: verify chữ ký → ghi vào **bảng inbox** với khoá idempotency → xử lý bất đồng bộ. Nhận trùng một sự kiện ⛔ không được tạo hai hệ quả.
7. **Vendor billing sở hữu: phương thức thanh toán, hoá đơn, nghĩa vụ thuế/VAT. ⛔ Vendor KHÔNG sở hữu entitlement.** `credit_ledger` (`D-60`) là **nguồn sự thật duy nhất** cho quyền sử dụng. Luồng đúng: vendor phát sự kiện *"đã thu tiền"* → ta ghi **một dòng ledger**. ⛔ **Cấm** đọc trạng thái subscription của vendor trong đường nóng của việc sinh ảnh.
8. **⛔ Không bao giờ chạm dữ liệu thẻ**, ⛔ không tự viết luồng thanh toán (`D-12`, `UC-10` b4).

### Tầng MẶC ĐỊNH — auth

**Clerk** làm vendor auth mặc định. Lý do neo vào ràng buộc: SDK ưu tiên React/SPA (khớp [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) điều 5), **hosted UI** nghĩa là ⛔ không phải viết một dòng UI đăng nhập/đăng ký/quên mật khẩu nào — với `SRS` §1.3 (1 dev), đó là khoản tiết kiệm lớn nhất mà seam ở trên đã làm cho vô hại.

**Ba tiêu chí nghiệm thu bắt buộc của spike** (⛔ trượt một trong ba là chuyển bậc, không thương lượng):
1. Phát ra JWT verify được bằng **JWKS chuẩn**, ⛔ không cần SDK vendor ở backend (điều 3).
2. Hỗ trợ **SPA + PKCE** hoàn chỉnh.
3. Có đường **xuất dữ liệu user** khi rời đi.

**Thang đường lui**: `1.` **Auth0** · `2.` **Supabase Auth** hoặc **WorkOS** · `3.` self-host **Keycloak/Ory** (chỉ khi ràng buộc lưu trữ dữ liệu trong nước ở [ADR-002](./ADR-002-Hosting-Platform-And-Region.md) buộc như vậy — xem `## Alternatives`).

> [!WARNING]
> ⚠️ **Phải verify trước khi mua, ⛔ ADR này không xác nhận thay**: ba tiêu chí trên + có gói dùng được ở mức doanh thu bằng 0. **Owner: dev · Mốc: kickoff MVP1, spike tối đa 1 ngày.** ⛔ **Không dán giá** — mọi con số chi phí phải tra tại thời điểm mua.

### `TBD` — billing vendor, ⛔ không tự gán

**Vendor billing = `TBD`.** Không phải vì thiếu thời gian phân tích, mà vì **ràng buộc chặn nằm ngoài kỹ thuật**: lựa chọn phụ thuộc **quốc gia của pháp nhân bán hàng** và ⛔ **không tài liệu nào trong repo trả lời điều đó**.

| Hạng mục | Nội dung |
|---|---|
| **Ai đóng** | **Founder** (quyết định pháp nhân) + dev (verify khả dụng kỹ thuật) |
| **Khi nào** | Trước khi bắt đầu **MVP3**. ⚠️ Nhưng **seam (điều 6, 7, 8) phải có từ MVP1** vì `D-62` cấm retrofit |
| **Đầu vào còn thiếu** | (a) pháp nhân bán hàng đặt ở đâu; (b) **verify khả dụng của từng PSP cho pháp nhân Việt Nam** — đây là ràng buộc **chặn**, ⛔ không phải chi tiết; (c) tỷ trọng khách trong nước / quốc tế |

**Ba lớp phương án đã cân nhắc sẵn để Founder khỏi bắt đầu từ số không:**

| Lớp | Ví dụ | Ưu | Nhược |
|---|---|---|---|
| **PSP trực tiếp** | Stripe và tương đương | Kiểm soát cao nhất, API trưởng thành nhất | ⚠️ **Nghĩa vụ VAT/thuế toàn cầu thuộc về ta** — với 1 dev đây là chi phí ẩn lớn nhất của cả ba lớp. Và khả dụng cho pháp nhân VN **phải verify** |
| **Merchant-of-record** | Paddle, Lemon Squeezy và tương đương | Vendor đứng tên người bán ⇒ **gánh luôn VAT/thuế toàn cầu** — đây là lý do lớp này đáng cân nhắc nghiêm túc cho `SRS` §1.3 | Phí cao hơn, ít kiểm soát luồng hơn, danh mục sản phẩm bị ràng buộc |
| **Cổng nội địa** | VNPay, MoMo và tương đương | Phù hợp thẻ nội địa và thói quen thanh toán trong nước | Khó phục vụ khách quốc tế; mô hình subscription/credit pack cần kiểm chứng |

⛔ **Không dán giá, phí, hay tỷ lệ chiết khấu nào vào bảng trên** — mọi con số phải tra tại thời điểm quyết định.

## Alternatives considered

### A. Tự viết auth (lưu mật khẩu, phát session)

⛔ **Không phải phương án và ⛔ không được đọc thành phương án.** `D-12` đã **CHỐT** (`SRS` `SRS-FR-03`). Mục này tồn tại **chỉ để** một run sau không tưởng rằng nó bị bỏ sót.

### B. Auth library self-host (Better Auth / Lucia / tương đương)

- **Ưu điểm thật**: dữ liệu user nằm trong chính PostgreSQL của ta ⇒ join thẳng với `membership`, ⛔ không webhook, ⛔ không phụ thuộc uptime bên ngoài; và nó rẻ.
- **Loại vì đây là ÁP DỤNG `D-12`, ⛔ không phải mở lại `D-12`**: library đưa **việc lưu credential, hash, xoay khoá, xử lý rò rỉ, chống nhồi mật khẩu** về phía ta. Đó **chính xác** là tập công việc mà `D-12` mua để tránh — *"vẫn có lỗ hổng"* trong nguyên văn `SRS` `SRS-FR-03` nói về đúng tập này. Đổi tên từ *"tự viết"* thành *"dùng library"* không đổi ai chịu trách nhiệm khi có sự cố.

### C. Self-host Keycloak / Ory

- **Ưu điểm thật**: thoả `D-12` theo nghĩa *"không tự viết"*; kiểm soát dữ liệu hoàn toàn; là **câu trả lời sẵn** nếu nghĩa vụ lưu trữ dữ liệu trong nước (`TBD` ở [ADR-002](./ADR-002-Hosting-Platform-And-Region.md)) hoá ra là có thật.
- **Loại ở MVP**: nó thêm **một service phải vận hành** — đụng thẳng điều 1 của `## Decision` trong ADR-002 và `SRS` §1.3.
- **Giữ làm bậc 3 có điều kiện**: chỉ kích hoạt khi luật sư trả lời ràng buộc dữ liệu trong nước.

### D. Auth0 · E. Supabase Auth · WorkOS

- **Auth0**: trưởng thành nhất, đường di trú và tài liệu tốt nhất, hỗ trợ SSO/SAML sẵn cho ngày `D-08` được mở lại. **Không loại — bậc 1 của đường lui**; xuống dưới Clerk chỉ vì phần *"⛔ không phải viết UI auth"* của Clerk trả trực tiếp vào `SRS` §1.3.
- **Supabase Auth**: hấp dẫn **nếu** ta dùng Supabase Postgres — vì khi đó nó tích hợp thẳng với RLS. Nhưng [ADR-002](./ADR-002-Hosting-Platform-And-Region.md) chọn managed Postgres của PaaS khác, nên mua Supabase **chỉ để lấy auth** là mất đúng lợi thế khiến nó đáng chọn. **Bậc 2.**
- **WorkOS**: mạnh ở SSO/SAML doanh nghiệp — mà `D-08` đã **hoãn**. Chọn nó bây giờ là trả tiền cho năng lực đã bị hoãn khỏi horizon. **Bậc 2.**

### F. ⚠️ Dùng "Organizations" của vendor auth làm `tenant`

- **Ưu điểm thật**: đây là **phương án hấp dẫn nhất** trong toàn ADR — vendor cho sẵn mời thành viên, role, chuyển tổ chức, UI quản lý; tiết kiệm cho 1 dev là có thật và lớn.
- **Loại dứt khoát, ba lý do độc lập**:
  1. Mâu thuẫn trực tiếp `D-11` — `tenant`/`user`/`membership` phải là **ba entity riêng của ta** ngay từ đầu.
  2. Mâu thuẫn `D-09` — `tenant_id` là cột đầu của **mọi** composite index và là biến neo của **mọi** RLS policy. Một `tenant_id` sống ở hệ thống khác thì RLS không có gì để neo, và mọi join nội bộ mất khoá.
  3. Biến vendor auth từ *"thứ đổi được bằng cách remap một cột"* thành *"thứ không đổi được"* — huỷ hoại chính seam mà ADR này tồn tại để dựng.
- ⚠️ Đây là chỗ **một dev sẽ làm ngược theo bản năng** vì nó tiết kiệm rõ ràng trong tuần đầu. Ghi lại tường minh để không ai phải phát hiện lại.

### G. Dùng trạng thái subscription của vendor billing làm entitlement

- **Ưu điểm thật**: ⛔ không phải viết ledger, ⛔ không phải đồng bộ; *"còn hạn thì cho dùng"* là mô hình đơn giản nhất có thể.
- **Loại vì**: `D-60` yêu cầu **HOLD trước khi enqueue** (*"check-rồi-gọi là race condition"*) và `CHECK (available >= 0)` **ở tầng DB**. Hai thứ đó đòi một số dư **giao dịch được trong cùng transaction với việc đẩy job** — mà trạng thái subscription của vendor là dữ liệu **từ xa, có độ trễ, đến qua webhook**. Đặt nó vào đường nóng là đưa một cuộc gọi mạng và một cửa sổ không nhất quán vào **đúng chỗ đang chống race condition**.
- Và `D-62` (ba tầng giá, credit pack **không hết hạn**, BYOK là *mở khoá*) ⛔ không biểu diễn được bằng một cờ *"subscription còn hạn"*.

### H. Tự viết luồng thanh toán / lưu thẻ

⛔ **Không phải phương án.** `D-12` + `UC-10` bước 4 đã **CHỐT**.

## Consequences

### Tích cực

- **Chi phí đổi vendor auth được giới hạn TRƯỚC khi ta biết mình chọn đúng hay sai**: remap `external_auth_id` + đổi JWKS URL + đổi SDK ở frontend. Mọi khoá ngoại nghiệp vụ không đổi vì chúng trỏ `tenant_id` (`D-11`).
- **Billing chưa chọn vẫn ⛔ không chặn MVP1**, vì seam đã dựng và `credit_ledger` là của ta. Khi Founder chốt pháp nhân, việc còn lại là viết **một** adapter webhook.
- Mọi invariant tầng DB của `D-60` (`CHECK`, HOLD, append-only) được giữ nguyên vẹn vì entitlement không rời khỏi database.

### Tiêu cực — cái gì trở nên KHÓ HƠN

1. **Mỗi request tốn thêm một truy vấn `membership`** (điều 4). Đây là cái giá có chủ ý của việc ⛔ không tin claim trong token. Được phép cache **trong phạm vi một request**; ⛔ **cấm** cache xuyên request cho tới khi có cơ chế vô hiệu hoá — nếu không ta tự tạo lại đúng lỗ hổng vừa tránh. ⇒ **ADR-006 phải bơm `tenant_id` SAU bước tra này**, không trước.
2. **Đăng nhập trở thành phụ thuộc uptime bên ngoài.** Vendor auth sập = ⛔ không ai đăng nhập được. Giảm nhẹ (một phần) là hệ quả sẵn có của `D-02`: job đang chạy ở worker **vẫn chạy**, vì worker ⛔ không phụ thuộc token (điều 5).
3. **Thêm một bảng và một đường code chỉ để nhận webhook** (điều 6). ⛔ Không bỏ được: webhook trùng lặp là chuẩn ngành, và với billing thì nhận trùng nghĩa là **cộng credit hai lần**.
4. **Ta phải tự viết phần quản lý thành viên** thay vì dùng của vendor (mục F). ⚠️ Chi phí này **chưa tới** ở horizon hiện tại vì `D-08` đã hoãn *"team nhiều thành viên có role"* — nhưng nó sẽ tới, và ADR này cố ý trả trước bằng `D-11`.
5. **Nghĩa vụ thuế/VAT là một quyết định kiến trúc trá hình.** Nếu Founder chọn lớp *PSP trực tiếp*, phần tính và nộp VAT nhiều quốc gia rơi về phía ta — với 1 dev đó là chi phí vận hành lớn hơn toàn bộ phần code billing. Đây là lý do lớp *merchant-of-record* được nêu tường minh thay vì bỏ qua.
6. **Rủi ro lịch cho MVP3 vẫn còn.** Seam có sẵn ⛔ không thay được việc chọn vendor; nếu Founder chốt pháp nhân muộn, MVP3 trượt. ADR này chỉ đảm bảo **cái trượt là một adapter, không phải kiến trúc**.

## Đã quyết ở đâu

### Kế thừa từ Phase 1 — ⛔ ADR này KHÔNG mở lại

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|---|---|
| ⭐ **MUA auth và billing, ⛔ KHÔNG tự viết** — *"tự viết auth là cách nhanh nhất để một dev đốt hai tháng và vẫn có lỗ hổng"* | `D-12` | [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-03` · §4.3 · `MVP-Scope` §3 `E4` |
| `tenant` / `user` / `membership` là **ba entity riêng**; dữ liệu nghiệp vụ trỏ `tenant_id`, ⛔ không trỏ `user_id` | `D-11` | `SRS` `SRS-FR-01` · `MVP-Scope` §3 `E2` |
| `tenant_id NOT NULL` mọi bảng + cột đầu mọi composite index + **RLS** lớp phòng thủ thứ hai | `D-09` | `SRS` `SRS-NFR-01` |
| ⛔ Cấm tenant isolation kiểu *"filter `tenant_id` ở tầng ứng dụng"* | `D-10` | `SRS` §3.E |
| Job queue trong Postgres, transactional enqueue (job mang sẵn ngữ cảnh) | `D-03` | `SRS` `SRS-FR-25` · §2.3 |
| Worker là process riêng — ⛔ không có HTTP request | `D-02` | `SRS` `SRS-NFR-03` · §2.3 |
| **Hoãn** SSO/SAML, team nhiều thành viên có role, self-serve refund | `D-08` | `SRS` `SRS-NFR-26` · §2.3 |
| **Credit ledger append-only + HOLD trước enqueue** + `CHECK (available >= 0)` tầng DB + hold reaper | `D-60` | `SRS` `SRS-FR-28` · §3.F · §5.1 · `UC-10` b8, b11 |
| Hard quota cưỡng chế **trước** khi enqueue | `D-61` | `SRS` `SRS-FR-29` |
| **Ba tầng giá ⛔ không retrofit** (không image gen · credit pack không hết hạn · BYOK là mở khoá) | `D-62` | `SRS` `SRS-FR-32` |
| ⛔ Không subscription phẳng unlimited, ⛔ không free tier kiểu *"100 ảnh/ngày"* | `D-63` | `SRS` `SRS-NFR-24` |
| Đội **1 người + AI assist** | — | `SRS` §1.3 |

### ADR này quyết (phần Phase 1 **cố ý** để mở)

| Quyết định | Mã | Nguồn (file + mã requirement) |
|---|---|---|
| **Vendor auth** (MẶC ĐỊNH: Clerk) + thang đường lui + tiêu chí nghiệm thu spike | `SRS-NFR-08` (`CHƯA QUYẾT` → `TBD`) | `SRS` §3.E · [findings/architect](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) §1.8, §2.1 |
| **Seam đổi vendor** (8 điều ở tầng CHỐT) — phần này ADR đóng lại, ⛔ không để mở | — (dẫn xuất từ `D-11`, `D-09`, `D-60`) | Như trên |
| **Vendor billing** — ở lại `TBD` có chủ đích, kèm owner (**Founder**) và mốc (**trước MVP3**) | `SRS-NFR-08` | `SRS` §3.E |
