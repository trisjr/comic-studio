---
id: RESEARCH-001
type: research
status: draft
project: comic-studio
owner: "@trisjr"
tags: [comic-studio, feasibility, architecture-review, ai-pipeline, saas]
created: 2026-08-23
updated: 2026-08-23
---

# Phân tích & Thẩm định Ý tưởng comic-studio

Tài liệu này thẩm định `Request.md` — 894 dòng, 18 mục, mô tả concept comic-studio (novel/truyện chữ → comic pages) — và trả lời bốn câu: ý tưởng có **phù hợp** chưa, có **khả thi** không, có **bán được** không, và cần **đổi** gì.

Ngày thực hiện: **23/08/2026**. Phương pháp: **bốn lens độc lập** (`architect`, `senior-ai-engineer`, `researcher`, và lens product do PM tự làm) + **một vòng delta** sau khi anh chốt tại gate rằng mô hình là **SaaS thương mại multi-tenant, 1 dev**.

Mọi con số trong tài liệu này truy được về findings; dữ liệu web kèm URL gốc.

- **Phân tích:** [Request.md](../999-Resources/Request.md)
- **Run-state:** [pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio](../010-Planning/pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio/)
- **Thuật ngữ:** [Glossary](../999-Resources/Glossary.md)

## Mục lục

