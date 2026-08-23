# Run Plan: 2026-08-23-danh-gia-y-tuong-comic-studio

**Lane**: doc · **Shape**: A (authoring) · **Tier**: T2 (điểm 2/4)

## Phases

| # | Phase | Agent | Song song? | Input | Output | Trạng thái |
|---|-------|-------|-----------|-------|--------|-----------|
| 1 | Intake & Triage | PM (main loop) | — | `Request.md`, `RULE-001`, `pm-core.md` | `brief.md` | ✅ Xong |
| 2a | Lens kiến trúc & data model | `architect` | ✅ Có (3 lens cùng lúc) | `Request.md`, `brief.md` | `findings/architect.md` | ✅ Xong — 8 tool call |
| 2b | Lens AI/ML pipeline | `senior-ai-engineer` | ✅ Có | `Request.md`, `brief.md` | `findings/senior-ai-engineer.md` | ✅ Xong — 8 tool call |
| 2c | Lens nghiên cứu thị trường & công nghệ | `researcher` | ✅ Có | `Request.md`, `brief.md`, web | trả trong final message → PM lưu `findings/researcher.md` | ✅ Xong — 53 tool call |
| 2d | Lens product & strategy | **PM (main loop)** | — | `Request.md` | `findings/product-manager-pm-lens.md` | ✅ Xong |
| 3 | **GATE** | PM | — | 4 findings | `run-plan.md` + `outline.md` + AskUserQuestion | ⏳ Đang trình |
| 4 | Doc plan | PM | — | 4 findings | `outline.md` | ✅ Xong |
| 5 | Soạn thảo tài liệu Analysis | `business-analyst` | Không (tuần tự) | `outline.md` toàn văn + 4 findings | `docs/050-Research/Analysis-Comic-Studio-Concept.md` | ⏳ Chờ gate |
| 5b | *(Tùy chọn — chờ anh chốt ở gate)* Risk Register | `quality-assurance` | ✅ Song song được với 5 (ownership rời) | `outline.md` + 4 findings | `docs/010-Planning/Risk-Register.md` | ⏳ Chờ gate |
| 6 | Verification | `context-auditor` | Không | tài liệu đã viết | `verdict.md` | ⏳ |
| 7 | Close-step | PM | — | `verdict.md` | Research-MOC, Glossary, `cost.md`, commit | ⏳ |

### Vì sao `business-analyst` viết, không phải `architect` hay `product-manager`

- **`architect` và `senior-ai-engineer` bị loại** vì đã tham gia fan-out. Người viết lại kết luận của chính mình sẽ neo vào (anchoring) và làm mất giá trị của việc tổng hợp chéo.
- **`researcher` bị loại** vì không có tool `Write`.
- **`product-manager` bị loại** theo `pm-core.md` Nguyên tắc 1 — vai trò PM do main loop giữ.
- **`business-analyst` được chọn**: có `Write`, remit là *"converting requirements into precise specifications, resolving ambiguity"* — đúng hình dạng việc tổng hợp 4 lens thành một tài liệu có cấu trúc. Và nó **chưa đọc gì** về dự án này ⇒ mắt sạch, buộc phải dựa vào findings chứ không dựa vào ký ức của chính mình.

## File ownership map

| Agent | Sở hữu (được ghi) | Cấm chạm |
|-------|-------------------|----------|
| `architect` (xong) | `findings/architect.md` | mọi thứ khác |
| `senior-ai-engineer` (xong) | `findings/senior-ai-engineer.md` | mọi thứ khác |
| `researcher` (xong) | **không file nào** (không có Write) | mọi thứ |
| `business-analyst` (phase 5) | `docs/050-Research/Analysis-Comic-Studio-Concept.md` | `*-MOC.md`, `docs/000-Index.md`, `outline.md`, `brief.md`, `findings/*`, `Request.md`, `docs/010-Planning/**` |
| `quality-assurance` (phase 5b, nếu duyệt) | `docs/010-Planning/Risk-Register.md` | `*-MOC.md`, `docs/000-Index.md`, `outline.md`, `Planning-MOC.md`, `docs/050-Research/**`, `findings/*` |
| `context-auditor` (phase 6) | `verdict.md` | **read-only trên toàn bộ `docs/` còn lại** |
| **PM** | `brief.md`, `run-plan.md`, `outline.md`, `cost.md`, `escalations.md`, `findings/product-manager-pm-lens.md`, phần *PM đọc được gì* của mọi findings, **và mọi `*-MOC.md` + `docs/000-Index.md` + `Glossary.md`** | — |

> Hai tập ownership của phase 5 và 5b **rời nhau tuyệt đối** (`050-Research/` vs `010-Planning/`) ⇒ chạy song song an toàn.
> `*-MOC.md`, `docs/000-Index.md`, `Glossary.md` **không cấp cho worker nào** — đây là điểm hội tụ, PM giữ độc quyền.

## Kế hoạch dispatch theo lô

| Lô | Gồm | Worker | Tuần tự / Song song | Ngân sách tool call |
|---|---|---|---|---|
| L1 | Lens kiến trúc | `architect` | Song song | 60 (dùng 8) |
| L2 | Lens AI pipeline | `senior-ai-engineer` | Song song | 60 (dùng 8) |
| L3 | Lens nghiên cứu | `researcher` | Song song | 60 (dùng 53) |
| L4 | Soạn `Analysis-Comic-Studio-Concept.md` — 12 mục | `business-analyst` | Song song với L5 | **60** |
| L5 | *(tùy chọn)* Soạn `Risk-Register.md` | `quality-assurance` | Song song với L4 | **45** |
| L6 | Verify 4 tiêu chí + spot-check citation | `context-auditor` | Tuần tự (sau L4/L5) | **50** |

