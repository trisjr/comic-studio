# Doc Plan: 2026-08-23-danh-gia-y-tuong-comic-studio

> `docs/999-Resources/Templates/Template-Analysis.md` là **stub** (chỉ frontmatter + "(Content to be added)").
> Vì vậy **file này là contract cấu trúc thật** của deliverable, không phải template.
> Chỉ PM tick cột *Xong*, sau khi đối chiếu `FILES_TOUCHED`.

## Hạng mục

| # | Tài liệu | Loại (RULE-001) | Đích | Trạng thái đích | Writer | Xong |
|---|----------|-----------------|------|-----------------|--------|------|
| 1 | Phân tích & thẩm định ý tưởng comic-studio | Research / Analysis | `docs/050-Research/Analysis-Comic-Studio-Concept.md` | `draft` | `business-analyst` §1–6 + PM §7–12 | [x] |
| 2 | *(Tùy chọn — chờ gate)* Sổ rủi ro | Risk Register | `docs/010-Planning/Risk-Register.md` | `draft` | `quality-assurance` | ❌ anh **không** duyệt tại gate |
| 3 | Bổ sung thuật ngữ domain | Glossary | `docs/999-Resources/Glossary.md` | `live` | **PM** (close-step) | [x] |
| 4 | Đăng ký MOC | MOC | `docs/050-Research/Research-MOC.md` | giữ nguyên | **PM** (close-step) | [x] |

> **Ghi chú tick hạng mục 1:** `business-analyst` trả payload §1–§6 dưới dạng **text** (harness chặn subagent ghi file), PM ghi file. §7–§12 + Tài liệu tham khảo do PM tự viết, không dispatch batch 2 — vì đã biết trước cùng một guardrail sẽ chặn lần nữa. `FILES_TOUCHED` của worker: **rỗng** (không sở hữu file nào) — đối chiếu xong, hợp lệ. Tick sau khi `context-auditor` trả `PASS_WITH_ISSUES` (0 CRITICAL) và PM đã vá xong 4 MAJOR + 9 MINOR; xem `verdict.md`.

---

## Outline tài liệu 1 — `Analysis-Comic-Studio-Concept.md`

- **Độc giả đích**: **anh trisjr**, với tư cách người ra quyết định build / không build / build khác đi. Một người, đã đọc kỹ `Request.md` (tự viết ra nó), có nền kỹ thuật. **Không** phải investor, **không** phải team ngoài. ⇒ Không cần giải thích lại ý tưởng cho người chưa biết; được phép tham chiếu `§n` của `Request.md` mà không trích lại toàn văn. Được phép đi thẳng vào phản biện.
- **Tiêu chí xong** (đo được, không phải "viết đầy đủ"):
  1. Trả lời tách bạch **3 câu hỏi** anh đặt ra: *(a)* phù hợp hay chưa, *(b)* khả thi hay không, *(c)* cần cải thiện/thay đổi gì. Mỗi câu có một verdict phát biểu được trong một câu.
  2. Mọi khẳng định định lượng đều **truy được về findings** — nêu rõ lens nào và, nếu là dữ liệu web, kèm URL.
  3. Mọi khuyến nghị **hành động được**: nêu rõ *sửa cái gì → thay bằng cái gì → không sửa thì hỏng thế nào*.
  4. Ghi rõ **những gì bản phân tích này KHÔNG biết** (9 khoảng trống của `researcher` + 3 open question).
  5. Không chỗ nào để `TBD` mà không nói vì sao và ai trả lời được.
- **Ngôn ngữ**: Tiếng Việt, giữ nguyên technical term (`.claude/rules/create-file-markdown.md`).
- **Bắt buộc theo `create-file-markdown.md`**: có **Table of Contents** ở đầu, **Tài liệu tham khảo** ở cuối (đây là tài liệu tri thức, không phải workflow/rule).
- **Link**: standard markdown link relative path theo `RULE-001` §Linking Rules. **KHÔNG** dùng wiki-link `[[...]]`.

### Frontmatter bắt buộc

```yaml
---
id: RESEARCH-001
type: research
status: draft
project: comic-studio
owner: "@trisjr"
tags: [comic-studio, feasibility, architecture-review, ai-pipeline]
created: 2026-08-23
updated: 2026-08-23
---
```

### Nguồn sự thật (writer KHÔNG được bịa ngoài bốn nguồn này)

| Nguồn | Dùng cho |
|---|---|
| `docs/999-Resources/Request.md` | mọi tham chiếu `§n`, nội dung ý tưởng gốc |
| `../pm-runs/2026-08-23-.../findings/architect.md` | kiến trúc, DDL, temporal model, ước lượng effort §14 |
| `../pm-runs/2026-08-23-.../findings/senior-ai-engineer.md` | pipeline LLM, Layout Score, Continuity Checker, ranh giới LLM/code, HITL |
| `../pm-runs/2026-08-23-.../findings/researcher.md` | **mọi con số và URL**, bảng khả thi, pháp lý, chi phí, đối thủ |
| `../pm-runs/2026-08-23-.../findings/product-manager-pm-lens.md` | product/moat/scope, và các phân xử của PM |

> Phần **PM đọc được gì** và **Mâu thuẫn với lens khác** trong mỗi findings là **phân xử đã chốt của PM** — writer phải theo, không được kết luận khác.

### Cấu trúc (heading cấp 1–2, thứ tự bắt buộc)

