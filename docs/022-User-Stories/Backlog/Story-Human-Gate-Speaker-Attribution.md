---
id: STORY-C-06
type: story
status: draft
created: 2026-08-24
---

# Story-Human-Gate-Speaker-Attribution

## 1. Story

Là tác giả truyện chữ, tôi muốn **bắt buộc phải xác nhận ai nói câu nào trước khi trang được xuất bản**, để **một dòng gán sai không làm hỏng cả trang**.

## 2. Part of

- Epic cha: [Epic-Comic-Director-And-Layout](../Epics/Epic-Comic-Director-And-Layout.md)
- BRD cha: [BRD-003-Comic-Director-And-Layout](../../020-Requirements/BRD/BRD-003-Comic-Director-And-Layout.md)
- UC liên quan: [UC-04-Human-Gate-Speaker-Attribution](../../020-Requirements/Use-Cases/UC-04-Human-Gate-Speaker-Attribution.md)

## 3. Bối cảnh & nguồn

- `MVP-Scope.md` §3 hạng mục **C7** — *"Hai human gate bắt buộc: speaker attribution + dialogue condensation"*: `❌` ở MVP0, `⛔` ở MVP1, `✅` từ MVP2. Căn cứ: CF-8.8 — *"không phải tuỳ chọn, không dồn sang MVP4"* · CF-6.10 `[EM]` lỗi **30–50%** (3+ người có tự sự chen) / **40–60%** (câu ngắn, thán từ) — **ước lượng, KHÔNG phải số đo**.
- `Roadmap.md` mốc **MVP2**, exit criterion **M2-4**: *"hai human gate (speaker attribution + dialogue condensation) không bypass được: không tồn tại đường code nào xuất bản page mà chưa qua cả hai"*.
- `Roadmap.md` §3.3 rủi ro chính MVP2: *"Hai human gate bị 'tạm bypass để test' rồi quên bật lại — M2-4 đo bằng sự VẮNG MẶT của đường code bypass, không bằng cấu hình"*.
- **Lý do vỡ Independent** (`findings/business-analyst.md` §4.10, nguyên văn): *"Cả hai được đo bằng M2-4: sự VẮNG MẶT của đường code bypass. Đó là thuộc tính của pipeline xuất bản, không của một màn hình ⇒ hai Story này chỉ 'xong' cùng nhau. Thêm ràng buộc thứ tự từ Glossary.md: dialogue condensation phải chạy sau layout"*.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Gọi đường xuất bản một page mà speaker attribution của mọi dòng thoại trong page đó **chưa** được người xác nhận: request bị từ chối (test) — đo bằng: test gọi API/route xuất bản trên page chưa qua gate, kiểm tra trả về lỗi/từ chối, không xuất bản.
- [ ] Sau khi người xác nhận (chấp nhận hoặc sửa) toàn bộ gán speaker của một page, page đó chuyển trạng thái "đã qua gate speaker attribution" — đo bằng: kiểm tra trường trạng thái đổi sau hành động xác nhận cuối cùng.
- [ ] Mỗi hành động chấp nhận/sửa gán speaker của người dùng sinh một `change_log` row — đo bằng: đếm số `change_log` row trước/sau 1 hành động xác nhận, tăng đúng 1.

### Đường không hạnh phúc (unhappy path)

- [ ] Không tồn tại một flag cấu hình hay biến môi trường nào có thể tắt gate này để "test nhanh" trong code đường xuất bản chính thức — đo bằng: rà code path xuất bản, xác nhận không có nhánh điều kiện bỏ qua bước kiểm tra trạng thái gate (đây chính là rủi ro *"tạm bypass rồi quên bật lại"* mà `Roadmap §3.3` đã cảnh báo — `M2-4` đo bằng sự vắng mặt của đường code, không phải bằng cấu hình).
- [ ] Page có dòng thoại mà speaker gợi ý ban đầu (từ pipeline tự động) là rỗng/không xác định: gate vẫn bắt buộc người chọn một speaker hợp lệ trước khi qua gate, không tự động gán "unknown" rồi cho qua — đo bằng: test dòng thoại không có speaker gợi ý, kiểm tra page không chuyển trạng thái "đã qua gate" nếu dòng đó chưa được người xác nhận.

### Ràng buộc cứng không được vi phạm

- `KC-2` — mọi hành động người dùng tại gate (kể cả *"chọn speaker X thay vì Y"*) phải sinh một `change_log` row; đây là gate sinh dữ liệu đó **dày nhất** theo DoD của Epic cha.

### Story này KHÔNG làm

- [ ] KHÔNG tự động sửa gán speaker sai bằng heuristic thay cho người — mục đích của gate là con người ra quyết định, không phải hệ thống tự sửa rồi báo cáo.
- [ ] KHÔNG xử lý nén thoại (dialogue condensation) — đó là `Story-Human-Gate-Dialogue-Condensation`, chạy **sau** Story này theo đúng thứ tự layout → condensation.
- [ ] KHÔNG cho phép xuất bản một phần page (một số panel qua gate, một số chưa) — `M2-4` đo ở cấp độ page.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~14 giờ-người** `[EM]` | Gồm cơ chế chặn đường xuất bản + UI xác nhận tối thiểu + `change_log` hook. Dưới trần 16h nhưng sát trần vì phải phối hợp với `Story-Human-Gate-Dialogue-Condensation` để cả hai cùng chặn đúng một đường xuất bản. |
| `E_hitl` | **`TBD`** | Không có nguồn số giờ-người/chapter cho việc review speaker attribution. Trần `≤2 giờ-người/chapter` của tầng Planning là placeholder `[EM]`, chỉ có nghĩa **sau khi** MVP0 đo được `G1-c` (human-reject rate sau VLM-select — không cùng chỉ số nhưng là chỉ báo gần nhất về khối lượng review con người phải chịu). Hiệu chỉnh số thực sau MVP0; nếu số đo thực tế vượt 2 giờ-người/chapter ⇒ **escalate cho Founder**, không tự split Story. |

## 6. INVEST

- **I (Independent)**: ⚠️ **Vỡ.** Lý do (nguyên văn `findings/business-analyst.md` §4.10): *"Cả hai được đo bằng M2-4: sự VẮNG MẶT của đường code bypass. Đó là thuộc tính của pipeline xuất bản, không của một màn hình ⇒ hai Story này chỉ 'xong' cùng nhau"*. Ràng buộc thứ tự bổ sung: dialogue condensation phải chạy **sau** layout (`Glossary.md`), và cả hai gate phải cùng chặn một đường xuất bản duy nhất — ship Story này mà chưa ship `Story-Human-Gate-Dialogue-Condensation` không tạo ra `M2-4` PASS.
- **S (Small)**: ⚠️ **Vỡ**, cùng lý do I — chi phí thật của "Small" không nằm ở khối lượng code của riêng gate này mà ở việc phối hợp hai gate cùng chặn một pipeline xuất bản không có đường lách.

---

_Created by product-owner_
_Author: trisjr_