- [1. Tóm tắt cho người ra quyết định](#1-tóm-tắt-cho-người-ra-quyết-định)
- [2. Phạm vi & phương pháp](#2-phạm-vi--phương-pháp)
- [3. Ý tưởng có phù hợp hay chưa?](#3-ý-tưởng-có-phù-hợp-hay-chưa)
  - [3.1 Là thiết kế kỹ thuật: có](#31-là-thiết-kế-kỹ-thuật-có)
  - [3.2 Là sản phẩm: chưa được định nghĩa — và đó là phát hiện](#32-là-sản-phẩm-chưa-được-định-nghĩa--và-đó-là-phát-hiện)
  - [3.3 Bốn thứ làm ĐÚNG, đừng đổi](#33-bốn-thứ-làm-đúng-đừng-đổi)
- [4. Có khả thi hay không?](#4-có-khả-thi-hay-không)
  - [4.1 Verdict: khả thi có điều kiện — BẢY điều kiện](#41-verdict-khả-thi-có-điều-kiện--bảy-điều-kiện)
  - [4.2 Bảng khả thi từng thành phần](#42-bảng-khả-thi-từng-thành-phần)
  - [4.3 Kiến trúc này ĐÃ được validate bằng số — CANVAS](#43-kiến-trúc-này-đã-được-validate-bằng-số--canvas)
  - [4.4 Boss cuối thật không phải cái tài liệu nghĩ](#44-boss-cuối-thật-không-phải-cái-tài-liệu-nghĩ)
- [5. Bảy vấn đề phải sửa TRƯỚC khi viết code](#5-bảy-vấn-đề-phải-sửa-trước-khi-viết-code)
  - [5.1 `(chapter, scene)` làm khóa thời gian — sai âm thầm ở flashback](#51-chapter-scene-làm-khóa-thời-gian--sai-âm-thầm-ở-flashback)
  - [5.2 Continuity Checker: từ "flag lỗi + autofix" sang "chọn giữa N ứng viên"](#52-continuity-checker-từ-flag-lỗi--autofix-sang-chọn-giữa-n-ứng-viên)
  - [5.3 Layout Score: bỏ số thực, dùng rubric rời rạc](#53-layout-score-bỏ-số-thực-dùng-rubric-rời-rạc)
  - [5.4 Chữ & speech bubble — mục bị bỏ sót hoàn toàn](#54-chữ--speech-bubble--mục-bị-bỏ-sót-hoàn-toàn)
    - [5.4b Gán thoại cho speaker — human gate bắt buộc thứ hai](#54b-gán-thoại-cho-speaker--human-gate-bắt-buộc-thứ-hai)
  - [5.5 Ranh giới LLM / deterministic code chưa được vẽ](#55-ranh-giới-llm--deterministic-code-chưa-được-vẽ)
  - [5.6 ≤3 nhân vật/panel — ràng buộc cứng](#56-3-nhân-vậtpanel--ràng-buộc-cứng)
  - [5.7 Multi-tenancy — 15-25% effort mà tài liệu không nhắc một dòng](#57-multi-tenancy--15-25-effort-mà-tài-liệu-không-nhắc-một-dòng)
- [6. Ba thứ nên CẮT (và một thứ KHÔNG được cắt)](#6-ba-thứ-nên-cắt-và-một-thứ-không-được-cắt)
  - [6.1 Canvas editor §14 — cắt một phần: editor tối thiểu ~20-25%](#61-canvas-editor-14--cắt-một-phần-editor-tối-thiểu-20-25)
  - [6.2 Microservices + Vector DB §12 — cắt, và lý do MẠNH LÊN dưới SaaS](#62-microservices--vector-db-12--cắt-và-lý-do-mạnh-lên-dưới-saas)
  - [6.3 Layout Score số thực — cắt](#63-layout-score-số-thực--cắt)
  - [6.4 `parent_generation` — KHÔNG cắt. PM tự thu hồi khuyến nghị của mình](#64-parent_generation--không-cắt-pm-tự-thu-hồi-khuyến-nghị-của-mình)
- [7. Phản biện luận điểm "moat"](#7-phản-biện-luận-điểm-moat)
- [8. Rủi ro pháp lý & compliance](#8-rủi-ro-pháp-lý--compliance)
  - [8.1 Ba lớp, và nửa nào có đường đi / nửa nào chặn ở cửa luật sư](#81-ba-lớp-và-nửa-nào-có-đường-đi--nửa-nào-chặn-ở-cửa-luật-sư)
  - [8.2 Zarya of the Dawn — tin tốt bị đọc sai](#82-zarya-of-the-dawn--tin-tốt-bị-đọc-sai)
  - [8.3 Safe harbour Điều 198b — checklist build được](#83-safe-harbour-điều-198b--checklist-build-được)
  - [8.4 Luật TTNT 2025 — nghĩa vụ nội địa VN, deadline ~01/03/2027](#84-luật-ttnt-2025--nghĩa-vụ-nội-địa-vn-deadline-01032027)
  - [8.5 Ba câu phải hỏi luật sư](#85-ba-câu-phải-hỏi-luật-sư)
- [9. Chi phí thật — và đơn vị đo đúng](#9-chi-phí-thật--và-đơn-vị-đo-đúng)
- [9b. Unit economics — ràng buộc thiết kế trung tâm của mô hình SaaS](#9b-unit-economics--ràng-buộc-thiết-kế-trung-tâm-của-mô-hình-saas)
  - [9b.1 Hệ số đúng là N=3, không phải 2x — và vì sao](#9b1-hệ-số-đúng-là-n3-không-phải-2x--và-vì-sao)
  - [9b.2 Bảng chi phí và margin](#9b2-bảng-chi-phí-và-margin)
  - [9b.3 Xung đột M13: tính năng cốt lõi vs margin](#9b3-xung-đột-m13-tính-năng-cốt-lõi-vs-margin)
  - [9b.4 Bốn đường ra, BYOK ở vị trí số 1](#9b4-bốn-đường-ra-byok-ở-vị-trí-số-1)
- [10. Lộ trình đề xuất: MVP0 đi trước](#10-lộ-trình-đề-xuất-mvp0-đi-trước)
  - [MVP0 — spec cụ thể](#mvp0--spec-cụ-thể)
  - [Bảng so sánh lộ trình](#bảng-so-sánh-lộ-trình)
- [11. Những gì bản phân tích này KHÔNG biết](#11-những-gì-bản-phân-tích-này-không-biết)
  - [Khoảng trống dữ liệu về công nghệ](#khoảng-trống-dữ-liệu-về-công-nghệ)
  - [Khoảng trống pháp lý — quan trọng nhất](#khoảng-trống-pháp-lý--quan-trọng-nhất)
  - [Khoảng trống thị trường](#khoảng-trống-thị-trường)
  - [Câu hỏi còn mở cần anh trả lời](#câu-hỏi-còn-mở-cần-anh-trả-lời)
- [12. Kết luận](#12-kết-luận)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo) — chỉ liệt kê tới cấp mục; bên trong chia theo 7 nhóm nguồn

> Thứ tự mục trong thân tài liệu: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → **9b** → 10 → 11 → 12 → Tài liệu tham khảo.

---

## 1. Tóm tắt cho người ra quyết định

**Bốn verdict, bốn câu độc lập:**

1. **Phù hợp hay chưa?** — Với tư cách **thiết kế kỹ thuật**: **có**, và ở mức trên trung bình đáng kể; với tư cách **sản phẩm**: **chưa xác định được**, vì `Request.md` là một thiết kế kiến trúc cho một sản phẩm chưa được định nghĩa (chưa có người dùng, chưa có vấn đề, chưa có tiêu chí thành công đo được).
2. **Khả thi hay không?** — **Khả thi có điều kiện**: kiến trúc này đã được một paper công khai implement và **đo bằng số** (CANVAS, character 4.91/5, human win-rate 86,7%), nhưng chỉ khả thi khi thoả **bảy** điều kiện của `researcher` **cộng hai** điều kiện từ hai lens kỹ thuật — **chín** điều kiện, tất cả cùng mức bắt buộc, tất cả đồng thời (§4.1).
3. **Bán được không?** — **Chưa, ở dạng đang thiết kế**: khả thi kỹ thuật **không** đồng nghĩa khả thi thương mại, và ở mô hình SaaS thì cái thứ hai mới là cái chặn — subscription phẳng $10/tháng không sống được ở hệ số N=3 ($12,06 COGS/chapter trên $9,99 doanh thu), và tính năng làm sản phẩm hay (regenerate từng panel) chính là tính năng làm margin âm.
4. **Cần đổi gì?** — **Bảy** vấn đề phải sửa trước dòng code đầu tiên (§5), **ba** hạng mục nên cắt hoặc cắt một phần (§6.1–6.3), và **một** hạng mục tuyệt đối không được cắt vì nó là hồ sơ pháp lý bắt buộc (§6.4).

**Bốn lens — verdict và phát hiện quan trọng nhất của từng lens:**

| Lens | Verdict của chính lens đó | Phát hiện quan trọng nhất |
|---|---|---|
| `architect` (kiến trúc & data model) | **"PHÙ HỢP CÓ ĐIỀU KIỆN"** — 3 điều kiện: thu §12 về modular monolith, đảo thứ tự §18 + MVP0, cắt canvas §14 | **`(chapter, scene)` làm khóa thời gian là lỗi data model gây sai dữ liệu ÂM THẦM.** Nó trộn thứ tự đọc với thứ tự sự việc → mọi cảnh flashback resolve sai state, và Continuity Checker sẽ "sửa" đúng những panel đang đúng. Lỗi không crash ⇒ phát hiện muộn và rất đắt. |
| `senior-ai-engineer` (AI/ML pipeline) | **"Khả thi có điều kiện"** — 5 điều kiện, trong đó: deterministic hoá 4 transform, HITL gate ở MVP1, eval kit cùng MVP1, bỏ Layout Score số thực + thu hẹp checker | **Nghịch lý moat**: thành phần tài liệu tự tuyên bố là moat (Continuity Checker) lại là thành phần **ít được kiểm chứng nhất**; check được nhấn mạnh nhất (`✓ face`) là check kém khả thi nhất trên art cách điệu, và panel nhiều nhân vật cần **re-identification** — chính bài toán checker được lập ra để giải. |
| `researcher` (công nghệ, thị trường, pháp lý) | **"✅ KHẢ THI CÓ ĐIỀU KIỆN"** — 4 điều kiện ở báo cáo gốc, **nâng lên 7** sau delta | **Kiến trúc của anh ĐÚNG nhưng KHÔNG MỚI**: CANVAS (arXiv 2604.13452, 15/04/2026) đã public gần đúng từng thành phần và đo được — tốt (không phải đánh cược) và xấu (concept đã công khai ⇒ không phải moat). Kèm đảo chiều: NĐ 134/2026 biến `Generation`/`parent_generation` thành hồ sơ pháp lý bắt buộc. |
| Lens product (PM tự làm) | **Thiết kế kỹ thuật: có. Sản phẩm: chưa xác định được** | `Request.md` **không phải một ý tưởng sản phẩm** mà là một **thiết kế kiến trúc cho một sản phẩm chưa được định nghĩa**: 18 mục, 894 dòng có pipeline 6 tầng và data model 13 entity, nhưng không có ai là người dùng, vấn đề gì đang được giải, và "đủ tốt" nghĩa là gì. |

**Nếu chỉ đọc một mục — 5 việc làm ngay, theo thứ tự:**

1. **Mang ba câu hỏi ở §8.5 tới một luật sư SHTT Việt Nam, trước khi thương mại hoá.** Đây là rủi ro **nhị phân** duy nhất còn lại: trả lời sai không làm sản phẩm chậm, mà làm nó **bất hợp pháp**. Chi phí một buổi tư vấn thấp hơn nhiều chi phí build sai.
2. **Chạy MVP0 (~$12, 1–2 tuần)** để tự đo **ba** chỉ số không ai công bố: consistency có đủ tốt không, **N tối thiểu** để VLM-select ra panel đạt, và **human-reject rate sau VLM-select**. Ba lens độc lập cùng đề xuất việc này.
3. **Sửa khóa thời gian trước dòng code đầu tiên**: hai trục `reading_order` / `story_order` + `timeline_id`, state neo vào `Event`, mọi truy vấn state đi qua **một** `resolveState()` (§5.1). Đây là schema **và** là giả định lan khắp mọi module — sửa sau đồng nghĩa migrate dữ liệu và rà lại toàn bộ query.
4. **Chốt mô hình giá là metered/BYOK, không phải subscription phẳng** (§9b.4). Ba căn cứ độc lập cùng chỉ về đây, và quyết định này quy định luôn kiến trúc (credit ledger + hold trước khi gọi model).
5. **Chốt danh sách "phải có trong schema từ ngày đầu"**: `tenant_id NOT NULL` là cột đầu tiên mọi composite index + RLS, `change_log` ghi **mọi** hành động người dùng (kể cả "chọn generation X"), và log preference data từ MVP1. Cả ba đều rẻ bây giờ và rất đắt về sau.

---

## 2. Phạm vi & phương pháp

**Đối tượng:** `Request.md`, 894 dòng, 18 mục. Toàn bộ nội dung được đọc nguyên văn bởi cả bốn lens. Tài liệu này tham chiếu `§n` của `Request.md` mà không trích lại toàn văn.

**Bốn lens — cái gì được verify bằng web, cái gì là lập luận, cái gì là ước lượng:**

| Lens | Có web access? | Bản chất của kết luận |
|---|---|---|
| `researcher` | **Có** — 53 tool call, ~50 lần WebSearch/WebFetch (+26/30 call ở vòng delta) | **Dữ liệu đã verify**: giá API official, benchmark có DOI/arXiv, văn bản pháp lý, pricing đối thủ. Mọi con số định lượng trong tài liệu này có URL đều đến từ lens này. Chỗ không tra ra được ghi rõ là khoảng trống. |
| `architect` | Không | **Lập luận kiến trúc thuần** trên schema/DDL/pattern. Ba giả định công nghệ được đánh dấu tường minh `GĐ-1/2/3` để đối chiếu chéo. Ước lượng effort (§14 = 50-60%) được lens tự ghi rõ là **ước lượng, không phải benchmark**. |
| `senior-ai-engineer` | **Không** (ghi rõ trong findings) | **Ước lượng engineering** kèm giả định. Bảy giả định về năng lực image model được gom thành `IM-A1`…`IM-A7` để PM đối chiếu chéo — phần lớn sau đó được `researcher` trả lời bằng số. |
| Lens product | — (PM main loop) | Phán đoán product/scope/moat, và **các phân xử** giữa các lens. |

**Giả định vận hành và hệ quả nếu sai** (nguồn: `brief.md` §Assumptions):

| # | Giả định | Sai thì hỏng ở đâu |
|---|---|---|
| A1 | Dự án cá nhân, 1 dev + AI assist, ngân sách tự bỏ | Nếu có team + funding thì phần cắt scope quá bảo thủ và verdict khả thi bị đánh giá thấp hơn thực tế |
| A2 | Chưa có dòng code nào | Nếu đã có prototype, phân tích bỏ sót ràng buộc từ code thật (đã verify bằng `find`, rủi ro thấp) |
| A3 | Nguồn truyện chưa xác định là IP tự sở hữu hay của tác giả khác | Biến làm đổi verdict **mạnh nhất** — mạnh hơn cả ngân sách |
| A4 | Deliverable viết Tiếng Việt, giữ technical term | — |
| A5 | Độc giả đích là chính anh, người ra quyết định build / không build | Nếu để pitch cho người khác thì cần thêm market sizing và business model mà run này không làm |

**Giả định đã đổi giữa run — nêu để minh bạch phương pháp:**

Cả bốn lens của phase fan-out chạy dưới giả định **A1 = "công cụ cá nhân"**. Tại gate, anh chốt: **nền tảng cho người khác tự upload truyện của họ** + **sản phẩm thương mại / SaaS**, vẫn **1 dev**. Ba giả định bị thay: **A1′** = 1 dev xây SaaS thương mại multi-tenant; **A3′** = đã rõ, nhánh nền tảng user-upload (rủi ro bản quyền sơ cấp chuyển sang user, nền tảng phát sinh nghĩa vụ riêng); **A5′** giữ nguyên độc giả nhưng bổ sung yêu cầu trả lời cả câu *"bán được không"*.

Tổ hợp mới đảo chiều hoặc làm yếu **bốn** kết luận đã chốt (chi tiết ở `escalations.md` **E1**). PM **không** chạy lại phase fan-out — phần kỹ thuật thuần (data model, pipeline AI, năng lực image model) bất biến với mô hình kinh doanh — mà **resume hai lens** (`architect`, `researcher`) bằng đúng các câu hỏi delta. Mọi chỗ trong tài liệu này mà bản sau gate khác bản trước, **bản sau gate thắng**. Thêm nữa, `escalations.md` **E2** ghi lại việc PM tự phát hiện và sửa một phép tính của chính mình: hệ số chi phí đúng là **N=3**, không phải 2x — chênh **+50%**.

**Giới hạn của chính bản phân tích này:**

- Không lens nào **chạy thử** bất cứ thứ gì. Không có ảnh nào được generate, không có chapter nào được extract. Toàn bộ là thẩm định trên giấy — đó chính là lý do khuyến nghị số 2 ở §1 là chạy MVP0.
- Hai lens (`architect`, `senior-ai-engineer`) không có web access; mọi con số của họ là ước lượng engineering, không phải benchmark.
- Phần pháp lý là **tổng hợp nguồn công khai**, không phải ý kiến pháp lý. Hai văn bản trọng yếu không đọc được nguyên văn (§8.5, §11).
- Những gì bản phân tích này **không biết** được liệt kê đầy đủ ở §11, và mục đó là bắt buộc — không bỏ để tài liệu trông chắc chắn hơn thực tế.

---

## 3. Ý tưởng có phù hợp hay chưa?

### 3.1 Là thiết kế kỹ thuật: có

**Verdict: phù hợp, và ở mức trên trung bình rõ rệt so với cách tiếp cận thông thường.**

Ba lens kỹ thuật hội tụ về cùng một nhận định, mỗi lens một đường lập luận:

- `architect`: tầm nhìn kiến trúc (spec-as-source, tách 3 layer, intermediate representation) là đúng và ở mức trên trung bình rõ rệt — tác giả đã nhìn ra đúng chỗ khó (consistency và state theo timeline) chứ không bị hút vào phần dễ (gọi image model).
- `senior-ai-engineer`: nguyên tắc *"đừng để AI đọc chapter rồi generate ảnh ngay"* (§1) là **đúng**, và IR như một data model bền vững người sửa được là **quyết định kiến trúc tốt nhất của cả tài liệu**.
- `researcher`: kiến trúc này **không phải science fiction** — nó là kiến trúc đã được CANVAS implement và đo lường thành công (§4.3).

Điểm cần nói rõ: cái làm nó "trên trung bình" không phải độ phức tạp mà là **thứ tự ưu tiên**. Tài liệu nhận ra rằng thứ đắt và không tái tạo được là **hiểu truyện** (quan hệ nhân vật, timeline, ý nghĩa cảnh), còn một lần gọi image model là **rẻ và thay thế được** — và thiết kế theo đúng thứ tự đó. Đa số dự án cùng loại bỏ qua điều này rồi trả giá về sau.

### 3.2 Là sản phẩm: chưa được định nghĩa — và đó là phát hiện

Sự tách bạch giữa 3.1 và 3.2 **không được gộp thành một verdict mờ**. `Request.md` **không** phải một ý tưởng sản phẩm; nó là một **thiết kế kiến trúc cho một sản phẩm chưa được định nghĩa**. Đây là quan sát định hình toàn bộ phần còn lại của lens product.

Bằng chứng, đếm trên 18 mục và 894 dòng:

| Có trong tài liệu | Không có trong tài liệu |
|---|---|
| Pipeline 6 tầng, 3 layer generation | **Ai** là người dùng |
| Data model 13 entity | **Vấn đề gì** của người đó đang được giải |
| Schema panel 12 field | Người đó **hiện đang làm thế nào** khi chưa có công cụ này |
| Kiến trúc 3 microservice + Vector DB | Vì sao họ **đổi** sang dùng công cụ này |
| Layout Score 5 chiều | Cái gì là **"đủ tốt"** — chất lượng tối thiểu để dùng được |
| 4 MVP milestone | Một tiêu chí thành công **đo được** nào |
| Moat được nêu tên | Bằng chứng có ai **cần** thứ này |

Từ "user" xuất hiện đúng ở §14 (UI) và §18 (human approval) — cả hai lần với nghĩa *người vận hành công cụ*, không phải người có nhu cầu.

**Hệ quả:** không thể trả lời "phù hợp hay chưa" theo nghĩa product-market fit, vì tài liệu chưa nêu market. Câu trả lời trung thực phải tách làm hai, và **việc chưa trả lời được nửa thứ hai chính là phát hiện**, không phải một khoảng trống cần lấp bằng suy đoán.

Đây không phải lời phê. Bắt đầu từ "kiến trúc thú vị" là động lực hợp lệ. Nhưng nó phải được **gọi đúng tên**, vì hai loại dự án này có tiêu chí thành công khác nhau hoàn toàn, và **cắt scope theo tiêu chí sai là cách hỏng phổ biến nhất**.

Còn một failure mode nữa mà tài liệu không lo: **tài liệu đo thành công bằng "hệ thống chạy đúng", không bằng "comic đọc được"**. 894 dòng nói về tính đúng đắn cơ học (state khớp, costume khớp, vũ khí không mất) và không có dòng nào về việc trang comic đó có **hay** không — pacing có nhịp, panel có đáng vẽ, người đọc có muốn lật trang. Một comic mà mọi nhân vật đều consistent nhưng nhịp truyện chán thì hệ thống *pass mọi check* và *thất bại hoàn toàn*. Lỗi này **vô hình đối với chính hệ thống**: Continuity Checker không bắt được, không metric nào trong tài liệu bắt được.

→ **Sửa cái gì:** cạnh mọi metric kỹ thuật phải có đúng một câu hỏi con người trả lời — *"trang này đọc có ổn không?"* — và câu trả lời đó **được ghi lại**, ngay từ MVP0. **Thay bằng gì:** nó vừa là metric chất lượng thật, vừa là dữ liệu preference cho moat ở §7. **Không sửa thì hỏng thế nào:** anh sẽ có một hệ thống pass mọi check và không ai muốn đọc, và sẽ không biết điều đó cho tới khi có người đọc thật.

### 3.3 Bốn thứ làm ĐÚNG, đừng đổi

Mục này đặt **trước** mọi phần phản biện, có chủ ý. Tài liệu có nhiều điểm đúng; một bản đánh giá chỉ toàn phản biện là bản đánh giá sai.

**(1) "Ảnh là output của specification, không phải dữ liệu chính" (§Quyết định kiến trúc cuối tài liệu) — quyết định đúng nhất của cả tài liệu.**

`architect` xếp nó là điểm mạnh nhất của toàn bộ tài liệu — nếu chỉ giữ được một quyết định trong `Request.md` thì giữ cái này — và ánh xạ được sang bốn pattern đã biết: source vs build artifact, CQRS write model vs materialized view, declarative desired-state + reconciliation (Continuity Checker = drift detection), và cache có key.

Và đây là phần đáng chú ý nhất: **quyết định này trùng khớp với đường ranh pháp lý.** Theo tiền lệ Zarya of the Dawn, phần **được bảo hộ bản quyền** chính là **panel layout + selection/coordination/arrangement + text do người viết** — tức là **đúng output của Comic IR (Comic Intermediate Representation) + Layout Director**; ảnh raw thì không được bảo hộ. Một quyết định kiến trúc thuần kỹ thuật hoá ra rơi đúng vào phía được bảo hộ của đường ranh. Chi tiết ở §8.2.

Một điều chỉnh về **cách diễn đạt**, không phải về quyết định: với closed API (không lộ seed, model đổi âm thầm phía provider), ảnh đã generate **không phải cache** — cache là thứ mất rồi tái tạo lại được y hệt. Ảnh là **immutable artifact có provenance**. Hệ quả kỹ thuật cụ thể: **không bao giờ xoá ảnh đã approved** để "tiết kiệm storage vì regenerate được"; pin cứng `approved_generation_id` vào panel; lifecycle policy chỉ được xoá ảnh rejected/orphan.

**(2) Tách `identity` / `appearance` (§9) — abstraction đúng, gần như miễn phí.**

`character` = Identity (bất biến: `face_ref_id`, `body_proportions`, `age_baseline`, `personality`); `character_state` = Appearance (biến thiên theo timeline). Đúng về mặt phân tách. Một bổ sung: Identity chỉ bất biến **trong phạm vi một timeline** — truyện có time-skip 10 năm hoặc nhân vật lúc nhỏ/lúc lớn thì face cũng đổi. → Thêm `character_identity_variant(character_id, variant_name, valid_from_story_order, face_ref_id, body_ref_id)`, ví dụ `lam_phong@child`, `lam_phong@adult`. Không có cái này, truyện dài nào có hồi ức tuổi thơ là vỡ.

**(3) Comic IR (§4) — chi phí thấp, giá trị cao, và nó là điều kiện của mọi thứ khác.**

`senior-ai-engineer` nêu rõ lợi ích số một **không phải** debuggability mà là **editability**: một panel spec sai thì con người sửa được **một field**; một ảnh sai thì chỉ có nút re-roll. Không có IR thì sản phẩm không có cơ chế sửa nào ngoài "tạo lại và cầu may". Cộng thêm: bảng `Generation` (§13) chỉ có nghĩa khi input của nó là một spec có ID ổn định. `researcher` xác nhận bằng prior art: R² (Novel-to-Screenplay với Causal Plot Graphs) và shot decomposition của CANVAS — đây là hàng **rủi ro thấp nhất** trong bảng khả thi (§4.2).

**(4) Timeline là first-class entity (§3), state neo vào `Event` chứ không vào chapter (§2, §3, §9).**

`architect` gọi việc nhìn ra đây là hạt nhân của consistency là insight then chốt — đúng, và hiếm. Pattern gần nhất đã được giải triệt để trong data warehousing (SCD Type 2 trên trục narrative time + temporal snapshot/as-of query) — không cần phát minh gì mới. Điều kiện duy nhất: siết bốn cách diễn đạt song song (`Character.timeline`, `Event.character_state`, `Appearance @ Chapter`, `CharacterState`) thành **một** mô hình duy nhất — xem §5.1.

---

## 4. Có khả thi hay không?

### 4.1 Verdict: khả thi có điều kiện — BẢY điều kiện

`researcher` chốt **"✅ KHẢ THI CÓ ĐIỀU KIỆN"**: ý tưởng **không** là science fiction, nhưng khả thi **chỉ trong các điều kiện đồng thời**. Báo cáo gốc nêu 4 điều kiện; sau vòng delta (mô hình SaaS user-upload), số điều kiện **tăng lên 7**:

| # | Điều kiện | Không thoả thì hỏng thế nào |
|---|---|---|
| 1 | **≤3 nhân vật/panel**, cứng hoá trong Comic IR; cảnh đông người dùng shot xa / silhouette / crop | Attribute binding thất bại gần hoàn toàn từ 4 người: ảnh trông hợp lý nhưng gắn sai trang phục cho sai người (§5.6) |
| 2 | **Chữ đi qua typeset layer riêng**, không nhúng vào ảnh AI | Sửa một câu thoại thành một lần regenerate ảnh; bubble che mặt nhân vật; mất phần được bảo hộ bản quyền (§5.4) |
| 3 | **User warrant + indemnify + safe harbour Điều 198b** — công cụ takedown, đăng ký đầu mối với Bộ VHTTDL, SLA 72 giờ *(điều kiện này **thay thế** điều kiện "IP tự sở hữu" của báo cáo gốc, vì mô hình đã đổi sang user-upload)* | Nền tảng chịu trách nhiệm cho nội dung user upload, không hưởng được miễn trừ (§8.3) |
| 4 | **AI disclosure** — giờ là **nghĩa vụ nội địa Việt Nam**, không chỉ chuyện thị trường Hàn Quốc | Vi phạm Luật TTNT 2025; deadline tuân thủ ~01/03/2027 (§8.4) |
| 5 | **Pricing metered / BYOK, không subscription phẳng** | Một power user xoá margin của bốn user thường; −262% margin ở 3 chapter/tháng (§9b) |
| 6 | **Tư vấn luật sư SHTT về Điều 37a và khoản 4 Điều 11 TRƯỚC khi thương mại hoá** | Rủi ro nhị phân: không làm sản phẩm chậm, mà làm sản phẩm **bất hợp pháp** (§8.5) |
| 7 | **Budget COGS ở hệ số 3x, không 2x** | Toàn bộ mô hình tài chính lệch **+50%** so với thực tế (§9b.1) |

Cộng thêm hai điều kiện từ hai lens kỹ thuật, cùng mức bắt buộc: **(8) deterministic hoá bốn transform** và **(9) HITL gate + eval kit ở MVP1, không phải MVP4** (§5.5, §10).

> [!IMPORTANT]
> **Vậy tổng là CHÍN điều kiện, không phải bảy.** Bảy là số của `researcher` (lens có web access, nhìn từ hướng thị trường + pháp lý); hai điều kiện còn lại đến từ `architect` và `senior-ai-engineer`. Con số "bảy" giữ trong tiêu đề mục này vì nó là số của một lens cụ thể và truy vết được về findings — nhưng **điều kiện phải thoả đồng thời là chín**. Đếm bảy khi lập kế hoạch là bỏ sót hai điều kiện có cùng mức bắt buộc.

### 4.2 Bảng khả thi từng thành phần

Bảng của `researcher` §8.2, giữ nguyên ký hiệu và giữ nguyên con số. Ký hiệu: ✅ đã giải được · 🟡 giải được một phần · ❌ chưa giải được · ⚪ không tìm được prior art.

| Thành phần | Trạng thái | Bằng chứng |
|---|---|---|
| **Story Bible extraction** | ✅ **Đã giải được** | CANVAS Global Continuity Plan hoạt động thực tế ([arXiv 2604.13452](https://arxiv.org/html/2604.13452v1)); two-stage extract-then-relate là pattern đã xác lập; Gemini Pro 2.5 đạt 62,5% literary evidence retrieval > human expert 55,0% ([arXiv 2506.03090](https://arxiv.org/html/2506.03090v1)); ComicInk đã ship extract 20-character roster từ novel 500 trang ([comicink.ai/blog](https://www.comicink.ai/blog/convert-book-to-comic-series)). **Caveat**: CANVAS tự nêu limitation là nó *giả định* entity extract được đáng tin cậy. |
| **Timeline state / query "state @ Ch12"** | 🟡 **Giải được một phần** | Sudowrite đã ship *"entries tagged by timeline... character states per era"* ([sudowrite.com/blog](https://sudowrite.com/blog/writing-multiple-timelines-ai/)) — nhưng cho novel writing, không phải comic. **Chưa có** ai làm queryable timeline state cho comic generation. Là engineering, không phải research risk. |
| **Comic IR / Comic Script Engine** | ✅ **Đã giải được** | R² — Novel-to-Screenplay với Causal Plot Graphs ([arXiv 2503.15655](https://arxiv.org/pdf/2503.15655)); CANVAS shot decomposition ([arXiv 2604.13452](https://arxiv.org/html/2604.13452v1)); mọi đối thủ đều làm được ở mức nào đó. Rủi ro thấp nhất trong bảng. |
| **Character consistency — 1 nhân vật/panel** | ✅ **Đã giải được** | CANVAS character avg **4.91/5** trên HardContinuityBench với Gemini-3-pro-image; human preference **86,7% win-rate** ([arXiv 2604.13452](https://arxiv.org/html/2604.13452v1)). Đủ tốt để xuất bản. |
| **Multi-character panel (2–3 nhân vật)** | 🟡 **Giải được một phần** — hàng load-bearing nhất | Triangulation 3 nguồn: (a) **vendor claim** Google *"up to 5 people"* / 14 reference images ([blog.google](https://blog.google/innovation-and-ai/products/nano-banana-pro/)) — chưa verify độc lập; (b) **open-source benchmark** CogCanvas ID-Sim 42.33 (2 người) → 27.21 (3) → 2.67 (4) → 0.52 (5) ([arXiv 2606.15867](https://arxiv.org/html/2606.15867)); (c) **pipeline-level** CANVAS 4.91/5 nhưng nhờ agentic memory + VLM selection, **không phải raw model**. **Không tìm được benchmark độc lập nào đo frontier model ở 2-3 nhân vật.** → Phải verify từng panel + regenerate. |
| **Multi-character panel (4+)** | ❌ **Chưa giải được** | CogCanvas: *"near-complete failure on object/fashion binding beyond three subjects"* ([arXiv 2606.15867](https://arxiv.org/html/2606.15867)); Nano Banana Pro blend traits / merged faces khi vượt giới hạn ([nenobanana.com](https://www.nenobanana.com/blogs/character-consistency-in-nano-banana)). |
| **Location consistency** | ✅ **Đã giải được** | CANVAS: Consecutive BG **4.88/5**, Non-consecutive BG **4.88/5** (baseline 4.06) — background giữ tốt hơn cả qua các shot không liên tiếp, đúng lo ngại §10 ([arXiv 2604.13452](https://arxiv.org/html/2604.13452v1)). Cơ chế: background anchors trong Visual State Memory. |
| **Props / vũ khí consistency** | 🟡 **Giải được một phần** | CANVAS Props chỉ **4.19/5** — thấp nhất trong 4 metric, cải thiện so baseline chỉ **+2,5%** ([arXiv 2604.13452](https://arxiv.org/html/2604.13452v1)). Đúng khớp ví dụ *"✗ sword missing"* §15. Cần Continuity Checker nhắm riêng vào props. |
| **Text rendering tiếng Việt trong ảnh** | 🟡 **Giải được một phần — nhưng đừng dùng** | Press VN xác nhận Nano Banana Pro render tiếng Việt có dấu tốt ([VietnamNet](https://vietnamnet.vn/nano-banana-pro-gay-soc-voi-kha-nang-tao-anh-voi-chu-tieng-viet-cuc-chuan-2465113.html)); Google claim multilingual ([blog.google](https://blog.google/innovation-and-ai/products/nano-banana-pro/)); ~94-95% accuracy English. **Không có benchmark định lượng nào cho tiếng Việt**; nền tảng khó khăn có tài liệu ([arXiv 2506.05061](https://arxiv.org/html/2506.05061)). → Dùng typeset layer bất kể, vì 3 lý do ở §5.4. |
| **Auto speech-bubble typesetting** | 🟡 **Giải được một phần — phải tự build** | Comical-JS có bubble/tail rendering nhưng auto-placement ghi rõ *"in the future may provide"* ([github.com/BloomBooks/comical-js](https://github.com/BloomBooks/comical-js)). Prior art thuật toán: [ACM DOI 10.1145/2505483.2505486](https://doi.org/10.1145/2505483.2505486). Là phần **tự viết**. |
| **Continuity check bằng VLM** | ✅ **Đã giải được** | **ContinuityEval** (trong CANVAS): VLM autorater 3 chiều, Likert 1-5, đã dùng làm metric trong paper ([arXiv 2604.13452](https://arxiv.org/html/2604.13452v1)). **MIE** (MIBE): **0.922** pairwise accuracy vs human preference, **0.884** trên unseen generator ([arXiv 2607.01383](https://arxiv.org/abs/2607.01383)). → Không phải ý tưởng suy đoán, là kỹ thuật có số. |
| **AI Layout Director / Layout Score** | ⚪ **Không tìm được prior art trực tiếp** | Không tìm được paper/tool nào về narrative-importance-driven panel layout với scoring như §5. Có thể là phần **thật sự mới** — hoặc là phần chưa ai làm vì không đáng. Không đủ dữ liệu để kết luận. |

> Đọc bảng này theo chiều dọc: hàng **load-bearing** duy nhất còn ở trạng thái 🟡 mà cả sản phẩm dựa vào là **multi-character panel 2–3 nhân vật**. Đó chính là thứ MVP0 phải tự đo, vì không benchmark công khai nào đo nó.

### 4.3 Kiến trúc này ĐÃ được validate bằng số — CANVAS

**CANVAS — Continuity-Aware Narratives via Visual Agentic Storyboarding**, [arXiv 2604.13452](https://arxiv.org/html/2604.13452v1), 15/04/2026. Backbone: **Gemini-3-pro-image**.

Kiến trúc CANVAS dùng đúng ba intermediate representation, và chúng ánh xạ gần như 1:1 sang `Request.md`:

| CANVAS | Tương ứng trong `Request.md` |
|---|---|
| **Global Continuity Plan (𝒫)** — track character appearance states, location assignments, object state transitions qua narrative | Story Bible + Timeline state (§2, §3) |
| **Visual State Memory (ℳ)** — character appearance anchors, background anchors, previously generated frames | Character Reference Sheet + Location Identity (§8, §10) |
| **Sequential retrieval + QA-based selection** — retrieve anchor, generate candidates, score bằng VLM-based consistency questions | Continuity Checker (§15) |

Kết quả đo trên HardContinuityBench (ContinuityEval, Likert 1–5, VLM autorater):

| Metric | CANVAS | Baseline (Gemini-CT) | Δ |
|---|---|---|---|
| Character Avg | **4.91** | 4.39 | +11,8% |
| Consecutive BG | 4.88 | 4.48 | +8,9% |
| Non-Consecutive BG | 4.88 | 4.06 | +14,0% |
| Props Consistency | 4.19 | 4.06 | +2,5% |

Human preference: **86,7% win-rate** vs AutoStudio.

**Phát hiện này cắt hai chiều, và phải nêu cả hai:**

- **Tốt** — anh **không** đang đánh cược vào một giả thuyết. Câu *"Story Bible + Timeline State + Canonical References + Visual Prompt Compiler + Continuity Checker"* ở cuối `Request.md` là **đúng về mặt kỹ thuật**, và research đồng ý bằng số. Rủi ro kỹ thuật của MVP1–MVP2 thấp hơn PM tưởng trước fan-out.
- **Xấu** — câu *"Đây mới là moat của sản phẩm"* là **sai**. Concept đã public trên arXiv từ 15/04/2026; ai đọc cũng dùng được. Moat thật phải nằm ở chỗ khác (§7). Điểm bù: **chưa có sản phẩm thương mại nào ship nó** — ComicInk sâu nhất mà vẫn chỉ dùng *"story so far"* summary text + cap 20 nhân vật / 12 issues. Khoảng cách research → product **đang mở**, nhưng cửa sổ này sẽ hẹp lại.

Limitation do chính tác giả CANVAS nêu, đáng ghi nhận vì nó chính là rủi ro của anh: tốn kém tính toán; không model được fine-grained physical interaction / complex motion; và **giả định "narrative entities can be reliably extracted from text"** — tức là giả định đúng cái mà MVP1 phải làm.

### 4.4 Boss cuối thật không phải cái tài liệu nghĩ

§7 gọi style/character consistency là "boss cuối". **Đúng ở thời điểm viết, nhưng đã hạ cấp trong 2026**: ngành ghi nhận character consistency chuyển từ *"mostly impossible"* sang *"actually workable"* trong cuối 2025–đầu 2026 ([javilopen.substack.com](https://javilopen.substack.com/p/consistency-of-characters-objects)). Ba boss thật, theo `researcher`:

1. **Multi-character attribute binding.** CogCanvas cho thấy model vẽ ra ảnh *"visually plausible"* nhưng **gắn sai trang phục cho sai người**. Đây là loại lỗi khó bắt nhất, vì ảnh trông ổn — không có gì lệch để mắt người nhận ra ngay.
2. **Props continuity.** CANVAS 4.19/5, kém nhất trong 4 metric, cải thiện so baseline chỉ +2,5%. Ví dụ *"✗ sword missing"* ở §15 không phải lo hão mà là **lỗi hệ thống đã đo được**.
3. **Backlash & pháp lý, không phải công nghệ.** Naver Webtoon bị độc giả **tổ chức boycott subscription** khi một tác phẩm AI-created bị phát hiện; BlueLine Studio bị buộc **vẽ lại các episode của _Knight King_** sau khi fan phát hiện background được AI-polish ([Korea Times 06/11/2025](https://www.koreatimes.co.kr/lifestyle/trends/20251106/webtoon-industry-seeks-ai-edge-amid-legal-ethical-challenges)). Cộng Korea AI Basic Act hiệu lực 22/01/2026, phạt tới 30 triệu won.

Và một boss thứ tư mà **ba lens độc lập cùng chỉ ra**, không lens nào biết kết luận của lens kia: **ràng buộc thật của dự án là thời gian người, không phải tiền.** `architect` suy ra từ phân bổ effort; `researcher` suy ra từ chi phí inference thấp bất ngờ; `senior-ai-engineer` suy ra từ HITL gate (5 phút/chapter × 100 chapter ≈ **8 giờ**, với một người). Ba đường lập luận khác nhau, một kết luận — đây là mức tin cậy cao nhất mà run này đạt được về bất kỳ điểm nào. Chi tiết ở §9.

---

## 5. Bảy vấn đề phải sửa TRƯỚC khi viết code

### 5.1 `(chapter, scene)` làm khóa thời gian — sai âm thầm ở flashback

**Sửa cái gì.** §3 dùng `(chapter, scene)` làm khóa thời gian (`Event #102 / Chapter: 17 / Scene: 4`). Đó là **thứ tự đọc** — *syuzhet*, thứ tự người đọc gặp sự việc — chứ không phải **thứ tự sự việc xảy ra** — *fabula*, thứ tự trong thế giới truyện. Với truyện tuyến tính hai cái trùng nhau nên lỗi bị che.

Với flashback thì sai **cả hai chiều**: Chapter 20 kể hồi ức 15 năm trước → Event ở Ch20 có thứ tự **lớn hơn** Ch19 → query "state tại Ch20" trả về costume hiện tại, trong khi cảnh đó phải là Lâm Phong lúc 9 tuổi. Ngược lại, sau khi xử lý Ch20, mọi query "state gần nhất" cho Ch21 sẽ vô tình lấy state của **quá khứ** vì nó là row mới nhất theo `(chapter, scene)`. Flashback/hồi tưởng/song tuyến là **cực kỳ phổ biến** trong truyện dài — đây là trường hợp thường, không phải edge case.

**Thay bằng gì** (DDL cụ thể ở `findings/architect.md` §2.2):

1. **Hai trục tách bạch** trên bảng `event`: `reading_order NUMERIC(20,6)` để render page theo thứ tự đọc, và `story_order NUMERIC(20,6)` cho **mọi** as-of state query. Trộn hai cái là nguồn của toàn bộ lớp bug này.
2. **`timeline_id`**: mỗi tuyến song song / mỗi flashback lớn là một `timeline` row có `kind` (`main`/`flashback`/`parallel`/`dream`) và `anchor_order`. State query luôn scope theo `timeline_id`; nhánh flashback kế thừa state từ timeline cha tại `anchor_order` (resolver fallback hai bước).
3. **State neo vào `Event` (mức scene), không vào chapter** — §9 (`Appearance @ Chapter 12`) là **sai mức**: nhân vật vào chapter mặc thường phục → bị tấn công → đổi áo giáp → cuối chapter giáp hỏng là **ba** state trong một chapter. Cho phép chia nhỏ hơn scene bằng `beat_no`.
4. **`story_order` là `NUMERIC` sparse (bước nhảy 1000), không phải `INT` tuần tự**, và **phải editable có UI**: LLM extract sai thứ tự là chắc chắn xảy ra; chèn giữa với NUMERIC là một UPDATE một row, với INT là renumber cả bảng.
5. **Index quyết định**: `(character_id, timeline_id, story_order DESC)` → as-of query thành **backward index scan + LIMIT 1**, O(log n) bất kể truyện dài bao nhiêu. Không replay, không aggregate.
6. **Guard bắt buộc**: mọi query state đi qua **một** hàm duy nhất `resolveState(entity, at_event)`, kèm một test kiểu guardrail: *"không được có `ORDER BY chapter_no` trong bất kỳ đường dẫn resolve state nào"*.

**Không sửa thì hỏng thế nào — và đây là hệ quả dây chuyền phải nêu.** Hệ thống vẽ sai trang phục/vết thương/vũ khí ở **mọi** cảnh hồi tưởng. Nhưng tệ hơn: **Continuity Checker sẽ "sửa" theo state sai — tức là tự động làm hỏng đúng những panel đang đúng.** Một lỗi data model biến feature đắt nhất của tài liệu thành công cụ phá hoại. Lỗi này **không crash**, chỉ corrupt dữ liệu âm thầm ⇒ phát hiện muộn, và vì `story_order` là giả định lan khắp mọi module, sửa sau đồng nghĩa migrate dữ liệu + rà lại toàn bộ query.

### 5.2 Continuity Checker: từ "flag lỗi + autofix" sang "chọn giữa N ứng viên"

> ⭐ **Đây là mục quan trọng nhất của cả tài liệu.** Nó là kết luận tổng hợp mà **không lens nào tự đến được** — nó chỉ xuất hiện khi đặt hai findings cạnh nhau.

**Hai lens nói ngược nhau, và cả hai đều đúng.**

- `senior-ai-engineer`: Continuity Checker ở dạng §15 mô tả tạo ra **giá trị âm**. Lập luận: (a) check được tài liệu nhấn mạnh nhất — `✓ face`, "có cùng người không" — là check **kém khả thi nhất** trên art cách điệu, FP ước lượng **40-60%**; (b) panel nhiều nhân vật **về cơ bản không kiểm được**, vì để biết "Lâm Phong trong panel này có mặc áo đen không" thì trước tiên phải biết **nhân vật nào trong panel là Lâm Phong** — đó chính là bài toán **re-identification**, tức là bài toán mà checker được lập ra để giải: một **vòng lặp logic**; (c) kinh tế của false positive: 35 panel/chapter, báo lỗi 30% panel, một nửa báo sai → sau hai chapter người dùng học được rằng checker không đáng tin và **bỏ qua toàn bộ cảnh báo, kể cả cảnh báo đúng**. Checker khi đó **tệ hơn không có**, vì nó đã tiêu **niềm tin** — thứ đắt hơn thời gian.
- `researcher`: continuity check bằng VLM là ✅ **"đã giải được"**, có số hẳn hoi — **ContinuityEval** dùng làm metric trong CANVAS, và **MIE** (MIBE) đạt **0.922 pairwise accuracy** vs human preference, **0.884** trên unseen generator.

**Phân xử: cả hai đúng, vì hai bên đang nói về HAI TASK KHÁC NHAU.**

| | Task | Trạng thái |
|---|---|---|
| `researcher` đo | **Pairwise ranking** — *"trong hai ứng viên này, cái nào consistent hơn?"* | **Đã được validate định lượng** (MIE 0.922) |
| `senior-ai-engineer` phản biện | **Absolute per-panel detection** — *"panel này đúng hay sai, có/không?"* | **Chưa được validate** |

Một VLM có thể rất tốt ở **so sánh tương đối** mà vẫn tệ ở **ngưỡng tuyệt đối**. Đó là khác biệt đã biết, không phải nghịch lý.

**Bằng chứng phân xử nằm trong chính CANVAS.** Paper mà `researcher` dẫn ra để nói "đã giải được" **không** dùng VLM làm checker gắn nhãn lỗi rồi autofix. Nó dùng VLM để **select giữa N candidate** — `QA-based selection`: generate N phương án cho mỗi shot, hỏi VLM các consistency question, chọn cái điểm cao nhất. Tức là chính cái paper đó đang dùng **cơ chế mà `senior-ai-engineer` mới là người mô tả đúng**.

**⇒ Kết luận: giữ công nghệ, đổi cách dùng.**

| | Bỏ | Thay bằng |
|---|---|---|
| Cơ chế | Generate 1 ảnh → checker gắn nhãn `✓/✗` từng attribute → `[Fix automatically]` | Generate **N candidate** → VLM QA-select cái consistent nhất → người xác nhận |
| Câu hỏi VLM phải trả lời | *"Panel này đúng hay sai?"* (chưa validate) | *"Trong N cái này, cái nào hơn?"* (MIE 0.922) |
| Hình thức output | Huy hiệu phán quyết trên từng panel | **Hàng đợi review được xếp hạng** — "những panel đáng xem lại nhất" |
| Khi sai thì mất gì | Mất niềm tin (một dấu ✗ sai là một phán quyết sai) | Mất 3 giây (một thứ hạng sai chỉ là một gợi ý sai) |

Cùng công nghệ, **cùng chi phí**, khác hoàn toàn về tính khả thi — vì cơ chế mới **không bao giờ phải trả lời "đúng hay sai"**, chỉ phải trả lời "cái nào hơn".

**Về `[Fix automatically]` — cắt.** Về mặt kỹ thuật nó chỉ có thể là một trong hai thứ, và cả hai đều không phải "fix": (a) **regenerate cả panel** = re-roll, mất mọi thứ đang đúng, có thể sửa được áo mà làm hỏng mặt, và nếu nguyên nhân gốc là spec sai thì re-roll **tái tạo đúng lỗi cũ**; (b) **inpaint** cần một **mask**, nhưng checker chỉ biết "costume mismatch", **không biết ở đâu** — nó không có localization. Phiên bản trung thực: **`[Tạo lại với ràng buộc được nhấn mạnh]`**, giữ cả hai version, hiển thị side-by-side, **người chọn**. Không bao giờ tự áp dụng.

**Nếu vẫn muốn giữ một checker report-only ở MVP**, phiên bản thu hẹp mà thực sự hoạt động: chỉ panel **một nhân vật**, chỉ **top 5 nhân vật chính**; chỉ **3 check thô** (nhóm màu trang phục, nhóm màu tóc, có/không vật lớn trên tay) + **1 check so sánh cặp** (drift so với panel liền trước của cùng nhân vật — so ảnh với ảnh, đây là check bị §15 bỏ sót và là check bền nhất); `unclear` là câu trả lời hợp lệ **hạng nhất**; cổng chất lượng **precision ≥ ~0.7** trên ≥100 panel dán nhãn tay trước khi bật một check nào — kể cả `face`; chạy **on-demand** lúc chốt trang, không trên mọi bản nháp.

⚠️ **Và bắt buộc nói rõ độ phủ với người dùng.** Phiên bản thu hẹp trên phủ ước lượng **40-60% số panel** (`senior-ai-engineer` ước lượng) — phần còn lại là panel nhiều nhân vật, tức phần **không kiểm được** vì vòng lặp re-identification ở trên. Đây không phải chi tiết kỹ thuật mà là **yêu cầu giao tiếp sản phẩm**: nếu UI để người dùng hiểu rằng "đã chạy check" nghĩa là "đã được bảo vệ toàn diện", thì mọi lỗi lọt qua 40-60% kia sẽ được ghi vào sổ nợ niềm tin của checker — đúng cơ chế tự sát đã mô tả ở lập luận (c) phía trên. Phải hiện tường minh: *"đã kiểm N/M panel, M−N panel không kiểm được vì có nhiều nhân vật"*.

**Và một định vị lại đáng tiền:** giá trị lớn nhất của checker **không** ở chỗ bắt lỗi, mà ở chỗ **tạo ra dữ liệu có nhãn** — mỗi lần người dùng chấp nhận/từ chối một cảnh báo là một nhãn preference. Đó là nguồn duy nhất cho eval của Layer 3, và cũng chính là nguyên liệu của moat thật ở §7. Nên coi nó là **công cụ đo lường có mặc áo feature** — và điều đó lại càng là lý do làm nó nhỏ và trung thực thay vì to và ồn ào.

**Không sửa thì hỏng thế nào:** anh sẽ build hạng mục đắt nhất, tự tuyên bố là moat, ở đúng dạng có FP profile xấu nhất, và nó sẽ tiêu niềm tin của khách hàng trong hai chapter đầu.

### 5.3 Layout Score: bỏ số thực, dùng rubric rời rạc

**Sửa cái gì.** §5 đề xuất `Narrative importance 0.95 / Emotional intensity 0.88 / Action intensity 0.76 / Dialogue density 0.20 / Visual spectacle 0.91 => FULL PAGE`. Cơ chế này, **đúng như đang viết, là trang trí — không phải khoa học**. Bốn lý do, theo thứ tự sức nặng:

1. **Không calibrated và không thể calibrate.** `0.95` neo vào đâu? Không có định nghĩa toán tử, không anchor example, không đơn vị. LLM đang sinh một **token trông giống số**. Khác biệt `0.95` vs `0.91` **không mang thông tin**. Hai chữ số thập phân ngụ ý độ phân giải mà quá trình sinh ra nó không có.
2. **Không ổn định giữa hai lần gọi.** Nếu ngưỡng là `> 0.90 → FULL PAGE` thì **cùng một chapter chạy hai lần ra hai layout khác nhau** — phi-determinism ở đúng chỗ người dùng nhìn thấy.
3. **Không so sánh được giữa chapter.** LLM chấm điểm tương đối với context nó đang thấy: panel "quan trọng nhất" của một chapter filler cũng được ~0.9, y như climax của cả bộ. Không có thang toàn cục ⇒ **ngưỡng cố định là vô nghĩa**, và kết quả thực tế là cứ vài trang lại một full page → "full page" mất hết sức nặng, tức là chính cái nó định làm (nhấn mạnh) bị phá.
4. **Hàm tổng hợp không tồn tại.** Tài liệu **không định nghĩa cách gộp** 5 số thành một quyết định. Nếu để LLM gộp luôn thì 5 con số là **lời biện minh hậu nghiệm** cho một quyết định đã được đưa ra bởi cùng một quá trình tiềm ẩn — chúng không tham gia vào quyết định. Đó là định nghĩa của trang trí.

**Bằng chứng tự tố, cụ thể và không thể bào chữa:** `dialogue density 0.20` là đại lượng **code đếm được chính xác** (số ký tự thoại / tổng ký tự). Tài liệu đang trả tiền cho LLM để **đoán** một con số mà một dòng Python cho ra đúng. Chi tiết này cho thấy vấn đề không phải "LLM tệ" mà là **ranh giới LLM/code chưa được vẽ** (§5.5).

**Ghép với dữ liệu web:** `researcher` xếp Layout Score ⚪ — *không tìm được prior art trực tiếp* — và nêu hai cách đọc: có thể thật sự mới, hoặc chưa ai làm vì không đáng. Phản biện của `senior-ai-engineer` **phân định câu này**: đây là phần **"chưa ai làm vì không đáng"**, không phải phần "thật sự mới".

**Thay bằng gì** — bốn tầng, làm được cả bốn:

- **(A) Rubric phân loại rời rạc + bảng tra deterministic** *(đề xuất chính)*. Không cho LLM sinh số; cho nó **phân loại** vào enum có anchor example: `beat_type ∈ {establishing, dialogue_exchange, reaction, reveal, action_burst, climax, transition, aftermath}`. Rồi một bảng tra thuần `beat_type × dialogue_density (code tính) × character_count (code đếm) → layout_template`. LLM làm việc nó giỏi (phân loại có nhãn); quyết định layout thành **hàm thuần** — reproducible, unit-testable, giải thích được cho user (*"panel này là climax nên full page"*), và **sửa được bằng cách sửa bảng** thay vì sửa prompt.
- **(B) Emphasis budget trong phạm vi chapter** — mỗi chapter tối đa **1 full page + 2-3 large panel**. LLM chỉ phải **xếp hạng** các beat trong chapter (ranking ổn định hơn scoring rất nhiều vì là so sánh nội bộ, không cần thang tuyệt đối); code phân bổ theo quota. Việc này một mình giải quyết cả vấn đề (3) ở trên **và** lỗi "pacing đều đều" — vì quota **buộc** phải có tương phản.
- **(C) So sánh cặp — chỉ dùng khi làm eval, không dùng ở runtime.** Pairwise đáng tin hơn scoring nhưng tốn O(n log n) call; dùng nó để hiệu chỉnh rubric (A) offline.
- **(D) User đổi template bằng một click** — luôn phải có, đây là lối thoát khi (A)+(B) chấm sai.

**Không sửa thì hỏng thế nào:** anh sẽ có một bảng cấu hình ngưỡng chẳng điều khiển gì, layout không tái lập được giữa hai lần chạy, và "full page" bị lạm phát tới mức mất tác dụng nhấn mạnh.

### 5.4 Chữ & speech bubble — mục bị bỏ sót hoàn toàn

**Sửa cái gì.** Comic là **tranh + chữ**. `Request.md` có `dialogue` như một field của panel (§6) và `Dialogue` trong Comic Director (§11), nhưng **không một dòng nào** nói chữ đó lên ảnh bằng cách nào. Với truyện chữ Trung/Việt, thoại là phần lớn nội dung — đây không phải chi tiết nhỏ, và nó **nổ ngay ở panel có thoại đầu tiên, tức là trong MVP0**.

**Ba lý do độc lập buộc dùng typeset layer riêng — và không lý do nào trong đó là "model render dở":**

1. **Editability.** Sửa một câu thoại **không được** biến thành một lần regenerate ảnh ($0.067 + rủi ro mất consistency). Best practice ngành: *"Generate manga and comic panels with an editable lettering layer... you can rewrite, drag, and resize them **without regenerating the artwork**"* ([comicsai.org](https://www.comicsai.org/en/manga-speech-bubble-generator)).
2. **Bubble không được che mặt.** *"The common problem is adding words after the art is already crowded. Bubbles then cover faces, hands, or action."* Ràng buộc này phải **đi ngược** vào panel spec và prompt compiler: panel spec cần field **`text_safe_zone`** (cộng `text_budget` — số ký tự thoại — và `negative_space_hint`), và compiler phải truyền yêu cầu để chỗ trống xuống prompt. Đây là ràng buộc kiến trúc **từ typesetting ngược vào Visual Prompt Compiler** mà tài liệu hoàn toàn không có.
3. **Ranh giới bản quyền.** Layer text riêng chính là phần *"human-authored text"* + *"selection/arrangement"* — đúng phần **được bảo hộ** theo Zarya (§8.2). Nhúng chữ vào ảnh AI làm mờ đường ranh đó.

**Nêu trung thực về tiền đề.** `architect` giả định (GĐ-3) model **không** render được tiếng Việt có dấu ở chất lượng xuất bản. Tiền đề đó **sai một phần**: press VN xác nhận Nano Banana Pro render tiếng Việt có dấu tốt. **Nhưng không có benchmark định lượng nào** cho tiếng Việt (đặc biệt các chữ chồng hai dấu như "ế", "ữ", "ượ") của bất kỳ image model — chỉ có press coverage. ⇒ **Kết luận hành động của `architect` vẫn đúng, và đúng vì ba lý do mạnh hơn lý do nó nêu.** Tài liệu này nêu đúng lý do, không nêu lý do sai.

**Thay bằng gì:**

- **Generate art KHÔNG có chữ** (đưa `text, letters, watermark, speech bubble` vào negative prompt), rồi **overlay bubble bằng code**.
- Bubble là **layer dữ liệu riêng**, không nướng vào ảnh: bảng `speech_bubble(panel_id, speaker_id, kind, text, x/y/w/h chuẩn hoá 0-1, tail_x/tail_y, font, z_index, reading_index)`. Toạ độ chuẩn hoá là điểm then chốt — cùng một dữ liệu render được cả thumbnail và bản in 300 DPI.
- **Hai field cho thoại, không phải một**: `dialogue_source` (nguyên văn + `source_span`, bất biến) và `dialogue_rendered` (bản đã nén theo `text_budget_chars`, người sửa được, và edit của người **phải khoá lại** khỏi bị re-run ghi đè). Bubble đọc thoải mái chứa ~8-20 từ, thoại web-novel dịch thường 30-80 từ ⇒ hệ số nén cần **2-5×**. Bước rút gọn này là **hành vi biên tập có mất**, cần LLM **và** cần người review — và nó phải nằm **sau** layout, vì `text_budget` phụ thuộc diện tích panel. Thứ tự trong §17 làm sai chỗ này.
- **Auto-placement phải tự build.** Comical-JS có bubble/tail rendering nhưng auto-placement thì repo ghi rõ *"in the future may provide"*. Có prior art thuật toán tham chiếu được ([ACM DOI 10.1145/2505483.2505486](https://doi.org/10.1145/2505483.2505486)). Ở MVP: heuristic đơn giản (gần speaker, tránh vùng có mặt, thứ tự đọc) + **cho user kéo tay**. Với tiếng Việt thêm ràng buộc: line-height rộng hơn tiếng Anh vì dấu chồng ăn không gian phía trên, và wrap phải dùng thư viện hiểu Unicode combining marks.

**Không sửa thì hỏng thế nào:** phát hiện muộn ⇒ phải **generate lại toàn bộ ảnh đã làm** vì bubble che mặt nhân vật.

#### 5.4b Gán thoại cho speaker — human gate bắt buộc thứ hai

Bảng `speech_bubble` ở trên có field `speaker_id`. Câu hỏi mà `Request.md` không đặt: **ai điền field đó, và sai bao nhiêu phần trăm?**

Đây là bước ít được để ý nhất trong cả pipeline, và là bước có chi phí lỗi **bất đối xứng nhất**: một dòng gán sai speaker không làm giảm chất lượng trang — nó **làm hỏng cả trang** trong mắt người đọc, vì người đọc thấy ngay lập tức mà không cần đối chiếu gì. Web-novel dịch làm bài toán này khó hơn tiếng Anh: hội thoại nhiều người, tự sự chen giữa các dòng thoại, và đại từ/cách gọi (sư phụ, đại nhân, tại hạ) mang thông tin quan hệ mà một model không có bible sẽ đoán bừa.

**Tỉ lệ lỗi ước lượng** — `senior-ai-engineer` ước lượng, **không phải số đo**, giả định model tier hiện tại:

| Tình huống | Không có anchor + constraint | Có đủ 4 tầng dưới |
|---|---|---|
| 2 người, hội thoại luân phiên sạch | 10-20% | 3-8% |
| **3+ người, có tự sự chen** | **30-50%** | 15-25% |
| **Câu ngắn / thán từ đơn lẻ** | **40-60%** | 25-40% |

**Bốn tầng phải có, theo đúng nguyên tắc "LLM đề xuất, code quyết định" của §5.5:**

1. **Anchor deterministic TRƯỚC.** Regex bắt các dòng có tag rõ ràng (`X nói:`, `— … — X lạnh giọng`, `X cười`, `giọng X`). Precision rất cao, phủ ước lượng 30-60% dòng thoại. Đây là code, không phải LLM.
2. **LLM chỉ gán phần còn lại**, và bắt buộc kèm ba thứ: (a) **danh sách nhân vật có mặt trong scene** lấy từ Story Bible, dùng làm constrained decoding — speaker **phải** nằm trong tập này; chỉ riêng ràng buộc này đã diệt một lớp lỗi lớn, vì phần lớn lỗi attribution là gán cho nhân vật **không có mặt**; (b) các dòng đã anchor ở bước 1 làm mốc; (c) **cho phép trả `UNKNOWN`** — bắt model phải đoán là tự tạo ra lỗi.
3. **Kiểm chéo bằng code**: prior luân phiên, và nhất quán đại từ/appellation (nếu dòng gọi "sư phụ" thì speaker phải là đệ tử của người nghe — `Relationships` trong bible cho phép kiểm việc này bằng code).
4. **Lưu `speaker_confidence` và hiện cờ trong UI khi thấp** — không âm thầm đoán.

⚠️ **Kết luận về roadmap:** đây là **một trong HAI** chỗ bắt buộc có human gate ở MVP2. Chỗ còn lại là **dialogue condensation** (đã nêu ở §5.4 trên — bước nén 2-5× là hành vi biên tập có mất). Hai gate này phải được tính vào ngân sách giờ-người ở §9, không phải vào ngân sách token: chúng là lý do con số "5 phút/chương review" là **sàn**, không phải trần.

### 5.5 Ranh giới LLM / deterministic code chưa được vẽ

**Sửa cái gì.** Tài liệu mặc định "AI" ở mọi transform. Nhưng error cascade **nhân, không cộng**: 5 tầng mỗi tầng đúng 90% → end-to-end ≈ 59%; mỗi tầng 95% → ≈ 77%; muốn end-to-end 90% thì mỗi tầng phải ≈ 98% — và **không tầng LLM nào trong pipeline này đạt 98% zero-shot**. Cách duy nhất thắng phép nhân đó là chuyển vài tầng từ 90% lên **100%**.

**Thay bằng gì — bốn transform phải deterministic:**

| Transform | Vì sao là code, không phải LLM |
|---|---|
| **Prompt compiler** (§16) | Tra bảng `field value → cụm từ`, sắp thứ tự, dedup, xử lý xung đột theo precedence ladder, thực thi constraint budget, ghi log ràng buộc bị drop. Đây là **lookup + policy**, không phải suy luận. Deterministic thì unit-test được bằng golden snapshot, chi phí bằng 0. |
| **Story Bible reduce** | `state_at(N) = reduce(events where story_order <= N)` là hàm thuần. LLM chỉ phát **event** (`entity, attribute, value, permanence, evidence_span, confidence`) cho **một** chapter; code sở hữu state. Vết sẹo tồn tại tới chapter 400 vì **code không quên**, không phải vì model nhớ. |
| **Layout mapping** | Sau khi bỏ Layout Score số thực (§5.3), đây là một bảng tra. |
| **Chapter parse + text clean** | Regex/heuristic trên `Chương N` / `Chapter N`, và lọc rác scrape (quảng cáo, lời tác giả cuối chương, "xin ủng hộ phiếu đề cử"). Bước làm sạch text **không có** trong MVP1 của tài liệu, nhưng nó phải là bước **đầu tiên**, và là job của code. |

Kèm theo, trong compiler: **precedence ladder** (identity refs bậc 1, không bao giờ bị drop → ... → camera angle/composition/props phụ bị drop đầu tiên), **constraint budget** cứng (trần thực tế ước lượng 5-8 ràng buộc thị giác được tôn trọng đồng thời, trong khi §16 bung ra dễ đạt 20-40), **drop log** (`generation.degradations JSONB`), và **hai output** thay vì một: `text_prompt` **và** `conditioning_set`. Điểm cuối này quan trọng: §8 của tài liệu đã có trực giác đúng (*"Chứ không chỉ đưa text prompt"*, có sơ đồ cộng các reference), nhưng §16 lại làm phẳng tất cả thành một *"Model-specific prompt"* — hai mục **mâu thuẫn nhau**, và §16 là mục đang định nghĩa kiến trúc. Identity **không được** cạnh tranh với "ánh trăng gay gắt" trong cùng một chuỗi text.

**Mâu thuẫn nội tại §13 vs §16 — hai mục không thể cùng đúng.** §13 dựng bảng `Generation` (`prompt / model / model_version / seed / parent_generation`) với mục đích tuyên bố là **reproducibility**. Nhưng nếu có LLM trong đường compile ở **runtime**, thì cùng một panel spec sẽ sinh ra prompt khác vào ngày mai — và reproducibility mà §13 tồn tại để bảo đảm **bị phá ngay tại chỗ**. **Compiler deterministic là điều kiện cần để §13 có nghĩa.**

Chỗ **cần** LLM (hẹp, và nên cache vĩnh viễn): soạn từ vựng offline một lần (sinh cụm từ cho mỗi giá trị attribute → người review → **lưu vào bảng**, đây là dữ liệu chứ không phải runtime), và dịch action tự do → cụm pose ngắn khi từ vựng chưa có entry, **cache theo hash của action text** (web-novel lặp lại rất nhiều: "rút kiếm", "chắp tay", "phi thân" ⇒ hit rate cao sau vài chapter). Ngoài hai việc đó: không có LLM trong compiler.

**Không sửa thì hỏng thế nào:** đặt LLM ở đây là chỗ **dễ đốt token nhất mà thu về ít nhất** — LLM-in-compiler một mình có thể chiếm >50% tổng token của pipeline text — **và** nó phá bảng `Generation`, tức là phá luôn hồ sơ pháp lý ở §6.4.

### 5.6 ≤3 nhân vật/panel — ràng buộc cứng

**Sửa cái gì.** `Request.md` không có giới hạn số nhân vật trong một panel, và LLM directing có xu hướng **nhồi tất cả nhân vật có mặt vào cùng một panel** — mà đó lại là panel khó giữ consistency nhất.

**Con số làm căn cứ** (CogCanvas, [arXiv 2606.15867](https://arxiv.org/html/2606.15867), 6/2026 — 1.952 reference images, 100 celebrity identities, 1.361 compositional prompts):

| Số nhân vật | ID-Sim (XVerse) | ID-Sim (UNO) |
|---|---|---|
| 2 | **42.33** | 23.23 |
| 3 | 27.21 | 19.60 |
| 4 | **2.67** | 19.60 |
| 5 | **0.52** | 13.47 |

> [!NOTE]
> **UNO có 19.60 ở cả hàng 3 và hàng 4 — đây là số thật của paper, không phải lỗi sao chép.** `context-auditor` đánh dấu con số lặp này là bất thường về mặt thống kê và yêu cầu đối chiếu nguyên văn; PM đã fetch trực tiếp Table 2 của [arXiv 2606.15867](https://arxiv.org/html/2606.15867v1) và xác nhận cả cặp `19.60/19.60` (ID-Sim) và cặp `14.65/14.65` (Attr-VQA) đúng như in trong paper. Nhãn cột của bảng này cũng đã đối chiếu: paper đánh theo **group size N=2..5**, khớp với cột "Số nhân vật" 2-5 ở đây — **không** lệch một bậc.

Attr-VQA (gắn đúng trang phục/vật phẩm cho đúng người) **sụp từ 3**: UNO 35.12 (2 người) → 14.65 (3 người) → 4-5 người gần như thất bại hoàn toàn. Kết luận của paper: *"near-complete failure on object/fashion binding beyond three subjects"* — ảnh trông hợp lý nhưng model **không gắn đúng attribute cho đúng identity**.

**Nêu rõ giới hạn của bằng chứng:** CogCanvas **chỉ test open-source** (OmniGen2, UNO, DreamO, XVerse, MOSAIC) — **không** test Nano Banana Pro / GPT Image 2 / FLUX.2. Với frontier model chỉ có **vendor claim** (*"up to 5 people"*, 14 reference images) và **không có benchmark độc lập nào** ở 2-3 nhân vật. ⇒ **MVP0 phải tự đo con số này** — nó là hàng 🟡 load-bearing duy nhất của §4.2.

**Thay bằng gì:**

- **Cứng hoá `≤3 nhân vật/panel` trong schema Comic IR**, không phải một guideline trong prompt.
- **Cảnh đông người**: shot xa / silhouette / crop — dùng ngôn ngữ hình ảnh để tránh phải bind attribute cho 5 identity.
- **Directing nên thiên vị panel một nhân vật vì lý do kỹ thuật**, và LLM không biết điều đó nếu không được nói. Đây là một khuyến nghị **xuyên tầng**: nó xuất phát từ giới hạn của Layer 3 nhưng phải được thực thi ở Layer 2.
- Ghi nhận thị trường: **hai đối thủ đã hard-code trần này** — ComicInk (*"additional characters beyond the first five per issue cost credits"*) và TaleAtelier (*"up to six named characters per project"*). Corroborate độc lập.

**Không sửa thì hỏng thế nào:** panel đông người sẽ ra ảnh *"visually plausible"* nhưng gắn sai trang phục cho sai người — loại lỗi khó bắt nhất, và cũng là loại lỗi mà checker ở §5.2 **không kiểm được** (panel nhiều nhân vật cần re-identification).

### 5.7 Multi-tenancy — 15-25% effort mà tài liệu không nhắc một dòng

**Sửa cái gì.** `Request.md` không có một dòng nào về multi-tenancy — hợp lý dưới giả định "công cụ cá nhân", nhưng sau gate thì đây là một khối công việc bị bỏ trắng. Ước lượng của `architect`: **15-25% tổng effort SaaS nếu tự viết; 8-12% nếu MUA phần mua được**. So sánh: pipeline lõi (story → panel → generate → composite) là 35-45%. Tức là **multi-tenancy không nhỏ hơn phần AI của sản phẩm**.

Nguyên tắc phân bổ cho 1 dev: **mua auth và billing, đừng viết.** Hai hạng mục này có sản phẩm chín, rủi ro bảo mật cao, giá trị khác biệt bằng không. Tự viết auth là cách nhanh nhất để một dev đơn lẻ đốt hai tháng và vẫn có lỗ hổng.

**Thay bằng gì — sáu quyết định không đảo được rẻ, phải đúng từ ngày đầu:**

1. ⭐ **`tenant_id NOT NULL` trên MỌI bảng, và là cột ĐẦU TIÊN của mọi composite index** (index as-of ở §5.1 đổi thành `(tenant_id, character_id, timeline_id, story_order DESC)`), cộng **Postgres RLS** làm lớp phòng thủ thứ hai. Mô hình: shared database + shared schema + `tenant_id` + RLS — **không** schema-per-tenant hay db-per-tenant (hai cái sau nhân chi phí migration lên N lần, thảm hoạ với 1 dev). Lập luận của `architect` về RLS đáng dẫn nguyên: app-layer filter sẽ có lúc bị lọt (một query quên `WHERE tenant_id`); RLS biến lỗi lập trình thành no-op thay vì rò rỉ dữ liệu chéo tenant — **với 1 dev không có code review, đây là bảo hiểm rẻ nhất tồn tại**.
2. **`tenant` và `user` là HAI entity riêng ngay từ đầu**, kể cả khi bản đầu là 1:1: `tenant(id, plan, status)`, `user(id, email)`, `membership(tenant_id, user_id, role)`. Mọi dữ liệu nghiệp vụ trỏ `tenant_id`, **không** trỏ `user_id` — nếu gắn vào `user_id`, ngày muốn bán gói team là viết lại toàn bộ authz + migrate quyền sở hữu.
3. **`cost_usd` + `model_id` + `model_version` + `attempt_no` trên `generation` từ generation ĐẦU TIÊN.** Dữ liệu lịch sử không backfill được; không có nó thì không trả lời được "khách nào lỗ" và không định giá được.
4. **Object storage key `tenant/{tenant_id}/{sha256}`, content-address TRONG phạm vi tenant, KHÔNG dedup chéo tenant.** Điểm tinh tế và đáng nêu: dedup chéo tenant nghe như tiết kiệm nhưng tạo hai vấn đề không sửa được — (a) suy ra được tenant khác có cùng asset (rò rỉ thông tin), (b) hai khách cùng "sở hữu" một ảnh, mà quyền tác giả của ảnh đó lại thuộc về đóng góp sáng tạo của **một** người ⇒ **mâu thuẫn trực tiếp với chính lập luận bản quyền** ở §6.1 và §8.2. Cộng: signed URL có hạn, không bao giờ public bucket.
5. **Kỷ luật `ON DELETE CASCADE` + một đường hard-delete tenant đã kiểm thử.** Takedown và yêu cầu xoá dữ liệu **sẽ** đến (§8.3); FK lỏng thì xoá một tenant biến thành khảo cổ học thủ công, và sót dữ liệu là rủi ro pháp lý.
6. **`usage_event` append-only từ ngày đầu**, billing/metric là hàm tổng hợp trên nó, không phải counter tăng tại chỗ — vì mô hình giá **sẽ** đổi (§9b), và đổi giá mà không có event thô để tính lại là bế tắc.

Kèm bốn hạng mục phải có ở bản trả phí đầu tiên: **hard quota cưỡng chế TRƯỚC khi enqueue** (không phải đếm sau — chi tiết cơ chế hold/reserve ở §9b), per-tenant cost attribution, ToS + user warrant + đường takedown (§8.3), và abuse controls tối thiểu (giới hạn dung lượng/số upload, rate limit per tenant, ghi lại mọi lần provider từ chối vì content policy — tín hiệu abuse sớm gần như miễn phí).

**Hoãn được:** SSO/SAML, team nhiều thành viên có role, custom domain / white-label, multi-region, fine-tune riêng từng tenant, self-serve refund tự động.

**Không sửa thì hỏng thế nào:** retrofit `tenant_id` vào schema đã có dữ liệu thật là một trong những migration đắt nhất tồn tại — phải sửa mọi bảng, mọi query, mọi index, và **không có cách nào xác minh đã sửa hết**. Bỏ sót một chỗ nghĩa là rò rỉ dữ liệu chéo tenant, tức là **sự cố tồn vong** với một SaaS.

---

## 6. Ba thứ nên CẮT (và một thứ KHÔNG được cắt)

### 6.1 Canvas editor §14 — cắt một phần: editor tối thiểu ~20-25%

> ⚠️ Mục này được trình bày như **một cuộc tranh luận có kết luận**, không phải một khuyến nghị đơn. Nó là chỗ mà đáp án gate làm đảo một kết luận đã chốt, và cách nó đảo lại là điều đáng đọc nhất.

**Vòng 1 — `architect` (trước gate): cắt sạch.** Ước lượng canvas editor đúng như §14 mô tả chiếm **50-60% tổng effort** của toàn sản phẩm. Lập luận mạnh nhất, và nó đến từ chính tài liệu: **cả ba tương tác mà §14 nêu ra — `Regenerate`, `Change camera → Low angle`, `Replace character costume` — đều là "sửa một field của spec rồi generate lại". Không cái nào cần canvas.** Canvas chỉ thật sự cần cho *bố trí hình học tự do* — mà đó chính là thứ nên thay bằng template ở MVP. Thêm nữa, yêu cầu "không ảnh hưởng các panel khác" **không phải yêu cầu UI mà là yêu cầu data model**, và schema ở §5.1 đã đảm bảo rồi.

**Vòng 2 — PM phản biện (sau gate): hai lý do.** (a) Với SaaS, **editor chính là sản phẩm** — khách trả tiền cho một trải nghiệm, không cho một CLI. (b) Theo US Copyright Office, *"iterative, interactive process rather than solely relying on prompts"* là cơ chế tạo ra phần **được bảo hộ bản quyền**. Cắt editor khỏi một SaaS = cắt mất cả sản phẩm và cả lá chắn pháp lý.

**Vòng 3 — `architect` phản biện lại, và thắng: "đúng về nghĩa vụ, sai về phương tiện".**

Yêu cầu *"iterative, interactive process"* là yêu cầu về **quyết định sáng tạo của con người có được ghi nhận hay không** — **không** phải yêu cầu về công nghệ render UI. Một canvas editor **không tự sinh ra** tính được bảo hộ; nó chỉ là một cách nhập liệu. Ngược lại, một **form editor có ghi vết đầy đủ cũng thoả**, miễn là nó emit đủ audit event: *người dùng đã chọn generation X thay vì Y*, *đã tự viết/sửa thoại*, *đã đổi camera từ medium sang low-angle*, *đã kéo bubble sang phải*, *đã sửa costume trong Story Bible*.

> **Nghĩa vụ pháp lý đặt lên tầng DỮ LIỆU (audit event), không đặt lên tầng CANVAS.**

Và toàn bộ cơ chế đó `architect` **đã đề xuất từ trước** dưới dạng dữ liệu chứ không phải UI: `generation.origin`, `parent_generation` + `relation_kind`, `field_provenance`, `change_log`. Ràng buộc thiết kế mới sinh ra từ đây là: **mọi hành động của người dùng trong editor phải sinh một `change_log` row — kể cả hành động chỉ là "chọn ảnh này thay vì ảnh kia"**. Nó không đòi canvas.

**⇒ Điều thú vị: phản biện của PM, truy tới cùng, lại CỦNG CỐ việc cắt.** Thứ phải build là **provenance đầy đủ**; còn hình dạng UI vẫn được tự do chọn cái rẻ.

Về nửa còn lại của phản biện (*"editor chính là sản phẩm"*), `architect` nhượng bộ một phần nhưng bác suy luận "phải là canvas", với hai lập luận ngược: (1) **trục cạnh tranh sai** — đối thủ đang thu $9-10/tháng và đã tồn tại; một dev đơn lẻ đua độ mượt editor với các team có funding là chọn trục yếu nhất, còn trục Story Bible + Timeline State + Canonical Reference + Continuity là trục **không ai làm được rẻ** và là trục duy nhất mà quy mô 1 dev có lợi thế (nó là thiết kế dữ liệu, không phải nhân lực UI); (2) **cả 3 tương tác §14 vẫn không cần canvas** — lập luận cũ đứng nguyên, dù người dùng là anh hay là khách trả tiền.

**Kết luận: CẮT MỘT PHẦN. Editor tối thiểu để một SaaS bán được:**

| # | Thành phần | Bắt buộc? | Vì sao | % effort (mẫu số SaaS) |
|---|---|---|---|---|
| 1 | Panel card: form spec + ảnh preview + `Regenerate` + **variant picker** | **CÓ** | Chính là vòng lặp iterative. Variant picker là hành động sáng tạo **rẻ nhất mà giá trị pháp lý cao nhất** (chọn = authorship, ghi được vào `change_log`) | 5-7% |
| 2 | **Bubble/text overlay editor trong phạm vi MỘT panel** (kéo bubble, sửa thoại, chọn kiểu, kéo đuôi trỏ) | **CÓ** — đây là chỗ nhượng bộ | Ba lý do độc lập: thoại do người viết là phần **được bảo hộ**; bubble che mặt là lỗi không thể tự động tránh; không sửa được thoại thì mọi lần sửa chữ thành một lần regenerate ảnh — đốt tiền. Đây là "canvas bị giới hạn" trong một khung, **không** phải scene graph tự do | 5-8% |
| 3 | Page: chọn **template layout**, đổi chỗ / swap panel giữa các ô, reorder | **CÓ** | Sắp đặt panel là quyết định sáng tạo của con người (selection & arrangement). Chỉ cần **rời rạc**, không cần hình học liên tục | 3-4% |
| 4 | Preview trang + chapter render **server-side** (composite PNG/PDF), read-only | **CÓ** | Khách phải thấy thành phẩm mới trả tiền. Rẻ vì tái dùng compositor của export | 3-5% |
| 5 | Story Bible editor (form: character, costume, location, state theo event) | **CÓ** | Đây mới là nơi moat lộ ra với khách hàng. Vẫn là form + list | 4-6% |
| — | **Tổng editor tối thiểu** | | | **~20-25%** |
| 6 | Infinite canvas, zoom/pan cả chapter, hình học panel tự do, panel xoay/không chữ nhật | **HOÃN** | Chi phí lớn nhất, giá trị tăng thêm nhỏ nhất ở bản trả phí đầu | — |
| 7 | Undo/redo xuyên toàn bộ state phân tán | **HOÃN** | Chỉ undo **cục bộ** trong form + vị trí bubble. Không undo qua generation — một `Regenerate` tiêu tiền thật và không hoàn lại được | — |
| 8 | Realtime collaboration | **HOÃN** | 1 user = 1 tenant ở bản đầu | — |
| 9 | Inpainting brush / drawing tools | **HOÃN** | Cần nhưng không phải để bán được bản đầu. Khi làm thì phải set `generation.origin='ai_edited'` | — |

**Hai ước lượng %, hai mẫu số khác nhau — không so trực tiếp.** §14 đầy đủ ≈ **50-60% mẫu số công cụ cá nhân** (không có multi-tenancy, billing, auth, moderation). Editor tối thiểu ≈ **20-25% mẫu số SaaS** (đã bao gồm khối multi-tenancy ở §5.7). Không được trừ hai số đó cho nhau. Nhưng kết luận hành động không đổi, và câu chốt của `architect` là câu đúng để dẫn: **vẫn tiết kiệm được khoảng một nửa effort của hạng mục đắt nhất** — và phần tiết kiệm đó chính là ngân sách để làm khối multi-tenancy, thứ vốn không có trong kế hoạch cũ.

**Đường nâng cấp không mất mát:** giữ layout dưới dạng **toạ độ chuẩn hoá 0-1** trong `page_layout JSONB` (bubble cũng vậy) ngay từ MVP; template chỉ là các preset ghi vào **cùng** schema đó. Khi (nếu) lên canvas thật bằng thư viện có sẵn — `tldraw` / `konva` / `fabric.js`, cần một spike riêng để chọn — thì **không phải migrate dữ liệu**, chỉ thay lớp tương tác. **Không viết renderer từ đầu.**

**Không cắt thì hỏng thế nào:** canvas editor là **software engineering thuần, khó thật, và không AI nào viết hộ được phần khó** (state machine, perf với hàng trăm ảnh, undo trên side-effect không hoàn lại, race khi user sửa spec trong lúc generation đang bay). Một dev đơn lẻ chọn build canvas editor trước là **gần như chắc chắn không bao giờ tới được phần AI**.

### 6.2 Microservices + Vector DB §12 — cắt, và lý do MẠNH LÊN dưới SaaS

**Kết luận: cắt, và khuyến nghị monolith MẠNH LÊN sau gate, không yếu đi.**

**Lý do cũ (vẫn đúng):** với 1 dev, 3 service + 2 PostgreSQL + Vector DB riêng + Job Queue riêng là over-engineering rõ ràng. Nặng nhất: **hai database = mất transaction** — Story ở DB1, Comic ở DB2, nhưng panel phải tham chiếu `character_id` và `event_id` ⇒ không FK, không join, không ACID, phải tự viết eventual consistency/saga. Đây chính là **thứ dữ liệu ràng buộc chặt nhất của hệ** bị cắt làm hai. Và không có lý do vận hành nào biện minh: microservices trả cho scale độc lập + team độc lập; team độc lập không tồn tại, còn bottleneck thật là quota/GPU phía provider, không phải CPU service của mình. Ước lượng: đi theo §12 nguyên bản làm chậm thời gian tới sản phẩm chạy được khoảng **2-3 lần**.

**Ba lý do mới, mạnh hơn lý do cũ, và một trong đó ở mức pháp lý:**

1. **Multi-tenancy làm việc tách 2 DB TỆ HƠN, không trung tính.** State resolution (§5.1) là truy vấn **xuyên** Story ↔ Comic. Với hai DB thì nó thành **join phía ứng dụng**, mà **RLS không bảo vệ được join phía ứng dụng** ⇒ lớp phòng thủ thứ hai biến mất đúng ở **đường dẫn dữ liệu nóng nhất**. Đây là lập luận đủ mạnh để một mình nó loại bỏ việc tách DB.
2. **Nghĩa vụ audit đòi một transaction boundary.** Bản ghi audit và artifact nó chứng minh **phải commit cùng nhau**: `INSERT generation` + `INSERT change_log` + `INSERT usage_event` trong **một** transaction, bất khả phân. Hai DB thì audit có thể mất độc lập với thứ nó audit — tức là audit trail **không đáng tin về mặt pháp lý**. Câu đáng ghim: **bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng.**
3. **Ngân sách effort đã bị khối multi-tenancy ăn mất 15-25%** (§5.7). Effort đó phải lấy từ đâu đó; lấy từ hạ tầng phân tán là lựa chọn hiển nhiên đúng.

**Thay bằng gì:** modular monolith — **1 process, module boundary bằng package + interface** (không HTTP nội bộ); **1 PostgreSQL, 3 schema** (`story`, `comic`, `generation`) — tách sẵn để sau này split bằng dump-restore; **queue nằm trong Postgres** (`SELECT ... FOR UPDATE SKIP LOCKED`), lợi thế kỹ thuật thật là **transactional enqueue** — `INSERT generation` + `INSERT job` trong một transaction ⇒ không bao giờ có job mồ côi; **Object Storage tách khỏi DB từ ngày đầu** (không bao giờ lưu ảnh blob trong Postgres); **WebSocket → polling 2s** (generation mất hàng chục giây, polling là quá đủ).

**Vector DB: bỏ hẳn khỏi MVP.** Tài liệu vẽ Vector DB dưới Story Service nhưng **không nói nó làm gì**. Với các use case hợp lý (semantic retrieval trên văn bản, entity resolution) thì `pgvector` là đủ tuyệt đối ở quy mô này (100 chapter × ~3000 từ → cỡ 20-50k chunk). Còn rẻ hơn nữa: **Story Bible _là_ index của mình** — nhân vật, địa điểm, event đều có ID và quan hệ tường minh trong SQL; truy vấn "mọi event có Lâm Phong ở Imperial Palace trước Ch17" là một câu SQL, **chính xác hơn** vector search. Cộng PostgreSQL full-text search cho tra cứu văn bản. Thêm `pgvector` khi có bằng chứng cụ thể là SQL + FTS không đủ. Không có gì trong mô hình SaaS làm nó cần thiết sớm hơn.

**Năm seam ĐÚNG chỗ — giữ, vì chúng miễn phí trong monolith:** (1) `Generation` sau một async job interface `enqueue(spec) → job_id → poll` — đây là seam đúng nhất trong §12; (2) Object Storage content-addressed tách khỏi DB; (3) module interface `story` / `comic` / `generation` với luật `comic` gọi `story` qua **duy nhất** `resolveState()` và `getBible()`, enforce bằng lint rule cấm import chéo; (4) adapter per image provider; (5) Visual Prompt Compiler là library thuần, module riêng, không lẫn vào adapter.

**Và một khái niệm mới sau gate: seam KINH TẾ khác seam kỹ thuật.** Không phải tách để chia code cho gọn, mà tách để scale theo tải khách hàng:

| Seam kinh tế | Chuẩn bị gì ngay | Vì sao là kinh tế |
|---|---|---|
| **Generation worker là process triển khai riêng, CÙNG codebase** | Hai entrypoint (`api`, `worker`) trên cùng repo/image, khác command. Chi phí ~0 | Tải generation biến thiên theo hành vi khách, không theo traffic API. Cần worker chết mà **API vẫn sống** — khách vẫn sửa spec, vẫn xem trang ⇒ vẫn thấy sản phẩm hoạt động ⇒ không churn |
| **Fairness per tenant trong câu CLAIM job** | Ngay trong câu `FOR UPDATE SKIP LOCKED` phải có `in_flight_per_tenant < N` | Noisy neighbour: một khách batch cả bộ truyện làm mọi khách khác chờ → churn của người vô can. Nhồi fairness vào **sau** là sửa lại đúng câu SQL nóng nhất, rất dễ sinh deadlock |
| **`usage_event` append-only** thay vì counter tăng tại chỗ | Bảng event thô, billing là hàm tổng hợp | Mô hình giá **chắc chắn** phải đổi (§9b). Có event thô thì đổi giá là viết lại query; chỉ có counter thì là mất dữ liệu vĩnh viễn |

Không đổi: **không** tách Story/Comic thành service.

### 6.3 Layout Score số thực — cắt

Cắt **cơ chế 5 số thực**, giữ **mục tiêu** (layout theo narrative importance). Lập luận đầy đủ, bằng chứng tự tố (`dialogue density 0.20`), và phương án thay thế cụ thể (rubric `beat_type` + bảng tra deterministic + emphasis quota theo chapter) đã trình bày ở **§5.3** — không nhắc lại ở đây.

Nói ngắn về lý do nó thuộc danh sách cắt chứ không chỉ danh sách sửa: đây là hạng mục mà `researcher` xếp ⚪ *không tìm được prior art*, và `senior-ai-engineer` phân định là **"chưa ai làm vì không đáng"**. Một hạng mục không có prior art, không kiểm chứng được là đúng hay sai, và có phương án thay thế rẻ hơn cả chục lần với chất lượng cao hơn ở MVP — đó là định nghĩa của thứ nên cắt sớm.

Ứng viên cắt bổ sung cùng loại, nếu cần cắt sâu hơn: **UI duyệt cây generation** (flat list theo `created_at` + `approved_generation_id` là đủ 95% giá trị — nhưng giữ **cột** `parent_generation_id`, xem §6.4), và **expression sheet đầy đủ mỗi nhân vật** (bắt đầu 3 góc + 3 biểu cảm).

### 6.4 `parent_generation` — KHÔNG cắt. PM tự thu hồi khuyến nghị của mình

> ⚠️ Mục này được viết như một **sự tự thu hồi công khai**. Nó là dấu vết quyết định, không phải một khuyến nghị.

**Khuyến nghị ban đầu của lens PM — và nó SAI.** Trong `findings/product-manager-pm-lens.md` mục 5, PM viết về `Generation` lineage (§13): *"Giữ **tối giản** — log prompt/model/seed/refs. **Bỏ cây `parent_generation` ở MVP**."* Lập luận lúc đó là scope: với 1 dev, cây lineage nghe như hạng mục có thể hoãn.

**Vì sao nó sai.** `researcher` tra ra **Nghị định 134/2026/NĐ-CP**, ban hành 06/04/2026, **hiệu lực 09/04/2026**, sửa đổi/bổ sung Nghị định 17/2023/NĐ-CP hướng dẫn Luật SHTT. Theo **Điều 5a**, tác phẩm AI-assisted chỉ được bảo hộ nếu con người có *"substantial and decisive intellectual contribution to the creative process"*, có meaningful control lên output; tác phẩm **do AI tạo hoàn toàn: KHÔNG được bảo hộ**. Và kèm theo là một **nghĩa vụ lưu trữ**: phải **lưu giữ prompts, inputs, intermediate drafts** cùng tài liệu chứng minh human contribution, và **truthfully disclose** việc dùng AI khi cơ quan có thẩm quyền yêu cầu. Nguồn: [Baker McKenzie](https://www.bakermckenzie.com/en/insight/publications/2026/05/vietnam-redefining-copyright-for-ai), [Mondaq](https://www.mondaq.com/copyright/1796822/vietnam-copyright-framework-critical-changes-under-decree-1342026), [Cục Bản quyền tác giả](https://cov.gov.vn/tin-tuc/gioi-thieu-nghi-dinh-so-1342026ndcp-quy-dinh-ve-quyen-tac-gia-quyen-lien-quan-168925.html).

⇒ Bảng `Generation` ở §13 — mà tác giả thiết kế cho **reproducibility/debug** — **chính là hồ sơ pháp lý bắt buộc** để chứng minh human contribution ở Việt Nam. Một feature engineering hoá ra là compliance artifact. **Khuyến nghị "bỏ `parent_generation` ở MVP" bị thu hồi.**

**Đây là lý do fan-out cần một lens có web access.** Nghị định này hiệu lực 09/04/2026 — **sau knowledge cutoff**, PM không thể tự biết. Đây là lần thứ nhất trong run mà lens có web access đảo một kết luận đã chốt; lần thứ hai là Luật TTNT 2025 ở §8.4. Không có lens đó, tài liệu này sẽ khuyên anh cắt đúng thứ mà luật bắt phải giữ.

**Và nó không chỉ "giữ nguyên" — nó phải MẠNH LÊN dưới mô hình SaaS.** Với multi-tenant, audit trail còn là bằng chứng phục vụ **khách hàng của anh** chứng minh quyền của họ, không chỉ của anh. Cụ thể phải làm:

1. **Giữ cột `parent_generation_id` (nullable FK)** — một cột, và thêm sau thì **mất dữ liệu quá khứ**. Cộng `relation_kind ENUM('retry','variation','refine','continuity_fix')`, vì `parent_generation` đang gánh ba ngữ nghĩa khác nhau bị gộp làm một. Một cột enum, gần như miễn phí.
2. **Lưu cả các bước human edit và quyết định chọn/loại** — `researcher` nhấn mạnh điểm này: **prompt một mình không chứng minh được "decisive contribution"**. Cái chứng minh được là *người đã chọn generation X thay vì Y*, *đã sửa thoại*, *đã đổi camera*, *đã kéo bubble*. ⇒ `change_log` ghi **mọi** hành động người dùng, `generation.origin ENUM('ai','ai_edited','human')`, `field_provenance` ở mức field. Đây cũng chính là cơ chế làm cho §6.1 (cắt canvas) hợp pháp.
3. **Vẫn được cắt UI duyệt cây.** Nghĩa vụ nằm ở **dữ liệu**, không ở giao diện: flat list theo `created_at` + `approved_generation_id` là đủ ở MVP. Đừng build tree view / diff view / branch-merge — đó là nơi effort bốc hơi.
4. **Cùng một transaction với artifact nó chứng minh** (§6.2 lý do 2).

**Điều chỉnh cách diễn đạt, không phải cách làm:** với closed API, mục tiêu đúng của `Generation` **không phải reproducibility mà là AUDITABILITY + LINEAGE** — trả lời được "ảnh này sinh ra từ spec nào, ref nào (hash gì), tham số gì, tốn bao nhiêu, ai approve". Cái đó **đạt được 100%** và đủ để chạy sản phẩm; còn reproducibility bit-exact thì không đạt được vì nhiều API không cho set seed, và provider cập nhật weights dưới cùng một tên model (silent model drift). `seed` là **provenance metadata**, không phải replay key. Hai lens đến kết luận này độc lập — `architect` bằng lập luận kỹ thuật thuần, `researcher` bằng văn bản pháp luật — và lens có web access giải thích được *vì sao* điều đó quan trọng.

**Không giữ thì hỏng thế nào:** tác phẩm của anh (và của khách hàng anh) **không được bảo hộ bản quyền ở Việt Nam**, vì không có hồ sơ chứng minh đóng góp của con người. Và dữ liệu đó không backfill được — không lưu từ generation đầu tiên thì vĩnh viễn không có.

---

## 7. Phản biện luận điểm "moat"

Tác giả kết luận `Request.md` bằng câu: *"cái giúp nó không loạn nhân vật chính là Story Bible + Timeline State + Canonical References + Visual Prompt Compiler + Continuity Checker. Đây mới là moat của sản phẩm, chứ không phải bản thân việc gọi image model."*

**Nửa đầu đúng và sắc.** Việc gọi image model là commodity — ai cũng gọi được, và giá đang giảm. Nhận ra điều đó trước khi build là dấu hiệu tư duy hệ thống tốt.

**Nửa sau — gọi 5 thành phần đó là _moat_ — sai, và ba lens bác bỏ nó bằng ba lý do khác nhau.**

Cần phân biệt hai khái niệm hay bị gộp: **barrier to entry** là thứ làm việc bắt chước *tốn công*; **moat** là lợi thế *tự củng cố theo thời gian* — càng dùng càng khó vượt.

| Thành phần | Khó làm? | Đối thủ khó copy? | Là moat? |
|---|---|---|---|
| Story Bible (schema) | Không — là data model, viết ra được trong một tuần | Không | ❌ |
| Timeline State | Trung bình | Không — công khai trong chính tài liệu này | ❌ |
| Canonical References | Không | Không | ❌ |
| Visual Prompt Compiler | Trung bình | Không | ❌ |
| Continuity Checker | **Có** | Trung bình | ⚠️ Có thể |

**Ba lý do bác bỏ, từ ba lens độc lập:**

1. **`researcher` — concept đã public.** CANVAS (arXiv 2604.13452, 15/04/2026) đã implement gần đúng cả năm thành phần và đo được kết quả. Ai đọc arXiv cũng dùng được. Một kiến trúc đã xuất bản không thể là moat.
2. **`senior-ai-engineer` — nghịch lý moat.** Thành phần duy nhất có khả năng là moat (Continuity Checker) lại là thành phần **ít được kiểm chứng nhất**, và ở dạng §15 mô tả thì nó tạo giá trị âm (§5.2). Tài liệu đặt cược vào đúng ô yếu nhất của bàn.
3. **Lens product — barrier ≠ moat.** Năm thành phần là rào cản gia nhập, không phải lợi thế tự củng cố. Barrier chỉ mua **thời gian**; moat mua **vị thế**.

**Moat thật, nếu có, nằm ở ba chỗ — và cả ba đều KHÔNG được nhắc trong `Request.md`:**

1. ⭐ **Dữ liệu preference tích luỹ.** Mỗi lần người dùng chọn generation này thay vì generation kia, sửa một panel, chấp nhận hay từ chối một cảnh báo continuity — đó là **một nhãn preference**. Sau hàng chục nghìn nhãn, hệ thống biết đạo diễn thế nào cho vừa mắt người đọc, và **đối thủ mới không có dữ liệu đó**. Đây là moat thật, nó **tự củng cố**, và nó gần như **miễn phí** — chỉ cần thiết kế để ghi lại từ ngày đầu.

   Dưới mô hình SaaS multi-tenant, moat này **mạnh lên một bậc**: preference data đến từ *nhiều* tác giả, không phải một. Nó chuyển từ "đáng làm" sang **lý do tồn tại của sản phẩm**. Và nó dùng chung đúng cơ chế mà §6.4 buộc phải có vì lý do pháp lý (`change_log` + `generation.origin`) — tức là **một khoản đầu tư trả hai lần**.

   ⚠️ **Bỏ qua ở MVP1 thì không lấy lại được.** Dữ liệu không sinh ra thì không backfill được.

2. **Switching cost qua Story Bible.** Một tác giả đã xây Story Bible cho truyện 300 chapter thì không muốn làm lại ở nơi khác — với điều kiện Story Bible đủ giá trị và không export dễ.

3. **Thư viện style/character đã lock** — cùng cơ chế.

**Và phải nêu cả rủi ro ngược, không chỉ nhánh lạc quan.** `researcher` chỉ ra một điều đáng lo: **hai nửa của ý tưởng đều đã có công ty làm, nhưng chưa ai ghép chúng lại.**

- Nửa *Story Bible + timeline state + continuity check*: **đã có** — nhưng ở ngành **viết novel**, không phải comic. Sudowrite ship *"entries tagged by timeline... character states per era"*; Novilot bắt *"a character whose eyes change color"* và timeline contradictions; ProseWeave inject Story Bible vào mọi AI operation.
- Nửa *comic generation*: **đã có** — nhưng state management rất nông. ComicInk là sản phẩm sâu nhất tìm được, và nó dùng *"story so far"* = **summary văn xuôi**, không phải structured state, cộng cap **20 nhân vật / 12 issues**.

Hai cách đọc, và không thể loại bỏ cách nào:

- **Cơ hội thật**: ComicInk cap 12 issues là hạn chế do **thiếu kiến trúc state**, không do thiếu nhu cầu — truyện Trung Quốc/web novel thường 500-2000 chương. Khoảng cách research → product đang mở.
- **Dấu hiệu xấu**: không ai ghép, dù cả hai nửa đều có công ty làm. Có thể vì **người dùng thực tế không cần adapt 100 chương** — họ cần 10 trang cho social media. Cap 12 issues của ComicInk có thể là quyết định **product**, không phải quyết định kỹ thuật. ROI của Story Bible tăng theo độ dài truyện, còn thị trường AI comic đang tập trung ở **đầu ngắn**.

⇒ **Rủi ro thật cần ghi nhận: over-engineering cho một use case (100+ chương) mà thị trường chưa chứng minh.** Moat "switching cost qua Story Bible" chỉ có giá trị **nếu có người muốn đi tới chương 50**. Đó là một giả định chưa được kiểm, và nó đứng ngay dưới nền của cả sản phẩm.

Thêm một dữ liệu lạnh: **Comicpad đóng cửa 01/09/2026** — chín ngày sau ngày viết tài liệu này (§11). Nó ủng hộ nhánh phản biện, không ủng hộ nhánh lạc quan.

---

## 8. Rủi ro pháp lý & compliance

### 8.1 Ba lớp, và nửa nào có đường đi / nửa nào chặn ở cửa luật sư

Lens product xếp rủi ro pháp lý là **rủi ro số 1, trên cả rủi ro kỹ thuật**. Lập luận: mọi rủi ro kỹ thuật trong tài liệu là *rủi ro về mức độ* (làm được tới đâu, tốn bao nhiêu) — chúng làm sản phẩm **kém hơn**. Rủi ro pháp lý là *rủi ro nhị phân* — nó làm sản phẩm **không tồn tại được**. Một rủi ro nhị phân chưa kiểm luôn phải xếp trên một rủi ro liên tục.

Sau vòng delta, rủi ro này **tách thành hai nửa có tính chất khác nhau** — và phải trình bày riêng, không gộp:

| Nửa | Câu hỏi | Trạng thái |
|---|---|---|
| **Nửa A — "user có quyền với truyện không?"** | Nếu user upload truyện họ không có quyền, nền tảng chịu gì? | 🟢 **HẠ CẤP.** Có safe harbour thật (Điều 198b), và điều kiện hưởng nó là **việc build được** — checklist ở §8.3 |
| **Nửa B — "extraction thương mại có hợp pháp không?"** | Nền tảng **thương mại** chạy LLM extraction trên văn bản có bản quyền — có rơi vào giới hạn *"non-commercial"* của Điều 37a? | 🔴 **GIỮ NGUYÊN MỨC NHỊ PHÂN.** Không ai tra ra được, và nó quyết định tính hợp pháp của **chính hoạt động lõi** |

**Ba lớp rủi ro, chi tiết:**

**Lớp 1 — Bản quyền truyện gốc (input).** Comic adaptation của novel là **derivative work** rõ ràng: *"Only the owner of copyright in a work has the right to prepare, or to authorize someone else to create, an adaptation of that work"* — ví dụ derivative work chính thức của US Copyright Office gồm *translation, fictionalization, motion picture adaptations, art reproduction, abridgement*; comic adaptation rơi đúng nhóm này ([Copyright.gov Circular 14](https://www.copyright.gov/circs/circ14.pdf), [Kirkland IP Primer for Comic Book Creators](https://www.kirkland.com/-/media/content/kirkland-ip-primer-for-comic-book-creators.pdf)).

Anh đã chốt nhánh **nền tảng cho user tự upload** ⇒ rủi ro sơ cấp **chuyển sang user**, và đây là nhánh dễ sống nhất về pháp lý trong ba nhánh. Nhưng nền tảng phát sinh nghĩa vụ riêng: điều khoản buộc user cam kết có quyền, cơ chế takedown, và câu hỏi Nửa B.

**Lớp 2 — Bản quyền ảnh AI (output).** Xem §8.2 — đây là tin tốt, và nó bị đọc sai phổ biến.

**Lớp 3 — Điều khoản của model provider.** **Gemini API cho phép commercial use**; Google không claim ownership ảnh bạn tạo, không thu royalty; phải tuân Acceptable Use Policy ([ai.google.dev/gemini-api/terms](https://ai.google.dev/gemini-api/terms)). Nano Banana Pro **đã nhúng SynthID watermark** trên output — hữu ích cho compliance (§8.4), nhưng cần biết là output mang provenance signal. ⚠️ Điều khoản về upload ảnh tham chiếu người thật / nhân vật có bản quyền: **không tìm được quy định rõ ràng**. Rủi ro thực tế thấp trong use case này vì reference images là nhân vật **do chính hệ thống generate** (canonical portrait), không phải người thật — nhưng đây là câu cần đọc AUP + Prohibited Use Policy trực tiếp trước khi build.

### 8.2 Zarya of the Dawn — tin tốt bị đọc sai

**Tiền lệ trực tiếp nhất, và nó đúng là một comic.** US Copyright Office ban đầu cấp registration cho graphic novel 18 trang *Zarya of the Dawn* của Kristina Kashtanova (ảnh từ Midjourney), sau đó **partially cancel** vì non-human authorship.

Phần bị đọc sai: **text và "selection, coordination, and arrangement" của các thành phần văn bản + hình ảnh VẪN được bảo hộ.** Office kết luận *"an arrangement of AI-generated images with human-authored text in a comic book"* là một **copyrightable compilation**. Guidance 2026 tái xác nhận: *"a sufficiently creative selection, arrangement, or modification of AI output may be copyrightable"*, và Office **có xét tới** các AI tool cho phép user control output *"through an iterative, interactive process rather than solely relying on prompts"*.

Nguồn: [copyright.gov/ai](https://www.copyright.gov/ai/), [AI policy guidance PDF](https://www.copyright.gov/ai/ai_policy_guidance.pdf), [Sidley Austin](https://www.sidley.com/en/insights/newsupdates/2025/02/us-copyright-office-issues-report-on-artificial-intelligence-and-copyrightability), [Harvard JOLT — Zarya digest](https://jolt.law.harvard.edu/digest/zarya-of-the-dawn-how-ai-is-changing-the-landscape-of-copyright-protection).

⭐ **Vì sao đây là tin tốt lớn cho comic-studio:** panel layout, page composition, script, dialogue, panel ordering — tức là **chính xác cái mà Comic IR + Layout Director của `Request.md` sản xuất** — là phần **được bảo hộ**. Ảnh raw thì không.

⇒ Kiến trúc *"spec là dữ liệu chính, ảnh chỉ là output/cache"* (kết luận cuối `Request.md`) **trùng khớp với đường ranh pháp lý**. Đây là lần thứ nhất trong tài liệu này mà quyết định kiến trúc đó tự chứng minh giá trị; lần thứ hai ở §9b.3.

Hệ quả hành động: đầu tư vào **spec, layout, và text do người viết** không chỉ là đầu tư kỹ thuật mà là đầu tư vào phần **tài sản có thể sở hữu được**. Và nó là lý do §5.4 (typeset layer riêng) có lý do thứ ba, độc lập với chất lượng render.

### 8.3 Safe harbour Điều 198b — checklist build được

Đây là phát hiện hữu dụng nhất của vòng delta: rủi ro Nửa A chuyển từ *nhị phân không kiểm soát được* sang *có checklist build được*.

**Điều 198b Luật SHTT** (sửa đổi 2022, Luật 07/2022/QH15) — miễn trừ trách nhiệm cho **doanh nghiệp cung cấp dịch vụ trung gian**, chuyển hoá từ **Điều 12.55 EVFTA**, bao ít nhất mere conduit / caching / **hosting**. Điều kiện với hosting — **có điều kiện, không tự động**:

- (a) **không biết** nội dung đó xâm phạm quyền;
- (b) **hành động kịp thời** xoá hoặc ngăn truy cập khi biết.

Nguồn: [Lexology — Safe Harbor under 2022 IP Law of Vietnam](https://www.lexology.com/library/detail.aspx?g=d865aa00-fd06-41ab-bde8-cd2f4f604cc1), [KENFOX — Notice and takedown regime](https://kenfoxlaw.com/notice-and-takedown-regime-against-online-ipr-infringement-in-vietnam).

**Nghĩa vụ notice-and-takedown cụ thể** (NĐ 17/2023 + NĐ 134/2026): OSP cung cấp dịch vụ hosting phải lập **công cụ tiếp nhận** yêu cầu xoá/ngăn truy cập — có thể là **chương trình máy tính, email, hoặc cổng thông tin điện tử**; phải **thông báo đầu mối liên hệ (email + số điện thoại) cho Bộ Văn hoá, Thể thao và Du lịch**; thời hạn là quy trình kép **"72 giờ và 10 ngày làm việc"** + **"24 giờ"** (livestream). NĐ 134 **mở rộng** định nghĩa ISP để gồm *"online social networks, e-commerce platforms, and other intermediary digital platforms"*, và **việc tuân thủ các nghĩa vụ này liên quan tới khả năng được hưởng miễn trừ Điều 198b**.

Nguồn: [Rouse](https://rouse.com/insights/news/2023/intermediary-service-providers-liabilities-under-the-amended-ip-law-and-decree-on-copyright), [Lexology — Notice and Takedown Process](https://www.lexology.com/library/detail.aspx?g=c0985dc4-1cfe-41c6-8050-fb169a701c58), [Tilleke & Gibbins](https://www.tilleke.com/insights/new-decree-guides-vietnams-ip-law-in-relation-to-copyright-and-related-rights/2/).

**Checklist đủ điều kiện — rẻ, thuộc MVP, làm sớm:**

| # | Việc | Chi tiết kỹ thuật |
|---|---|---|
| 1 | **Công cụ tiếp nhận takedown** | Có thể chỉ là một form + email `copyright@` — luật cho phép "email hoặc cổng thông tin" |
| 2 | **Đăng ký đầu mối với Bộ VHTTDL** | Email + số điện thoại |
| 3 | **SLA 72 giờ** | **Soft-delete + disable-access ở cấp project**, không hard delete — còn phải giữ dữ liệu cho counter-notice. Đây là lý do §5.7 mục 5 đòi một đường hard-delete *đã kiểm thử* tách biệt |
| 4 | ⚠️ **KHÔNG chủ động rà soát nội dung để "biết"** | Xem cảnh báo dưới |
| 5 | **User warrant + indemnify trong ToS** | Xem mẫu ngành dưới |
| 6 | **Kiểm opt-out signal của file upload trước khi xử lý** | Xem dưới — chi phí ~0, xoá được một nhánh rủi ro |

**Về item 6 — Điều 37b (opt-out), việc rẻ nhất trong cả bản phân tích này.** NĐ 134/2026 Điều 37b cho tác giả **bảo lưu quyền** qua bốn kênh: metadata, biện pháp bảo vệ công nghệ, **thông tin quản lý quyền dạng máy đọc** (machine-readable rights-management information), hoặc thông báo công khai từ tổ chức quản lý tập thể.

Lập luận điều kiện — nêu rõ để anh thấy nó phòng cho tình huống nào: nếu Điều 37a **không** áp cho comic-studio (§8.2 lập luận rằng extraction ≠ training) thì 37b cũng không áp, và bước kiểm này là dư. **Nhưng nếu** cơ quan chức năng coi extraction là TDM, nền tảng **phải** kiểm machine-readable opt-out signal **trước khi** xử lý — và lúc đó việc không có bước kiểm là một vi phạm đã xảy ra hàng nghìn lần, không sửa hồi tố được.

⇒ **Thêm một bước trong pipeline ingest: đọc metadata / rights-management-info của file user upload, log kết quả kèm timestamp, chặn nếu có signal bảo lưu.** Chi phí xây gần bằng 0, chi phí chạy bằng 0, và nó xoá hẳn một nhánh rủi ro pháp lý thay vì làm nhỏ nhánh đó. Đây là loại đánh đổi không cần cân: **làm, kể cả khi tin rằng 37a không áp.**

> [!NOTE]
> Bước này **không** xung đột với nghịch lý safe harbour ở dưới. Hai việc khác bản chất: kiểm opt-out signal là đọc **tuyên bố tường minh do chính chủ quyền gắn vào file** — một dữ kiện khách quan; còn thứ phá miễn trừ Điều 198b là **tự suy đoán** rằng "truyện này *có thể* có bản quyền của người khác". Đọc nhãn không tạo ra tri thức suy đoán.

> ⚠️ **Nghịch lý safe harbour — điểm phản trực giác nhất của cả bản phân tích này.**
> Điều kiện miễn trừ (a) là **"không biết"**. Nghĩa là **xây một bộ phát hiện "truyện này có thể có bản quyền" có thể PHÁ chính miễn trừ của mình** — vì nó tạo ra tri thức mà luật đang miễn trừ cho việc không có.
> Một dev sẽ làm ngược điều này theo bản năng, vì "chủ động kiểm tra" nghe như hành vi có trách nhiệm. **Cần luật sư xác nhận trước khi build feature "cảnh báo truyện có thể có bản quyền".**

**Ba pattern ToS nhất quán trong ngành, nên copy:**

1. **User warrant + indemnify** — phòng tuyến hợp đồng số 1, **mọi** đối thủ đều có. ComicInk buộc user *indemnify, defend, hold harmless*; myComics.ai buộc user *assume full liability* cho mọi claim từ việc tạo, dùng, xuất bản, chia sẻ.
2. **Assign toàn bộ quyền output cho user + disclaimer về tính bất định pháp lý theo jurisdiction.** ComicInk làm chính xác điều này — vừa hào phóng vừa tự bảo vệ: *"the legal status of AI-generated content may vary by jurisdiction"*.
3. **DMCA designated agent đăng ký với US Copyright Office** nếu nhắm thị trường Mỹ — livecomics.to đã làm.

Nguồn: [comicink.ai/terms](https://www.comicink.ai/terms), [mycomics.ai/terms](https://mycomics.ai/terms/), [comicai.com/terms-of-service](https://comicai.com/terms-of-service), [livecomics.to/terms](https://livecomics.to/terms).

⚠️ **Hai khoảng trống trong lớp này:** (a) một SaaS **xử lý** nội dung (không phải hosting thuần) có được coi là "hosting service" theo NĐ 17 không — NĐ 17 chỉ nói rõ về *"lưu trữ nội dung số theo yêu cầu"*; (b) DMCA §512(c) vốn dành cho *"storage at the direction of a user"* — có phủ cả việc nền tảng chủ động chạy LLM **biến đổi** nội dung đó không. Cả hai cùng một cấu trúc: **hosting thuần có safe harbour rõ; "hosting + processing" là vùng chưa test.** Cả hai vào §8.5.

### 8.4 Luật TTNT 2025 — nghĩa vụ nội địa VN, deadline ~01/03/2027

⭐ **Đây là phát hiện mà lens product không thể tự biết** (hiệu lực sau knowledge cutoff), và nó **nâng cấp** rủi ro compliance từ "chuyện của thị trường Hàn Quốc" thành **nghĩa vụ nội địa có deadline cụ thể**.

**LUẬT TRÍ TUỆ NHÂN TẠO 2025 — Luật số 134/2025/QH15.** Quốc hội khoá XV Kỳ họp thứ 10 thông qua **10/12/2025**, **hiệu lực 01/03/2026**. Phạm vi bao gồm *"nghiên cứu, phát triển, cung cấp, triển khai và sử dụng hệ thống trí tuệ nhân tạo... tại Việt Nam"*.

⇒ **Một SaaS comic-studio đặt tại Việt Nam là "nhà cung cấp" và/hoặc "nhà triển khai" hệ thống AI theo luật này.**

| Điều khoản | Nghĩa vụ |
|---|---|
| **Điều 11 (minh bạch)** | Phải có cơ chế để **người dùng nhận biết khi đang tương tác với hệ thống AI** |
| **Khoản 4 Điều 11** | Nội dung AI tạo/chỉnh sửa nhằm **mô phỏng người thật hoặc sự kiện thực tế** phải **gắn nhãn dễ nhận biết**; nhà cung cấp phải bảo đảm nội dung do hệ thống AI tạo ra được **đánh dấu bằng định dạng máy đọc** theo quy định của Chính phủ |
| **Điều 8** | **Đăng ký thử nghiệm có kiểm soát, báo cáo sự cố nghiêm trọng, báo cáo định kỳ** |
| **Điều 8 — chuyển tiếp** | Hệ thống đang tồn tại có **12 tháng** (lĩnh vực ngoài y tế/giáo dục/tài chính) để tuân thủ từ 01/03/2026 ⇒ comic-studio: **deadline ~01/03/2027** |
| **Điều 7 — nghiêm cấm** | Gồm **thu thập dữ liệu trái pháp luật để huấn luyện AI** và **che giấu thông tin minh bạch bắt buộc** |

Nguồn: [thuvienphapluat.vn](https://thuvienphapluat.vn/chinh-sach-phap-luat-moi/vn/ho-tro-phap-luat/chinh-sach-moi/106139/luat-tri-tue-nhan-tao-2025-chinh-thuc-co-hieu-luc), [luatminhkhue.vn](https://luatminhkhue.vn/yeu-cau-bat-buoc-doi-voi-noi-dung-tao-boi-ai-tu-1-3-2026.aspx), [genk.vn 01/03/2026](https://genk.vn/tu-hom-nay-1-3-luat-tri-tue-nhan-tao-co-hieu-luc-noi-dung-ai-tao-ra-phai-co-dau-nhan-biet-165260301185217976.chn), [Sở KHCN Đồng Nai](https://skhcn.dongnai.gov.vn/vi/news/khoa-hoc-va-cong-nghe/luat-tri-tue-nhan-tao-chinh-thuc-co-hieu-luc-tu-thang-3-2026-1000.html).

⚠️ **Bất định về phạm vi, phải nêu rõ chứ không được lấp.** Khoản 4 Điều 11 nói *"mô phỏng người thật hoặc sự kiện thực tế"* — comic với nhân vật **hư cấu** có thể **không** rơi vào phạm vi đó. Nhưng câu tiếp theo của cùng nguồn nói nhà cung cấp phải bảo đảm nội dung AI tạo ra được đánh dấu định dạng máy đọc, **không** giới hạn "mô phỏng người thật". Hai mô tả này **có thể mâu thuẫn về phạm vi**, và **không đọc được nguyên văn điều luật** (thuvienphapluat và luatminhkhue đều trả 403). Vào §8.5.

**Tin thực dụng:** Nano Banana Pro **đã nhúng SynthID** — nếu quy định chấp nhận watermark của model provider thì nghĩa vụ này gần như **tự động thoả**. Phải verify, không giả định.

**Bối cảnh thị trường liên quan** — nghĩa vụ tương tự đã có ở nơi khác: **South Korea AI Basic Act** hiệu lực **22/01/2026**, đầu tiên ở châu Á bắt buộc disclosure với nội dung AI-generated/AI-assisted, cho phép **watermark machine-readable không hiển thị** với webtoon/animation, phạt tới **30 triệu won**, và **áp cho mọi service coi Hàn Quốc là market** — gồm Webtoon, Tapas, Tappytoon ([PetaPixel 29/01/2026](https://petapixel.com/2026/01/29/south-korea-launches-landmark-laws-requiring-labels-on-ai-generated-content/), [The New Publishing Standard](https://thenewpublishingstandard.com/2026/01/28/korea-ai-act-webtoon-creators/), [Anime News Network](https://www.animenewsnetwork.com/news/2026-01-24/south-korea-new-ai-law-raises-questions-for-webtoon-creators-platforms/.233383)).

**Hệ quả kiến trúc, cụ thể:** cần **AI provenance metadata field ở cấp page/panel**, và export path phải **nhúng được machine-readable watermark**. Đây là requirement, không phải nice-to-have. Và pattern rút ra từ backlash (§4.4) trùng hướng: khủng hoảng bùng khi **AI use bị che giấu**, không khi được disclose — *"covert use can corrode brand trust more than disclosure ever could"*. Đề xuất từ ngành là **granular disclosure**: label "AI-assisted backgrounds" nhưng che vùng sensitive.

### 8.5 Ba câu phải hỏi luật sư

Ba câu dưới đây đã được **narrow xuống mức luật sư trả lời được**. Đây là khuyến nghị hành động số 1 của cả tài liệu (§1).

1. **Điều 37a Nghị định 134/2026 có áp cho _inference-time extraction_ trên nội dung do user upload, hay chỉ áp cho _huấn luyện_ model?**

   Bối cảnh để đưa cho luật sư: cả ba điều 37a/37b/37c đóng khung quanh **"huấn luyện"** — phạm vi ghi rõ *"để nghiên cứu khoa học, thử nghiệm, huấn luyện hệ thống trí tuệ nhân tạo"*, và Điều 37c nói *"sử dụng văn bản và dữ liệu để huấn luyện... khi khai thác thương mại phải thực hiện nghĩa vụ trả tiền bản quyền"*. Use case comic-studio **không phải training**: không tạo model mới, không lưu nội dung vào weights, xử lý **theo chỉ dẫn của chính người upload**. Có lập luận mạnh rằng giới hạn *"non-commercial purposes at the point of use"* của Điều 37a **không áp** — nhưng đây là vùng chưa có tiền lệ, và luật so sánh xác nhận nó chưa được test: *"the analysis becomes more complex... particularly regarding whether users have sufficient rights to authorize TDM uses by commercial AI services"* ([DLA Piper/Lexology](https://mse.dlapiper.com/post/102ivrx/training-ai-models-content-copyright-and-the-eu-and-uk-tdm-exceptions), [CMS Law-Now](https://cms-lawnow.com/en/ealerts/2024/10/ai-and-copyright-exploring-exceptions-for-text-and-data-mining)).

2. **Khoản 4 Điều 11 Luật TTNT 2025 — nghĩa vụ đánh dấu định dạng máy đọc áp cho _mọi_ nội dung AI, hay chỉ nội dung _"mô phỏng người thật hoặc sự kiện thực tế"_? Watermark của model provider (SynthID) có thoả nghĩa vụ này không?**

3. **Nền tảng có được coi là "doanh nghiệp cung cấp dịch vụ trung gian" để hưởng miễn trừ Điều 198b không**, khi nó không chỉ *lưu trữ* mà còn *xử lý/biến đổi* nội dung của user? (Câu tương đương ở luật Mỹ: DMCA §512(c) có phủ "hosting + AI processing"?)

**Vì sao ba câu này là ưu tiên số 1:** đây là rủi ro **nhị phân** duy nhất còn lại trong toàn bộ bản phân tích. Mọi rủi ro khác — consistency, chi phí, effort, unit economics — đều là rủi ro *mức độ*: trả lời sai thì sản phẩm **kém hơn hoặc chậm hơn**. Ba câu này trả lời sai thì sản phẩm **bất hợp pháp**. Và chi phí một buổi tư vấn luật sư SHTT thấp hơn nhiều bậc so với chi phí build sai rồi phải dỡ.

---

## 9. Chi phí thật — và đơn vị đo đúng

**Chi phí inference thấp hơn trực giác một bậc độ lớn.** Giá official (8/2026):

| Model | Standard | Batch |
|---|---|---|
| Gemini 3 Pro Image (Nano Banana Pro) 1K/2K | $0.134/ảnh | **$0.067/ảnh** |
| Gemini 3 Pro Image 4K | $0.24/ảnh | $0.12/ảnh |
| Gemini 3 Flash Image 1K | $0.067/ảnh | $0.034/ảnh |
| FLUX.2 [pro] | từ **$0.03** (t2i) / $0.045 (edit) | — |
| FLUX.2 [klein] 4B | $0.014/MP | — |
| FLUX.1 Kontext [pro] | $0.04/ảnh | — |

Nguồn: [ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing), [docs.bfl.ml/quick_start/pricing](https://docs.bfl.ml/quick_start/pricing).

Với **công cụ cá nhân**, 100 chapter (60 ảnh/chapter) ở hệ số 3x tốn khoảng **$1.206** ở Gemini batch, hoặc **~$540** ở FLUX.2 pro. Đó là một khoản chi cá nhân **không phải rào cản** — thấp hơn giá một card RTX 4090.

**Hai chi tiết kiến trúc có giá trị tiền thật:**

- **Batch mode giảm đúng 50%** giá Gemini. Comic generation vốn là async job queue (§12 đã có Job Queue) ⇒ **batch API là fit tự nhiên, phải dùng**, không phải realtime API. Đây là khoản tiết kiệm lớn nhất mà không đánh đổi gì.
- **Self-host thắng về đơn giá thuần nhưng là câu trả lời sai.** RTX 4090 thuê $0.34/hr, FLUX.2 [dev] quantized 12–30s/ảnh ⇒ ~$0.0019/ảnh, rẻ hơn API ~16x. **Nhưng** FLUX.2 [dev] quantized **không phải** model dẫn đầu về multi-reference character consistency — chính năng lực đó là yêu cầu cốt lõi. Self-host tiết kiệm vài trăm đô và **đánh mất đúng thứ khiến project khả thi**. Cộng: 12–30s × 60 ảnh = **12–30 phút GPU time mỗi chapter**, chưa tính retry. ⇒ **API cho main path; self-host chỉ cho LoRA train ($2–5/LoRA), upscale, inpainting. Không mua GPU.**

**Và đây là kết luận quan trọng nhất của mục này: đơn vị đo chi phí đúng của dự án này là GIỜ-NGƯỜI, không phải đô-la.**

**Ba lens độc lập cùng đến kết luận đó, bằng ba đường lập luận không liên quan nhau:**

| Lens | Đường lập luận |
|---|---|
| `researcher` | Chi phí inference thấp bất ngờ ($1.206 cho 100 chapter) ⇒ tiền không phải rào cản |
| `architect` | Phân bổ effort: canvas editor 50-60% + multi-tenancy 15-25% + pipeline lõi 35-45% ⇒ tổng vượt xa năng lực một người |
| `senior-ai-engineer` | HITL gate ở **5 phút/chapter × 100 chapter ≈ 8 giờ** chỉ riêng review, với **một** người — và đó là con số tối thiểu, giả định mọi thứ khác tự động hoàn hảo |

Ba đường khác nhau, một kết luận — mức tin cậy cao nhất mà run này đạt được về bất kỳ điểm nào.

**Hệ quả thiết kế:** đừng tối ưu kiến trúc để giảm chi phí inference. Hãy tối ưu để giảm **thời gian người**: tăng tỉ lệ panel dùng được ngay lần đầu, giảm số quyết định con người phải đưa ra mỗi chapter, và tự động hoá đúng những bước không cần phán đoán (§5.5). Một cải tiến làm giảm 1 phút review mỗi chapter đáng giá hơn một cải tiến làm giảm $1 inference mỗi chapter.

⚠️ **Nhưng toàn bộ mục này chỉ đúng cho mô hình CÔNG CỤ CÁ NHÂN.** Khi chi phí inference trở thành **COGS trên mỗi khách hàng**, kết luận "chi phí không phải rào cản" **đảo chiều hoàn toàn** — xem §9b.

---

## 9b. Unit economics — ràng buộc thiết kế trung tâm của mô hình SaaS

Mục này **không có** trong kế hoạch phân tích ban đầu. Nó chỉ tồn tại vì đáp án gate đổi mô hình từ công cụ cá nhân sang SaaS thương mại. Và nó là chỗ mà câu trả lời cho *"bán được không?"* nằm.

### 9b.1 Hệ số đúng là N=3, không phải 2x — và vì sao

**PM đã tính sai con số này ở lần đầu, và tự sửa. Ghi lại vì sự minh bạch đó làm tăng độ tin cậy của các con số còn lại, không giảm.**

Ở `escalations.md` **E1**, PM dùng hệ số regenerate **2x** làm kịch bản trung tâm — lấy từ cách trình bày tham số hoá 1x/2x/3x của `researcher`, nơi ghi rõ *"không có dữ liệu ngành"*. Vòng delta tra ra con số thật:

> **CANVAS dùng N = 3 candidate mỗi shot.** *"Performance saturates at N=3, providing the best balance between quality and computation."* ([arXiv 2604.13452](https://arxiv.org/html/2604.13452v1))

Ablation của paper: N=1 là baseline thấp nhất mọi metric; N=2 cải thiện vừa phải về character consistency; **N=3 tối ưu**, diminishing returns từ đó; N>3 chủ yếu chỉ cải thiện thêm character consistency, còn background và prop *"largely stable due to memory constraints"*.

**Và điều quan trọng hơn con số: bản chất của nó khác hẳn giả định ban đầu.** PM hiểu 2x là *"generate, nếu lỗi thì generate lại"* — **retry-on-failure**. Thực tế N=3 là **best-of-N**: generate 3 candidate cho **mọi** panel rồi để VLM chọn 1, **mặc định, không có ngoại lệ**. Đó chính là setting để đạt con số `character 4.91/5` mà cả verdict "khả thi" đang dựa vào (§4.3). **Không thể lấy con số chất lượng của N=3 mà tính chi phí của N=2.**

| | PM tính ở E1 (2x) | **Đúng (N=3)** | Lệch |
|---|---|---|---|
| Chi phí/chapter, Gemini 3 Pro batch $0.067 | $8,04 | **$12,06** | **+50%** |
| 100 chapter | ~$804 | **~$1.206** | +50% |

Chưa tính chi phí VLM call để score 3 candidate — `researcher` không tính được vì không biết token cost của prompt QA của CANVAS. ⇒ **$12,06 là sàn, không phải trần.**

**Tin tốt duy nhất trong mục này: 3 là TRẦN, không phải sàn.** Paper nói rõ performance saturate ở N=3 ⇒ không cần N=5 hay N=10. Con số hữu hạn, biết trước, **budget được**. Và mỗi bậc N giảm được là **~33% COGS** — đó là lý do MVP0 phải đo N tối thiểu cho style của anh (§10).

**Bài học phương pháp, ghi lại để không lặp:** PM tính một con số quan trọng từ input mà `researcher` **đã đánh dấu rõ là khoảng trống dữ liệu**, rồi trình bày kết quả như một con số chắc chắn. Đúng ra phải viết *"$8,04 — dựa trên hệ số 2x giả định, chưa có căn cứ"*. Khi input là khoảng trống, output tính từ nó phải mang cùng cảnh báo — nếu không, **khoảng trống bị rửa sạch qua một phép nhân**.

### 9b.2 Bảng chi phí và margin

**Trần giá thị trường, đo được:** ComicInk credit-based **$9.99 / 1.500 credits** (Comic Page = 50 credits ⇒ **$0.333/page**; Creator tier $54.99/12.000 ⇒ $0.229/page), TaleAtelier subscription + coin **$9.99 / $24.99 / $59.99**, Anifusion Creator **$9/mo**. Nguồn: [comicink.ai/pricing](https://www.comicink.ai/pricing), [taleatelier.com](https://taleatelier.com/ai-comic-generator), [aigregator — Anifusion](https://aigregator.com/tools/anifusion).

**Usage thật:** người dùng trung bình generate **42 ảnh/tháng** (tăng từ 27 năm 2024); Midjourney ~50/tháng; 28 ảnh/session, ~23 phút/session ([digitalapplied.com](https://www.digitalapplied.com/blog/ai-image-generation-statistics-2026-data-points), [sqmagazine.co.uk](https://sqmagazine.co.uk/ai-image-generation-statistics/)).

**Margin trên $9.99/tháng:**

| Kịch bản | COGS/tháng | Margin |
|---|---|---|
| 42 ảnh @1x, Gemini batch $0.067 | $2.81 | **+72%** ✅ |
| 42 ảnh @N=3, Gemini batch | $8.44 | **+15%** ⚠️ |
| 42 ảnh @1x, FLUX.2 pro $0.03 | $1.26 | **+87%** ✅ |
| 42 ảnh @N=3, FLUX.2 pro | $3.78 | **+62%** ✅ |
| **1 chapter/tháng (60 ảnh) @N=3, Gemini batch** | **$12.06** | **−21%** ❌ |
| **Power user 3 chapter/tháng @N=3** | **$36.18** | **−262%** ❌❌ |

⇒ **Subscription phẳng $10/tháng sống được ở usage trung bình, CHẾT ở power user.** Và đó chính là lý do **không đối thủ nào dùng subscription phẳng không giới hạn**: ComicInk thuần credit **không hết hạn**, TaleAtelier subscription **+ coin metered**, Dashtoon **cố ý không công bố bảng giá minh bạch** (*"the public pricing story is less transparent than a normal SaaS pricing page"* — [toolworthy.ai](https://www.toolworthy.ai/tool/dashtoon-studio)). Không phải trùng hợp — họ có cùng cấu trúc chi phí và đã tới cùng kết luận.

**Bối cảnh margin ngành, để hiệu chỉnh kỳ vọng:** gross margin AI product trung bình **52%** (ICONIQ 2026, tăng từ 41% năm 2024); Bessemer đo **50–60%** so với **70–90%** của SaaS trưởng thành; inference chiếm **23% doanh thu** ở AI B2B giai đoạn scaling ([saasmag.com](https://www.saasmag.com/ai-cogs-saas-gross-margin-compression/), [softwareseni.com](https://www.softwareseni.com/why-ai-gross-margins-are-so-much-lower-than-saas-and-what-that-means-for-your-business/)).

⚠️ **Và con số đáng lo nhất của cả bản phân tích: gross revenue retention ở AI budget-tier là 23% sau 12 tháng** — giữ lại chưa tới 1 trên 4 đồng doanh thu cohort. Median GRR của AI-native SaaS là 27% (01/2025) → 40% (09/2025); churn tốt tham chiếu là <2%/tháng ([saasultra.com](https://www.saasultra.com/saas-churn-rate-statistics-benchmarks/)).

Với **1 dev, không budget marketing, LTV thấp** ⇒ **subscription tháng là mô hình sai**. Credit pack **không hết hạn** (đúng như ComicInk làm) né được vấn đề này về mặt cấu trúc: doanh thu ghi nhận **trước**, và không có churn theo nghĩa subscription.

### 9b.3 Xung đột M13: tính năng cốt lõi vs margin

> ⭐ **Đây là xung đột sắc nhất của cả run, và nó không phải lỗi của bên nào.**

`researcher` làm ngược từ giá ComicInk ($0.333/page) và thử hai kiến trúc:

| Kiến trúc | COGS/page @1x | COGS/page @N=3 | Margin @1x | Margin @N=3 |
|---|---|---|---|---|
| **1 ảnh/panel** (4 ảnh/page) | $0.268 | **$0.804** | +20% | **−141%** ❌ |
| **1 ảnh/page** (whole-page composition) | $0.067 | **$0.201** | +80% | **+40%** ✅ |

⇒ **ComicInk gần như chắc chắn generate MỘT ảnh cho cả trang, không phải một ảnh mỗi panel.** Không có cách nào bán $0.333/page mà chi $0.804/page. **Đây là phát hiện kiến trúc, không phải phát hiện pricing** — và nó đến từ lens nghiên cứu chứ không phải lens kiến trúc, vì nó được suy ra từ *giá*, không từ *thiết kế*.

Hai bằng chứng bổ trợ: ComicInk *"additional characters beyond the **first five** per issue cost credits"* — khớp chính xác trần *"up to 5 people"* của Nano Banana Pro; TaleAtelier *"up to **six** named characters per project"*. Cả hai đối thủ đã **hard-code trần ~5 nhân vật** vào product, corroborate độc lập cho §5.6.

**Nhưng `Request.md` §14 xây toàn bộ trải nghiệm quanh việc regenerate MỘT panel mà "không ảnh hưởng các panel khác"** — và §6 định nghĩa panel là đơn vị spec.

> **Tính năng làm sản phẩm hay chính là tính năng làm margin âm.**

Per-panel generation cho phép sửa cục bộ — giá trị lớn nhất của §14 — và đồng thời **nhân COGS lên gấp 4** (4 panel/page thay vì 1 ảnh/page). Không thể có cả hai ở cùng một mức giá.

**Ba đường ra, xếp theo mức khuyến nghị:**

1. ⭐ **BYOK — xung đột BIẾN MẤT HOÀN TOÀN**, vì COGS không còn là của anh. Đây là lập luận thứ hai, độc lập, ủng hộ BYOK (§9b.4).
2. **Whole-page mặc định + per-panel là hành động TRẢ PHÍ.** Người dùng thấy giá trị đúng lúc họ *cần* sửa, và trả tiền đúng lúc đó. Khớp mô hình credit của ComicInk.
3. Whole-page thuần — rẻ nhất, nhưng **bỏ mất §14**, tức là bỏ mất lý do sản phẩm tồn tại. **Không khuyến nghị.**

**Và một hệ quả tích cực đáng nêu.** `Panel Specification` (§6) **không mất giá trị** — nó là *spec*, không bắt buộc mỗi panel một lần gọi model. Một page compile được **nhiều panel spec thành MỘT prompt whole-page**. Chính vì spec tách khỏi ảnh mà mình mới **đổi được granularity render mà không đổi data model**.

⇒ **Đây là lần thứ hai quyết định kiến trúc "spec là dữ liệu chính, ảnh chỉ là output/cache" tự chứng minh giá trị** — lần thứ nhất là trùng khớp đường ranh bản quyền Zarya (§8.2). Một quyết định, hai lần trả lãi, ở hai chiều hoàn toàn không liên quan nhau. Đó là dấu hiệu của một abstraction đúng.

### 9b.4 Bốn đường ra, BYOK ở vị trí số 1

**Khuyến nghị: KHÔNG subscription phẳng. Dùng hybrid — flat platform fee thấp + BYOK.**

| Thành phần | Đề xuất | Căn cứ |
|---|---|---|
| **Platform fee** | **$5–15/tháng** cho phần **không đốt inference**: Story Bible editor, Comic IR, layout editor, versioning, export | Phần này có margin SaaS thật (~90%), không bị AI COGS compression |
| **Image generation** | ⭐ **BYOK** — user cắm Gemini/BFL API key của họ | Xoá hoàn toàn rủi ro unit economics; power user không làm mình lỗ; trend 2026 đã xác lập |
| Phương án thay thế | **Credit pack không hết hạn**, ~$0.30–0.35/page (bám ComicInk $0.333) | Có tiền lệ giá; doanh thu ghi trước ⇒ né 23% GRR |
| Phân tầng model | FLUX.2 pro ($0.03) cho tier thấp, Gemini batch ($0.067) cho tier cao | **§16 Visual Prompt Compiler đã hỗ trợ sẵn** — lần đầu abstraction đó chứng minh giá trị **kinh tế**, không chỉ kỹ thuật |
| **Tuyệt đối tránh** | Subscription phẳng unlimited, hoặc free tier kiểu "100 ảnh/ngày" | 60 ảnh @N=3 = $12.06 > $9.99. **Một power user xoá margin của bốn user thường** |
| Ràng buộc product | Hard-code trần ~5 nhân vật/project | ComicInk (5) và TaleAtelier (6) đã làm |
| Kỳ vọng margin | **50–60%**, không phải 80% | ICONIQ 52%, Bessemer 50-60% |

**BYOK có BA căn cứ độc lập — đó là lý do nó ở vị trí số 1:**

1. **23% GRR ở AI budget-tier** ⇒ subscription tháng là mô hình sai cho 1 dev không budget marketing (§9b.2).
2. **Power user ở −262% margin** không chặn được bằng pricing phẳng (§9b.2).
3. **Xung đột M13 biến mất hoàn toàn** dưới BYOK (§9b.3).

Ba lập luận từ ba hướng khác nhau hội tụ về cùng một khuyến nghị. Bối cảnh xác nhận: *"BYOK is quietly rewriting how AI software gets priced in 2026"*; JetBrains đã áp dụng; tool truyền thống markup **300–500%** trong khi BYOK user trả $1–5/tháng API thay vì $20–249/tháng subscription; OpenRouter thu BYOK fee **5%** ([buildmvpfast.com](https://www.buildmvpfast.com/blog/byok-bring-your-own-key-ai-saas-pricing-model-2026), [copilot-alternatives.com](https://copilot-alternatives.com/blog/what-is-byok-ai-coding-tools/)).

⚠️ **Điểm yếu của BYOK, nói thẳng:** friction cao với non-technical user — và đó **đúng là phân khúc mục tiêu** mà `researcher` đánh giá khả năng cao nhất (tác giả web novel tự sở hữu IP). Nguồn ngành xác nhận BYOK cho non-technical buyer vẫn là **ngoại lệ** ([dmchamp.com](https://dmchamp.com/best/best-ai-tools-byok-2026/)). ⇒ **Nếu chọn BYOK, onboarding flow là rủi ro sản phẩm số 1, không phải một feature phụ.** Nó cần được thiết kế và test như tính năng cốt lõi.

**Cơ chế kiến trúc bắt buộc đi kèm — dù chọn BYOK hay credit:**

`architect` (B4) tính rằng giải bài toán chi phí bằng **pipeline** (draft rẻ → final đắt) gần như không tiết kiệm: $8,04 một-pass vs $7,62 two-pass = chỉ **5%**, và **lỗ** nếu final regen ≥1,2x; điểm hoà vốn ở 1,1x. Nguyên nhân nó nêu: tỉ lệ giá hai model chỉ 2,2x — quá hẹp để pass phụ tự trả tiền.

> [!NOTE]
> **Nhãn cho cặp số trên:** `architect` tính $8,04 / $7,62 ở **hệ số 2x** — chính hệ số đã bị E2 phủ định ở §9b.1 (giá trị đúng là N=3). Bản phân tích **cố ý không quy đổi lại sang N=3**, vì đoạn ngay dưới đây chứng minh câu hỏi two-pass là **moot** dưới best-of-N: quy đổi một phép so sánh đã mất hiệu lực chỉ tạo ấn tượng sai rằng nó còn đáng so. Giữ số nguyên trạng, gắn nhãn, và đọc nó như *bằng chứng cho tỉ lệ giá quá hẹp* — kết luận duy nhất của nó còn đứng.

**PM phân xử: kết luận của `architect` đúng, và đúng vì một lý do mạnh hơn lý do nó nêu.** Về câu hỏi nó đặt ra (giá có tính theo resolution không): **có, nhưng không giúp** — Gemini 3 Pro Image tính **cùng giá $0.134 cho cả 1K và 2K**, chỉ 4K mới đắt hơn ⇒ hạ resolution không làm draft rẻ hơn trên Pro. Nhưng phát hiện N=3 làm câu hỏi đó **không còn liên quan**: N=3 **không phải** retry-on-failure mà `architect` đang mô hình hoá — nó là **best-of-N để ĐẠT consistency**. Một draft pass ở model khác **không thể thay thế** nó, vì draft trả lời câu *"composition có đúng không"* còn N=3 trả lời câu *"candidate nào giữ được identity"*. **Hai câu khác nhau; pass phụ không hấp thụ được pass chính.**

⇒ **Giải bằng METERING, không bằng pipeline.** Cơ chế lõi:

| Cơ chế | Chi tiết |
|---|---|
| **Credit ledger + HOLD trước khi enqueue** | Check-rồi-gọi là **race condition**: 10 job đồng thời đều thấy đủ số dư. Phải reserve trước khi đưa job vào queue |
| **Hold reserve 3 credit/panel, không 1** | Vì N=3 là mặc định. Đây là chi tiết chỉ hiện ra khi ghép hai lens: `architect` biết cần hold-trước-khi-enqueue nhưng không biết N=3; `researcher` biết N=3 nhưng không thiết kế ledger |
| **`CHECK (available >= 0)`** ở tầng DB | Chốt cuối, phòng khi logic ứng dụng sai |
| **Hold reaper cho `expires_at`** | Thiếu reaper là rỉ chậm thành "có credit mà không generate được" — lỗi khó chẩn đoán nhất |
| **Đo regen ratio theo p50/p90** từ MVP0 | Biến quyết định của cả mô hình tài chính |
| Cache | `architect` nói thật: hit rate chỉ vài % tới ~10% (ước lượng, không có dữ liệu) ⇒ **đừng dựa vào nó**. Hai chỗ ra tiền thật là **reference-sheet amortization** và **idempotency** |

---

## 10. Lộ trình đề xuất: MVP0 đi trước

**Vấn đề với thứ tự §18.** Tác giả xếp: MVP1 Story Intelligence (*"Chưa cần generate ảnh"*) → MVP2 Comic Director → MVP3 Visual Generation → MVP4 Production System. Thứ tự này **hợp lý về kiến trúc** (xây nền trước) nhưng **rủi ro cao về product**: câu hỏi sống-chết của cả ý tưởng — *"ảnh sinh ra có đủ consistency để đọc như một bộ comic không?"* — chỉ được trả lời ở **MVP3**. Nghĩa là có thể build xong hai milestone, phần lớn công sức, rồi mới phát hiện tiền đề sai.

**Ba lens độc lập cùng đề xuất chèn một bước trước MVP1**, mỗi lens một tên gọi khác nhau — `architect` gọi là *vertical slice*, `researcher` gọi là *"đẩy một spike nhỏ của MVP3 lên sớm"* (~$12), `senior-ai-engineer` nói thẳng rằng nếu chỉ chạy được một thí nghiệm thì **image consistency phải chạy trước**. **Ba tên, một việc.** Tài liệu này dùng một tên duy nhất: **MVP0**.

**Điều chỉnh theo dữ liệu:** **không cắt MVP1** — `researcher` cho thấy nó là phần **rủi ro thấp nhất** (Story Bible extraction ✅, Comic IR ✅, có CANVAS làm bằng chứng). Chỉ **chèn MVP0 trước nó**.

### MVP0 — spec cụ thể

| | |
|---|---|
| **Thời lượng** | 1–2 tuần |
| **Chi phí** | ~**$12** (30 panel × 3 candidate × $0.134) đến ~$50 nếu lặp nhiều vòng |
| **Input** | **Một** chapter duy nhất. Tự tay viết Story Bible cho 2–3 nhân vật (**không** code extraction). Tự tay viết panel script cho ~8–30 panel (**không** code director) |
| **Code cần viết** | Đúng một việc: generate panel với character reference + N candidate + VLM select |
| **Model** | Gemini 3 Pro Image (Nano Banana Pro) |
| **Giá dùng để tính** | Con số $12 ở trên tính ở **giá standard $0.134/ảnh**. Nếu chạy **batch API** ($0.067/ảnh) thì MVP0 chỉ ~**$6**. Bản phân tích cố ý lấy số cao làm **trần an toàn** — đừng lập ngân sách theo số thấp rồi phát hiện batch không dùng được vì cần vòng lặp nhanh |

**Ba chỉ số phải đo — không chỉ một:**

1. **Consistency có đủ tốt không.** Tiêu chí pass/fail đo được: *nhìn 8 panel liền nhau, có nhận ra đó là cùng một nhân vật mà không cần được nhắc không?* Nếu **không** → toàn bộ ý tưởng cần đổi cách tiếp cận, và anh biết điều đó sau 2 tuần thay vì sau 4 tháng.
2. **N tối thiểu để VLM-select ra panel đạt.** CANVAS nói 3; tự verify xem 2 có đủ với style của anh không. **Mỗi bậc N giảm được là ~33% COGS** — đây là con số có giá trị tiền trực tiếp.
3. **Human-reject rate sau VLM-select.** ⚠️ **Chưa ai công bố con số này** — CANVAS không báo, `researcher` tra hai lần không ra. Nó quyết định liệu Continuity Checker có thực sự cắt được công human review hay chỉ thêm một lớp chi phí (§5.2). Và vì §9 kết luận đơn vị đo là **giờ-người**, đây là chỉ số quan trọng nhất trong ba.

Bổ sung, gần như miễn phí: đo luôn **multi-character panel 2–3 nhân vật** — hàng 🟡 load-bearing duy nhất của §4.2, và **không benchmark công khai nào đo nó** trên frontier model (§5.6).

### Bảng so sánh lộ trình

| | §18 gốc | Đề xuất |
|---|---|---|
| Bước 0 | — | **MVP0** — vertical slice 1 chapter, đo 3 chỉ số, ~$12, 1–2 tuần |
| MVP1 | Story Intelligence (upload, parser, extraction, timeline, Story Bible) | **Giữ nguyên** + thêm: text clean là bước đầu tiên (§5.5), `tenant_id` từ ngày đầu (§5.7), **HITL gate** và **eval kit** ngay tại đây thay vì MVP4, **log preference data** (§7), và **kiểm opt-out signal Điều 37b ngay trong bước ingest** (§8.3 item 6) — chi phí ~0 và phải nằm ở đây, vì đây là nơi file user lần đầu đi vào hệ thống |
| MVP2 | Comic Director | **Giữ**, nhưng bỏ Layout Score số thực → rubric + emphasis quota (§5.3); cứng hoá ≤3 nhân vật/panel (§5.6); thêm `text_safe_zone` vào panel spec (§5.4); và **hai human gate bắt buộc: speaker attribution (§5.4b) + dialogue condensation (§5.4)** — không phải tuỳ chọn, không dồn sang MVP4 |
| MVP3 | Visual Generation | **Giữ**. Rủi ro đã được MVP0 kiểm trước ⇒ đây là scale-up, không phải khám phá |
| MVP4 | Production System | **Nâng ưu tiên export lên sớm** — đó là thứ **duy nhất** trong MVP4 mà người dùng thật sự nhận được. Continuity Checker chuyển sang dạng N-candidate selection (§5.2), không phải flag+autofix |

**Ba việc phải xen vào lộ trình mà §18 không có:**

- **Checklist safe harbour Điều 198b** (§8.3) — rẻ, nhưng phải có **trước** khi mở cho người ngoài upload.
- **Hard quota cưỡng chế trước khi enqueue**, hold reserve 3 credit/panel (§9b.4) — phải có **trước** bản trả phí đầu tiên.
- **Typeset layer + bubble overlay** (§5.4) — nổ ngay ở panel có thoại đầu tiên, tức là **trong MVP0**.

**Nguyên tắc bao trùm:** MVP1 của §18 kết thúc bằng *"Chưa cần generate ảnh"* — đó là câu cần đảo lại. **Sinh một ảnh trong tuần đầu tiên**, dù bằng tay, dù chỉ 8 panel. Không phải để có sản phẩm, mà để biết tiền đề còn đứng.

---

## 11. Những gì bản phân tích này KHÔNG biết

Mục này **bắt buộc**, và không được bỏ để tài liệu trông chắc chắn hơn thực tế. Gộp từ hai vòng của `researcher`, bỏ trùng.

### Khoảng trống dữ liệu về công nghệ

1. **Benchmark độc lập đo frontier model (Nano Banana Pro / GPT Image 2 / FLUX.2) ở 2–3 nhân vật/panel** — **không tồn tại** trong dữ liệu công khai. Chỉ có vendor claim + benchmark open-source + kết quả pipeline-level. Đây là khoảng trống nằm ngay dưới hàng load-bearing của §4.2 ⇒ MVP0 phải tự đo.
2. **Human-reject rate sau VLM-select** — CANVAS không báo. Quyết định liệu checker có cắt được công người hay chỉ thêm chi phí.
3. **Benchmark định lượng render tiếng Việt có dấu** của bất kỳ image model — chỉ có press coverage, không có nghiên cứu có phương pháp. Đặc biệt thiếu số cho chữ chồng hai dấu ("ế", "ữ", "ượ").
4. **Prior art cho AI Layout Director / Layout Score** (§5) — không tìm được gì trực tiếp.
5. **Tỉ lệ regenerate thực tế trong sản xuất** (khác với N=3 của CANVAS) — không có số liệu ngành.

### Khoảng trống pháp lý — quan trọng nhất

6. ⚠️ **Nguyên văn Điều 37a/37b/37c Nghị định 134/2026** — cov.gov.vn chỉ có bản giới thiệu tóm tắt; thuvienphapluat.vn và nhansu.vn trả **403**; IAPP **paywall**. **Mọi kết luận về phạm vi "phi thương mại" đều dựa trên bản tóm tắt + phân tích của hãng luật, không phải nguyên văn.**
7. ⚠️ **Nguyên văn khoản 4 Điều 11 Luật TTNT 2025** — hai nguồn mô tả phạm vi **khác nhau** (chỉ "mô phỏng người thật" vs. mọi nội dung AI). Không giải quyết được bằng nguồn thứ cấp.
8. **DMCA §512(c) có phủ "hosting + AI processing" không** — không tìm được phân tích pháp lý trực tiếp.
9. **Điều 198b có áp cho SaaS xử lý nội dung** (không phải hosting thuần) không — NĐ 17 chỉ nói rõ về *"lưu trữ nội dung số theo yêu cầu"*.
10. **Tiền lệ/vụ kiện nhắm vào nền tảng AI** vì user-uploaded copyrighted content — không tìm được. Có thể do chưa có vụ nào, hoặc do ngách quá nhỏ; **không đủ dữ liệu để phân biệt hai khả năng đó**.
11. **ToS cụ thể về upload ảnh tham chiếu người thật / nhân vật có bản quyền** của các image model — không tìm được điều khoản rõ ràng.

### Khoảng trống thị trường

12. **Willingness-to-pay study** cho tác giả web novel với tool adapt truyện — không tìm được. Đây là khoảng trống nằm dưới nền của câu "bán được không".
13. **Usage pattern thật của khách hàng AI creative tool** ngoài con số trung bình 42 ảnh/tháng — không có phân phối, không có phân khúc.
14. **Gross margin công bố của một AI image SaaS cụ thể** — chỉ có benchmark ngành (ICONIQ 52%, Bessemer 50-60%), không công ty nào trong ngách này công bố.
15. **Dashtoon pricing chính thức** — họ **cố ý** không công bố bảng giá minh bạch. Con số $10/mo và 100 ảnh/ngày là **nguồn thứ cấp**.
16. **Coin/credit cụ thể mỗi ảnh của TaleAtelier** — không công bố.
17. **Số liệu CHI 2026 paper về thái độ độc giả webtoon với AI** (*"AI in Webtoon Creation: Challenges, Perceptions, and Design Implications"*, [DOI 10.1145/3772318.3790343](https://dl.acm.org/doi/10.1145/3772318.3790343)) — fetch bị **403**, chỉ biết title/venue. Chưa có số định lượng về thái độ độc giả.
18. 🪦 **Lý do Comicpad đóng cửa và quan hệ với TaleAtelier.** Notice là **primary source** — đọc trực tiếp từ [comicpad.app/pricing](https://www.comicpad.app/pricing): *"New subscriptions are paused"* + *"Comicpad is closing on September 1, 2026"*, và domain 301-redirect sang taleatelier.com. Nhưng **nguyên nhân không xác nhận được** (rebrand? acquisition? shutdown?). Đáng ghi nhận riêng: một AI comic generator có nội dung marketing cập nhật tới 7/2026 mà đóng cửa 9/2026 là dữ liệu đáng cân nhắc — và nó ủng hộ nhánh phản biện ở §7, không ủng hộ nhánh lạc quan.

### Câu hỏi còn mở cần anh trả lời

| # | Câu hỏi | Ai trả lời | Chặn gì |
|---|---|---|---|
| OQ1 | Ba câu ở §8.5 | **Luật sư SHTT Việt Nam** | Chặn thương mại hoá. **Ưu tiên số 1** |
| OQ2 | Chọn BYOK hay credit pack? | Anh — sau khi MVP0 cho ra regen ratio thật | Quyết định kiến trúc metering (§9b.4) |
| OQ3 | Có ai muốn đi tới chương 50 không? | Người dùng thật, không phải phân tích | Quyết định toàn bộ giá trị của moat "switching cost" (§7) |

---

## 12. Kết luận

**Ý tưởng này đúng ở tầng khó nhất và chưa được định nghĩa ở tầng dễ bị bỏ qua nhất.**

Tài liệu 894 dòng của anh nhận ra một điều mà phần lớn dự án AI cùng loại bỏ qua: thứ đắt và không tái tạo được là **hiểu truyện**, còn một lần gọi image model là rẻ và thay thế được. Quyết định *"ảnh là output của specification, không phải dữ liệu chính"* là quyết định chín chắn, và trong bản phân tích này nó **tự chứng minh giá trị hai lần ở hai chiều không liên quan nhau** — trùng khớp đường ranh bản quyền Zarya (§8.2), và cho phép đổi granularity render để cứu unit economics mà không đổi data model (§9b.3). Một abstraction trả lãi ở nơi tác giả không thiết kế cho nó là dấu hiệu của abstraction đúng.

Đồng thời, `researcher` xác nhận anh **không đang đánh cược**: kiến trúc này đã được CANVAS implement và đo bằng số (character 4.91/5, human win-rate 86,7%). Rủi ro kỹ thuật của MVP1–MVP2 thấp hơn mức lo ngại thông thường.

**Nhưng ba điều cần nói thẳng.**

**Thứ nhất, `Request.md` chưa phải một ý tưởng sản phẩm.** Nó có data model 13 entity và không có một dòng nào về ai là người dùng, vấn đề gì đang được giải, và "đủ tốt" nghĩa là gì. Điều này không sai — nó chỉ cần được **gọi đúng tên**, vì hai loại dự án này có tiêu chí thành công khác nhau hoàn toàn, và cắt scope theo tiêu chí sai là cách hỏng phổ biến nhất.

**Thứ hai, luận điểm moat sai — nhưng sai theo cách sửa được.** Năm thành phần anh nêu là *barrier to entry*, không phải *moat*, và concept đã public trên arXiv. Moat thật là **dữ liệu preference tích luỹ** — và nó gần như miễn phí, chỉ cần thiết kế để ghi lại từ MVP1. Nó lại dùng chung đúng cơ chế mà luật Việt Nam **buộc** phải có (§6.4). Một khoản đầu tư, trả hai lần.

**Thứ ba, cái chặn không phải kỹ thuật.** Ba lens độc lập, ba đường lập luận không liên quan, cùng đến một kết luận: **ràng buộc thật là giờ-người, không phải đô-la.** Và trên nó còn một tầng nữa — ba câu hỏi pháp lý ở §8.5 là **rủi ro nhị phân duy nhất** còn lại: mọi rủi ro khác trả lời sai thì sản phẩm kém hơn; ba câu này trả lời sai thì sản phẩm bất hợp pháp.

**Ba việc trước dòng code đầu tiên**, theo đúng thứ tự đó: mang §8.5 tới luật sư · chạy MVP0 (~$12, 1–2 tuần, đo ba chỉ số) · sửa khóa thời gian và chốt danh sách "phải có trong schema từ ngày đầu".

**Và điều đáng khen, nói rõ để không bị đọc lệch thành một bản phủ định:** vấn đề của `Request.md` không phải tư duy sai. Tư duy đúng ở những chỗ khó nhất. Vấn đề là **thiết kế đi trước xác thực** — và đó là thứ sửa được rẻ nhất, ngay bây giờ, bằng hai tuần và mười hai đô.

---

## Tài liệu tham khảo

### Tài liệu trong repo

- [Request.md](../999-Resources/Request.md) — ý tưởng gốc được thẩm định
- [pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio](../010-Planning/pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio/) — run-state: `brief.md`, `run-plan.md`, `outline.md`, `escalations.md`, `verdict.md`, `cost.md`, và toàn văn findings của bốn lens
- [Glossary](../999-Resources/Glossary.md) — thuật ngữ domain
- [Research-MOC](./Research-MOC.md) — mục lục thư mục Research

### Paper & benchmark

- [arXiv 2604.13452 — CANVAS: Continuity-Aware Narratives via Visual Agentic Storyboarding](https://arxiv.org/html/2604.13452v1) (15/04/2026) — nguồn quan trọng nhất của bản phân tích
- [arXiv 2606.15867 — CogCanvas](https://arxiv.org/html/2606.15867) — multi-subject reference benchmark
- [arXiv 2607.01383 — MIBE: Multi-subject Interaction Benchmark and Evaluator](https://arxiv.org/abs/2607.01383)
- [arXiv 2503.20871 — VinaBench](https://arxiv.org/pdf/2503.20871)
- [arXiv 2503.15655 — R²: Novel-to-Screenplay with Causal Plot Graphs](https://arxiv.org/pdf/2503.15655)
- [arXiv 2506.03090 — Literary Evidence Retrieval via Long-Context LMs](https://arxiv.org/html/2506.03090v1)
- [arXiv 2605.28643 — GraphLit](https://arxiv.org/pdf/2605.28643)
- [arXiv 2603.05890 — Lost in Stories](https://arxiv.org/html/2603.05890v1)
- [arXiv 2505.14925 — Too Long, Didn't Model](https://arxiv.org/html/2505.14925)
- [arXiv 2607.04112 — DynaVieW](https://arxiv.org/pdf/2607.04112)
- [arXiv 2511.06490 — Zooming into Comics](https://arxiv.org/pdf/2511.06490)
- [arXiv 2506.05061 — Survey on Vietnamese Document Analysis and Recognition](https://arxiv.org/html/2506.05061)
- [arXiv 2503.18641 — AI-Driven Graphic Design survey](https://arxiv.org/pdf/2503.18641)
- [arXiv 2504.14202](https://arxiv.org/pdf/2504.14202) · [arXiv 2510.25084](https://arxiv.org/pdf/2510.25084) · [Omni-ID arXiv 2412.09694](https://arxiv.org/pdf/2412.09694) — face similarity
- [ACM DOI 10.1145/2505483.2505486 — Optimized speech balloon placement](https://doi.org/10.1145/2505483.2505486)
- [CHI 2026 — AI in Webtoon Creation](https://dl.acm.org/doi/10.1145/3772318.3790343) (⚠️ 403, chỉ có metadata)

### Pháp lý

- [Cục Bản quyền tác giả — Giới thiệu Nghị định 134/2026/NĐ-CP](https://cov.gov.vn/tin-tuc/gioi-thieu-nghi-dinh-so-1342026ndcp-quy-dinh-ve-quyen-tac-gia-quyen-lien-quan-168925.html)
- [Baker McKenzie — Vietnam: Redefining Copyright for AI](https://www.bakermckenzie.com/en/insight/publications/2026/05/vietnam-redefining-copyright-for-ai)
- [Mondaq — Vietnam Copyright Framework: Decree 134/2026](https://www.mondaq.com/copyright/1796822/vietnam-copyright-framework-critical-changes-under-decree-1342026)
- [thuvienphapluat.vn — Luật Trí tuệ nhân tạo 2025 hiệu lực 01/03/2026](https://thuvienphapluat.vn/chinh-sach-phap-luat-moi/vn/ho-tro-phap-luat/chinh-sach-moi/106139/luat-tri-tue-nhan-tao-2025-chinh-thuc-co-hieu-luc)
- [luatminhkhue.vn — Yêu cầu bắt buộc với nội dung tạo bởi AI từ 01/03/2026](https://luatminhkhue.vn/yeu-cau-bat-buoc-doi-voi-noi-dung-tao-boi-ai-tu-1-3-2026.aspx)
- [genk.vn — Luật TTNT có hiệu lực 01/03/2026](https://genk.vn/tu-hom-nay-1-3-luat-tri-tue-nhan-tao-co-hieu-luc-noi-dung-ai-tao-ra-phai-co-dau-nhan-biet-165260301185217976.chn)
- [Sở KHCN Đồng Nai — Luật TTNT hiệu lực từ tháng 3/2026](https://skhcn.dongnai.gov.vn/vi/news/khoa-hoc-va-cong-nghe/luat-tri-tue-nhan-tao-chinh-thuc-co-hieu-luc-tu-thang-3-2026-1000.html)
- [Lexology — Safe Harbor under the 2022 IP Law of Vietnam](https://www.lexology.com/library/detail.aspx?g=d865aa00-fd06-41ab-bde8-cd2f4f604cc1)
- [Lexology — Notice and Takedown Process under Vietnamese Copyright Legislation](https://www.lexology.com/library/detail.aspx?g=c0985dc4-1cfe-41c6-8050-fb169a701c58)
- [KENFOX — Notice and takedown regime against online IPR infringement in Vietnam](https://kenfoxlaw.com/notice-and-takedown-regime-against-online-ipr-infringement-in-vietnam)
- [Rouse — Intermediary Service Providers' liabilities](https://rouse.com/insights/news/2023/intermediary-service-providers-liabilities-under-the-amended-ip-law-and-decree-on-copyright)
- [Tilleke & Gibbins — New Decree guides Vietnam's IP Law on copyright](https://www.tilleke.com/insights/new-decree-guides-vietnams-ip-law-in-relation-to-copyright-and-related-rights/2/)
- [US Copyright Office — AI](https://www.copyright.gov/ai/) · [AI policy guidance PDF](https://www.copyright.gov/ai/ai_policy_guidance.pdf) · [Circular 14 — Derivative Works](https://www.copyright.gov/circs/circ14.pdf)
- [Harvard JOLT — Zarya of the Dawn](https://jolt.law.harvard.edu/digest/zarya-of-the-dawn-how-ai-is-changing-the-landscape-of-copyright-protection)
- [Sidley Austin — US Copyright Office Report on AI and Copyrightability](https://www.sidley.com/en/insights/newsupdates/2025/02/us-copyright-office-issues-report-on-artificial-intelligence-and-copyrightability)
- [Kirkland — IP Primer for Comic Book Creators](https://www.kirkland.com/-/media/content/kirkland-ip-primer-for-comic-book-creators.pdf)
- [DLA Piper / Lexology — Training AI models: EU and UK TDM exceptions](https://mse.dlapiper.com/post/102ivrx/training-ai-models-content-copyright-and-the-eu-and-uk-tdm-exceptions)
- [CMS Law-Now — AI and copyright: exceptions for text and data mining](https://cms-lawnow.com/en/ealerts/2024/10/ai-and-copyright-exploring-exceptions-for-text-and-data-mining)
- [PetaPixel — South Korea AI content labelling laws](https://petapixel.com/2026/01/29/south-korea-launches-landmark-laws-requiring-labels-on-ai-generated-content/)
- [The New Publishing Standard — Korea AI Act & webtoon creators](https://thenewpublishingstandard.com/2026/01/28/korea-ai-act-webtoon-creators/)
- [Anime News Network — South Korea's new AI law](https://www.animenewsnetwork.com/news/2026-01-24/south-korea-new-ai-law-raises-questions-for-webtoon-creators-platforms/.233383)

### Model & pricing (official)

- [Google — Nano Banana Pro](https://blog.google/innovation-and-ai/products/nano-banana-pro/)
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) · [Gemini API terms](https://ai.google.dev/gemini-api/terms)
- [Black Forest Labs — pricing](https://docs.bfl.ml/quick_start/pricing) · [FLUX.2 launch](https://bfl.ai/blog/flux-2)

### Đối thủ, thị trường & pricing

- [comicink.ai/pricing](https://www.comicink.ai/pricing) · [comicink.ai/blog — convert book to comic series](https://www.comicink.ai/blog/convert-book-to-comic-series) · [comicink.ai/terms](https://www.comicink.ai/terms)
- [taleatelier.com — AI comic generator](https://taleatelier.com/ai-comic-generator)
- [comicpad.app/pricing](https://www.comicpad.app/pricing) — ⚠️ notice đóng cửa 01/09/2026
- [toolworthy.ai — Dashtoon Studio](https://www.toolworthy.ai/tool/dashtoon-studio)
- [aigregator — Anifusion](https://aigregator.com/tools/anifusion)
- [comistitch.com — where to publish AI comic 2026](https://comistitch.com/blog/where-to-publish-ai-comic-2026-platform-decision-tree/) · [best AI comic generator 2026](https://comistitch.com/blog/best-ai-comic-generator-2026/)
- [sudowrite.com — writing multiple timelines with AI](https://sudowrite.com/blog/writing-multiple-timelines-ai/)
- [novilot.com/features](https://www.novilot.com/features) · [blog.proseweave.ai — Story Bible guide](https://blog.proseweave.ai/story-bible-guide-templates-examples/)
- [mycomics.ai/terms](https://mycomics.ai/terms/) · [comicai.com/terms-of-service](https://comicai.com/terms-of-service) · [livecomics.to/terms](https://livecomics.to/terms)
- [tabstory.net — AI comic generator copyright comparison](https://www.tabstory.net/blog/ai-comic-generator-copyright-comparison-20260517)
- [Korea Times — Webtoon industry seeks AI edge amid legal, ethical challenges](https://www.koreatimes.co.kr/lifestyle/trends/20251106/webtoon-industry-seeks-ai-edge-amid-legal-ethical-challenges)
- [Forbes — Webtoon's growth is slowing but its ambitions are growing](https://www.forbes.com/sites/robsalkowitz/2026/08/11/webtoons-growth-is-slowing-but-its-ambitions-are-growing/)
- [BusinessWire — WEBTOON webcomic adaptations of hit web novels](https://www.businesswire.com/news/home/20230118005243/en/WEBTOON-Expands-its-IP-Creator-Ecosystem-With-Webcomic-Adaptations-of-Hit-Web-Novels)
- [digitalapplied.com — AI image generation statistics 2026](https://www.digitalapplied.com/blog/ai-image-generation-statistics-2026-data-points) · [sqmagazine.co.uk](https://sqmagazine.co.uk/ai-image-generation-statistics/)
- [saasmag.com — AI COGS & SaaS gross margin compression](https://www.saasmag.com/ai-cogs-saas-gross-margin-compression/) · [softwareseni.com](https://www.softwareseni.com/why-ai-gross-margins-are-so-much-lower-than-saas-and-what-that-means-for-your-business/)
- [saasultra.com — SaaS churn rate statistics & benchmarks](https://www.saasultra.com/saas-churn-rate-statistics-benchmarks/)
- [buildmvpfast.com — BYOK AI SaaS pricing model 2026](https://www.buildmvpfast.com/blog/byok-bring-your-own-key-ai-saas-pricing-model-2026) · [copilot-alternatives.com](https://copilot-alternatives.com/blog/what-is-byok-ai-coding-tools/) · [dmchamp.com](https://dmchamp.com/best/best-ai-tools-byok-2026/)
- [javilopen.substack.com — consistency of characters and objects](https://javilopen.substack.com/p/consistency-of-characters-objects)
- [nenobanana.com — character consistency in Nano Banana](https://www.nenobanana.com/blogs/character-consistency-in-nano-banana)

### Text rendering & typesetting

- [comicsai.org — manga speech bubble generator](https://www.comicsai.org/en/manga-speech-bubble-generator)
- [github.com/BloomBooks/comical-js](https://github.com/BloomBooks/comical-js)
- [VietnamNet — Nano Banana Pro và chữ tiếng Việt](https://vietnamnet.vn/nano-banana-pro-gay-soc-voi-kha-nang-tao-anh-voi-chu-tieng-viet-cuc-chuan-2465113.html)
- [dejaoffice.com — Nano Banana Pro text rendering](https://www.dejaoffice.com/blog/2026/05/26/nano-banana-pro-the-image-model-with-the-best-text-rendering-right-now/)

### Hạ tầng & self-host

- [runpod.io/pricing](https://www.runpod.io/pricing) · [spheron.network — RunPod vs Vast.ai 2026](https://www.spheron.network/blog/runpod-vs-vastai-2026/)
- [tinytiny.tools — FLUX.2 self-hosting](https://tinytiny.tools/en/blog/flux-2-self-hosting) · [willitrunai.com — FLUX.2 dev](https://willitrunai.com/image-models/flux-2-dev)
- [thefluxtrain.com — FLUX LoRA training guide](https://thefluxtrain.com/blog/noobs-guide-to-flux-lora-training/)
