---
id: STORY-H-04
type: story
status: draft
created: 2026-08-24
---

# Story-Log-Preference-Data

## 1. Story

Là Founder (operator), tôi muốn **mọi lần người dùng chấp nhận/từ chối một gợi ý được ghi làm preference data**, để **moat thật được tích luỹ từ ngày đầu bằng đúng cơ chế mà luật đã buộc phải có**.

## 2. Part of

- Epic cha: [Epic-Quality-And-Operations](../Epics/Epic-Quality-And-Operations.md)
- BRD cha: [BRD-008-Quality-And-Operations](../../020-Requirements/BRD/BRD-008-Quality-And-Operations.md)
- UC liên quan: [UC-06-Generate-Panel-And-Pick-Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) — nơi *"chọn X thay vì Y"* xảy ra, theo `Epic-Quality-And-Operations.md` §6.2: *"nguồn của preference data (H2)"*. Cũng liên quan [UC-02-Review-And-Edit-Story-Bible](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) — nơi người dùng chấp nhận/sửa entity do extraction đề xuất.

## 3. Bối cảnh & nguồn

- `MVP-Scope.md` §3 hạng mục **H2** — *"Log preference data (moat thật)"*: `❌` MVP0 → `✅` từ MVP1. Căn cứ CF-8.7 + Analysis §12 — *"một khoản đầu tư, trả hai lần"*.
- `Roadmap.md` §3.2 MVP1 bổ sung #4: *"Log preference data — đây là moat thật (không phải 5 thành phần kỹ thuật). Gần như miễn phí, chỉ cần thiết kế để ghi lại. Và nó dùng chung đúng cơ chế mà luật VN buộc phải có ⇒ một khoản đầu tư, trả hai lần"*.
- ⚠️ **Không có exit criterion `M1-x` riêng cho H2** — đã được `findings/product-owner.md` §3.4 khối `[!WARNING]` xác nhận tường minh: *"H2 (log preference data — ✅ ở MVP1 nhưng KHÔNG ứng với exit criterion M1-x nào)"*. Theo đúng nguyên tắc "không có mã riêng ⇒ ghi rõ nằm ở cột Deliverable", em neo vào exit criterion **M1-5** (`Roadmap.md` §2 mốc MVP1) — *"5 hạng mục provenance (`parent_generation_id`, `relation_kind`, `change_log`, `field_provenance`, `generation.origin`) tồn tại, và có test chứng minh chúng commit CÙNG MỘT transaction"* — vì preference data **tái dùng đúng cơ chế `change_log`** mà M1-5 đã đòi hỏi phải có (không phải một hệ ghi log riêng).
- `MVP-Scope.md` §6 **KC-2**: *"`change_log` ghi mọi hành động người dùng — kể cả 'chọn generation X thay vì Y'"*. Đây chính là cơ chế mà preference data tái sử dụng.
- Analysis §12 (`Analysis-Comic-Studio-Concept.md`, **không sửa tài liệu này** — `CẤM-18`): preference data là ứng viên moat thật của dự án.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Mỗi lần người dùng chấp nhận một trong nhiều gợi ý (ví dụ chọn 1 trong 3 candidate panel ở UC-06) tạo ra đúng **một** bản ghi preference data ghi rõ: gợi ý được chọn + (các) gợi ý bị từ chối — đo bằng: đếm số hành động "chọn" trong luồng, phải bằng số bản ghi preference data tương ứng.
- [ ] Bản ghi preference data commit **CÙNG MỘT transaction** với hành động nghiệp vụ mà nó ghi lại — đo bằng: test rollback transaction làm mất cả hai bản ghi cùng lúc, không có trường hợp một bản ghi tồn tại mà bản ghi kia không.
- [ ] Preference data lưu đủ 3 thành phần tối thiểu: hành động (accept/reject), timestamp, và tham chiếu tới đối tượng được chọn/bị từ chối — đo bằng: schema validation trên ≥1 bản ghi mẫu có đủ 3 trường.
- [ ] Preference data được ghi cho **mọi** luồng "chọn X thay vì Y" đã triển khai ở MVP1 (không chỉ luồng panel selection) — đo bằng: liệt kê tất cả luồng "chọn X thay vì Y" đã có ở MVP1, đối chiếu 100% có bản ghi preference tương ứng.

