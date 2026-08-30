# Run Plan: 2026-08-30-brand-guidelines-va-design-system-comic-studio

**Lane**: doc · **Shape**: A · **Tier**: T3 (điểm 4/4)
**Worktree**: `.claude/worktrees/phase-3-brand-design-system`, branch `worktree-phase-3-brand-design-system`

## Tóm tắt phân tích (Bước 2 — 3 lens, đều `DONE`, không lens nào vượt ngân sách)

1. **Hai hệ font BẮT BUỘC tách** — cả `product-designer` và `architect` độc lập kết luận giống nhau. Font UI là lựa chọn thẩm mỹ; font render là **tham số đầu vào của thuật toán wrap**, phải **đơn trị, ⛔ không fallback stack**. Gộp một bộ ⇒ ngắt dòng tính theo font A, glyph vẽ bằng font B ⇒ dấu bị mép bubble cắt, **chỉ lộ sau khi ảnh đã sinh** (đã tiêu tiền), và `D-29` cấm nướng chữ vào pixel nên ⛔ không có đường vá nhanh. ⚠️ **⛔ Không tài liệu nào trong repo đang nói điều này** — không tách ở tầng 040 thì không ai tách hộ.
2. **`architect` sản xuất 38 ràng buộc cứng `ARC-01`…`ARC-38`**, mỗi cái có nguồn + dấu hiệu verify. Nặng nhất: `API-HG-6` cấm batch ⇒ ⛔ **không được có component "Duyệt cả trang"**; `SDD-HG-01.1` cấm mọi control pre-selected; **Preview ⛔ KHÔNG bị chặn bởi gate, Export thì bị** ⇒ hai bề mặt riêng.
3. **`business-analyst` đọc đủ 11/11 UC kể cả Exception flow** — 67 nhánh ngoại lệ ⇒ **19 surface + 6 bề mặt xuyên suốt → 12 nhóm màn hình**; **24 component**, trong đó **16 không hoãn được**. Quan trọng nhất là `C-01` **Alert ba mức** (13 surface): repo phân biệt gắt *"bị TỪ CHỐI ở tầng DB"* vs *"cảnh báo, cho qua được"* — trộn hai mức là **lỗi nghiệp vụ, không phải lỗi thẩm mỹ**.
4. **Có bề mặt bị CẤM và có bề mặt BẮT BUỘC.** Cấm mọi biểu đạt phán đoán bản quyền (`SRS-NFR-15` anti-feature — badge "đã kiểm", icon shield, nhãn "Original", cả brand messaging kiểu *"an tâm về bản quyền"*). Bắt buộc **AI-disclosure indicator** (`SRS-FR-40`, mức **CHỐT**): bằng chứng tuân thủ là *một bề mặt UI*, ⛔ không để lại hàng dữ liệu ⇒ **không có Design System thì nghĩa vụ này không có nhà**.
5. **Ba khoảng trống repo không có gì**, xác nhận bằng grep thật, ⛔ không lens nào lấp: **persona/JTBD** · **accessibility/responsive** (0 hit trong toàn `020-Requirements/`) · **màu, logo, tên hiển thị**.

### Mâu thuẫn giữa các lens — PM phân xử

