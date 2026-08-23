---
id: RESEARCH-002
type: research
status: draft
project: comic-studio
owner: "@trisjr"
tags: [comic-studio, market-sizing, competitor-analysis, pricing, byok, retention, go-to-market]
created: 2026-08-23
updated: 2026-08-23
---

# Phân tích Thị trường & Bối cảnh Đối thủ — comic-studio

Tài liệu này trả lời năm câu hỏi thương mại của comic-studio: thị trường **thật sự** lớn cỡ nào, ai đang ở trong đó, mô hình kinh doanh nào có tiền lệ chạy được, giữ chân người dùng ở mức giá này thì kỳ vọng ra sao, và một sản phẩm **1 dev** phân phối qua kênh nào.

**Đây là tài liệu bổ sung, không thay thế** [Analysis-Comic-Studio-Concept.md](./Analysis-Comic-Studio-Concept.md) — tài liệu đó thẩm định **khả thi kỹ thuật, pháp lý và unit economics** của concept. Chỗ nào cần tới kết luận của nó, tài liệu này **link sang** chứ không chép lại.

- **Căn cứ kỹ thuật & pháp lý:** [Analysis-Comic-Studio-Concept.md](./Analysis-Comic-Studio-Concept.md)
- **Tài liệu neo quyết định:** [Charter-Comic-Studio.md](../010-Planning/Charter-Comic-Studio.md)
- **Thuật ngữ:** [Glossary](../999-Resources/Glossary.md)

> [!IMPORTANT]
> **Ngày truy cập toàn bộ URL trong tài liệu: 23/08/2026.** Mọi con số định lượng đều mang nhãn nguồn. **Đọc con số mà bỏ nhãn là đọc sai tài liệu này** — một con số `[EM]` mất nhãn sẽ biến một phép nhân từ giả định thành một sự thật đo được.

## Mục lục

