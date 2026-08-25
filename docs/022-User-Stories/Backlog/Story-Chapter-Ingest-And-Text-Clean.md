---
id: STORY-B-02
type: story
status: draft
created: 2026-08-24
---

# Story-Chapter-Ingest-And-Text-Clean

## 1. Story

Là tác giả truyện chữ, tôi muốn **rác scrape bị loại trước khi extraction chạy**, để **Story Bible không sinh entity giả**

## 2. Part of

- Epic cha: [Epic-Story-Intelligence](../Epics/Epic-Story-Intelligence.md)
- BRD: [BRD-002-Story-Intelligence](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)
- Use Case liên quan: [UC-01-Upload-And-Ingest-Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) — text clean là bước bên trong UC này, ngay sau khi chapter được đưa vào hệ thống

## 3. Bối cảnh & nguồn

Đây là hàng **`B1`** của [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope): *"Chapter parse + text clean (regex/heuristic, deterministic)"* — `❌ viết tay` ở MVP0, `✅` từ MVP1 trở đi, căn cứ CF-8.7 *"text clean là bước ĐẦU TIÊN"*.

Exit criterion tương ứng là **`M1-2`** của [Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng), mốc **MVP1**: *"pipeline ingest có bước text clean là bước ĐẦU TIÊN, chạy được trên ≥1 chapter scrape thật (không phải văn bản sạch tự soạn)"*. Nếu text clean không đứng đầu, Story Bible **sinh entity giả** từ quảng cáo và lời tác giả cuối chương (CF-8.7) — đây cũng là mục tiêu D1 trong [Epic-Story-Intelligence §5](../Epics/Epic-Story-Intelligence.md#5-definition-of-done-cấp-epic).

## 4. Acceptance Criteria

### Xác minh được

- [ ] Text clean chạy là **bước đầu tiên** của pipeline ingest, trước khi extraction bắt đầu — đo bằng: log pipeline cho thấy thứ tự bước `text-clean → extraction`, không có thứ tự ngược lại xuất hiện trong bất kỳ lần chạy nào
- [ ] Với ≥1 chapter scrape thật (không phải văn bản sạch tự soạn), các mẫu rác đã biết (quảng cáo, lời tác giả cuối chương, watermark) bị loại trước khi vào extraction — đo bằng: so sánh input thô và input sau clean, các dòng rác đã biết không còn xuất hiện trong output
- [ ] Text clean áp dụng cho **100%** file upload đi qua ingest — đo bằng: rà soát code, không tồn tại đường gọi extraction nào bỏ qua bước clean
- [ ] Sau clean, extraction không sinh entity giả từ nội dung rác đã biết — đo bằng: chạy trên chapter test có quảng cáo chèn giữa nội dung, kết quả extraction không chứa entity nào bắt nguồn từ đoạn quảng cáo đó

### Đường không hạnh phúc (unhappy path)

- [ ] Chapter scrape có rác không khớp pattern regex/heuristic đã biết (dạng rác mới) — pipeline không crash, extraction vẫn chạy nhưng log ghi lại đoạn nghi ngờ chưa được lọc (đo bằng: pipeline hoàn tất không throw exception, log có cảnh báo tương ứng)
- [ ] Toàn bộ nội dung chapter bị heuristic coi là rác (over-aggressive clean, ví dụ chapter chỉ chứa hội thoại ngắn bị nhận nhầm là spam) — hệ thống dừng lại trước extraction và báo lỗi rõ ràng, không chạy extraction trên chuỗi rỗng (đo bằng: input toàn rác trả về lỗi tường minh, không tạo Story Bible rỗng)
- [ ] File scrape lỗi encoding (không phải UTF-8 sạch, ký tự tiếng Việt có dấu bị vỡ) — bước clean không crash và log ghi nhận tỉ lệ ký tự không giải mã được (đo bằng: chạy trên file cố tình lỗi encoding, pipeline hoàn tất, log có số liệu ký tự lỗi)

### Ràng buộc cứng không được vi phạm

- —

### Story này KHÔNG làm

- Không kiểm **opt-out signal Điều 37b** — đó là `Story-Opt-Out-Check-At-Ingest` (Epic-G), dù cùng chạy ở bước ingest
- Không thực hiện Story Bible extraction (nhân vật, địa điểm, trang phục) — đó là `Story-Story-Bible-Extraction`, chạy **sau** bước clean này
- Không sửa khoá thời gian — đó là `Story-Fix-Narrative-Time-Key`, đã phải xong trước
- Không xử lý input không phải văn bản (ảnh, PDF quét) — phạm vi chỉ text scrape từ nguồn chapter

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **10h** `[EM]` | Viết regex/heuristic deterministic cho các mẫu rác đã biết (quảng cáo, lời tác giả cuối chương, watermark) + wiring pipeline để text clean chạy trước extraction + xử lý encoding lỗi. Trong trần 16h |
| `E_hitl` | **0** | Text clean là bước deterministic, không tạo HITL gate; rác lọt qua được xử lý ở lần rà soát Story Bible qua `Story-Story-Bible-Editor-Form`, không tính vào Story này để tránh đếm trùng |

## 6. INVEST

- **I (Independent)**: ✅ — deliverable của nó (bước clean chạy trước extraction, chạy được trên chapter scrape thật) hoàn chỉnh mà không cần chờ Story nào khác của Epic-B, chỉ phụ thuộc gián tiếp vào việc chapter đã được upload (thuộc UC-01, không phải một Story của Epic này).
- **S (Small)**: ✅ — phạm vi hẹp, deterministic, không có sub-domain rẽ nhánh, nằm gọn trong trần `E_build ≤ 16h`.

---

_Created by product-owner_
_Author: trisjr_