**Tổng ngân sách cấp**: 60×3 + 60 + 45 + 50 = **335 tool call** (đã dùng 69 ở L1–L3).
Lane doc không có phụ cấp mutation-test.

## Artifact sẽ tạo/sửa ngoài run-state

| Đường dẫn | Mục đích | Loại (RULE-001) | Trạng thái đích |
|---|---|---|---|
| `docs/050-Research/Analysis-Comic-Studio-Concept.md` | **Deliverable chính** — trả lời 3 câu hỏi của anh | Research / Analysis → `Analysis-{Topic}.md` | `draft` |
| `docs/010-Planning/Risk-Register.md` *(tùy chọn)* | Sổ rủi ro có thể theo dõi được | Risk Register | `draft` |
| `docs/050-Research/Research-MOC.md` | Đăng ký tài liệu mới (bắt buộc, RULE-001 #4) | MOC | giữ nguyên |
| `docs/010-Planning/Planning-MOC.md` *(nếu có 5b)* | Đăng ký Risk Register | MOC | giữ nguyên |
| `docs/999-Resources/Glossary.md` | Bổ sung ~12 thuật ngữ của domain này | Glossary | `live` |

**Không** tạo `docs/000-Index.md` trong run này — đó là nợ kỹ thuật đã ghi ở `brief.md`, thuộc một run Shape B riêng. `Analysis` không phải tài liệu cấp PRD/SDD nên RULE-001 không buộc cập nhật `000-Index.md`.

## Assumptions

Xem `brief.md` mục *Assumptions* (A1–A5). Bổ sung sau fan-out:

- **A6 — Con số và citation của `researcher` là đúng như nó báo.** PM không tự verify 50 URL.
  → **Sai thì hỏng ở đâu**: verdict "khả thi" dựa nặng vào CANVAS (character 4.91/5) và CogCanvas (ID-Sim sụp từ 4 người). Nếu hai nguồn này bị đọc sai thì phần *Bảng khả thi* mất căn cứ.
  → **Giảm thiểu**: cấp cho `context-auditor` ở L6 nhiệm vụ **spot-check 3 citation load-bearing** (CANVAS, CogCanvas, Nghị định 134/2026), không phải verify cả 50.
- **A7 — Anh muốn một tài liệu thẳng thắn, không phải một bản khen.** Fan-out sinh ra nhiều phản biện mạnh (bác bỏ luận điểm moat, cắt 50-60% effort, gọi Layout Score là trang trí).
  → **Sai thì hỏng ở đâu**: nếu anh muốn một bản đánh giá nhẹ nhàng để giữ động lực, tài liệu này sẽ đọc như một bản phủ định. PM chọn thẳng thắn vì anh hỏi *"có khả thi hay không? Cần cải thiện, thay đổi gì không?"* — đó là câu hỏi xin phản biện, không xin xác nhận. Đã nêu ở gate.

## Gate

- **Trình ngày**: 2026-08-23
- **Kết quả**: *(chờ anh)*
- **Điều chỉnh của anh**: *(chờ anh)*

---

## Kết quả GATE — 2026-08-23

**Kết quả: DUYỆT như plan** (hạng mục 1 + 3 + 4; **không** làm Risk Register).

| Câu hỏi | Đáp án của anh |
|---|---|
| Duyệt plan | Duyệt như plan — một tài liệu Analysis 12 mục |
| Nguồn truyện (OQ1) | **Nền tảng cho người khác tự upload truyện của họ** |
| Mục tiêu (OQ2) | **Sản phẩm thương mại / SaaS** |
| Quy mô (A1) | Đúng — 1 mình anh + AI assist |

### Điều chỉnh phát sinh từ đáp án gate

Hai đáp án giữa **thay thế** phần "công cụ cá nhân" của A1 bằng "**SaaS thương mại multi-tenant**", làm vô hiệu 4 kết luận của phase 2. Xem `escalations.md` **E1** để biết chi tiết và lập luận phân xử.

**Phase bổ sung (2e) — chèn giữa gate và phase 5:**

| Lô | Gồm | Worker | Cơ chế | Ngân sách |
|---|---|---|---|---|
| L3b | Kiến trúc dưới SaaS multi-tenant: canvas editor còn cắt được không, multi-tenancy effort, seam kinh tế, cơ chế quota/cost-attribution | `architect` (**resume**, không spawn mới) | `SendMessage` — agent đã có full context | **25** |
| L3c | NĐ 134/2026 Điều 37a/37c cho nền tảng thương mại, nghĩa vụ platform với user-uploaded content, pricing đối thủ chi tiết, regen rate | `researcher` (**resume**) | `SendMessage` — trả text, PM lưu | **30** |
| L3d | Unit economics | **PM (main loop)** | tự làm | — |

**Vì sao resume thay vì spawn mới**: overhead một spawn ≈ 23.6k token và agent mới phải đọc lại `Request.md` (894 dòng) + findings. Hai agent này đã có sẵn toàn bộ context. `pm-core.md` Nguyên tắc 3 cấm *phụ thuộc* vào SendMessage, không cấm dùng như tiện ích — cả hai lệnh resume đã trả `success: true`. Nếu thất bại, phương án dự phòng là spawn mới với ngân sách 40.

**Ngân sách tổng cập nhật**: 335 + 25 + 30 = **390 tool call**.
