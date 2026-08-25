---
id: STORY-H-03
type: story
status: draft
created: 2026-08-24
---

# Story-HITL-Gate-And-Eval-Kit

## 1. Story

Là Founder (operator), tôi muốn **HITL gate và eval kit có ngay ở MVP1**, để **mọi thay đổi prompt/model về sau không phải thay đổi mù**.

## 2. Part of

- Epic cha: [Epic-Quality-And-Operations](../Epics/Epic-Quality-And-Operations.md)
- BRD cha: [BRD-008-Quality-And-Operations](../../020-Requirements/BRD/BRD-008-Quality-And-Operations.md)
- UC liên quan: [UC-02-Review-And-Edit-Story-Bible](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) (điểm HITL gate tự nhiên nhất của MVP1 — xác nhận nhân vật/địa điểm/trang phục do extraction sinh ra) · [UC-06-Generate-Panel-And-Pick-Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) (nơi eval kit đo output của best-of-N).

## 3. Bối cảnh & nguồn

- `MVP-Scope.md` §3 hạng mục **H1** — *"HITL gate + eval kit"*: `❌` ở MVP0 → `✅` từ MVP1. Căn cứ CF-8.7: *"ngay tại MVP1, không dồn MVP4"*.
- `Charter-Comic-Studio.md` §4 điều kiện khả thi **R9**: *"HITL gate + eval kit ở MVP1, không phải MVP4"* — không thoả thì *"không có vòng phản hồi người trong 3 milestone; preference data (moat thật) không được ghi từ đầu"*.
- `Roadmap.md` §2 mốc **MVP1**, exit criterion **M1-6**: *"eval kit chạy được trên golden dataset của MVP0 và cho ra số"*.
- `Roadmap.md` §3.2 MVP1 bổ sung #3: *"HITL gate + eval kit ngay tại đây, không dồn MVP4 — không có eval kit thì mọi thay đổi prompt/model về sau là thay đổi mù. Và golden dataset để chạy eval đã có sẵn từ MVP0"*.
- `Roadmap.md` §6.2 bảng phụ thuộc: *"Golden dataset của MVP0 → Eval kit ở MVP1 (M1-6) — Mềm"* — nếu dataset của `Story-Golden-Dataset-For-Regression` mất, eval kit dựng lại được nhưng tốn tiền API lần hai.
- `Glossary.md`: **HITL gate** — *"đơn vị đo là giờ-người, không phải token — với một người làm một mình, đây mới là ràng buộc thật, không phải chi phí API"*. **eval kit** — *"bộ dữ liệu và script đo chất lượng output, có từ sớm để mọi thay đổi sau đó đo được. Thuộc MVP1, không phải MVP4"*.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Eval kit chạy được trên golden dataset của MVP0 (15–20 panel, `Story-Golden-Dataset-For-Regression`) và trả về **≥1 chỉ số số học tổng hợp** — đo bằng: chạy script eval kit, output có ≥1 giá trị số, không phải mô tả định tính.
- [ ] Tồn tại **≥1 điểm HITL gate bắt buộc** trong pipeline MVP1 mà không có đường code nào bỏ qua được — đo bằng: rà code path, không tìm thấy nhánh nào tiếp tục pipeline mà chưa đi qua điểm gate đó.
- [ ] Chạy eval kit hai lần liên tiếp trên cùng golden dataset (không đổi model/prompt) cho ra cùng một giá trị số — đo bằng: so sánh output hai lần chạy, diff = 0.
- [ ] Sau khi thay đổi một prompt hoặc một model có tác động đã biết trước, chạy lại eval kit cho ra giá trị **khác** với lần trước — đo bằng: test cố ý gây thay đổi (ví dụ đổi một field trong Visual Prompt Compiler), hai lần chạy eval kit trước/sau cho hai giá trị khác nhau.

### Đường không hạnh phúc (unhappy path)

- [ ] Nếu golden dataset thiếu hoặc hỏng, eval kit phải báo lỗi và dừng — **không** được chạy trên tập dữ liệu rỗng rồi báo cáo "100% pass" — đo bằng: test chạy eval kit với dataset rỗng, kết quả là lỗi, không phải số pass.
- [ ] Nếu một request cố gắng gọi thẳng bước sau HITL gate mà chưa qua xác nhận (ví dụ gọi trực tiếp API publish), request đó phải bị **từ chối ở tầng code**, không chỉ cảnh báo ở UI — đo bằng: test gọi trực tiếp bước sau gate mà chưa xác nhận, nhận về lỗi/reject.
- [ ] Nếu eval kit chạy trên một bản dataset đã bị chỉnh sửa so với golden dataset gốc (spec/ref/ảnh khác), kết quả phải bị đánh dấu **không hợp lệ** — đo bằng: eval kit kiểm tra checksum dataset trước khi chạy, báo lỗi nếu không khớp.