| # | Mâu thuẫn | Phân xử |
|---|---|---|
| `X-1` | Độ rắn `D-45` (polling 2s) đọc ra hai kiểu: `SRS`+`ADR-015` ghi **MẶC ĐỊNH**, `ADR-001` xếp dưới tiêu đề *"⛔ không mở lại"* | **⛔ Không chặn run.** Design System chỉ cần khai **trạng thái chờ**, thứ này độc lập với transport. Writer mô tả trạng thái theo `job_status`, ⛔ không hardcode "2 giây" như hằng số thiết kế. Mâu thuẫn thuộc tầng 030 ⇒ ghi vào *Nợ*, ⛔ run này không sửa ADR |
| `X-2` | `brief.md` §Assumptions #2 gán cho `ADR-001` danh sách tên biến CSS (`--background`…) mà ADR ⛔ **không hề có** | **Lens đúng, PM sai. ĐÃ SỬA `brief.md`.** Tên biến shadcn là **quyết định Phase 3**, writer phải dán nhãn như vậy và verify theo version thật, ⛔ không trích `ADR-001` làm nguồn |
| `X-3` | Mọi neo (`ADR-001`/`ADR-013`/`SDD`/`SRS`) đều `status: draft` | **⛔ Không chặn.** Toàn bộ 57 tài liệu Phase 2 là `draft` — đây là trạng thái đã biết của repo, ⛔ không phải phát hiện mới. Design System cũng sẽ là `draft` |
| `X-4` | BA đính chính: prompt của PM ghi *"14 NFR TBD"*; `SRS` §5.2 thực có **21 hàng**, §3.9 có **7** (nghĩa khác) | **BA đúng.** Con số 14 lấy từ `000-Index.md`, ⛔ không phải từ `SRS`. Writer đối chiếu `SRS` trực tiếp, ⛔ không dùng lại con số của Index |
| `X-5` | BA phát hiện `SRS-NFR-09` (tầng 020) vẫn ghi framework frontend **CHƯA QUYẾT → TBD**, trong khi `ADR-001` (tầng 030) đã chốt | **Ripple thật, nhưng ngoài lane.** Run này ⛔ **không sửa SRS**. Ghi vào *Nợ* để anh xử ở run đồng bộ tầng 020↔030 |

### Lỗi repo phát hiện được (⛔ không sửa trong run này)

- **`UC-09`, `UC-10`, `UC-11` bị lọt tag XML của tool call vào cuối file** (`</content>`). BA báo, ⛔ không sửa vì ngoài ownership. → *Nợ*, sửa ở run dọn riêng.

## Phases

| # | Phase | Agent | Song song? | Input | Output |
|---|-------|-------|-----------|-------|--------|
| 0 | Analysis fan-out ✅ **xong** | `product-designer` · `architect` · `business-analyst` | ✅ 3 song song | brief + repo | 3 file `findings/` |
| 1 | **GATE** | PM | — | findings | `run-plan.md` + quyết định của anh |
| 2 | Doc plan | PM | — | gate | `outline.md` |
| 3 | **Lô 1** — nguồn của mọi file sau | `product-designer` | ❌ tuần tự | gate + findings | `Brand-Guidelines.md` · `Foundations.md` |
| 4 | **Lô 2** ‖ **Lô 3** | `product-designer` ×2 | ✅ song song | Lô 1 đã đóng | Lô 2: `Color-Tokens.md` · `Spacing-And-Layout.md` — Lô 3: `Typography.md` |
| 5 | **Lô 4** | `product-designer` | ❌ tuần tự | Lô 2+3 đã đóng | `Components.md` |
| 6 | **Lô 5** | `business-analyst` | ❌ tuần tự | 6 file trên đã đóng | Bổ sung thuật ngữ `Glossary.md` |
| 7 | **Lô 6 — verify** | `context-auditor` | ❌ tuần tự | toàn bộ deliverable | `verdict.md` |
| 8 | Close-step | PM | — | verdict | `Design-MOC.md` · `000-Index.md` · `cost.md` |

> **Vì sao Lô 1 phải chạy một mình trước.** `Foundations.md` phát biểu *hợp đồng token* — thứ 4 file sau đều **đọc** để tuân theo; `Brand-Guidelines.md` là nguồn của màu chủ đạo mà `Color-Tokens.md` **đọc**. Dispatch lô đọc khi lô sửa chính nguồn đó chưa đóng là đúng lỗi đã làm run `2026-08-28` tốn **~$90 = 21% chi phí subagent** cho 8 lô dọn. Giao file rời nhau **⛔ không đủ** — phải rời nhau **cả về thời gian**.

> **Vì sao `Typography.md` đứng riêng một lô.** Đây là file **rủi ro cao nhất** (hai hệ font, `TBD-FONT` chưa đóng, dấu tiếng Việt) và **dài nhất** (~250–350 dòng). Ghép nó với file khác là ép writer chọn giữa làm kỹ và lọt ngân sách.

## File ownership map

