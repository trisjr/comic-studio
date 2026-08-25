---
id: STORY-E-02
type: story
status: draft
created: 2026-08-24
---

# Story-Tenant-User-Membership-As-Three-Entities

## 1. Story

Là **Founder (architect)**, tôi muốn **`tenant` / `user` / `membership` là ba entity riêng kể cả khi quan hệ đang là 1:1**, để **ngày bán gói team không phải migrate mô hình định danh**

## 2. Part of

- Epic cha: [Epic-Multi-Tenancy-And-Platform](../Epics/Epic-Multi-Tenancy-And-Platform.md)
- BRD: [BRD-005-Multi-Tenancy-And-Platform](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md) — `BR-005-02`
- Use Case liên quan: Epic-E **không sở hữu UC riêng** ([BRD-005 §7.2](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md#72-use-case)) — luồng signup/tạo tenant do vendor auth sở hữu (`Story-Buy-Authentication-Provider`). Story này là mô hình định danh nền mà mọi UC gắn dữ liệu vào `tenant_id` phụ thuộc, ví dụ [UC-01-Upload-And-Ingest-Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md)

## 3. Bối cảnh & nguồn

Đây là hàng **`E2`** của [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope): *"`tenant` / `user` / `membership` là ba entity riêng (kể cả khi 1:1)"* — `❌` ở MVP0 → `✅` từ **MVP1**. Căn cứ: `Analysis §5.7` quyết định #2. [MVP-Scope §5.3 hàng #8](../../010-Planning/MVP-Scope.md#53-bốn-thành-phần-hoãn) ghi rõ: *"`membership` đã chuẩn bị sẵn cho ngày đó"* — ngày bán gói team.

Không có exit criterion `M1-x` riêng cho hạng mục này trong [Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) — ghi rõ khoảng trống này thay vì bịa số. Exit criterion cấp mốc dùng làm anchor là **`M1-1`** (mốc MVP1): *"`tenant_id NOT NULL` trên 100% bảng nghiệp vụ ... test rò rỉ chéo tenant PASS"* — mô hình `tenant`/`user`/`membership` đúng là **tiền đề** để `tenant_id` trên các bảng nghiệp vụ khác trỏ đúng chỗ; Story này không tự có `M1-x` nhưng Story `Story-Tenant-Id-And-RLS-Everywhere` (mà `M1-1` đo trực tiếp) không có nghĩa nếu ba entity định danh này bị gộp sai.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Schema có đúng 3 bảng riêng biệt `tenant`, `user`, `membership` — đo bằng: liệt kê bảng trong schema định danh, xác nhận có mặt đủ 3 tên bảng, không bảng nào gộp hai vai trò làm một
- [ ] Bảng `membership` có khoá ngoại tới cả `tenant.id` và `user.id`, kèm ràng buộc unique trên cặp `(tenant_id, user_id)` — đo bằng: insert 2 row `membership` trùng cặp `(tenant_id, user_id)`, kỳ vọng bị DB từ chối
- [ ] Mọi bảng dữ liệu nghiệp vụ (không phải bảng định danh) trỏ `tenant_id` trực tiếp, KHÔNG dùng `user_id` làm khoá phân vùng dữ liệu — đo bằng: liệt kê toàn bộ khoá ngoại của bảng nghiệp vụ, 0 bảng dùng `user_id` làm cột phân vùng tenant

### Đường không hạnh phúc (unhappy path)

- [ ] Xoá một `user` không cascade xoá `tenant` tương ứng (một user rời đội không được xoá cả tenant) — đo bằng: test xoá `user`, xác nhận row `tenant` vẫn tồn tại
- [ ] Một `tenant` có 0 `membership` (trạng thái transient khi tenant vừa tạo, chưa gán user) không làm crash truy vấn danh sách user của tenant — đo bằng: query danh sách user của tenant rỗng, kỳ vọng trả mảng rỗng, không lỗi

### Ràng buộc cứng không được vi phạm

- —

### Story này KHÔNG làm

- Không xây UI quản lý team/role — thuộc SSO/team nhiều thành viên có role (`E8`, hoãn Full Scope, không có mốc)
- Không xây luồng invite user vào tenant hay đổi role trong membership — thuộc phạm vi cấu hình của auth vendor (`Story-Buy-Authentication-Provider`) và ngoài phạm vi horizon này
- Không thiết kế billing gắn theo `membership` — thuộc [Epic-Credit-And-Unit-Economics](../Epics/Epic-Credit-And-Unit-Economics.md)

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~8h** `[EM]` | Trong trần 16h — ba bảng + ràng buộc unique + cập nhật FK của các bảng nghiệp vụ hiện có sang `tenant_id` |
| `E_hitl` | **0** | Story không tạo ra hoặc tiêu thụ HITL gate lặp lại theo chapter — đây là mô hình định danh nền, chạy một lần |

## 6. INVEST

- **I (Independent)**: ✅ — không nằm trong bảy Story vỡ ở [`findings/business-analyst.md` §4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md#410-bảy-story-sẽ-vỡ-khi-cắt-lô--pm-cần-biết-trước); độc lập về deliverable với `Story-Tenant-Id-And-RLS-Everywhere` dù cả hai chạy cùng mốc MVP1.
- **S (Small)**: ✅ — phạm vi hẹp (ba bảng + một ràng buộc unique), nằm gọn trong trần `E_build ≤ 16h`.

---

_Created by architect_
_Author: trisjr_
