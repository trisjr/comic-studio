---
id: STORY-B-03
type: story
status: draft
created: 2026-08-24
---

# Story-Story-Bible-Extraction

## 1. Story

Là tác giả truyện chữ, tôi muốn **nhân vật, địa điểm, trang phục được rút ra tự động từ chapter**, để **không phải khai tay toàn bộ Story Bible**

## 2. Part of

- Epic cha: [Epic-Story-Intelligence](../Epics/Epic-Story-Intelligence.md)
- BRD: [BRD-002-Story-Intelligence](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)
- Use Case liên quan: [UC-02-Review-And-Edit-Story-Bible](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) — extraction tự động là bước sinh dữ liệu mà UC-02 cho tác giả xác nhận/sửa; đầu vào lấy từ [UC-01-Upload-And-Ingest-Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) sau bước text clean

## 3. Bối cảnh & nguồn

Đây là hàng **`B2`** của [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope): *"Story Bible extraction tự động (character, location, costume)"* — `❌ viết tay` ở MVP0, `✅` từ MVP1 trở đi, căn cứ CF-8.4 (*"không code extraction"* ở MVP0) và CF-8.7.

Exit criterion tương ứng là **`M1-3`** của [Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng), mốc **MVP1**: *"extraction đạt **≥80%** entity (nhân vật + địa điểm) khớp với Story Bible viết tay của MVP0"*. ⚠️ Ngưỡng 80% là `[EM]` **do `Roadmap` TỰ ĐỊNH NGHĨA** — ⛔ **cấm trích như số đo hoặc benchmark ngành**. Dưới ngưỡng ⇒ **tăng phần human-in-the-loop, không kéo dài mốc** (nguyên văn hàng rủi ro của [Roadmap §1.4](../../010-Planning/Roadmap.md#14-giả-định-của-lộ-trình--mỗi-cái-kèm-sai-thì-hỏng-ở-đâu)). ⚠️ **Ngưỡng không được sửa sau khi nhìn kết quả** (`CẤM-16` của `findings/business-analyst.md` §5.3).

[Epic-Story-Intelligence §5](../Epics/Epic-Story-Intelligence.md#5-definition-of-done-cấp-epic) ghi thêm điều kiện DoD: Story Bible phải tách **Identity** (bất biến qua chương) khỏi **Appearance** (thay đổi theo trạng thái) — gộp hai thứ vào một field là **nguyên nhân của phần lớn lỗi consistency** (PRD `FR-B-02`). Định nghĩa hai khái niệm này ở [Glossary.md](../../999-Resources/Glossary.md) mục *Identity vs Appearance*.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Extraction tự động rút ra được nhân vật, địa điểm, trang phục từ text đã qua text-clean của ≥1 chapter scrape thật — đo bằng: tồn tại record Story Bible cho chapter đó ngay sau khi pipeline chạy xong, không cần nhập tay
- [ ] Tỉ lệ entity (nhân vật + địa điểm) khớp với Story Bible viết tay của MVP0 đạt **≥80%** `[EM]` (`M1-3`) — đo bằng: đối chiếu tự động/thủ công giữa danh sách entity extraction sinh ra và bible viết tay, tính tỉ lệ % khớp
- [ ] Mỗi entity extraction sinh ra có `generation.origin = 'ai'` — đo bằng: query entity vừa tạo, field `origin` đúng giá trị này (khớp KC-3)
- [ ] Record nhân vật tách riêng nhóm field **Identity** (bất biến) khỏi nhóm field **Appearance** (theo trạng thái) — đo bằng: schema/record cho thấy hai nhóm field tách biệt trên cùng một entity, không gộp chung một field mô tả tự do

### Đường không hạnh phúc (unhappy path)

- [ ] Chapter có tên nhân vật viết hoa/thường không nhất quán (lỗi scrape) khiến extraction tách một người thành hai entity — hệ thống **không** tự động merge âm thầm; cả hai entity vẫn tồn tại và truy vấn được, chờ tác giả xử lý qua `Story-Story-Bible-Editor-Form` (đo bằng: cả hai entity đều xuất hiện trong kết quả, không entity nào biến mất ngầm)
- [ ] Extraction chạy trên chapter cho tỉ lệ khớp thực đo **dưới 80%** — hệ thống KHÔNG tự hạ ngưỡng hay đề xuất kéo dài mốc (`CẤM-16`); thay vào đó số lượng entity được đánh dấu `cần xác nhận thủ công` tăng lên (đo bằng: khi tỉ lệ khớp <80%, đếm entity ở trạng thái `cần xác nhận` > 0 và ngưỡng 80% trong cấu hình không đổi)
- [ ] Chapter có nhân vật chỉ được nhắc gián tiếp (đại từ, biệt danh, không có tên riêng) — extraction không tạo entity rác từ đại từ nhân xưng thuần (đo bằng: rà soát danh sách entity sinh ra, không có mục nào là đại từ nhân xưng đứng một mình)

### Ràng buộc cứng không được vi phạm

- —

### Story này KHÔNG làm

- Không cho tác giả sửa entity bằng tay — đó là `Story-Story-Bible-Editor-Form` (Epic-D)
- Không dùng `pgvector`/vector search để hỗ trợ extraction — `B5` bị `❌` tới MVP2, không dùng ở mốc này **nhưng không bị cấm vĩnh viễn** (Full Scope `🟡` khi có bằng chứng SQL+FTS không đủ)
- Không tự sửa khoá thời gian — phụ thuộc `Story-Fix-Narrative-Time-Key` đã phải xong trước
- Không phải là Timeline State Resolver — đó là `Story-Timeline-State-Resolver`, tiêu thụ event do Story này sinh ra

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **18h** `[EM]` — **vượt trần 16h, lý do ghi thành văn** | Extraction phải phủ **ba loại entity khác nhau** (nhân vật, địa điểm, trang phục) từ text tiếng Việt scrape thật, tách được Identity/Appearance, và cần một vòng lặp hiệu chỉnh (tuning) để tiệm cận ngưỡng `M1-3 ≥80%` `[EM]` — bản thân ngưỡng chỉ đo được sau khi có dữ liệu thật, nên khối lượng cần cho vòng lặp hiệu chỉnh không nén gọn trong 16h như một extraction đơn loại |
| `E_hitl` | **0** cho chính Story này | Phần con người xác nhận/sửa entity dưới ngưỡng 80% được **Story-Story-Bible-Editor-Form** (Epic-D) sở hữu và đã tính `~0,5h/chapter` `[EM]` ở đó — không đếm trùng vào Story này |

## 6. INVEST

- **I (Independent)**: ✅ — deliverable (entity extraction chạy được, đo được tỉ lệ khớp) hoàn chỉnh không cần Story nào khác của Epic-B hoàn tất song song, chỉ phụ thuộc nền vào `Story-Chapter-Ingest-And-Text-Clean` (đã khai ở mục 2/3) và `Story-Fix-Narrative-Time-Key` (mục *KHÔNG làm*).
- **S (Small)**: ⚠️ — **[PO suy luận, KHÔNG có trong bảng `findings/business-analyst.md` §4.10]**. Nguồn chấm `S = ⚠️` ở bảng §4.2 nhưng bảng §4.10 chỉ liệt 7 Story khác, không giải thích lý do cho Story này. Lý do PO tự suy ra: (1) extraction phải phủ ba loại entity khác nhau trong cùng một lần chạy, không phải một loại đơn giản; (2) ngưỡng `M1-3 ≥80%` chỉ đo được **sau khi** có dữ liệu thật, nên khối lượng thật sự (bao nhiêu vòng hiệu chỉnh cần) không biết trước khi MVP1 chạy — đúng loại bất định mà [Roadmap §1.4](../../010-Planning/Roadmap.md#14-giả-định-của-lộ-trình--mỗi-cái-kèm-sai-thì-hỏng-ở-đâu) đã cảnh báo (*"nếu extraction không đạt trên truyện tiếng Việt scrape thật, MVP1 phồng lên"*). Đây là lý do `E_build` ở mục 5 vượt trần 16h.

---

_Created by product-owner_
_Author: trisjr_
