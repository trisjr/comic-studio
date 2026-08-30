---
id: CHARTER-001
type: charter
status: draft
created: 2026-08-23
---

# 📜 Project Charter — comic-studio

> [!IMPORTANT]
> **Quy ước nhãn nguồn** (giữ nguyên từ bảng Canonical Facts của run `/pm-doc` 2026-08-23, **cấm tách số khỏi nhãn**):
> `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` **ước lượng hoặc phép nhân — không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> Mọi con số trong tài liệu này được **copy nguyên** từ bảng Canonical Facts (CF) tại [outline.md của run](./pm-runs/2026-08-23-khoi-tao-tai-lieu-planning-comic-studio/outline.md). Không tài liệu nào trong bộ Planning được tự tính lại.

## Mục lục

1. [Thông tin dự án](#1-thông-tin-dự-án)
2. [Business Case](#2-business-case)
3. [Mục tiêu dự án](#3-mục-tiêu-dự-án)
4. [Yêu cầu cấp cao](#4-yêu-cầu-cấp-cao)
5. [Phạm vi](#5-phạm-vi)
6. [Stakeholder Matrix (RACI)](#6-stakeholder-matrix-raci)
7. [Ràng buộc (Constraints)](#7-ràng-buộc-constraints)
8. [Giả định (Assumptions)](#8-giả-định-assumptions)
9. [Tiêu chí thành công & Go/No-Go](#9-tiêu-chí-thành-công--gono-go)
10. [Tài liệu liên quan](#10-tài-liệu-liên-quan)

---

## 1. Thông tin dự án

| Trường | Giá trị |
|---|---|
| **Project Name** | `comic-studio` |
| **Bản chất sản phẩm** | **SaaS thương mại multi-tenant** — nền tảng để **người khác tự upload truyện chữ của họ** và sinh comic pages `[CHỐT]` CF-1.1 |
| **Sponsor** | **Founder (anh)** — *cùng một người với Manager. Dự án không có sponsor tách biệt; ghi thẳng thay vì bịa một vai trò không tồn tại.* |
| **Manager** | **Founder (anh)** |
| **Đội thực thi** | **1 người (anh) + AI assist (Comic Studio agents)**. Không funding, không ngân sách marketing `[CHỐT]` CF-1.2 |
| **Ngày khởi tạo Charter** | 2026-08-23 |
| **Trạng thái dự án** | **Pre-code** — `src/`, `test/`, `openspec/changes/` đều rỗng `[OFF]` CF-1.3 (đo bằng `find`) |
| **Trạng thái tài liệu** | `draft` |
| **Horizon lập kế hoạch** | 09/2026 → 02/2027 (6 tháng) `[CHỐT]` CF-8.1 — xem [Roadmap.md](./Roadmap.md) |
| **Phân khúc mục tiêu** | **Tác giả truyện chữ (writer) KHÔNG biết vẽ** — *không* nhắm hoạ sĩ `[CHỐT]` CF-1.5 |

---

## 2. Business Case

### 2.1 Con số KHÔNG được dùng để biện minh cho dự án

Phần này đứng **trước** phần biện minh, có chủ ý. Đây là phần chống tự lừa mình của tài liệu.

Thị trường webtoon được các báo cáo ngành định cỡ **$14,0–18,3B (2026), CAGR 26,3–33,1%** `[BCN]` — 7 firm phân kỳ (CF-4.1). **Con số này bị cấm dùng làm căn cứ biện minh dự án này**, vì hai lý do đo được:

| Lý do | Bằng chứng | Nguồn |
|---|---|---|
| **Nó đo sai thứ** | TAM webtoon đo **tiêu thụ nội dung** của độc giả. comic-studio **không lấy tiền từ độc giả** — nó bán công cụ cho tác giả. Hai dòng tiền khác nhau hoàn toàn | CF-4.1 |
| **Bản thân con số không ổn định** | Đổi nhãn từ "webtoon" sang "digital comics"/"webcomics" ⇒ CAGR sụp còn **6,7–10,4%**, chênh **4–5 lần** cho cùng một hiện tượng | `[BCN]` CF-4.2 |
| **Platform số 1 cũng không chạm được TAM của chính nó** | WEBTOON làm **~$1,4–1,5B/năm** `[EM từ OFF]`, tức **8–10%** của cái TAM mà nó thống trị | `[BCN]` + `[EM]` CF-4.2 |

> [!WARNING]
> Bất kỳ tài liệu con nào của Charter này (Roadmap, OKRs, Risk Register, MVP Scope) **trích TAM làm lý do đầu tư thời gian** đều là vi phạm ràng buộc của Charter, không phải một lựa chọn diễn đạt.

Tầng SAM (công cụ cho tác giả) được ước **$0,4M – $9M ARR** — nhưng phải mang nhãn ⚠️ `[EM]`, vì **3/4 thừa số là giả định và không firm nào bán con số này** (CF-4.3). SAM vì thế cũng không đủ tư cách làm căn cứ.

### 2.2 Con số dự án thực sự neo vào

**SOM năm 1 = $4K – $14K ARR ≈ $300–1.200 MRR, tương đương 30–80 paying user** ⚠️ `[EM]` (CF-4.4).

Neo thực tế của con số này là **Anifusion**: solo founder, có lãi, **$0 marketing spend**, đạt được sau **~2 năm** kể từ launch 2024 `[TC]` (CF-4.5).

> [!CAUTION]
> **Nguồn về Anifusion mâu thuẫn và Charter giữ nguyên cả hai, không chọn một:** một nguồn ghi **$833 MRR**, nguồn khác ghi **$5.000/tháng**; giá cũng lệch **$9/mo** (run trước) vs **€20/mo** (vòng delta). Chọn một con số rồi trình bày như sự thật là chính xác cách mà một `[EM]` bị rửa thành một `[OFF]`.

### 2.3 Vì sao vẫn làm

Ba luận cứ, không luận cứ nào dựa trên quy mô thị trường:

1. **Kiến trúc đã được validate bằng số, không phải giả thuyết.** CANVAS đạt character **4.91/5**, human win-rate **86,7%**, background **4.88/5** `[OFF]` (CF-6.2). Rủi ro kỹ thuật của phần lõi thấp hơn mức lo ngại thông thường.
2. **Khoảng cách research → product đang mở.** Concept đã public trên arXiv nhưng **chưa có sản phẩm thương mại nào ship nó** ([Analysis §4.3](../050-Research/Analysis-Comic-Studio-Concept.md)). Cửa sổ này sẽ hẹp lại — xem CF-5.2 (GlobalComix mua lại INKR, **$13M (25/03/2026)** `[TC]`) trong [Risk-Register.md](./Risk-Register.md).
3. **Chi phí kiểm chứng cực thấp.** MVP0 tốn **~$12** ở giá standard $0.134 / **~$6** nếu batch — Charter lấy **số cao ($12) làm trần an toàn** vì vòng lặp nhanh khiến batch khó dùng `[EM tính từ OFF]` (CF-3.11). Với chi phí đó, việc **không** kiểm chứng mới là quyết định khó biện minh.

**Ràng buộc thật của dự án là giờ-người, không phải đô-la** — ba lens độc lập cùng đến kết luận này ([Analysis §4.4, §12](../050-Research/Analysis-Comic-Studio-Concept.md)).

---

## 3. Mục tiêu dự án

Năm mục tiêu, mỗi mục tiêu map tới một chỉ số có trong CF. **Không mục tiêu nào đặt ngưỡng số mà CF không có** — chỗ nào CF không cho ngưỡng, Charter ghi `TBD` và giao cho [MVP-Scope.md](./MVP-Scope.md) định nghĩa.

| # | Mục tiêu | Chỉ số đo | Neo CF | Ngưỡng |
|---|---|---|---|---|
| **MT-1** | **Biết tiền đề còn đứng hay không, trong 1–2 tuần và ~$12** | MVP0 chạy xong 1 chapter, trả lời được **cả ba** chỉ số CF-8.5 | CF-8.4, CF-8.5, CF-3.11 `[EM tính từ OFF]` | Hoàn thành trong **1–2 tuần**, chi phí **≤ ~$12** |
| **MT-2** | **Đo được thứ chưa ai đo: human-reject rate sau VLM-select** | Tỷ lệ panel bị người bác bỏ sau khi VLM đã chọn | CF-8.5 (3) — ⭐ **chưa ai công bố con số này** | Ngưỡng PASS: `TBD` (định tại [MVP-Scope.md](./MVP-Scope.md) gate G1) |
| **MT-3** | **Xác nhận hàng load-bearing: multi-character panel 2–3 nhân vật** | Đo trực tiếp trên panel có 2–3 nhân vật | CF-8.6 (MVP0 đo thêm, gần như miễn phí) + CF-6.4 `[OFF]` — **không benchmark độc lập nào đo frontier model ở mức này** | Ngưỡng PASS: `TBD` (gate G1) |
| **MT-4** | **Hạ N tối thiểu — mỗi bậc N giảm được là ~33% COGS** | N nhỏ nhất còn giữ chất lượng; regen ratio thực tế **p50/p90** | CF-8.5 (2), CF-8.6, CF-3.1 `[OFF]` | Mặc định N=3 `[OFF]`; mục tiêu là **đo**, không phải giả định giảm được |
| **MT-5** | **Doanh thu năm 1 nằm trong dải SOM, không vượt ra ngoài** | MRR và số paying user | CF-4.4 ⚠️ `[EM]` | **$300–1.200 MRR**, **30–80 paying user** — thang **trăm đô**, không phải nghìn |

> [!IMPORTANT]
> **Hai hệ định danh, đừng lẫn:** `MT-n` là **mục tiêu dự án** (bảng trên); `G0` / `G1` / `G2` là **ba gate Go/No-Go** do [MVP-Scope.md](./MVP-Scope.md) §7 định nghĩa. Chúng không ánh xạ 1-1 với nhau — ví dụ `MT-2` và `MT-3` đều lấy ngưỡng PASS từ **gate G1**.

> [!NOTE]
> **MT-1 là mục tiêu bao trùm.** Nguyên tắc CF-8.12: *"Sinh một ảnh trong tuần đầu tiên, dù bằng tay, dù chỉ 8 panel. Không phải để có sản phẩm, mà để biết tiền đề còn đứng."*

---

## 4. Yêu cầu cấp cao

Verdict thẩm định: **KHẢ THI CÓ ĐIỀU KIỆN — CHÍN điều kiện phải thoả ĐỒNG THỜI** (CF-6.1).

> [!IMPORTANT]
> [Analysis §4.1](../050-Research/Analysis-Comic-Studio-Concept.md) đặt tiêu đề là *"BẢY điều kiện"* — đó là số của **một lens** (`researcher`, hướng thị trường + pháp lý) và được giữ để truy vết. **Số điều kiện phải thoả là CHÍN**: bảy của `researcher` cộng hai từ `architect` và `senior-ai-engineer`, **cùng mức bắt buộc**. Đếm bảy khi lập kế hoạch là bỏ sót hai điều kiện.

| # | Yêu cầu (điều kiện khả thi) | Không thoả thì hỏng thế nào | Lens |
|---|---|---|---|
| **R1** | **≤3 nhân vật/panel**, cứng hoá trong Comic IR; cảnh đông người dùng shot xa / silhouette / crop | Attribute binding thất bại gần hoàn toàn từ 4 người: ảnh trông hợp lý nhưng **gắn sai trang phục cho sai người** | `researcher` |
| **R2** | **Chữ đi qua typeset layer riêng**, không nhúng vào ảnh AI | Sửa một câu thoại thành một lần regenerate ảnh; bubble che mặt nhân vật; **mất phần được bảo hộ bản quyền** | `researcher` |
| **R3** | **User warrant + indemnify + safe harbour Điều 198b** — công cụ takedown, đăng ký đầu mối với **Bộ VHTTDL**, **SLA 72 giờ** `[OFF]` CF-7.6 | Nền tảng chịu trách nhiệm cho nội dung user upload, không hưởng miễn trừ | `researcher` |
| **R4** | **AI disclosure** — nghĩa vụ **nội địa Việt Nam**, không chỉ chuyện thị trường Hàn Quốc | Vi phạm Luật TTNT 2025; deadline tuân thủ **~01/03/2027** `[OFF]` CF-7.7 | `researcher` |
| **R5** | **Pricing metered / BYOK, không subscription phẳng** | Một power user xoá margin của bốn user thường; **−262%** margin ở 3 chapter/tháng `[EM]` CF-3.7 | `researcher` |
| **R6** | **Tư vấn luật sư SHTT về Điều 37a và khoản 4 Điều 11 TRƯỚC khi thương mại hoá** | **Rủi ro nhị phân**: không làm sản phẩm chậm, mà làm sản phẩm **bất hợp pháp** (CF-7.9) | `researcher` |
| **R7** | **Budget COGS ở hệ số N=3, không 2x** `[OFF]` CF-3.1 | Toàn bộ mô hình tài chính lệch **+50%** so với thực tế | `researcher` |
| **R8** | **Deterministic hoá bốn transform** — vẽ rõ ranh giới LLM / deterministic code | Phần đáng ra là code tất định bị giao cho LLM: không test được, không tái lập được, chi phí trôi | `architect` |
| **R9** | **HITL gate + eval kit ở MVP1, không phải MVP4** (CF-8.7) | Không có vòng phản hồi người trong 3 milestone; **preference data (moat thật) không được ghi từ đầu** | `senior-ai-engineer` |

**Ba yêu cầu hạ tầng bắt buộc kèm theo** (CF-6.12, CF-7.3 — không phải feature, là điều kiện tồn tại):

- **Credit ledger + HOLD trước khi enqueue** (check-rồi-gọi là race condition), **hold reserve 3 credit/panel** vì N=3, `CHECK (available >= 0)` ở tầng DB, hold reaper cho `expires_at`.
- **Provenance chain**: bảng `Generation` + `parent_generation_id` + `change_log` + `field_provenance` — là **hồ sơ pháp lý bắt buộc** theo NĐ 134/2026 Điều 5a, **không backfill được** `[OFF]` CF-7.3.
- **`tenant_id` từ ngày đầu** (CF-8.7) — multi-tenancy chiếm **15–25%** effort mà `Request.md` không nhắc một dòng `[EM]` CF-6.9.

---

## 5. Phạm vi

> [!IMPORTANT]
> Đây là **phạm vi sản phẩm** — cái gì thuộc về comic-studio và cái gì không, ở mọi thời điểm. **Ranh giới MVP** (cái gì vào MVP0/1/2/3/4, cái gì hoãn) là câu hỏi khác và thuộc [MVP-Scope.md](./MVP-Scope.md). Charter **không lặp lại** nội dung đó.

### 5.1 Scope In — thuộc về sản phẩm

| Hạng mục | Neo |
|---|---|
| Nền tảng **SaaS multi-tenant** để tác giả bên ngoài tự upload truyện chữ và sinh comic pages | CF-1.1 `[CHỐT]` |
| **Story Bible editor + Comic IR + layout + versioning + export** — lõi giá trị, có mặt ở cả tầng không-image-gen | CF-2.2 `[CHỐT]` |
| **Managed inference** (credit pack không hết hạn) cho user dưới ngưỡng **~125 ảnh/tháng** | CF-2.3 `[CHỐT]`, CF-2.5 `[TC]` |
| **BYOK** như **tùy chọn MỞ KHÓA** cho power user — không phải điều kiện để dùng sản phẩm | CF-2.4 `[CHỐT]` |
| **Typeset layer + speech bubble overlay** — tự build (Comical-JS chưa có auto-placement) | R2, CF-8.11(c) |
| **Provenance / audit trail** phục vụ nghĩa vụ pháp lý và làm nền cho preference data | CF-7.3 `[OFF]` |
| **Compliance layer**: takedown tool, opt-out check Điều 37b tại bước ingest, AI disclosure | CF-7.5, CF-7.6, CF-7.7 |
| **Editor tối thiểu** (~20–25% effort, mẫu số SaaS) | CF-6.7 `[EM]` — chi tiết ranh giới ở [MVP-Scope.md](./MVP-Scope.md) |

### 5.2 Scope Out — KHÔNG thuộc về sản phẩm

| Hạng mục loại trừ | Vì sao |
|---|---|
| **Trở thành content studio** (tự sản xuất và phát hành truyện) | Đó là mô hình Dashtoon: **$20,1M / 3 vòng, 465 nhân viên (31/05/2026)** `[TC]` CF-5.1 — khác loại hình, và **không dùng giá Dashtoon làm neo pricing** |
| **Nhắm phân khúc hoạ sĩ (artist)** | CF-1.5 `[CHỐT]` + CF-5.6: cộng đồng vẽ đã có tiền lệ **boycott** và **buộc vẽ lại** tác phẩm dính AI `[TC]` |
| **Subscription phẳng unlimited; free tier kiểu "100 ảnh/ngày"** | ⛔ CF-2.7 — mâu thuẫn trực tiếp với R5 và CF-3.7 |
| **Huấn luyện model riêng trên nội dung user** | Không tạo model mới, không lưu nội dung vào weights — đây là chính lập luận pháp lý của dự án tại [Analysis §8.5 câu 1](../050-Research/Analysis-Comic-Studio-Concept.md). Phá nó là phá luôn phòng tuyến TDM |
| **Panel có ≥4 nhân vật** | ❌ Chưa giải được: ID-Sim rơi từ **27.21** (3 người) xuống **2.67** (4) `[OFF]` CF-6.5 |
| **Microservices + Vector DB** | ❌ CẮT — monolith; lý do **mạnh lên** dưới mô hình SaaS CF-9.2 |
| **Canvas editor đầy đủ §14** (infinite canvas, undo xuyên state, realtime collab, inpainting) | CẮT MỘT PHẦN CF-9.1 — nghĩa vụ pháp lý đặt lên **tầng DỮ LIỆU**, không đặt lên tầng canvas |
| **Layout Score 5 số thực** | ❌ CẮT cơ chế, GIỮ mục tiêu → rubric rời rạc CF-9.3 |
| **Render text tiếng Việt trực tiếp vào ảnh AI** | Loại trừ theo R2, kể cả khi model làm được |
| **Chiến dịch marketing trả phí** | Không có ngân sách marketing CF-1.2 `[CHỐT]` |

---

## 6. Stakeholder Matrix (RACI)

**Chú giải**: **R** = Responsible (người trực tiếp làm) · **A** = Accountable (chịu trách nhiệm cuối, **duy nhất một** mỗi hàng) · **C** = Consulted (hỏi ý kiến trước khi quyết) · **I** = Informed (được thông báo sau) · **—** = không tham gia.

> [!WARNING]
> **Đọc bảng này với ba cảnh báo, nếu không nó là bảng trang trí:**
> 1. **Cột A gần như luôn là Founder** — đó là **sự thật của đội 1 người** (CF-1.2), không phải lỗi trình bày. Giá trị của bảng nằm ở cột **R** và **C**, nơi công việc thật sự được phân và nơi lỗ hổng lộ ra.
> 2. **Hai cột đang RỖNG trong thực tế**: Luật sư SHTT **chưa engage** và Design partner **chưa có ai**. Chữ **C** ở đó là **nghĩa vụ chưa thực hiện**, không phải năng lực đang có.
> 3. **Model provider không phải participant** — Google (Gemini 3 Pro Image) và BFL (FLUX.2) là **ràng buộc ngoài, không đàm phán được**. Họ chỉ xuất hiện với **I** ở nghĩa "dự án phải theo dõi thay đổi của họ", không có nghĩa họ có nghĩa vụ gì với dự án.

| Nhóm hoạt động | Founder | AI Agent (Comic Studio) | Luật sư SHTT *(chưa engage)* | Model provider *(ngoài, không đàm phán)* | Design partner *(chưa có ai)* |
|---|---|---|---|---|---|
| **1. Định hướng sản phẩm** | **A, R** | C — `business-analyst`, `product-owner` phản biện định vị & phân khúc | — | — | C — *sẽ là nguồn tín hiệu chính khi có; hiện **không có**, nên định hướng đang dựa hoàn toàn vào suy luận desk research* |
| **2. Quyết định kiến trúc** | **A** | **R** — `architect` soạn phương án, đánh giá đánh đổi, viết ADR | — | I — ràng buộc kỹ thuật của họ giới hạn không gian thiết kế | — |
| **3. Implementation** | **A** | **R** — `software-engineer` viết code dưới điều phối của Founder | — | — | — |
| **4. Quyết định pháp lý** | **A** | R — `security-auditor` chuẩn bị hồ sơ, checklist Điều 198b, soạn câu hỏi | ⚠️ **C — BẮT BUỘC, và HIỆN CHƯA ENGAGE.** Ba câu CF-7.8 chưa ai trả lời ⇒ [ô này là điều kiện chặn của mục 9](#9-tiêu-chí-thành-công--gono-go) | — | — |
| **5. Định giá & unit economics** | **A** | **R** — `business-analyst` dựng mô hình 3 tầng, tính margin, theo dõi regen ratio | C — khi cấu trúc giá chạm ranh giới TDM thương mại (Điều 37a, CF-7.4) · **chưa engage** | I — **giá đầu vào do họ đặt**: $0.134 standard / $0.067 batch / FLUX.2 $0.03 `[OFF]` CF-3.4. Đổi giá là đổi toàn bộ mô hình | — |
| **6. Kiểm thử & nghiệm thu** | **A, R** — *human gate cuối là mắt người, không uỷ quyền được (CF-8.8: hai human gate bắt buộc)* | R — `security-auditor`, `software-engineer` chạy eval kit, VLM autorater | — | — | C — *nghiệm thu "trang này đọc có ổn không" cần người ngoài; **chưa có ai** ⇒ hiện chỉ có một cặp mắt, đây là khoảng trống đã biết* |
| **7. Phân phối / marketing** | **A** | **R** — `business-analyst` sản xuất **comparison-listicle SEO** (kênh thống trị ngách, 8/8 đối thủ đều làm) ⚠️ `[EM]` CF-5.9 | — | — | C — *khi có, là kênh word-of-mouth rẻ nhất; **chưa có*** |
| **8. Vận hành & sự cố** | **A** | **R** — `software-engineer` xử lý incident, hold reaper, quota enforcement | C — sự cố liên quan takedown / SLA 72 giờ Điều 198b · **chưa engage** | I — **silent model drift là sự cố mà dự án không kiểm soát được**, chỉ phát hiện được | — |
| **9. Quản trị tri thức & tài liệu** | **A** | **R** — mọi role Comic Studio ghi findings, cập nhật MOC, giữ traceability | — | — | — |

**Ba lỗ hổng bảng này để lộ ra, nêu thẳng thay vì tô vẽ:**

- **Bus factor = 1.** Founder là **A** ở cả 9 hàng. Không có phương án dự phòng nào ở cấp con người — đây là rủi ro vận hành, thuộc [Risk-Register.md](./Risk-Register.md).
- **Hàng 4 có một chữ C không tồn tại.** Đó là rủi ro nhị phân duy nhất của dự án (CF-7.9), và nó đang treo.
- **Hàng 1 và 6 mất tín hiệu người dùng.** Không Design partner nghĩa là mọi phán đoán về "đủ tốt" đang do chính người build đưa ra — đúng cái failure mode mà [Analysis §3.2](../050-Research/Analysis-Comic-Studio-Concept.md) chỉ ra.

---

## 7. Ràng buộc (Constraints)

| # | Ràng buộc | Nguồn | Hệ quả bắt buộc |
|---|---|---|---|
| **C1** | **Đội 1 người (anh) + AI assist. Không funding, không ngân sách marketing.** | `[CHỐT]` CF-1.2 | Mọi scope phải chia được cho một người. Kênh phân phối phải là kênh **$0 spend** |
| **C2** | **Mô hình 3 tầng kiểu Novelcrafter đã CHỐT — không mở lại trong horizon này.** Tầng 1 **$4–8/tháng KHÔNG có image gen** (margin ~90%, không cần API key) · Tầng 2 **credit pack không hết hạn**, managed inference, cho user **<125 ảnh/tháng** · Tầng 3 **BYOK là tùy chọn MỞ KHÓA**, không phải điều kiện dùng sản phẩm | `[CHỐT]` CF-2.1, CF-2.2, CF-2.3, CF-2.4 (ngưỡng ~125 ảnh/tháng: `[TC]` CF-2.5) | Kiến trúc billing, credit ledger và onboarding phải được thiết kế cho **ba** tầng ngay từ đầu, không retrofit |
| **C3** | **Trần cứng ≤3 nhân vật/panel**, cứng hoá trong Comic IR | `[OFF]` CF-6.5 — CogCanvas ID-Sim **42.33** (2 người) → **27.21** (3) → **2.67** (4) → **0.52** (5); *"near-complete failure beyond three subjects"* | Cảnh đông người phải giải bằng shot xa / silhouette / crop. Đây là ràng buộc **sản phẩm**, không phải tuỳ chọn kỹ thuật |
| **C4** | **Deadline pháp lý ~01/03/2027** — AI disclosure là nghĩa vụ nội địa Việt Nam theo Luật TTNT 2025 | `[OFF]` CF-7.7 ⚠️ **kèm caveat: hai nguồn mô tả phạm vi KHÁC NHAU** (chỉ "mô phỏng người thật" vs mọi nội dung AI) | Deadline nằm **ngay sau** horizon 09/2026–02/2027. Vì phạm vi chưa rõ, phải thiết kế theo diễn giải **rộng** (mọi nội dung AI) cho tới khi luật sư chốt |
| **C5** | **Positioning bắt buộc: disclosure-first, nhắm writer KHÔNG nhắm artist** | phân tích PM CF-5.7, dựa trên `[TC]` CF-5.6 (Naver Webtoon bị **độc giả boycott subscription**; **BlueLine Studio bị buộc vẽ lại** episode) | Kênh cộng đồng là kênh **có rủi ro ngược**. Cấm marketing vào cộng đồng hoạ sĩ. Bằng chứng đối chứng: Novelcrafter **220.000+ authors** `[OFF]` CF-2.6 — cộng đồng viết chấp nhận |
| **C6** | **Gross margin kỳ vọng 50–60%, KHÔNG phải 80%** | `[BCN]` CF-3.10 — ICONIQ 52%, Bessemer 50–60% | Mọi mô hình tài chính đặt mục tiêu margin >60% là mô hình sai kỳ vọng ngành, không phải mô hình tham vọng |
| **C7** | **Chi phí sàn $12,06/chapter @N=3, Gemini batch** — và đây là **SÀN, không phải trần** (chưa tính VLM call để score 3 candidate) | `[EM tính từ OFF]` CF-3.5 | Cấm dùng $12,06 như chi phí thực tế trong bất kỳ tính toán margin nào mà không nêu nó là sàn |
| **C8** | **N = 3 là mặc định cho MỌI panel** (best-of-N; *"Performance saturates at N=3"*), và **KHÔNG phải retry-on-failure** | `[OFF]` CF-3.1, CF-3.2 | Không thể lấy chất lượng của N=3 mà tính chi phí của N=2. Hold reserve phải là **3 credit/panel** (CF-6.12) |
| **C9** | **Thứ tự milestone cố định: MVP0 → MVP1 → MVP2 → MVP3 → MVP4** | CF-8.3 | Không đảo thứ tự để "làm phần dễ trước". Chi tiết ở [Roadmap.md](./Roadmap.md) |
| **C10** | **Horizon 6 tháng (09/2026–02/2027) CHƯA được ai xác nhận là đủ cho 1 dev** | `[CHỐT]` CF-8.1 + ràng buộc PM CF-8.13 | **Cấm nén lịch cho vừa khung.** Nếu khung không chứa hết MVP0–MVP3, [Roadmap.md](./Roadmap.md) phải nói thẳng cái gì rơi ra ngoài |

---

## 8. Giả định (Assumptions)

Mỗi giả định dưới đây là một mục mang nhãn ⚠️ `[EM]` trong bảng CF — **ước lượng, không phải số đo**. Cột cuối là câu hỏi *"sai thì hỏng ở đâu"*, và nó là lý do mục này tồn tại.

| # | Giả định | Nhãn & nguồn | Sai thì hỏng ở đâu |
|---|---|---|---|
| **A1** | **60 ảnh/chapter** (15 page × 4 panel) | ⚠️ `[EM]` CF-3.3 — **giả định của `researcher` run trước, KHÔNG phải số đo** | Đây là **thừa số gốc của toàn bộ mô hình chi phí**. Sai 2 lần ⇒ chi phí/chapter, ngưỡng 125 ảnh, margin, và giá tầng 2 sai theo cùng bội số. Mọi con số tài chính dưới nó thừa hưởng nguyên vẹn sai số này |
| **A2** | **$12,06/chapter @N=3 (Gemini batch)** là chi phí đại diện | ⚠️ `[EM tính từ OFF]` CF-3.5 — **là SÀN, chưa tính VLM call score 3 candidate** | Nếu VLM scoring đắt hơn dự kiến, margin âm sâu hơn CF-3.6 (**−21%** `[EM]` trên $9.99, 1 chapter/tháng) và CF-3.7 (**−262%** `[EM]` power user 3 chapter/tháng). Mô hình 3 tầng có thể không cứu được unit economics |
| **A3** | **1 chapter = 180 ảnh @N=3**, vượt ngưỡng 125 ngay ở chapter đầu tiên | ⚠️ `[EM]` CF-3.9 (60 × 3) — kế thừa sai số của A1 | Nếu sai, **ranh giới phân tuyến tầng 2 / tầng 3 đặt sai chỗ**: hoặc BYOK bị đẩy cho người không cần, hoặc credit pack gánh lỗ cho power user |
| **A4** | **SOM năm 1 = $4K–14K ARR / 30–80 paying user** | ⚠️ `[EM]` CF-4.4, neo vào CF-4.5 `[TC]` **có mâu thuẫn nội tại** ($833 MRR vs $5.000/tháng; $9/mo vs €20/mo) | Nếu SOM thực thấp hơn dải này, dự án không đạt điểm hoà vốn thời gian dù kỹ thuật thành công. Nếu cao hơn, rủi ro ngược: hạ tầng 1 người không gánh nổi |
| **A5** | **Credit pack không hết hạn né được GRR 23%** | ⚠️ `[EM]` CF-4.9 — **là lập luận logic (doanh thu ghi trước), KHÔNG phải số đo. Không tìm được dữ liệu retention nào cho mô hình credit pack** | Nếu sai, retention thực rơi về band `[OFF]` CF-4.6 (**GRR 23% / NRR 32%** cho AI-native `<$50/tháng`, **kèm BA CAVEAT BẮT BUỘC CF-4.7**: (a) cohort AI-native chỉ **~200 công ty**, n của riêng band này **không công bố**; (b) lọc **≥$250K ARR** ⇒ **loại đúng nhóm indie mà comic-studio thuộc về**; (c) dữ liệu **2025**, không phải 2026) và toàn bộ giả định về vòng đời khách hàng sụp. Đây là giả định **được biện luận nhiều nhất và có bằng chứng ít nhất** |
| **A6** | **Editor tối thiểu tốn ~20–25% effort** (mẫu số **SaaS**, đã gồm multi-tenancy) | ⚠️ `[EM]` CF-6.7 — `architect` | Nếu vượt, nó ăn vào thời gian của phần lõi. ⛔ **Lưu ý bắt buộc: CF-6.8 (50–60%, §14 đầy đủ) dùng MẪU SỐ KHÁC — mẫu số công cụ cá nhân, không gồm multi-tenancy/billing/auth. CẤM TRỪ 6.8 CHO 6.7** |
| **A7** | **Multi-tenancy tốn 15–25% effort** | ⚠️ `[EM]` CF-6.9 — `architect`, và `Request.md` **không nhắc một dòng** | Đây là effort **hoàn toàn không có trong tài liệu gốc**. Nếu ước thiếu, nó không lấy chỗ của tính năng — nó lấy chỗ của **thời gian không tồn tại** |
| **A8** | **Speaker attribution lỗi 30–50% (3+ người) / 40–60% (câu ngắn)** | ⚠️ `[EM]` CF-6.10 — **ước lượng, KHÔNG phải số đo** | Nếu tệ hơn, human gate speaker attribution (CF-8.8) chuyển từ "kiểm tra" sang "làm lại từ đầu" — và đúng vào ràng buộc thật của dự án là **giờ-người** |
| **A9** | **Continuity Checker chỉ phủ 40–60% số panel** | ⚠️ `[EM]` CF-6.11 | Phải **nói rõ với user**, đừng để họ hiểu là được bảo vệ toàn diện. Nếu giấu, đây là lời hứa sản phẩm không giữ được — rủi ro uy tín, không chỉ rủi ro kỹ thuật |
| **A10** | **Cache hit rate chỉ vài % tới ~10%** | ⚠️ `[EM]` CF-6.13 — `architect` **tự khai là ước lượng** | Hệ quả thực tế là **đừng dựa vào cache** để cứu margin. Nếu kế hoạch tài chính nào giả định cache tiết kiệm đáng kể, kế hoạch đó sai |
| **A11** | **Comparison-listicle SEO là kênh thống trị ngách** | ⚠️ `[EM]` CF-5.9 — **quan sát SERP, không phải số traffic đo được** | Nếu sai, dự án không còn kênh $0-spend nào đã kiểm chứng. Kênh đã chết: **Show HN — ComicInk 30/04/2026 được 2 điểm / 2 comment** `[OFF]` CF-5.8 |
| **A12** | **Horizon 6 tháng đủ cho MVP0–MVP3 với 1 dev** | `[CHỐT]` CF-8.1 nhưng ⚠️ **CF-8.13: chưa ai xác nhận** | Nếu sai, hệ quả không phải "chậm một chút" mà là **deadline pháp lý C4 (~01/03/2027) trôi qua trước khi compliance layer xong**. [Roadmap.md](./Roadmap.md) bắt buộc trả lời tường minh câu này |
| **A13** | **Constella (WEBTOON) là rủi ro nền tảng** | `[TC]` CF-5.4 ⚠️ **fetch nguồn fail — chưa xác nhận đã ship hay còn là announcement** | Nếu đã ship và mở rộng sang creator không biết vẽ, kênh phân phối tự nhiên nhất bị chặn ở cửa. Điểm bù hiện tại: Constella nhắm creator **đã biết vẽ**, comic-studio nhắm người **không biết vẽ** — hai phân khúc, nhưng khoảng cách **có thể** hẹp lại (CF-5.5) |

---

## 9. Tiêu chí thành công & Go/No-Go

**Chi tiết ba gate (G0 pháp lý · G1 kỹ thuật sau MVP0 · G2 kinh tế sau MVP1) và kill criteria nằm ở [MVP-Scope.md](./MVP-Scope.md).** Charter **không lặp lại** — mục này chỉ nêu **điều kiện chặn ở cấp dự án**, thứ mà không tài liệu con nào được phép nới.

### 9.1 Điều kiện chặn cấp dự án (project-level blocker)

> [!CAUTION]
> **BLOCKER-01 — Ba câu hỏi luật sư SHTT (CF-7.8).**
> **Chừng nào ba câu ở [Analysis §8.5](../050-Research/Analysis-Comic-Studio-Concept.md) chưa có câu trả lời từ luật sư SHTT Việt Nam, dự án KHÔNG được thương mại hoá** — không thu tiền, không mở cho người ngoài upload.
>
> 1. **Điều 37a NĐ 134/2026** có áp cho *inference-time extraction* trên nội dung user upload, hay chỉ áp cho *huấn luyện* model? *(⚠️ Điều 37a hiện chỉ được biết qua **bản tóm tắt, không phải nguyên văn** — CF-7.4)*
> 2. **Khoản 4 Điều 11 Luật TTNT 2025** — nghĩa vụ đánh dấu định dạng máy đọc áp cho *mọi* nội dung AI hay chỉ nội dung *"mô phỏng người thật hoặc sự kiện thực tế"*? Watermark của provider (SynthID) có thoả không?
> 3. Nền tảng có được coi là **"doanh nghiệp cung cấp dịch vụ trung gian"** để hưởng miễn trừ **Điều 198b** không, khi nó không chỉ *lưu trữ* mà còn *xử lý/biến đổi* nội dung user?

**Vì sao đây là blocker chứ không phải một rủi ro thường** (CF-7.9): mọi rủi ro khác của dự án là rủi ro **mức độ** — trả lời sai thì sản phẩm **kém hơn hoặc chậm hơn**. Ba câu này trả lời sai thì sản phẩm **bất hợp pháp**. Đây là **rủi ro nhị phân duy nhất** của toàn dự án.

**Trạng thái hiện tại: CHƯA ENGAGE luật sư** (xem hàng 4 bảng RACI).

### 9.2 Ranh giới của blocker — chống hiểu nhầm

> [!NOTE]
> **BLOCKER-01 chặn THƯƠNG MẠI HOÁ, KHÔNG chặn MVP0–MVP1.** Đọc thành *"phải chờ luật sư mới được viết dòng code đầu tiên"* là đọc sai, và là cách hiểu nhầm đắt nhất mà tài liệu này có thể gây ra. MVP0 (~$12, 1–2 tuần, dùng nội dung của chính Founder) không tạo ra nghĩa vụ mà ba câu trên đang hỏi.

### 9.3 Ba điều kiện chặn phụ

| ID | Điều kiện chặn | Neo | Chặn cái gì |
|---|---|---|---|
| **BLOCKER-02** | **Checklist safe harbour Điều 198b chưa hoàn tất** | CF-7.6, CF-8.11(a) | Chặn việc **mở cho người ngoài upload** (không chặn dùng nội bộ) |
| **BLOCKER-03** | **Hard quota cưỡng chế trước khi enqueue chưa có** | CF-6.12, CF-8.11(b) | Chặn **bản trả phí đầu tiên**. Không có nó, một power user (**−262%** margin `[EM]` CF-3.7) có thể chạy không giới hạn |
| **BLOCKER-04** | **Provenance chain chưa ghi từ generation đầu tiên** | `[OFF]` CF-7.3 | Chặn **mọi thứ** — vì **không backfill được**. Không lưu từ generation đầu tiên thì **vĩnh viễn** không có hồ sơ Điều 5a |

### 9.4 Tiêu chí thành công cấp dự án

Charter coi dự án **thành công ở mức tối thiểu** khi cả bốn điều sau đúng: (1) năm mục tiêu ở [mục 3](#3-mục-tiêu-dự-án) có kết quả **đo được** — kể cả kết quả âm; (2) BLOCKER-01 đã được trả lời, dù câu trả lời là "không được làm"; (3) không blocker nào bị bỏ qua một cách âm thầm; (4) quyết định dừng-hay-tiếp được đưa ra **dựa trên số của MVP0**, không dựa trên cảm giác.

> Một dự án dừng sau MVP0 vì số nói không, với chi phí ~$12 và 2 tuần, **là một kết quả thành công của Charter này** — không phải thất bại.

---

## 10. Tài liệu liên quan

### Bộ tài liệu Planning (cùng thư mục)

| Tài liệu | Trả lời câu hỏi gì | Quan hệ với Charter |
|---|---|---|
| [MVP-Scope.md](./MVP-Scope.md) | *Cái gì vào MVP, cái gì không* — ba gate G0/G1/G2 và kill criteria | Chi tiết hoá [mục 5](#5-phạm-vi) và [mục 9](#9-tiêu-chí-thành-công--gono-go) |
| [Roadmap.md](./Roadmap.md) | *Khi nào làm gì* — horizon 09/2026–02/2027, MVP0→MVP4 | Chi tiết hoá C9, C10 và trả lời CF-8.13 |
| [OKRs.md](./OKRs.md) | *Tuần này làm đúng việc hay không* — Q4/2026 + preview Q1/2027 | Chuyển [mục 3](#3-mục-tiêu-dự-án) thành Objective/Key Result theo chu kỳ |
| [Risk-Register.md](./Risk-Register.md) | *Cái gì có thể giết dự án và dấu hiệu sớm* | Chi tiết hoá [mục 8](#8-giả-định-assumptions) và các blocker ở [mục 9](#9-tiêu-chí-thành-công--gono-go) |
| [Planning-MOC.md](./Planning-MOC.md) | Chỉ mục thư mục Planning | Điều hướng |

### Căn cứ thẩm định

| Tài liệu | Vai trò |
|---|---|
| [Analysis-Comic-Studio-Concept.md](../050-Research/Analysis-Comic-Studio-Concept.md) | **Nguồn thẩm định gốc** — §3 (ý tưởng phù hợp chưa), §4.1 (điều kiện khả thi), §8.5 (ba câu luật sư), §12 (kết luận). ⛔ Đây là **dấu vết quyết định tại thời điểm viết** — không sửa nó |
| [Analysis-Market-Competitor-Landscape.md](../050-Research/Analysis-Market-Competitor-Landscape.md) | Research Notes bổ sung — TAM/SAM/SOM, đối thủ, pricing, retention benchmark, khoảng trống dữ liệu |
| [outline.md — run `/pm-doc` 2026-08-23](./pm-runs/2026-08-23-khoi-tao-tai-lieu-planning-comic-studio/outline.md) | **Bảng Canonical Facts CF-1→CF-9** — nguồn sự thật chung của cả bộ Planning. Mọi con số trong Charter copy từ đây |
| [findings/researcher.md](./pm-runs/2026-08-23-khoi-tao-tai-lieu-planning-comic-studio/findings/researcher.md) | Findings thị trường & cạnh tranh của run này |
| [verdict.md — run thẩm định ý tưởng](./pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio/verdict.md) | Verdict của run phân tích trước |

---

_Generated by Comic Studio — role `business-analyst`._
_Author: trisjr_