```
# Phân tích & Thẩm định Ý tưởng comic-studio

## Mục lục

## 1. Tóm tắt cho người ra quyết định
    - 3 verdict, mỗi cái một câu (phù hợp / khả thi / cần đổi gì)
    - Bảng: 4 lens × verdict × phát hiện quan trọng nhất
    - "Nếu chỉ đọc một mục": 5 việc làm ngay, xếp theo thứ tự
## 2. Phạm vi & phương pháp
    - Đối tượng: Request.md, 894 dòng, 18 mục
    - 4 lens: cái gì được verify bằng web, cái gì là lập luận, cái gì là ước lượng
    - Giả định A1-A7 (từ brief.md + run-plan.md) và hệ quả nếu sai
    - Giới hạn của chính bản phân tích này
## 3. Câu hỏi 1 — Ý tưởng có phù hợp hay chưa?
    ### 3.1 Với tư cách một thiết kế kỹ thuật: có
    ### 3.2 Với tư cách một sản phẩm: chưa xác định được — và vì sao đó là phát hiện
    ### 3.3 Bốn thứ tài liệu làm ĐÚNG, đừng đổi
         (spec-là-dữ-liệu-chính trùng khớp ranh giới bản quyền Zarya;
          identity/appearance split; Comic IR; timeline là first-class)
## 4. Câu hỏi 2 — Có khả thi hay không?
    ### 4.1 Verdict: khả thi có điều kiện — 4 điều kiện đồng thời
    ### 4.2 Bảng khả thi từng thành phần (12 dòng, có bằng chứng + nguồn)
    ### 4.3 Phát hiện đảo chiều: kiến trúc này ĐÃ được validate bằng số (CANVAS)
    ### 4.4 Boss cuối thật không phải cái tài liệu nghĩ
## 5. Câu hỏi 3a — Sáu vấn đề phải sửa TRƯỚC khi viết code
    ### 5.1 `(chapter, scene)` làm khóa thời gian — sai âm thầm ở flashback
    ### 5.2 Continuity Checker: từ "flag lỗi + autofix" sang "chọn giữa N ứng viên"
    ### 5.3 Layout Score: bỏ số thực, dùng rubric rời rạc
    ### 5.4 Chữ & speech bubble — mục bị bỏ sót hoàn toàn
    ### 5.5 Ranh giới LLM / deterministic code chưa được vẽ
    ### 5.6 `≤3 nhân vật/panel` — ràng buộc cứng, có số làm căn cứ
## 6. Câu hỏi 3b — Ba thứ nên CẮT khỏi MVP
    ### 6.1 Canvas editor §14 — 50-60% tổng effort, và không cần thiết
    ### 6.2 Microservices + Vector DB §12
    ### 6.3 Cây `parent_generation`? — KHÔNG, và đây là chỗ PM tự thu hồi khuyến nghị
## 7. Phản biện luận điểm "moat"
## 8. Rủi ro pháp lý & compliance
## 9. Chi phí thật — và đơn vị đo đúng
## 10. Lộ trình đề xuất: MVP0 đi trước
## 11. Những gì bản phân tích này KHÔNG biết
## 12. Kết luận

## Tài liệu tham khảo
```

### Ràng buộc nội dung theo từng mục — writer phải tuân thủ

