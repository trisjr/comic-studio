---
id: STORY-H-06
type: story
status: draft
created: 2026-08-24
---

# Story-Export-Chapter-To-PDF-CBZ-Webtoon

## 1. Story

Là tác giả truyện chữ, tôi muốn **xuất chương ra PDF / CBZ / webtoon**, để **tôi thật sự nhận được một thứ ra khỏi hệ thống**.

## 2. Part of

- Epic cha: [Epic-Quality-And-Operations](../Epics/Epic-Quality-And-Operations.md)
- BRD cha: [BRD-008-Quality-And-Operations](../../020-Requirements/BRD/BRD-008-Quality-And-Operations.md)
- UC liên quan: [UC-09-Export-Chapter](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) — hiện thực hoá trực tiếp hạng mục H4.

## 3. Bối cảnh & nguồn

> Ghi chú áp dụng cho toàn bộ khối dưới: Story này mang **hai giai đoạn** kế thừa từ bảng `MVP-Scope §3` hạng mục H4 — bản **PDF** (`🟡 preview server-side` ở MVP2, exit criterion **M2-5**, **TRONG HORIZON**) và phần mở rộng **CBZ/webtoon** (`✅` đủ định dạng ở MVP3, **NGOÀI HORIZON**). Bốn khối AC ở mục 4 mô tả phần **TRONG HORIZON** (PDF); phần CBZ/webtoon ngoài horizon không có AC chi tiết vì chưa tới mốc đó, chỉ được ghi nhận ở mục 5/6.

- `MVP-Scope.md` §3 hạng mục **H4** — *"Export PDF / CBZ / webtoon"*: `❌` MVP0, `⛔` MVP1, `🟡 preview server-side` MVP2, `✅` MVP3. Căn cứ CF-8.10: *"thứ **duy nhất** trong MVP4 người dùng thật sự nhận được"* ⇒ kéo lên sớm.
- `Roadmap.md` §2 mốc **MVP2 — Comic Director**, exit criterion **M2-5**: *"export ra PDF của 1 chapter hoàn chỉnh từ preview server-side"*.
- `Roadmap.md` §5.2 ⭐ *"Hệ quả tích cực: thứ có thể bán được trong horizon"*: export/preview server-side hoàn thành ở MVP2 (exit M2-5) là **1 trong 3 điều kiện** để Tầng 1 (`FR-F-06`, `CF-2.2`) bán được trong horizon — cùng với X-a (safe harbour) và G0 PASS.
- `Epic-Quality-And-Operations.md` §2 mục 2: *"Không có export ở MVP2 thì Tầng 1 không bán được và horizon 6 tháng khép lại với $0"*.
- `MVP-Scope.md` §6 **KC-2**: `change_log` ghi mọi hành động người dùng — export là một hành động tác động lên chapter, phải được ghi lại.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Xuất 1 chapter hoàn chỉnh ra file **PDF** từ preview server-side thành công — đo bằng: chạy export trên ≥1 chapter đã hoàn tất, nhận được 1 file PDF mở được, số trang PDF bằng số trang của chapter.
- [ ] File PDF xuất ra chứa đúng nội dung đã được duyệt qua hai human gate (speaker attribution + dialogue condensation, nếu chapter thuộc phạm vi MVP2 trở đi) — đo bằng: đối chiếu nội dung text trong PDF với nội dung đã xác nhận qua HITL gate, khớp 100%.
- [ ] Export chạy **server-side**, không phụ thuộc trạng thái trình duyệt/client — đo bằng: gọi export qua API/background job độc lập với phiên trình duyệt, kết quả không đổi khi đóng trình duyệt giữa chừng.
- [ ] Mỗi lần export tạo ra một bản ghi trong `change_log` (`KC-2`) — đo bằng: đếm số lần export, phải bằng số bản ghi `change_log` tương ứng.

### Đường không hạnh phúc (unhappy path)

