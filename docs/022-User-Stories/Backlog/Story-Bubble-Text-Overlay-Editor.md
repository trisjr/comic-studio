---
id: STORY-D-05
type: story
status: draft
created: 2026-08-24
---

# Story-Bubble-Text-Overlay-Editor

## 1. Story

Là tác giả truyện chữ, tôi muốn **kéo bubble và sửa thoại trong phạm vi một panel**, để **sửa chữ không thành một lần đốt tiền API**

## 2. Part of

- Epic cha: [Epic-Minimum-Editor](../Epics/Epic-Minimum-Editor.md)
- BRD: [BRD-004-Minimum-Editor](../../020-Requirements/BRD/BRD-004-Minimum-Editor.md)
- Use Case liên quan: [UC-07-Edit-Bubble-And-Dialogue-In-Panel](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) — đây là thành phần `#2`, tiêu thụ **typeset layer** đã sinh từ `Story-Typeset-Layer-And-Bubble-Overlay` (Epic-Image-Generation-Pipeline)

## 3. Bối cảnh & nguồn

Đây là **thành phần bắt buộc `#2`** của hàng **`D1`** ([MVP-Scope §3](../../010-Planning/MVP-Scope.md)), chiếm **5–8%** `[EM]` effort (mẫu số SaaS) — hạng mục đắt nhất trong 5 thành phần editor, [MVP-Scope §5.2](../../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas): *"Bubble/text overlay editor trong phạm vi MỘT panel (kéo bubble, sửa thoại, chọn kiểu, kéo đuôi trỏ)"*, với **ba lý do độc lập**: (a) thoại do người viết là phần **được bảo hộ**; (b) bubble che mặt là lỗi không thể tự động tránh; (c) không sửa được thoại thì mọi lần sửa chữ thành một lần regenerate ảnh — **đốt tiền**. Đây là *"canvas bị giới hạn trong một khung"*, **không** phải scene graph tự do.