| Mục | Ràng buộc |
|---|---|
| **1** | Tối đa 1 trang. Ba verdict phải phát biểu được thành ba câu độc lập. Bảng 4 lens phải nêu **phát hiện quan trọng nhất** của từng lens, không phải tóm tắt lens. |
| **3.1 / 3.2** | Phải giữ **sự tách bạch** này. Đây là phát hiện của lens PM, không được gộp thành một verdict mờ. `Request.md` là thiết kế kiến trúc cho một sản phẩm chưa được định nghĩa — nói rõ, kèm bảng bằng chứng "có gì / không có gì". |
| **3.3** | **Bắt buộc có mục này và đặt trước phần phản biện.** Tài liệu có nhiều điểm đúng; một bản đánh giá chỉ toàn phản biện là bản đánh giá sai. Nêu cả chi tiết Zarya: phần *được bảo hộ* là panel layout + arrangement + text — đúng output của Comic IR ⇒ quyết định kiến trúc của tác giả trùng khớp đường ranh pháp lý. |
| **4.2** | Dùng đúng bảng 12 dòng của `researcher` §8.2, giữ nguyên ký hiệu ✅/🟡/❌/⚪ và **giữ nguyên con số**. Cột bằng chứng phải có URL. Không thêm dòng nào không có bằng chứng. |
| **4.3** | CANVAS (arXiv 2604.13452, 15/04/2026): character 4.91/5, BG 4.88/5, props 4.19/5, human win-rate 86,7%, backbone Gemini-3-pro-image. Nêu **cả hai chiều**: tốt (không phải đánh cược) và xấu (concept đã public ⇒ không phải moat). |
| **5.1** | Phải nêu **hệ quả dây chuyền**: lỗi này làm Continuity Checker "sửa" đúng những panel đang đúng. Trích DDL cụ thể từ `architect.md` (hai trục `reading_order`/`story_order`, `timeline_id`, index, state neo vào `Event`). Giải thích syuzhet vs fabula bằng một câu. |
| **5.2** | ⭐ **Mục quan trọng nhất của tài liệu — trình bày đầy đủ lập luận M8.** `senior-ai-engineer` nói checker tạo giá trị âm (FP cao, vòng lặp re-identification, `✓ face` khó nhất trên art cách điệu); `researcher` nói VLM continuity check "đã giải được" (MIE 0.922 pairwise). **Cả hai đúng vì nói về hai task khác nhau**: *pairwise ranking* (đã validate) vs *absolute per-panel detection* (chưa). Bằng chứng phân xử: CANVAS dùng VLM để **select giữa N candidate**, không dùng làm checker gắn nhãn + autofix. Kết luận: giữ công nghệ, đổi cách dùng. |
| **5.3** | Nêu bằng chứng tự tố: `dialogue density 0.20` là đại lượng **code đếm được** mà lại giao cho LLM đoán; và không có hàm tổng hợp nào được định nghĩa cho 5 số ⇒ nếu LLM gộp luôn thì 5 số là biện minh hậu nghiệm. Ghép với `researcher` ⚪ (không có prior art) ⇒ đây là "chưa ai làm vì không đáng", không phải "thật sự mới". Đề xuất thay thế cụ thể. |
| **5.4** | Ba lý do **độc lập** buộc dùng typeset layer riêng, và nêu rõ **không** lý do nào trong đó là "model render dở": editability, bubble không che mặt (`text_safe_zone` phải đi ngược vào panel spec + prompt compiler), ranh giới bản quyền. Nêu trung thực: press VN xác nhận Nano Banana Pro render tiếng Việt có dấu tốt, nhưng **không có benchmark định lượng**; và Comical-JS chưa có auto-placement ⇒ phải tự build. |
| **5.5** | Bốn transform phải deterministic: prompt compiler, Story Bible reduce, layout mapping, chapter parse. Nêu **mâu thuẫn nội tại §13 vs §16**: `Generation` hứa reproducibility nhưng LLM trong đường compile runtime phá vỡ nó — hai mục không thể cùng đúng. |
| **5.6** | Số của CogCanvas: ID-Sim 42.33 (2) → 27.21 (3) → 2.67 (4) → 0.52 (5); Attr-VQA sụp từ 3. Nêu rõ CogCanvas **chỉ test open-source**, frontier model chưa có benchmark độc lập ⇒ MVP0 phải tự đo. Đề xuất cách xử cảnh đông người: shot xa / silhouette / crop. |
| **6.1** | Con số 50-60% và lập luận cả 3 tương tác §14 nêu ra đều không cần canvas. Nêu các vấn đề kỹ thuật §14 sinh ra mà tài liệu chưa nhắc. Đề xuất đường thay thế đạt ~80% giá trị. |
| **6.3** | ⚠️ **Phải viết mục này như một sự tự thu hồi công khai.** Lens PM ban đầu khuyến nghị bỏ `parent_generation` ở MVP; `researcher` phát hiện Nghị định 134/2026/NĐ-CP (hiệu lực 09/04/2026) biến nó thành **hồ sơ pháp lý bắt buộc**. Khuyến nghị đó **sai và bị thu hồi**. Bổ sung: phải lưu cả human edit steps + quyết định chọn/loại, vì prompt một mình không chứng minh được "decisive contribution". Nêu rõ đây là lý do một trong bốn lens cần có web access. |
| **7** | Phân biệt **barrier to entry** vs **moat**. Bảng 5 thành phần × khó làm × khó copy × là moat. Ba moat thật (dữ liệu preference tích luỹ — miễn phí nhưng phải log từ MVP1; switching cost; style library). Nêu cả rủi ro ngược: chưa ai ghép hai nửa có thể vì thị trường tập trung ở đầu ngắn, không phải vì không ai làm được. |
| **8** | Ba lớp: bản quyền input (nhánh A/B/C theo OQ1), bản quyền output (Zarya — tin tốt), ToS provider. Cộng compliance: NĐ 134/2026 VN (record-keeping), Korea AI Basic Act (hiệu lực 22/01/2026, phạt 30 triệu won, áp cho mọi service coi HQ là market). Backlash có bằng chứng: Naver Webtoon bị boycott, BlueLine Studio phải vẽ lại *Knight King*. Kết luận: rủi ro **nhị phân**, phải kiểm trước khi viết code. |
| **9** | $400–1.600/100 chapter (regen 2x) — thấp hơn trực giác một bậc. Batch giảm 50%, fit job queue. Self-host thắng về đơn giá nhưng **mất đúng năng lực cốt lõi** ⇒ chỉ dùng cho LoRA/upscale, không mua GPU. **Kết luận đơn vị đo**: giờ-người, không phải đô-la — HITL 5 phút/chapter ≈ 8 giờ cho 100 chapter, với 1 người. |
| **10** | MVP0 phải có **spec cụ thể**: input gì, làm gì, tiêu chí pass/fail đo được, chi phí (~$12–50), thời lượng (1–2 tuần). Ghi rõ **ba lens độc lập cùng đề xuất** MVP0 — dùng một tên duy nhất "MVP0", không dùng 3 tên. Điều chỉnh: **không cắt MVP1** (rủi ro thấp, có CANVAS làm bằng chứng), chỉ chèn MVP0 trước. Bảng so sánh lộ trình gốc §18 vs đề xuất. Nâng ưu tiên export (thứ duy nhất trong MVP4 người dùng thật sự nhận được) + log preference từ MVP1. |
| **11** | 9 khoảng trống của `researcher` + OQ1–OQ3. Mục này **bắt buộc**, không được bỏ để tài liệu trông chắc chắn hơn thực tế. |
| **Tài liệu tham khảo** | Nhóm theo: Request gốc & run-state (markdown link relative), paper/benchmark, pháp lý, đối thủ & thị trường, pricing. Mọi URL lấy từ `findings/researcher.md`, **không tự thêm URL mới**. |