- [Quy ước nhãn](#quy-ước-nhãn)
- [1. Tóm tắt](#1-tóm-tắt)
- [2. Quy mô thị trường (TAM / SAM / SOM)](#2-quy-mô-thị-trường-tam--sam--som)
  - [2.1 TAM — bảy firm, và vì sao con số $14B KHÔNG dùng được](#21-tam--bảy-firm-và-vì-sao-con-số-14b-không-dùng-được)
  - [2.2 SAM — không ai bán con số này](#22-sam--không-ai-bán-con-số-này)
  - [2.3 SOM — reference class của sản phẩm 1 dev](#23-som--reference-class-của-sản-phẩm-1-dev)
- [3. Bối cảnh đối thủ](#3-bối-cảnh-đối-thủ)
  - [3.1 Bảng đối thủ — phần bổ sung](#31-bảng-đối-thủ--phần-bổ-sung)
  - [3.2 Ba kết luận](#32-ba-kết-luận)
- [4. Mô hình kinh doanh & pricing](#4-mô-hình-kinh-doanh--pricing)
  - [4.1 BYOK — ai đang chạy thật](#41-byok--ai-đang-chạy-thật)
  - [4.2 Ma sát onboarding BYOK — không có số](#42-ma-sát-onboarding-byok--không-có-số)
  - [4.3 Ba cấu hình lai của ngành (A / B / C)](#43-ba-cấu-hình-lai-của-ngành-a--b--c)
  - [4.4 Ngưỡng hoà vốn ~125 ảnh/tháng](#44-ngưỡng-hoà-vốn-125-ảnhtháng)
- [5. Retention benchmark](#5-retention-benchmark)
  - [5.1 23% GRR — ChartMogul, và ba caveat bắt buộc](#51-23-grr--chartmogul-và-ba-caveat-bắt-buộc)
  - [5.2 RevenueCat — dataset độc lập, KHÔNG được gộp](#52-revenuecat--dataset-độc-lập-không-được-gộp)
  - [5.3 Không có benchmark cho creative tool $5–20/tháng](#53-không-có-benchmark-cho-creative-tool-520tháng)
- [6. Kênh phân phối](#6-kênh-phân-phối)
  - [6.1 Bảng kênh](#61-bảng-kênh)
  - [6.2 Rủi ro ngược của kênh cộng đồng](#62-rủi-ro-ngược-của-kênh-cộng-đồng)
  - [6.3 Key Result đo được](#63-key-result-đo-được)
- [7. Khoảng trống dữ liệu](#7-khoảng-trống-dữ-liệu)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## Quy ước nhãn

Nhãn áp cho **mọi** con số trong tài liệu này. Nhãn là một phần của dữ liệu, không phải chú thích trang trí.

| Nhãn | Nghĩa |
|---|---|
| `[OFF]` | Nguồn official — trang pricing/IR/homepage của chính chủ, hoặc paper gốc |
| `[BCN]` | Báo cáo ngành — market research firm, có tên firm |
| `[TC]` | Thứ cấp — blog/aggregator dẫn lại, không phải chính chủ |
| `[EM]` | Ước lượng hoặc phép nhân từ giả định — **không phải số đo được** |

Nhãn ghép (ví dụ `[EM từ OFF]`, `[EM tính từ OFF]`) mô tả **chuỗi suy dẫn**: số gốc là `[OFF]`, nhưng con số đang đọc là kết quả của một phép tính thêm vào. Giữ nguyên dạng ghép, không rút gọn.

---

## 1. Tóm tắt

**Ba điều đọc trước tiên.**

**Một — thị trường thật của comic-studio nhỏ hơn thị trường webtoon từ ba đến bốn bậc độ lớn.** TAM webtoon **$14,0–18,3B (2026)** `[BCN]` là thị trường **tiêu thụ nội dung**; comic-studio không lấy tiền từ độc giả mà bán công cụ cho tác giả. SAM cho tầng công cụ ước **$0,4M – $9M ARR** `[EM]` — tức **0,003% – 0,06%** của TAM — và ba trong bốn thừa số của phép nhân đó là giả định. SOM năm 1 ước **$4K – $14K ARR** `[EM]`, neo vào Anifusion. Hệ quả trực tiếp: **mọi tài liệu planning trích TAM $14B để biện minh cho dự án đều đang phạm lỗi logic**; con số cần đặt vào mục tiêu doanh thu nằm ở **thang trăm đô/tháng**, không phải nghìn.

**Hai — con số 23% GRR sống sót qua kiểm chứng, nhưng chỉ dùng được kèm ba caveat.** Nguồn gốc là **ChartMogul**, cỡ mẫu **~3.500 công ty**, dữ liệu **2025**, band AI-native `<$50/tháng` `[OFF]`. Một dataset hoàn toàn độc lập (**RevenueCat**, ~115.000 app) xác nhận **cùng chiều**: AI app retention 12 tháng **21,1%** vs non-AI **30,7%** `[TC]`. Hai bộ số **không được gộp** — chúng đo hai metric khác nhau. Kết luận có sức nặng nhất của ChartMogul không phải "AI churn" mà là **giá**: sản phẩm AI bán trên $250/tháng đạt GRR **70%** `[OFF]`, ngang B2B SaaS thường.

**Ba — câu hỏi BYOK phải được đặt lại, vì cấu hình đang giả định không tồn tại trong ngành.** Không tìm được sản phẩm nào chạy "free = key nền tảng, tier cao = BYOK"; ba cấu hình thực tế đều **đảo ngược** nó. Comp gần nhất và gần như hoàn hảo là **Novelcrafter** `[OFF]`: **220.000+ authors**, tier **$4 không có AI**, BYOK mở khoá từ **$8**, nền tảng **không bao giờ** bán inference. Ngưỡng hoà vốn BYOK cho ảnh là **~125 ảnh/tháng** `[TC]` — con số vận hành đắt giá nhất của toàn bộ nghiên cứu này, vì nó biến câu hỏi "BYOK hay credit" từ lựa chọn nhị phân thành **quy tắc phân tuyến user có thể code được**.

---

## 2. Quy mô thị trường (TAM / SAM / SOM)

### 2.1 TAM — bảy firm, và vì sao con số $14B KHÔNG dùng được

Các báo cáo **không chênh nhau vì sai**, mà vì **định nghĩa thị trường khác nhau**.

| # | Firm | Định nghĩa | Giá trị hiện tại | Dự báo | CAGR | Nhãn |
|---|---|---|---|---|---|---|
| 1 | **Mordor Intelligence** | Webtoons | **$10,85B (2025) → $14,44B (2026)** | **$60,25B (2031)** | **33,1%** (2026–31) | `[BCN]` — verify bằng fetch trực tiếp |
| 2 | **Grand View Research** | Webtoons | $8,3B (2023) → $18,3B (2026) | $45,3B (2030) | 27,3% (2024–30) | `[BCN]` qua search snippet |
| 3 | **TBRC / Research&Markets** | Webtoons | $10,75B (2025) → $14,02B (2026) | — | 30,5% | `[BCN]` qua search snippet |
| 4 | **IMARC Group** | Webtoons | $11,8B (2025) | $101,8B (2034) | 26,26% (2026–34) | `[BCN]` qua search snippet |
| 5 | **market.us** | Webtoons | — | — | 28,1% | `[BCN]` |
| 6 | Không rõ firm | **Digital comics** (hẹp hơn) | $5,806M (2025) → $6,306M (2026) | $14,4B (2034) | **10,4%** | `[TC]` |
| 7 | **Fortune Business Insights** | **Webcomics** | $8,76B (2026) | $14,73B (2034) | **6,72%** | `[BCN]` qua search snippet |

**Đọc bảng này thế nào:**

- Cùng gọi là "webtoon", giá trị 2026 dao động **$14,0B – $18,3B** `[BCN]`; CAGR **26,3% – 33,1%** `[BCN]`.
- Nhưng khi đổi nhãn thị trường sang **"digital comics"** hoặc **"webcomics"**, CAGR sụp xuống **6,7% – 10,4%** — chênh **4–5 lần**. ⇒ **CAGR 33% chỉ tồn tại dưới định nghĩa "webtoon"**, vốn gộp cả platform revenue, ads và IP licensing. **Không được dùng nó cho thị trường công cụ.**
- **Truy nguyên nguồn:** bộ số `$14,44B / $60,25B / 33,1%` từng được ghi nhận là "nguồn thứ cấp abovea.tech" trong [Analysis-Comic-Studio-Concept.md](./Analysis-Comic-Studio-Concept.md); nguồn gốc thật là **Mordor Intelligence**, đã fetch trực tiếp xác nhận. Số này **nâng hạng từ `[TC]` lên `[BCN]`**.

**Sanity-check bằng dữ liệu công ty thật:**

| Chỉ số | Giá trị | Nhãn |
|---|---|---|
| WEBTOON Entertainment (WBTN) — guidance Q3/2026 | $358M–368M | `[OFF]` |
| ⇒ Annualize | **~$1,4–1,5B/năm** | `[EM từ OFF]` — phép nhân ×4 từ số quý |
| WBTN MAU (toàn ecosystem, gồm Wattpad) | ~155 triệu | `[TC]` |
| WBTN trả cho creator 2021–2025 | **$2,7B**, cập nhật **$2,8B** tới 2026 | `[TC]` |

> [!WARNING]
> **Mâu thuẫn WEBTOON — đây là bằng chứng TAM không dùng được.**
> Platform số 1 thế giới làm **~$1,4–1,5B/năm** `[EM từ OFF]`. Nếu TAM 2026 thật sự là **$14–18B** `[BCN]`, WEBTOON chỉ chiếm **8–10%** một thị trường mà nó **thống trị**.
> Điều này *có thể* đúng (Kakao, Lezhin, Piccoma, Kuaikan, Bilibili Comics chia phần còn lại), nhưng nó cũng là dấu hiệu rõ rằng các con số `[BCN]` đang tính cả những thứ nằm ngoài phạm vi "người trả tiền đọc webtoon".
> ⇒ **Không dùng TAM $14B làm căn cứ cho bất kỳ quyết định nào.**

### 2.2 SAM — không ai bán con số này

> [!CAUTION]
> **KHÔNG CÓ DỮ LIỆU TRỰC TIẾP CHO SAM.**
> Đã tìm ba hướng: (a) search *"creator tools market webtoon"*; (b) fetch trang Mordor — chỉ có *"South Korea alone counted 12,000 professional artists in 2024"* và ghi nhận AI tools *"trims page-level costs by 68%"*, **không có market size cho creator tooling**; (c) search *"digital comics market"* — mọi báo cáo đều đo **tiêu thụ**, **không firm nào tách segment công cụ tác giả**.
> ⇒ **Bất cứ con số SAM nào cũng là phép nhân và phải được gắn nhãn `[EM]`.**

**Tầng A — INPUT ĐO ĐƯỢC** (đây là phần có nguồn):

| Input | Giá trị | Nhãn | Caveat |
|---|---|---|---|
| Tapas — số creator | **>75.000** (từ 61.000 tháng 2/2021) | `[TC]` | Wikipedia, không phải trang official |
| Tapas — series / episode | 100.000 series, >1,6M episode; **80% là comic** | `[TC]` | |
| WEBTOON Canvas — số series | **2,2 triệu series** | `[TC]` | ⚠️ **series ≠ creator** |
| Hàn Quốc — artist chuyên nghiệp | **12.000** (2024) | `[BCN]` Mordor | Chỉ Hàn Quốc, chỉ nhóm "professional" |
| WEBTOON Canvas ecosystem | Unified CANVAS 26/03/2026, 7 ngôn ngữ; hạ ngưỡng payout PayPal **$100 → $25** | `[TC]` | Tín hiệu: WEBTOON đang **mở rộng** đáy creator |
| **Novelcrafter — số tác giả** | **220.000+ authors** | `[OFF]` | Ngành **liền kề** (novel writing tool, BYOK, $4–20/mo) |
| Novelcrafter — độ phủ | "almost 120 countries" (15/09/2025) | `[OFF]` | |

**Tầng B — PHÉP NHÂN.** Mọi dòng dưới đây là `[EM]`, **không phải dữ liệu**:

| Kịch bản | Creator addressable | × Tỉ lệ trả tiền | × ARPU/tháng | = SAM (ARR) | Giả định gãy ở đâu |
|---|---|---|---|---|---|
| **Thận trọng** | ~87.000 `[EM]` (Tapas 75K + KR pro 12K) | 3% `[EM]` | $12 `[EM]` | **~$376K** `[EM]` | Cộng hai nguồn khác chuẩn, **có thể chồng lấn** |
| **Trung bình** | 500.000 `[EM]` (suy từ 2,2M series ÷ ~4 series/creator) | 3% `[EM]` | $12 `[EM]` | **~$2,2M** `[EM]` | Tỉ lệ **4 series/creator không có nguồn** |
| **Lạc quan** | 1.000.000 `[EM]` | 5% `[EM]` | $15 `[EM]` | **~$9,0M** `[EM]` | Cả ba thừa số đều là giả định |

> [!IMPORTANT]
> **Kết luận SAM — con số quan trọng nhất của mục này.**
> SAM = **$0,4M – $9M ARR** `[EM — 3/4 thừa số là giả định]`, tức **0,003% – 0,06%** của TAM $14B `[BCN]`.
>
> **Ý nghĩa quyết định:** đây **không phải một thị trường lớn**. Thị trường bán công cụ cho tác giả nhỏ hơn thị trường tiêu thụ nội dung **3–4 bậc độ lớn**.
>
> Bằng chứng gián tiếp: toàn bộ ngách AI comic tool hiện có — Dashtoon (**$20,1M** funding, **465** người) `[TC]`, Anifusion (**~$10K** cumulative revenue) `[TC]`, ComicInk, TaleAtelier, Comicpad (đã đóng cửa) — **không có unicorn nào**.
> Đối chiếu ngược lại: **Novelcrafter 220K authors** `[OFF]` cho thấy segment "tác giả tự viết dài, chịu trả $4–20/mo" **có thật và đo được** — nhưng đó là novel writing, **không phải** comic generation.

### 2.3 SOM — reference class của sản phẩm 1 dev

**Reference class — sản phẩm cùng hình dạng, có số công khai:**

| Sản phẩm | Mô hình | Doanh thu | Team | Nhãn |
|---|---|---|---|---|
| **Anifusion** (AI comic, solo founder) | Subscription **€20/mo** + free tier 100 credit | **$833 MRR** · **$10.000 cumulative** kể từ launch 2024 · **có lãi** | **1 người** | `[TC]` |
| **Anifusion — số MÂU THUẪN** | — | **"$5.000/tháng"**, ~220–250 paying subs | 1 | `[TC]` |
| **TypingMind** (BYOK chat UI) | $39 one-time + BYOK | **$1M lifetime trong 20 tháng**; hiện **$130–160K/tháng**; ARR 2024 **$817,3K**; bootstrapped | Nhỏ | `[TC]` |
| **ComicInk** (iOS app) | Credit pack | **<1.000 downloads**, 4,9★/27 rating, launch **19/03/2026** | Không tra được | `[TC]` |

> [!WARNING]
> **Hai mâu thuẫn phải giữ nguyên dạng mâu thuẫn, không được phân xử.**
>
> **1. Anifusion — hai con số giá và hai con số doanh thu, không con số nào chính chủ:**
>
> | Chiều | Nguồn A | Nguồn B | Trạng thái |
> |---|---|---|---|
> | **Giá** | **$9/mo** — ghi nhận trong [Analysis-Comic-Studio-Concept.md](./Analysis-Comic-Studio-Concept.md) `[TC]` | **€20/mo** (10.000 credit) + free 100 — Starter Story `[TC]` | ❌ **Chưa phân xử.** Giá có thể đã đổi giữa hai lần ghi nhận |
> | **Doanh thu** | **$833 MRR** (+ $10.000 cumulative) — Starter Story `[TC]` | **$5.000/tháng**, ~220–250 paying subs — maxincubator `[TC]` | ❌ **Chưa phân xử.** Starter Story cụ thể hơn (tách MRR vs cumulative) nên *nghiêng về* $833 MRR, nhưng **không xác minh được** |
>
> Cả bốn con số đều `[TC]`, **không nguồn nào là chính chủ** (`anifusion.ai/pricing` chưa fetch lại). ⇒ **Ghi cả hai, không chọn một rồi trình bày như sự thật.** Nếu dùng số này để định giá, phải fetch lại trang pricing chính chủ trước.
>
> **2. ComicInk <1.000 downloads chỉ đo app iOS**, không đo web app. **Đừng đọc thành "ComicInk rất nhỏ"** — phần reverse-engineer unit economics ở [Analysis-Comic-Studio-Concept.md](./Analysis-Comic-Studio-Concept.md) dựa trên pricing **web** và vẫn đứng vững.

**SOM đề xuất:**

| Mốc | Paying user | ARPU | MRR | Nhãn | Neo |
|---|---|---|---|---|---|
| Năm 1 (thực tế) | 30–80 | $10–15 | **$300–1.200** | `[EM]` | Anifusion mất **~2 năm** solo để tới $833 MRR `[TC]` |
| Năm 2 (tốt) | 150–300 | $12–15 | **$1.800–4.500** | `[EM]` | — |
| Trần lạc quan | 800–1.500 | $15 | **$12K–22K** | `[EM]` | Trên mức này cần team hoặc marketing budget |

⇒ **SOM năm 1 ≈ $4K–14K ARR** `[EM]`. Đây là con số cần đặt vào mục tiêu doanh thu, **không phải** một phần trăm của TAM $14B.

---

## 3. Bối cảnh đối thủ

### 3.1 Bảng đối thủ — phần bổ sung

> Phần dưới đây **chỉ chứa thông tin mới hoặc đã được sửa lại**. Bảng đối thủ nền (ComicInk pricing, TaleAtelier, Dashtoon ~$10/mo, Anifusion, Lore Machine, AI Comic Factory, Comicsmaker.ai, Comicpad đóng cửa 01/09/2026) nằm ở [Analysis-Comic-Studio-Concept.md](./Analysis-Comic-Studio-Concept.md) — **không lặp lại ở đây**.

| Tên | Mô hình giá | Quy mô / funding | Giải consistency? |
|---|---|---|---|
| **Dashtoon** | ~$10/mo `[TC]`, không công bố chính thức | **$20,1M / 3 vòng** `[TC]` Tracxn: Seed 07/04/2023 **$1,006M** · Seed 02/11/2023 **$6,024M** · Series A 17/09/2024 **$8,813M**. Matrix Partners India, Stellaris VP, Z47. ⚠️ **465 nhân viên** tính tới 31/05/2026 `[TC]` | Character library + recurring character. **Không công bố kỹ thuật** |
| ⭐ **GlobalComix** — đối thủ chưa xuất hiện trong lần rà trước | Platform; creator tool **đang xây** | **$13M (25/03/2026)** `[TC]`, lead **SBI US Gateway Fund + Point72 Ventures**; cùng Scrum Ventures, Wise Ventures, Wicklow Capital, Upside VC. **Mua lại INKR**. CEO mới Henrik Rydberg (ex-Tinkercad) | **Gián tiếp — nhưng đúng chỗ đau.** INKR đem về *"translation, text detection, image cleaning, and typesetting"*; Ken Luong (ex-INKR CEO) làm head of AI engineering. Định vị **"the Figma for comics"** |
| **WEBTOON / Naver — công cụ nội bộ** | **Miễn phí** cho creator của platform | WBTN niêm yết NASDAQ, ~155M MAU `[TC]` | **Constella**: convert 3D character model nhiều pose → 2D theo **đúng nét vẽ của chính creator**. Rollout **professional creators trước**. Cộng **AI Painter** (2021) + **WebtoonMe** |
| **WEBTOON byUs** (11/07/2026) | Miễn phí, reader-facing | — | **Không** liên quan consistency — AI story chat trên IP đã duyệt. Nêu ra để **không nhầm** nó là creator tool |
| **ComicInk** | Credit pack | CEO **Sanjoy Ghosh**. **Không tra được** team/funding. iOS launch 19/03/2026, **<1K downloads** `[TC]`. Ra tính năng video 07/2026 | **Đối thủ duy nhất công bố cơ chế**: *"addressing character consistency through reference image injection and structured attributes"* — Show HN 30/04/2026 |
| **Anifusion** | **€20/mo** (10.000 credit) + free 100 `[TC]` ⚠️ **mâu thuẫn với $9/mo** — xem [§2.3](#23-som--reference-class-của-sản-phẩm-1-dev) | **1 người**. **$833 MRR** `[TC]` ⚠️ **mâu thuẫn với $5.000/tháng** `[TC]`. Có lãi, không funding | Không công bố cơ chế |
| **Jenova Webtoon Creator** | Không tra được | Không tra được | *"...with character consistency"* — ⚠️ **chỉ là marketing claim**, không có benchmark |
| **Comicsmaker.ai** | Xem tài liệu nền | Không tra được | **LoRA training trên 15–30 ảnh/nhân vật** `[TC]` — đối thủ duy nhất cho user **tự train LoRA** |

### 3.2 Ba kết luận

**Kết luận 1 — Dashtoon là content studio dùng AI, không phải đối thủ tool.**
**465 nhân viên** với **$20,1M** funding `[TC]` là con số phải nhìn thẳng. Ở một công ty comic-AI, 465 người nghĩa là **phần lớn nhân sự làm nội dung**, không làm phần mềm. Hai hệ quả cứng:
- Dashtoon **không** cạnh tranh trực tiếp với comic-studio ở tầng công cụ.
- **Không được dùng giá Dashtoon (~$10/mo) làm neo pricing.** Điều này làm **yếu** một phần lập luận "trần giá thị trường $9–10", nhưng **không lật** nó — ComicInk, TaleAtelier và Anifusion vẫn nằm trong khoảng đó.

**Kết luận 2 — GlobalComix + INKR là mối đe doạ chiến lược thật.**
Có **$13M** `[TC]`, có đội AI chuyên **typesetting / text detection / image cleaning** — đúng phần mà [Analysis-Comic-Studio-Concept.md](./Analysis-Comic-Studio-Concept.md) kết luận comic-studio **"phải tự build"** (Comical-JS chưa có auto-placement). Định vị **"the Figma for comics"** trùng thẳng với định vị mà concept đang nhắm. ⇒ **Cần theo dõi liên tục**, và phải là một hàng trong Risk Register.

**Kết luận 3 — Constella của WEBTOON là rủi ro NỀN TẢNG, khác loại với rủi ro đối thủ.**
Nếu platform lớn nhất phát công cụ consistency **miễn phí** cho creator của nó, thì kênh phân phối tự nhiên nhất của comic-studio (tác giả Canvas) **bị chặn ngay ở cửa** — không phải vì thua về sản phẩm, mà vì mất đường đi.
**Nhưng** khoảng cách phân khúc vẫn còn: Constella nhắm creator **đã biết vẽ** (nó chuyển 3D model sang **đúng nét vẽ của chính creator**), còn comic-studio nhắm **tác giả truyện chữ không biết vẽ**. Hai phân khúc khác nhau — và khoảng cách đó **có thể** hẹp lại. ⚠️ Trạng thái rollout của Constella **chưa xác nhận được** (nguồn fetch fail, chỉ có snippet) — xem [§7](#7-khoảng-trống-dữ-liệu), khoảng trống 2.d.

---

## 4. Mô hình kinh doanh & pricing

> Phần unit economics của chính comic-studio (chi phí/chapter, hệ số N=3, margin âm ở power user, bốn đường ra) nằm ở [Analysis-Comic-Studio-Concept.md](./Analysis-Comic-Studio-Concept.md) §9b. Mục này **không nhắc lại** các con số đó; nó cung cấp **tiền lệ ngành** để đọc chúng.

### 4.1 BYOK — ai đang chạy thật

Câu hỏi: **có AI SaaS nào chạy BYOK thành công không?** — **Có, và có một comp gần như hoàn hảo.**

| Sản phẩm | Lĩnh vực | Định giá phần mềm | Bằng chứng quy mô | Nhãn |
|---|---|---|---|---|
| ⭐⭐ **Novelcrafter** | **Novel writing** — phân khúc **kề cận nhất** | **4 tier: Scribe $4 · Hobbyist $8 · Artisan $14 · Specialist $20**/tháng. **Scribe $4 = KHÔNG có AI.** BYOK mở khoá từ **Hobbyist $8**. **Nền tảng KHÔNG bán credit, KHÔNG có AI hosted** | **220.000+ authors** · ~120 quốc gia · Discord **9.825** members | `[OFF]` |
| **TypingMind** | Chat UI | **$39 one-time lifetime** + BYOK | **$1M lifetime / 20 tháng**; **$130–160K/tháng**; bootstrapped; có khách Fortune 500 hợp đồng **3.000 seat** | `[TC]` |
| **JetBrains AI** | IDE | Credit + BYOK **song song** | — | `[TC]` |
| **Natively AI** | Meeting assistant | **Free = BYOK. Paid = managed** | Không có số revenue | `[TC]` |
| **Cline / Aider / Roo Code / Continue / Zed** | Coding agent | **Free/OSS**, 100% BYOK | Adoption lớn, **không monetize qua license** | `[TC]` |
| **AI-Flow** | **Image/video workflow** | *"pay providers directly — no platform markup, no subscription"* | Không có số | `[TC]` |
| **ComfyUI** | **Image pipeline** | OSS, free | Adoption rất lớn | `[TC]` |
| **DM Champ** | Marketing SaaS | Managed + BYOK | *"one of the **rare** managed SaaS platforms that supports BYOK for **non-technical** buyers"* | `[TC]` |
| **OpenRouter** | Router | BYOK fee **5%** | — | `[TC]` |

> [!IMPORTANT]
> **Novelcrafter là comp cần dùng.** Nó chứng minh **đồng thời ba điều**:
> 1. **BYOK bán được cho tác giả (writer), không chỉ cho developer** — **220.000 authors** `[OFF]`.
> 2. **Mức platform fee $5–15 là ĐÚNG BIÊN** — Novelcrafter thu **$4–20** `[OFF]` và **không hề bán inference**.
> 3. **Tier $4 không-AI là pattern đáng copy**: cho người dùng vào sản phẩm (editor, Story Bible/Codex) **trước khi** phải đối mặt với API key. Đây là câu trả lời **kiến trúc** cho vấn đề friction — và comic-studio có cấu trúc y hệt: Story Bible editor + Comic IR + layout editor đều **không đốt inference**.

### 4.2 Ma sát onboarding BYOK — không có số

> [!CAUTION]
> **KHÔNG CÓ SỐ LIỆU ĐỊNH LƯỢNG VỀ MA SÁT BYOK.**
> Đã tìm: 3 lần search + fetch trends.vc (**HTTP 403**) + fetch kompozy. Chỉ thu được benchmark onboarding SaaS **chung** và mô tả **định tính**. **Không có A/B test hay cohort nào tách riêng biến "nhập API key".**

| Bằng chứng | Giá trị | Nhãn |
|---|---|---|
| Baymard friction formula | `Friction = (Required Fields × 1,5) + (Required Decisions × 2) + (External Dependencies × 3)`. Score **>15** ⇒ abandonment **>50%** | `[TC]` — **không đo BYOK** |
| → Áp cho BYOK | API key là external dependency ⇒ rơi vào hệ số nặng nhất (**×3**) | `[EM]` — **suy luận, không phải đo** |
| Onboarding drop-off SaaS chung | **30–50%**; **80%** user rời trong 3 ngày; B2B activation trung bình **37,5%** | `[TC]` |
| Time-to-first-value (TTFV) | **>30 phút** ⇒ abandonment **cao gấp 3x** so với <10 phút | `[TC]` |
| Chi phí thời gian setup BYOK | *"Plan an hour per provider for first-time setup"*; vận hành **1–2 giờ/tháng** ở quy mô; key rotation **60–90 ngày**; OpenAI tier 3 cần **$250+** lịch sử chi tiêu **+ chờ 14 ngày** | `[TC]` — **vendor blog của một platform managed** ⇒ có động cơ phóng đại |
| → Ghép hai số | "1 giờ setup" **gấp đôi ngưỡng 30 phút** của TTFV ⇒ **BYOK bắt buộc ngay từ signup là cấu hình rủi ro cao nhất** | `[EM]` — **ghép hai nguồn không liên quan** |

### 4.3 Ba cấu hình lai của ngành (A / B / C)

Giả thiết ban đầu — *"free tier dùng key nền tảng, tier cao BYOK"* — **không tìm được sản phẩm nào chạy đúng cấu hình đó**. Ba cấu hình thực tế của ngành đều **đảo ngược** nó:

| Cấu hình thực tế | Ví dụ | Logic |
|---|---|---|
| **A. Tier rẻ = KHÔNG AI · tier trên = BYOK · KHÔNG BAO GIỜ managed** | **Novelcrafter** ($4 no-AI → $8+ BYOK) `[OFF]` | Nền tảng **không bao giờ** chạm inference ⇒ **không có COGS** |
| **B. Free = BYOK · Paid = MANAGED** (ngược hẳn) | **Natively AI** `[TC]` | BYOK là cách rẻ để **thử**; người dùng **trả tiền để KHÔNG phải cắm key** ⇒ *convenience* mới là thứ bán được |
| **C. Tier rẻ self-serve = BYOK · Tier premium = managed credits** | **JetBrains**, **DM Champ** `[TC]` | *"BYOK with full model choice on a cheaper self-serve plan for the technical crowd, managed credits on a premium plan for everyone who just wants it to work"* |

**Vì sao ngành đảo ngược giả thiết?** Vì **BYOK tự lọc người dùng technical**. Đặt BYOK ở tier cao là bắt người trả nhiều tiền nhất chịu nhiều friction nhất — ngược logic. `[EM — diễn giải từ pattern A/B/C]`

### 4.4 Ngưỡng hoà vốn ~125 ảnh/tháng

**Điểm hoà vốn BYOK vs managed, theo loại output:**

| Loại output | Ngưỡng hoà vốn BYOK | Nhãn |
|---|---|---|
| Text post | ~700 output/tháng | `[TC]` — vendor blog |
| ⭐ **Ảnh (DALL·E 3)** | **~125 ảnh/tháng** | `[TC]` — vendor blog |
| Video 60s | ~25 video/tháng | `[TC]` — vendor blog |
| Khuyến nghị chung | **<50/tháng** → managed thắng · **50–200** → tuỳ mix · **200+** → BYOK thắng | `[TC]` |

> [!IMPORTANT]
> **Ngưỡng 125 ảnh/tháng chia đúng hai loại user, và cả hai đều tồn tại.**
>
> | Loại user | Khối lượng | Ai thắng |
> |---|---|---|
> | "Làm vài trang thử" | **42 ảnh/tháng** `[TC]` — mức trung bình của user AI | **Managed / credit thắng.** BYOK là friction thuần tuý |
> | "Làm 1 chapter/tháng trở lên" | **180 ảnh** `[EM]` — 60 panel × hệ số N=3 | **BYOK thắng rõ**, và đây đúng là nhóm user gây margin âm ở [Analysis-Comic-Studio-Concept.md](./Analysis-Comic-Studio-Concept.md) §9b |
>
> ⇒ Người dùng trung bình **nằm sâu dưới ngưỡng**, nhưng **vượt ngưỡng ngay ở chapter đầu tiên** nếu thật sự làm truyện. Đây là lý do câu hỏi "BYOK hay credit" **không có đáp án nhị phân**.

**Cấu hình được khuyến nghị — cấu hình A của Novelcrafter, có cửa thoát cho power user:**

| Tầng | Nội dung | Vì sao |
|---|---|---|
| **1. Tier $4–8: KHÔNG có image gen** | Story Bible editor + Comic IR + layout + versioning + export | Margin ~90% `[EM]`, **không COGS**, **không cần API key** ⇒ TTFV thấp. Đây là tier chứng minh giá trị |
| **2. Credit pack không hết hạn** | Cho người dùng thường (**<125 ảnh/tháng** `[TC]`) | Managed, có margin, không bắt ai cắm key |
| **3. BYOK là TÙY CHỌN mở khoá ở tier trả phí** | Cho power user vượt **125 ảnh/tháng** `[TC]` | Họ **tự có động cơ kinh tế** để cắm key — tiết kiệm tiền cho chính họ, không phải mình ép |

Cấu hình này giữ nguyên các căn cứ ủng hộ BYOK ở [Analysis-Comic-Studio-Concept.md](./Analysis-Comic-Studio-Concept.md) §9b.4, **nhưng gỡ được điểm yếu duy nhất** của nó (friction với non-technical user) — vì **không ai bị bắt cắm key để dùng sản phẩm**.

**Comp Novelcrafter — đối chiếu 1:1 với cấu hình trên:**

| Chiều | Novelcrafter `[OFF]` | comic-studio (đề xuất) |
|---|---|---|
| Tier vào cửa | **Scribe $4**, không AI | **$4–8**, không image gen |
| Nơi BYOK xuất hiện | Từ **Hobbyist $8** | Tuỳ chọn ở tier trả phí |
| Nền tảng có bán inference không | **Không, không bao giờ** | **Có** — credit pack cho tầng giữa (khác biệt duy nhất) |
| Bằng chứng segment | **220.000+ authors**, ~120 quốc gia | Chưa có |
| Kênh support/product update chính | **Discord 9.825 members** `[OFF]` | Xem [§6](#6-kênh-phân-phối) |

⚠️ Khác biệt duy nhất giữa hai cấu hình là tầng credit pack — và đó chính là tầng **không có tiền lệ retention nào** để đối chiếu (xem [§5](#5-retention-benchmark) và khoảng trống 4.d).

---

## 5. Retention benchmark

### 5.1 23% GRR — ChartMogul, và ba caveat bắt buộc

**Con số 23% GRR xác minh được. Có thật, có methodology.**
Chuỗi truy nguyên: `saasultra.com` (aggregator) → tự khai nguồn **ChartMogul SaaS Retention Report** → fetch trực tiếp báo cáo ChartMogul → **khớp hoàn toàn**. Xác nhận chéo lần thứ ba bởi VentureCurator (25/06/2026).

| Thuộc tính | Giá trị | Nhãn |
|---|---|---|
| **Nguồn gốc** | **ChartMogul — "The SaaS Retention Report: The AI churn wave"** | `[OFF]` |
| **Cỡ mẫu** | **~3.500 software companies**: ~2.700 B2B SaaS · ~600 B2C SaaS · **~200 AI-native** | `[OFF]` |
| **Năm dữ liệu** | **2025** (tháng 1 → tháng 9/2025) | `[OFF]` |
| **Ngưỡng lọc** | Chỉ công ty **≥ $250K ARR** | `[OFF]` |
| **Ngày xuất bản** | Không ghi rõ trên trang | ❌ không xác định |

| Price band | GRR | NRR | Nhãn |
|---|---|---|---|
| **< $50/tháng** | **23%** | **32%** | `[OFF]` ChartMogul |
| $50–249/tháng | **45%** | **61%** | `[OFF]` |
| > $250/tháng | **70%** | **85%** | `[OFF]` |
| AI-native tổng thể (median 09/2025) | **40%** | **48%** | `[OFF]` |
| B2B SaaS (median NRR) | — | **82%** | `[OFF]` |
| B2C SaaS (median NRR) | — | **49%** | `[OFF]` |

> [!WARNING]
> **BA CAVEAT PHẢI ĐI KÈM CON SỐ 23%. Trích 23% mà bỏ ba dòng này là trích sai.**
>
> 1. **Cohort AI-native chỉ có ~200 công ty** `[OFF]`, và band `<$50` là **một tập con** của 200 đó. ChartMogul **không công bố n của riêng band này** — nó **có thể chỉ vài chục công ty**.
> 2. **Bộ lọc ≥$250K ARR loại bỏ toàn bộ sản phẩm quy mô indie** `[OFF]` — tức loại đúng nhóm mà comic-studio sẽ thuộc về (SOM năm 1 ước **$4–14K ARR** `[EM]`). **Không có bằng chứng nào cho thấy 23% áp được cho indie scale.**
> 3. **Đây là dữ liệu 2025, không phải 2026.**

> [!IMPORTANT]
> **Luận điểm chính vẫn đứng vững, và còn mạnh hơn.** ChartMogul kết luận: *"AI-native products that sell for >$250 per month see 70% GRR and 85% NRR. This is essentially the same as B2B SaaS"* `[OFF]`.
> ⇒ **Vấn đề không phải "AI churn". Vấn đề là GIÁ.** Comic-studio ở mức $5–20/tháng nằm trọn trong band tệ nhất.

> [!CAUTION]
> **Luận điểm *"credit pack không hết hạn né được 23% GRR"* là một LẬP LUẬN LOGIC, KHÔNG PHẢI SỐ ĐO.**
> Lập luận: credit pack ghi nhận doanh thu **trước**, nên về mặt kế toán nó không chịu cùng cơ chế churn hàng tháng của subscription.
> **Nhưng không tìm được bất kỳ dữ liệu retention nào cho mô hình credit pack** để kiểm chứng lập luận đó — xem khoảng trống **4.d** ở [§7](#7-khoảng-trống-dữ-liệu).
> ⇒ Trong mọi tài liệu, luận điểm này **phải được ghi kèm nhãn `[EM]`** và không được trình bày như một benchmark.

### 5.2 RevenueCat — dataset độc lập, KHÔNG được gộp

**RevenueCat — State of Subscription Apps 2026** là một dataset **hoàn toàn khác** ChartMogul:

| Chỉ số | AI apps | Non-AI apps | Nhãn |
|---|---|---|---|
| **Retention 12 tháng (annual plan)** | **21,1%** | **30,7%** | `[TC]` |
| Retention monthly plan | **6,1%** | **9,5%** | `[TC]` |
| Realized LTV / năm | **$30,16** | **$21,37** | `[TC]` |
| Cỡ mẫu | ~**115.000** app, >**$11B** revenue/năm, >**1 tỷ** giao dịch; AI apps chiếm **27,1%** mẫu | | `[TC]` |
| Ngày xuất bản | **10/03/2026** | | `[TC]` |
| So với 2025 | AI app 12-month payer retention **9,2% / 11,5%** — *ngang* app truyền thống ⇒ **sụt giảm 2026 là hiện tượng MỚI** | | `[TC]` |

> [!WARNING]
> **KHÔNG ĐƯỢC GỘP HAI BỘ SỐ NÀY.**
> - ChartMogul đo **GRR — gross revenue retention** của **SaaS**.
> - RevenueCat đo **payer retention** của **mobile subscription app**.
>
> **GRR ≠ payer retention.** Hai metric khác nhau về định nghĩa, mẫu và đơn vị đo. **Không cộng, không lấy trung bình, không so sánh trực tiếp** (ví dụ: nói "23% và 21,1% khớp nhau" là **sai**).
>
> Giá trị thật của RevenueCat nằm ở chỗ khác: nó là **một dataset độc lập, cỡ mẫu lớn hơn ~30 lần**, và nó **xác nhận CÙNG CHIỀU** — sản phẩm AI giữ chân kém hơn sản phẩm không-AI.

### 5.3 Không có benchmark cho creative tool $5–20/tháng

> [!CAUTION]
> **KHÔNG FIRM NÀO TÁCH SEGMENT "creative tool" HAY "comic/art tool" RIÊNG.**
> Proxy gần nhất hiện có chỉ có hai: band `<$50/tháng` của ChartMogul (**23% GRR** `[OFF]`) và AI-app 12-month của RevenueCat (**21,1%** `[TC]`).
> Comic-studio ở mức giá **$5–20/tháng** nằm trọn trong **band tệ nhất của cả hai dataset** — nhưng cả hai đều là proxy, không phải benchmark của đúng ngách.

---

## 6. Kênh phân phối

### 6.1 Bảng kênh

| Kênh | Ví dụ có số | Kết quả | Nhãn |
|---|---|---|---|
| ⭐ **Build-in-public trên X + freemium** | **Anifusion** — solo, **$0 marketing spend**, **KHÔNG làm SEO** | **$833 MRR**, có lãi ⚠️ (mâu thuẫn $5.000/tháng — [§2.3](#23-som--reference-class-của-sản-phẩm-1-dev)). Nguyên văn: *"Despite not investing in traditional marketing or SEO, Anifusion achieved revenue milestones by leveraging authentic social media engagement"*; phong cách *"shitposting"* | `[TC]` |
| ❌ **Show HN** | **ComicInk**, 30/04/2026 | **2 điểm · 2 comment.** Kênh **chết** với ngách này | `[OFF]` HN API |
| ⭐⭐ **Comparison-listicle SEO** | Quan sát qua 8 lần search: taleatelier.com, comicpad.app, comicsai.org, gentoon.ai, jenova.ai, anifusion.ai, comicink.ai/blog, llamagen.ai đều xuất bản trang listicle | **Kênh thống trị ngách** — gần như mọi kết quả search về *"AI comic tool"* đều do **chính đối thủ tự viết**, không phải báo chí | `[EM]` — **quan sát SERP, KHÔNG phải số traffic** |
| ⭐ **Discord tác giả** | WEBTOON official **17.777 members** · WEBTOON HQ **5.000+** · Webtoon Club **1.460** · Webtoon Canvas Creators · **Novelcrafter Discord 9.825** | Nơi tập trung đúng phân khúc. Novelcrafter dùng Discord làm kênh support + product update **chính thức** | `[TC]` / `[OFF]` (Novelcrafter) |
| **Forum nền tảng** | Tapas Forum có thread creator hỏi nhau về công cụ | Không có số traffic | `[TC]` |
| **Reddit** | r/comics **3,8M subscribers** (07/2026) | Có quy mô, **nhưng là cộng đồng độc giả + hoạ sĩ truyền thống** ⇒ xem [§6.2](#62-rủi-ro-ngược-của-kênh-cộng-đồng) | `[TC]` |
| **Marketplace asset** | **Clip Studio Assets** (template, panel tool, speech balloon) · **Gumroad** | Không tra được số. Nhưng là nơi tác giả webtoon **đã có thói quen cài thêm công cụ** | `[TC]` |

### 6.2 Rủi ro ngược của kênh cộng đồng

> [!WARNING]
> **Cộng đồng tác giả comic là kênh CÓ RỦI RO NGƯỢC, không phải kênh trung tính.**
>
> Bằng chứng: **Naver Webtoon bị độc giả tổ chức boycott subscription** khi đăng tác phẩm AI `[TC]`; **BlueLine Studio bị buộc vẽ lại episode** *Knight King* sau khi fan phát hiện background có AI-polish `[TC]`. Pattern rút ra: *"covert use can corrode brand trust more than disclosure ever could."*
>
> ⇒ **Hệ quả:** một launch post kiểu *"AI biến truyện chữ thành comic"* đăng vào r/comics hoặc Discord WEBTOON **có xác suất phản tác dụng cao**. Kênh cộng đồng chỉ hoạt động khi thoả **đồng thời** hai điều kiện:
> 1. **Positioning disclosure-first** — nói rõ AI-assisted ngay từ đầu.
> 2. Nhắm vào **tác giả truyện chữ (writer)** — nhóm **không cạnh tranh** với hoạ sĩ — **chứ không** vào cộng đồng hoạ sĩ.
>
> Bằng chứng ủng hộ hướng "writer, không phải artist": **Novelcrafter 220K authors** `[OFF]` cho thấy cộng đồng **viết** chấp nhận AI tool ở quy mô lớn, trong khi cộng đồng **vẽ** thì boycott.
>
> ⚠️ Đây là ràng buộc **thu hẹp** không gian kênh, không mở rộng nó.

### 6.3 Key Result đo được

| Kênh | Key Result đề xuất | Neo bằng chứng |
|---|---|---|
| **Build-in-public trên X** | **1 post/tuần × 12 tuần**; đạt **500 follower** + **50 email waitlist** | Anifusion đạt **$833 MRR** `[TC]` bằng đúng kênh này với **$0 spend** |
| **SEO listicle/comparison** | **12 trang** so sánh + how-to; **top-10** cho **≥3 keyword** dạng *"novel to comic AI"* | **8/8** đối thủ trong SERP đều làm `[EM]` |
| **Discord tác giả** | Tham gia **5 server**; **20 cuộc trò chuyện 1-1** với tác giả **trước khi** ship MVP1 | WEBTOON official **17.777** `[TC]`; đồng thời là cách lấp khoảng trống WTP (**1.c**) |
| ❌ **KHÔNG làm** | **Show HN, Product Hunt** làm kênh chính | ComicInk Show HN = **2 điểm** `[OFF]` |
| **Positioning bắt buộc** | **100%** nội dung marketing nêu rõ AI-assisted + nhắm **writer**, không nhắm artist | Boycott Naver + BlueLine `[TC]` |

---

## 7. Khoảng trống dữ liệu

Mục này **bắt buộc và phải đầy đủ**. **23 khoảng trống**, gom theo năm nhóm câu hỏi. Mã (ví dụ `1.c`) giữ nguyên để truy vết ngược về nguồn.

> Đây là khoảng trống **thị trường & thương mại**. Khoảng trống về **công nghệ và pháp lý** nằm ở [Analysis-Comic-Studio-Concept.md](./Analysis-Comic-Studio-Concept.md) §11 — **không lặp lại ở đây**.

### Nhóm 1 — Quy mô thị trường (4 mục)

| Mã | Khoảng trống | Trạng thái |
|---|---|---|
| **1.a** | **Số creator Canvas official** — `ir.webtoon.com` **timeout 60s**; Forbes fetch được nhưng **không chứa số** | ❌ Chưa lấp. Con số 2,2M **series** `[TC]` không thay thế được |
| **1.b** | **Market size cho creator tooling** — **không firm nào tách segment này** | ❌ Không tồn tại công khai. Đây là lý do SAM buộc phải là `[EM]` |
| **1.c** | **Tỉ lệ creator sẵn sàng trả tiền (willingness-to-pay)** | ❌ Chưa lấp — trùng với khoảng trống WTP đã ghi nhận ở [Analysis-Comic-Studio-Concept.md](./Analysis-Comic-Studio-Concept.md) §11. **Cách lấp đề xuất: 20 cuộc trò chuyện 1-1 ở [§6.3](#63-key-result-đo-được)** |
| **1.d** | **Số series trung bình mỗi creator** — giả định **÷4** dùng trong kịch bản "Trung bình" | ❌ **Không có nguồn.** Đây là thừa số làm cả kịch bản trung bình thành `[EM]` |

### Nhóm 2 — Đối thủ (5 mục)

| Mã | Khoảng trống | Trạng thái |
|---|---|---|
| **2.a** | **Team / funding của ComicInk, TaleAtelier, Comicsmaker.ai, Jenova** | ❌ Không có profile Tracxn/Crunchbase |
| **2.b** | **Shutdown khác ngoài Comicpad** | ❌ Không tìm thêm được cái nào |
| **2.c** | **Benchmark consistency có số của bất kỳ đối thủ nào** | ❌ **Không đối thủ nào công bố.** Jenova chỉ có marketing claim; ComicInk chỉ mô tả cơ chế, không có số |
| **2.d** | **Trạng thái rollout của Constella** | ❌ Fetch nguồn **fail** (socket hang up). **Chưa xác nhận đã ship hay còn là announcement** — điều này ảnh hưởng trực tiếp tới mức độ cấp bách của rủi ro nền tảng ở [§3.2](#32-ba-kết-luận) |
| **2.e** | **Entrant mới được đưa tin** | ❌ Không tìm được cái nào |

### Nhóm 3 — Mô hình BYOK (5 mục)

| Mã | Khoảng trống | Trạng thái |
|---|---|---|
| **3.a** | **Conversion / drop-off riêng cho bước nhập API key** | ❌ **Không tồn tại công khai.** Mọi kết luận về friction BYOK ở [§4.2](#42-ma-sát-onboarding-byok--không-có-số) đều là `[EM]` |
| **3.b** | **Ví dụ BYOK trong ngách image gen thương mại có số revenue** | ❌ Không có. AI-Flow và ComfyUI đều không công bố số |
| **3.c** | **Cấu hình "free = platform key, paid = BYOK"** | ❌ **Không tìm được tiền lệ nào.** ⇒ không có cơ sở để tự chế cấu hình này |
| **3.d** | **ARR của Novelcrafter** | ❌ Không công bố. Và **220K "authors" không rõ là user hay paying user** — caveat này áp cho mọi chỗ dùng con số 220K trong tài liệu |
| **3.e** | **Bias của nguồn kompozy** | ⚠️ Đã đánh giá: số đến từ **vendor bán managed** nên có bias. **Nhưng** họ vẫn khuyến nghị BYOK ở **>200 output/tháng**, tức bias **ngược chiều lợi ích của chính họ** ⇒ độ tin cậy **chấp nhận được** |

### Nhóm 4 — Retention (4 mục)

| Mã | Khoảng trống | Trạng thái |
|---|---|---|
| **4.a** | **n của riêng band `<$50/tháng`** trong dataset ChartMogul | ❌ Không công bố. Có thể chỉ vài chục công ty |
| **4.b** | **Ngày xuất bản báo cáo ChartMogul** | ❌ Không ghi trên trang |
| **4.c** | **Benchmark cho creative / art / comic tool** | ❌ **Không tồn tại.** Xem [§5.3](#53-không-có-benchmark-cho-creative-tool-520tháng) |
| **4.d** | ⭐ **Retention của mô hình credit pack (không hết hạn) so với subscription** | ❌ **Không tìm được.** Đây là khoảng trống nằm **trực tiếp dưới khuyến nghị pricing** ở [§4.4](#44-ngưỡng-hoà-vốn-125-ảnhtháng): luận điểm *"credit pack né được 23% GRR"* **chưa có bằng chứng nào** — nó là **lập luận logic** (doanh thu ghi trước), **không phải số đo** |

### Nhóm 5 — Kênh phân phối (5 mục)

| Mã | Khoảng trống | Trạng thái |
|---|---|---|
| **5.a** | **Dữ liệu Product Hunt launch của Dashtoon / Anifusion** | ❌ Không tra được |
| **5.b** | **Số subscriber của r/webtoons** | ❌ Không tra được. Chỉ có r/comics **3,8M** `[TC]`, mà đó là cộng đồng **sai phân khúc** |
| **5.c** | **Traffic thật của kênh SEO listicle** | ❌ Không có. Kết luận *"SEO thống trị ngách"* là **quan sát SERP `[EM]`**, không phải số đo |
| **5.d** | **Tool AI nào phân phối qua marketplace asset** | ❌ Không tìm được ví dụ nào |
| **5.e** | ⚠️ **Kênh phân phối ở thị trường Việt Nam** | ❌ **CHƯA TRA — hết ngân sách tool call của vòng nghiên cứu.** Đây là khoảng trống **có thể lấp được** (khác với các mục "không tồn tại" ở trên) và **phải là ưu tiên của vòng nghiên cứu kế tiếp**, vì comic-studio chịu ràng buộc pháp lý Việt Nam nhưng chưa có một dòng dữ liệu nào về kênh đi tới người dùng Việt Nam |

---

## Tài liệu tham khảo

> **Ngày truy cập toàn bộ URL: 23/08/2026.** Nhãn trong ngoặc là hạng nguồn áp cho dữ liệu lấy từ URL đó.

### Báo cáo thị trường (TAM) — §2.1

1. [Mordor Intelligence — Webtoons Market](https://www.mordorintelligence.com/industry-reports/webtoons-market) `[BCN]`
2. [Grand View Research — Webtoons Market Report](https://www.grandviewresearch.com/industry-analysis/webtoons-market-report) `[BCN]`
3. [Research and Markets — Webtoon](https://www.researchandmarkets.com/report/webtoon) `[BCN]`
4. [IMARC Group — Webtoons Market Statistics](https://www.imarcgroup.com/webtoons-market-statistics) `[BCN]`
5. [market.us — Webtoons Market](https://market.us/report/webtoons-market/) `[BCN]`
6. [Fortune Business Insights — Webcomics Market](https://www.fortunebusinessinsights.com/webcomics-market-105731) `[BCN]`

### Input đo được cho SAM — §2.2

7. [Wikipedia — Tapas (website)](https://en.wikipedia.org/wiki/Tapas_(website)) `[TC]`
8. [Gitnux — Webtoon Industry Statistics](https://gitnux.org/webtoon-industry-statistics/) `[TC]`
9. [Novelcrafter — homepage](https://www.novelcrafter.com/) `[OFF]`
10. [Novelcrafter — Community Update 09/2025](https://www.novelcrafter.com/blog/2025-09-community-update) `[OFF]`

### Reference class SOM — §2.3

11. [Starter Story — Anifusion breakdown](https://www.starterstory.com/anifusion-ai-breakdown) `[TC]`
12. [MaxIncubator — AI comic creation tool $5K/month](https://ideas.maxincubator.com/ai-comic-creation-tool-5k-month/) `[TC]` ⚠️ mâu thuẫn với #11
13. [GetLatka — TypingMind](https://getlatka.com/companies/typingmind) `[TC]`
14. [MWM — ComicInk (App Store data)](https://mwm.ai/apps/comicink/6760571933) `[TC]`

### Đối thủ — §3

15. [Tracxn — Dashtoon](https://tracxn.com/d/companies/dashtoon/__fyb3bu53aHKlNq-E11RgO5SgmUncP_QslwzZGvYeNqc) `[TC]`
16. [TechCrunch — Dashtoon (02/11/2023)](https://techcrunch.com/2023/11/02/dashtoon/) `[TC]`
17. [Publishers Weekly — GlobalComix "the Figma for comics"](https://www.publishersweekly.com/pw/by-topic/industry-news/comics/article/100003-globalcomix-wants-to-create-the-figma-for-comics-with-new-funding-and-ceo.html) `[TC]`
18. [The Next Web — GlobalComix $13M + INKR acquisition](https://thenextweb.com/news/globalcomix-13m-inkr-acquisition) `[TC]`
19. [CBR — WEBTOON AI product (Constella)](https://www.cbr.com/webtoon-controversial-ai-product-develop/) `[TC]` ⚠️ fetch fail, chỉ lấy được snippet
20. [KoreaProductPost — Naver Webtoon AI services](https://koreaproductpost.com/naver-webtoon-ai-services-toon-radar-painter-filter-chat/) `[TC]`
21. [Anime News Network — WEBTOON byUs (11/07/2026)](https://www.animenewsnetwork.com/news/2026-07-11/webtoon-launches-ai-story-chat-service-byus-featuring-creator-approved-webtoon-ip/.239448) `[TC]`
22. [Hacker News — ComicInk Show HN (item 47964060)](https://news.ycombinator.com/item?id=47964060) `[OFF]`
23. [OpenPR — ComicInk video generation](https://www.openpr.com/news/4570303/comicink-debuts-video-generation-capabilities) `[TC]`
24. [Jenova — AI Webtoon Creator](https://www.jenova.ai/en/resources/ai-webtoon-creator) `[TC]` ⚠️ marketing claim, không benchmark
25. [Mage Space Blog — Best AI comic generators 2026](https://blog.mage.space/article/best-ai-comic-generators-2026/bf9d1669-438a-49ee-8a60-68f2e7710601) `[TC]`

### BYOK & pricing — §4

26. [Novelcrafter — Pricing](https://www.novelcrafter.com/pricing) `[OFF]`
27. [Natively AI — Pricing](https://natively.software/blog/natively-ai-pricing) `[TC]`
28. [GitHub — awesome-byok-apps](https://github.com/yatsyk/awesome-byok-apps) `[TC]`
29. [AI-Flow — BYOK](https://ai-flow.net/byok/) `[TC]`
30. [DM Champ — Best AI tools BYOK 2026](https://dmchamp.com/best/best-ai-tools-byok-2026/) `[TC]`
31. [SaaS Factor — The science of SaaS onboarding (Baymard friction formula)](https://www.saasfactor.co/blogs/the-science-of-saas-onboarding-a-comprehensive-framework-for-reducing-friction-improving-activation-and-preventing-churn) `[TC]`
32. [Chameleon — Reducing onboarding drop-off](https://www.chameleon.io/blog/reducing-onboarding-drop-off-and-improving-activation-rates) `[TC]`
33. [Kompozy — BYOK vs managed](https://kompozy.io/ai-content-tools/byok-vs-managed) `[TC]` ⚠️ vendor blog của platform managed — xem khoảng trống 3.e

### Retention — §5

34. [ChartMogul — The SaaS Retention Report: The AI churn wave](https://chartmogul.com/reports/saas-retention-the-ai-churn-wave/) `[OFF]`
35. [VentureCurator — Below this price, AI products churn (25/06/2026)](https://www.venturecurator.com/p/below-this-price-ai-products-churn) `[TC]`
36. [TechCrunch — AI-powered apps struggle with long-term retention (10/03/2026, RevenueCat)](https://techcrunch.com/2026/03/10/ai-powered-apps-struggle-with-long-term-retention-new-report-shows) `[TC]`

### Kênh phân phối — §6

37. [HN Algolia API — item 47964060 (Show HN ComicInk)](https://hn.algolia.com/api/v1/items/47964060) `[OFF]`
38. [Disboard — Discord server tag "webtoon"](https://disboard.org/servers/tag/webtoon) `[TC]`
39. [Tapas Forums — Small Discord servers for comic creators](https://forums.tapas.io/t/small-discord-servers-for-comic-creators/72597) `[TC]`
40. [ReddTrends — r/comics](https://www.reddtrends.com/r/comics) `[TC]`
41. [Clip Studio Assets](https://assets.clip-studio.com/en-us) `[TC]`

### Tài liệu nội bộ liên quan

- [Analysis-Comic-Studio-Concept.md](./Analysis-Comic-Studio-Concept.md) — thẩm định khả thi kỹ thuật, pháp lý và unit economics (RESEARCH-001)
- [Charter-Comic-Studio.md](../010-Planning/Charter-Comic-Studio.md) — tài liệu neo quyết định cấp dự án
- [Glossary.md](../999-Resources/Glossary.md) — thuật ngữ chung
