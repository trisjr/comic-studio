---
id: STORY-D-01
type: story
status: draft
created: 2026-08-24
---

# Story-Story-Bible-Editor-Form

## 1. Story

Là tác giả truyện chữ, tôi muốn **sửa nhân vật / trang phục / địa điểm / state bằng form**, để **kiểm soát được tài sản tích luỹ của mình**

## 2. Part of

- Epic cha: [Epic-Minimum-Editor](../Epics/Epic-Minimum-Editor.md)
- BRD: [BRD-004-Minimum-Editor](../../020-Requirements/BRD/BRD-004-Minimum-Editor.md)
- Use Case liên quan: [UC-02-Review-And-Edit-Story-Bible](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) — đây chính là thành phần `#5`, nơi UC-02 được thực thi trên UI

## 3. Bối cảnh & nguồn

Đây là **thành phần bắt buộc `#5`** trong năm thành phần editor tối thiểu, chiếm **4–6%** `[EM]` effort (mẫu số SaaS) của tổng ~20–25% editor — [MVP-Scope §5.2](../../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas), hàng `D1` của [MVP-Scope §3](../../010-Planning/MVP-Scope.md). Đây là thành phần **duy nhất** trong Epic-D chạy ở **MVP1** — theo Epic mục 2, đây là *"nơi moat lộ ra với khách hàng"*.

