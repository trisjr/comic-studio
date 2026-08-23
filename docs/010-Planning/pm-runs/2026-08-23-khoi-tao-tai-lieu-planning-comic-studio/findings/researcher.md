# Findings — `researcher`: Thị trường, đối thủ, mô hình kinh doanh

> Worker không có tool `Write` (tools: `Read, Glob, Grep, WebFetch, WebSearch`). PM ghi lại **nguyên văn** báo cáo của nó ở Mục A. Mục B, C là phần PM tự thêm.
> **Ngày truy cập toàn bộ URL**: 2026-08-23. Tool call dùng: 51/60.

---

# A. Kết luận của worker (nguyên văn)

## Quy ước nhãn (áp cho mọi con số bên dưới)

| Nhãn | Nghĩa |
|---|---|
| `[OFF]` | Nguồn official — trang pricing/IR/homepage của chính chủ, hoặc paper gốc |
| `[BCN]` | Báo cáo ngành — market research firm, có tên firm |
| `[TC]` | Thứ cấp — blog/aggregator dẫn lại, không phải chính chủ |
| `[EM]` | Ước lượng hoặc phép nhân của worker từ giả định — **không phải số đo được** |

---

## Câu 1 — Quy mô thị trường (TAM / SAM / SOM)

### 1.1. TAM — bảng phân kỳ giữa các firm

Các báo cáo **không chênh nhau vì sai** mà vì **định nghĩa thị trường khác nhau**.