| Agent | Sở hữu (được ghi) | Cấm chạm |
|-------|-------------------|----------|
| Lô 1 · `product-designer` | `docs/040-Design/Design-System/Brand-Guidelines.md`<br>`docs/040-Design/Design-System/Foundations.md` | mọi `*-MOC.md` · `docs/000-Index.md` · `outline.md` · `brief.md` · `findings/**` · mọi file 010/020/030 · `Glossary.md` · file của lô khác |
| Lô 2 · `product-designer` | `docs/040-Design/Design-System/Color-Tokens.md`<br>`docs/040-Design/Design-System/Spacing-And-Layout.md` | — nt — + `Typography.md` (lô 3 đang giữ) |
| Lô 3 · `product-designer` | `docs/040-Design/Design-System/Typography.md` | — nt — + `Color-Tokens.md`, `Spacing-And-Layout.md` (lô 2 đang giữ) |
| Lô 4 · `product-designer` | `docs/040-Design/Design-System/Components.md` | — nt — |
| Lô 5 · `business-analyst` | `docs/999-Resources/Glossary.md` | — nt — + toàn bộ `docs/040-Design/**` (chỉ đọc) |
| Lô 6 · `context-auditor` | `docs/010-Planning/pm-runs/<run-id>/verdict.md` | **READ-ONLY toàn repo** ngoài `verdict.md` |
| **PM (không cấp cho ai)** | `docs/040-Design/Design-MOC.md` · `docs/000-Index.md` · `outline.md` · `brief.md` · `run-plan.md` · `escalations.md` · `cost.md` · `findings/**` | — |

> ⚠️ **Lô 2 và Lô 3 chạy song song và cùng dùng agent type `product-designer`** — hợp lệ vì tập file **rời nhau tuyệt đối** và **cả hai chỉ ĐỌC** `Foundations.md`/`Brand-Guidelines.md` (đã đóng ở Lô 1), ⛔ không lô nào sửa nguồn của lô kia.

## Kế hoạch dispatch theo lô — ngân sách tool call

| Lô | File | Số file | Ngân sách | Ghi chú |
|---|---|:--:|:--:|---|
| Lô 1 | `Brand-Guidelines.md` · `Foundations.md` | 2 | **60** | Không có phụ cấp mutation-test (lane doc) |
| Lô 2 | `Color-Tokens.md` · `Spacing-And-Layout.md` | 2 | **60** | |
| Lô 3 | `Typography.md` | 1 | **60** | 1 file nhưng nặng nhất run — ngân sách đầy đủ là cố ý |
| Lô 4 | `Components.md` | 1 | **60** | Phải phủ 16 component không hoãn được |
| Lô 5 | `Glossary.md` (bổ sung) | 1 | **45** | Lô quét có phạm vi hẹp, chỉ append nhóm thuật ngữ mới |
| Lô 6 | `verdict.md` (verify, read-only) | 1 | **60** | ⚠️ Read-only **⛔ KHÔNG miễn trần** — đây đúng là chỗ agent đắt nhất run `2026-08-22` chui lọt (26.5M, 19% toàn run) |

**Tổng ngân sách cấp**: 3 lens (đã dùng **18+28+28 = 74**/180) + 6 lô × ~58 = **~345 tool call** cho cả run.
**`advisor`**: cấp cho **Lô 1** và **Lô 3** (hai lô ra quyết định thiết kế thật). ⛔ Cắt ở Lô 2, 4, 5, 6 — lô sản xuất theo hợp đồng đã chốt và lô quét cơ học.

## Artifact sẽ tạo/sửa ngoài run-state

| Đường dẫn | Loại (RULE-001) | Mục đích | Ai ghi |
|---|---|---|---|
| `docs/040-Design/Design-System/Brand-Guidelines.md` | Design System ⚠️ **chờ Q-A** | Nền brand: tên, tone, màu chủ đạo, điều cấm | Lô 1 |
| `docs/040-Design/Design-System/Foundations.md` | Design System | Hợp đồng token, kiến trúc primitive→semantic, chuẩn a11y | Lô 1 |
| `docs/040-Design/Design-System/Color-Tokens.md` | Design System | Palette + semantic mapping + contrast audit | Lô 2 |
| `docs/040-Design/Design-System/Spacing-And-Layout.md` | Design System | Thang spacing, radius, elevation, breakpoint, z-index | Lô 2 |
| `docs/040-Design/Design-System/Typography.md` | Design System | ⭐ **Hai hệ font**, thang cỡ, tiếng Việt, NFC | Lô 3 |
| `docs/040-Design/Design-System/Components.md` | Design System | Inventory + ma trận state + ánh xạ shadcn/Radix | Lô 4 |
| `docs/999-Resources/Glossary.md` | Glossary | Bổ sung nhóm thuật ngữ design | Lô 5 |
| `docs/040-Design/Design-MOC.md` | *(MOC — hiện **0 byte**)* | Viết từ số 0 | **PM** |
| `docs/000-Index.md` | Index | Cập nhật mục 040-Design + gỡ dòng *"MOC 0 byte"* ở Nợ kỹ thuật | **PM** |

