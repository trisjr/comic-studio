# Doc Plan: 2026-08-23-khoi-tao-tai-lieu-planning-comic-studio

> **File này do PM độc quyền chỉnh sửa.** Writer báo xong trong `SUMMARY`; PM đối chiếu `FILES_TOUCHED` rồi mới tick cột *Xong*.

## Hạng mục

| # | Tài liệu | Loại (RULE-001) | Đích | Khuôn | `status` đích | Writer | Xong |
|---|----------|-----------------|------|-------|---------------|--------|------|
| 1 | Project Charter | `charter` | `docs/010-Planning/Charter-Comic-Studio.md` | `Template-Project-Charter.md` **+ RACI tự định nghĩa** | `draft` | `business-analyst` #1 | [x] ✅ 300 dòng, 11 H2, RACI 9×5, 0 wiki-link, `FILES_TOUCHED` khớp ownership |
| 2 | Product Roadmap | `roadmap` | `docs/010-Planning/Roadmap.md` ⚠️ **SỬA stub** | không có khuôn → outline này | `draft` | `architect` | [x] ✅ 369 dòng, frontmatter **giữ đúng** `id: ROADMAP-001` + `created: 2026-02-04`, thêm `updated`; CF-8.13 trả lời **KHÔNG**; 0 wiki-link |
| 3 | OKRs | `okrs` | `docs/010-Planning/OKRs.md` ⚠️ **SỬA stub** | không có khuôn → outline này | `draft` | `product-owner` | [x] ✅ 267 dòng, frontmatter **giữ đúng** `id: OKRS-001` + `created: 2026-02-04`; Q4 4 Obj/13 KR, Q1 3 Obj/8 KR, 8 anti-goal, 0 wiki-link |
| 4 | Risk Register | `risk-register` | `docs/010-Planning/Risk-Register.md` | `Template-Risk-Register.md` **+ 4 cột bổ sung + công thức Score** | `draft` | `security-auditor` | [x] ✅ 224 dòng, **23 rủi ro** (vượt trần ≥16) + 10 khoảng trống không Score + RP-01 + RB-01, 5 mục đủ, 0 wiki-link |
| 5 | MVP Scope | `mvp-scope` | `docs/010-Planning/MVP-Scope.md` | không có khuôn → outline này | `draft` | `architect` | [x] ✅ 500 dòng, 3 gate G0/G1/G2 có ngưỡng đo được, 0 wiki-link |
| 6 | Cấu trúc Dewey + Index | `index` | 32 thư mục + `docs/000-Index.md` | RULE-001 §Cấu trúc bắt buộc | `live` | **PM** | [x] ✅ 32 dir + 32 `.gitkeep`, `find` khớp 100% RULE-001; `000-Index.md` đã tạo |
| 7 | Research Notes | `research` | `docs/050-Research/Analysis-Market-Competitor-Landscape.md` | `Template-Analysis.md` là stub → outline này | `draft` | `business-analyst` #2 | [x] ⚠️ **Writer soạn, PM ghi file** — `Write` của subagent bị guardrail chặn theo mẫu tên `Analysis-*`. 41 URL, 23 khoảng trống / 5 nhóm, 0 wiki-link. Xem `brief.md` §*Kết luận cuối về guardrail* |

---

# 🔒 BẢNG CANONICAL FACTS — nguồn sự thật chung của cả 5 tài liệu

> [!IMPORTANT]
> **Đây là phần quan trọng nhất của outline.** Năm tài liệu Planning được viết **song song bởi bốn writer khác nhau**. Nếu mỗi writer tự suy ra số của mình, kho tài liệu sẽ mâu thuẫn với chính nó — và đó là failure mode mà chính việc song song hoá sinh ra.
>
> **Quy tắc cứng cho mọi writer:**
> 1. Mọi con số dùng chung **phải copy từ bảng này**, không tự tra lại, không tự tính lại.
> 2. **Copy cả số VÀ nhãn của nó như một cặp không tách rời.** Một con số `[EM]` mà mất nhãn khi sang tài liệu là lỗi nghiêm trọng — đó chính xác là failure mode E2 của run trước: *"khi input đã được đánh dấu là khoảng trống, output tính từ nó phải mang cùng cảnh báo; nếu không, khoảng trống bị **rửa sạch** qua một phép nhân."*
> 3. **Cấm nhân/chia hai số trong bảng này để tạo ra số thứ ba** mà không gắn nhãn `[EM]` cho kết quả.
> 4. Cần một con số **không có** trong bảng → ghi `TBD` và báo `PARTIAL`. **Không bịa.**

**Quy ước nhãn**: `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` thứ cấp · `[EM]` ước lượng/phép nhân, **không phải số đo** · `[CHỐT]` quyết định của anh tại gate

## CF-1 — Bối cảnh sản phẩm (bất biến, không writer nào được diễn giải khác)

| # | Sự thật | Giá trị | Nhãn |
|---|---|---|---|
| 1.1 | Bản chất sản phẩm | **SaaS thương mại multi-tenant** — nền tảng cho **người khác tự upload truyện của họ** | `[CHỐT]` gate run trước |
| 1.2 | Quy mô đội | **1 người (anh) + AI assist**. Không funding, không ngân sách marketing | `[CHỐT]` |
| 1.3 | Trạng thái code | **Chưa có dòng nào** — `src/`, `test/`, `openspec/changes/` đều rỗng | `[OFF]` đo bằng `find` |
| 1.4 | Rủi ro IP đầu vào | Chuyển sang **người upload**; nền tảng phát sinh nghĩa vụ safe harbour + TDM thương mại | `[CHỐT]` |
| 1.5 | Phân khúc mục tiêu | **Tác giả truyện chữ (writer) KHÔNG biết vẽ** — *không* nhắm hoạ sĩ | `[CHỐT]` + củng cố bởi CF-5.6 |

## CF-2 — Mô hình kinh doanh (chốt tại gate run này)

| # | Sự thật | Giá trị | Nhãn |
|---|---|---|---|
| 2.1 | **Cấu hình đã chốt** | **3 tầng kiểu Novelcrafter** | `[CHỐT]` gate 2026-08-23 |
| 2.2 | Tầng 1 — cửa vào | **$4–8/tháng, KHÔNG có image gen.** Story Bible editor + Comic IR + layout + versioning + export. Margin ~90%, **không cần API key** | `[CHỐT]` |
| 2.3 | Tầng 2 — user thường | **Credit pack không hết hạn**, managed inference. Dành cho user **<125 ảnh/tháng** | `[CHỐT]` |
| 2.4 | Tầng 3 — power user | **BYOK là tùy chọn MỞ KHÓA**, không phải điều kiện để dùng sản phẩm | `[CHỐT]` |
| 2.5 | **Ngưỡng phân tuyến** | **~125 ảnh/tháng** — dưới ngưỡng credit thắng, trên ngưỡng BYOK thắng | `[TC]` vendor blog kompozy.io ⚠️ bên bán managed, nhưng khuyến nghị **ngược chiều lợi ích của họ** ⇒ chấp nhận được |
| 2.6 | Comp chuẩn | **Novelcrafter**: 220.000+ authors, tier $4 (không AI) / $8 / $14 / $20, **không bao giờ bán inference** | `[OFF]` novelcrafter.com/pricing |
| 2.7 | ⛔ Tuyệt đối tránh | Subscription phẳng unlimited; free tier kiểu "100 ảnh/ngày" | `[OFF]` suy từ CF-3.5 |