### Đường không hạnh phúc (unhappy path)

- [ ] Nếu hành động chấp nhận/từ chối bị lỗi giữa chừng (crash sau khi ghi preference nhưng trước khi commit nghiệp vụ), preference data **không** được tồn tại đơn lẻ mà không có hành động nghiệp vụ tương ứng — đo bằng: test crash-injection giữa hai bước, sau rollback không còn bản ghi preference mồ côi.
- [ ] Nếu người dùng đổi ý và chọn lại một gợi ý khác cho cùng một quyết định, preference data phải ghi **cả hai** lần chọn theo thứ tự thời gian, không ghi đè bản ghi cũ — đo bằng: bảng preference data có ≥2 dòng cho cùng một đối tượng quyết định khi có đổi ý.
- [ ] Nếu một luồng chọn diễn ra hàng loạt (batch), mỗi lựa chọn trong batch vẫn phải sinh một bản ghi preference riêng, không được gộp thành một bản ghi tổng — đo bằng: đếm số bản ghi preference sau một hành động batch N lựa chọn, phải bằng N.

### Ràng buộc cứng không được vi phạm

- `KC-2`: `change_log` ghi mọi hành động, kể cả "chọn generation X thay vì Y" — preference data là một use case cụ thể của cơ chế này, không phải hệ ghi log riêng.
- `KC-4`: cả `change_log` (và do đó preference data đi kèm) phải commit **cùng một transaction** với artifact mà nó chứng minh.

### Story này KHÔNG làm

- [ ] KHÔNG xây mô hình ML học từ preference data — Story chỉ chịu trách nhiệm **ghi lại** dữ liệu, không huấn luyện hay dùng dữ liệu để ra quyết định tự động.
- [ ] KHÔNG log preference data cho các luồng ngoài MVP1 (ví dụ luồng generate ảnh thật ở MVP3 — ngoài horizon).
- [ ] KHÔNG dùng preference data để thay thế eval kit (`Story-HITL-Gate-And-Eval-Kit`) — eval kit đo chất lượng kỹ thuật trên golden dataset; preference data đo sở thích thẩm mỹ trên hành vi người dùng thật. Hai nguồn khác nhau, không gộp.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~10 giờ-người** `[EM]` | Thiết kế schema preference data + instrument các luồng "chọn X thay vì Y" hiện có ở MVP1, tái dùng cơ chế `change_log` đã xây cho `KC-2`. Trong trần 16h — khớp tinh thần "gần như miễn phí" của Analysis §12. |
| `E_hitl` | **0 giờ-người/chapter** | Đây là instrumentation thụ động trên hành động người dùng **vốn đã làm** (chọn candidate, sửa Story Bible) — không tạo thêm bước xác nhận mới, không tạo nghĩa vụ giờ-người mới. |

## 6. INVEST

- **I (Independent)**: ⚠️ **Vỡ**, theo `findings/business-analyst.md` §4.8 và lý do đã có sẵn tại `Epic-Quality-And-Operations.md` §3: *"nó là nhãn gắn vào mỗi lần người dùng chấp nhận/từ chối một gợi ý ⇒ nó sống bên trong các luồng của Epic khác, không tự đứng riêng"*. Story này không có UI/luồng riêng — nó chỉ tồn tại **bên trong** UC-06, UC-02 và các luồng chọn khác của các Epic khác. **Không có hàng chi tiết ở `findings/business-analyst.md` §4.10** cho Story này; áp dụng quy tắc quyết định của PM: gắn nhãn `[QA suy luận]` cho việc dùng lại lý do đã có ở Epic cha thay vì tự phát minh lý do mới.
- **S (Small)**: ✅ theo `findings/business-analyst.md` §4.8 (không vỡ). `E_build` trong trần 16h.

---

_Created by quality-assurance_
_Author: trisjr_