## Standard markdown link phải tạo (RULE-001 §Linking Rules — KHÔNG dùng wiki-link)

| Từ | Tới | Quan hệ |
|---|---|---|
| `Analysis-Comic-Studio-Concept.md` | `../999-Resources/Request.md` | `Phân tích:` — đối tượng được thẩm định |
| `Analysis-Comic-Studio-Concept.md` | `../010-Planning/pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio/` | `Run-state:` — dấu vết điều phối & findings đầy đủ |
| `Analysis-Comic-Studio-Concept.md` | `../999-Resources/Glossary.md` | `Thuật ngữ:` |
| `Analysis-Comic-Studio-Concept.md` | `../010-Planning/Risk-Register.md` | `Rủi ro chi tiết:` — **chỉ thêm nếu hạng mục 2 được duyệt ở gate** |
| `Risk-Register.md` *(nếu có)* | `../050-Research/Analysis-Comic-Studio-Concept.md` | `Nguồn:` |
| `Research-MOC.md` | `./Analysis-Comic-Studio-Concept.md` | mục lục |

## MOC cần cập nhật (PM làm ở close-step, không cấp cho worker)

| MOC | Mục thêm/sửa |
|---|---|
| `docs/050-Research/Research-MOC.md` | Thêm mục *Phân tích & Thẩm định* với link tới `Analysis-Comic-Studio-Concept.md` kèm một dòng mô tả |
| `docs/010-Planning/Planning-MOC.md` | Thêm link `Risk-Register.md` — **chỉ nếu hạng mục 2 được duyệt** |
| `docs/999-Resources/Glossary.md` | Bổ sung ~12 thuật ngữ (xem dưới) |

### Thuật ngữ đề xuất bổ sung vào Glossary

`Story Bible` · `Comic IR (Comic Intermediate Representation)` · `Panel Specification` · `Visual Prompt Compiler` · `Continuity Checker` · `Identity vs Appearance` · `Canonical Reference / Character Reference Sheet` · `Layout Score` · `syuzhet vs fabula` (thứ tự đọc vs thứ tự sự việc) · `attribute binding` · `typeset layer` · `text_safe_zone` · `HITL gate` · `vertical slice / MVP0`

> Glossary hiện chỉ có 3 thuật ngữ về OTP — di sản từ dự án khác, không liên quan comic-studio.
> Theo `pm-doc.md` Bước 6, việc Glossary im lặng **không** được coi là đã đạt tiêu chí Coherence.

---

# ĐIỀU CHỈNH SAU GATE — mô hình là SaaS thương mại, không phải công cụ cá nhân

> Anh đã chốt tại gate: **nền tảng cho người khác tự upload truyện của họ** + **sản phẩm thương mại / SaaS**, vẫn **1 dev**.
> Toàn bộ phase 2 chạy dưới giả định "công cụ cá nhân". Xem `escalations.md` **E1**.
> **Phần dưới ghi đè phần trên ở đúng những điểm được nêu; mọi điểm khác giữ nguyên.**

## Giả định thay thế

- ~~**A1** dự án cá nhân, 1 dev, công cụ cho chính mình~~ → **A1′**: **1 dev xây SaaS thương mại multi-tenant**, user tự upload truyện của họ.
- ~~**A3** chưa rõ nguồn truyện~~ → **A3′**: **đã rõ** — nhánh C (nền tảng, user tự upload). Rủi ro bản quyền sơ cấp chuyển sang user; nền tảng phát sinh nghĩa vụ riêng.
- ~~**A5** độc giả đích là anh, người ra quyết định build/không build~~ → **A5′ giữ nguyên** (vẫn là anh), nhưng bổ sung: tài liệu phải trả lời được cả câu *"bán được không"*, không chỉ *"build được không"*.

## Thay đổi cấu trúc tài liệu

### Thêm mục mới

**`## 9b. Unit economics — ràng buộc thiết kế trung tâm của mô hình SaaS`** (đặt ngay sau mục 9)

Đây là **mục mới, không có trong outline gốc**, và là phát hiện chỉ tồn tại vì đáp án gate. Nội dung bắt buộc, lấy từ `escalations.md` mục *Phân tích bổ sung của PM* + delta của `researcher`:

- Bảng chi phí biến đổi mỗi chapter × 3 hệ số regen × 2 model.
- Phép tính đối chiếu trần giá thị trường **$9–10/tháng** (Dashtoon, Anifusion) → kết luận **subscription phẳng không sống được**: 1 chapter/tháng ở regen 2x đã tiêu $8,04 trên $10 doanh thu, chưa trừ LLM Layer 1/2, storage, hạ tầng, phí thanh toán.
- Bốn đường ra, xếp theo mức khuyến nghị: (1) ⭐ credit-based — **ComicInk đã làm đúng thế này**, và nó là bằng chứng thị trường mạnh nhất có được; (2) bring-your-own-key; (3) phân tầng model theo tier — **đây là lần đầu abstraction §16 chứng minh giá trị kinh tế, không chỉ giá trị kỹ thuật**; (4) định giá cao hơn thị trường, nhắm tác giả chuyên nghiệp.
- Nêu rõ: **tỉ lệ regenerate là biến quyết định, và không có dữ liệu ngành nào** ⇒ MVP0 phải tự đo.

