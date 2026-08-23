# Findings — researcher (DELTA sau GATE)

> Tiếp nối `researcher.md`. Delta dispatch qua `SendMessage` (resume, không spawn mới). 26/30 tool call.
> Giả định mới: 1 dev xây **SaaS thương mại multi-tenant**, user tự upload truyện của họ.
> **File này ghi đè `researcher.md` ở đúng những điểm nó nêu.** Agent không có `Write` → PM lưu nguyên văn.

## Kết luận của worker

### Câu 1 — Nghị định 134/2026 Điều 37a/37c áp cho nền tảng thương mại thế nào?

#### 1.1. Một luật MỚI, chưa biết ở lần trước, và quan trọng hơn Điều 37a

⭐⭐ **LUẬT TRÍ TUỆ NHÂN TẠO 2025 — Luật số 134/2025/QH15.** Quốc hội khóa XV Kỳ họp thứ 10 thông qua **10/12/2025**, **hiệu lực 01/03/2026**.

Phạm vi: *"quy định về nghiên cứu, phát triển, **cung cấp, triển khai** và sử dụng hệ thống trí tuệ nhân tạo; quyền, nghĩa vụ của tổ chức, cá nhân có liên quan và quản lý nhà nước đối với hoạt động trí tuệ nhân tạo tại Việt Nam."*

→ **Một SaaS comic-studio đặt tại Việt Nam là "nhà cung cấp" và/hoặc "nhà triển khai" hệ thống AI theo luật này.** Nghĩa vụ trực tiếp, không phải gián tiếp qua copyright.

| Điều khoản | Nội dung |
|---|---|
| **Khoản 4 Điều 11** | Nội dung âm thanh/hình ảnh/video tạo ra hoặc chỉnh sửa bằng AI nhằm **mô phỏng người thật hoặc sự kiện thực tế** phải được **gắn nhãn dễ nhận biết**. Nhà cung cấp phải bảo đảm nội dung do hệ thống AI tạo ra được **đánh dấu bằng định dạng máy đọc** theo quy định của Chính phủ. |
| **Điều 11 (minh bạch)** | Phải có cơ chế để **người dùng nhận biết khi đang tương tác với hệ thống AI**. |
| **Điều 8** | Nhà cung cấp và nhà triển khai phải **đăng ký thử nghiệm có kiểm soát, báo cáo sự cố nghiêm trọng, báo cáo định kỳ**. |
| **Điều 8 — chuyển tiếp** | Hệ thống đang tồn tại có **18 tháng** (y tế/giáo dục/tài chính) hoặc **12 tháng** (lĩnh vực khác) để tuân thủ, tính từ 01/03/2026 → comic-studio: deadline **~01/03/2027**. |
| **Điều 7 — nghiêm cấm** | Lợi dụng/chiếm đoạt hệ thống AI xâm phạm quyền; deepfake lừa dối/lũng đoạn dư luận; nhắm nhóm dễ bị tổn thương; **thu thập dữ liệu trái pháp luật để huấn luyện AI**; cản trở kiểm soát của con người hoặc **che giấu thông tin minh bạch bắt buộc**. |

