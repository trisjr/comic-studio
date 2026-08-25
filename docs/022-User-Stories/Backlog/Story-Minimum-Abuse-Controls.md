---
id: STORY-H-05
type: story
status: draft
created: 2026-08-24
---

# Story-Minimum-Abuse-Controls

## 1. Story

Là Founder (operator), tôi muốn **rate limit/tenant, giới hạn upload, log provider từ chối**, để **tín hiệu abuse xuất hiện sớm khi nó gần như miễn phí**.

## 2. Part of

- Epic cha: [Epic-Quality-And-Operations](../Epics/Epic-Quality-And-Operations.md)
- BRD cha: [BRD-008-Quality-And-Operations](../../020-Requirements/BRD/BRD-008-Quality-And-Operations.md)
- UC liên quan: [UC-01-Upload-And-Ingest-Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) — theo `Epic-Quality-And-Operations.md` §6.2: *"nơi abuse control cho upload (H5) được cưỡng chế — giới hạn dung lượng/số upload, rate limit per tenant"*.

## 3. Bối cảnh & nguồn

- `MVP-Scope.md` §3 hạng mục **H5** — *"Abuse controls tối thiểu (rate limit/tenant, giới hạn upload, log provider từ chối)"*: `🟡` ở MVP1 → `✅` từ MVP2. Căn cứ Analysis §5.7 — *"tín hiệu abuse sớm gần như miễn phí"*.
- `Roadmap.md` §4 *"Ba việc xen ngang"*, hàng **X-b**: nội dung chính của X-b (hard quota + credit ledger cưỡng chế chi phí) đặt ở MVP3, **nhưng** callout phạm vi ghi rõ: *"nếu trong horizon chỉ bán Tầng 1 không có image gen, X-b chưa cần — nhưng **abuse control cho upload thì cần ngay ở MVP1** (giới hạn dung lượng/số upload, rate limit per tenant)"*. ⚠️ **Không có exit criterion `M1-x`/`M2-x` riêng dạng mã cho H5** — đã rà toàn bộ danh sách `M1-1…M1-7` và `M2-1…M2-6` của `Roadmap.md` §2, không có hàng nào là "abuse controls". Theo nguyên tắc "không có mã riêng ⇒ ghi rõ nằm ở cột Deliverable": neo vào callout **X-b** của `Roadmap.md` §4 (bảng "Ba việc xen ngang" — không phải bảng lộ trình tổng, nhưng là tài liệu Roadmap có nêu rõ mốc và trigger) làm exit-criterion-tương-đương của Story này.
- `MVP-Scope.md` §6 **KC-5**: `tenant_id NOT NULL` trên mọi bảng + Postgres RLS, từ MVP1 — rate limit "theo tenant" của Story này phụ thuộc trực tiếp vào `tenant_id` đã tồn tại từ KC-5.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Tồn tại rate limit theo tenant cho hành động upload — vượt ngưỡng đã định nghĩa trong một khung thời gian cố định bị từ chối — đo bằng: test gửi N+1 request upload trong khung thời gian đã cấu hình cho ngưỡng N, request thứ N+1 bị từ chối với mã lỗi rate-limit.
- [ ] Tồn tại giới hạn dung lượng/số lượng file upload theo tenant — upload vượt giới hạn bị từ chối **tại thời điểm upload**, không phải phát hiện sau — đo bằng: test upload vượt ngưỡng, request bị từ chối ngay, file không được lưu vào storage.
- [ ] Mỗi lần provider ảnh/dịch vụ ngoài từ chối một request được ghi log với đủ thông tin: `tenant_id`, thời điểm, lý do từ chối — đo bằng: đếm số lần provider trả về mã từ chối, phải bằng số dòng log tương ứng.
- [ ] Rate limit áp dụng độc lập theo từng `tenant_id` — một tenant đạt ngưỡng không ảnh hưởng khả năng upload của tenant khác — đo bằng: test hai tenant song song, tenant A đạt ngưỡng bị chặn trong khi tenant B vẫn upload thành công.

### Đường không hạnh phúc (unhappy path)

- [ ] Nếu rate limit counter bị mất do restart service, hệ thống phải mặc định về trạng thái **an toàn** (chặn tạm thời hoặc giá trị bảo thủ), **không** được mặc định "cho phép không giới hạn" — đo bằng: test restart service giữa lúc counter đang đếm, hành vi sau restart không cho phép upload không giới hạn.
- [ ] Nếu một tenant chia nhỏ upload để né giới hạn dung lượng (nhiều file nhỏ thay vì 1 file lớn), giới hạn phải áp theo **tổng** dung lượng/số lượng trong khung thời gian, không chỉ theo từng request đơn lẻ — đo bằng: test upload N file nhỏ cộng dồn vượt ngưỡng tổng, request thứ N+1 bị từ chối dù từng file riêng lẻ dưới ngưỡng.
- [ ] Nếu provider trả lỗi do sự cố hạ tầng (timeout, 5xx) chứ không phải từ chối nội dung, sự kiện đó **không** được tính vào log "provider từ chối" — đo bằng: đối chiếu log lỗi hạ tầng và log provider-reject, không có phần giao nhau.

### Ràng buộc cứng không được vi phạm

- `KC-5`: `tenant_id NOT NULL` trên mọi bảng + Postgres RLS — rate limit theo tenant phải dựa trên `tenant_id` đã tồn tại, không tự tạo cơ chế định danh tenant riêng.

### Story này KHÔNG làm

- [ ] KHÔNG xây credit ledger / hard quota cưỡng chế chi phí — đó thuộc `KC-7`/Epic-Credit-And-Unit-Economics (MVP3). Story này chỉ sở hữu **tín hiệu abuse**, không sở hữu cưỡng chế kinh tế (`Epic-Quality-And-Operations.md` §5.4 mục 2).
- [ ] KHÔNG xây hệ thống phát hiện abuse bằng ML/heuristic phức tạp — phạm vi MVP1 chỉ là rate limit + giới hạn cứng + logging, đúng tinh thần "tối thiểu" (`🟡`) của hạng mục H5.
- [ ] KHÔNG áp rate limit cho các hành động khác ngoài upload trong phạm vi Story này (ví dụ rate limit cho API sinh ảnh — thuộc phạm vi MVP3, ngoài horizon).

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~8 giờ-người** `[EM]` | Rate limit theo tenant + giới hạn upload + logging là hạ tầng nhỏ, tái dùng `tenant_id` đã có từ `KC-5`. Trong trần 16h. |
| `E_hitl` | **0 giờ-người/chapter** | Cơ chế hoàn toàn tự động (rate limit, giới hạn dung lượng, logging) — không tạo nghĩa vụ giờ-người cho Founder. |

## 6. INVEST

- **I (Independent)**: ✅ theo `findings/business-analyst.md` §4.8 — không vỡ.
- **S (Small)**: ✅ theo `findings/business-analyst.md` §4.8 — không vỡ. `E_build` trong trần 16h.

---

_Created by quality-assurance_
_Author: trisjr_