**`## 8b. Nghĩa vụ của nền tảng — rủi ro pháp lý ở mô hình user-upload`** (đặt trong mục 8, thành mục con)

- NĐ 134/2026 **Điều 37a** giới hạn TDM ở *"non-commercial purposes at the point of use"* — một nền tảng **thương mại** chạy extraction trên truyện có bản quyền của user có rơi vào giới hạn đó không? **Điều 37c**: *"royalty payment obligations may arise"*.
- Điều khoản buộc user cam kết (warrant) có quyền; cơ chế notice-and-takedown; safe harbour.
- ⚠️ Nếu delta của `researcher` trả về "không rõ" → **viết thẳng là không rõ và đây là câu cần luật sư.** Không suy đoán. Đây là rủi ro nhị phân.

### Sửa mục đã có

| Mục | Thay đổi |
|---|---|
| **1** Tóm tắt | Thêm một dòng verdict thứ tư: **"bán được không?"** — tách khỏi "khả thi không". Ba verdict cũ giữ nguyên. |
| **2** Phạm vi | Ghi rõ: 4 lens phase 2 chạy dưới A1 cũ; **4 kết luận bị ảnh hưởng** đã được xét lại bằng delta dispatch (dẫn `escalations.md` E1). Đây là tính minh bạch của phương pháp, không phải điểm yếu — phải nêu. |
| **6.1** Cắt canvas editor | ⚠️ **VIẾT LẠI HOÀN TOÀN, chờ delta của `architect`.** Lập luận "cắt 50-60% effort" rất mạnh cho công cụ cá nhân nhưng **yếu đi đáng kể** cho SaaS: editor *chính là sản phẩm*, và theo US Copyright Office thì *"iterative, interactive process rather than solely relying on prompts"* là cơ chế tạo ra phần **được bảo hộ bản quyền**. Cắt editor khỏi SaaS = cắt mất cả sản phẩm và cả lá chắn pháp lý. Tiêu đề mục có thể phải đổi từ *"nên cắt"* thành *"cắt bao nhiêu là đúng"*. |
| **6.2** Cắt microservices | Chờ delta `architect` xác nhận khuyến nghị monolith còn đúng. Bổ sung khái niệm **seam kinh tế** (tách để scale theo tải khách hàng) khác với seam kỹ thuật. |
| **6.3** `parent_generation` | Giữ nguyên (không cắt), **và mạnh lên**: với SaaS, audit trail còn là bằng chứng phục vụ *khách hàng của anh* chứng minh quyền của họ, không chỉ của anh. |
| **7** Moat | **Nâng cấp.** Moat "dữ liệu preference tích luỹ" chuyển từ *"đáng làm"* sang **lý do tồn tại của sản phẩm** — multi-tenant nghĩa là preference data từ nhiều tác giả. Khuyến nghị log từ MVP1 tăng lên mức bắt buộc. Giữ nguyên phản biện barrier ≠ moat và việc CANVAS đã public. |
| **10** Lộ trình | **MVP0 phải đo HAI thứ, không phải một**: (a) consistency có đủ tốt không — mục tiêu gốc; (b) **tỉ lệ regenerate thực tế** — vì đó là biến quyết định unit economics và không ai có dữ liệu. Bổ sung vào lộ trình: multi-tenancy (`tenant_id` trong schema từ ngày đầu — quyết định không sửa được rẻ về sau), hard quota **cưỡng chế trước khi gọi model** (không phải đếm sau), cost attribution per tenant. |
| **11** Không biết gì | Thêm: câu hỏi Điều 37a cho nền tảng thương mại (nếu `researcher` không tra ra); usage pattern thật của khách hàng AI creative tool; gross margin của AI image SaaS. |

### Nguồn sự thật bổ sung

| Nguồn | Dùng cho |
|---|---|
| `escalations.md` mục *Phân tích bổ sung của PM* | mục 9b — **toàn bộ phép tính unit economics đã có sẵn ở đó, writer dùng lại, không tự tính lại** |
| `findings/architect.md` mục `## Bổ sung sau GATE` | mục 6.1, 6.2, 10 |
| `findings/researcher.md` mục `## Bổ sung sau GATE` | mục 8b, 9b, 11 |

> **Ràng buộc cho writer**: hai mục `## Bổ sung sau GATE` **ghi đè** nội dung cũ ở đúng những điểm chúng nêu. Nội dung cũ **không bị xoá** vì nó là dấu vết quyết định — nhưng khi hai bên khác nhau, **bản sau gate thắng**. Writer phải đọc cả hai và viết theo bản sau.

---

# CẤU TRÚC CHỐT — sau cả hai delta. Đây là bản writer phải theo.

> Ba khối trước trong file này là dấu vết tiến hoá của plan. **Khối này thắng mọi khối trước.**

## Danh sách mục cuối cùng (16 mục)