Story này không có exit criterion `M1-x` riêng của chính nó. Nó gắn chặt với **M1-3** ([Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng), mốc MVP1): *"extraction đạt ≥80% entity (nhân vật + địa điểm) khớp với Story Bible viết tay của MVP0"* `[EM]` ngưỡng do BA tự định nghĩa. Lý do nghiệp vụ để coi M1-3 là điều kiện ra của Story này (suy luận của PO, không phải phát biểu trực tiếp của nguồn): ngưỡng 80% chỉ có ý nghĩa vận hành nếu phần **≤20% sai** sửa được bằng chính form này — nếu không có UI sửa, một extraction dưới ngưỡng là một lỗi không có đường khắc phục. Cùng lý do này đã được ghi tại [Epic-Minimum-Editor mục 5](../Epics/Epic-Minimum-Editor.md#5-definition-of-done-cấp-epic).

## 4. Acceptance Criteria

### Xác minh được

- [ ] Tác giả mở được danh sách **nhân vật** của một chapter đã ingest, và sửa **tên / mô tả / trang phục hiện tại** — đo bằng: sau khi lưu, `GET` lại entity trả về đúng giá trị vừa sửa
- [ ] Tác giả mở được danh sách **địa điểm** của một chapter và sửa **tên / mô tả** — đo bằng: `GET` lại trả về đúng giá trị vừa sửa
- [ ] Tác giả sửa được **state của một nhân vật tại một event cụ thể** (ví dụ trang phục ở chương 40 khác chương 10) — đo bằng: sau khi lưu, `state_at(N)` (theo cơ chế của `Story-Timeline-State-Resolver`) trả về đúng giá trị đã sửa cho event N, và **không** đổi giá trị của các event khác
- [ ] Mỗi lần lưu một thay đổi qua form này sinh **đúng một** `change_log` row với `origin` phản ánh hành động của người (đo bằng: query `change_log` sau một lần sửa trả về đúng 1 row mới, khớp KC-2/KC-3)
- [ ] Form hiển thị **rõ nguồn gốc** của mỗi field: `ai` (do extraction tự động), `ai_edited`, hoặc `human` (đo bằng: field vừa sửa tay đổi `origin` sang `human` hoặc `ai_edited`, xác minh được qua truy vấn `generation.origin`/`field_provenance`)

### Đường không hạnh phúc (unhappy path)

- [ ] Tác giả sửa một nhân vật rồi **đóng tab mà không lưu** — hệ thống không tạo `change_log` row nào và giá trị cũ được giữ nguyên khi mở lại (đo bằng: `GET` lại entity, so với `change_log` không có row mới)
- [ ] Hai tab của cùng một tài khoản cùng sửa **một** entity gần như đồng thời — hệ thống không được để một bản ghi đè mất dấu vết bản kia mà không sinh `change_log` cho cả hai lần ghi (đo bằng: sau hai lần lưu liên tiếp cách nhau <1s, `change_log` có đủ 2 row, không row nào biến mất)
- [ ] Tác giả sửa entity của một `tenant_id` không phải của mình (thử qua API trực tiếp) — request bị từ chối, không entity nào bị đổi (đo bằng: response lỗi 403/404, `GET` lại entity ở tenant gốc không đổi — RLS theo KC-5)
- [ ] Extraction ban đầu tạo một entity **trùng lặp** (cùng một nhân vật bị tách thành hai) — tác giả có đường **merge hoặc xoá** entity thừa mà không làm mất `change_log` của entity bị xoá (đo bằng: sau merge, entity trùng không còn xuất hiện trong danh sách hiển thị nhưng `change_log` cũ vẫn truy vấn được)

### Ràng buộc cứng không được vi phạm

- `KC-2` — mọi hành động sửa qua form này phải sinh `change_log` row, kể cả sửa một field nhỏ
- `KC-3` — field vừa sửa tay phải cập nhật đúng `field_provenance`/`generation.origin`
- `KC-4` — `change_log` của một lần sửa phải commit **cùng transaction** với việc ghi giá trị mới của entity
- `KC-5` — mọi truy vấn/ghi qua form đều phải đi qua `tenant_id` + RLS, không có đường vòng

### Story này KHÔNG làm

- Không tự động **phát hiện** entity trùng lặp bằng thuật toán — merge là thao tác tay của tác giả trong phạm vi Story này
- Không sửa được **timeline key** (`timeline_id` + `story_order`) — đó là `Story-Fix-Narrative-Time-Key`, đã phải xong **trước** Story này
- Không hiển thị **preview trực quan** của nhân vật (ảnh) trong form này — đó thuộc phạm vi `Story-Character-Expression-Sheet` (ngoài horizon)
- Không có API công khai cho bên thứ ba chỉnh sửa Story Bible — chỉ có UI cho chính tác giả

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **14h** `[EM]` | Form CRUD cho 3 loại entity (nhân vật, địa điểm, state-theo-event) + wiring `change_log`/`field_provenance`. Trong trần 16h nhưng sát trần do phần state-theo-event đòi hỏi UI nhận biết event, không phải CRUD phẳng |
| `E_hitl` | **~0,5h/chapter** `[EM]` | Ước lượng thời gian tác giả bỏ ra để rà và sửa phần **≤20%** entity extraction sai theo ngưỡng M1-3. Đây là ước lượng **đặt trước MVP0**, chưa có số đo thật — không dùng làm ngưỡng chặn trước khi MVP0 chạy (cảnh báo W8 của `findings/product-owner.md`) |

## 6. INVEST

- **I (Independent)**: ✅ — không phụ thuộc trực tiếp vào Story nào khác của Epic-D để deliverable của nó hoàn chỉnh, ngoài phụ thuộc nền (Story Bible extraction ở Epic-B và khoá thời gian ở `Story-Fix-Narrative-Time-Key`, đã khai rõ ở mục 3 và mục *KHÔNG làm*)
- **S (Small)**: ⚠️ — **[PO suy luận, không có trong bảng §4.10 của `findings/business-analyst.md`]**. Nguồn chấm `S = ⚠️` ở bảng §4.4 nhưng không giải thích lý do trong bảng §4.10 (bảng đó chỉ liệt 7 Story khác). Lý do PO tự suy ra từ chính mô tả thành phần `#5` ([MVP-Scope §5.2](../../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas)): form phải phủ **ba loại entity khác nhau** (nhân vật, địa điểm, state-theo-event), và phần state-theo-event đòi hỏi UI nhận biết `timeline_id`/`story_order` (cùng cơ chế SCD Type 2 làm vỡ `Story-Timeline-State-Resolver`) — đây là một slice bó nhiều sub-domain hơn một Story "nhỏ" điển hình, dù vẫn nằm trong trần `E_build ≤ 16h`. **Câu hỏi cần trả lời nếu PM muốn tách nhỏ hơn**: có nên tách phần sửa state-theo-event thành Story riêng sau Story CRUD nhân vật/địa điểm cơ bản không — hiện giữ nguyên làm một Story theo đúng tên file trong `findings/business-analyst.md` §4.4, không tự tách vì nguồn cấm *"tự đặt tên mới, tự thêm Story"*.

---

_Created by product-owner_
_Author: trisjr_
