# Findings — researcher

> Agent `researcher` **không có tool Write/Edit** (chỉ Read/Glob/Grep/WebFetch/WebSearch).
> Nó trả toàn văn trong final message; PM lưu lại nguyên văn tại đây.
> Dispatch read-only, `FILES_TOUCHED: none`. 53 tool call, ~50 lần WebSearch/WebFetch.

## Kết luận của worker

Ngày: 23/08/2026 · Toàn bộ số liệu được verify bằng WebSearch/WebFetch trong run này. Chỗ nào không tra ra, ghi rõ.

---

### 1. Character consistency trong image generation — state of the art 8/2026

#### 1.1. Ba họ kỹ thuật và vị thế hiện tại

**A. Reference/adapter-based (IP-Adapter, InstantID, PuLID)** — vẫn sống nhưng đã tụt xuống tầng "component", không còn là giải pháp chủ đạo cho production.

Số face-similarity từ literature (cosine similarity trên face embedding, thang 0-1):

| Method | DivID-120 | Unsplash-50 |
|---|---|---|
| PuLID | 0.733 | 0.659 |
| InstantID | 0.725 | 0.614 |
| IP-Adapter | 0.619 | 0.615 |
| FaceCLIP-SDXL | — | 0.866 (Internal-v1: 0.869) |