```
# Phân tích & Thẩm định Ý tưởng comic-studio
## Mục lục
## 1. Tóm tắt cho người ra quyết định        ← 4 verdict: phù hợp / khả thi / bán được / đổi gì
## 2. Phạm vi & phương pháp                  ← gồm cả việc giả định đổi giữa run và cách xử lý
## 3. Ý tưởng có phù hợp hay chưa?
     3.1 Là thiết kế kỹ thuật: có
     3.2 Là sản phẩm: chưa được định nghĩa — và đó là phát hiện
     3.3 Bốn thứ làm ĐÚNG, đừng đổi
## 4. Có khả thi hay không?
     4.1 Verdict: khả thi có điều kiện — BẢY điều kiện
     4.2 Bảng khả thi từng thành phần (12 dòng, có nguồn)
     4.3 Kiến trúc này ĐÃ được validate bằng số — CANVAS
     4.4 Boss cuối thật không phải cái tài liệu nghĩ
## 5. Bảy vấn đề phải sửa TRƯỚC khi viết code
     5.1 (chapter, scene) làm khóa thời gian — sai âm thầm ở flashback
     5.2 Continuity Checker: từ "flag lỗi + autofix" sang "chọn giữa N ứng viên"
     5.3 Layout Score: bỏ số thực, dùng rubric rời rạc
     5.4 Chữ & speech bubble — mục bị bỏ sót hoàn toàn
     5.5 Ranh giới LLM / deterministic code chưa được vẽ
     5.6 ≤3 nhân vật/panel — ràng buộc cứng
     5.7 [MỚI] Multi-tenancy — 15-25% effort mà tài liệu không nhắc một dòng
## 6. Ba thứ nên CẮT (và một thứ KHÔNG được cắt)
     6.1 Canvas editor §14 — cắt một phần: editor tối thiểu ~20-25%
     6.2 Microservices + Vector DB §12 — cắt, và lý do MẠNH LÊN dưới SaaS
     6.3 Layout Score số thực — cắt (trỏ về 5.3)
     6.4 parent_generation — KHÔNG cắt. PM tự thu hồi khuyến nghị của mình
## 7. Phản biện luận điểm "moat"
## 8. Rủi ro pháp lý & compliance
     8.1 Ba lớp, và nửa nào có đường đi / nửa nào chặn ở cửa luật sư
     8.2 Zarya of the Dawn — tin tốt bị đọc sai
     8.3 [MỚI] Safe harbour Điều 198b — checklist build được
     8.4 [MỚI] Luật TTNT 2025 — nghĩa vụ nội địa VN, deadline ~01/03/2027
     8.5 Ba câu phải hỏi luật sư
## 9. Chi phí thật — và đơn vị đo đúng
## 9b. [MỚI] Unit economics — ràng buộc thiết kế trung tâm của mô hình SaaS
     9b.1 Hệ số đúng là N=3, không phải 2x — và vì sao
     9b.2 Bảng chi phí và margin
     9b.3 Xung đột M13: tính năng cốt lõi vs margin
     9b.4 Bốn đường ra, BYOK ở vị trí số 1
## 10. Lộ trình đề xuất: MVP0 đi trước
## 11. Những gì bản phân tích này KHÔNG biết
## 12. Kết luận
## Tài liệu tham khảo
```

## Nguồn sự thật — bản chốt, SÁU file

| Nguồn | Ưu tiên |
|---|---|
| `docs/999-Resources/Request.md` | tham chiếu §n |
| `findings/architect.md` — gồm cả `## Bổ sung sau GATE` (B1–B4) | phần sau gate **thắng** phần trước |
| `findings/senior-ai-engineer.md` | không có delta, dùng nguyên |
| `findings/researcher.md` | báo cáo gốc §1–§8 |
| `findings/researcher-delta.md` | **thắng** `researcher.md` ở mọi điểm nó nêu |
| `findings/product-manager-pm-lens.md` | lens PM |
| `escalations.md` E1 + E2 | **E2 sửa E1** — phép tính đúng là 3x |

## Ràng buộc bổ sung cho các mục MỚI

