---
id: STORY-E-01
type: story
status: draft
created: 2026-08-24
---

# Story-Tenant-Id-And-RLS-Everywhere

## 1. Story

Là **khách hàng SaaS**, tôi muốn **dữ liệu của tôi không bao giờ lọt sang tenant khác**, để **tôi dám đưa bản thảo chưa công bố của mình vào hệ thống**

## 2. Part of

- Epic cha: [Epic-Multi-Tenancy-And-Platform](../Epics/Epic-Multi-Tenancy-And-Platform.md)
- BRD: [BRD-005-Multi-Tenancy-And-Platform](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md) — `BR-005-01`
- Use Case liên quan: Epic-E **không sở hữu UC riêng** — có chủ ý, ghi rõ ở [BRD-005 §7.2](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md#72-use-case) vì tenant isolation là một **thuộc tính xuyên suốt hệ thống** (NFR/schema requirement), không phải một tương tác goal-level của actor. Story này là **precondition ngầm** của mọi UC chạm dữ liệu người dùng, ví dụ [UC-01-Upload-And-Ingest-Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) — nơi đầu tiên biên tenant được vận dụng trên dữ liệu thật.

## 3. Bối cảnh & nguồn

Đây là hàng **`E1`** của [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope): *"`tenant_id NOT NULL` mọi bảng + cột đầu tiên mọi composite index + Postgres RLS"* — `❌` ở MVP0 (không có DB, chủ ý) → `✅` từ **MVP1 — ngày đầu**. Đây đồng thời là hàng **`KC-5`** của [MVP-Scope §6 — danh sách cứng](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng): *"không có cách nào xác minh đã sửa hết"* nếu để retrofit sau khi có dữ liệu thật.

Exit criterion tương ứng là **`M1-1`** của [Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng), mốc **MVP1**: *"`tenant_id NOT NULL` trên 100% bảng nghiệp vụ; RLS policy bật trên 100% bảng có `tenant_id`; test rò rỉ chéo tenant PASS (query của tenant A không trả về 1 row nào của tenant B)"*. [Roadmap §6.2](../../010-Planning/Roadmap.md#62-bảng-phụ-thuộc) xếp `tenant_id + RLS ở MVP1` là **phụ thuộc CỨNG** chặn mọi tính năng multi-tenant sau đó.

Nền lý thuyết: [Glossary.md](../../999-Resources/Glossary.md) mục `tenant_id` (*"phải là cột đầu tiên của mọi composite index, `NOT NULL`, có từ ngày đầu; thêm sau là một cuộc migration xuyên toàn bộ schema"*) và mục `RLS` (*"cơ chế Postgres chặn truy cập ở tầng DB theo hàng ... với một dev không có code review, đây là bảo hiểm rẻ nhất tồn tại; RLS không bảo vệ được join thực hiện phía application"*).

Sản phẩm là SaaS thương mại multi-tenant — nền tảng cho **người khác tự upload truyện của họ** `[CHỐT]` CF-1.1 — nên `tenant_id` không phải một tính năng, nó là **tiền đề của mọi bảng** ([Epic cha mục 2](../Epics/Epic-Multi-Tenancy-And-Platform.md#2-mục-tiêu-epic)).

## 4. Acceptance Criteria

### Xác minh được

- [ ] `tenant_id NOT NULL` tồn tại trên 100% bảng nghiệp vụ của cả 3 schema (`story`/`comic`/`generation`) — đo bằng: script liệt kê toàn bộ bảng nghiệp vụ và kiểm tra ràng buộc `NOT NULL` trên cột `tenant_id`; 0 bảng thiếu
- [ ] `tenant_id` là cột **đầu tiên** trong định nghĩa của mọi composite index — đo bằng: truy vấn catalog Postgres (`pg_index` + `pg_attribute`) đối chiếu thứ tự cột của từng composite index; 0 index có `tenant_id` không phải cột đầu
- [ ] RLS được bật (`ROW LEVEL SECURITY` + có ≥1 `CREATE POLICY`) trên 100% bảng có `tenant_id` — đo bằng: đếm bảng trong `pg_policies` phải bằng đúng số bảng có cột `tenant_id`
- [ ] Bộ test rò rỉ chéo tenant PASS 100% trên toàn bộ bảng nghiệp vụ — đo bằng: seed 2 tenant A, B có dữ liệu tương ứng; mọi câu query chạy dưới session tenant A trả về **0 row** thuộc tenant B (`M1-1`)

### Đường không hạnh phúc (unhappy path)

- [ ] Insert một row nghiệp vụ thiếu `tenant_id` bị DB từ chối ở tầng constraint, không lọt qua bằng validation tầng ứng dụng — đo bằng: gọi insert thiếu `tenant_id`, kỳ vọng lỗi vi phạm ràng buộc, 0 row được tạo
- [ ] Một session không set biến `app.current_tenant` (hoặc set giá trị không hợp lệ) bị RLS chặn trả về **0 row** thay vì lỗi 500 không kiểm soát được — đo bằng: gọi query khi biến session rỗng/sai định dạng, kỳ vọng 0 row, không có exception làm crash tiến trình
- [ ] Hai request đồng thời từ hai tenant khác nhau tái sử dụng cùng một connection trong pool không làm rò rỉ biến `app.current_tenant` sang request kia — đo bằng: test tải N request xen kẽ 2 tenant trên cùng pool, kiểm tra không request nào nhận nhầm dữ liệu tenant khác

### Ràng buộc cứng không được vi phạm

- `KC-5` ([MVP-Scope §6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng)): danh sách duy nhất không mở ra thương lượng scope
- `C1` ([Charter §7](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints)): đội 1 người, không code review ⇒ RLS là lớp phòng thủ bắt buộc, không phải tuỳ chọn

### Story này KHÔNG làm

- Không dùng mô hình schema-per-tenant hoặc database-per-tenant — chốt là **shared database + shared schema** (`Analysis §5.7`)
- Không migrate dữ liệu sản xuất thật — MVP0 không có database (chủ ý, `C9`), nên không có dữ liệu lịch sử cần migrate tại thời điểm Story này chạy
- Không xây UI cho end-user — Story này thuần schema/backend/policy
- Không định nghĩa `tenant`/`user`/`membership` là ba entity — đó là `Story-Tenant-User-Membership-As-Three-Entities`, Story này chỉ tiêu thụ cột `tenant_id` mà entity đó cung cấp

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~24h** `[EM]` — **vượt trần 16h** | Lý do vượt trần ghi thành văn (được phép theo quy ước cắt lô): Story chạm **100% bảng nghiệp vụ** của cả 3 schema + mọi composite index + toàn bộ RLS policy + bộ test rò rỉ chéo tenant, và **không có sub-slice nào "xong" mà có nghĩa** — `KC-5` ghi rõ "không có cách nào xác minh đã sửa hết" nên không thể ước lượng như một tính năng đơn lẻ dưới 16h |
| `E_hitl` | **0** | Story không tạo ra hoặc tiêu thụ bất kỳ HITL gate nào lặp lại theo chapter — đây là hạ tầng nền tảng chạy một lần, không phải một bước trong content pipeline |

## 6. INVEST

⚠️⚠️ **Vỡ cả `I` và `S` ở mức nặng nhất của cả backlog** — theo nguyên văn lý do tại [`findings/business-analyst.md` §4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md#410-bảy-story-sẽ-vỡ-khi-cắt-lô--pm-cần-biết-trước):

> *"Chạm **100% bảng nghiệp vụ** + 100% composite index + 100% query. Không có sub-slice nào 'xong' mà có nghĩa: `tenant_id` trên 8/10 bảng = **vẫn rò rỉ**. `MVP-Scope` KC-5: 'không có cách nào xác minh đã sửa hết' ⇒ **DoD phải là test rò rỉ chéo tenant PASS (M1-1), không phải số bảng đã sửa**."*

- **I (Independent)**: ⚠️⚠️ — không tách được thành lô con vì mọi lô con để lại một khoảng trống bằng chính rủi ro mà Story tồn tại để chặn.
- **S (Small)**: ⚠️⚠️ — không tồn tại một trần giờ-người hợp lý mà vẫn giữ nguyên tiêu chí "xong" (test PASS 100%, không phải % bảng); `E_build` vì vậy vượt trần 16h và **không được split** — split một Story mà DoD là một test nhị phân toàn cục chỉ tạo ra ảo giác tiến độ.

**Definition of Done bắt buộc**: ⭐ **Test rò rỉ chéo tenant PASS (`M1-1`)**, KHÔNG phải "đã thêm `tenant_id` cho N/M bảng". Đếm bảng là một chỉ số có thể tăng trong khi kết quả vẫn là thất bại — ghi tường minh theo cảnh báo riêng của module E trong prompt dispatch.

---

_Created by architect_
_Author: trisjr_