Nguồn: [arXiv 2504.14202](https://arxiv.org/pdf/2504.14202), [arXiv 2510.25084](https://arxiv.org/pdf/2510.25084), [Omni-ID arXiv 2412.09694](https://arxiv.org/pdf/2412.09694).

⚠️ Lưu ý quan trọng: các metric này chỉ đo **mặt**. Không có metric nào trong họ này đo trang phục, tỉ lệ cơ thể, hay phụ kiện — đúng chỗ comic cần nhất. Đây là giới hạn cấu trúc, không phải giới hạn kỹ thuật.

**B. Per-character LoRA / DreamBooth** — chi phí đã rất thấp, không còn là rào cản.

| Chỉ số | Giá trị | Nguồn |
|---|---|---|
| Số ảnh cần (FLUX) | 12–15 ảnh cho consistency tốt hơn SDXL trained 50 ảnh; sweet spot cộng đồng 20–25 | [thefluxtrain.com](https://thefluxtrain.com/blog/noobs-guide-to-flux-lora-training/) |
| Số ảnh cần (FLUX.2) | 10–20 ảnh cho "95%+ consistency across poses" | [FLUX.2 LoRA Training Guide](https://workingnotworking.com/flux-2-lora-training-guide/) |
| Thời gian train | 2–4h trên RunPod RTX 4090; 15–45 phút trên platform managed | [lewdly.ai](https://lewdly.ai/blog/nsfw-flux-lora-training-runpod-2026), [imagera.ai](https://imagera.ai/guides/how-to-train-lora-model-online-no-gpu-2026) |
| Chi phí | **$2–5 / LoRA** (RunPod RTX 4090 @ $0.34/hr); ~$4–5 trên managed platform | cùng nguồn trên |

→ Với 20 nhân vật: **$40–100 tổng chi phí train**, một lần. Không phải blocker. Nhưng: mỗi lần đổi costume version theo timeline (§9) **không** cần LoRA mới — LoRA giữ identity, costume đi qua prompt/reference.

**C. Native multi-image reference models — nhóm dẫn đầu 2026.**

| Model | Reference images | Claim về character | Giá (official) |
|---|---|---|---|
| **Gemini 3 Pro Image (Nano Banana Pro)** | **tới 14 ảnh** | "maintaining the consistency and resemblance of **up to 5 people**" | $0.134/ảnh 1K-2K; $0.24/ảnh 4K; **batch $0.067 / $0.12** |
| Gemini 3 Flash Image (Nano Banana 2) | — | — | $0.067/ảnh 1K; batch $0.034 |
| **FLUX.2 [pro]** | **tới 10 ảnh** | "strong preservation of character identity... recurring characters, multi-scene" | từ $0.03 (t2i), $0.045 (edit) |
| FLUX.1 Kontext [pro] | — | — | $0.04/ảnh |
| FLUX.2 [klein] 4B | — | — | $0.014/MP |
| GPT Image 2 (4/2026) | — | — | ⚠️ xem §5 |

Nguồn official: [blog.google Nano Banana Pro](https://blog.google/innovation-and-ai/products/nano-banana-pro/) (release 20/11/2025), [ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing), [docs.bfl.ml pricing](https://docs.bfl.ml/quick_start/pricing), [bfl.ai/blog/flux-2](https://bfl.ai/blog/flux-2) (FLUX.2 launch 25/11/2025, [the-decoder](https://the-decoder.com/black-forest-labs-launches-flux-2-with-a-new-multi-reference-feature/)).

Mốc thời gian bổ sung: Google GA **Gemini 3.1 Flash Image + Gemini 3 Pro Image ngày 28/05/2026**; **GPT Image 2 ra 4/2026** ([gradually.ai](https://www.gradually.ai/en/ai-image-models/)).

#### 1.2. Multi-character trong một panel — chỗ hỏng nhất, câu trả lời có 3 tầng

**Tầng 1 — Open-source: sụp đổ rõ ràng ngoài 3 nhân vật.** Benchmark **CogCanvas** (arXiv 2606.15867, 6/2026): 1.952 reference images, 100 celebrity identities, 1.361 compositional prompts, nhóm 2–5 người. Metric ID-Sim:

| Số nhân vật | XVerse | UNO |
|---|---|---|
| 2 | **42.33** | 23.23 |
| 3 | 27.21 | 19.60 |
| 4 | **2.67** | 19.60 |
| 5 | **0.52** | 13.47 |

Attr-VQA (gắn đúng trang phục/vật phẩm cho đúng người): 2 người UNO 35.12 → 3 người 14.65 → **4-5 người gần như thất bại hoàn toàn**. Kết luận của paper: *"near-complete failure on object/fashion binding beyond three subjects"* — ảnh trông hợp lý nhưng model **không gắn đúng attribute cho đúng identity**. Nguồn: [arXiv 2606.15867](https://arxiv.org/html/2606.15867).

⚠️ **CogCanvas chỉ test open-source** (OmniGen2, UNO, DreamO, XVerse, MOSAIC). **Không** test Nano Banana Pro / GPT Image 2 / FLUX.2.

**Tầng 2 — Frontier models: chỉ có vendor claim.** Google nói "up to 5 people". **Không tìm được benchmark độc lập nào đo frontier models ở 2-3 nhân vật/khung.** Bằng chứng gián tiếp: khi vượt 5 nhân vật, "the identity latent mechanism begins to fail, and characters will blend traits, resulting in merged facial features or entirely generic faces" ([nenobanana.com](https://www.nenobanana.com/blogs/character-consistency-in-nano-banana)) — nguồn thứ cấp, không phải Google.

**Tầng 3 — Có pipeline agentic phía trên thì đo được, và kết quả tốt.** **CANVAS** (arXiv 2604.13452, 15/04/2026) — xem §7. Trên HardContinuityBench với backbone **Gemini-3-pro-image**, ContinuityEval (thang Likert 1–5, VLM autorater):

| Metric | CANVAS | Baseline (Gemini-CT) | Δ |
|---|---|---|---|
| Character Avg | **4.91** | 4.39 | +11.8% |
| Consecutive BG | 4.88 | 4.48 | +8.9% |
| Non-Consecutive BG | 4.88 | 4.06 | +14.0% |
| Props Consistency | 4.19 | 4.06 | +2.5% |

Human preference: **86.7% win-rate** vs AutoStudio. Nguồn: [arXiv 2604.13452v1](https://arxiv.org/html/2604.13452v1).

Chú ý con số **Props 4.19** — thấp hơn hẳn character 4.91. Đúng khớp với ví dụ "✗ sword missing" ở §15 `Request.md`. Vật phẩm/vũ khí là điểm yếu thật, không phải lo hão.

Benchmark liên quan khác: **MIBE** (arXiv 2607.01383, 7/2026) — 60K-pair Silver Set + 4K-pair human Gold Set. Kết luận abstract: *"state-of-the-art models still struggle with this process, frequently omitting subjects, failing to preserve reference appearances, or misattributing interactions"*, và metric truyền thống (CLIP, DINO) **suy giảm nghiêm trọng** khi số subject tăng. Nguồn: [arXiv 2607.01383](https://arxiv.org/abs/2607.01383). Cũng có **MultiHuman-Testbench** (NeurIPS 2025, 1.800 samples / 5.550 faces).

#### 1.3. Kết luận §1 — khuyến nghị cho 1 dev đơn lẻ

**Hướng khuyến nghị: native multi-image reference model (Nano Banana Pro / FLUX.2 pro) làm backbone + pipeline có state memory + VLM verification phía trên. Không dùng adapter-based làm trục chính. LoRA là lớp tăng cường tùy chọn, không phải nền tảng.**

Lý do: LoRA giải identity nhưng không giải composition đa nhân vật; adapter chỉ giải mặt; native multi-ref giải cả mặt + costume + style trong một lần gọi, đúng hình dạng của §8 (Panel Prompt + Character Ref + Costume Ref + Style Ref + Location Ref).

**Mức consistency đạt được:**

- **1 nhân vật/panel**: đủ tốt để xuất bản. Bằng chứng: CANVAS character avg 4.91/5.
- **2–3 nhân vật/panel**: khả thi nhưng cần verify từng panel + regenerate. Không có benchmark độc lập trên frontier model để khẳng định; open-source đã sụp ở 3.
- **4+ nhân vật/panel**: **chưa giải được**. CogCanvas cho thấy attribute binding thất bại gần hoàn toàn. → Ràng buộc thiết kế: Comic IR nên **cứng hóa giới hạn ≤3 nhân vật/panel**, cảnh đông người dùng shot xa/silhouette/crop.
- **Vẫn thấy sai ở**: props/vũ khí (4.19/5), màu mắt và chi tiết phụ nếu không lock rõ, và các đặc điểm không xuất hiện trong reference ở góc đó — model "lacks a 3D memory of a character" ([medium/pauls-world](https://medium.com/pauls-world/your-ai-characters-keep-changing-faces-heres-how-to-fix-it-c7cc5c2f7247)).

**Điều chỉnh giả định của tác giả**: §7 gọi consistency là "boss cuối" — đúng nhưng đã **hạ cấp** trong 2026. Ghi nhận từ ngành: cuối 2025–đầu 2026 character consistency chuyển từ *"mostly impossible"* sang *"actually workable"* ([javilopen.substack.com](https://javilopen.substack.com/p/consistency-of-characters-objects)). Boss cuối thật sự bây giờ là **multi-character attribute binding** và **props continuity**, không phải single-character identity.

---

### 2. Đã có ai làm đúng việc này chưa?

#### 2.1. Bối cảnh đối thủ (còn sống 2026)

| Sản phẩm | Input | Cách giải consistency | Pricing | Trạng thái |
|---|---|---|---|---|
| **ComicInk** | ⭐ **PDF novel nguyên bản**, tới ~1.5M ký tự (~500 trang) | Tự động extract character roster (**tối đa 20 nhân vật/series**); series-level character entries; **"Story so far"** = summary text sau mỗi issue đưa vào prompt issue sau | Credit: ~150 (50tr), ~500 (200tr), ~900 (400tr); art tính riêng | Alive |
| **Dashtoon Studio** | Story text | Character library + recurring-character support | ~$10/mo, freemium; **50% rev-share sau 10 episode free** trên Reader app | Alive |
| **Anifusion** | Prompt/story | — | Creator $9/mo, **layered export** (Photoshop/Clip Studio) | Alive (verified 6/2026) |
| **Lore Machine** | Text tới **30k words** | Custom characters (v2); v3 = "World Building Toolkit" | 4 subscription tiers | Alive (Substack có nội dung 2026) |
| **C2Story / ComicPad / LlamaGen / Novel2Comic / ComicsAI** | Chapter/excerpt/TXT | Character sheet, consistent art style | freemium/credit | Alive |
| **AI Comic Factory** | Prompt | — | Free | Alive |
| **Comicsmaker.ai** | Prompt | Custom page designer, panel shapes | — | Alive (tested 7/2026) |

Nguồn: [comicink.ai/blog](https://www.comicink.ai/blog/convert-book-to-comic-series), [toolworthy.ai Dashtoon](https://www.toolworthy.ai/tool/dashtoon-studio), [comistitch.com](https://comistitch.com/blog/best-ai-comic-generator-2026/), [aigregator Anifusion](https://aigregator.com/tools/anifusion), [loremachine.world](https://www.loremachine.world/), [MIT Tech Review về Lore Machine](https://www.technologyreview.com/2024/03/05/1089458/generative-ai-turn-my-story-into-comic-images-lore-machine/), [comicpad.app](https://www.comicpad.app/best-ai-comic-generators).

#### 2.2. Có ai đã có "Story Bible + Timeline state + Continuity Checker" chưa?

**Câu trả lời: hai nửa tồn tại riêng, chưa ai ghép.**

**Nửa Story Bible + timeline state + continuity check — ĐÃ CÓ, nhưng ở ngành viết novel, không phải comic:**

- **Sudowrite Story Bible**: "persistent memory for your manuscript, with entries **tagged by timeline** and the system storing **character states**, locations, and plot details **per era**"; Chapter Continuity kéo tới 25 linked documents / 20.000 words. → **Đây gần như đúng §2 + §3 của `Request.md`.** Nguồn: [sudowrite.com/blog](https://sudowrite.com/blog/writing-multiple-timelines-ai/).
- **Novilot**: đọc manuscript, bắt "a character whose eyes change color", timeline contradictions (ages, dates, seasons, sequence across chapters). Nguồn: [novilot.com/features](https://www.novilot.com/features).
- **ProseWeave**: Story Bible inject vào mọi AI operation, AI flag khi nội dung mới mâu thuẫn bible. Nguồn: [blog.proseweave.ai](https://blog.proseweave.ai/story-bible-guide-templates-examples/).

**Nửa comic generation — ĐÃ CÓ, nhưng state management rất nông:** ComicInk là sản phẩm sâu nhất tìm được, và nó dùng **"Story so far" = summary văn xuôi**, không phải structured state. Nó cũng **cap ở 20 nhân vật và 12 issues**. Không có timeline query kiểu "Lâm Phong đang mặc gì ở Chapter 17 Scene 4".

#### 2.3. Đây là cơ hội thật hay dấu hiệu không ai cần? — Xét cả hai

**Lập luận "cơ hội thật":**

- Structured state management đã được chứng minh có nhu cầu **ở ngành liền kề** (Sudowrite, Novilot, ProseWeave đang bán được). Không phải giả định — là sản phẩm đang thu tiền.
- Trong ngành comic AI, nhược điểm được ngành tự nhận là *"inconsistent characters, weak facial expressions... bad lettering"* ([comistitch.com](https://comistitch.com/blog/where-to-publish-ai-comic-2026-platform-decision-tree/)) — đúng chỗ Story Bible nhắm.
- ComicInk cap 20 nhân vật / 12 issues cho thấy **hạn chế do thiếu kiến trúc state**, không do thiếu nhu cầu. Truyện Trung Quốc/web novel thường 500-2000 chương.

**Lập luận "dấu hiệu xấu" — không thể loại bỏ:**

- Không ai ghép hai nửa, dù cả hai nửa đều đã có công ty làm. Điều đó **có thể** nghĩa là: người dùng thực tế không cần adapt 100 chương, họ cần 10 trang cho social media. ComicInk giới hạn 12 issues có thể là quyết định **product**, không phải quyết định kỹ thuật.
- ROI của Story Bible tăng theo độ dài truyện, còn thị trường AI comic đang tập trung ở đầu ngắn (workload thật của AI image *"concentrated around repeatable, revenue-adjacent jobs rather than open-ended art"*, [digitalapplied.com](https://www.digitalapplied.com/blog/ai-image-generation-statistics-2026-data-points)).
- → **Rủi ro thật: over-engineering cho một use case (100+ chương) mà thị trường chưa chứng minh.** Moat có giá trị chỉ khi có người muốn đi tới chương 50.

#### 2.4. Ai đã thất bại/đóng cửa?

**Tra hai lần và không tìm được shutdown nào được xác nhận trong ngách AI comic/novel-to-comic.** Lore Machine — cái nghi ngờ nhất vì được MIT Tech Review đưa 3/2024 — vẫn sống (v2, v3, Substack có nội dung 2026). Dashtoon, Anifusion, Comicsmaker.ai, AI Comic Factory đều được review trong 2026.

⚠️ Phân biệt rõ: **"không tìm được shutdown được xác nhận"** ≠ **"chưa ai thất bại"**. Đã kiểm [Killed by AI graveyard](https://mixtpatrik.github.io/killedbyai/) và [techstartups.com top AI shutdowns 2025](https://techstartups.com/2025/12/09/top-ai-startups-that-shut-down-in-2025-what-founders-can-learn/) qua search result nhưng không thấy tên nào thuộc ngách này. Bài học "vì sao thất bại" — **không tìm được dữ liệu đáng tin cậy**.

---

### 3. Nhu cầu thị trường

#### 3.1. Quy mô & xu hướng

- Thị trường webtoon toàn cầu: **USD 14,44 tỷ**, dự báo **USD 60,25 tỷ tới 2031, CAGR 33,1%** ([abovea.tech](https://abovea.tech/webtoon-statistics-and-trends/)) — số từ nguồn thứ cấp, không phải báo cáo gốc.
- WEBTOON Entertainment (NASDAQ: WBTN): Q3 2026 guidance **$358M–$368M**, nhắm double-digit growth 2026 + Disney partnership; **Q2 2026 loss widens** — tăng trưởng đang chậm lại ([Forbes 11/08/2026](https://www.forbes.com/sites/robsalkowitz/2026/08/11/webtoons-growth-is-slowing-but-its-ambitions-are-growing/), [Seeking Alpha](https://seekingalpha.com/news/4630403-webtoon-expects-358m-368m-q3-revenue-as-it-targets-exiting-q4-in-double-digit-growth)).
- Tiền lệ nghiệp vụ: **WEBTOON đã chủ động adapt web novel thành webcomic** như một hướng IP chiến lược ([BusinessWire 2023](https://www.businesswire.com/news/home/20230118005243/en/WEBTOON-Expands-its-IP-Creator-Ecosystem-With-Webcomic-Adaptations-of-Hit-Web-Novels)). → Novel→comic là workflow **đã được ngành xác nhận**, không phải ý tưởng lạ.

#### 3.2. Backlash có thật ở mức nào? — CÓ, và có bằng chứng cụ thể

- **Naver Webtoon**: đăng một tác phẩm AI-created, khi bị phát hiện, **độc giả tổ chức boycott subscription**.
- **BlueLine Studio** bị buộc **vẽ lại các episode của *Knight King*** sau khi fan phát hiện background được AI-polish.

Nguồn: [comistitch.com decision tree](https://comistitch.com/blog/where-to-publish-ai-comic-2026-platform-decision-tree/), [Korea Times 06/11/2025](https://www.koreatimes.co.kr/lifestyle/trends/20251106/webtoon-industry-seeks-ai-edge-amid-legal-ethical-challenges).

- Nghiên cứu học thuật: **CHI 2026** có paper *"AI in Webtoon Creation: Challenges, Perceptions, and Design Implications"* ([DOI 10.1145/3772318.3790343](https://dl.acm.org/doi/10.1145/3772318.3790343)) — ⚠️ fetch bị **403 Forbidden**, chỉ biết title/venue, **không đọc được số liệu**. Ghi nhận trung thực: chưa có số định lượng về thái độ độc giả.
- Pattern rút ra được: backlash bùng khi **AI use bị che giấu**, không khi được disclose. *"covert use can corrode brand trust more than disclosure ever could."*
- Đề xuất từ ngành: **"granular disclosure"** — label "AI-assisted backgrounds" nhưng che vùng sensitive (characters).

#### 3.3. Chính sách platform — ĐÃ CÓ LUẬT BẮT BUỘC

**South Korea AI Basic Act**: thông qua 21/01/2025, **hiệu lực 22/01/2026**. Đầu tiên ở châu Á bắt buộc disclosure với nội dung AI-generated/AI-assisted. Với webtoon/animation, **cho phép watermark machine-readable không hiển thị** (không phá trải nghiệm đọc). Phạt tới **30 triệu won (~£18.000)** sau grace period ≥1 năm. **Áp dụng cho mọi service coi Hàn Quốc là market — gồm Webtoon, Tapas, Tappytoon.**

Nguồn: [PetaPixel 29/01/2026](https://petapixel.com/2026/01/29/south-korea-launches-landmark-laws-requiring-labels-on-ai-generated-content/), [The New Publishing Standard 28/01/2026](https://thenewpublishingstandard.com/2026/01/28/korea-ai-act-webtoon-creators/), [Anime News Network 24/01/2026](https://www.animenewsnetwork.com/news/2026-01-24/south-korea-new-ai-law-raises-questions-for-webtoon-creators-platforms/.233383), [FPF](https://fpf.org/blog/south-koreas-new-ai-framework-act-a-balancing-act-between-innovation-and-regulation/).

Thực trạng platform: hầu hết **accept AI content với mandatory AI-assisted tag**: Webtoons, Tapas, Lezhin, GlobalComix, Substack, KDP, Gumroad. **WEBTOON Canvas hiện chưa có mandatory labelling rule**, chỉ editorial recommendation voluntary disclosure.

→ **Hệ quả kiến trúc**: cần **AI provenance metadata field** ở cấp page/panel export, và export path phải nhúng được machine-readable watermark. Đây là requirement, không phải nice-to-have.

#### 3.4. Ai trả tiền? — bằng chứng WTP còn yếu

Bằng chứng gián tiếp có:

- WEBTOON Originals: creator nhận per-episode fee + rev split; **payout cho creator tiếng Anh >$27M từ 2020, >$1M/tháng** ([BusinessWire](https://www.businesswire.com/news/home/20220718005148/en/Building-a-Creator-Economy-for-Comic-Artists-English-Language-WEBTOON-Creator-Payments-Surpass-%2427-Million-Since-2020)).
- **Lezhin global contests trả $5.000–50.000/accepted series**; Lezhin + Tapas dẫn đầu revenue-per-reader với pay-per-episode.
- Giá tool đối thủ đang thu được: Dashtoon ~$10/mo, Anifusion $9/mo. → **Trần giá tham chiếu cho tool cá nhân ~$10-20/mo.**
- Chi phí sản xuất webtoon truyền thống: creator tự bỏ tiền thuê assistant + software + 3D models ([s-morishitastudio.com](https://www.s-morishitastudio.com/how-much-do-line-webtoon-artists-get-paid/)) → có ngân sách sẵn để dịch chuyển.

⚠️ **Không tìm được study/survey nào về willingness-to-pay cụ thể của tác giả web novel cho tool adapt truyện.** Đây là gap thật.

**Phân khúc khả năng cao nhất theo dữ liệu**: không phải studio (họ có artist và sợ backlash), mà **tác giả web novel tự sở hữu IP muốn tự adapt** — vì họ vừa có IP (giải được §4), vừa có động lực kinh tế, vừa không bị ràng buộc brand như studio.

---

### 4. Rủi ro pháp lý & bản quyền ⚠️

#### 4.1. Hai nhánh theo A3 — KHÔNG được gộp

**Nhánh A — Truyện của tác giả khác: chặn đường thương mại hóa.**

Comic adaptation của novel là **derivative work** rõ ràng. Khung pháp lý: *"Only the owner of copyright in a work has the right to prepare, or to authorize someone else to create, an adaptation of that work"*; ví dụ derivative work chính thức của US Copyright Office gồm *translation, fictionalization, motion picture adaptations, art reproduction, abridgement*. Comic adaptation rơi đúng vào nhóm này. Cần **license hoặc permission trực tiếp**. Nguồn: [Copyright.gov Circular 14](https://www.copyright.gov/circs/circ14.pdf), [Kirkland IP Primer for Comic Book Creators](https://www.kirkland.com/-/media/content/kirkland-ip-primer-for-comic-book-creators.pdf), [lawshelf.com](https://www.lawshelf.com/videocoursesmoduleview/part-2-module-2-building-on-copyrighted-works/).

→ Ở nhánh này: tool vẫn dùng được **cho cá nhân/private**, nhưng **không xuất bản, không thương mại hóa** được. Phần lớn giá trị "moat" của §18 MVP 4 (Export, publish workflow) mất ý nghĩa.

**Nhánh B — IP tự sở hữu: khả thi, có điều kiện.**

#### 4.2. Bản quyền output AI

**US — Zarya of the Dawn (tiền lệ trực tiếp nhất, và nó ĐÚNG LÀ comic):**

US Copyright Office ban đầu cấp registration cho graphic novel 18 trang của Kristina Kashtanova (ảnh từ Midjourney), sau đó **partially cancel** vì non-human authorship. Nhưng: **text và "selection, coordination, and arrangement" của các thành phần văn bản + hình ảnh VẪN được bảo hộ** — Office kết luận *"an arrangement of AI-generated images with human-authored text in a comic book"* là **copyrightable compilation**.

Guidance 2026 tái xác nhận: *"a sufficiently creative selection, arrangement, or modification of AI output may be copyrightable"*, và Office **có xét tới** các AI tool cho phép user control output *"through an iterative, interactive process rather than solely relying on prompts"*.

Nguồn: [copyright.gov/ai](https://www.copyright.gov/ai/), [copyright.gov AI policy guidance PDF](https://www.copyright.gov/ai/ai_policy_guidance.pdf), [Sidley Austin](https://www.sidley.com/en/insights/newsupdates/2025/02/us-copyright-office-issues-report-on-artificial-intelligence-and-copyrightability), [Harvard JOLT Zarya digest](https://jolt.law.harvard.edu/digest/zarya-of-the-dawn-how-ai-is-changing-the-landscape-of-copyright-protection).

⭐ **Đây là tin TỐT cho comic-studio, và hầu hết mọi người đọc sai Zarya.** Panel layout, page composition, script, dialogue, panel ordering — tức là **chính xác cái mà Comic IR + Layout Director của `Request.md` sản xuất** — là phần **được bảo hộ**. Ảnh raw thì không. Kiến trúc "spec là dữ liệu chính, ảnh chỉ là output/cache" (kết luận cuối `Request.md`) **trùng khớp với đường ranh pháp lý**.

#### 4.3. Việt Nam — ĐÃ CÓ LUẬT, hiệu lực 9/4/2026 ⭐

**Nghị định 134/2026/NĐ-CP**, hiệu lực **09/04/2026**, sửa đổi/bổ sung Nghị định 17/2023/NĐ-CP, hướng dẫn Luật SHTT.

| Nội dung | Quy định |
|---|---|
| **Điều 5a — điều kiện bảo hộ** | Con người phải có **"substantial and decisive intellectual contribution to the creative process"**, có meaningful control lên output và chịu trách nhiệm về tính hợp pháp. Tác phẩm **do AI tạo hoàn toàn: KHÔNG được bảo hộ**. Phải thể hiện human intent, không phải "automated algorithmic arrangements". |
| **Nghĩa vụ lưu trữ** ⭐ | **Phải lưu giữ prompts, inputs, intermediate drafts** và tài liệu chứng minh human contribution; **truthfully disclose** việc dùng AI khi cơ quan có thẩm quyền yêu cầu. |
| **Điều 37a — TDM** | TDM được phép cho nghiên cứu/testing/training AI, nhưng **"limited to non-commercial purposes at the point of use"**; nguồn phải hợp pháp, không được vượt technological protection measures, không thay thế thị trường gốc. |
| **Điều 37b — opt-out** | Tác giả có quyền **reserve tác phẩm khỏi AI training** bằng machine-readable means hoặc qua tổ chức quản lý tập thể. |
| **Điều 37c — thương mại hóa** | Phải giữ technical records; **"royalty payment obligations may arise"** khi hệ thống đã train được khai thác thương mại. |

Nguồn: [Baker McKenzie — Vietnam: Redefining Copyright for AI (5/2026)](https://www.bakermckenzie.com/en/insight/publications/2026/05/vietnam-redefining-copyright-for-ai), [Mondaq — Decree 134/2026](https://www.mondaq.com/copyright/1796822/vietnam-copyright-framework-critical-changes-under-decree-1342026), [IAPP](https://iapp.org/news/a/vietnam-clarifies-ai-authorship-training-data-and-copyright-liability-a-comparative-lens), [One Asia Lawyers](https://oneasia.legal/en/7348), [Conventus Law](https://conventuslaw.com/featured-content/artificial-intelligence-ai-and-vietnams-amended-ip-law-importance-of-the-human-factor/).

⭐⭐ **Phát hiện đáng chú ý nhất của §4**: bảng `Generation` ở §13 `Request.md` (prompt, model, model_version, seed, character_refs, style_refs, location_refs, input_panel, output_image, **parent_generation**, status) — tác giả thiết kế nó cho **reproducibility/debug**. Theo Nghị định 134, nó chính là **hồ sơ pháp lý bắt buộc** để chứng minh human contribution ở Việt Nam. Một feature engineering hóa ra là compliance artifact. **Đừng cắt nó khỏi MVP.** Cần bổ sung: lưu cả **các bước edit/regenerate của con người** (intermediate drafts) và **quyết định chọn/loại** — đó mới là bằng chứng "decisive contribution", không phải chỉ prompt.

#### 4.4. Terms of Service của model thương mại

- **Gemini API**: commercial use **được phép**; Google không claim ownership ảnh bạn tạo, không thu royalty; phải tuân Acceptable Use Policy. Nguồn: [ai.google.dev/gemini-api/terms](https://ai.google.dev/gemini-api/terms).
- **Nano Banana Pro có SynthID watermark** trên output ([vneconomy](https://vneconomy.vn/nano-banana-pro-moi-nhat-co-the-phat-hien-hinh-anh-do-ai-tao-ra.htm)) — hữu ích cho compliance Hàn Quốc, nhưng cần biết output có mang provenance signal.
- ⚠️ **Điều khoản về upload ảnh tham chiếu người thật / nhân vật có bản quyền: không tìm được quy định cụ thể, rõ ràng.** Không lấp bằng suy đoán. Cần đọc trực tiếp AUP + Prohibited Use Policy trước khi build. Rủi ro thực tế thấp trong use case này vì reference images là nhân vật **do chính hệ thống generate** (canonical portrait), không phải người thật.

---

### 5. Chi phí thực tế

#### 5.1. Giá API (8/2026)

**Official (verified từ trang nhà cung cấp):**

| Model | Standard | Batch |
|---|---|---|
| Gemini 3 Pro Image (Nano Banana Pro) 1K/2K | **$0.134/ảnh** | **$0.067/ảnh** |
| Gemini 3 Pro Image 4K | $0.24/ảnh | $0.12/ảnh |
| Gemini 3 Flash Image (Nano Banana 2) 1K | $0.067/ảnh | $0.034/ảnh |
| Gemini 3 Flash Image 2K | $0.101/ảnh | $0.050/ảnh |
| Gemini 2.5 Flash Image 1024² | $0.039/ảnh | $0.0195/ảnh |
| FLUX.2 [pro] | từ **$0.03** (t2i) / **$0.045** (edit) | — |
| FLUX.2 [flex] | từ $0.05 | — |
| FLUX.2 [klein] 4B | $0.014/MP | — |
| FLUX.1 Kontext [pro] / [max] | $0.04 / $0.08 | — |

**⚠️ Không official — chỉ là estimate của bên thứ ba:** GPT Image 2. Trang [developers.openai.com/api/docs/pricing](https://developers.openai.com/api/docs/pricing) **chỉ công bố token rate** ($8/1M image input, $30/1M image output, $5/1M text input), **không công bố per-image price**. Con số lưu hành ($0.006 low / $0.053 medium / $0.211 high tại 1024²; hoặc $0.03 @1K / $0.05 @2K / $0.08 @4K) là **estimate của bên thứ ba**, được chính họ ghi rõ *"not official list prices"*. Nguồn: [wavespeed.ai](https://wavespeed.ai/blog/posts/gpt-image-2-pricing-2026/), [nemovideo.com](https://www.nemovideo.com/blog/gpt-image-2-pricing-breakdown). Ghi nhận thêm: GPT Image 2 đã **bỏ knob low/medium/high, đổi sang output resolution 1K/2K/4K từ đầu 2026**.

#### 5.2. Tỉ lệ regenerate — KHÔNG CÓ DỮ LIỆU ĐÁNG TIN CẬY

**Không tìm được số liệu ngành nào về số lần generate cần để ra một ảnh dùng được.** Chỉ có ghi nhận định tính: *"artifacts in generations, distortions in animal or people figures, and uncanny compositions made users find generations unusable"*; một observation lẻ: user generate 4 ảnh, 2 đầu unusable, 2 sau "lukewarm" ([arXiv 2204.09007 Opal](https://arxiv.org/pdf/2204.09007) — paper từ 2022, đã lạc hậu).

→ Vì vậy chi phí được trình bày **tham số hóa theo hệ số regen 1x / 2x / 3x**, không bịa một con số.

#### 5.3. Bài toán chi phí — 1 chapter = 15 page × 4 panel = 60 ảnh

| Model | 1x | 2x | 3x | 100 chapter @2x |
|---|---|---|---|---|
| **Gemini 3 Pro Image, batch** ($0.067) | **$4,02** | $8,04 | $12,06 | **~$804** |
| Gemini 3 Pro Image, standard ($0.134) | $8,04 | $16,08 | $24,12 | ~$1.608 |
| Gemini 3 Flash Image, batch 1K ($0.034) | $2,04 | $4,08 | $6,12 | ~$408 |
| **FLUX.2 [pro]** ($0.03 / $0.045 edit) | **$1,80–2,70** | $3,60–5,40 | $5,40–8,10 | **~$360–540** |
| FLUX.2 [klein] ($0.014/MP) | ~$0,84 | ~$1,68 | ~$2,52 | ~$168 |
| GPT Image 2 (⚠️ estimate $0.03 @1K) | ~$1,80 | ~$3,60 | ~$5,40 | ~$360 |

**Kết luận chi phí**: **$400–1.600 cho 100 chapter** ở giả định regen 2x. Với dev đơn lẻ ngân sách tự bỏ (A1), đây **không phải blocker**. Con số này thấp hơn nhiều so với trực giác. Chi phí thật của project là **thời gian dev**, không phải inference.

Thêm: **batch mode giảm đúng 50%** giá Gemini. Vì comic generation là async job queue (§12 đã có Job Queue) → **batch mode là fit tự nhiên, phải dùng.** Khuyến nghị kiến trúc cụ thể: batch API, không phải realtime API.

#### 5.4. Self-host vs API — và tại sao câu hỏi này gần như vô nghĩa ở đây

**Số liệu self-host:**

- RTX 4090: **$0.34/hr** (RunPod Community, Vast.ai $0.39–0.50), $0.69/hr (RunPod Secure). H100 80GB SXM: $0.90–1.87/hr (Vast.ai), $2.89/hr (RunPod Secure PCIe). Nguồn: [spheron.network](https://www.spheron.network/blog/runpod-vs-vastai-2026/), [runpod.io/pricing](https://www.runpod.io/pricing).
- FLUX.2 [dev] trên 4090: **12–30s/ảnh 1024px**, cần quantization GGUF Q4/Q8 (~13–24GB) vì weight full precision là **64GB**; một report khác ghi ~3m09s ở FP16/28 steps. Nguồn: [tinytiny.tools](https://tinytiny.tools/en/blog/flux-2-self-hosting), [willitrunai.com](https://willitrunai.com/image-models/flux-2-dev).

**Điểm hòa vốn (tự tính, ghi rõ là estimate):** 4090 @ $0.34/hr, 20s/ảnh → 180 ảnh/hr → **~$0.0019/ảnh**. So với FLUX.2 pro API $0.03 → self-host rẻ hơn ~16x. **Về đơn giá thuần, self-host luôn thắng.**

⚠️ **Nhưng đây là câu trả lời sai cho câu hỏi thật.** FLUX.2 [dev] quantized **không phải** model dẫn đầu về multi-reference character consistency — chính năng lực đó là yêu cầu cốt lõi của project. Self-host tiết kiệm $600 nhưng đánh mất đúng thứ khiến project khả thi. Cộng thêm: 12–30s/ảnh × 60 ảnh = **12–30 phút/chapter** chỉ riêng GPU time, chưa tính retry.

**Khuyến nghị cho 1 dev, ngân sách tự bỏ:**

1. **Main generation path: API (Gemini 3 Pro Image batch hoặc FLUX.2 pro).** Chi phí đã đủ thấp để không cần tối ưu.
2. **Self-host chỉ cho việc phụ**: LoRA training ($2-5/LoRA trên 4090 thuê), upscale, inpainting, batch experimentation khi tune prompt compiler.
3. **Không mua GPU.** $400-1.600 cho 100 chapter thấp hơn giá một card 4090.

---

### 6. Rendering chữ trong ảnh — đặc biệt TIẾNG VIỆT ⚠️

#### 6.1. Tình trạng chung

Bối cảnh lịch sử: các model thương mại (DALL·E 3, Imagen 3, SD3, Ideogram 1.01) *"have demonstrated underwhelming performance in multilingual text rendering tasks"* ([arXiv 2503.18641](https://arxiv.org/pdf/2503.18641)).

**2026 đã khác:** Nano Banana Pro được Google công bố *"correctly rendered and legible text directly in the image"*, *"generate text in multiple languages, or localize and translate your content"* ([blog.google](https://blog.google/innovation-and-ai/products/nano-banana-pro/)). Đánh giá bên thứ ba: **~94-95% accuracy** với English text; xử lý được Chinese, Arabic, Cyrillic, Devanagari với letter shape đúng; *"for any application requiring accurate typography in languages beyond basic English, Nano Banana Pro is currently the only viable option among major image generators"* ([dejaoffice.com](https://www.dejaoffice.com/blog/2026/05/26/nano-banana-pro-the-image-model-with-the-best-text-rendering-right-now/), [bluefx.net](https://bluefx.net/blog/nano-banana-pro-review-95-percent-accurate-text/)). Caveat từ chính các nguồn này: *"Quality is highest in major world languages; less common languages may have more errors."*

#### 6.2. Tiếng Việt có dấu — có bằng chứng, nhưng là báo chí không phải benchmark

Nhiều nguồn báo Việt Nam xác nhận Nano Banana Pro xử lý được tiếng Việt có dấu:

- *"Nano Banana Pro gây sốc với khả năng tạo ảnh với chữ tiếng Việt cực chuẩn"* — [VietnamNet](https://vietnamnet.vn/nano-banana-pro-gay-soc-voi-kha-nang-tao-anh-voi-chu-tieng-viet-cuc-chuan-2465113.html)
- *"Google công bố AI tạo ảnh viết chữ chuẩn, hỗ trợ đầy đủ tiếng Việt có dấu"* — [Thời báo Ngân hàng](https://thoibaonganhang.vn/google-cong-bo-ai-tao-anh-viet-chu-chuan-ho-tro-day-du-tieng-viet-co-dau-173944.html)
- *"cải thiện đáng kể việc hiển thị chính xác chữ, gồm cả tiếng Việt, vốn thường bị lệch hoặc sai chính tả ở nhiều mô hình AI tạo ảnh"* — [Một Thế Giới](https://1thegioi.vn/nano-banana-pro-cua-google-giup-tao-anh-ai-voi-chu-tieng-viet-chinh-xac-hon-241322.html)

⚠️ **Đánh giá trung thực: đây là press coverage, KHÔNG phải benchmark có phương pháp.** Không tìm được nghiên cứu định lượng nào đo accuracy render tiếng Việt (đặc biệt các chữ chồng 2 dấu như "ế", "ữ", "ượ") của bất kỳ image model. Nền tảng khó khăn thì có tài liệu: *"Vietnamese... introduce additional complexity through diacritics and tonal marks that affect glyph rendering"* ([arXiv 2506.05061](https://arxiv.org/html/2506.05061)).

Điểm tham chiếu ngược (OCR, không phải generation): FastOCR nhận diện đúng cả 6 dấu thanh và stacked diacritics ở **96% trên clean printed text** ([fastocr.org](https://fastocr.org/vietnamese-ocr)).

#### 6.3. Khuyến nghị: BẮT BUỘC dùng typeset layer riêng — và không phải vì rendering

**Kết luận: generate ảnh KHÔNG có chữ, sau đó typeset bằng layer riêng (SVG/Canvas/PIL). Đây là bắt buộc kiến trúc, kể cả nếu model render tiếng Việt hoàn hảo 100%.**

Ba lý do độc lập, không liên quan tới chất lượng render:

1. **Editability.** Best practice ngành: *"Generate manga and comic panels with an editable lettering layer... you can rewrite, drag, and resize them **without regenerating the artwork**."* ([comicsai.org](https://www.comicsai.org/en/manga-speech-bubble-generator), [llamagen.ai](https://llamagen.ai/features/speech-bubble-generator)). Sửa một câu thoại không được đốt lại $0.067 + rủi ro mất consistency.
2. **Bubble không được che mặt.** *"The common problem is adding words after the art is already crowded. Bubbles then cover faces, hands, or action. Better lettering begins before final image approval."* → Panel spec (§6) **cần thêm field `text_safe_zone`** truyền vào prompt compiler để model để trống chỗ.
3. **Compliance.** Layer text riêng = phần "human-authored text" và "selection/arrangement" — đúng phần **được bảo hộ bản quyền** theo Zarya (§4.2). Nhúng chữ vào ảnh AI làm mờ ranh giới đó.

#### 6.4. Thư viện/công cụ typeset

- **Comical-JS** ([github.com/BloomBooks/comical-js](https://github.com/BloomBooks/comical-js)) — JS library duy nhất open-source tìm được: hiển thị và edit comic balloon, caption, callout float trên ảnh; **có UI control cho bubble tail**. Hạn chế được chính repo ghi: control vị trí/bounds bubble *"in the future may provide"* → **auto-placement chưa có**.
- Prior art học thuật cho auto-placement: *"Optimized speech balloon placement for automatic comics generation"*, ACM ([DOI 10.1145/2505483.2505486](https://doi.org/10.1145/2505483.2505486)) — cũ nhưng là thuật toán tham chiếu được.
- Heuristic ngành đã được viết ra rõ: bubble theo reading path (trái→phải, trên→dưới), không che key visual detail, thứ tự = reading order → bubble placement → wording.

→ **Không có thư viện nào làm auto-placement hoàn chỉnh.** Đây là phần **phải tự build**. Với tiếng Việt, thêm ràng buộc: line-height phải rộng hơn tiếng Anh vì dấu chồng ("ữ", "ế") ăn không gian phía trên; wrap phải dùng thư viện hiểu Unicode combining marks.

---

### 7. Novel → structured data: prior art

#### 7.1. Có, và nhiều hơn tưởng

⭐ **CANVAS: Continuity-Aware Narratives via Visual Agentic Storyboarding** — arXiv 2604.13452, 15/04/2026. **Đây là phát hiện quan trọng nhất của cả §7.**

Kiến trúc CANVAS dùng đúng ba intermediate representation:

1. **Global Continuity Plan (𝒫)**: track character appearance states (𝒞), location assignments (ℒ), object state transitions (𝒪) qua narrative → **= Story Bible + Timeline state của §2/§3**
2. **Visual State Memory (ℳ)**: character appearance anchors (ℳc), background anchors (ℳl), previously generated frames (ℳf) → **= Character Reference Sheet + Location Identity của §8/§10**
3. **Sequential retrieval + QA-based selection**: mỗi shot retrieve anchor từ memory, generate candidates, score bằng **VLM-based consistency questions** → **= Continuity Checker của §15**

Backbone image model: **Gemini-3-pro-image**. Kết quả: xem bảng ở §1.2. Limitation do chính tác giả nêu: tốn kém tính toán; không model được fine-grained physical interaction / complex motion; **giả định "narrative entities can be reliably extracted from text"**; HardContinuityBench còn nhỏ.

Nguồn: [arXiv 2604.13452v1](https://arxiv.org/html/2604.13452v1).

**Prior art khác:**

| Công cụ/paper | Nội dung | Nguồn |
|---|---|---|
| **ContinuityEval** (trong CANVAS) | VLM metric fine-grained, 3 chiều: character (face/clothing/body identity), background (geometric stability), prop (identity + placement). Likert 1–5. | arXiv 2604.13452 |
| **VinaBench** | Benchmark faithful & consistent visual narratives; dùng VLM kiểm "whether generated images for multiple scenes all show the same character" | [arXiv 2503.20871](https://arxiv.org/pdf/2503.20871) |
| **R²** | LLM-based **Novel-to-Screenplay generation framework với Causal Plot Graphs** — gần đúng "Comic Script Engine" §4 | [arXiv 2503.15655](https://arxiv.org/pdf/2503.15655) |
| **GraphLit** | Text-enriched **dynamic character network representations** for literary study | [arXiv 2605.28643](https://arxiv.org/pdf/2605.28643) |
| **Lost in Stories** | Consistency bugs in long story generation by LLMs — taxonomy lỗi | [arXiv 2603.05890](https://arxiv.org/html/2603.05890v1) |
| **TLDM** | 40 novel tiếng Anh, <32k → >128k token; task: summarization, **storyworld description, narrative time estimation** | [arXiv 2505.14925](https://arxiv.org/html/2505.14925) |
| **NarraBench** | Framework narrative benchmarking, EACL 2026 | qua arXiv 2505.14925 |
| **DynaVieW** | Schema-guided world modeling, đánh giá character consistency qua VLM | [arXiv 2607.04112](https://arxiv.org/pdf/2607.04112) |
| **Zooming into Comics** | Region-aware RL cải thiện fine-grained comic understanding trong VLM | [arXiv 2511.06490](https://arxiv.org/pdf/2511.06490) |

#### 7.2. Con số accuracy tham chiếu

- **Literary evidence retrieval** (long-context, hiểu văn học): **Gemini Pro 2.5 = 62,5%** vs **human expert 55,0%**; open-weight models chỉ **29,1%**. Nguồn: [arXiv 2506.03090](https://arxiv.org/html/2506.03090v1).
  → Tín hiệu quan trọng: frontier closed model **vượt human expert** ở task hiểu văn học, còn open-weight kém hơn 2x. **Story Analyzer không được dùng model open-weight nhỏ.**
- **MIE evaluator** (MIBE): 0.922 overall pairwise accuracy vs human preference (0.982 seen / 0.884 unseen generator); Silver Set đạt **95,1% cross-VLM preference agreement**. → **VLM làm autorater cho continuity check là đã được validate định lượng.**
- Cảnh báo nền: LLM *"often fail to maintain consistency... contradicting their own established facts, character traits, and world rules"* qua narrative dài — đúng lý do vì sao Story Bible không phải optional.

Extraction pattern được literature xác nhận: **two-stage extract-then-relate** — scene-by-scene processing, extract relation triple (subject-predicate-object) từng scene → knowledge graph quan hệ nhân vật. → Khuyến nghị cụ thể: Story Analyzer nên **chunk theo scene, không theo chapter**, và extract dạng triple.

---

### 8. Kết luận nghiên cứu

#### 8.1. Verdict

**✅ KHẢ THI CÓ ĐIỀU KIỆN (technically feasible, conditionally)**

Ý tưởng **không** là science fiction — nó là kiến trúc đã được một paper peer-reviewable (CANVAS, 4/2026) implement và đo lường thành công. Nhưng khả thi **chỉ trong 4 điều kiện đồng thời**:

1. **≤3 nhân vật/panel**, cứng hóa trong Comic IR. Cảnh đông người dùng shot xa/silhouette/crop. (Bằng chứng: CogCanvas — attribute binding thất bại gần hoàn toàn từ 4 người.)
2. **Chữ đi qua typeset layer riêng, KHÔNG nhúng vào ảnh AI.** (3 lý do độc lập ở §6.3.)
3. **Nguồn truyện là IP tự sở hữu hoặc đã licensed.** Nếu là truyện tác giả khác → tool chỉ dùng private, không xuất bản. (§4.1)
4. **Có AI provenance/disclosure ở export path** nếu nhắm platform có Korea là market (Webtoon, Tapas, Tappytoon). (§3.3)

Cộng thêm: **chi phí không phải rào cản** ($400–1.600/100 chapter). Rào cản thật là **thời gian của 1 dev** (A1).

#### 8.2. Bảng khả thi từng thành phần

| Thành phần | Trạng thái | Bằng chứng |
|---|---|---|
| **Story Bible extraction** | ✅ **Đã giải được** | CANVAS Global Continuity Plan hoạt động thực tế; two-stage extract-then-relate là pattern đã xác lập; Gemini Pro 2.5 đạt 62,5% > human expert 55,0%; ComicInk đã ship extract 20-character roster từ novel 500 trang. **Caveat**: CANVAS tự nêu limitation là nó *giả định* entity extract được đáng tin cậy. |
| **Timeline state / query "state @ Ch12"** | 🟡 **Giải được một phần** | Sudowrite đã ship "entries tagged by timeline... character states per era" — nhưng cho novel writing, không phải comic. **Chưa có** ai làm queryable timeline state cho comic generation. Là engineering, không phải research risk. |
| **Comic IR / Comic Script Engine** | ✅ **Đã giải được** | R² (Novel-to-Screenplay với Causal Plot Graphs); CANVAS shot decomposition; mọi đối thủ đều làm được ở mức nào đó. Rủi ro thấp nhất trong bảng. |
| **Character consistency — 1 nhân vật/panel** | ✅ **Đã giải được** | CANVAS character avg **4.91/5** trên HardContinuityBench với Gemini-3-pro-image; human preference 86,7% win-rate. Đủ tốt để xuất bản. |
| **Multi-character panel (2–3 nhân vật)** | 🟡 **Giải được một phần** — hàng load-bearing nhất | Triangulation 3 nguồn: (a) **vendor claim** Google "up to 5 people" / 14 reference images — chưa verify độc lập; (b) **open-source benchmark** CogCanvas: ID-Sim 42.33 (2 người) → 27.21 (3) → 2.67 (4) → 0.52 (5); (c) **pipeline-level** CANVAS 4.91/5 nhưng nhờ agentic memory + VLM selection, **không phải raw model**. **Không tìm được benchmark độc lập nào đo frontier model ở 2-3 nhân vật.** → Phải verify từng panel + regenerate. |
| **Multi-character panel (4+)** | ❌ **Chưa giải được** | CogCanvas: *"near-complete failure on object/fashion binding beyond three subjects"*; Nano Banana Pro blend traits/merged faces khi vượt giới hạn. |
| **Location consistency** | ✅ **Đã giải được** | CANVAS: Consecutive BG **4.88/5**, Non-consecutive BG **4.88/5** (baseline 4.06) — **background giữ tốt hơn cả qua các shot không liên tiếp**, đúng lo ngại §10. Cơ chế: background anchors trong Visual State Memory. |
| **Props / vũ khí consistency** | 🟡 **Giải được một phần** | CANVAS Props chỉ **4.19/5** — thấp nhất trong 4 metric, cải thiện so baseline chỉ +2,5%. Đúng khớp ví dụ "✗ sword missing" §15. Cần Continuity Checker nhắm riêng vào props. |
| **Text rendering tiếng Việt trong ảnh** | 🟡 **Giải được một phần — nhưng đừng dùng** | Press VN xác nhận Nano Banana Pro render tiếng Việt có dấu tốt; Google claim multilingual; ~94-95% accuracy English. **Không có benchmark định lượng nào cho tiếng Việt.** → Dùng typeset layer bất kể, vì 3 lý do ở §6.3. |
| **Auto speech-bubble typesetting** | 🟡 **Giải được một phần — phải tự build** | Comical-JS có bubble/tail rendering nhưng auto-placement ghi rõ *"in the future may provide"*. Prior art thuật toán: ACM DOI 10.1145/2505483.2505486. Là phần **tự viết**. |
| **Continuity check bằng VLM** | ✅ **Đã giải được** | **ContinuityEval** (CANVAS): VLM autorater 3 chiều, Likert 1-5, đã dùng làm metric trong paper. **MIE** (MIBE): 0.922 pairwise accuracy vs human preference, 0.884 trên unseen generator. → Không phải ý tưởng suy đoán, là kỹ thuật có số. |
| **AI Layout Director / Layout Score** | ⚪ **Không tìm được prior art trực tiếp** | Không tìm được paper/tool nào về narrative-importance-driven panel layout với scoring như §5. Có thể là phần **thật sự mới** — hoặc là phần chưa ai làm vì không đáng. Không đủ dữ liệu để kết luận. |

#### 8.3. Top 3 phát hiện làm anh đổi ý

**#1 — Kiến trúc của anh ĐÚNG, nhưng KHÔNG MỚI. Moat không nằm ở concept.**

CANVAS (arXiv 2604.13452, 15/04/2026) đã implement gần như đúng từng thành phần: Global Continuity Plan ≈ Story Bible + Timeline state, Visual State Memory ≈ Canonical References, QA-based selection ≈ Continuity Checker — trên backbone Gemini-3-pro-image, và **đo được**: character 4.91/5, 86,7% human win-rate.

Điều này cắt hai chiều:

- **Tốt**: không phải đánh cược vào một giả thuyết. Kiến trúc đã được validate bằng số. Câu "Story Bible + Timeline State + Canonical References + Visual Prompt Compiler + Continuity Checker" ở cuối `Request.md` là **đúng về mặt kỹ thuật** — research đồng ý.
- **Xấu**: câu *"Đây mới là moat của sản phẩm"* là **sai**. Concept đã public trên arXiv, ai đọc cũng dùng được. Moat thật phải là **execution + product** (UI editor kiểu Figma ở §14, VN-language support, workflow cho truyện 100+ chương). Đồng thời: **chưa có sản phẩm thương mại nào ship nó** (ComicInk sâu nhất mà vẫn chỉ dùng "story so far" summary text + cap 20 nhân vật / 12 issues). Khoảng cách research → product **đang mở**, nhưng cửa sổ này sẽ hẹp lại.

**#2 — Bảng `Generation` không phải feature engineering. Nó là hồ sơ pháp lý bắt buộc ở Việt Nam.**

Nghị định **134/2026/NĐ-CP** hiệu lực **09/04/2026** (post-cutoff, không thể biết từ ký ức): tác phẩm AI-assisted chỉ được bảo hộ nếu con người có *"substantial and decisive intellectual contribution"*, và creator **phải lưu giữ prompts, inputs, intermediate drafts** + disclose khi được yêu cầu. Bảng `Generation` (§13) **chính là artifact đó**.

→ Ba hệ quả: (a) **không được cắt** `Generation` khỏi MVP để "làm nhanh"; (b) phải lưu thêm **các bước human edit/regenerate và quyết định chọn-loại**, vì đó mới là bằng chứng "decisive contribution", prompt một mình không đủ; (c) `parent_generation` chain trở thành audit trail có giá trị pháp lý.

**#3 — Consistency đã HẠ CẤP khỏi vị trí "boss cuối". Boss cuối thật là ba thứ khác.**

§7 gọi style/character consistency là boss cuối. Đúng ở thời điểm viết, nhưng ngành ghi nhận consistency chuyển từ *"mostly impossible"* sang *"actually workable"* trong cuối 2025–đầu 2026. Ba boss thật:

- **Multi-character attribute binding** — CogCanvas: model vẽ ra ảnh "visually plausible" nhưng **gắn sai trang phục cho sai người**. Đây là loại lỗi Continuity Checker phải bắt, và cũng là lỗi khó bắt nhất vì ảnh trông ổn.
- **Props continuity** — CANVAS 4.19/5, kém nhất. "Sword missing" là lỗi hệ thống, không phải lỗi lẻ.
- **Backlash & pháp lý, không phải công nghệ** — Naver Webtoon bị **boycott subscription**; BlueLine Studio phải **vẽ lại episode** *Knight King*; Korea AI Basic Act hiệu lực 22/01/2026, phạt tới 30 triệu won. Rủi ro lớn nhất của project 8/2026 **không còn là "AI vẽ có giống không"** mà là **"xuất bản được không, và có bị tẩy chay không"**.

**Bonus #4 — Chi phí thấp hơn trực giác nhiều.** $400–1.600 cho 100 chapter. Đừng thiết kế kiến trúc để tối ưu chi phí inference — hãy thiết kế để tối ưu **thời gian dev** và **tỉ lệ panel dùng được ngay lần đầu**.

#### 8.4. Khuyến nghị công nghệ cụ thể — nếu bắt đầu hôm nay

| Lớp | Khuyến nghị | Giá | Lý do có nguồn |
|---|---|---|---|
| **Story understanding (Layer 1)** | **Gemini 3 Pro** (hoặc frontier closed model tương đương). **KHÔNG dùng open-weight nhỏ.** | theo token | Gemini Pro 2.5 đạt 62,5% literary evidence retrieval > human expert 55,0%; open-weight chỉ 29,1% |
| **Chunking strategy** | Scene-by-scene, extract relation triple (subj-pred-obj) → knowledge graph. Không chunk theo chapter. | — | Pattern extract-then-relate xác lập trong literature |
| **Image gen (Layer 3) — chính** | **Gemini 3 Pro Image (Nano Banana Pro) qua BATCH API** | **$0.067/ảnh 1K-2K** | Backbone của CANVAS (char 4.91/5); 14 reference images / 5 người; batch giảm đúng 50% và fit job queue §12 |
| **Image gen — dự phòng / rẻ hơn** | **FLUX.2 [pro]** | **$0.03 (t2i) / $0.045 (edit)** | 10 reference images, official BFL price; rẻ hơn ~2x; giữ được kiến trúc "đổi model dễ" của §16 |
| **Thử nghiệm/tune giá rẻ** | Gemini 3 Flash Image batch | $0.034/ảnh 1K | Rẻ nhất trong họ Gemini, đủ để iterate prompt compiler |
| **LoRA (tùy chọn)** | FLUX LoRA, 12–25 ảnh, train trên RunPod RTX 4090 thuê | **$0.34/hr → $2–5/LoRA** | Dùng cho nhân vật chủ chốt; ~$40-100 cho 20 nhân vật |
| **Text / speech bubble** | **Layer riêng: SVG hoặc Canvas.** Comical-JS làm điểm khởi đầu; auto-placement tự viết theo heuristic reading-path. **Panel spec thêm field `text_safe_zone`.** | free | 3 lý do độc lập §6.3; Comical-JS chưa có auto-placement |
| **Continuity Checker** | VLM autorater theo pattern **ContinuityEval**: 3 chiều, Likert 1-5. Generate N candidates → VLM QA select. | theo token | CANVAS đã dùng; MIE đạt 0.922 pairwise accuracy. Ưu tiên props vì đó là chiều yếu nhất (4.19/5) |
| **Self-host** | **Không dùng cho main path.** Chỉ cho LoRA train, upscale, inpainting. Không mua GPU. | 4090 $0.34/hr | FLUX.2 dev quantized không phải leader về multi-ref consistency; $400-1.600/100 chapter thấp hơn giá một card |
| **Ràng buộc thiết kế cứng** | ≤3 nhân vật/panel trong Comic IR schema | — | CogCanvas: attribute binding sụp từ 4 người |
| **Compliance** | Field AI provenance ở page/panel; export path nhúng machine-readable watermark; `Generation` lưu cả human edit steps | — | Korea AI Basic Act 22/01/2026; NĐ 134/2026 Điều 5a record-keeping |

**Về thứ tự MVP (§18)** — dữ liệu ủng hộ thứ tự với một điều chỉnh: MVP 1 (Story Intelligence) là **đúng** và là phần rủi ro thấp nhất. Nhưng nên **đẩy một spike nhỏ của MVP 3 lên sớm**: test 20-30 panel với 2-3 nhân vật trên Nano Banana Pro để tự đo cái mà **không benchmark công khai nào đo** — vì đó là hàng "giải được một phần" load-bearing duy nhất. Chi phí spike: 30 ảnh × $0.134 × 3 lần thử ≈ **$12**.

---

### Các khoảng trống KHÔNG lấp được (ghi trung thực)

1. **Benchmark độc lập đo frontier model (Nano Banana Pro / GPT Image 2 / FLUX.2) ở 2–3 nhân vật/panel** — không tồn tại trong dữ liệu công khai.
2. **Tỉ lệ regenerate thực tế** — không có số liệu ngành. Đã tham số hóa 1x/2x/3x.
3. **Benchmark định lượng render tiếng Việt có dấu** của bất kỳ image model — chỉ có press coverage.
4. **Số liệu CHI 2026 paper về thái độ độc giả webtoon với AI** — fetch bị 403.
5. **Willingness-to-pay study** cho tác giả web novel với tool adapt truyện — không tìm được.
6. **Bài học từ startup thất bại trong ngách này** — không tìm được shutdown nào được xác nhận (≠ chưa ai thất bại).
7. **ToS cụ thể về upload ảnh tham chiếu người thật / nhân vật có bản quyền** — không tìm được điều khoản rõ ràng.
8. **Prior art cho AI Layout Director / Layout Score** (§5) — không tìm được gì trực tiếp.
9. **GPT Image 2 official per-image price** — OpenAI chỉ công bố token rate.

---

## PM đọc được gì

1. **Lens này lật ngược luận điểm trung tâm của `Request.md`.** Tác giả kết luận 5 thành phần là moat. Research cho thấy CANVAS đã public gần đúng kiến trúc đó trên arXiv từ 15/04/2026. → Hội tụ với kết luận độc lập của lens PM (mục 2, `product-manager-pm-lens.md`): đây là *barrier to entry*, không phải moat. **Hai lens đến từ hai hướng khác nhau, cùng một kết luận** ⇒ đây là phát hiện mạnh nhất của run.
2. **Nhưng cùng dữ liệu đó cũng là tin TỐT lớn nhất.** Kiến trúc được validate bằng số (character 4.91/5, 86,7% human win-rate) nghĩa là anh **không** đang đánh cược vào giả thuyết. Rủi ro kỹ thuật của MVP1–MVP2 thấp hơn PM tưởng trước fan-out.
3. **Chi phí thấp hơn trực giác một bậc độ lớn** ($400–1.600/100 chapter). Điều này **hủy** một phần lo ngại "ngân sách" của Assumption A1 và làm câu hỏi OQ3 ở GATE bớt quan trọng. Ràng buộc thật là **thời gian 1 dev** — đúng như lens architect kết luận độc lập.
4. **Nghị định VN 134/2026 là thông tin PM không thể tự biết** (hiệu lực 09/04/2026, sau knowledge cutoff). Nó **đảo chiều** một khuyến nghị PM đã viết: mục 5 của `product-manager-pm-lens.md` ghi *"Giữ `Generation` tối giản — bỏ cây `parent_generation` ở MVP"*. **Khuyến nghị đó SAI và PM thu hồi.** `parent_generation` là audit trail có giá trị pháp lý ở VN. Đây là ví dụ đúng cho việc vì sao fan-out cần một lens có web access.
5. **Rủi ro pháp lý được xác nhận là rủi ro nhị phân, đúng như PM xếp hạng** — và research làm nó sắc hơn: Zarya of the Dawn cho thấy phần **được bảo hộ** chính là panel layout + arrangement + text, tức là đúng output của Comic IR. Kiến trúc "spec là dữ liệu chính" của tác giả **trùng khớp đường ranh pháp lý** — một sự trùng hợp đáng nêu trong tài liệu deliverable.
6. **`≤3 nhân vật/panel` là ràng buộc thiết kế cứng, có số làm căn cứ.** Đây là loại khuyến nghị hành động được ngay, phải đưa vào deliverable ở dạng nổi bật.
7. **Lens này trung thực về giới hạn của chính nó** — 9 khoảng trống được đánh dấu rõ, và nó phân biệt được "không tìm thấy shutdown" với "chưa ai thất bại". Tăng độ tin cậy của phần còn lại.

## Mâu thuẫn với lens khác

| # | Mâu thuẫn | PM phân xử |
|---|---|---|
| M1 | **`researcher` ủng hộ thứ tự MVP của §18** ("MVP1 là đúng và rủi ro thấp nhất", chỉ đề xuất thêm spike $12). **`architect` và lens PM đề xuất ĐẢO thứ tự** để de-risk consistency trước. | **Không phải mâu thuẫn thật — là cùng một kết luận diễn đạt khác nhau.** Cả ba đều nói: *đẩy việc kiểm chứng consistency lên sớm*. `researcher` gọi nó là "spike nhỏ của MVP3 lên trước", `architect` gọi là "vertical slice MVP0", PM gọi là "MVP0". Ba tên, một việc. **Deliverable dùng một tên duy nhất: MVP0**, và ghi rõ nó được cả ba lens độc lập đề xuất — đó là tín hiệu mạnh. Điểm khác biệt thật duy nhất: `researcher` nói MVP1 rủi ro *thấp* (có bằng chứng CANVAS), nên **không cần cắt MVP1**, chỉ cần chèn MVP0 trước nó. PM chấp nhận cách đọc này vì nó có dữ liệu hậu thuẫn. |
| M2 | **`architect` GĐ-1**: giả định consistency đạt bằng *reference-image conditioning*, không phải fine-tune per-character. | ✅ **`researcher` XÁC NHẬN.** Native multi-image reference model là hướng khuyến nghị; LoRA chỉ là "lớp tăng cường tùy chọn, không phải nền tảng". → GĐ-1 đúng, `architect` **không** cần thêm entity `character_model` có version ở MVP. |
| M3 | **`architect` GĐ-2**: closed API nên reproducibility đúng nghĩa không đạt được; `seed` chỉ còn giá trị provenance; mục tiêu thật của `Generation` là auditability/lineage. | ✅ **`researcher` XÁC NHẬN VÀ NÂNG CẤP.** Đúng là auditability, không phải reproducibility — nhưng `researcher` cho biết auditability đó là **nghĩa vụ pháp lý** ở VN (NĐ 134/2026), không chỉ tiện lợi kỹ thuật. `architect` suy ra đúng bản chất mà không biết lý do pháp lý. Hai lens hội tụ, và lens có web access giải thích được *vì sao*. |
| M4 | **`architect` GĐ-3**: model không render được text tiếng Việt có dấu ở chất lượng xuất bản. | 🟡 **`researcher` BÁC BỎ MỘT PHẦN** — press VN xác nhận Nano Banana Pro render tiếng Việt có dấu tốt, dù không có benchmark định lượng. **NHƯNG kết luận hành động của `architect` vẫn ĐÚNG**, vì `researcher` khuyến nghị typeset layer riêng *bất kể* chất lượng render, dựa trên 3 lý do độc lập (editability, bubble không che mặt, ranh giới bản quyền). → Deliverable phải trình bày cẩn thận: *tiền đề của `architect` sai, kết luận đúng, và đúng vì lý do mạnh hơn lý do nó nêu.* |
| M5 | **PM (mục 5)**: "Giữ `Generation` tối giản, bỏ `parent_generation` ở MVP". | ❌ **PM tự thu hồi.** Xem *PM đọc được gì* #4. NĐ 134/2026 biến nó thành compliance artifact. |
| M6 | **PM (mục 2)** và **`researcher` (§2.3)** cùng nêu rủi ro over-engineering, nhưng khác góc: PM lo *thiếu định nghĩa người dùng*; `researcher` lo *use case 100+ chương chưa được thị trường chứng minh* (ComicInk cap 12 issues có thể là quyết định product, không phải kỹ thuật). | **Bổ sung cho nhau, không xung đột.** Gộp thành một rủi ro trong deliverable: *giá trị của Story Bible tỉ lệ thuận với độ dài truyện, và chưa có bằng chứng thị trường cho đầu dài.* Đây là câu hỏi OQ2 ở GATE. |
| M7 | Chờ `senior-ai-engineer` — đặc biệt phản biện **Layout Score §5**. `researcher` xếp nó ⚪ *"không tìm được prior art trực tiếp"* và nêu hai cách đọc: có thể thật sự mới, hoặc chưa ai làm vì không đáng. | Chờ lens AI phân định. Đây là chỗ duy nhất còn thiếu dữ liệu để kết luận. |