| Mục | Ràng buộc |
|---|---|
| **1** | Verdict thứ ba **"bán được không?"** phải nói rõ: khả thi kỹ thuật ≠ khả thi thương mại, và ở mô hình SaaS thì cái thứ hai mới là cái chặn. |
| **2** | **Bắt buộc nêu**: 4 lens chạy dưới giả định "công cụ cá nhân"; gate đổi thành SaaS thương mại; 2 lens được resume để xét lại 4 kết luận bị ảnh hưởng. Đây là tính minh bạch phương pháp — nêu ngắn, đừng biện hộ. |
| **4.1** | **BẢY** điều kiện, không phải bốn. Lấy danh sách 7 từ cuối `researcher-delta.md`. ➕ **Sửa sau verify:** phải nói rõ **tổng là CHÍN** — bảy của `researcher` + hai của lens kỹ thuật, cùng mức bắt buộc. §1 và §4.1 phải khớp số. |
| **5.4b** | ➕ **THIẾU Ở BẢN ĐẦU — thêm sau verify.** Gán thoại cho speaker là **một trong HAI** human gate bắt buộc ở MVP2 (chỗ còn lại là dialogue condensation ở §5.4). Bắt buộc nêu: bảng tỉ lệ lỗi 30-50% (3+ người có tự sự chen) và 40-60% (câu ngắn/thán từ), đánh dấu rõ là **ước lượng của `senior-ai-engineer`, không phải số đo**; bốn tầng (anchor regex trước → LLM constrained decoding theo danh sách nhân vật có mặt, cho phép `UNKNOWN` → kiểm chéo prior luân phiên + appellation qua `Relationships` → `speaker_confidence` + cờ UI). Lý do nó bắt buộc: chi phí lỗi **bất đối xứng** — một dòng gán sai làm hỏng cả trang trong mắt người đọc. Nguồn: `findings/senior-ai-engineer.md` §3 (dòng ~290-303). |
| **5.7** | Multi-tenancy 15-25% effort (8-12% nếu mua auth+billing). Sáu quyết định không đảo được rẻ, đứng đầu: `tenant_id NOT NULL` là **cột đầu tiên** mọi composite index + Postgres RLS. Nêu lập luận của `architect`: với 1 dev không có code review, RLS là bảo hiểm rẻ nhất tồn tại. Và điểm tinh tế: content-address **trong** phạm vi tenant, **không** dedup chéo tenant — vì dedup chéo mâu thuẫn với lập luận quyền tác giả. |
| **6.1** | ⚠️ **Trình bày như một cuộc tranh luận có kết luận, không phải một khuyến nghị đơn.** PM phản biện: editor là sản phẩm + là cơ chế tạo phần được bảo hộ. `architect` phản biện lại: **đúng về nghĩa vụ, sai về phương tiện** — "iterative, interactive process" là yêu cầu về **quyết định con người được ghi vết**, không phải về công nghệ render UI; form editor có `change_log` đầy đủ cũng thoả. Nghĩa vụ nằm ở **tầng dữ liệu** (`origin`, `field_provenance`, `change_log`, `parent_generation`). ⇒ Phản biện của PM, truy tới cùng, **củng cố** việc cắt. Kết luận: **cắt một phần**, editor tối thiểu ~20-25% (mẫu số SaaS) vs §14 đầy đủ 50-60% (mẫu số công cụ cá nhân) — **nêu rõ hai mẫu số khác nhau, không so trực tiếp**. Nhượng bộ: phải có **bubble/text overlay trong phạm vi một panel**. |
| **6.2** | Lý do mới, mạnh hơn lý do cũ: state resolution là truy vấn xuyên Story↔Comic; tách 2 DB thành join phía app, mà **RLS không bảo vệ được join phía app** ⇒ mất lớp phòng thủ ở đường dẫn nóng nhất. Cộng: audit record và artifact nó chứng minh phải commit **cùng transaction** — *bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng*. Nêu **seam kinh tế** (worker process riêng cùng codebase, fairness per-tenant trong câu claim job, `usage_event` append-only) khác seam kỹ thuật. |
| **8.3** | Checklist **SÁU** điểm của Điều 198b (bản đầu ghi 5 — thiếu item 6). ➕ **Item 6 thêm sau verify: kiểm opt-out signal Điều 37b của file upload trước khi xử lý** — metadata / biện pháp bảo vệ công nghệ / rights-management-info dạng máy đọc / thông báo từ tổ chức quản lý tập thể; log kết quả kèm timestamp; chặn nếu có signal bảo lưu. **Chi phí ~0, xoá được một nhánh rủi ro** (nguồn: `researcher-delta.md` §1.3). Phải nêu lập luận điều kiện (nếu 37a không áp thì 37b cũng không — nhưng nếu áp thì không có bước kiểm là vi phạm đã xảy ra hàng nghìn lần, không sửa hồi tố được) **và** phải nói rõ nó **không** xung đột với nghịch lý safe harbour: đọc nhãn tường minh do chủ quyền gắn vào file ≠ tự suy đoán về quyền của người khác. **Bắt buộc nêu nghịch lý safe harbour**: điều kiện miễn trừ là *"không biết"*, nên xây bộ phát hiện truyện có bản quyền có thể **phá** chính miễn trừ của mình. Đây là điểm phản trực giác nhất của run — một dev sẽ làm ngược vì "chủ động kiểm tra" nghe như có trách nhiệm. |
| **8.4** | Luật TTNT 2025 (Luật 134/2025/QH15), hiệu lực 01/03/2026, deadline tuân thủ **~01/03/2027**. Nghĩa vụ: minh bạch (Điều 11), đánh dấu định dạng máy đọc, đăng ký/báo cáo (Điều 8). ⚠️ Nêu rõ **sự bất định về phạm vi**: khoản 4 Điều 11 nói *"mô phỏng người thật hoặc sự kiện thực tế"* nhưng câu sau không giới hạn thế — hai nguồn mô tả khác nhau và **không đọc được nguyên văn**. Tin thực dụng: Nano Banana Pro đã nhúng SynthID. |
| **8.5** | Đúng ba câu, đã narrow tới mức luật sư trả lời được. Lấy nguyên từ `researcher-delta.md` §1.2. |
| **9b.1** | Giải thích **bản chất** N=3, không chỉ con số: đây là **best-of-N mặc định mọi panel**, không phải retry-on-failure. Đó là setting để đạt 4.91/5 ⇒ không được lấy chất lượng của N=3 mà tính chi phí của N=2. **Và nêu rằng PM đã tính sai 50% ở lần đầu, đã tự sửa** (dẫn `escalations.md` E2) — sự minh bạch này làm tăng độ tin cậy của các con số còn lại, không giảm. |
| **9b.3** | ⭐ **Mục sắc nhất của phần kinh tế.** Xung đột M13: `researcher` chứng minh 1 ảnh/panel = margin **−141%**, 1 ảnh/trang = **+40%**; nhưng §14 xây toàn bộ trải nghiệm quanh **regenerate một panel độc lập**. ⇒ **Tính năng làm sản phẩm hay chính là tính năng làm margin âm.** Ba đường ra: BYOK (xung đột **biến mất**), whole-page mặc định + per-panel là hành động trả phí, whole-page thuần (không khuyến nghị — bỏ mất lý do sản phẩm tồn tại). **Và nêu hệ quả tích cực**: `Panel Specification` §6 vẫn giữ nguyên giá trị vì một page compile được nhiều panel spec thành **một** prompt whole-page — đây là **lần thứ hai** quyết định "spec là dữ liệu chính" tự chứng minh giá trị (lần đầu: ranh giới bản quyền Zarya). |
| **9b.4** | BYOK ở vị trí 1 với **ba căn cứ độc lập**: (a) 23% GRR ở AI budget-tier ⇒ subscription là mô hình sai với 1 dev không budget marketing; (b) power user ở −262% không chặn được bằng pricing phẳng; (c) xung đột M13 biến mất. Nêu **điểm yếu thẳng thắn**: friction cao với non-technical user — đúng phân khúc mục tiêu ⇒ onboarding flow là rủi ro sản phẩm số 1. Margin kỳ vọng **50–60%** (ICONIQ 52%, Bessemer 50-60%), không phải 80%. |
| **10** | MVP0 đo **HAI** chỉ số: (a) consistency đủ tốt không; (b) **N tối thiểu** để VLM-select ra panel đạt (mỗi bậc N giảm ~33% COGS) và **human-reject rate sau VLM-select** — chưa ai công bố. Chi phí ~$12. Thêm vào lộ trình: `tenant_id` từ ngày đầu, hard quota **cưỡng chế trước khi enqueue** (hold reserve **3 credit/panel**, không 1 — vì N=3), checklist Điều 198b, log preference data. ➕ **Thêm sau verify:** MVP1 phải có **bước kiểm opt-out Điều 37b ngay trong ingest** (đây là nơi file user lần đầu vào hệ thống); MVP2 phải có **hai human gate tường minh** — speaker attribution (§5.4b) + dialogue condensation (§5.4). Và nêu rõ chi phí MVP0: ~$12 ở **giá standard $0.134**, ~$6 nếu batch — lấy số cao làm trần an toàn, đừng lập ngân sách theo số thấp. |
| **11** | Gộp 9 khoảng trống của `researcher.md` + 10 của `researcher-delta.md`, bỏ trùng. **Bắt buộc nêu Comicpad đóng cửa 01/09/2026** như dữ liệu ủng hộ nhánh phản biện. |