- [ ] Nếu chapter chưa qua đủ hai human gate bắt buộc (`M2-4`), yêu cầu export bị **từ chối**, không xuất ra bản PDF "tạm" — đo bằng: test gọi export trên chapter chưa qua gate, nhận lỗi/reject, không có file output.
- [ ] Nếu export bị lỗi giữa chừng (ví dụ hết bộ nhớ khi render trang nhiều panel), hệ thống **không** được trả về file PDF một phần mà không báo lỗi — đo bằng: test kill process giữa lúc export, không tồn tại file output không hoàn chỉnh được đánh dấu "thành công".
- [ ] Nếu chapter có panel thiếu ảnh (generation lỗi chưa xử lý), export phải báo lỗi liệt kê panel thiếu, **không** tự động bỏ qua panel đó và xuất ra chapter thiếu trang mà không cảnh báo — đo bằng: test export chapter có 1 panel thiếu ảnh, output là lỗi có danh sách panel thiếu.

### Ràng buộc cứng không được vi phạm

- `KC-2`: `change_log` ghi mọi hành động người dùng, kể cả export.

### Story này KHÔNG làm

- [ ] KHÔNG xuất ra định dạng **CBZ** hoặc **webtoon** trong phạm vi bốn khối AC ở trên — phần "đủ định dạng" hoàn tất ở **MVP3, ngoài horizon** của lô tài liệu này; chỉ **PDF** (`M2-5`) nằm trong horizon và có AC chi tiết.
- [ ] KHÔNG xây dựng canvas editor để chỉnh sửa trước khi export — export chỉ đọc dữ liệu đã có từ preview server-side, không phải một công cụ chỉnh sửa.
- [ ] KHÔNG tính export vào phạm vi credit ledger/billing — export nằm trong margin ~90% của Tầng 1 (`CF-2.2`), không tiêu credit theo mô hình 3 tầng.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~28 giờ-người** `[EM]` — **vượt trần 16h** | Lý do vượt trần, ghi thành văn theo đúng quy tắc (không tự split): số giờ này tính cho **toàn bộ phạm vi Story theo đúng tên gọi** mà `findings/business-analyst.md` §4.8 đặt (PDF + CBZ + webtoon), vì BA không tách Story theo định dạng và Story này cũng không nằm trong 7 Story vỡ của §4.10 để có hướng dẫn tách sẵn. Ba định dạng có pipeline đóng gói khác nhau (PDF: render trang tĩnh; CBZ: đóng gói ảnh trang theo chuẩn đọc truyện; webtoon: re-layout dạng cuộn dọc liên tục) dù dùng chung compositor của preview (Epic-Minimum-Editor). Riêng phần **PDF trong horizon (M2-5)** có thể nhỏ hơn 16h, nhưng vì Story giữ nguyên một tên/một phạm vi đầy đủ, `E_build` ghi cho toàn bộ. |
| `E_hitl` | **0 giờ-người/chapter** | Bước export tự nó không tạo human gate mới — nội dung đã qua xác nhận ở các gate khác (`M2-4`) trước khi tới bước export; export chỉ đóng gói, không đòi thêm quyết định của người. |

## 6. INVEST

- **I (Independent)**: ✅ theo `findings/business-analyst.md` §4.8.
- **S (Small)**: ⚠️ **Vỡ** — không có hàng chi tiết ở `findings/business-analyst.md` §4.10 cho Story này; áp dụng quy tắc quyết định của PM: *"Story có ⚠️ ở §4.8 nhưng không có hàng chi tiết §4.10: tự suy lý do và gắn nhãn `[QA suy luận]`"*. Lý do (`[QA suy luận]`): Story vắt biên MVP2 (PDF, trong horizon) → MVP3 (CBZ/webtoon, ngoài horizon), và **tái dùng compositor của preview** vốn thuộc Epic-Minimum-Editor (`Epic-Quality-And-Operations.md` §6.1: *"export tái dùng compositor của preview"*) — phụ thuộc chéo Epic cộng với ba pipeline đóng gói khác nhau khiến tổng phạm vi vượt 16h giờ-người (xem mục 5).

---

_Created by quality-assurance_
_Author: trisjr_