Nguồn: [thuvienphapluat.vn](https://thuvienphapluat.vn/chinh-sach-phap-luat-moi/vn/ho-tro-phap-luat/chinh-sach-moi/106139/luat-tri-tue-nhan-tao-2025-chinh-thuc-co-hieu-luc), [luatminhkhue.vn](https://luatminhkhue.vn/yeu-cau-bat-buoc-doi-voi-noi-dung-tao-boi-ai-tu-1-3-2026.aspx), [pbgdpl.cantho.gov.vn](https://pbgdpl.cantho.gov.vn/mot-so-diem-moi-cua-luat-tri-tue-nhan-tao), [genk.vn](https://genk.vn/tu-hom-nay-1-3-luat-tri-tue-nhan-tao-co-hieu-luc-noi-dung-ai-tao-ra-phai-co-dau-nhan-biet-165260301185217976.chn), [baohatinh.vn](https://baohatinh.vn/tv/luat-tri-tue-nhan-tao-2025-viet-nam-bat-buoc-gan-nhan-noi-dung-ai-tu-thang-32026-32240.html), [Sở KHCN Đồng Nai](https://skhcn.dongnai.gov.vn/vi/news/khoa-hoc-va-cong-nghe/luat-tri-tue-nhan-tao-chinh-thuc-co-hieu-luc-tu-thang-3-2026-1000.html).

⚠️ **Điểm không tự kết luận**: khoản 4 Điều 11 nói *"mô phỏng người thật hoặc sự kiện thực tế"* — comic nhân vật hư cấu **có thể không** rơi vào phạm vi. Nhưng câu tiếp theo cùng nguồn nói nhà cung cấp phải bảo đảm nội dung AI được đánh dấu định dạng máy đọc, **không** giới hạn "mô phỏng người thật". **Hai câu có thể mâu thuẫn về phạm vi, và không đọc được nguyên văn** (thuvienphapluat + luatminhkhue đều trả 403). → Câu cần luật sư.

Tin thực dụng: Nano Banana Pro **đã nhúng SynthID** — nếu quy định chấp nhận watermark của provider thì nghĩa vụ gần như tự động thỏa. Phải verify, không giả định.

#### 1.2. Điều 37a có áp cho extraction thương mại không? — KHÔNG RÕ, CẦN LUẬT SƯ

**Tầng 1 — nguyên văn phạm vi (verify được):** NĐ 134/2026/NĐ-CP ban hành **06/04/2026**, hiệu lực **09/04/2026**, bổ sung **Mục 3 Chương III**: *"Sử dụng văn bản và dữ liệu là đối tượng được bảo hộ quyền tác giả, quyền liên quan đối với hệ thống trí tuệ nhân tạo"* (Điều 37a, 37b, 37c). Phạm vi ghi rõ: *"điều kiện sử dụng văn bản và dữ liệu... để **nghiên cứu khoa học, thử nghiệm, huấn luyện** hệ thống trí tuệ nhân tạo"*. Điều 37c: *"tổ chức, cá nhân sử dụng văn bản và dữ liệu **để huấn luyện** hệ thống trí tuệ nhân tạo, khi khai thác thương mại phải thực hiện nghĩa vụ trả tiền bản quyền kể từ khi sử dụng"*.

Nguồn official: [Cục Bản quyền tác giả (cov.gov.vn)](https://cov.gov.vn/tin-tuc/gioi-thieu-nghi-dinh-so-1342026ndcp-quy-dinh-ve-quyen-tac-gia-quyen-lien-quan-168925.html). Xác nhận: [Mondaq](https://www.mondaq.com/copyright/1796822/vietnam-copyright-framework-critical-changes-under-decree-1342026), [Baker McKenzie](https://www.bakermckenzie.com/en/insight/publications/2026/05/vietnam-redefining-copyright-for-ai).

**Tầng 2 — lập luận (đánh dấu rõ: phân tích, không phải nguồn):** cả ba điều đóng khung quanh **"huấn luyện"**. Use case comic-studio **không phải training** — nó là **inference-time extraction**: gọi LLM đọc văn bản user upload để rút Story Bible. Hành vi pháp lý khác: không tạo model mới, không lưu nội dung vào weights, xử lý **theo chỉ dẫn của chính người upload**; nếu user là chủ quyền thì bản chất là chủ quyền tự khai thác tác phẩm mình, nền tảng chỉ là công cụ. → Nếu đúng, giới hạn "phi thương mại" Điều 37a **không áp**, và Điều 37c cũng không phát sinh (không có "hệ thống được huấn luyện" nào để khai thác).

**Tầng 3 — vì sao KHÔNG kết luận:** luật so sánh cho thấy đây là vùng chưa test. *"The exception is primarily focused on the training phase, not inference"*; *"Whether this exception applies to AI model training remains legally uncertain"*; riêng nội dung user upload: *"the analysis becomes more complex since such content may not fall into the standard categories addressed by most TDM exception discussions, particularly regarding **whether users have sufficient rights to authorize TDM uses by commercial AI services**"* — [DLA Piper / Lexology](https://mse.dlapiper.com/post/102ivrx/training-ai-models-content-copyright-and-the-eu-and-uk-tdm-exceptions), [CMS Law-Now](https://cms-lawnow.com/en/ealerts/2024/10/ai-and-copyright-exploring-exceptions-for-text-and-data-mining). Và **không đọc được nguyên văn Điều 37a** (cov.gov.vn chỉ có bản giới thiệu; thuvienphapluat 403; IAPP paywall).

> ⚖️ **KẾT LUẬN: KHÔNG TRA RA CÂU TRẢ LỜI DỨT KHOÁT. CẦN LUẬT SƯ SHTT VIỆT NAM.**
>
> Ba câu đã narrow xuống mức trả lời được, để đưa cho luật sư:
> 1. Điều 37a NĐ 134/2026 có áp cho **inference-time extraction** trên nội dung user upload, hay chỉ áp cho **huấn luyện** model?
> 2. Khoản 4 Điều 11 Luật TTNT 2025 — nghĩa vụ đánh dấu định dạng máy đọc áp cho **mọi** nội dung AI, hay chỉ nội dung *"mô phỏng người thật hoặc sự kiện thực tế"*? Watermark provider (SynthID) có thỏa không?
> 3. Nền tảng có được coi là "doanh nghiệp cung cấp dịch vụ trung gian" để hưởng miễn trừ **Điều 198b Luật SHTT** không?
>
> **Rủi ro nhị phân** — trả lời sai không làm sản phẩm chậm, mà làm sản phẩm **bất hợp pháp**. Chi phí một buổi tư vấn thấp hơn nhiều chi phí build sai.

#### 1.3. Điều 37b (opt-out) — ảnh hưởng gián tiếp

Tác giả có thể **bảo lưu quyền** qua: metadata, biện pháp bảo vệ công nghệ, **thông tin quản lý quyền dạng máy đọc**, hoặc thông báo công khai từ tổ chức quản lý tập thể. Nếu Điều 37a **không** áp thì 37b cũng không. Nhưng nếu cơ quan chức năng coi extraction là TDM, nền tảng **phải kiểm machine-readable opt-out signal** trước khi xử lý. → **Rẻ để phòng ngừa**: thêm bước kiểm metadata/rights-management-info của file upload, log kết quả. Chi phí ~0, xóa được một nhánh rủi ro.

#### 1.4. Trách nhiệm nền tảng khi user upload truyện không có quyền — CÓ safe harbour, có điều kiện

**Điều 198b Luật SHTT** (sửa đổi 2022, Luật 07/2022/QH15) — miễn trừ trách nhiệm cho **doanh nghiệp cung cấp dịch vụ trung gian**. Chuyển hóa từ **Điều 12.55 EVFTA**. Bao ít nhất: mere conduit, caching, **hosting**.

Điều kiện với **hosting** — **có điều kiện, không tự động**:

- (a) **không biết** nội dung đó xâm phạm quyền;
- (b) **hành động kịp thời** xóa hoặc ngăn truy cập khi biết.

Nguồn: [Lexology — Safe Harbor under 2022 IP Law of Vietnam](https://www.lexology.com/library/detail.aspx?g=d865aa00-fd06-41ab-bde8-cd2f4f604cc1), [Lexology — 10 Key Changes](https://www.lexology.com/library/detail.aspx?g=471adf5e-858c-4a39-aae4-b6d40921dc76), [KENFOX — Notice and takedown regime](https://kenfoxlaw.com/notice-and-takedown-regime-against-online-ipr-infringement-in-vietnam).

**NĐ 17/2023 + NĐ 134/2026 — nghĩa vụ notice-and-takedown cụ thể:**

| Nghĩa vụ | Chi tiết |
|---|---|
| Công cụ tiếp nhận | OSP cung cấp **dịch vụ hosting** phải lập công cụ tiếp nhận yêu cầu xóa/ngăn truy cập. Có thể là **chương trình máy tính, email, hoặc cổng thông tin điện tử**. |
| Đăng ký đầu mối | Phải **thông báo đầu mối (email + số điện thoại) cho Bộ Văn hóa, Thể thao và Du lịch**. |
| Thời hạn | Quy trình kép **"72 giờ và 10 ngày làm việc"** + **"24 giờ"**. Phải tạm xóa/vô hiệu hóa truy cập trong **72 giờ** (**24 giờ** với livestream). |
| Mở rộng ISP (NĐ 134) | Mở rộng để gồm *"online social networks, e-commerce platforms, and **other intermediary digital platforms**"*. Phải **chặn và xóa nội dung xâm phạm, dỡ bỏ dịch vụ/ứng dụng xâm phạm**. **Việc tuân thủ liên quan tới khả năng hưởng miễn trừ Điều 198b.** |

Nguồn: [Rouse](https://rouse.com/insights/news/2023/intermediary-service-providers-liabilities-under-the-amended-ip-law-and-decree-on-copyright), [Lexology — Notice and Takedown Process](https://www.lexology.com/library/detail.aspx?g=c0985dc4-1cfe-41c6-8050-fb169a701c58), [KENFOX — Takedown Notices](https://kenfoxlaw.com/takedown-notices-how-do-isps-handle-copyright-infringement-claims-in-vietnam), [Tilleke & Gibbins](https://www.tilleke.com/insights/new-decree-guides-vietnams-ip-law-in-relation-to-copyright-and-related-rights/2/).

⭐ **Tin TỐT, và là phát hiện hữu dụng nhất của câu 1.** Có safe harbour thật, và điều kiện hưởng nó **là việc build được**, không phải việc phải xin phép.

**Checklist đủ điều kiện Điều 198b — rẻ, làm sớm:**

1. **Công cụ tiếp nhận takedown** — có thể chỉ là form + email `copyright@`; luật cho phép "email hoặc cổng thông tin".
2. **Đăng ký đầu mối với Bộ VHTTDL** (email + điện thoại).
3. **SLA 72 giờ** — quy trình tạm xóa/vô hiệu hóa truy cập. Kỹ thuật: **soft-delete + disable-access ở cấp project**, không hard delete (còn phải giữ cho counter-notice).
4. ⚠️ **KHÔNG chủ động rà soát nội dung để "biết"** — nghịch lý safe harbour: điều kiện (a) là *"không biết"*. Xây bộ phát hiện truyện có bản quyền có thể **phá** chính miễn trừ của mình. Phản trực giác, cần luật sư xác nhận trước khi làm feature "cảnh báo truyện có thể có bản quyền".
5. **User warrant + indemnify** trong ToS.

⚠️ Không tra được: một SaaS **xử lý** nội dung (không phải hosting thuần) có được coi là "hosting service" theo NĐ 17 hay không. NĐ 17 nói rõ nghĩa vụ chỉ áp cho OSP **cung cấp dịch vụ hosting (lưu trữ nội dung số theo yêu cầu)**. comic-studio lưu novel + ảnh nên **có vẻ** thuộc, nhưng phần "xử lý/biến đổi nội dung" không có tiền lệ. → Vào danh sách hỏi luật sư.

---

### Câu 3 — Unit economics: mâu thuẫn của PM là THẬT, nhưng nguyên nhân khác giả định

#### 3.1. Pricing thật của đối thủ

**ComicInk** — credit-based, **KHÔNG có subscription** (verify từ trang pricing official):

| Pack | Giá | Credits | $/credit |
|---|---|---|---|
| Lite | **$9.99** | 1.500 | $0.00666 |
| Starter | **$24.99** | 4.500 | $0.00555 |
| Creator | **$54.99** | 12.000 | $0.00458 |
| Video | **$109.99** | 30.000 | $0.00367 |

Chi phí theo hạng mục: **Comic Pages = 50 credits**, Cover Art = 50, **Characters = 10**, World/Settings = 10, story video ~151 credits/giây. Free tier **100 credits**. Credits **không hết hạn**. Nguồn: [comicink.ai/pricing](https://www.comicink.ai/pricing).

→ **Giá thực trên user: $0.333/page (Lite) → $0.229/page (Creator).** Nhân vật $0.067/nhân vật (Lite).

**TaleAtelier** — subscription + coin pack, *"every generation burns coins"*: Starter **$9.99/mo**, Plus **$24.99/mo**, Pro **$59.99/mo**. Không công bố coin/ảnh. Tối đa **400 pages** ở tier Custom, **tối đa 6 named characters/project**. Nguồn: [taleatelier.com](https://taleatelier.com/ai-comic-generator).

**Dashtoon** — ⚠️ **không có bảng giá công khai minh bạch.** Review ghi: *"Dashtoon clearly markets free access, but the public pricing story is less transparent than a normal SaaS pricing page"*; không công bố dollar amount, credit pack, hay generation cap. Nguồn: [toolworthy.ai](https://www.toolworthy.ai/tool/dashtoon-studio). Số lưu hành (⚠️ **thứ cấp**): free tới 100 ảnh/ngày, pack từ ~$27 — [allbestapps.net](https://allbestapps.net/ai-app/dashtoon/).

**Anifusion**: Creator **$9/mo** với layered export.

⭐⭐ **COMICPAD ĐANG ĐÓNG CỬA.** Đọc trực tiếp từ [comicpad.app/pricing](https://www.comicpad.app/pricing): **"New subscriptions are paused"** + **"Comicpad is closing on September 1, 2026"**. `comicpad.app/ai-comic-generator` **301-redirect sang `taleatelier.com/ai-comic-generator`**.

⚠️ **Không xác nhận được** lý do đóng cửa, và **không xác nhận được** quan hệ Comicpad ↔ TaleAtelier (TaleAtelier không nhắc Comicpad; không có tin tức nào). Có thể rebrand / acquisition / shutdown + domain redirect. **Nhưng notice đóng cửa là primary source.** → Lấp một phần khoảng trống #6 của báo cáo trước.

#### 3.2. Giải mã mâu thuẫn: nguyên nhân là KIẾN TRÚC, không phải pricing

PM tính $8,04/chapter trên $10 → không sống được. **Con số đúng, nhưng giả định "60 ảnh/chapter" mới là chỗ cần xét lại.**

Làm ngược từ giá ComicInk **$0.333/page**, thử hai kiến trúc:

| Kiến trúc | Cost/page @1x (Gemini batch $0.067) | Cost/page @N=3 | Margin @1x | Margin @N=3 |
|---|---|---|---|---|
| **1 ảnh/panel** (4 ảnh/page) | $0.268 | $0.804 | **+20%** | **−141%** ❌ |
| **1 ảnh/page** (whole-page composition) | $0.067 | $0.201 | **+80%** | **+40%** ✅ |

⭐ **Suy ra: ComicInk gần như chắc chắn generate MỘT ảnh cho cả trang, không phải một ảnh/panel.** Không có cách nào bán $0.333/page mà chi $0.804/page. **Đây là phát hiện kiến trúc, không phải phát hiện pricing.**

Hai bằng chứng bổ trợ:

- ComicInk: *"additional characters beyond the **first five** per issue cost credits"* — khớp chính xác trần "up to 5 people" của Nano Banana Pro.
- TaleAtelier: *"up to **six** named characters per project"* — cùng bậc.

→ Cả hai đối thủ đã **hard-code trần ~5 nhân vật** vào product. Corroborate độc lập cho ràng buộc ở §1 báo cáo trước.

#### 3.3. Usage thật giải quyết phần còn lại

**User trung bình generate 42 ảnh/tháng** (từ 27 năm 2024); Midjourney ~50/tháng; 28 ảnh/session, ~23 phút/session. Nguồn: [digitalapplied.com](https://www.digitalapplied.com/blog/ai-image-generation-statistics-2026-data-points), [sqmagazine.co.uk](https://sqmagazine.co.uk/ai-image-generation-statistics/).

| Kịch bản | Cost/tháng | Margin trên $9.99 |
|---|---|---|
| 42 ảnh @1x, Gemini batch $0.067 | $2.81 | **+72%** ✅ |
| 42 ảnh @N=3 | $8.44 | **+15%** ⚠️ |
| 42 ảnh @1x, FLUX.2 pro $0.03 | $1.26 | **+87%** ✅ |
| 42 ảnh @N=3, FLUX.2 pro | $3.78 | **+62%** ✅ |
| 1 chapter/tháng (60 ảnh) @N=3, Gemini batch | $12.06 | **−21%** ❌ |
| Power user 3 chapter/tháng @N=3 | $36.18 | **−262%** ❌❌ |

→ **Subscription phẳng $10/tháng SỐNG ĐƯỢC ở usage trung bình, CHẾT ở power user.** Đó chính là lý do ComicInk chọn **thuần credit**, TaleAtelier chọn **subscription + coin (metered)**. **Không đối thủ nào dùng subscription phẳng** — không phải trùng hợp.

#### 3.4. Benchmark margin & churn ngành

| Chỉ số | Giá trị | Nguồn |
|---|---|---|
| Gross margin AI product trung bình | **52%** (ICONIQ 2026, từ **41%** năm 2024) | [saasmag.com](https://www.saasmag.com/ai-cogs-saas-gross-margin-compression/) |
| Gross margin AI (Bessemer) | **50–60%** vs **70–90%** SaaS trưởng thành | [softwareseni.com](https://www.softwareseni.com/why-ai-gross-margins-are-so-much-lower-than-saas-and-what-that-means-for-your-business/) |
| Inference chiếm % doanh thu | **23%** ở AI B2B giai đoạn scaling | saasmag |
| ⚠️ **Gross revenue retention, AI budget-tier** | **23% sau 12 tháng** — giữ chưa tới 1 trên 4 đồng | [saasultra.com](https://www.saasultra.com/saas-churn-rate-statistics-benchmarks/) |
| Median GRR AI-native SaaS | 27% (01/2025) → **40%** (09/2025) | saasultra |
| Churn tốt tham chiếu | <2%/tháng (SMB SaaS), <0.5% (enterprise) | saasultra |

⚠️ **23% GRR ở budget-tier là con số đáng lo nhất của cả delta.** Sản phẩm AI giá rẻ mất ~77% doanh thu cohort trong 12 tháng. Với 1 dev, không budget marketing, LTV thấp → **subscription tháng là mô hình sai**. Credit pack không hết hạn (đúng như ComicInk) né được: doanh thu ghi nhận trước, không có churn theo nghĩa subscription.

#### 3.5. BYOK — có thật, là trend 2026

| Dữ kiện | Nguồn |
|---|---|
| *"BYOK is quietly rewriting how AI software gets priced in 2026"*; JetBrains đã áp dụng; "hàng trăm AI productivity tool" đang chuyển sang | [buildmvpfast.com](https://www.buildmvpfast.com/blog/byok-bring-your-own-key-ai-saas-pricing-model-2026) |
| Tool truyền thống markup **300–500%**; BYOK user trả **$1–5/tháng** API thay vì **$20–249/tháng** | [copilot-alternatives.com](https://copilot-alternatives.com/blog/what-is-byok-ai-coding-tools/), [xreplyai.com](https://xreplyai.com/blog/what-is-byok) |
| BYOK cắt chi phí AI tới **80%** | [serenitiesai.com](https://serenitiesai.com/articles/bring-your-own-ai-byok-cut-costs-2026) |
| **OpenRouter** thu BYOK fee = **5%** chi phí tương đương, miễn 1tr request đầu/tháng | buildmvpfast |
| ⚠️ BYOK cho **non-technical buyer** vẫn hiếm | [dmchamp.com](https://dmchamp.com/best/best-ai-tools-byok-2026/) |

#### 3.6. Khuyến nghị pricing cho 1 dev

**Không dùng subscription phẳng. Dùng hybrid: flat platform fee thấp + BYOK (hoặc credit metered).**

| Thành phần | Đề xuất | Căn cứ |
|---|---|---|
| **Platform fee** | $5–15/tháng cho phần **không đốt inference**: Story Bible editor, Comic IR, layout editor, versioning, export | Phần này có margin SaaS thật (~90%), không bị AI COGS compression |
| **Image generation** | ⭐ **BYOK là lựa chọn đề xuất** — user cắm Gemini/BFL API key của họ | Xóa hoàn toàn rủi ro unit economics; power user không làm mình lỗ; trend 2026 đã xác lập; 1 dev không kham được rủi ro COGS |
| Phương án thay thế | Credit pack **không hết hạn**, ~$0.30–0.35/page (bám ComicInk $0.333) | Có tiền lệ giá; doanh thu ghi trước → né 23% GRR |
| **Tuyệt đối tránh** | Subscription phẳng unlimited, hoặc free tier "100 ảnh/ngày" | 60 ảnh @N=3 = $12.06 > $9.99. Một power user xóa margin của 4 user thường |
| Ràng buộc product | Hard-code trần ~5 nhân vật/project | ComicInk (5) và TaleAtelier (6) đã làm; khớp trần model |
| Kỳ vọng margin | **50–60%**, không phải 80% | ICONIQ 52%, Bessemer 50-60% |

⚠️ **Điểm yếu của BYOK phải nói thẳng**: friction cao với non-technical user — đúng phân khúc đã xác định ở §3.4 báo cáo trước (tác giả web novel). Nguồn ngành xác nhận BYOK cho non-technical buyer vẫn là ngoại lệ. → Nếu chọn BYOK, **onboarding flow là rủi ro sản phẩm số 1**, không phải feature phụ.

---

### Câu 2 — Nghĩa vụ nền tảng: thực tiễn ngành

#### 2.1. Đối thủ đặt điều khoản thế nào

| Nền tảng | Điều khoản tra được |
|---|---|
| **ComicInk** | User phải **indemnify, defend, hold harmless** ComicInk và officer/director/employee/agent. **Assign toàn bộ quyền cho user**, nhưng ghi rõ disclaimer: *"the legal status of AI-generated content may vary by jurisdiction"* |
| **myComics.ai** | User **acknowledge** nội dung generated + tài liệu upload là **trách nhiệm riêng của họ**, **assume full liability** cho mọi claim/damage/dispute từ việc tạo, dùng, xuất bản, chia sẻ. Có indemnify Filli S.r.l. |
| **ComicAI** | Phản hồi notice xâm phạm **theo DMCA** |
| **livecomics.to** | Có **DMCA designated agent đăng ký với US Copyright Office**; user giữ ownership mọi thứ upload |

Nguồn: [comicink.ai/terms](https://www.comicink.ai/terms), [mycomics.ai/terms](https://mycomics.ai/terms/), [comicai.com/terms-of-service](https://comicai.com/terms-of-service), [livecomics.to/terms](https://livecomics.to/terms), [tabstory.net so sánh copyright](https://www.tabstory.net/blog/ai-comic-generator-copyright-comparison-20260517).

**Ba pattern nhất quán, nên copy:**

1. **User warrant + indemnify** — phòng tuyến hợp đồng số 1, mọi đối thủ đều có.
2. **Assign toàn bộ quyền output cho user** + disclaimer bất định pháp lý theo jurisdiction (ComicInk làm chính xác thế — vừa hào phóng vừa tự bảo vệ).
3. **DMCA designated agent** đăng ký với US Copyright Office, nếu nhắm thị trường Mỹ.

#### 2.2. DMCA safe harbour có áp cho loại xử lý này? — GAP

Tra được có phân tích *"DMCA Compliance in the Age of AI-Generated Content"* ([patentpc.com](https://patentpc.com/blog/dmca-compliance-in-the-age-of-ai-generated-content-what-platforms-need-to-know)), và các nền tảng AI comic **đang tự xử sự như thể DMCA §512 áp dụng**. Nhưng **không tìm được** phân tích trả lời trực tiếp: §512(c) vốn dành cho *"storage at the direction of a user"* — **có phủ cả việc nền tảng chủ động chạy LLM xử lý/biến đổi nội dung không?** Cùng cấu trúc câu hỏi như 1.4 với Điều 198b: **hosting thuần có safe harbour rõ; "hosting + processing" là vùng chưa test.**

#### 2.3. Vụ kiện nhắm vào NỀN TẢNG?

⚠️ **Không tìm được tiền lệ hoặc vụ kiện nào nhắm riêng vào nền tảng AI vì xử lý nội dung có bản quyền do user upload.** Không suy đoán. Có thể do (a) chưa có vụ nào, hoặc (b) ngách quá nhỏ. Không đủ dữ liệu để phân biệt. Bằng chứng gián tiếp duy nhất về intermediary liability ở VN: vụ **Tri Viet v. Lazada** ([LinkedIn analysis](https://www.linkedin.com/pulse/liability-intermediaries-telecommunication-networks-via-ha-nguyen)) — nhưng là e-commerce, không phải AI processing, không dùng làm tiền lệ trực tiếp.

---

### Câu 4 — Tỉ lệ regenerate: LẦN NÀY TRA RA, và xấu hơn giả định của PM

**CANVAS dùng N = 3 candidate/shot.** Nguyên văn: *"Performance saturates at N=3, providing the best balance between quality and computation."*

Ablation (Table 4 + Figure 6):

- **N=1**: baseline, thấp nhất mọi metric
- **N=2**: cải thiện vừa phải về character consistency
- **N=3**: tối ưu, diminishing returns từ đây
- **N>3**: *"Increasing the number of generated variants mainly improves character consistency... Performance saturates at N=3"*; background và prop *"largely stable due to memory constraints"*

Nguồn: [arXiv 2604.13452v1](https://arxiv.org/html/2604.13452v1).

**Ý nghĩa — con số PM cần, và nó là 3x không phải 2x:**

1. **N=3 là setting để ĐẠT con số 4.91/5** ở §1 báo cáo trước. Không phải "regen khi lỗi" — mà là **generate 3 candidate mỗi panel rồi để VLM chọn 1, mặc định, mọi panel**. Kiến trúc **best-of-N**, không phải retry-on-failure.
2. → **Hệ số nhân đúng cho unit economics là 3x.** Mọi con số ở §5 báo cáo trước phải đọc ở cột 3x: **$12,06/chapter** (Gemini batch), **~$1.206 cho 100 chapter**. Margin ở §3.3 delta phải đọc ở dòng N=3.
3. Cộng thêm chi phí VLM call để score 3 candidate — **không tính được**, không biết token cost của prompt QA của CANVAS.
4. **Tin tốt: 3 là TRẦN, không phải sàn.** Paper nói rõ saturate ở 3 → không cần N=5 hay N=10. Hữu hạn, biết trước, budget được.
5. ⚠️ Paper **không** báo first-pass acceptance rate. QA-selection chọn candidate điểm cao nhất trong 3 → **luôn có output**, nhưng không có số nói output đó có cần human reject hay không. **Tỉ lệ human-reject sau VLM-select: vẫn không tìm được.**

**Khuyến nghị MVP0** — chỉ số cần tự đo không còn là "regen rate" chung mà là hai chỉ số tách biệt:

- **N tối thiểu để VLM-select ra panel đạt** (CANVAS nói 3; tự verify xem 2 có đủ với style của anh — mỗi bậc N giảm ~33% COGS).
- **Human-reject rate sau VLM-select** — chưa ai công bố, và nó quyết định liệu Continuity Checker có thực sự cắt được công human review hay chỉ thêm một lớp chi phí.

Chi phí spike đo hai chỉ số: 30 panel × 3 candidate × $0.134 ≈ **$12**.

---

### Tổng hợp delta — 4 điều chỉnh cho verdict

1. ⚖️ **Câu 1 không có đáp án dứt khoát — cần luật sư SHTT VN.** Nhưng phần tra ra được thì tốt: Điều 198b có safe harbour thật, điều kiện là **không biết + xóa kịp thời trong 72h**, và NĐ 134 đã mở rộng ISP gồm *"other intermediary digital platforms"*. → Có đường đi, và checklist đủ điều kiện là việc build được (§1.4).
2. ⚠️ **Nghĩa vụ pháp lý MỚI: Luật Trí tuệ nhân tạo 2025 (Luật 134/2025/QH15), hiệu lực 01/03/2026.** SaaS đặt tại VN là "nhà cung cấp/nhà triển khai" → nghĩa vụ minh bạch (Điều 11), đánh dấu nội dung AI định dạng máy đọc, đăng ký/báo cáo (Điều 8), deadline **~01/03/2027**. Điều 7 cấm *"thu thập dữ liệu trái pháp luật để huấn luyện AI"* và *"che giấu thông tin minh bạch bắt buộc"*. → **AI-labeling không còn là chuyện riêng của Hàn Quốc — nó là nghĩa vụ nội địa Việt Nam.**
3. 💰 **Mâu thuẫn unit economics là THẬT và tệ hơn tính ban đầu, vì hệ số đúng là 3x (CANVAS N=3).** Nhưng nguyên nhân gốc là **kiến trúc, không phải pricing**: reverse-engineer giá ComicInk cho thấy họ generate **1 ảnh/TRANG**, không phải 1 ảnh/panel. Cộng usage thật (**42 ảnh/tháng**) thì $10/tháng sống được ở user thường nhưng chết ở power user. **Không đối thủ nào dùng subscription phẳng.** Khuyến nghị: **flat platform fee thấp + BYOK**, hoặc credit pack không hết hạn ~$0.30/page. Margin kỳ vọng **50–60%**. Và **23% GRR ở AI budget-tier** nghĩa là subscription tháng là mô hình sai cho 1 dev không budget marketing.
4. 🪦 **Đã tìm được một shutdown được xác nhận — lấp khoảng trống #6.** **COMICPAD: "New subscriptions are paused" + "Comicpad is closing on September 1, 2026"**, đọc trực tiếp từ comicpad.app/pricing; domain 301-redirect sang taleatelier.com. Lý do và quan hệ với TaleAtelier: không xác nhận được. Nhưng một AI comic generator có nội dung marketing cập nhật tới 7/2026 mà đóng cửa 9/2026 là dữ liệu đáng cân nhắc — ủng hộ nhánh "dấu hiệu xấu" đã nêu ở §2.3.

**Verdict vẫn "KHẢ THI CÓ ĐIỀU KIỆN", nhưng số điều kiện tăng từ 4 lên 7:** (1) ≤3 nhân vật/panel; (2) chữ qua typeset layer; (3) IP tự sở hữu → thay bằng **user warrant + indemnify + safe harbour Điều 198b (tool takedown, đầu mối Bộ VHTTDL, SLA 72h)**; (4) AI disclosure — **giờ là nghĩa vụ VN, không chỉ Hàn Quốc**; (5) **pricing metered/BYOK, không subscription phẳng**; (6) **tư vấn luật sư SHTT về Điều 37a và khoản 4 Điều 11 TRƯỚC khi thương mại hóa**; (7) budget COGS ở hệ số **3x**, không 2x.

### Khoảng trống KHÔNG lấp được (delta)

1. **Nguyên văn Điều 37a/37b/37c NĐ 134/2026** — cov.gov.vn chỉ có bản giới thiệu; thuvienphapluat.vn và nhansu.vn **403**; IAPP **paywall**.
2. **Nguyên văn khoản 4 Điều 11 Luật TTNT 2025** — hai nguồn mô tả phạm vi **khác nhau**.
3. **DMCA §512(c) có phủ "hosting + AI processing"** — không tìm được phân tích trực tiếp.
4. **Điều 198b có áp cho SaaS xử lý nội dung** (không phải hosting thuần) — NĐ 17 chỉ nói rõ về "dịch vụ hosting".
5. **Tiền lệ/vụ kiện nhắm vào nền tảng AI** vì user-uploaded copyrighted content — không tìm được.
6. **Dashtoon pricing chính thức** — họ cố ý không công bố. Số lưu hành là thứ cấp.
7. **Lý do Comicpad đóng cửa + quan hệ với TaleAtelier** — notice là primary source, nguyên nhân thì không.
8. **Human-reject rate sau VLM-select** — CANVAS không báo. Phải tự đo.
9. **Coin/credit cụ thể mỗi ảnh của TaleAtelier** — không công bố.
10. **Gross margin công bố của một AI image SaaS cụ thể** — chỉ có benchmark ngành.

---

## PM đọc được gì

1. **Luật TTNT 2025 là thứ PM không thể tự biết** (hiệu lực 01/03/2026, sau knowledge cutoff). Nó **nâng cấp** rủi ro compliance từ "chuyện của thị trường Hàn Quốc" thành **nghĩa vụ nội địa Việt Nam có deadline cụ thể (~01/03/2027)**. Đây là lần thứ hai trong run mà lens có web access đảo một kết luận — lần đầu là NĐ 134/2026 với `parent_generation`.
2. **Con số N=3 sửa phép tính của chính PM.** PM dùng 2x làm hệ số regen ở `escalations.md`. Con số đúng là **3x**, và nó không phải "regen khi lỗi" mà là **best-of-N mặc định mọi panel** — đó là setting để đạt 4.91/5. Mọi số trong `escalations.md` mục *Phân tích bổ sung của PM* phải đọc lại ở cột 3x: **$12,06/chapter**, không $8,04. **PM đã tính thiếu 50%.**
3. **Phát hiện "ComicInk generate 1 ảnh/TRANG" là phát hiện kiến trúc quan trọng nhất của delta**, và nó đến từ một lens nghiên cứu chứ không phải lens kiến trúc — vì nó được suy ra từ *giá*, không từ *thiết kế*. Xem mục *Mâu thuẫn* M13 bên dưới: nó xung đột trực tiếp với tính năng cốt lõi của §14.
4. **Safe harbour Điều 198b là tin tốt nhất của delta.** Rủi ro pháp lý ở nhánh "user tự upload" chuyển từ *nhị phân không kiểm soát được* sang *có checklist build được*. Bốn hạng mục (tool takedown, đầu mối Bộ VHTTDL, SLA 72h soft-delete, ToS warrant+indemnify) đều rẻ và đều thuộc MVP.
5. **Nghịch lý safe harbour ở §1.4 điểm 4 là điểm phản trực giác nhất của cả run**: điều kiện miễn trừ là *"không biết"*, nên **xây bộ phát hiện truyện có bản quyền có thể phá chính miễn trừ của mình**. Đây là loại kết luận mà nếu không có lens pháp lý thì một dev sẽ làm ngược — vì "chủ động kiểm tra" nghe như hành vi có trách nhiệm.
6. **Comicpad đóng cửa 01/09/2026** — tám ngày sau hôm nay. Đây là dữ liệu thị trường lạnh nhất mà run này tìm được, và nó ủng hộ nhánh phản biện chứ không phải nhánh lạc quan.
7. **23% GRR ở AI budget-tier** kết hợp với "1 dev, không budget marketing" là lập luận mạnh nhất cho **credit pack không hết hạn** thay vì subscription. Doanh thu ghi nhận trước thì churn không còn là churn.

## Mâu thuẫn với lens khác

| # | Mâu thuẫn | PM phân xử |
|---|---|---|
| **M13** ⭐⭐ | **Mâu thuẫn quan trọng nhất của cả run.** `researcher` suy ra đối thủ generate **1 ảnh/TRANG** vì đó là cách duy nhất có margin dương ($0.201/page @N=3, +40%) — trong khi **1 ảnh/panel là −141%**. Nhưng `Request.md` §14 xây toàn bộ trải nghiệm quanh việc **regenerate một panel mà "không ảnh hưởng các panel khác"**, và §6 định nghĩa panel là đơn vị spec. | **Đây là xung đột thật giữa tính năng cốt lõi và unit economics, không phải lỗi của bên nào.** Phân xử: <br><br>**Tính năng làm sản phẩm hay chính là tính năng làm margin âm.** Per-panel generation cho phép sửa cục bộ — giá trị lớn nhất của §14 — và đồng thời nhân COGS lên gấp 4 (4 panel/page thay vì 1 ảnh/page). Không thể có cả hai ở cùng một mức giá. <br><br>**Ba đường ra, PM xếp theo mức khuyến nghị:** <br>1. ⭐ **BYOK** — xung đột **biến mất hoàn toàn**, vì COGS không còn là của anh. Đây là lập luận thứ hai, độc lập, ủng hộ BYOK; cộng với lập luận 23% GRR ở §3.4 thì BYOK có ba căn cứ riêng biệt. <br>2. **Whole-page mặc định + per-panel là hành động trả phí.** Người dùng thấy giá trị khi *cần* sửa, và trả đúng lúc đó. Khớp mô hình credit của ComicInk. <br>3. Whole-page thuần — **rẻ nhất nhưng bỏ mất §14**, tức là bỏ mất lý do sản phẩm tồn tại. Không khuyến nghị. <br><br>**Hệ quả cho kiến trúc**: `Panel Specification` (§6) **vẫn giữ nguyên giá trị** — nó là spec, không bắt buộc mỗi panel một lần gọi model. Một page có thể compile nhiều panel spec thành **một** prompt whole-page. Điều này **củng cố** kết luận cuối `Request.md` ("spec là dữ liệu chính, ảnh chỉ là output/cache"): chính vì spec tách khỏi ảnh mà mình mới đổi được granularity render mà không đổi data model. **Đây là lần thứ hai quyết định kiến trúc đó tự chứng minh giá trị** — lần đầu là ranh giới bản quyền Zarya. |
| **M14** | `architect` (B4) tính two-pass "draft rẻ rồi final đắt" chỉ tiết kiệm 5%, và **lỗ** nếu final regen ≥1,2x; hoà vốn tại 1,1x. Nó nêu câu cần xác nhận: **giá có tính theo resolution không?** | **PM trả lời được từ dữ liệu `researcher` đã có: CÓ, nhưng không giúp.** Gemini 3 Pro Image tính **$0.134 cho CẢ 1K và 2K** (cùng giá), chỉ 4K mới đắt hơn ($0.24) → **hạ resolution không làm draft rẻ hơn trên Pro**. Draft rẻ nhất là Gemini Flash batch $0.034 hoặc FLUX.2 klein $0.014/MP. <br><br>**Nhưng phát hiện N=3 làm câu hỏi này trở nên không liên quan, và đó mới là điều đáng nói.** N=3 **không phải** retry-on-failure mà `architect` đang mô hình hoá — nó là **best-of-N để ĐẠT consistency**. Một draft pass ở model khác **không thể thay thế** nó, vì draft trả lời câu *"composition có đúng không"* còn N=3 trả lời câu *"candidate nào giữ được identity"*. Hai câu khác nhau; pass phụ không hấp thụ được pass chính. <br><br>→ **Kết luận của `architect` ("giải bằng metering, không bằng pipeline") ĐÚNG, và đúng vì một lý do mạnh hơn lý do nó nêu.** Lý do nó nêu là *tỉ lệ giá quá hẹp*; lý do thật là *hai pass không thay thế được nhau về mặt chức năng*. Deliverable phải nêu lý do thật. |
| **M15** | `researcher` (báo cáo trước) khuyến nghị Gemini 3 Pro Image batch làm main path. `architect` (B2/B4) nhấn mạnh hard quota + cost attribution + credit ledger. | **Bổ sung cho nhau, và hợp thành một khuyến nghị duy nhất.** Với N=3 là mặc định, mỗi panel = 3 lần gọi model ⇒ **quota phải tính theo `candidate`, không theo `panel`**. Đây là chi tiết thiết kế cụ thể mà chỉ hiện ra khi ghép hai lens: `architect` biết cần hold-trước-khi-enqueue nhưng không biết N=3; `researcher` biết N=3 nhưng không thiết kế ledger. **Hold phải reserve 3 credit/panel, không 1.** |
| **M16** | Lens PM (báo cáo gốc, mục 3) xếp rủi ro pháp lý là **rủi ro nhị phân số 1**. | **Vẫn đúng, nhưng đã tách thành hai nửa có tính chất khác nhau.** Nửa *"user có quyền với truyện không"* → **hạ cấp**, vì Điều 198b cho safe harbour và checklist là việc build được. Nửa *"extraction thương mại có hợp pháp không"* (Điều 37a) → **giữ nguyên mức nhị phân**, vì không ai tra ra được và nó quyết định tính hợp pháp của chính hoạt động lõi. → Deliverable phải trình bày hai nửa riêng, không gộp: một nửa có đường đi, một nửa chặn ở cửa luật sư. |