---

# BÀI HỌC GỐC — vì sao hai khuyến nghị bị rơi

Ghi ở đây, không ghi ở `verdict.md`, vì chỗ hỏng là **file này**.

`context-auditor` tìm ra hai khuyến nghị **có trong findings mà không có trong deliverable**: Điều 37b opt-out check (`researcher-delta.md` §1.3) và speaker attribution (`senior-ai-engineer.md` §3). Nó quy trách chính xác:

> *"cả (1) và (2) **không** có trong bảng ràng buộc của block `CẤU TRÚC CHỐT`. Writer tuân thủ contract đúng; chỗ rơi nằm ở **bước lập outline**, không phải ở writer."*

**Cơ chế lỗi.** PM lập bảng *Ràng buộc bổ sung* bằng cách đi qua findings và trích những điểm **sắc nhất** — điểm gây tranh luận, điểm đảo kết luận, điểm có con số gây sốc. Cả hai khuyến nghị bị rơi đều **không sắc**: 37b là một dòng "chi phí ~0, rẻ để phòng ngừa" nằm trong một tiểu mục có tiêu đề *"ảnh hưởng gián tiếp"*; speaker attribution là một mục kỹ thuật không mâu thuẫn với lens nào nên không bao giờ được PM phân xử. **Bộ lọc "sắc" không phải bộ lọc "quan trọng".** Một khuyến nghị rẻ và không gây tranh cãi là loại dễ rơi nhất, và cũng chính là loại đáng làm nhất — chi phí ~0.

**Sửa quy trình cho lần sau.** Khi lập `outline.md` cho lane doc, sau khi trích các điểm sắc thì chạy thêm **một lượt quét cơ học**: đi qua từng heading của từng file findings và đánh dấu heading nào **chưa** xuất hiện trong bảng ràng buộc. Heading không có mặt là ứng viên bị rơi — phải kết luận tường minh *"đưa vào mục X"* hoặc *"cố ý bỏ, lý do…"*, không được để trạng thái im lặng. Với run này, hai heading đó là `#### 1.3` của `researcher-delta.md` và mục speaker của `senior-ai-engineer.md`.

**Điểm cần nói thẳng:** bốn tiêu chí của Bước 6 (`pm-doc.md`) **không** bắt được lỗi này một cách hiển nhiên — *Correctness* được định nghĩa là "nội dung khớp Nguồn sự thật, không có khẳng định không có căn cứ", tức là bắt **thừa**, không bắt **thiếu**. `context-auditor` bắt được vì nó tự chủ động grep findings tìm khuyến nghị không xuất hiện trong doc. Đó là hành vi nên được viết thành yêu cầu tường minh trong dispatch prompt của mọi lần verify sau: *"liệt kê khuyến nghị có trong findings mà KHÔNG có trong deliverable"*.