## CF-3 — Kinh tế đơn vị

| # | Sự thật | Giá trị | Nhãn |
|---|---|---|---|
| 3.1 | Hệ số generate | **N = 3 (best-of-N, mặc định cho MỌI panel)** — *"Performance saturates at N=3"* | `[OFF]` [arXiv 2604.13452](https://arxiv.org/html/2604.13452v1) |
| 3.2 | ⚠️ Bản chất N=3 | **KHÔNG phải retry-on-failure.** Là generate 3 candidate cho mọi panel rồi VLM chọn 1. Không thể lấy chất lượng của N=3 mà tính chi phí của N=2 | `[OFF]` |
| 3.3 | Ảnh / chapter | **60** (15 page × 4 panel) | ⚠️ `[EM]` **giả định của `researcher` run trước, KHÔNG phải số đo** |
| 3.4 | Giá ảnh | Gemini 3 Pro Image: **$0.134** standard / **$0.067** batch · FLUX.2 pro: **$0.03** | `[OFF]` |
| 3.5 | **Chi phí/chapter @N=3, Gemini batch** | **$12,06** | `[EM tính từ OFF]` ⚠️ **là SÀN, không phải trần** — chưa tính VLM call để score 3 candidate |
| 3.6 | Margin trên $9.99, 1 chapter/tháng @N=3 | **−21%** | `[EM]` |
| 3.7 | Margin power user 3 chapter/tháng @N=3 | **−262%** | `[EM]` |
| 3.8 | Usage trung bình ngành | **42 ảnh/tháng** (tăng từ 27 năm 2024) | `[TC]` |
| 3.9 | 1 chapter @N=3 | **180 ảnh** — vượt ngưỡng 125 ngay ở chapter đầu tiên | `[EM]` 60 × 3 |
| 3.10 | Kỳ vọng gross margin | **50–60%**, không phải 80% | `[BCN]` ICONIQ 52%, Bessemer 50–60% |
| 3.11 | Chi phí MVP0 | **~$12** ở giá standard $0.134 · **~$6** nếu batch. Lấy **số cao làm trần an toàn** vì cần vòng lặp nhanh nên batch khó dùng | `[EM tính từ OFF]` |

## CF-4 — Thị trường

| # | Sự thật | Giá trị | Nhãn |
|---|---|---|---|
| 4.1 | ⛔ **TAM webtoon** | $14,0–18,3B (2026), CAGR 26,3–33,1% | `[BCN]` 7 firm phân kỳ · ⚠️ **CẤM dùng làm căn cứ biện minh dự án** — nó đo **tiêu thụ nội dung**, comic-studio không lấy tiền từ độc giả |
| 4.2 | Bằng chứng TAM không dùng được | Đổi nhãn sang "digital comics"/"webcomics" ⇒ CAGR sụp còn **6,7–10,4%**, chênh 4–5 lần. Và WEBTOON — platform số 1 — chỉ làm **~$1,4–1,5B/năm** `[EM từ OFF]`, tức 8–10% của TAM nó thống trị | `[BCN]` + `[EM]` |
| 4.3 | **SAM** (công cụ cho tác giả) | **$0,4M – $9M ARR** | ⚠️ `[EM]` **3/4 thừa số là giả định. Không firm nào bán con số này.** |
| 4.4 | **SOM năm 1** | **$4K – $14K ARR** ≈ **$300–1.200 MRR**, 30–80 paying user | ⚠️ `[EM]` neo vào CF-4.5 |
| 4.5 | **Neo thực tế** | **Anifusion**: solo founder, **$833 MRR**, có lãi, **~2 năm** kể từ launch 2024, **$0 marketing spend** | `[TC]` ⚠️ **mâu thuẫn**: nguồn khác ghi $5.000/tháng; và giá $9/mo (run trước) vs €20/mo (delta). **Ghi cả hai, không chọn một.** |
| 4.6 | Retention band của comic-studio | **GRR 23% / NRR 32%** cho AI-native `<$50/tháng` | `[OFF]` ChartMogul, ~3.500 công ty · **BA CAVEAT BẮT BUỘC** — xem CF-4.7 |
| 4.7 | ⚠️ **Ba caveat của 23%** | (a) cohort AI-native chỉ **~200 công ty**, n của riêng band này **không công bố**; (b) lọc **≥$250K ARR** ⇒ **loại đúng nhóm indie mà comic-studio thuộc về**; (c) dữ liệu **2025**, không phải 2026 | `[OFF]` |
| 4.8 | Xác nhận độc lập cùng chiều | RevenueCat 10/03/2026: AI app retention 12 tháng **21,1%** vs non-AI **30,7%**; ~115.000 app | `[TC]` ⚠️ **KHÔNG gộp với 4.6** — GRR ≠ payer retention, hai metric khác nhau |
| 4.9 | ⚠️ Luận điểm chưa có bằng chứng | *"Credit pack không hết hạn né được 23% GRR"* — **là lập luận logic (doanh thu ghi trước), KHÔNG phải số đo.** Không tìm được dữ liệu retention nào cho mô hình credit pack | `[EM]` |

## CF-5 — Đối thủ & rủi ro cạnh tranh

| # | Sự thật | Giá trị | Nhãn |
|---|---|---|---|
| 5.1 | **Dashtoon** | **$20,1M / 3 vòng**, **465 nhân viên (31/05/2026)** ⇒ là **content studio dùng AI**, KHÔNG phải đối thủ tool. **Không dùng giá Dashtoon làm neo pricing** | `[TC]` Tracxn |
| 5.2 | ⭐ **GlobalComix** — đe doạ chiến lược | **$13M (25/03/2026)**, lead SBI US Gateway Fund + Point72. **Mua lại INKR** → đem về **typesetting, text detection, image cleaning**; ex-INKR CEO làm head of AI engineering. Định vị **"the Figma for comics"** | `[TC]` Publishers Weekly |
| 5.3 | Vì sao 5.2 nguy hiểm | Typesetting là đúng phần run trước kết luận comic-studio **"phải tự build"** (Comical-JS chưa có auto-placement). Và "Figma for comics" trùng định vị §14 `Request.md` | phân tích PM |
| 5.4 | ⭐ **Constella (WEBTOON)** — rủi ro **nền tảng** | Convert 3D character model → 2D theo **đúng nét vẽ của chính creator**, miễn phí cho creator của platform. Rollout professional trước | `[TC]` ⚠️ fetch nguồn fail, **chưa xác nhận đã ship hay còn là announcement** |
| 5.5 | Vì sao 5.4 khác loại | Nếu platform lớn nhất phát công cụ consistency **miễn phí**, kênh phân phối tự nhiên nhất bị chặn ở cửa. **Nhưng** Constella nhắm creator **đã biết vẽ**; comic-studio nhắm tác giả **không biết vẽ**. Hai phân khúc — khoảng cách **có thể** hẹp lại | phân tích PM |
| 5.6 | ⚠️ **Cộng đồng là kênh CÓ RỦI RO NGƯỢC** | Naver Webtoon bị **độc giả boycott subscription** khi đăng tác phẩm AI; **BlueLine Studio bị buộc vẽ lại** episode sau khi fan phát hiện background AI-polish | `[TC]` run trước |
| 5.7 | Hệ quả của 5.6 | Kênh cộng đồng chỉ chạy được với **positioning disclosure-first**, nhắm **writer** không nhắm **artist**. Bằng chứng: Novelcrafter 220K authors (cộng đồng viết chấp nhận) vs boycott (cộng đồng vẽ) | phân tích PM |
| 5.8 | ❌ Kênh đã chết | **Show HN**: ComicInk 30/04/2026 được **2 điểm / 2 comment** | `[OFF]` HN API |
| 5.9 | ⭐ Kênh thống trị ngách | **Comparison-listicle SEO** — 8/8 đối thủ đều tự xuất bản trang so sánh | ⚠️ `[EM]` **quan sát SERP, không phải số traffic đo được** |
| 5.10 | Kênh có quy mô đo được | Discord WEBTOON official **17.777 members**; Novelcrafter Discord **9.825** | `[TC]` |

## CF-6 — Khả thi kỹ thuật

| # | Sự thật | Giá trị | Nhãn |
|---|---|---|---|
| 6.1 | **Verdict tổng** | **KHẢ THI CÓ ĐIỀU KIỆN — CHÍN điều kiện phải thoả ĐỒNG THỜI** (7 từ `researcher` + 2 từ `architect`/`senior-ai-engineer`) | run trước §4.1 |
| 6.2 | Điểm mạnh đã được validate | CANVAS: **character 4.91/5**, human win-rate **86,7%**, background **4.88/5** | `[OFF]` [arXiv 2604.13452](https://arxiv.org/html/2604.13452v1) |
| 6.3 | Điểm yếu nhất | **Props chỉ 4.19/5** — thấp nhất trong 4 metric, cải thiện so baseline chỉ **+2,5%** | `[OFF]` |
| 6.4 | ⚠️ **Hàng load-bearing** | **Multi-character panel 2–3 nhân vật** — 🟡 giải được một phần. **KHÔNG benchmark độc lập nào đo frontier model ở mức này** ⇒ MVP0 phải tự đo | `[OFF]` |
| 6.5 | Trần nhân vật | CogCanvas ID-Sim: **42.33** (2 người) → **27.21** (3) → **2.67** (4) → **0.52** (5). *"near-complete failure beyond three subjects"* | `[OFF]` [arXiv 2606.15867](https://arxiv.org/html/2606.15867) |
| 6.6 | Corroborate từ thị trường | ComicInk hard-code trần **5 nhân vật**/issue; TaleAtelier **6 named characters**/project | `[TC]` |
| 6.7 | Effort editor tối thiểu | **~20–25%** (mẫu số **SaaS**, đã gồm multi-tenancy) | `[EM]` `architect` |
| 6.8 | ⚠️ Effort §14 đầy đủ | **50–60%** (mẫu số **công cụ cá nhân**, không gồm multi-tenancy/billing/auth) | `[EM]` ⚠️ **HAI MẪU SỐ KHÁC NHAU — CẤM TRỪ 6.8 CHO 6.7** |
| 6.9 | Effort multi-tenancy | **15–25%** — `Request.md` không nhắc một dòng | `[EM]` `architect` |
| 6.10 | Speaker attribution | Lỗi **30–50%** (3+ người) / **40–60%** (câu ngắn) | ⚠️ `[EM]` **ước lượng, KHÔNG phải số đo** |
| 6.11 | Độ phủ Continuity Checker | **40–60% số panel** — phải **nói rõ với user**, đừng để họ hiểu là được bảo vệ toàn diện | ⚠️ `[EM]` |
| 6.12 | Ràng buộc kiến trúc bắt buộc | Credit ledger + **HOLD trước khi enqueue** (check-rồi-gọi là race condition), **hold reserve 3 credit/panel** (vì N=3), `CHECK (available >= 0)` ở tầng DB, hold reaper cho `expires_at` | `architect` + `researcher` |
| 6.13 | ⚠️ Đừng dựa vào cache | Hit rate chỉ **vài % tới ~10%** | `[EM]` `architect` — tự khai là ước lượng |

## CF-7 — Pháp lý (rủi ro nhị phân duy nhất)

| # | Sự thật | Giá trị | Nhãn |
|---|---|---|---|
| 7.1 | **NĐ 134/2026/NĐ-CP** | Ban hành **06/04/2026**, hiệu lực **09/04/2026**, sửa đổi NĐ 17/2023 | `[OFF]` cov.gov.vn + Baker McKenzie |
| 7.2 | **Điều 5a** | Tác phẩm AI-assisted chỉ được bảo hộ nếu con người có *"substantial and decisive intellectual contribution"*. **AI tạo hoàn toàn: KHÔNG được bảo hộ.** Kèm **nghĩa vụ lưu giữ prompts, inputs, intermediate drafts** | `[OFF]` |
| 7.3 | Hệ quả của 7.2 | Bảng `Generation` + `parent_generation_id` + `change_log` + `field_provenance` **là hồ sơ pháp lý bắt buộc**, không phải feature. **Không backfill được** — không lưu từ generation đầu tiên thì vĩnh viễn không có | `[OFF]` |
| 7.4 | ⚠️ **Điều 37a** | Giới hạn TDM ở *"non-commercial purposes at the point of use"* | ⚠️ **DỰA TRÊN BẢN TÓM TẮT, KHÔNG PHẢI NGUYÊN VĂN.** thuvienphapluat/nhansu trả **403**, IAPP **paywall** |
| 7.5 | Điều 37b | Kiểm **opt-out signal** ngay trong bước ingest — chi phí ~0 | `[OFF]` tóm tắt |
| 7.6 | Điều 198b safe harbour | Công cụ takedown, đăng ký đầu mối với **Bộ VHTTDL**, **SLA 72 giờ** | `[OFF]` tóm tắt |
| 7.7 | **Luật TTNT 2025** | AI disclosure là **nghĩa vụ nội địa Việt Nam**. Deadline tuân thủ **~01/03/2027** | `[OFF]` ⚠️ **hai nguồn mô tả phạm vi KHÁC NHAU** (chỉ "mô phỏng người thật" vs mọi nội dung AI) |
| 7.8 | ⭐ **Ưu tiên số 1** | **Ba câu hỏi ở §8.5 phải mang tới luật sư SHTT Việt Nam TRƯỚC khi thương mại hoá** | run trước |
| 7.9 | Vì sao 7.8 là ưu tiên 1 | **Rủi ro nhị phân duy nhất**: mọi rủi ro khác trả lời sai thì sản phẩm **kém hơn**; ba câu này trả lời sai thì sản phẩm **bất hợp pháp** | run trước §12 |

## CF-8 — Lộ trình (khung cố định, writer phân bổ effort bên trong)

| # | Sự thật | Giá trị | Nhãn |
|---|---|---|---|
| 8.1 | **Horizon Roadmap** | **09/2026 → 02/2027** (6 tháng) | `[CHỐT]` assumption A1 |
| 8.2 | Chu kỳ OKR | **Q4/2026** (10–12/2026) là chu kỳ chính + **preview Q1/2027**. Tháng 09/2026 là **pre-cycle**, đo bằng gate không bằng OKR | `[CHỐT]` assumption A2 |
| 8.3 | **Thứ tự milestone (cố định)** | **MVP0 → MVP1 → MVP2 → MVP3 → MVP4** | run trước §10 |
| 8.4 | **MVP0** | 1–2 tuần · ~$12 · **1 chapter duy nhất** · Story Bible + panel script **viết tay** · code đúng một việc: generate panel với reference + N candidate + VLM select | run trước §10 |
| 8.5 | **MVP0 đo BA chỉ số** | (1) consistency có đủ tốt không — *nhìn 8 panel liền nhau có nhận ra cùng một nhân vật không*; (2) **N tối thiểu** — mỗi bậc N giảm được là ~33% COGS; (3) ⭐ **human-reject rate sau VLM-select** — **chưa ai công bố con số này**, và nó quyết định checker có cắt được công người hay chỉ thêm chi phí | run trước §10 |
| 8.6 | MVP0 đo thêm, gần như miễn phí | **Multi-character panel 2–3 nhân vật** (CF-6.4) và **regen ratio thực tế p50/p90** (biến quyết định của cả mô hình tài chính) | run trước |
| 8.7 | MVP1 | Story Intelligence + **`tenant_id` từ ngày đầu** + **HITL gate & eval kit ngay tại đây** (không dồn MVP4) + **log preference data** + **kiểm opt-out Điều 37b trong bước ingest** + text clean là bước đầu tiên | run trước §10 |
| 8.8 | MVP2 | Comic Director. Bỏ Layout Score số thực → **rubric `beat_type` + emphasis quota**. Cứng hoá **≤3 nhân vật/panel**. Thêm `text_safe_zone`. **HAI human gate bắt buộc: speaker attribution + dialogue condensation** | run trước §10 |
| 8.9 | MVP3 | Visual Generation — **scale-up, không phải khám phá** (rủi ro đã được MVP0 kiểm trước) | run trước §10 |
| 8.10 | MVP4 | **Nâng ưu tiên export lên sớm** — thứ duy nhất người dùng thật sự nhận được. Continuity Checker chuyển sang **N-candidate selection**, không phải flag+autofix | run trước §10 |
| 8.11 | Ba việc xen vào mà §18 gốc không có | (a) **Checklist safe harbour Điều 198b** — trước khi mở cho người ngoài upload; (b) **Hard quota cưỡng chế trước khi enqueue** — trước bản trả phí đầu tiên; (c) **Typeset layer + bubble overlay** — nổ ngay ở panel có thoại đầu tiên, tức **trong MVP0** | run trước §10 |
| 8.12 | Nguyên tắc bao trùm | **Sinh một ảnh trong tuần đầu tiên**, dù bằng tay, dù chỉ 8 panel. Không phải để có sản phẩm, mà để biết tiền đề còn đứng | run trước §10 |
| 8.13 | ⚠️ Ràng buộc kiểm chứng | **Chưa ai xác nhận 6 tháng đủ cho 1 dev.** Writer Roadmap **BẮT BUỘC** nêu rõ nếu khung 09/2026–02/2027 không chứa hết MVP0–MVP3, và nói thẳng cái gì rơi ra ngoài. **Cấm nén lịch cho vừa khung.** | ràng buộc của PM |

## CF-9 — Ba thứ nên CẮT (đã có kết luận, không mở lại)

| # | Hạng mục | Quyết định | Lý do ngắn |
|---|---|---|---|
| 9.1 | Canvas editor §14 | **CẮT MỘT PHẦN** — giữ editor tối thiểu ~20–25% (panel card + variant picker · bubble/text overlay trong 1 panel · template layout · preview server-side · Story Bible editor). **HOÃN**: infinite canvas, undo xuyên state, realtime collab, inpainting | Nghĩa vụ pháp lý đặt lên **tầng DỮ LIỆU (audit event), không đặt lên tầng CANVAS** |
| 9.2 | Microservices + Vector DB §12 | **CẮT** — monolith. Lý do **MẠNH LÊN** dưới SaaS | run trước §6.2 |
| 9.3 | Layout Score số thực | **CẮT** cơ chế 5 số thực, **GIỮ** mục tiêu (layout theo narrative importance) → rubric rời rạc | Không có prior art; *"chưa ai làm vì không đáng"* |
| 9.4 | ⛔ `parent_generation` | **KHÔNG CẮT** — PM run trước đã **tự thu hồi** khuyến nghị cắt của chính mình | NĐ 134/2026 Điều 5a biến nó thành **compliance artifact bắt buộc** (CF-7.3) |

---

# Outline từng tài liệu

## 1. `Charter-Comic-Studio.md` — `business-analyst` #1

- **Độc giả đích**: anh — người ra quyết định build/không build. Thứ cấp: các AI agent của TNMCORE-OS ở run sau, dùng Charter làm ràng buộc đầu vào.
- **Nguồn sự thật**: bảng CF-1, CF-2, CF-4, CF-7 · [Analysis-Comic-Studio-Concept.md](../../../050-Research/Analysis-Comic-Studio-Concept.md) §3, §4.1, §12 · [findings/researcher.md](./findings/researcher.md) §A.1
- **Cấu trúc** (mở rộng `Template-Project-Charter.md` — 6 H2 gốc **giữ nguyên thứ tự**, thêm 4 mục):

  | # | Heading | Nội dung bắt buộc |
  |---|---|---|
  | 1 | `## 1. Thông tin dự án` | Tên, chủ sở hữu, ngày khởi tạo, trạng thái. **Sponsor = Manager = anh** — ghi thẳng, đừng bịa vai trò không tồn tại |
  | 2 | `## 2. Business Case` | ⚠️ **Neo vào CF-4.4 (SOM $4–14K ARR), TUYỆT ĐỐI KHÔNG dùng TAM $14B để biện minh.** Nêu rõ CF-4.1 và **vì sao nó không dùng được** (CF-4.2) — đây là phần chống tự lừa mình của tài liệu |
  | 3 | `## 3. Mục tiêu dự án` | 3–5 mục tiêu **đo được**. Mỗi mục tiêu phải map tới một chỉ số ở CF-8.5 hoặc CF-4.4 |
  | 4 | `## 4. Yêu cầu cấp cao` | Rút từ CHÍN điều kiện khả thi (CF-6.1) — liệt kê đủ chín, không rút gọn thành bảy |
  | 5 | `## 5. Phạm vi` **(mục MỚI)** | **Scope In / Scope Out**. ⚠️ Scope In ở đây là **phạm vi sản phẩm**, không phải ranh giới MVP — ranh giới MVP thuộc [MVP-Scope.md](./MVP-Scope.md), **link sang, đừng lặp lại** |
  | 6 | `## 6. Stakeholder Matrix (RACI)` **(mục MỚI — template không có)** | Bảng RACI, cột và hàng định nghĩa bên dưới |
  | 7 | `## 7. Ràng buộc (Constraints)` | ≥6 ràng buộc, mỗi cái một dòng, có nguồn. Bắt buộc gồm: 1 dev (CF-1.2) · mô hình 3 tầng đã chốt (CF-2.1) · trần ≤3 nhân vật/panel (CF-6.5) · deadline pháp lý ~01/03/2027 (CF-7.7) · **positioning writer-không-artist** (CF-5.7) · gross margin kỳ vọng 50–60% (CF-3.10) |
  | 8 | `## 8. Giả định (Assumptions)` | Mỗi giả định kèm **"sai thì hỏng ở đâu"**. Lấy các mục `[EM]` của CF làm nguồn |
  | 9 | `## 9. Tiêu chí thành công & Go/No-Go` **(mục MỚI)** | Trỏ sang [MVP-Scope.md](./MVP-Scope.md) cho Go/No-Go chi tiết; ở đây chỉ nêu **điều kiện chặn cấp dự án**: CF-7.8 (luật sư) chưa xong ⇒ không thương mại hoá |
  | 10 | `## 10. Tài liệu liên quan` **(mục MỚI)** | Link tới 4 tài liệu Planning còn lại + Analysis + Research Notes |

- **Bảng RACI — PM định nghĩa (template không có):**

  | Vai trò (cột) | Là ai |
  |---|---|
  | **Founder** | Anh — người duy nhất trong đội |
  | **AI Agent (TNMCORE-OS)** | `architect`, `business-analyst`, `software-engineer`, `security-auditor`… — thực thi dưới sự điều phối của anh |
  | **Luật sư SHTT** | Bên ngoài, **chưa engage** — ghi rõ trạng thái |
  | **Model provider** | Google (Gemini 3 Pro Image), BFL (FLUX.2) — bên ngoài, không đàm phán được |
  | **Design partner** | Tác giả truyện chữ tham gia thử — **chưa có ai**, ghi rõ |

  Hàng = nhóm hoạt động: Định hướng sản phẩm · Quyết định kiến trúc · Implementation · Quyết định pháp lý · Định giá & unit economics · Kiểm thử & nghiệm thu · Phân phối/marketing · Vận hành & sự cố.

  > ⚠️ **Ràng buộc chống RACI suy biến**: với đội 1 người, mọi ô dễ thành "A = Founder". Writer **phải** phân biệt được **A (Accountable)** với **R (Responsible)** ở những hàng mà AI agent thực sự làm, và **phải** đánh dấu **C (Consulted)** cho Luật sư SHTT ở hàng *Quyết định pháp lý* — kèm ghi chú **chưa engage**. Một RACI mà mọi ô là "Founder" là một RACI vô dụng, và thà nói thẳng điều đó còn hơn tô vẽ.

- **Tiêu chí xong**: đủ 10 mục · RACI ≥8 hàng × 5 cột, không hàng nào toàn "Founder" mà không giải thích · ≥6 ràng buộc có nguồn · **0 lần xuất hiện TAM $14B như một lý do biện minh** · frontmatter `id: CHARTER-001, type: charter, status: draft, created: 2026-08-23` · ≥4 markdown link phân giải được.

## 2. `MVP-Scope.md` — `architect`

- **Độc giả đích**: anh, tại thời điểm phải quyết "build tiếp hay dừng".
- **Nguồn sự thật**: CF-6, CF-8, CF-9 · Analysis §4.2, §6, §10 · `findings/architect.md` của run trước.
- **Cấu trúc**:

  | # | Heading | Nội dung bắt buộc |
  |---|---|---|
  | 1 | `## 1. Mục đích & cách đọc tài liệu` | Ranh giới với Charter và Roadmap — tài liệu này trả lời *"cái gì vào MVP, cái gì không"*, không trả lời *"khi nào"* |
  | 2 | `## 2. Nguyên tắc cắt scope` | 3–4 nguyên tắc rút từ CF-9 + CF-8.12 |
  | 3 | `## 3. Bảng MVP vs Full Scope` | **Bảng chính.** Cột: Hạng mục · MVP0 · MVP1 · MVP2 · MVP3 · MVP4 · Full Scope · Căn cứ. Dùng ✅ / 🟡 một phần / ⛔ hoãn / ❌ cắt hẳn |
  | 4 | `## 4. Cắt gì và vì sao` | Bốn mục CF-9.1–9.4. ⚠️ **CF-9.4 phải trình bày như một sự tự thu hồi** — nó là dấu vết quyết định, không phải khuyến nghị |
  | 5 | `## 5. Editor tối thiểu — ranh giới chi tiết` | 5 thành phần BẮT BUỘC (~20–25%) vs 4 thành phần HOÃN. ⚠️ **Nêu rõ CF-6.7 và CF-6.8 là HAI MẪU SỐ KHÁC NHAU, cấm trừ cho nhau** |
  | 6 | `## 6. Không được cắt — danh sách cứng` | `parent_generation_id` + `relation_kind` + `change_log` + `field_provenance` + `generation.origin` (CF-7.3) · `tenant_id` từ ngày đầu · opt-out check Điều 37b · hold reserve 3 credit/panel (CF-6.12). Mỗi mục kèm **"không giữ thì hỏng thế nào"** |
  | 7 | `## 7. Go/No-Go Decision` | **Mục quan trọng nhất.** Ba gate, mỗi gate có tiêu chí **đo được** và hành động cho cả hai nhánh |
  | 8 | `## 8. Điều kiện thoát (kill criteria)` | Khi nào thì dừng hẳn dự án — nêu thẳng, đây là thứ tài liệu planning hay né |

- **Ba gate của mục 7 — PM định khung, writer điền chi tiết:**

  | Gate | Thời điểm | Tiêu chí PASS | Nếu FAIL |
  |---|---|---|---|
  | **G0 — Pháp lý** | Trước dòng code thương mại đầu tiên | Ba câu CF-7.8 có câu trả lời từ luật sư SHTT VN, và không câu nào chặn mô hình user-upload thương mại | **Dừng thương mại hoá.** Rủi ro nhị phân (CF-7.9) |
  | **G1 — Kỹ thuật (sau MVP0)** | Cuối 09/2026 | Ba chỉ số CF-8.5 đạt ngưỡng writer định nghĩa; đặc biệt **multi-character 2–3 nhân vật** (CF-6.4) | Đổi cách tiếp cận — và biết sau **2 tuần** thay vì 4 tháng |
  | **G2 — Kinh tế (sau MVP1)** | Cuối Q4/2026 | Regen ratio p50/p90 đo được cho phép mô hình 3 tầng (CF-2) giữ margin trong khoảng CF-3.10 | Đổi granularity render sang whole-page (CF-9 / Analysis §9b.3) — **data model không phải đổi** |

- **Tiêu chí xong**: bảng mục 3 phủ đủ MVP0–MVP4 · ba gate đều có tiêu chí đo được, không có gate nào ghi "đánh giá chủ quan" · mục 8 tồn tại và không rỗng · frontmatter `id: MVPSCOPE-001, type: mvp-scope, status: draft, created: 2026-08-23`.

## 3. `Roadmap.md` — `architect` ⚠️ SỬA STUB

> ⛔ **File đã tồn tại.** `id: ROADMAP-001`, `created: 2026-02-04`. **GIỮ NGUYÊN `id` và `created`. THÊM `updated: 2026-08-23`.** Ghi đè frontmatter mới là lỗi im lặng và sẽ bị verify bắt.

- **Độc giả đích**: anh — người phân bổ thời gian của chính mình.
- **Nguồn sự thật**: CF-8 toàn bộ · CF-6.7–6.9 (effort) · Analysis §10.
- **Cấu trúc**:

  | # | Heading | Nội dung |
  |---|---|---|
  | 1 | `## 1. Khung thời gian & giả định` | Horizon CF-8.1. **Nêu thẳng CF-8.13** — đây là mục đầu tiên vì nó chi phối cách đọc mọi thứ phía dưới |
  | 2 | `## 2. Bảng lộ trình tổng` | Cột: Mốc · Khoảng thời gian · Mục tiêu · Deliverable · Điều kiện ra (exit criteria) · Effort ước tính |
  | 3 | `## 3. Chi tiết từng mốc` | H3 cho mỗi mốc: **Pre-cycle 09/2026** · MVP1 · MVP2 · MVP3. Mỗi mốc: input, output, rủi ro chính, gate liên quan |
  | 4 | `## 4. Ba việc xen ngang` | CF-8.11 — đặt đúng mốc, không dồn cuối |
  | 5 | `## 5. Ngoài horizon` | MVP4 và phần bị đẩy ra khỏi 6 tháng (nếu có) |
  | 6 | `## 6. Phụ thuộc & đường găng` | Cái gì chặn cái gì. **G0 pháp lý chặn thương mại hoá nhưng KHÔNG chặn MVP0–MVP1** — nêu rõ, vì đây là thứ dễ hiểu nhầm thành "chờ luật sư mới được code" |

- **Pre-cycle 09/2026 phải chứa đủ ba việc** (Analysis §12 kết luận "ba việc trước dòng code đầu tiên"): mang CF-7.8 tới luật sư · chạy MVP0 (CF-8.4–8.6) · sửa khóa thời gian `(chapter, scene)` và chốt danh sách phải-có-trong-schema.
- **Tiêu chí xong**: mọi mốc có **exit criteria đo được** · CF-8.13 được trả lời tường minh (khung có đủ hay không, cái gì rơi ra) · mục 6 nêu rõ G0 không chặn MVP0–MVP1 · frontmatter giữ `id`/`created`, có `updated`.

## 4. `OKRs.md` — `product-owner` ⚠️ SỬA STUB · ⛔ CHẠY SAU `architect`

> ⛔ **File đã tồn tại.** `id: OKRS-001`, `created: 2026-02-04`. **GIỮ `id` và `created`, THÊM `updated: 2026-08-23`.**
> ⛔ **Phải đọc `Roadmap.md` và `MVP-Scope.md` đã hoàn thành** — Key Result trỏ tới mốc trong Roadmap, không tự chế mốc mới.

- **Độc giả đích**: anh — dùng để biết tuần này làm đúng việc hay không.
- **Nguồn sự thật**: `Roadmap.md` + `MVP-Scope.md` (đã viết xong) · CF-4.4 (SOM) · CF-8.5 (ba chỉ số MVP0) · CF-5.7–5.10 (kênh) · [findings/researcher.md](./findings/researcher.md) §A.5.
- **Cấu trúc**: `## 1. Cách dùng` · `## 2. Pre-cycle 09/2026 — đo bằng gate` · `## 3. Q4/2026 — chu kỳ chính` · `## 4. Preview Q1/2027` · `## 5. Chỉ số theo dõi (không phải KR)` · `## 6. Anti-goals`
- **Ràng buộc nội dung:**
  - **3–4 Objective mỗi chu kỳ, mỗi Objective 2–4 Key Result.** Nhiều hơn là danh sách việc, không phải OKR.
  - **Mọi KR phải có con số và cách đo.** KR không đo được thì cắt.
  - ⚠️ **KR doanh thu phải neo CF-4.4** — thang **trăm đô/tháng**, không phải nghìn. Neo tham chiếu: Anifusion **$833 MRR sau ~2 năm solo** (CF-4.5, kèm nhãn mâu thuẫn).
  - ⚠️ **Không đặt KR nào dựa trên TAM.**
  - **Mục 6 Anti-goals là bắt buộc**, gồm tối thiểu: không làm Show HN/Product Hunt làm kênh chính (CF-5.8) · không marketing vào cộng đồng hoạ sĩ (CF-5.6–5.7) · không build canvas editor đầy đủ (CF-9.1) · không đặt mục tiêu doanh thu thang nghìn đô trong năm 1.
  - KR kênh phân phối lấy từ bảng đề xuất ở `findings/researcher.md` §A.5, **giữ nguyên phần neo lý do**.
- **Tiêu chí xong**: mỗi KR có số + cách đo + tần suất đo · Anti-goals ≥4 mục · **0 KR trích TAM** · KR doanh thu nằm trong dải CF-4.4 · frontmatter giữ `id`/`created`.

## 5. `Risk-Register.md` — `security-auditor`

- **Độc giả đích**: anh — dùng để biết cái gì có thể giết dự án và dấu hiệu nhận biết sớm.
- **Nguồn sự thật**: CF-3 (kinh tế), CF-4.6–4.9 (retention), CF-5 (cạnh tranh), CF-6 (kỹ thuật), CF-7 (pháp lý) · Analysis §5, §8, §9b · [findings/researcher.md](./findings/researcher.md).
- **Cấu trúc** (mở rộng `Template-Risk-Register.md`):

  | # | Heading | Nội dung |
  |---|---|---|
  | 1 | `## 1. Risk Matrix Overview` | ⚠️ **Template để RỖNG mục này. PM định nghĩa thang bên dưới — writer chép vào và giải thích.** |
  | 2 | `## 2. Risk Log` | Bảng chính, **11 cột** (7 gốc + 4 bổ sung) |
  | 3 | `## 3. Rủi ro nhị phân — tách riêng` | CF-7.8/7.9. Đây **không** phải một hàng bình thường trong bảng: mọi rủi ro khác làm sản phẩm kém hơn, rủi ro này làm sản phẩm **bất hợp pháp** |
  | 4 | `## 4. Rủi ro đã biết là KHOẢNG TRỐNG` | Những thứ **không đánh giá được vì thiếu dữ liệu** — CF-4.9, CF-7.4, CF-5.4, CF-6.10/6.11. Ghi rõ *"chưa đo được"* thay vì gán một Score giả |
  | 5 | `## 5. Lịch rà soát` | Rủi ro nào rà ở gate nào (G0/G1/G2 của MVP-Scope) |

- **Thang đánh giá — PM định nghĩa (template không có):**

  | Thang | 1 | 2 | 3 |
  |---|---|---|---|
  | **Probability** | Low — chưa có dấu hiệu | Med — có dấu hiệu, chưa xảy ra | High — đã/gần như chắc xảy ra |
  | **Impact** | Low — làm chậm | Med — phải làm lại một phần | High — chặn ra mắt hoặc đe doạ sự tồn tại |

  **`Score = Probability × Impact`**, dải **1–9**. Phân loại: **1–2 Thấp** · **3–4 Trung bình** · **6 Cao** · **9 Nghiêm trọng**.

  > Thang này **khớp ngược** với hàng ví dụ của template (`High × Med = 6` ⇒ 3 × 2 = 6), nên không phá tương thích. Nhưng template **chưa từng nêu công thức** — nó là suy luận, và tài liệu phải nói rõ đây là định nghĩa được thiết lập tại run này.

- **11 cột của Risk Log**: `ID` · `Category` · `Risk Description` · `Trigger` · `Probability` · `Impact` · `Score` · `Mitigation Plan` · `Residual Risk` · `Status` · `Owner`
  - `Category` ∈ { Pháp lý · Kỹ thuật · Kinh tế · Thị trường/Cạnh tranh · Vận hành }
  - `Status` ∈ { open · mitigating · accepted · closed }
  - `Owner`: với đội 1 người, ghi **vai trò TNMCORE-OS** chịu trách nhiệm (`architect`, `security-auditor`…), không ghi "Founder" ở mọi hàng
- **Rủi ro BẮT BUỘC có mặt** (writer bổ sung thêm, nhưng không được thiếu cái nào trong đây):

  | Nhóm | Phải có |
  |---|---|
  | Pháp lý | Điều 37a TDM thương mại (CF-7.4) · safe harbour Điều 198b chưa đăng ký (CF-7.6) · deadline Luật TTNT ~01/03/2027 (CF-7.7) · không lưu provenance từ đầu ⇒ mất bảo hộ và **không backfill được** (CF-7.3) |
  | Kinh tế | Power user −262% margin (CF-3.7) · GRR 23% band `<$50` (CF-4.6 **+ ba caveat**) · $12,06 là **sàn không phải trần** (CF-3.5) |
  | Kỹ thuật | Multi-character 2–3 nhân vật chưa có benchmark (CF-6.4) · props 4.19/5 (CF-6.3) · speaker attribution (CF-6.10) · checker chỉ phủ 40–60% (CF-6.11) |
  | Thị trường | **GlobalComix + INKR** (CF-5.2–5.3) · **Constella — rủi ro nền tảng, hàng RIÊNG** (CF-5.4–5.5) · backlash cộng đồng (CF-5.6) |
  | Vận hành | **Bus factor = 1** (CF-1.2) · phụ thuộc model provider, silent model drift · onboarding BYOK không đo được friction (CF-2.5 caveat) |

- **Tiêu chí xong**: ≥16 rủi ro · mọi hàng có `Trigger` không rỗng · mục 4 tồn tại và không gán Score giả cho thứ chưa đo được · công thức Score được nêu tường minh · frontmatter `id: RISK-001, type: risk-register, status: draft, created: 2026-08-23`.

## 6. Scaffolding Dewey + `000-Index.md` — **PM**

- **Nguồn sự thật**: [findings/inventory.md](./findings/inventory.md) Mục 1A (danh sách 32 thư mục) và Mục 4.3.
- **Việc**: `mkdir` đúng **32** thư mục + `.gitkeep` mỗi thư mục (git không track thư mục rỗng) + tạo `docs/000-Index.md`.
- **Tiêu chí xong**: `find docs -type d` khớp 100% khối *Required Folder Structure* của RULE-001 · `000-Index.md` chỉ liệt kê tài liệu **có thật** · 2 link chết tới `000-Index.md` hết chết.

## 7. `Analysis-Market-Competitor-Landscape.md` — `business-analyst` #2

- **Độc giả đích**: anh, khi cần quyết định định vị và định giá. Thứ cấp: chính writer của Charter/OKR ở các run sau.
- **Nguồn sự thật**: [findings/researcher.md](./findings/researcher.md) — **đây là nguồn gần như duy nhất**, đọc trực tiếp, đừng chờ PM tóm tắt lại.
- **Cấu trúc**: `## 1. Tóm tắt` · `## 2. Quy mô thị trường (TAM/SAM/SOM)` · `## 3. Bối cảnh đối thủ` · `## 4. Mô hình kinh doanh & pricing` · `## 5. Retention benchmark` · `## 6. Kênh phân phối` · `## 7. Khoảng trống dữ liệu` · `## Tài liệu tham khảo`
- **Ràng buộc riêng:**
  - ⚠️ **KHÔNG lặp lại nội dung của [Analysis-Comic-Studio-Concept.md](../../../050-Research/Analysis-Comic-Studio-Concept.md)** — **link sang** nó. Trùng lặp sẽ bị tiêu chí *Coherence* của verify bắt.
  - **Giữ nguyên hệ nhãn `[OFF]/[BCN]/[TC]/[EM]`** của findings. Đây là tài liệu mà nhãn quan trọng ngang nội dung.
  - **Mục 7 là bắt buộc và phải đầy đủ** — findings liệt kê khoảng trống theo từng câu (1.a–1.d, 2.a–2.e, 3.a–3.e, 4.a–4.d, 5.a–5.e). Gom lại, **không bỏ mục nào**, đặc biệt **5.e (thị trường Việt Nam — chưa tra)**.
  - **Mâu thuẫn Anifusion (CF-4.5) phải xuất hiện dưới dạng mâu thuẫn**, không được chọn một số rồi trình bày như sự thật.
  - Mọi URL trong findings phải được mang sang mục *Tài liệu tham khảo*.
- **Tiêu chí xong**: 7 mục + tham khảo · mọi số định lượng có nhãn · mục 7 phủ đủ 5 nhóm khoảng trống · ≥25 URL · **0 đoạn trùng lặp với Analysis-Comic-Studio-Concept** · frontmatter `id: RESEARCH-002, type: research, status: draft, created: 2026-08-23`.

---

# Markdown link phải tạo

> RULE-001 quy tắc #5: **standard markdown link, relative path. CẤM wiki-link `[[...]]`.**

| Từ | Tới | Quan hệ |
|---|---|---|
| `Charter-Comic-Studio.md` | `./MVP-Scope.md` · `./Roadmap.md` · `./OKRs.md` · `./Risk-Register.md` | Charter là gốc, trỏ tới 4 tài liệu con |
| `Charter-Comic-Studio.md` | `../050-Research/Analysis-Comic-Studio-Concept.md` | Căn cứ thẩm định |
| `MVP-Scope.md` | `./Charter-Comic-Studio.md` · `./Roadmap.md` | Ranh giới ↔ lịch trình |
| `Roadmap.md` | `./MVP-Scope.md` · `./OKRs.md` | Mốc ↔ phạm vi ↔ mục tiêu |
| `OKRs.md` | `./Roadmap.md` · `./MVP-Scope.md` | KR trỏ mốc |
| `Risk-Register.md` | `./MVP-Scope.md` (gate G0/G1/G2) · `../050-Research/Analysis-Comic-Studio-Concept.md` | Rủi ro ↔ gate ↔ căn cứ |
| `Analysis-Market-Competitor-Landscape.md` | `./Analysis-Comic-Studio-Concept.md` · `../010-Planning/Charter-Comic-Studio.md` | Bổ sung, không thay thế |
| `docs/000-Index.md` | Toàn bộ MOC + 6 tài liệu mới | Trang chủ |

# MOC cần cập nhật (PM giữ, writer cấm chạm)

| MOC | Mục thêm/sửa |
|---|---|
| `docs/010-Planning/Planning-MOC.md` | Thêm 5 tài liệu mới (Charter, MVP-Scope, Risk-Register + mô tả cho Roadmap/OKRs vốn đang là link trần); sửa dòng `pm-runs` đang ghi sai là *"run-state của `/pm-run`"*; bump `updated` |
| `docs/050-Research/Research-MOC.md` | Thêm `Analysis-Market-Competitor-Landscape.md`; `Competitor-Analysis/` và `User-Interviews/` hết là placeholder sau scaffolding — sửa cảnh báo; bump `updated` |
| `docs/999-Resources/Resources-MOC.md` | Link `../000-Index.md` hết chết; `./Meeting-Notes/` hết chết. **Không** xoá link `Template-Daily-Report.md` (guardrail: không xoá) — đánh dấu là chưa tồn tại |
| `docs/000-Index.md` | **Tạo mới** |
| Các MOC 0 byte (`Specs-MOC.md`, `Design-MOC.md`) | ⚠️ **NGOÀI SCOPE** — thuộc run Shape B. Chỉ ghi nhận. |

# Ripple (bắt buộc với T3)

| Bị ảnh hưởng | Ảnh hưởng thế nào | Xử lý trong run này |
|---|---|---|
| `knowledge-base/99-Templates/Documents-Template.md` (RULE-001, `approved`) | Thêm **một hàng** `MVP Scope` vào bảng Document Type Mapping | ✅ Có — **PM làm ở close-step**, đã được duyệt tại gate. Additive, bump `updated` |
| `docs/050-Research/Analysis-Comic-Studio-Concept.md` | Run này **bổ sung** 2 rủi ro cạnh tranh (GlobalComix, Constella) và **điều chỉnh** khuyến nghị pricing của nó | ⛔ **KHÔNG sửa.** Nó là dấu vết quyết định tại thời điểm viết. Research Notes mới **link sang** và nêu rõ phần nào đã được cập nhật |
| `docs/999-Resources/Glossary.md` | Thuật ngữ mới: BYOK, TAM/SAM/SOM, GRR/NRR, RACI, best-of-N, unit economics… | ✅ PM bổ sung ở close-step nếu term chưa có |
| `knowledge-base/00-Index.md:66` | Đang link chết tới `docs/000-Index.md` | ✅ Tự lành sau khi tạo file |
| `docs/999-Resources/Request.md` | Thiếu hoàn toàn frontmatter | ⛔ Ngoài scope — ghi vào *Nợ lại* |

---

# Ràng buộc chống bỏ sót (bài học verdict run trước)

> Run trước có **2 MAJOR** là **khuyến nghị bị rơi khỏi outline**, không phải writer làm sai. Nguyên nhân: PM lập bảng ràng buộc bằng cách trích những điểm **sắc nhất**, mà *"bộ lọc sắc không phải bộ lọc quan trọng"* — hai khuyến nghị bị rơi đều rẻ và không gây tranh cãi, tức là loại **dễ rơi nhất và cũng đáng làm nhất**.

**Đối sách đã áp dụng cho outline này:**

1. Bảng canonical facts được xây bằng **quét cơ học qua từng mục** của Analysis (§4.1, §5, §6, §8, §9b, §10, §11, §12) và từng câu của `findings/researcher.md` — không chỉ trích điểm sắc.
2. Mỗi tài liệu có mục **"phải có mặt"** liệt kê tường minh (Risk Register có bảng riêng; OKRs có Anti-goals bắt buộc; MVP-Scope có danh sách "không được cắt").
3. **Dispatch verify BẮT BUỘC kèm yêu cầu**: *"liệt kê khuyến nghị có trong CF/findings mà KHÔNG có trong deliverable"* — bốn tiêu chí Bước 6 bắt **thừa**, không bắt **thiếu**.
4. **Thêm cho run này**: verify phải kiểm **cross-doc consistency** — cùng một con số CF có xuất hiện khác nhau ở hai tài liệu không, và nhãn caveat có sống sót không. Đây là rủi ro **mới** do chính việc song song hoá 4 writer sinh ra.