### Ràng buộc cứng không được vi phạm

- — Không có `KC-x` trong `MVP-Scope.md` §6 áp trực tiếp cho HITL gate/eval kit. Ghi chú: `Charter-Comic-Studio.md` §4 **R9** là một trong chín **điều kiện khả thi** của dự án (không nằm trong danh sách `KC-1…KC-7`/`C1…C10`/`AG-1…AG-8`), nhưng có cùng tính chất bắt buộc: không thoả R9 thì preference data (moat) không được ghi từ đầu.

### Story này KHÔNG làm

- [ ] KHÔNG xây hai human gate bắt buộc của Comic Director (speaker attribution, dialogue condensation) — đó là `Story-Human-Gate-Speaker-Attribution` và `Story-Human-Gate-Dialogue-Condensation` (thuộc Epic-C, hạng mục **C7**, MVP2).
- [ ] KHÔNG huấn luyện hoặc dùng preference data để tự động điều chỉnh model — Story này chỉ đo (eval kit) và chặn (HITL gate), không tối ưu hoá tự động.
- [ ] KHÔNG dựng lại golden dataset — đó là phạm vi của `Story-Golden-Dataset-For-Regression`; Story này chỉ **tiêu thụ** dataset đã có.
- [ ] KHÔNG mở rộng eval kit sang đo chi phí (`cost_usd`) — đó thuộc phạm vi `usage_event`/`usage_daily` của Epic-F.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~24 giờ-người** `[EM]` — **vượt trần 16h** | Lý do vượt trần, ghi thành văn theo đúng quy tắc (không tự split): Story bó hai hạng mục bắt buộc phải cùng tồn tại — HITL gate (cơ chế chặn không-bypass-được) và eval kit (script đo trên golden dataset, ra số). CF-8.7 đòi cả hai **cùng lúc** ở MVP1; chỉ có một nửa (gate mà không có eval kit đo được, hoặc ngược lại) thì R9 vẫn **không** thoả — *"mọi thay đổi prompt/model về sau là thay đổi mù"*. `findings/business-analyst.md` §4.10 không liệt kê Story này trong 7 Story vỡ, nhưng BA table §4.8 đã chấm `S=⚠️`; suy lý do tại chỗ theo đúng quy tắc quyết định của PM — `[QA suy luận]`. |
| `E_hitl` | `TBD` | Nội dung cụ thể của "điểm HITL gate" ở MVP1 chưa được `Roadmap.md`/`MVP-Scope.md` mô tả chi tiết (chỉ nói "HITL gate ngay tại đây", không chỉ rõ gate nào ngoài gợi ý UC-02 review Story Bible). Thời gian giờ-người thật cho gate này phụ thuộc tải review, đo được **sau khi** có số `G1-c` (human-reject rate) từ MVP0 (`findings/product-owner.md` §4.3 cảnh báo W8). **Điều kiện escalate**: nếu đo thực tế ở MVP1 cho thấy thời gian qua gate vượt **2 giờ-người/chapter**, escalate cho Founder — không tự split Story. |

## 6. INVEST

- **I (Independent)**: ✅ theo `findings/business-analyst.md` §4.8. Story dựa vào golden dataset đã có sẵn từ MVP0 (`Story-Golden-Dataset-For-Regression`) nhưng không cần Story đó "xong đồng thời" — golden dataset là input đã tồn tại từ trước MVP1.
- **S (Small)**: ⚠️ **Vỡ** — không có hàng chi tiết ở `findings/business-analyst.md` §4.10 cho Story này; áp dụng quy tắc quyết định của PM: *"Story có ⚠️ ở §4.8 nhưng không có hàng chi tiết §4.10: tự suy lý do và gắn nhãn `[QA suy luận]`"*. Lý do: xem cột `Ghi chú` của `E_build` ở mục 5 — hai hạng mục (gate + eval kit) phải cùng tồn tại để thoả R9, không tách nhỏ hợp lý được mà vẫn giữ ý nghĩa "không thay đổi mù" `[QA suy luận]`.

---

_Created by quality-assurance_
_Author: trisjr_
