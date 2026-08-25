---
id: STORY-E-04
type: story
status: draft
created: 2026-08-24
---

# Story-Buy-Authentication-Provider

## 1. Story

Là **Founder (operator)**, tôi muốn **mua auth thay vì tự viết**, để **không đốt hai tháng và vẫn có lỗ hổng**

## 2. Part of

- Epic cha: [Epic-Multi-Tenancy-And-Platform](../Epics/Epic-Multi-Tenancy-And-Platform.md)
- BRD: [BRD-005-Multi-Tenancy-And-Platform](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md) — `BR-005-04` (phần auth, MVP1; phần billing thuộc `Story-Buy-Billing-Provider`, MVP3, ngoài horizon)
- Use Case liên quan: Epic-E **không sở hữu UC riêng** ([BRD-005 §7.2](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md#72-use-case)) — *"luồng signup/tạo tenant không có UC vì `E4` là 'mua auth, không tự viết' ⇒ luồng đó do vendor sở hữu; viết spec cho thứ mình không điều khiển là spec không thực thi được"*. Story này là **yêu cầu cấu hình**, không phải một luồng người dùng do đội tự thiết kế.

## 3. Bối cảnh & nguồn

Đây là hàng **`E4`** của [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope): *"Mua auth + billing (không tự viết)"* — `❌` ở MVP0 → `✅ auth` từ **MVP1** (phần billing đạt `✅ +billing` ở MVP3, ngoài phạm vi Story này). Căn cứ: `Analysis §5.7` — *"tự viết auth là cách nhanh nhất để một dev đốt hai tháng và vẫn có lỗ hổng"*.

Không có exit criterion `M1-x` riêng cho việc mua auth trong [Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) — ghi rõ khoảng trống này thay vì bịa số. Exit criterion cấp mốc dùng làm anchor là **`M1-1`** (mốc MVP1): auth vendor cấp `user.id` là điều kiện để mô hình `tenant`/`user`/`membership` và cột `tenant_id` trên bảng nghiệp vụ (mà `M1-1` đo trực tiếp) có một nguồn định danh xác thực đằng sau nó.

Ràng buộc dự án: [Charter §7 C1](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints) — đội **1 người + AI assist, không funding, không ngân sách marketing** `[CHỐT]` CF-1.2 — là lý do trực tiếp buộc phải mua thay vì tự viết.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Luồng signup/login/session của sản phẩm chạy hoàn toàn qua auth provider bên thứ ba — đo bằng: rà soát codebase, 0 dòng code tự cài đặt password hashing/OTP/session token tự viết
- [ ] Mỗi user đăng nhập thành công có `user.id` khớp với định danh (external id) do provider cấp, và được map vào bảng `user`/`membership` nội bộ — đo bằng: test login end-to-end, kiểm tra row `user` được tạo hoặc khớp đúng external id của provider
- [ ] Đăng xuất (logout) vô hiệu hoá session ở phía provider — đo bằng: gọi lại một endpoint yêu cầu xác thực sau logout, kỳ vọng lỗi 401

### Đường không hạnh phúc (unhappy path)

- [ ] Provider auth bị timeout/trả lỗi 5xx — hệ thống trả lỗi tường minh cho client, không crash, và **không cho qua bằng cơ chế fallback không xác thực** — đo bằng: giả lập provider trả lỗi, kỳ vọng response lỗi rõ ràng, không có session nào được cấp
- [ ] Webhook/callback đồng bộ user từ provider vào bảng nội bộ chạy **idempotent** khi nhận trùng event — đo bằng: gửi lại đúng một webhook event 2 lần, kiểm tra không tạo ra 2 row `user` trùng nhau

### Ràng buộc cứng không được vi phạm

- `C1` ([Charter §7](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints)): đội 1 người, không funding ⇒ mua, không tự viết auth

### Story này KHÔNG làm

- Không tự viết password hashing, MFA, hay OTP — mọi cơ chế xác thực nằm ở provider
- Không tích hợp billing provider — thuộc `Story-Buy-Billing-Provider` (MVP3, ngoài horizon)
- Không xây SSO/SAML — thuộc `E8`, hoãn Full Scope, chưa có mốc
- Không chọn tên vendor cụ thể trong tài liệu này — chỉ chốt là "mua, không tự viết"; lựa chọn vendor `TBD`, sẽ được đặc tả tại tầng 030-Specs

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~12h** `[EM]` | Trong trần 16h — tích hợp SDK provider, map webhook → bảng `user`/`membership` nội bộ, viết test idempotency và test lỗi provider |
| `E_hitl` | **0** | Story không tạo ra hoặc tiêu thụ HITL gate lặp lại theo chapter — đây là cấu hình vendor một lần |

## 6. INVEST

- **I (Independent)**: ✅ — không nằm trong bảy Story vỡ ở [`findings/business-analyst.md` §4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md#410-bảy-story-sẽ-vỡ-khi-cắt-lô--pm-cần-biết-trước); độc lập về deliverable — cấu hình vendor không cần chờ hai Story định danh khác hoàn tất, dù cả ba nên chạy cùng mốc MVP1 vì lý do thứ tự nghiệp vụ.
- **S (Small)**: ✅ — phạm vi rõ: tích hợp một provider có sẵn + map webhook, không bao gồm billing hay SSO.

---

_Created by architect_
_Author: trisjr_