> ⚠️ **`docs/030-Specs/Architecture/ADR-001-*.md` hiện hiện `M` trong `git status` của worktree.** Đây là **bản anh đang sửa ở checkout gốc, PM copy sang làm input read-only**, ⛔ **KHÔNG phải deliverable của run này** và **⛔ sẽ KHÔNG được commit** cùng run. Anh giữ quyền commit nó ở checkout gốc.

## Gate

- **Trình ngày**: 2026-08-30
- **Kết quả**: ✅ **DUYỆT** — anh chọn đúng 4/4 phương án PM đề xuất.
- **Điều chỉnh của anh**: không có.

### Bốn quyết định đã chốt — ràng buộc bắt buộc cho mọi writer

| # | Quyết định | Hệ quả trực tiếp lên writer |
|---|---|---|
| **G-1** | **Brand: trung tính, accent lạnh (xanh/indigo).** Tone điềm tĩnh, tin cậy, ⛔ không ồn ào | Lý do neo, ⛔ không phải sở thích: sản phẩm **luôn hiển thị artwork comic nhiều màu** ngay trong editor và preview ⇒ UI có màu mạnh sẽ **cạnh tranh với chính nội dung người dùng đang đánh giá**. Mọi lựa chọn màu phải kiểm lại bằng câu hỏi này. Accent lạnh còn **tách bạch được với dải màu cảnh báo** của `C-01` Alert ba mức (13 surface) |
| **G-2** | **Light là default; token khai ĐỦ CẶP light/dark ngay** — dark ⛔ chưa implement ở MVP | Lý do chọn light: **preview trang comic có nền trắng giấy**; đặt lên chrome tối làm lệch chính cảm nhận người dùng đang đánh giá. Khai sẵn cặp dark ⇒ ⛔ **không retrofit** tầng semantic token về sau. Chi phí ≈ một cột trong bảng token |
| **G-3** | **WCAG 2.2 Level AA**, phạm vi giới hạn luồng chính, **desktop-first** | ⭐ **Kéo theo SC 2.5.7 Dragging Movements**: kéo bubble/kéo đuôi trỏ (`SRS-FR-16`, đã **CHỐT**) **BẮT BUỘC có đường thao tác thay thế không-kéo** ⇒ đây là **UI thật phải đặc tả trong `Components.md`**, ⛔ không phải một dòng CSS. Đồng thời `Foundations.md` là **chỗ duy nhất** phát biểu chuẩn a11y ⇒ tiêu chí gate kiểm cơ học được |
| **G-4** | `Brand-Guidelines.md` **map vào hàng `Design System`** sẵn có ⇒ `docs/040-Design/Design-System/Brand-Guidelines.md`. ⛔ **KHÔNG sửa RULE-001** | Q2 của triage **hạ nhiệt**: run này ⛔ không còn đụng tài liệu `status: approved` nào. Điểm yếu đã biết và chấp nhận: `type:` frontmatter mang giá trị lỏng (tiền lệ RULE-001: hàng *User Story* ứng `type: story`) |

> ⚠️ **Vẫn còn MỘT khoảng trống anh chưa lấp, và writer ⛔ KHÔNG được lấp hộ: TÊN HIỂN THỊ thương mại.**
> `comic-studio` là **project name** (`Charter` §1), ⛔ không phải tên sản phẩm. Tên thương mại là quyết định **kinh doanh + pháp lý**. `Brand-Guidelines.md` phải ghi `TBD` **có chủ** (Founder) tại mục tên, ⛔ tuyệt đối không tự đặt tên, ⛔ không suy ra logo/wordmark từ nó.
