---
id: STORY-E-03
type: story
status: draft
created: 2026-08-24
---

# Story-Per-Tenant-Object-Storage-No-Cross-Dedup

## 1. Story

Là **khách hàng SaaS**, tôi muốn **file của tôi nằm ở `tenant/{tenant_id}/{sha256}` và KHÔNG bị dedup chéo tenant**, để **không có ai chia sẻ artifact của tôi một cách vô hình**

## 2. Part of

- Epic cha: [Epic-Multi-Tenancy-And-Platform](../Epics/Epic-Multi-Tenancy-And-Platform.md)
- BRD: [BRD-005-Multi-Tenancy-And-Platform](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md) — `BR-005-03`
- Use Case liên quan: Epic-E **không sở hữu UC riêng** ([BRD-005 §7.2](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md#72-use-case)). Storage tách tenant là precondition ngầm của mọi UC ghi/đọc file, ví dụ [UC-01-Upload-And-Ingest-Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) (upload chapter) và [UC-06-Generate-Panel-And-Pick-Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) (lưu ảnh sinh ra)

## 3. Bối cảnh & nguồn

Đây là hàng **`E3`** của [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope): *"Object storage `tenant/{tenant_id}/{sha256}`, không dedup chéo tenant"* — `❌` ở MVP0 → `✅` từ **MVP1**. Căn cứ: `Analysis §5.7 #4` — *"dedup chéo mâu thuẫn trực tiếp với lập luận bản quyền"* của dự án. Đây cũng là **seam #2** ở [MVP-Scope §4.2](../../010-Planning/MVP-Scope.md#42-microservices--vector-db-12--cắt-cf-92): Object Storage **content-addressed**, tách khỏi DB từ ngày đầu.

Không có exit criterion `M1-x` riêng cho hạng mục storage trong [Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) — ghi rõ khoảng trống này thay vì bịa số. Exit criterion cấp mốc dùng làm anchor là **`M1-1`** (mốc MVP1, isolation dữ liệu tổng thể): Story này mở rộng đúng nguyên tắc "không rò rỉ chéo tenant" của `M1-1` sang lớp object storage, nơi RLS (một cơ chế của Postgres) không áp dụng được.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Mọi object ghi vào storage có key đúng theo pattern `tenant/{tenant_id}/{sha256}` — đo bằng: upload N file test, kiểm tra path trả về khớp regex `^tenant/[0-9a-f-]+/[a-f0-9]{64}$`, N/N khớp
- [ ] Hai tenant khác nhau upload file có nội dung giống hệt nhau (cùng `sha256`) tạo ra **2 object riêng biệt**, không share — đo bằng: tenant A và tenant B cùng upload một file giống hệt, kiểm tra tồn tại đúng 2 object ở 2 path khác nhau (`tenant/{A}/{hash}` và `tenant/{B}/{hash}`), không object nào bị reference chéo
- [ ] Signed URL trả về cho client có thời hạn hết hạn (không phải URL vĩnh viễn) — đo bằng: kiểm tra field hết hạn tồn tại và có giá trị > thời điểm hiện tại
- [ ] Bucket/prefix không cho phép truy cập public (không có ACL public-read) — đo bằng: gọi GET trực tiếp bằng URL không ký, kỳ vọng nhận lỗi truy cập bị từ chối (403/Access Denied)

### Đường không hạnh phúc (unhappy path)

- [ ] Upload lại một file trùng `sha256` trong **cùng một tenant** không tạo object thứ hai (content-addressed trong phạm vi tenant) — đo bằng: upload lại file giống hệt trong cùng tenant, kiểm tra vẫn chỉ có 1 object tồn tại ở path đó
- [ ] Request lấy object bằng key thuộc tenant khác (đoán path) bị từ chối ở tầng ứng dụng, không dựa vào việc key khó đoán làm biện pháp bảo mật — đo bằng: gọi API lấy signed URL cho object của tenant khác, kỳ vọng lỗi tường minh (403/404), không trả URL hợp lệ

### Ràng buộc cứng không được vi phạm

- `KC-5` ([MVP-Scope §6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng)) — gián tiếp: storage tách tenant là phần mở rộng của isolation `tenant_id`, dù cơ chế RLS không áp dụng ở tầng object storage

### Story này KHÔNG làm

- Không xây lifecycle/tiering policy cho object cũ — thuộc thiết kế sẽ được đặc tả tại tầng 030-Specs
- Không tích hợp CDN trong Story này
- Không xây cơ chế multipart upload cho file lớn — thuộc thiết kế sẽ được đặc tả tại tầng 030-Specs
- Không chọn vendor object storage cụ thể — chỉ chốt là **mua/dùng dịch vụ có sẵn** theo `[SRC]` `MVP-Scope §3 E3`; tên vendor `TBD`, sẽ được đặc tả tại tầng 030-Specs

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~10h** `[EM]` | Trong trần 16h — thiết lập bucket/prefix, cấu hình signed URL, viết logic tính key `tenant/{tenant_id}/{sha256}`, test dedup trong-tenant và test cấm dedup chéo-tenant |
| `E_hitl` | **0** | Story không tạo ra hoặc tiêu thụ HITL gate lặp lại theo chapter — đây là hạ tầng storage nền, chạy một lần |

## 6. INVEST

- **I (Independent)**: ✅ — không nằm trong bảy Story vỡ ở [`findings/business-analyst.md` §4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md#410-bảy-story-sẽ-vỡ-khi-cắt-lô--pm-cần-biết-trước); độc lập về deliverable với hai Story định danh (`Story-Tenant-Id-And-RLS-Everywhere`, `Story-Tenant-User-Membership-As-Three-Entities`).
- **S (Small)**: ✅ — phạm vi rõ: key schema + signed URL + cấm dedup chéo tenant, không phụ thuộc lifecycle/CDN (đã tách ra ngoài phạm vi Story và đẩy sang tầng 030-Specs).

---

_Created by architect_
_Author: trisjr_