Story này **tự vắt biên horizon**: bảng `findings/business-analyst.md` §4.4 ghi mốc bắt đầu **MVP2** nhưng cột *Hoàn tất* = **MVP3** (ngoài horizon). Không có exit criterion `M2-x` được đánh số riêng cho bản MVP2 của thành phần này trong [Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) — bảng M2-1…M2-6 không nhắc trực tiếp bubble editor. Anchor Roadmap được dùng ở cấp gần nhất có căn cứ: **X-c** ([Roadmap §4](../../010-Planning/Roadmap.md#4-ba-việc-xen-ngang)) đặt *"Typeset layer + bubble overlay"* là việc phải có **ngay ở panel có thoại đầu tiên, trong MVP0** (exit criterion **G1-e**) — Story này là phần **editor tương tác** (kéo bubble, sửa thoại tay) xây trên nền typeset layer đó, không phải chính typeset layer (đã có ở `Story-Typeset-Layer-And-Bubble-Overlay`, MVP0). **Ghi nhận khoảng trống tường minh**: không có mã `M2-x` riêng cho phần UI tương tác này — chỉ có anchor gián tiếp qua X-c/G1-e và deliverable "Preview/export server-side" ở dòng MVP2 của bảng lộ trình.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Tác giả **kéo (drag)** một bubble tới vị trí khác **trong phạm vi panel** — đo bằng: sau khi kéo, toạ độ bubble lưu trong dữ liệu panel khớp vị trí mới, nằm trong biên panel
- [ ] Tác giả **sửa nội dung thoại** trong một bubble — đo bằng: `GET` lại panel trả về đúng text mới, **không** kèm theo một job `generation` mới nào bị tạo ra (đo bằng: đếm số `generation` row trước/sau thao tác không đổi)
- [ ] Tác giả **chọn kiểu bubble** (ví dụ: thoại thường / hét / suy nghĩ) từ danh mục có sẵn — đo bằng: `GET` lại bubble trả về đúng `style` đã chọn
- [ ] Tác giả **kéo đuôi trỏ (tail)** của bubble để chỉ đúng nhân vật đang nói — đo bằng: toạ độ/hướng đuôi trỏ lưu lại khớp thao tác kéo
- [ ] Mỗi lần kéo bubble / sửa thoại / đổi kiểu / kéo đuôi trỏ sinh **đúng một** `change_log` row (đo bằng: query `change_log` sau mỗi hành động trả về đúng 1 row mới, khớp `Story-Change-Log-On-Every-Editor-Action`)

### Đường không hạnh phúc (unhappy path)

- [ ] Tác giả kéo bubble ra **ngoài biên panel** — hệ thống chặn (clamp) bubble về trong biên, không lưu toạ độ ngoài [0,1] của khung panel (đo bằng: sau thao tác kéo vượt biên, toạ độ lưu lại nằm trong giới hạn hợp lệ)
- [ ] Tác giả sửa thoại thành một chuỗi **rỗng hoặc chỉ khoảng trắng** — hệ thống từ chối lưu và giữ giá trị cũ, báo lỗi rõ ràng (đo bằng: request lưu chuỗi rỗng trả về lỗi validate, `GET` lại bubble vẫn giữ text trước đó)
- [ ] Tác giả sửa thoại **vượt quá số ký tự mà `text_safe_zone` của panel đó chứa được** — hệ thống cảnh báo tràn vùng an toàn thay vì âm thầm cho chữ đè lên mặt nhân vật (đo bằng: nhập chuỗi dài hơn ngưỡng ký tự ước tính của `text_safe_zone`, response/UI trả về cảnh báo tràn, không lưu im lặng)
- [ ] Hai request sửa cùng một bubble gần như đồng thời (race condition) — trạng thái cuối phải nhất quán với một trong hai lần ghi, kèm đủ `change_log` cho cả hai lần (đo bằng: 2 request ghi cách nhau <100ms, `change_log` có đủ 2 row, bubble ở trạng thái hợp lệ)
- [ ] Tác giả thao tác trên panel thuộc `tenant_id` khác — request bị từ chối bởi RLS (đo bằng: response lỗi, dữ liệu bubble ở tenant gốc không đổi)

### Ràng buộc cứng không được vi phạm

- `KC-2` — mọi hành động sửa bubble/thoại sinh `change_log` row
- `KC-3` — thoại do người sửa tay phải được đánh dấu `origin = human` hoặc `ai_edited`, phân biệt với thoại gốc do AI sinh (`ai`)
- `KC-5` — thao tác qua `tenant_id` + RLS

### Story này KHÔNG làm

- Không cho phép chỉnh sửa **ngoài phạm vi một panel** (không có scene graph tự do, không kéo bubble sang panel khác) — vượt ranh giới này là đi vào `D2` infinite canvas, đã hoãn
- Không tự động **regenerate ảnh** khi sửa thoại — đúng giá trị cốt lõi của Story: sửa chữ không phải một lần đốt tiền API
- Không thực hiện **speaker attribution** hay **dialogue condensation** tự động — đó là hai human gate của Epic-Comic-Director-And-Layout (`Story-Human-Gate-Speaker-Attribution`, `Story-Human-Gate-Dialogue-Condensation`), chạy **trước** khi thoại tới được panel này để sửa tay
- Không hỗ trợ **SFX / narration box** như một loại riêng nếu nguồn chưa phân loại rõ (danh mục kiểu bubble bám theo `Panel Specification` đã có, không tự thêm loại mới)

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **18h** `[EM]` ⚠️ vượt trần 16h | **Lý do vượt trần, ghi thành văn**: đây là thành phần đắt nhất trong 5 thành phần editor (**5–8%** effort, cao nhất so với 3–7% của các thành phần khác) và chính bảng nguồn (`findings/business-analyst.md` §4.4) đã ghi nó **tự trải hai mốc** (bắt đầu MVP2, hoàn tất MVP3) — bản thân nguồn thừa nhận nó không gọn trong một lát cắt nhỏ. Ước lượng 18h là cho **phần MVP2** (kéo bubble, sửa thoại, chọn kiểu, kéo đuôi trỏ cơ bản); phần hoàn thiện thêm ở MVP3 nằm ngoài phạm vi Story này (ngoài horizon, không ước lượng ở đây) |
| `E_hitl` | **~1h/chapter** `[EM]` | Ước lượng thời gian tác giả bỏ ra để rà và chỉnh bubble/thoại sau khi hai human gate (speaker attribution, dialogue condensation) đã xác nhận nội dung — đây **không phải** bản thân một HITL gate bắt buộc, mà là thao tác tinh chỉnh tuỳ chọn. Trong trần 2h/chapter, nhưng là ước lượng **đặt trước MVP0/MVP2**, chưa có số đo thật (cảnh báo W8 của `findings/product-owner.md`) |

## 6. INVEST

- **I (Independent)**: ✅ — theo bảng §4.4 của `findings/business-analyst.md`. Deliverable là một UI riêng tiêu thụ typeset layer đã có (từ `Story-Typeset-Layer-And-Bubble-Overlay`), không cần Story khác của Epic-D hoàn thành trước
- **S (Small)**: ⚠️ — nguồn chấm `S = ⚠️` ở bảng §4.4 nhưng Story này **không nằm trong bảng chi tiết §4.10** (bảng đó chỉ liệt 7 Story khác, không có Story này). **Lý do PO suy ra trực tiếp từ chính hàng dữ liệu của bảng §4.4**: cột *Mốc* ghi *"MVP2 (bắt đầu)"* và cột *Hoàn tất* ghi *"MVP3"* — tức bản thân nguồn đã xác nhận thành phần này **không hoàn chỉnh trong một mốc**, phải chia làm hai giai đoạn (MVP2 rồi MVP3). Đây là dấu hiệu trực tiếp của việc vỡ chuẩn `Small`, không phải suy diễn xa. Cộng thêm `E_build` 18h vượt trần 16h (mục 5) càng củng cố việc chấm `⚠️`. **Không tự tách thành hai Story** vì tên file trong `findings/business-analyst.md` §4.4 chỉ có một dòng cho thành phần `#2` — Story này giữ nguyên phạm vi MVP2 theo đúng tên file được giao, phần hoàn tất MVP3 nằm ngoài horizon và ngoài phạm vi ước lượng của Story này.

---

_Created by product-owner_
_Author: trisjr_
