---
id: STORY-C-07
type: story
status: draft
created: 2026-08-24
---

# Story-Human-Gate-Dialogue-Condensation

## 1. Story

Là tác giả truyện chữ, tôi muốn **bắt buộc phải xác nhận thoại đã nén trước khi trang được xuất bản**, để **việc nén có mất không âm thầm đổi nghĩa lời nhân vật**.

## 2. Part of

- Epic cha: [Epic-Comic-Director-And-Layout](../Epics/Epic-Comic-Director-And-Layout.md)
- BRD cha: [BRD-003-Comic-Director-And-Layout](../../020-Requirements/BRD/BRD-003-Comic-Director-And-Layout.md)
- UC liên quan: [UC-05-Human-Gate-Dialogue-Condensation](../../020-Requirements/Use-Cases/UC-05-Human-Gate-Dialogue-Condensation.md)

## 3. Bối cảnh & nguồn

- `MVP-Scope.md` §3 hạng mục **C7** — *"Hai human gate bắt buộc: speaker attribution + dialogue condensation"*: `❌` ở MVP0, `⛔` ở MVP1, `✅` từ MVP2. Căn cứ: CF-8.8 — *"không phải tuỳ chọn, không dồn sang MVP4"*.
- `Roadmap.md` mốc **MVP2**, exit criterion **M2-4**: *"hai human gate (speaker attribution + dialogue condensation) không bypass được: không tồn tại đường code nào xuất bản page mà chưa qua cả hai"*.
- `dialogue condensation` (`Glossary.md`): bước nén thoại gốc (thường **30–80 từ** với web-novel dịch) xuống mức bubble đọc thoải mái (**~8–20 từ**), tức hệ số **2–5×**. Là **hành vi biên tập có mất** ⇒ cần LLM **và** cần người review. **Phải chạy sau layout**, vì `text_budget` phụ thuộc diện tích panel (tức phụ thuộc `text_safe_zone` đã có từ `Story-Text-Safe-Zone-In-Panel-Spec`).
- **Lý do vỡ Independent** (`findings/business-analyst.md` §4.10, nguyên văn) — chung với `Story-Human-Gate-Speaker-Attribution`: *"Cả hai được đo bằng M2-4 […] hai Story này chỉ 'xong' cùng nhau. Thêm ràng buộc thứ tự từ Glossary.md: dialogue condensation phải chạy sau layout"*.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Với mỗi dòng thoại đã qua bước nén tự động, hệ thống hiển thị cả bản gốc và bản nén cho người xác nhận trước khi cho qua gate — đo bằng: kiểm tra UI/data trả về có đủ hai trường `original_text` và `condensed_text` khi ở trạng thái chờ xác nhận.
- [ ] Gọi đường xuất bản một page mà **bất kỳ** dòng thoại nào trong page chưa được người xác nhận bản nén: request bị từ chối (test) — đo bằng: test gọi route xuất bản trên page có ≥1 dòng thoại chưa qua gate, kiểm tra bị từ chối.
- [ ] Bước nén chỉ chạy **sau** khi panel đã có `text_safe_zone`/diện tích xác định (tức sau layout) — đo bằng: kiểm tra thứ tự gọi hàm/pipeline: bước tính `text_budget` (phụ thuộc diện tích panel) xảy ra trước bước gọi LLM nén.
- [ ] Mỗi hành động chấp nhận/sửa bản nén của người dùng sinh một `change_log` row — đo bằng: đếm `change_log` row trước/sau 1 hành động xác nhận, tăng đúng 1.

### Đường không hạnh phúc (unhappy path)

- [ ] Không tồn tại flag/biến môi trường nào tắt được gate này trong code đường xuất bản chính thức — đo bằng: rà code path xuất bản, xác nhận không có nhánh bỏ qua kiểm tra trạng thái gate (cùng rủi ro *"tạm bypass rồi quên bật lại"* mà `Roadmap §3.3` cảnh báo cho cả hai gate).
- [ ] Bản nén tự động vượt `text_budget` của panel (không vừa `text_safe_zone`): hệ thống phải chặn không cho gán bản nén đó cho panel, buộc chạy lại bước nén hoặc để người tự viết lại, không được cắt chữ một cách cơ học để "vừa khung" — đo bằng: test bản nén dài hơn `text_budget` cho phép, kiểm tra hệ thống từ chối gán/xuất bản panel đó.
- [ ] Người xác nhận sửa tay bản nén thành một câu **dài hơn** `text_budget`: hệ thống phải cảnh báo tường minh (không chặn cứng, vì đây là quyết định của con người) nhưng vẫn ghi `change_log` — đo bằng: test sửa tay vượt `text_budget`, kiểm tra có cảnh báo và vẫn ghi log.

### Ràng buộc cứng không được vi phạm

- `KC-2` — mọi hành động người dùng tại gate (kể cả chấp nhận bản nén không sửa) phải sinh một `change_log` row.

### Story này KHÔNG làm

- [ ] KHÔNG tự chạy trước khi layout xác định diện tích panel — vi phạm trực tiếp ràng buộc thứ tự đã nêu ở mục 3.
- [ ] KHÔNG xử lý gán speaker — đó là `Story-Human-Gate-Speaker-Attribution`, chạy song song về mặt dữ liệu nhưng cùng chặn chung một đường xuất bản.
- [ ] KHÔNG tự động chọn bản nén "tốt nhất" mà không có bước người xác nhận — đó chính là điều gate này tồn tại để ngăn.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~14 giờ-người** `[EM]` | Gồm bước nén (gọi LLM), tính `text_budget` phụ thuộc `text_safe_zone`, UI xác nhận, và phối hợp với gate speaker attribution để cùng chặn một đường xuất bản. Sát trần 16h vì phần phối hợp thứ tự (sau layout) không tầm thường. |
| `E_hitl` | **`TBD`** | Không có nguồn số giờ-người/chapter cho việc review bản nén. Trần `≤2 giờ-người/chapter` là placeholder `[EM]` của tầng Planning, chưa có căn cứ trước khi MVP0 chạy. Hiệu chỉnh sau MVP0 bằng số đo thực tế; vượt 2 giờ-người/chapter ⇒ **escalate cho Founder**, không tự split (nén thoại là hành vi biên tập có mất, tách nhỏ Story không giảm được khối lượng review mỗi chapter). |

## 6. INVEST

- **I (Independent)**: ⚠️ **Vỡ.** Lý do (nguyên văn `findings/business-analyst.md` §4.10, dùng chung với `Story-Human-Gate-Speaker-Attribution`): *"Cả hai được đo bằng M2-4: sự VẮNG MẶT của đường code bypass […] hai Story này chỉ 'xong' cùng nhau"*. Thêm ràng buộc thứ tự riêng của Story này: dialogue condensation **phải chạy sau layout** — không độc lập được với việc `text_safe_zone`/diện tích panel đã tồn tại.
- **S (Small)**: ⚠️ **Vỡ**, cùng lý do I — chi phí thật nằm ở việc đảm bảo đúng thứ tự pipeline (sau layout) và phối hợp với gate speaker attribution để `M2-4` PASS như một cặp, không phải ở khối lượng code của riêng bước nén.

---

_Created by product-owner_
_Author: trisjr_