| # | Firm | Định nghĩa | Giá trị hiện tại | Dự báo | CAGR | Nhãn | Nguồn |
|---|---|---|---|---|---|---|---|
| 1 | **Mordor Intelligence** | Webtoons | **$10,85B (2025) → $14,44B (2026)** | **$60,25B (2031)** | **33,1%** (2026–31) | `[BCN]` verify bằng fetch trực tiếp | [mordorintelligence.com](https://www.mordorintelligence.com/industry-reports/webtoons-market) |
| 2 | **Grand View Research** | Webtoons | $8,3B (2023) → $18,3B (2026) | $45,3B (2030) | 27,3% (2024–30) | `[BCN]` qua search snippet | [grandviewresearch.com](https://www.grandviewresearch.com/industry-analysis/webtoons-market-report) |
| 3 | **TBRC / Research&Markets** | Webtoons | $10,75B (2025) → $14,02B (2026) | — | 30,5% | `[BCN]` qua search snippet | [researchandmarkets.com](https://www.researchandmarkets.com/report/webtoon) |
| 4 | **IMARC Group** | Webtoons | $11,8B (2025) | $101,8B (2034) | 26,26% (2026–34) | `[BCN]` qua search snippet | [imarcgroup.com](https://www.imarcgroup.com/webtoons-market-statistics) |
| 5 | **market.us** | Webtoons | — | — | 28,1% | `[BCN]` | [market.us](https://market.us/report/webtoons-market/) |
| 6 | Không rõ firm | **Digital comics** (hẹp hơn) | $5,806M (2025) → $6,306M (2026) | $14,4B (2034) | **10,4%** | `[TC]` | search result |
| 7 | **Fortune Business Insights** | **Webcomics** | $8,76B (2026) | $14,73B (2034) | **6,72%** | `[BCN]` qua search snippet | [fortunebusinessinsights.com](https://www.fortunebusinessinsights.com/webcomics-market-105731) |

**Đọc bảng này thế nào:**

- Cùng gọi là "webtoon", 2026 dao động **$14,0B – $18,3B**; CAGR **26,3% – 33,1%**.
- Nhưng khi đổi nhãn sang **"digital comics"** hoặc **"webcomics"**, CAGR sụp xuống **6,7% – 10,4%** — chênh **4–5 lần**. ⇒ **Con số CAGR 33% chỉ tồn tại dưới định nghĩa "webtoon" (bao gồm platform revenue, ads, IP licensing). Không được dùng nó cho thị trường công cụ.**
- ⭐ **Đã truy ra nguồn gốc số của run trước**: `$14,44B / $60,25B / 33,1%` mà run trước ghi *"từ nguồn thứ cấp abovea.tech"* → nguồn gốc là **Mordor Intelligence**, đã fetch trực tiếp xác nhận. Số này **nâng hạng từ `[TC]` lên `[BCN]`**.

**Sanity-check bằng dữ liệu công ty thật:**

| Chỉ số | Giá trị | Nhãn |
|---|---|---|
| WEBTOON Entertainment (WBTN) — guidance Q3/2026 | $358M–368M | `[OFF]` (đã có ở run trước) |
| ⇒ Annualize | **~$1,4–1,5B/năm** | `[EM]` — phép nhân ×4 từ số quý |
| WBTN MAU (toàn ecosystem, gồm Wattpad) | ~155 triệu | `[TC]` |
| WBTN trả cho creator 2021–2025 | **$2,7B**, cập nhật $2,8B tới 2026 | `[TC]` |

> ⚠️ **Mâu thuẫn cần PM biết**: platform số 1 thế giới làm **~$1,4–1,5B/năm** `[EM từ OFF]`. Nếu TAM 2026 thật sự là **$14–18B** `[BCN]`, WEBTOON chỉ chiếm **8–10%** một thị trường nó thống trị. Có thể đúng (Kakao, Lezhin, Piccoma, Kuaikan, Bilibili Comics chia phần còn lại), nhưng cũng là dấu hiệu các con số `[BCN]` tính cả những thứ ngoài "người trả tiền đọc webtoon". **Đừng dùng TAM $14B làm căn cứ cho bất kỳ quyết định nào.**

### 1.2. SAM — thị trường công cụ sáng tạo cho tác giả

> ### ❌ **KHÔNG CÓ DỮ LIỆU TRỰC TIẾP.**
> Đã tìm: (a) search "creator tools market webtoon"; (b) fetch trang Mordor — chỉ có *"South Korea alone counted 12,000 professional artists in 2024"* và *AI tools "trims page-level costs by 68%"*, **không có market size cho creator tooling**; (c) search "digital comics market" — mọi báo cáo đều đo **tiêu thụ**, **không firm nào tách segment công cụ tác giả**.
> **Không ai bán một con số này. Bất cứ số SAM nào cũng là phép nhân và phải được gắn nhãn như vậy.**

**Tầng A — INPUT ĐO ĐƯỢC:**

| Input | Giá trị | Nhãn | Nguồn | Caveat |
|---|---|---|---|---|
| Tapas — số creator | **>75.000** (từ 61.000 tháng 2/2021) | `[TC]` | [Wikipedia](https://en.wikipedia.org/wiki/Tapas_(website)) | Không phải trang official |
| Tapas — series / episode | 100.000 series, >1,6M episode; 80% là comic | `[TC]` | như trên | |
| WEBTOON Canvas — số series | **2,2 triệu series** | `[TC]` [gitnux.org](https://gitnux.org/webtoon-industry-statistics/) | ⚠️ **series ≠ creator** |
| Hàn Quốc — artist chuyên nghiệp | **12.000** (2024) | `[BCN]` Mordor | Chỉ Hàn Quốc, chỉ "professional" |
| WEBTOON Canvas ecosystem | Unified CANVAS 26/03/2026, 7 ngôn ngữ; hạ ngưỡng payout PayPal $100 → $25 | `[TC]` | Tín hiệu: WEBTOON đang **mở rộng** đáy creator |
| ⭐ **Novelcrafter — số tác giả** | **220.000+ authors** | `[OFF]` [novelcrafter.com](https://www.novelcrafter.com/) | Ngành **liền kề** (novel writing tool, BYOK, $4–20/mo) |
| Novelcrafter — độ phủ | "almost 120 countries" (15/09/2025) | `[OFF]` [blog](https://www.novelcrafter.com/blog/2025-09-community-update) | |

**Tầng B — PHÉP NHÂN (mọi dòng là `[EM]`, không phải dữ liệu):**

| Kịch bản | Creator addressable | × Tỉ lệ trả tiền | × ARPU/tháng | = SAM (ARR) | Giả định |
|---|---|---|---|---|---|
| **Thận trọng** | ~87.000 (Tapas 75K + KR pro 12K) `[EM — cộng hai nguồn khác chuẩn, có thể chồng lấn]` | 3% `[EM]` | $12 `[EM]` | **~$376K** | Chỉ đếm creator có nguồn số |
| **Trung bình** | 500.000 `[EM — suy từ 2,2M series ÷ ~4 series/creator]` | 3% `[EM]` | $12 `[EM]` | **~$2,2M** | Tỉ lệ 4 series/creator **không có nguồn** |
| **Lạc quan** | 1.000.000 `[EM]` | 5% `[EM]` | $15 `[EM]` | **~$9,0M** | |

> ⭐⭐ **Kết luận SAM — con số quan trọng nhất của Câu 1:**
> SAM = **$0,4M – $9M ARR** `[EM — 3/4 thừa số là giả định]`, tức **0,003% – 0,06% của TAM $14B**.
>
> **Ý nghĩa quyết định:** đây **không phải một thị trường lớn**. TAM webtoon $14B là thị trường **tiêu thụ nội dung**; thị trường **bán công cụ cho tác giả** nhỏ hơn 3–4 bậc độ lớn. Nếu Charter hoặc OKR trích TAM $14B để biện minh cho dự án, **đó là lỗi logic** — comic-studio không lấy tiền từ độc giả.
>
> Bằng chứng gián tiếp: toàn bộ ngách AI comic tool hiện có Dashtoon ($20,1M funding, 465 người), Anifusion (~$10K ARR), ComicInk, TaleAtelier, Comicpad (đóng cửa). **Không unicorn nào.** Đối chiếu: **Novelcrafter 220K authors** `[OFF]` cho thấy segment "tác giả tự viết dài, chịu trả $4–20/mo" **có thật và đo được** — nhưng đó là novel writing, không phải comic generation.

### 1.3. SOM — 1 dev, không ngân sách marketing

**Reference class — sản phẩm cùng hình dạng, có số công khai:**

| Sản phẩm | Mô hình | Doanh thu | Team | Nhãn | Nguồn |
|---|---|---|---|---|---|
| ⭐ **Anifusion** (AI comic, solo founder) | Subscription €20/mo + free tier 100 credit | **$833 MRR** · **$10.000 cumulative** kể từ launch 2024 · **có lãi** | **1 người** | `[TC]` | [starterstory.com](https://www.starterstory.com/anifusion-ai-breakdown) |
| Anifusion (số mâu thuẫn) | — | **"$5.000/tháng"**, ~220–250 paying subs | 1 | `[TC]` | [ideas.maxincubator.com](https://ideas.maxincubator.com/ai-comic-creation-tool-5k-month/) |
| **TypingMind** (BYOK chat UI) | $39 one-time + BYOK | **$1M lifetime trong 20 tháng**; hiện **$130–160K/tháng**; 2024 ARR $817,3K; bootstrapped | Nhỏ | `[TC]` | [getlatka](https://getlatka.com/companies/typingmind) |
| **ComicInk** (iOS app) | Credit pack | **<1.000 downloads**, 4.9★/27 rating, launch **19/03/2026** | — | `[TC]` | [mwm.ai](https://mwm.ai/apps/comicink/6760571933) |

> ⚠️ **Hai mâu thuẫn phải nói thẳng:**
> 1. **Anifusion: $833/tháng hay $5.000/tháng?** Hai nguồn `[TC]` khác nhau. Starter Story cụ thể hơn (tách MRR vs cumulative) nên nghiêng về **$833 MRR**, nhưng **không xác minh được**. Run trước ghi "Creator $9/mo"; Starter Story ghi **€20/month** — giá có thể đã đổi. **Cần fetch lại anifusion.ai/pricing nếu dùng số này để định giá.**
> 2. **ComicInk <1.000 downloads chỉ đo app iOS**, không đo web app. **Đừng đọc thành "ComicInk rất nhỏ"** — phép reverse-engineer unit economics của run trước dựa trên pricing web và vẫn đứng vững.

**SOM đề xuất:**

| Mốc | Paying user | ARPU | MRR | Nhãn | Neo |
|---|---|---|---|---|---|
| Năm 1 (thực tế) | 30–80 | $10–15 | **$300–1.200** | `[EM]` | Anifusion mất ~2 năm solo để tới $833 MRR |
| Năm 2 (tốt) | 150–300 | $12–15 | **$1.800–4.500** | `[EM]` | |
| Trần lạc quan | 800–1.500 | $15 | **$12K–22K** | `[EM]` | Trên mức này cần team hoặc marketing budget |

⇒ **SOM năm 1 ≈ $4K–14K ARR.** Đây là con số cần đặt vào OKR, **không phải** % của TAM $14B.

**Khoảng trống Câu 1**: (1.a) số creator Canvas official — ir.webtoon.com **timeout 60s**, Forbes fetch được nhưng không có số; (1.b) market size creator tooling — **không firm nào tách**; (1.c) tỉ lệ creator sẵn sàng trả tiền — **chưa lấp được**, vẫn là khoảng trống #12 của run trước; (1.d) số series/creator — giả định ÷4 **không có nguồn**.

---

## Câu 2 — Đối thủ: DELTA

> Đã có ở run trước, **không lặp**: ComicInk pricing, TaleAtelier, Dashtoon ~$10/mo, Anifusion, Lore Machine, AI Comic Factory, Comicsmaker.ai, Comicpad đóng cửa 01/09/2026.

| Tên | Mô hình giá | Quy mô / funding | Giải consistency? | Nguồn |
|---|---|---|---|---|
| ⭐ **Dashtoon** | ~$10/mo, không công bố | **$20,1M / 3 vòng** `[TC Tracxn]`: Seed 07/04/2023 $1,006M · Seed 02/11/2023 $6,024M · **Series A 17/09/2024 $8,813M**. Matrix Partners India, Stellaris VP, Z47. ⚠️ **465 nhân viên tính tới 31/05/2026** | Character library + recurring character. Không công bố kỹ thuật | [tracxn.com](https://tracxn.com/d/companies/dashtoon/__fyb3bu53aHKlNq-E11RgO5SgmUncP_QslwzZGvYeNqc), [techcrunch](https://techcrunch.com/2023/11/02/dashtoon/) |
| ⭐⭐ **GlobalComix** — **ĐỐI THỦ MỚI, run trước bỏ sót** | Platform; creator tool đang xây | **$13M (25/03/2026)** `[TC]`, lead **SBI US Gateway Fund + Point72 Ventures**; Scrum Ventures, Wise Ventures, Wicklow Capital, Upside VC. **Mua lại INKR**. CEO mới Henrik Rydberg (ex-Tinkercad) | **Gián tiếp — đúng chỗ đau của comic-studio.** INKR đem về *"translation, text detection, image cleaning, and **typesetting**"*; Ken Luong (ex-INKR CEO) làm head of AI engineering. Định vị **"the Figma for comics"** | [publishersweekly.com](https://www.publishersweekly.com/pw/by-topic/industry-news/comics/article/100003-globalcomix-wants-to-create-the-figma-for-comics-with-new-funding-and-ceo.html), [thenextweb](https://thenextweb.com/news/globalcomix-13m-inkr-acquisition) |
| ⭐ **WEBTOON / Naver — công cụ nội bộ** | Miễn phí cho creator của platform | WBTN NASDAQ, ~155M MAU `[TC]` | **Constella**: convert 3D character model nhiều pose → 2D theo **đúng nét vẽ của chính creator**. Rollout **professional creators trước**. Cộng **AI Painter** (2021) + **WebtoonMe** | [cbr.com](https://www.cbr.com/webtoon-controversial-ai-product-develop/) (fetch **socket hang up**, lấy từ snippet `[TC]`), [koreaproductpost](https://koreaproductpost.com/naver-webtoon-ai-services-toon-radar-painter-filter-chat/) |
| **WEBTOON byUs** (11/07/2026) | Miễn phí, reader-facing | — | Không liên quan consistency — AI story chat trên IP đã duyệt. Nêu để **không nhầm** là creator tool | [Anime News Network](https://www.animenewsnetwork.com/news/2026-07-11/webtoon-launches-ai-story-chat-service-byus-featuring-creator-approved-webtoon-ip/.239448) |
| **ComicInk** | (run trước) | CEO **Sanjoy Ghosh**. **Không tra được** team/funding. iOS launch 19/03/2026, <1K downloads. Ra tính năng video 07/2026 | **Đối thủ duy nhất công bố cơ chế**: *"addressing character consistency through **reference image injection and structured attributes**"* — Show HN 30/04/2026 | [HN item 47964060](https://news.ycombinator.com/item?id=47964060), [openpr](https://www.openpr.com/news/4570303/comicink-debuts-video-generation-capabilities) |
| **Anifusion** | €20/mo (10.000 credit) + free 100 `[TC]` ⚠️ mâu thuẫn $9/mo của run trước | **1 người**. **$833 MRR**, có lãi, không funding | Không công bố cơ chế | [starterstory.com](https://www.starterstory.com/anifusion-ai-breakdown) |
| **Jenova Webtoon Creator** | Không tra được | Không tra được | *"...with character consistency"* — ⚠️ **chỉ marketing claim**, không benchmark | [jenova.ai](https://www.jenova.ai/en/resources/ai-webtoon-creator) |
| **Comicsmaker.ai** | (run trước) | Không tra được | **LoRA training trên 15–30 ảnh/nhân vật** — đối thủ duy nhất cho user tự train LoRA `[TC]` | [blog.mage.space](https://blog.mage.space/article/best-ai-comic-generators-2026/bf9d1669-438a-49ee-8a60-68f2e7710601) |

**Ba kết luận delta:**

1. ⚠️ **Dashtoon 465 người / $20,1M là con số phải nhìn thẳng.** Run trước xếp nó ngang "một tool $10/mo". Thực tế là **quy mô studio** — 465 người ở công ty comic-AI nghĩa là phần lớn nhân sự **làm nội dung**, không làm phần mềm. ⇒ Dashtoon **không** là đối thủ về tool; nó là **content studio dùng AI**. Không cạnh tranh trực tiếp, và **không thể** dùng làm benchmark pricing.
2. ⭐⭐ **GlobalComix + INKR là mối đe dọa chiến lược thật, run trước bỏ sót.** Có **$13M**, có đội AI chuyên **typesetting/text detection** — đúng phần run trước kết luận comic-studio **"phải tự build"**. Định vị "Figma for comics" trùng §14 `Request.md`. **Cần theo dõi liên tục.**
3. ⚠️ **Constella của WEBTOON là rủi ro nền tảng, không phải rủi ro đối thủ.** Nếu platform lớn nhất phát công cụ consistency **miễn phí** cho creator của nó, kênh phân phối tự nhiên nhất (tác giả Canvas) bị chặn ở cửa. **Nhưng**: Constella nhắm creator **đã biết vẽ**, còn comic-studio nhắm **tác giả truyện chữ không biết vẽ**. Hai phân khúc khác nhau — khoảng cách đó **có thể** hẹp lại.

**Khoảng trống Câu 2**: (2.a) team/funding của ComicInk, TaleAtelier, Comicsmaker.ai, Jenova — không có profile Tracxn/Crunchbase; (2.b) không tìm thêm shutdown nào ngoài Comicpad; (2.c) **không đối thủ nào công bố benchmark consistency có số**; (2.d) trạng thái rollout Constella chưa xác nhận (fetch fail); (2.e) không tìm được entrant mới nào được đưa tin.

---

## Câu 3 — Mô hình BYOK

### 3.1. Có AI SaaS nào chạy BYOK thành công không? — **CÓ, và có một comp gần như hoàn hảo**

| Sản phẩm | Lĩnh vực | Định giá phần mềm | Bằng chứng | Nhãn | Nguồn |
|---|---|---|---|---|---|
| ⭐⭐ **Novelcrafter** | **Novel writing** — **phân khúc kề cận nhất** | **4 tier: Scribe $4 · Hobbyist $8 · Artisan $14 · Specialist $20**/tháng. **Scribe $4 = KHÔNG có AI.** BYOK mở khóa từ **Hobbyist $8**. **Nền tảng KHÔNG bán credit, KHÔNG có AI hosted.** | **220.000+ authors** `[OFF]` · ~120 quốc gia · Discord 9.825 members | `[OFF]` | [novelcrafter.com/pricing](https://www.novelcrafter.com/pricing) |
| ⭐ **TypingMind** | Chat UI | **$39 one-time lifetime** + BYOK | **$1M lifetime/20 tháng**; **$130–160K/tháng**; bootstrapped; khách Fortune 500 hợp đồng 3.000 seat | `[TC]` | [getlatka](https://getlatka.com/companies/typingmind) |
| **JetBrains AI** | IDE | Credit + BYOK song song | (run trước) | `[TC]` | — |
| **Natively AI** | Meeting assistant | **Free = BYOK**. **Paid = managed** | Không có số revenue | `[TC]` | [natively.software](https://natively.software/blog/natively-ai-pricing) |
| **Cline / Aider / Roo Code / Continue / Zed** | Coding agent | **Free/OSS**, 100% BYOK | Adoption lớn, không monetize qua license | `[TC]` | [awesome-byok-apps](https://github.com/yatsyk/awesome-byok-apps) |
| **AI-Flow** | **Image/video workflow** | *"pay providers directly — no platform markup, no subscription"* | Không có số | `[TC]` | [ai-flow.net/byok](https://ai-flow.net/byok/) |
| **ComfyUI** | **Image pipeline** | OSS, free | Adoption rất lớn | `[TC]` | — |
| **DM Champ** | Marketing SaaS | Managed + BYOK | *"one of the **rare** managed SaaS platforms that supports BYOK for **non-technical** buyers"* | `[TC]` | [dmchamp.com](https://dmchamp.com/best/best-ai-tools-byok-2026/) |
| **OpenRouter** | Router | BYOK fee **5%** | (run trước) | `[TC]` | — |

> ⭐⭐ **Novelcrafter là comp cần dùng.** Nó chứng minh **đồng thời ba điều** mà run trước chỉ suy đoán:
> 1. **BYOK bán được cho tác giả (writer), không chỉ cho dev.** 220.000 authors `[OFF]`.
> 2. **Mức platform fee $5–15 mà run trước đề xuất là ĐÚNG BIÊN** — Novelcrafter thu $4–20 và **không hề bán inference**.
> 3. **Tier $4 không-AI là pattern đáng copy**: cho người dùng vào sản phẩm (editor, Story Bible/Codex) **trước khi** phải đối mặt với API key. Đó là câu trả lời kiến trúc cho friction — và comic-studio có cấu trúc y hệt (Story Bible editor + Comic IR + layout editor **không đốt inference**).

### 3.2. Ma sát onboarding BYOK — ❌ **KHÔNG CÓ SỐ LIỆU ĐỊNH LƯỢNG**

> Đã tìm: 3 search + fetch trends.vc (**HTTP 403**) + fetch kompozy. Chỉ có benchmark onboarding SaaS chung và mô tả định tính. **Không A/B hay cohort nào tách riêng biến "API key".**

| Bằng chứng | Giá trị | Loại | Nguồn |
|---|---|---|---|
| Baymard friction formula | `Friction = (Required Fields × 1,5) + (Required Decisions × 2) + (**External Dependencies × 3**)`. Score >15 ⇒ abandonment >50% | `[TC]` — **không đo BYOK** | [saasfactor.co](https://www.saasfactor.co/blogs/the-science-of-saas-onboarding-a-comprehensive-framework-for-reducing-friction-improving-activation-and-preventing-churn) |
| → Áp cho BYOK | API key là external dependency, hệ số nặng nhất (×3) | `[EM]` — **suy luận, không phải đo** | — |
| Onboarding drop-off SaaS chung | 30–50%; 80% user rời trong 3 ngày; B2B activation TB 37,5% | `[TC]` | [chameleon.io](https://www.chameleon.io/blog/reducing-onboarding-drop-off-and-improving-activation-rates) |
| Time-to-first-value | >30 phút ⇒ abandonment **cao gấp 3x** so với <10 phút | `[TC]` | saasfactor |
| ⭐ **Chi phí thời gian setup BYOK** | *"**Plan an hour per provider** for first-time setup"*; vận hành *"1–2 hours/month at scale"*; key rotation 60–90 ngày; OpenAI tier 3 cần **$250+ lịch sử chi tiêu + chờ 14 ngày** | `[TC]` — **vendor blog của platform managed** ⇒ có động cơ phóng đại | [kompozy.io](https://kompozy.io/ai-content-tools/byok-vs-managed) |
| → Ghép hai số | "1 giờ setup" **gấp đôi ngưỡng 30 phút** của TTFV ⇒ **BYOK bắt buộc ngay từ signup là cấu hình rủi ro cao nhất** | `[EM]` — **ghép hai nguồn không liên quan** | — |

### 3.3. Mô hình lai — ⭐⭐ **CÓ, NHƯNG NGƯỢC CHIỀU VỚI GIẢ THIẾT**

> PM hỏi: *"free tier dùng key nền tảng, tier cao BYOK"*. **Không tìm được sản phẩm nào chạy đúng cấu hình đó.** Ba cấu hình thực tế đều **đảo ngược** nó:

| Cấu hình thực tế | Ví dụ | Logic |
|---|---|---|
| **A. Tier rẻ = KHÔNG AI · tier trên = BYOK · KHÔNG BAO GIỜ managed** | **Novelcrafter** ($4 no-AI → $8+ BYOK) `[OFF]` | Nền tảng **không bao giờ** chạm inference. Không có COGS |
| **B. Free = BYOK · Paid = MANAGED** (ngược hẳn) | **Natively AI** `[TC]` | BYOK là cách rẻ để thử; **trả tiền để KHÔNG phải cắm key**. ⇒ *convenience* mới là thứ bán được |
| **C. Tier rẻ self-serve = BYOK · Tier premium = managed credits** | JetBrains, DM Champ `[TC]` | *"BYOK with full model choice on a **cheaper** self-serve plan for the technical crowd, managed credits on a **premium** plan for everyone who just wants it to work"* — [kompozy.io](https://kompozy.io/ai-content-tools/byok-vs-managed) |

**Vì sao ngành đảo ngược?** Vì **BYOK tự lọc người dùng technical**. Đặt BYOK ở tier cao là bắt người trả nhiều tiền nhất chịu nhiều friction nhất — ngược logic. `[EM — diễn giải từ pattern A/B/C]`

**Điểm hòa vốn BYOK vs managed:**

| Loại output | Ngưỡng hòa vốn BYOK | Nhãn |
|---|---|---|
| Text post | ~700 output/tháng | `[TC]` kompozy, **vendor blog** |
| ⭐ **Ảnh (DALL·E 3)** | **~125 ảnh/tháng** | `[TC]` |
| Video 60s | ~25 video/tháng | `[TC]` |
| Khuyến nghị chung | <50/tháng → managed thắng · 50–200 → tùy mix · **200+ → BYOK thắng** | `[TC]` |

> ⚠️ **Đối chiếu dữ liệu run trước:** user AI trung bình generate **42 ảnh/tháng** `[TC]` — **SÂU dưới ngưỡng 125**. Nhưng một chapter ở N=3 = **180 ảnh** `[EM — 60 panel × 3, từ số run trước]` ⇒ **vượt ngưỡng ngay ở chapter đầu tiên**.
>
> ⇒ **Kết luận cho OQ2: câu trả lời phụ thuộc user là ai, và cả hai loại đều tồn tại.**
> - User "làm vài trang thử" (42 ảnh/tháng) → **managed/credit thắng**, BYOK là friction thuần túy.
> - User "làm 1 chapter/tháng trở lên" (180+ ảnh) → **BYOK thắng rõ**, và đây đúng là user gây −262% margin ở run trước.
>
> **⇒ Khuyến nghị, khác một nấc so với run trước** — không phải "BYOK" hay "credit", mà là **cấu hình A của Novelcrafter, có cửa thoát cho power user**:
> 1. **Tier $4–8: KHÔNG có image gen.** Story Bible editor + Comic IR + layout + versioning + export. Margin ~90%, không COGS, **không cần API key** ⇒ TTFV thấp. Đây là tier chứng minh giá trị.
> 2. **Credit pack không hết hạn** cho người dùng thường (<125 ảnh/tháng) — managed, có margin.
> 3. **BYOK là tùy chọn mở khóa ở tier trả phí** cho power user — người vượt 125 ảnh/tháng **tự có động cơ kinh tế** để cắm key (họ tiết kiệm tiền, không phải mình bắt họ).
>
> Cấu hình này giữ cả ba căn cứ ủng hộ BYOK ở run trước **nhưng gỡ được điểm yếu duy nhất** (friction với non-technical user) — vì không ai bị bắt cắm key để dùng sản phẩm.

**Khoảng trống Câu 3**: (3.a) conversion/drop-off riêng cho bước nhập API key — **không tồn tại công khai**; (3.b) không có ví dụ BYOK nào trong ngách image gen thương mại có số revenue; (3.c) không tìm được cấu hình "free = platform key, paid = BYOK"; (3.d) Novelcrafter không công bố ARR, 220K "authors" **không rõ là user hay paying user**; (3.e) số kompozy đến từ vendor bán managed — có bias, nhưng họ vẫn khuyến nghị BYOK ở >200 output/tháng, tức bias **ngược chiều lợi ích của họ** ⇒ độ tin cậy chấp nhận được.

---

## Câu 4 — Retention / churn

### 4.1. Con số 23% GRR — ✅ **XÁC MINH ĐƯỢC. Có thật, có methodology.**

Chuỗi truy nguyên: `saasultra.com` (nguồn run trước, aggregator) → tự khai nguồn **ChartMogul SaaS Retention Report** → fetch trực tiếp báo cáo ChartMogul → **khớp hoàn toàn**. Xác nhận chéo lần 3 bởi VentureCurator (25/06/2026).

| Thuộc tính | Giá trị | Nhãn |
|---|---|---|
| **Nguồn gốc** | **ChartMogul — "The SaaS Retention Report: The AI churn wave"** | `[OFF]` |
| **Cỡ mẫu** | **~3.500 software companies**: ~2.700 B2B SaaS · ~600 B2C SaaS · **~200 AI-native** | `[OFF]` |
| **Năm dữ liệu** | **2025** (tháng 1 → tháng 9/2025) | `[OFF]` |
| **Ngưỡng lọc** | Chỉ công ty **≥ $250K ARR** | `[OFF]` |
| **Ngày xuất bản** | Không ghi rõ trên trang | ❌ |

| Price band | GRR | NRR | Nhãn |
|---|---|---|---|
| **< $50/tháng** | **23%** | **32%** | `[OFF ChartMogul]` |
| $50–249/tháng | **45%** | **61%** | `[OFF]` |
| > $250/tháng | **70%** | **85%** | `[OFF]` |
| AI-native tổng thể (median 09/2025) | 40% | 48% | `[OFF]` |
| B2B SaaS (median NRR) | — | 82% | `[OFF]` |
| B2C SaaS (median NRR) | — | 49% | `[OFF]` |

> ⚠️ **BA CAVEAT PHẢI ĐI KÈM CON SỐ 23% — bỏ ba dòng này là tái phạm lỗi của run trước:**
> 1. **Cohort AI-native chỉ ~200 công ty**, và band `<$50` là **một tập con** của 200 đó. ChartMogul **không công bố n của riêng band này**. Có thể chỉ vài chục công ty.
> 2. **Bộ lọc ≥$250K ARR loại bỏ toàn bộ sản phẩm quy mô indie** — tức loại đúng nhóm comic-studio sẽ thuộc về (SOM năm 1 ước $4–14K ARR). **Không có bằng chứng 23% áp cho indie scale.**
> 3. **Đây là dữ liệu 2025, không phải 2026.**
>
> ⭐ **Nhưng luận điểm chính của run trước ĐỨNG VỮNG và mạnh hơn**: ChartMogul kết luận *"AI-native products that sell for >$250 per month see 70% GRR and 85% NRR. This is essentially the same as B2B SaaS"* ⇒ **vấn đề không phải "AI churn", vấn đề là GIÁ.**

Nguồn: [chartmogul.com](https://chartmogul.com/reports/saas-retention-the-ai-churn-wave/) `[OFF]` · [venturecurator.com 25/06/2026](https://www.venturecurator.com/p/below-this-price-ai-products-churn) `[TC]`

### 4.2. Dataset ĐỘC LẬP thứ hai xác nhận cùng chiều

**RevenueCat — State of Subscription Apps 2026** (dataset hoàn toàn khác ChartMogul):

| Chỉ số | AI apps | Non-AI apps | Nhãn |
|---|---|---|---|
| **Retention 12 tháng (annual plan)** | **21,1%** | **30,7%** | `[TC]` |
| Retention monthly plan | 6,1% | 9,5% | `[TC]` |
| Realized LTV / năm | **$30,16** | $21,37 | `[TC]` |
| Cỡ mẫu | ~115.000 app, >$11B revenue/năm, >1 tỷ giao dịch; AI apps = **27,1% mẫu** | | `[TC]` |
| Ngày xuất bản | **10/03/2026** | | `[TC]` |
| So 2025 | AI app 12-month payer retention **9,2% / 11,5%** — *ngang* app truyền thống ⇒ **sụt giảm 2026 là hiện tượng MỚI** | | `[TC]` |

Nguồn: [techcrunch.com 10/03/2026](https://techcrunch.com/2026/03/10/ai-powered-apps-struggle-with-long-term-retention-new-report-shows) `[TC]`

> ⚠️ **KHÔNG được gộp hai bộ số này.** ChartMogul đo **GRR (revenue retention, SaaS)**; RevenueCat đo **payer retention (mobile subscription app)**. **Hai metric khác nhau, không cộng, không so trực tiếp.** Giá trị của RevenueCat: một dataset độc lập, cỡ mẫu lớn hơn 30 lần, **xác nhận CÙNG CHIỀU**.

### 4.3. Benchmark riêng cho creative tool $5–20/tháng — ❌ **KHÔNG CÓ**

> **Không firm nào tách segment "creative tool" hay "comic/art tool" riêng.** Proxy gần nhất là band `<$50/tháng` của ChartMogul (23% GRR) và AI-app 12-month 21,1% của RevenueCat. Comic-studio ở mức giá $5–20 **nằm trọn trong band tệ nhất của cả hai dataset.**

**Khoảng trống Câu 4**: (4.a) n của riêng band `<$50/mo` — không công bố; (4.b) ngày xuất bản ChartMogul — không có; (4.c) benchmark cho creative/art/comic tool — không tồn tại; (4.d) ⭐ **retention cho mô hình credit pack (không hết hạn) vs subscription — không tìm được.** Đây là khoảng trống **trực tiếp dưới khuyến nghị pricing của run trước** — luận điểm *"credit pack né được 23% GRR"* **chưa có bằng chứng nào**, nó là lập luận logic (doanh thu ghi trước) chứ không phải số đo.

---

## Câu 5 — Kênh phân phối cho sản phẩm 1-dev

| Kênh | Ví dụ có số | Kết quả | Nhãn | Nguồn |
|---|---|---|---|---|
| ⭐ **Build-in-public trên X + freemium** | **Anifusion** — solo, **$0 marketing spend, KHÔNG làm SEO** | **$833 MRR, có lãi**. Nguyên văn: *"Despite not investing in traditional marketing or SEO, Anifusion achieved revenue milestones by leveraging **authentic social media engagement**"*; phong cách *"shitposting"* | `[TC]` | [starterstory.com](https://www.starterstory.com/anifusion-ai-breakdown) |
| ❌ **Show HN** | **ComicInk**, 30/04/2026 | **2 điểm · 2 comment.** Kênh **chết** với ngách này | `[OFF]` HN API | [hn.algolia.com](https://hn.algolia.com/api/v1/items/47964060) |
| ⭐⭐ **Comparison-listicle SEO** | Quan sát từ 8 lần search: taleatelier.com, comicpad.app, comicsai.org, gentoon.ai, jenova.ai, anifusion.ai, comicink.ai/blog, llamagen.ai đều xuất bản trang listicle | **Kênh thống trị ngách, đo được bằng chính SERP** — gần như mọi kết quả search về "AI comic tool" đều do đối thủ tự viết, không phải báo chí | `[EM]` — **quan sát SERP, không phải số traffic** | — |
| ⭐ **Discord tác giả** | WEBTOON official **17.777 members** · WEBTOON HQ 5.000+ · Webtoon Club 1.460 · **Webtoon Canvas Creators** · **Novelcrafter Discord 9.825** | Nơi tập trung đúng phân khúc. Novelcrafter dùng Discord làm kênh support + product update chính thức | `[TC]` / `[OFF]` | [disboard.org](https://disboard.org/servers/tag/webtoon), [novelcrafter blog](https://www.novelcrafter.com/blog/2025-09-community-update) |
| **Forum nền tảng** | Tapas Forum có thread creator hỏi nhau về công cụ | Không có số traffic | `[TC]` | [forums.tapas.io](https://forums.tapas.io/t/small-discord-servers-for-comic-creators/72597) |
| **Reddit** | r/comics **3,8M subscribers** (07/2026) | Có quy mô, nhưng là **cộng đồng độc giả + họa sĩ truyền thống** ⇒ xem rủi ro bên dưới | `[TC]` | [reddtrends.com](https://www.reddtrends.com/r/comics) |
| **Marketplace asset** | **Clip Studio Assets** (template, panel tool, speech balloon) · **Gumroad** | Không tra được số. Nhưng là nơi tác giả webtoon **đã có thói quen cài thêm công cụ** | `[TC]` | [assets.clip-studio.com](https://assets.clip-studio.com/en-us) |

> ⚠️ **Cộng đồng tác giả comic là kênh CÓ RỦI RO NGƯỢC, không phải kênh trung tính.**
>
> Dữ liệu run trước: Naver Webtoon bị **độc giả tổ chức boycott subscription** khi đăng tác phẩm AI; **BlueLine Studio bị buộc vẽ lại episode** *Knight King* sau khi fan phát hiện background AI-polish. Pattern: *"covert use can corrode brand trust more than disclosure ever could."*
>
> ⇒ **Hệ quả cho OKR:** một launch post kiểu "AI biến truyện chữ thành comic" vào r/comics hoặc Discord WEBTOON **có xác suất phản tác dụng cao**. Kênh cộng đồng chỉ hoạt động với **positioning disclosure-first** và nhắm vào **tác giả truyện chữ (writer)** — nhóm không cạnh tranh với họa sĩ — chứ **không** vào cộng đồng họa sĩ.
>
> Bằng chứng ủng hộ hướng "writer, không phải artist": **Novelcrafter 220K authors** `[OFF]` cho thấy cộng đồng **viết** chấp nhận AI tool ở quy mô lớn, trong khi cộng đồng **vẽ** thì boycott.

**Đề xuất Key Result đo được:**

| Kênh | KR | Neo |
|---|---|---|
| Build-in-public X | 1 post/tuần × 12 tuần; **500 follower** + **50 email waitlist** | Anifusion đạt $833 MRR bằng đúng kênh này với $0 spend `[TC]` |
| SEO listicle/comparison | **12 trang** so sánh + how-to; top-10 cho ≥3 keyword dạng *"novel to comic AI"* | 8/8 đối thủ trong SERP đều làm `[EM]` |
| Discord tác giả | Tham gia **5 server**; **20 cuộc trò chuyện 1-1** với tác giả trước khi ship MVP1 | WEBTOON official 17.777 `[TC]`; cũng là cách lấp khoảng trống WTP (1.c) |
| ❌ **Không làm** | Show HN, Product Hunt như kênh chính | ComicInk Show HN = **2 điểm** `[OFF]` |
| Positioning bắt buộc | 100% nội dung marketing nêu rõ AI-assisted + nhắm **writer**, không nhắm artist | Boycott Naver + BlueLine |

**Khoảng trống Câu 5**: (5.a) PH launch data của Dashtoon/Anifusion; (5.b) số subscriber r/webtoons; (5.c) traffic thật của kênh SEO listicle — kết luận "SEO thống trị" là **quan sát SERP `[EM]`**; (5.d) không tìm được tool AI nào phân phối qua marketplace; (5.e) ⚠️ **kênh phân phối ở thị trường Việt Nam — CHƯA TÌM, hết ngân sách tool call.** Đề xuất run sau.

---

## Ba điều đọc trước tiên (nguyên văn kết luận của worker)

1. **TAM $14B là con số sai để trích vào Charter.** SAM thật ước **$0,4–9M ARR** `[EM]`, SOM năm 1 ước **$4–14K ARR** `[EM]`, neo vào Anifusion $833 MRR sau 2 năm solo `[TC]`. Nếu OKR đặt mục tiêu doanh thu, hãy đặt ở thang **trăm đô/tháng**, không phải nghìn.
2. **Con số 23% GRR sống sót qua kiểm chứng** (ChartMogul, ~3.500 công ty, dữ liệu 2025, band `<$50/mo` AI-native), có dataset độc lập thứ hai xác nhận cùng chiều (RevenueCat 21,1% vs 30,7%). Ba caveat bắt buộc đi kèm.
3. **Câu hỏi BYOK nên được đặt lại.** Cấu hình "free = platform key, cao = BYOK" **không tồn tại trong ngành**. Comp gần nhất là **Novelcrafter** `[OFF]`: 220K tác giả, $4 tier không-AI, BYOK từ $8, nền tảng không bao giờ bán inference. Ngưỡng hòa vốn **~125 ảnh/tháng** chia đúng hai loại user: người thử (42 ảnh/tháng → credit) và người làm chapter (180 ảnh/tháng → BYOK).

---

# B. PM đọc được gì

1. ⭐⭐ **Điều chỉnh lớn nhất: TAM không được vào Charter.** Charter phải neo vào **SOM $4–14K ARR năm 1**, và phải nói rõ SAM là phép nhân `[EM]` chứ không phải số đo. Đây là chỗ tài liệu planning dễ tự lừa mình nhất — trích một con số tỷ đô để biện minh cho một dự án có thị trường thật cỡ vài trăm nghìn đô.
2. ⭐⭐ **Khuyến nghị pricing của run trước bị điều chỉnh một nấc, không bị lật.** Run trước: *"BYOK ở vị trí số 1"*. Delta này: **cấu hình 3 tầng kiểu Novelcrafter** — tier không-AI làm cửa vào, credit cho user thường, BYOK **mở khóa** cho power user. Ba căn cứ ủng hộ BYOK vẫn nguyên; điểm yếu duy nhất (friction) được gỡ bằng cách **không bắt ai cắm key để dùng sản phẩm**. Đây là phương án em khuyến nghị tại gate.
3. **Ngưỡng 125 ảnh/tháng là con số vận hành đắt giá nhất của báo cáo này** — nó biến câu hỏi "BYOK hay credit" từ một lựa chọn nhị phân thành một **quy tắc phân tuyến user** có thể code được.
4. **GlobalComix + INKR phải vào Risk Register**, không chỉ vào Research Notes. $13M + đội AI typesetting + định vị "Figma for comics" chạm đúng hai thứ comic-studio định làm.
5. **Constella của WEBTOON là rủi ro nền tảng riêng biệt** — khác loại với rủi ro đối thủ, phải là một hàng riêng trong Risk Register.
6. **Kênh phân phối có rủi ro ngược** — đây là input trực tiếp cho OKR, và nó **hạn chế** chứ không mở rộng không gian KR. Positioning "writer, không phải artist" phải là một constraint trong Charter.
7. **Anifusion $833 MRR sau ~2 năm solo là neo thực tế nhất** cho toàn bộ phần mục tiêu doanh thu. Nó cũng là lời cảnh báo về thang thời gian.

# C. Mâu thuẫn với lens khác

| # | Mâu thuẫn | PM phân xử |
|---|---|---|
| 1 | **Anifusion: run trước ghi $9/mo, delta ghi €20/mo**; và **$833 MRR vs $5.000/tháng** | **Chưa phân xử được, và không cần phân xử để đi tiếp.** Cả hai đều `[TC]`, không nguồn nào là chính chủ. → Tài liệu phải ghi **cả hai con số kèm nhãn mâu thuẫn**, không được chọn một rồi trình bày như sự thật. Ghi vào Research Notes như một khoảng trống đã biết. |
| 2 | **Run trước xếp Dashtoon là đối thủ tool trực tiếp; delta cho thấy nó là content studio 465 người** | **Theo delta.** Bằng chứng cụ thể hơn (Tracxn, có ngày, có vòng gọi vốn, có headcount). Hệ quả: **không dùng giá Dashtoon làm neo pricing** — điều này làm yếu một phần lập luận "trần giá thị trường $9–10" của run trước, nhưng **không lật nó**, vì ComicInk/TaleAtelier/Anifusion vẫn nằm trong khoảng đó. |
| 3 | **Run trước: "credit pack né được 23% GRR". Delta: khoảng trống 4.d — không có bằng chứng nào cho điều đó** | **Theo delta.** Luận điểm đó là **lập luận logic, không phải số đo**, và phải được ghi đúng như vậy trong mọi tài liệu. Đây chính xác là loại khẳng định mà E2 của run trước cảnh báo. |
| 4 | **Run trước hỏi cấu hình hybrid "free = platform key, cao = BYOK"; delta nói cấu hình đó không tồn tại** | **Theo delta.** Không nguồn nào tìm được ⇒ không có tiền lệ ⇒ không tự chế. Dùng cấu hình A của Novelcrafter, là cái **có 220K người dùng làm bằng chứng**. |
