---
id: RISK-001
type: risk-register
status: draft
created: 2026-08-23
updated: 2026-08-23
owner: "@security-auditor"
tags: [risk, planning, comic-studio, compliance]
linked-to: "./MVP-Scope.md"
---

# ⚠️ Risk Register — comic-studio

> [!IMPORTANT]
> Tài liệu này trả lời đúng một câu hỏi: **cái gì có thể giết dự án, và dấu hiệu nào cho biết nó đang xảy ra.**
> Cột có giá trị thực dụng cao nhất không phải `Score` mà là **`Trigger`** — thứ anh có thể quan sát được mà không cần đợi ai báo cáo.

**Điều hướng nhanh**: [1. Risk Matrix Overview](#1-risk-matrix-overview) · [2. Risk Log](#2-risk-log) · [3. Rủi ro nhị phân — tách riêng](#3-rủi-ro-nhị-phân--tách-riêng) · [4. Rủi ro đã biết là KHOẢNG TRỐNG](#4-rủi-ro-đã-biết-là-khoảng-trống) · [5. Lịch rà soát](#5-lịch-rà-soát)

**Nguồn sự thật**: bảng `CANONICAL FACTS` (CF-1 → CF-9) tại [outline.md của run 2026-08-23](./pm-runs/2026-08-23-khoi-tao-tai-lieu-planning-comic-studio/outline.md) · [Analysis-Comic-Studio-Concept.md](../050-Research/Analysis-Comic-Studio-Concept.md) §5, §8, §9b · [findings/researcher.md](./pm-runs/2026-08-23-khoi-tao-tai-lieu-planning-comic-studio/findings/researcher.md).

**Quy ước nhãn nguồn — giữ nguyên từ bảng CF, số và nhãn là một cặp không tách rời**: `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` thứ cấp · `[EM]` ước lượng/phép nhân, **không phải số đo** · `[CHỐT]` quyết định của anh tại gate. Ngưỡng nào do chính tài liệu này đặt ra được đánh dấu `[ngưỡng nội bộ đặt tại run này]` để không bị đọc nhầm thành số đo.

---

## 1. Risk Matrix Overview

> [!WARNING]
> **Thang dưới đây được thiết lập TẠI RUN NÀY, không phải kế thừa.** `Template-Risk-Register.md` để trống mục này và **chưa từng nêu công thức** — nó chỉ có đúng một hàng ví dụ (`High × Med = 6`). Thang này được **khớp ngược** từ hàng ví dụ đó (3 × 2 = 6) nên không phá tương thích với template, nhưng phải nói rõ: công thức là **suy luận**, không phải quy định có sẵn.

### 1.1 Hai thang thành phần

| Thang | 1 | 2 | 3 |
|---|---|---|---|
| **Probability** | **Low** — chưa có dấu hiệu | **Med** — có dấu hiệu, chưa xảy ra | **High** — đã xảy ra hoặc gần như chắc xảy ra |
| **Impact** | **Low** — làm chậm | **Med** — phải làm lại một phần | **High** — chặn ra mắt hoặc đe doạ sự tồn tại |

### 1.2 Công thức

```
Score = Probability × Impact        (dải 1–9)
```

| Score | Phân loại | Nghĩa thực dụng |
|---|---|---|
| **1–2** | **Thấp** | Ghi nhận, không tiêu thời gian chủ động |
| **3–4** | **Trung bình** | Có kế hoạch giảm thiểu, rà theo gate |
| **6** | **Cao** | Phải có hành động cụ thể trước gate liên quan |
| **9** | **Nghiêm trọng** | Chặn công việc khác cho tới khi hạ được |

### 1.3 Cách dùng — ba điểm phải hiểu đúng

1. **Dải hợp lệ chỉ có sáu giá trị: 1 · 2 · 3 · 4 · 6 · 9.** Đó là toàn bộ tích số có thể có của `{1,2,3} × {1,2,3}`. **Nếu thấy Score bằng 5, 7 hoặc 8 thì đó là lỗi nhập liệu**, không phải một mức mới. Đây là lý do bảng phân loại nhảy từ 4 thẳng lên 6.
2. **Probability đo khả năng rủi ro *thành hiện thực nếu không làm gì thêm*** — không phải khả năng tiền đề của nó đang tồn tại. Ví dụ: bus factor = 1 là **sự thật hiện hữu** (CF-1.2 `[CHỐT]`), nhưng *"1 dev gián đoạn dài ngày"* là **Med**, không phải High.
3. **Score không phải thứ tự ưu tiên tuyệt đối.** Có hai loại rủi ro nằm **ngoài thang này** và cố ý không được gán Score:
   - **Rủi ro nhị phân** (mục [3](#3-rủi-ro-nhị-phân--tách-riêng)) — nó không làm sản phẩm *kém hơn*, nó làm sản phẩm *bất hợp pháp*. Nhân một xác suất chưa biết với một impact vô hạn cho ra một con số vô nghĩa.
   - **Khoảng trống dữ liệu** (mục [4](#4-rủi-ro-đã-biết-là-khoảng-trống)) — thứ CF ghi rõ là **chưa đo được**. Gán một Score cho nó là biến *"không biết"* thành *"đã đánh giá"*, và đó là loại sai tệ nhất trong một tài liệu rủi ro.

---

## 2. Risk Log

> [!NOTE]
> **Hai điều cố ý về bảng này:**
> 1. **Điều 37a (TDM thương mại) KHÔNG có hàng trong bảng.** Đây là bỏ sót có chủ đích: nó là rủi ro nhị phân → xem mục [3 (RB-01)](#3-rủi-ro-nhị-phân--tách-riêng); và bản thân điều luật hiện chỉ đọc được qua **bản tóm tắt** → xem mục [4 (G-01)](#41-năm-khoảng-trống--không-gán-score).
> 2. **Constella (WEBTOON) không nằm trong bảng chính** mà ở bảng riêng [§2.2](#22-rủi-ro-nền-tảng--một-hàng-riêng-khác-loại) — nó khác loại với rủi ro đối thủ.
>
> `Owner` ghi **vai trò TNMCORE-OS** chịu trách nhiệm thực thi, không ghi "Founder" ở mọi hàng — đội 1 người (CF-1.2 `[CHỐT]`) nên mọi hàng đều quy về anh ở cấp *Accountable*, và một bảng mà mọi ô là "Founder" thì không dùng được.

### 2.1 Bảng chính

| ID | Category | Risk Description | Trigger (dấu hiệu quan sát được) | Probability | Impact | Score | Mitigation Plan | Residual Risk | Status | Owner |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- | :--- | :--- |
| **R-01** | Pháp lý | **Không lưu provenance từ generation ĐẦU TIÊN ⇒ mất bảo hộ bản quyền và KHÔNG BACKFILL ĐƯỢC.** NĐ 134/2026 Điều 5a `[OFF]` chỉ bảo hộ tác phẩm AI-assisted khi con người có *"substantial and decisive intellectual contribution"*, kèm **nghĩa vụ lưu prompts, inputs, intermediate drafts**. Bảng `Generation` + `parent_generation_id` + `change_log` + `field_provenance` là **hồ sơ pháp lý**, không phải feature (CF-7.3 `[OFF]`) | Migration đầu tiên tạo bảng `generation` mà **thiếu** `parent_generation_id` / `relation_kind` / `change_log` / `field_provenance` / `origin`; **hoặc** chạy generation thật đầu tiên trước khi migration đó merge; **hoặc** xuất hiện script seed ghi ảnh vào storage mà không có row `generation` tương ứng | 3 | 3 | **9** | Đưa 5 trường vào **migration số 1**, không phải backlog. Test guardrail: mọi INSERT vào `generation` thiếu `origin` phải fail ở tầng DB. CF-9.4 đã **tự thu hồi** khuyến nghị cắt `parent_generation` | **Không có đường lùi.** Mọi ảnh sinh trước khi schema đúng là mất vĩnh viễn phần hồ sơ — chỉ có thể vứt bỏ, không sửa được | open | `architect` |
| **R-02** | Pháp lý | **Safe harbour Điều 198b chưa đủ điều kiện**: chưa có công cụ tiếp nhận takedown, **chưa đăng ký đầu mối (email + số điện thoại) với Bộ VHTTDL**, chưa có quy trình **SLA 72 giờ** (CF-7.6 `[OFF]` tóm tắt). Mở cho người ngoài upload trước khi xong checklist ⇒ nền tảng chịu trách nhiệm trực tiếp thay vì được miễn trừ | Mở đăng ký cho user ngoài trước khi checklist CF-8.11(a) tick xong; **hoặc** nhận yêu cầu takedown đầu tiên mà không có form/email `copyright@` và không có đầu mối đã đăng ký; **hoặc** một takedown quá **72 giờ** chưa xử lý | 2 | 3 | **6** | Checklist 6 mục (Analysis §8.3): form + `copyright@`, đăng ký đầu mối, **soft-delete + disable-access** cấp project (không hard delete, còn phải giữ cho counter-notice), user warrant, opt-out check. Rẻ, thuộc MVP, làm trước khi mở upload | Câu *"SaaS có xử lý/biến đổi nội dung có được coi là hosting service không"* vẫn mở → RB-01 câu 3 | open | `security-auditor` |
| **R-03** | Pháp lý | **Deadline Luật TTNT 2025 ~01/03/2027** (CF-7.7 `[OFF]`) rơi **ngay sau** horizon roadmap 09/2026–02/2027 (CF-8.1 `[CHỐT]`). Nghĩa vụ disclosure + đánh dấu định dạng máy đọc là **nghĩa vụ nội địa Việt Nam**, không phải chuyện thị trường nước ngoài. ⚠️ **Hai nguồn mô tả phạm vi KHÁC NHAU** (chỉ *"mô phỏng người thật"* vs mọi nội dung AI) — xem G-06 | Tới **12/2026** mà export path chưa nhúng được machine-readable marker, hoặc UI chưa có chỗ nào cho user biết đang tương tác với hệ thống AI; **hoặc** Chính phủ ban hành hướng dẫn định dạng máy đọc mà sản phẩm chưa có provenance field ở cấp page/panel | 2 | 3 | **6** | Provenance field cấp page/panel là **requirement** (đã trùng với R-01 ⇒ một lần build, hai nghĩa vụ). Verify xem **SynthID** đã nhúng sẵn trong Nano Banana Pro có thoả nghĩa vụ không — **phải verify, không giả định** (RB-01 câu 2) | Nếu SynthID không được chấp nhận, phải tự nhúng watermark ở export path — chi phí chưa ước lượng | open | `security-auditor` |
| **R-04** | Pháp lý | **Nghịch lý safe harbour**: build feature *"cảnh báo truyện này có thể có bản quyền của người khác"* **PHÁ chính miễn trừ Điều 198b**, vì điều kiện (a) của miễn trừ là **"không biết"** — bộ phát hiện tạo ra đúng tri thức mà luật đang miễn trừ cho việc không có (Analysis §8.3). Một dev sẽ làm ngược điều này theo bản năng vì "chủ động kiểm tra" nghe như hành vi có trách nhiệm | Xuất hiện backlog item / issue / PR mang tên kiểu `copyright detection`, `plagiarism check`, `flag nội dung khả nghi`, `similarity scan` — **trước khi** có xác nhận của luật sư | 2 | 3 | **6** | Ghi thẳng vào danh sách **anti-feature**. Phân biệt rõ với việc **được phép**: đọc opt-out signal do chính chủ quyền gắn vào file là dữ kiện khách quan, không phải tri thức suy đoán (R-06) | Ranh giới giữa "đọc nhãn" và "suy đoán" chưa được luật sư xác nhận | open | `security-auditor` |
| **R-05** | Pháp lý | **ToS thiếu ba pattern phòng tuyến hợp đồng** mà **mọi** đối thủ đều có: user warrant + indemnify; assign toàn bộ quyền output cho user kèm disclaimer bất định pháp lý theo jurisdiction; DMCA designated agent nếu nhắm thị trường Mỹ (Analysis §8.3) | User ngoài đầu tiên đăng ký được mà trang `/terms` còn trống, hoặc không có điều khoản buộc user cam kết có quyền với truyện họ upload | 2 | 2 | **4** | Copy pattern ngành (ComicInk, myComics.ai, livecomics.to). Gắn checkbox cam kết quyền vào **bước upload**, không chỉ ở trang ToS | ToS copy từ đối thủ chưa được luật sư Việt Nam rà — hiệu lực trước toà VN chưa chắc chắn | open | `business-analyst` |
| **R-06** | Pháp lý | **Điều 37b (opt-out) không được kiểm trong bước ingest** (CF-7.5 `[OFF]` tóm tắt, chi phí ~0). Nếu cơ quan chức năng coi extraction là TDM, việc thiếu bước kiểm là **một vi phạm đã xảy ra hàng nghìn lần**, không sửa hồi tố được | Pipeline ingest được merge mà không có bước đọc metadata / rights-management-info của file upload + log kết quả kèm timestamp | 2 | 2 | **4** | Thêm một bước trong ingest: đọc metadata, log kèm timestamp, **chặn nếu có signal bảo lưu**. Chi phí xây ≈ 0, chi phí chạy = 0. **Làm kể cả khi tin rằng 37a không áp** — đây là loại đánh đổi không cần cân | Nếu 37a thực sự áp, bước kiểm này giảm rủi ro nhưng **không** trả lời được RB-01 câu 1 | open | `architect` |
| **R-07** | Kinh tế | **Power user đốt margin −262%** (CF-3.7 `[EM]`): 3 chapter/tháng @N=3 ⇒ COGS **$36.18** `[EM]` (3 × $12,06 `[EM tính từ OFF]`) trên doanh thu $9.99. Và **1 chapter @N=3 = 180 ảnh** (CF-3.9 `[EM]` 60 × 3) đã **vượt ngưỡng ~125 ảnh/tháng** (CF-2.5 `[TC]`) **ngay ở chapter đầu tiên** — tức phân khúc mục tiêu chính *là* power user | Một tài khoản vượt **~125 ảnh/tháng** `[TC]` mà vẫn nằm ở tầng credit managed; **hoặc** COGS/user/tháng vượt doanh thu tầng đó trong bất kỳ chu kỳ billing nào; **hoặc** xuất hiện đề xuất nội bộ về "gói unlimited" | 2 | 3 | **6** | Mô hình 3 tầng đã chốt (CF-2.1 `[CHỐT]`): tầng 1 **$4–8/tháng không có image gen** (CF-2.2), tầng 2 credit pack không hết hạn cho user <125 ảnh (CF-2.3), tầng 3 **BYOK là tùy chọn mở khoá** (CF-2.4). **Hard quota cưỡng chế TRƯỚC khi enqueue** (CF-8.11b) — không phải cảnh báo sau | Người dùng ở đúng ranh giới ~125 (bản thân ngưỡng là `[TC]` từ vendor blog) vẫn có thể lỗ; ngưỡng cần đo lại bằng dữ liệu thật | mitigating | `product-owner` |
| **R-08** | Kinh tế | **$12,06/chapter là SÀN, không phải trần** (CF-3.5 `[EM tính từ OFF]`) — **chưa tính VLM call để score 3 candidate**. Mọi mô hình tài chính dựng trên con số này đang lạc quan một khoản chưa biết độ lớn | Hoá đơn MVP0 vượt **~$12** `[EM tính từ OFF]` (CF-3.11, đã lấy giá standard $0.134 `[OFF]` làm trần an toàn); **hoặc** dòng chi phí VLM select xuất hiện như một khoản riêng chưa có trong mô hình | 3 | 2 | **6** | MVP0 đo **cost thực/chapter đã gồm VLM call**, thay số đo vào chỗ `[EM]`. Trước khi có số đo, mọi bảng margin phải mang chú thích *"sàn"* | Cho tới hết MVP0, mọi con số margin trong kho tài liệu đều là **cận trên của margin**, tức cận dưới của rủi ro | mitigating | `business-analyst` |
| **R-09** | Kinh tế | **GRR 23% / NRR 32%** cho AI-native band `<$50/tháng` (CF-4.6 `[OFF]` ChartMogul, ~3.500 công ty) — giữ lại chưa tới 1 trên 4 đồng doanh thu cohort sau 12 tháng. ⚠️ **Ba caveat bắt buộc đi kèm — xem khối ngay dưới bảng.** Xác nhận độc lập **cùng chiều** (không phải cùng metric): RevenueCat 10/03/2026 AI app retention 12 tháng **21,1%** vs non-AI **30,7%** (CF-4.8 `[TC]`, **KHÔNG gộp với CF-4.6**) | Cohort có ≥3 người trả tiền đầu tiên: tới tháng thứ 6 mà **<50% doanh thu cohort còn lại** `[ngưỡng nội bộ đặt tại run này]` ⇒ đang đi theo band 23%; **hoặc** tỉ lệ mua lại credit pack lần 2 thấp hơn tỉ lệ mua lần 1 quá một nửa | 2 | 3 | **6** | Credit pack **không hết hạn** (CF-2.3 `[CHỐT]`) ghi nhận doanh thu **trước** và không có churn theo nghĩa subscription. ⚠️ **Đây là lập luận cấu trúc, KHÔNG phải bằng chứng** — xem G-02 | Không có dữ liệu retention nào cho mô hình credit pack. Nếu lập luận sai, không có phương án B đã được kiểm chứng | open | `business-analyst` |
| **R-10** | Kinh tế | **Không giảm được N xuống dưới 3.** N=3 là **best-of-N mặc định cho MỌI panel**, không phải retry-on-failure (CF-3.1–3.2 `[OFF]`) — không thể lấy chất lượng của N=3 mà tính chi phí của N=2. **Mỗi bậc N giảm được là ~33% COGS** (CF-8.5) | MVP0 đo: hạ xuống N=2 làm **human-reject rate sau VLM-select** tăng vượt ngưỡng chấp nhận `[ngưỡng nội bộ đặt tại run này]` ⇒ N=3 bị khoá cứng và COGS sàn không giảm được | 2 | 2 | **4** | Đưa "N tối thiểu" thành **một trong ba chỉ số bắt buộc của MVP0** (CF-8.5). Nếu N=3 khoá cứng thì đổi đòn bẩy sang granularity render (whole-page, Analysis §9b.3) hoặc sang FLUX.2 pro **$0.03** `[OFF]` | Đổi provider để giảm giá kéo theo rủi ro chất lượng chưa đo — CANVAS đo trên setting của paper, không đo trên FLUX.2 | open | `senior-ai-engineer` |
| **R-11** | Kinh tế | **SOM năm 1 chỉ $4K–14K ARR ≈ $300–1.200 MRR, 30–80 paying user** (CF-4.4 `[EM]`) — không đủ để biện minh 6 tháng toàn thời gian của 1 dev nếu tính chi phí cơ hội. Neo thực tế: **Anifusion, solo founder, $833 MRR, có lãi, ~2 năm kể từ launch 2024, $0 marketing** (CF-4.5 `[TC]`) ⚠️ **nguồn mâu thuẫn**: nguồn khác ghi **$5.000/tháng**; giá **$9/mo** vs **€20/mo** — ghi cả hai, không chọn một | Hết Q4/2026 mà MRR nằm **dưới dải $300–1.200** `[EM]`; **hoặc** hết horizon 02/2027 mà số paying user < 30 `[EM]` | 2 | 2 | **4** | Neo kỳ vọng vào **SOM, tuyệt đối không vào TAM $14,0–18,3B** (CF-4.1 `[BCN]` — ⛔ cấm dùng làm căn cứ biện minh; CF-4.2 cho thấy đổi nhãn sang "digital comics" thì CAGR sụp còn 6,7–10,4%). Đặt kill criteria tường minh ở [MVP-Scope.md](./MVP-Scope.md) §8 | SAM $0,4M–9M ARR (CF-4.3 `[EM]`) có **3/4 thừa số là giả định** — dải rộng 22 lần, gần như không ràng buộc được gì | open | `product-owner` |
| **R-12** | Kỹ thuật | **Multi-character panel 2–3 nhân vật chưa có benchmark độc lập** (CF-6.4 `[OFF]`) — đây là **hàng load-bearing** của cả verdict khả thi. Trần đã biết: CogCanvas ID-Sim **42.33** (2 người) → **27.21** (3) → **2.67** (4) → **0.52** (5), *"near-complete failure beyond three subjects"* (CF-6.5 `[OFF]`). Thị trường corroborate: ComicInk hard-code trần **5 nhân vật**/issue, TaleAtelier **6 named characters**/project (CF-6.6 `[TC]`) | MVP0: trong 8 panel liền nhau có ≥2 nhân vật, tỉ lệ panel phải regen vì **nhầm/lẫn danh tính nhân vật** vượt ngưỡng đặt trước `[ngưỡng nội bộ đặt tại run này]`; **hoặc** bất kỳ panel nào cần **4+ nhân vật** lọt được vào panel script | 2 | 3 | **6** | **MVP0 tự đo** (CF-8.6) — biết sau 2 tuần thay vì 4 tháng. **Cứng hoá ≤3 nhân vật/panel** ở MVP2 (CF-8.8): ràng buộc ở tầng schema + validation, không phải ở tầng khuyến nghị | Truyện có cảnh đông người là chuyện thường; ép ≤3 nhân vật/panel là **giới hạn sản phẩm nhìn thấy được**, không phải chi tiết kỹ thuật ẩn | open | `senior-ai-engineer` |
| **R-13** | Kỹ thuật | **Props chỉ 4.19/5 — thấp nhất trong 4 metric của CANVAS**, cải thiện so baseline chỉ **+2,5%** (CF-6.3 `[OFF]`), trong khi character đạt **4.91/5** và background **4.88/5** (CF-6.2 `[OFF]`). Vũ khí / trang sức / vật phẩm cốt truyện là thứ độc giả truyện chữ để ý nhất | Reviewer MVP0 đánh dấu *"đồ vật/vũ khí/trang sức sai"* là lý do reject **nhiều hơn** *"nhân vật sai"*; **hoặc** Story Bible có ≥1 prop mang ý nghĩa cốt truyện mà không panel nào render đúng qua 3 candidate | 3 | 1 | **3** | Đưa prop quan trọng vào reference image như một entity riêng, không mô tả bằng chữ trong prompt. Chấp nhận sửa tay ở editor tối thiểu (CF-9.1) | Sửa tay tốn công người — mà cắt công người chính là mệnh đề bán hàng | accepted | `senior-ai-engineer` |
| **R-14** | Kỹ thuật | **Race condition ở credit ledger**: pattern *check-rồi-gọi* thay vì **HOLD trước khi enqueue** cho phép user vượt quota bằng request song song. Ràng buộc kiến trúc bắt buộc: hold reserve **3 credit/panel** (vì N=3), `CHECK (available >= 0)` ở tầng DB, hold reaper cho `expires_at` (CF-6.12) | Xuất hiện code path gọi provider **trước khi** ghi hold; **hoặc** cột `available` xuống âm dù chỉ một lần; **hoặc** job treo mà credit hold không được reaper thu hồi sau `expires_at` | 2 | 2 | **4** | Ba lớp: hold trước enqueue, constraint ở DB (lớp cuối không bypass được bằng code), reaper. Test đồng thời N request song song trên cùng tài khoản | Reaper sai chu kỳ có thể thu hồi hold của job đang chạy chậm ⇒ user mất credit oan | open | `architect` |
| **R-15** | Kỹ thuật | **Khóa thời gian `(chapter, scene)` sai âm thầm ở flashback** (Analysis §5.1): đó là *thứ tự đọc*, không phải *thứ tự sự việc xảy ra*. Hệ quả dây chuyền: **Continuity Checker sẽ "sửa" theo state sai — tự động làm hỏng đúng những panel đang đúng.** Lỗi **không crash**, chỉ corrupt dữ liệu âm thầm | Bất kỳ đường dẫn resolve state nào chứa `ORDER BY chapter_no`; **hoặc** panel hồi tưởng đầu tiên render ra trang phục/vết thương của hiện tại; **hoặc** có nhiều hơn một hàm truy vấn state trong codebase | 2 | 3 | **6** | Tách `reading_order` / `story_order` (NUMERIC sparse, bước 1000, editable), `timeline_id` có `kind` + `anchor_order`, state neo vào `Event` mức scene. **Một** hàm `resolveState(entity, at_event)` duy nhất + test guardrail cấm `ORDER BY chapter_no`. Việc này thuộc **pre-cycle 09/2026**, trước dòng code đầu tiên | Sửa sau khi có dữ liệu = migrate + rà lại toàn bộ query, vì `story_order` là giả định lan khắp mọi module | open | `architect` |
| **R-16** | Kỹ thuật | **Multi-tenancy không có trong `Request.md` một dòng nào** nhưng chiếm **15–25% effort** (CF-6.9 `[EM]`). Sản phẩm là **SaaS thương mại multi-tenant** (CF-1.1 `[CHỐT]`) ⇒ `tenant_id` phải có **từ ngày đầu** (CF-8.7), không phải thêm sau | Migration nào tạo bảng nghiệp vụ mà **không có cột `tenant_id`**; **hoặc** một query bất kỳ không scope theo tenant lọt qua review; **hoặc** xuất hiện endpoint trả dữ liệu theo `id` mà không kiểm tenant ownership | 2 | 3 | **6** | `tenant_id` NOT NULL trên mọi bảng nghiệp vụ ngay từ migration đầu; row-level scoping ở một lớp duy nhất; test rò rỉ cross-tenant nằm trong bộ test bắt buộc | ⚠️ Effort 20–25% của editor tối thiểu (CF-6.7 `[EM]`) và 50–60% của §14 đầy đủ (CF-6.8 `[EM]`) là **HAI MẪU SỐ KHÁC NHAU — cấm trừ cho nhau**; tổng effort thật chưa có con số hợp nhất | open | `architect` |
| **R-17** | Kỹ thuật | **Dựa vào cache để cứu margin là sai**: hit rate ước lượng chỉ **vài % tới ~10%** (CF-6.13 `[EM]`, `architect` tự khai là ước lượng) | Trong bất kỳ bảng tính margin nào xuất hiện dòng "tiết kiệm nhờ cache" với tỉ lệ > 10% `[EM]` mà không kèm số đo thật | 2 | 1 | **2** | Không đưa cache vào mô hình tài chính cho tới khi có hit rate đo được từ traffic thật | Con số 40–60% hay 90% từ trực giác vẫn có thể lọt vào slide/pricing nếu không ai chặn | accepted | `architect` |
| **R-18** | Thị trường/Cạnh tranh | **GlobalComix gọi $13M (25/03/2026), lead SBI US Gateway Fund + Point72, và MUA LẠI INKR** — đem về **typesetting, text detection, image cleaning**; ex-INKR CEO làm head of AI engineering; định vị **"the Figma for comics"** (CF-5.2 `[TC]` Publishers Weekly). Nguy hiểm vì **typesetting đúng là phần run trước kết luận comic-studio "phải tự build"** (Comical-JS chưa có auto-placement), và "Figma for comics" **trùng định vị** §14 `Request.md` (CF-5.3) | GlobalComix phát hành công cụ **auto-typesetting / auto-placement** công khai cho creator; **hoặc** trang pricing của họ xuất hiện tier dành cho **tác giả cá nhân** (không phải publisher); **hoặc** họ ra tính năng text-to-comic từ truyện chữ | 3 | 2 | **6** | Không cạnh tranh ở typesetting. Định vị theo **input**: comic-studio bắt đầu từ **truyện chữ dài của chính tác giả**, GlobalComix bắt đầu từ **comic đã có**. Rà trang sản phẩm của họ theo lịch mục [5](#5-lịch-rà-soát) | Họ có **$13M** `[TC]` và một đội AI; khoảng cách hai định vị có thể hẹp lại bất cứ lúc nào và comic-studio không có cách nào biết trước | open | `business-analyst` |
| **R-19** | Thị trường/Cạnh tranh | **Backlash cộng đồng khi lộ dùng AI**: Naver Webtoon bị **độc giả boycott subscription** khi đăng tác phẩm AI; **BlueLine Studio bị buộc vẽ lại** episode sau khi fan phát hiện background AI-polish (CF-5.6 `[TC]`). Cộng đồng là kênh phân phối **có rủi ro ngược** — dùng sai thì nó phản đòn, không chỉ là không hiệu quả | Một post giới thiệu sản phẩm trong cộng đồng **hoạ sĩ** nhận downvote/comment tiêu cực áp đảo; **hoặc** một user công bố tác phẩm làm bằng comic-studio và bị cộng đồng đích danh tấn công | 2 | 2 | **4** | **Positioning disclosure-first**, nhắm **tác giả truyện chữ không biết vẽ** (CF-1.5 `[CHỐT]`), **không** nhắm hoạ sĩ (CF-5.7). Bằng chứng hai chiều: Novelcrafter **220.000+ authors** `[OFF]` (cộng đồng viết chấp nhận) vs boycott (cộng đồng vẽ). Granular disclosure ở export | Ranh giới writer/artist không tuyệt đối — một tác phẩm lan ra ngoài cộng đồng viết là mất kiểm soát kênh | open | `product-owner` |
| **R-20** | Thị trường/Cạnh tranh | **Kênh launch kiểu Show HN đã chết cho ngách này**: ComicInk 30/04/2026 được **2 điểm / 2 comment** (CF-5.8 `[OFF]` HN API). Đặt cược go-to-market vào một lần launch là đặt cược vào con số 2 | Kế hoạch go-to-market xuất hiện dòng "launch trên Show HN / Product Hunt" như **kênh chính** thay vì kênh phụ | 3 | 1 | **3** | Kênh chính là **comparison-listicle SEO** — 8/8 đối thủ đều tự xuất bản trang so sánh (CF-5.9 ⚠️ `[EM]` **quan sát SERP, không phải số traffic đo được**) + Discord ngách (WEBTOON official **17.777 members**, Novelcrafter **9.825** — CF-5.10 `[TC]`) | Kênh SEO cũng chỉ dựa trên `[EM]` quan sát SERP — không có traffic thật để biết nó đáng bao nhiêu | mitigating | `product-owner` |
| **R-21** | Vận hành | **Bus factor = 1.** Đội là **1 người + AI assist, không funding, không ngân sách marketing** (CF-1.2 `[CHỐT]`). Ốm, việc gấp, hoặc mất động lực ở tháng thứ 4 là kịch bản không có phương án dự phòng nào | Hai tuần liên tiếp không có commit; **hoặc** một mốc trong [Roadmap.md](./Roadmap.md) trượt >2 tuần mà không có quyết định cắt scope kèm theo | 2 | 3 | **6** | Giữ dự án ở trạng thái **có thể bỏ dở và quay lại**: monolith (CF-9.2), tài liệu quyết định trong `docs/`, mọi ràng buộc pháp lý nằm ở tầng dữ liệu chứ không ở tầng UI (CF-9.1). Cắt scope sớm thay vì nén lịch (CF-8.13) | Không giảm được xác suất gián đoạn, chỉ giảm chi phí của nó. **Chưa ai xác nhận 6 tháng đủ cho 1 dev** (CF-8.13) | accepted | `pm` |
| **R-22** | Vận hành | **Phụ thuộc model provider + silent model drift**: Gemini 3 Pro Image / FLUX.2 pro là bên ngoài, **không đàm phán được**. Provider đổi model behind the same endpoint, đổi giá, siết Acceptable Use Policy, hoặc deprecate version — không có thông báo tương xứng. Chất lượng character consistency có thể tụt mà **không có lỗi nào được ném ra** | Golden-set 8 panel chạy lại hàng tuần cho kết quả khác đáng kể mà **không có thay đổi nào từ phía code**; **hoặc** giá/đơn vị billing của provider đổi so với **$0.134 standard / $0.067 batch** `[OFF]`; **hoặc** provider đăng thông báo deprecate version đang dùng | 2 | 3 | **6** | **Golden set + eval kit ngay từ MVP1** (CF-8.7), chạy định kỳ, lưu kết quả để so sánh theo thời gian. Pin model version tường minh trong config. Giữ FLUX.2 pro như đường thoát đã được thử ít nhất một lần | Đường thoát chưa được đo bằng chính benchmark của mình; đổi provider giữa chừng làm gãy consistency của truyện đang dở | open | `senior-ai-engineer` |
| **R-23** | Vận hành | **Onboarding BYOK có ma sát — nhưng ĐỘ LỚN KHÔNG ĐO ĐƯỢC** (CF-2.5 caveat; findings §3.2: *"không có số liệu định lượng"*). Chỉ có dấu hiệu định tính: API key là **external dependency** — hệ số nặng nhất trong công thức friction `[TC]`; *"plan an hour per provider for first-time setup"* `[TC]` ⚠️ **vendor blog của bên bán managed** ⇒ có động cơ phóng đại. Xem G-08 | Tỉ lệ user đăng ký xong nhưng **không tạo được panel đầu tiên** cao bất thường; **hoặc** support question về API key chiếm phần lớn hộp thư; **hoặc** thời gian từ signup tới panel đầu tiên vượt 30 phút cho đa số user `[ngưỡng nội bộ đặt tại run này]` | 2 | 2 | **4** | **BYOK là tùy chọn MỞ KHOÁ, không phải điều kiện để dùng sản phẩm** (CF-2.4 `[CHỐT]`) — pattern Novelcrafter: tầng $4–8 **không cần API key** (CF-2.2 `[CHỐT]`) để user vào được sản phẩm trước khi đối mặt với key | Độ lớn ma sát vẫn không đo được cho tới khi có user thật — mitigation là **cấu trúc né**, không phải giải | mitigating | `product-owner` |

> [!WARNING]
> **Ba caveat bắt buộc của con số 23% ở R-09** (CF-4.7 `[OFF]`) — không được tách khỏi con số:
> - **(a)** cohort AI-native chỉ khoảng **~200 công ty**; **n của riêng band `<$50` không được công bố**.
> - **(b)** dữ liệu lọc **≥$250K ARR** ⇒ **loại đúng nhóm indie mà comic-studio thuộc về**. Con số mô tả một nhóm mà comic-studio không nằm trong.
> - **(c)** dữ liệu **2025**, không phải 2026.
>
> ⇒ 23% là **tín hiệu về hướng**, không phải dự báo cho comic-studio. Dùng nó để thiết kế mô hình doanh thu, **không** dùng nó để dự phóng số.

### 2.2 Rủi ro NỀN TẢNG — một hàng riêng, khác loại

> [!IMPORTANT]
> Hàng dưới đây **không cùng loại** với R-18 (rủi ro đối thủ). Đối thủ cạnh tranh **trong cùng thị trường**; một **platform** kiểm soát **kênh phân phối** của thị trường đó. Nếu platform lớn nhất phát công cụ tương đương **miễn phí**, kênh phân phối tự nhiên nhất bị chặn **ở cửa** — không phải thua ở tính năng hay giá.
>
> **Không gán Score** vì trạng thái của chính rủi ro chưa xác nhận được (CF-5.4 → mục [4, G-03](#41-năm-khoảng-trống--không-gán-score)). Gán một xác suất ở đây là bịa.

| ID | Category | Risk Description | Trigger (dấu hiệu quan sát được) | Probability | Impact | Score | Mitigation Plan | Residual Risk | Status | Owner |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- | :--- | :--- |
| **RP-01** | Thị trường/Cạnh tranh (**nền tảng**) | **Constella của WEBTOON**: convert 3D character model → 2D **theo đúng nét vẽ của chính creator**, **miễn phí cho creator của platform**, rollout professional trước (CF-5.4 `[TC]` ⚠️ **fetch nguồn fail — chưa xác nhận đã ship hay còn là announcement**). Khác loại vì đây là chủ sở hữu kênh, không phải người cùng xếp hàng trong kênh. **Nhưng**: Constella nhắm creator **đã biết vẽ** (cần 3D model của chính họ), comic-studio nhắm tác giả **không biết vẽ** (CF-1.5 `[CHỐT]`) — hai phân khúc, và khoảng cách **có thể** hẹp lại (CF-5.5) | WEBTOON công bố Constella **GA** cho creator (không còn giới hạn professional); **hoặc** Constella mở rộng từ *3D model của chính creator* sang **text/mô tả → nhân vật** — thời điểm đó hai phân khúc chập làm một; **hoặc** WEBTOON mở Constella cho creator **không có tác phẩm trên platform** | **không gán được** — xem [G-03](#41-năm-khoảng-trống--không-gán-score) | **không gán được** | **—** | Không mitigate được bằng kỹ thuật. Việc duy nhất làm được: **theo dõi định kỳ** và giữ định vị ở phân khúc *không biết vẽ*. Nếu trigger nổ ⇒ đây là input cho **kill criteria** ở [MVP-Scope.md](./MVP-Scope.md) §8, không phải cho một sprint mitigation | Toàn bộ. Đây là loại rủi ro chỉ quan sát được, không giảm được | open | `business-analyst` |

---

## 3. Rủi ro nhị phân — tách riêng

> [!CAUTION]
> **RB-01 không phải một hàng trong bảng ở mục 2, và cố ý không có Score.**
>
> Lý do (CF-7.9): **mọi rủi ro khác trả lời sai thì sản phẩm KÉM HƠN — rủi ro này trả lời sai thì sản phẩm BẤT HỢP PHÁP.** Một rủi ro nhị phân chưa kiểm luôn phải xếp trên mọi rủi ro liên tục, bất kể Score của chúng là bao nhiêu. Nhân một xác suất **chưa ai biết** với một impact **không phải "làm lại một phần" mà là "không tồn tại"** cho ra một con số trông giống dữ liệu nhưng không mang thông tin.

### RB-01 — Ba câu hỏi phải mang tới luật sư SHTT Việt Nam TRƯỚC khi thương mại hoá

**Đây là khuyến nghị hành động số 1 của toàn bộ quá trình thẩm định** (CF-7.8). Ba câu đã được narrow xuống mức luật sư trả lời được:

| # | Câu hỏi | Vì sao chưa tự trả lời được |
|---|---|---|
| **1** | **Điều 37a NĐ 134/2026 có áp cho _inference-time extraction_ trên nội dung do user upload, hay chỉ áp cho _huấn luyện_ model?** Điều 37a giới hạn TDM ở *"non-commercial purposes at the point of use"* (CF-7.4) — mà comic-studio là **SaaS thương mại** (CF-1.1 `[CHỐT]`) | Cả 37a/37b/37c đóng khung quanh **"huấn luyện"**; comic-studio không tạo model mới, không lưu nội dung vào weights, xử lý theo chỉ dẫn của chính người upload ⇒ **có lập luận mạnh rằng 37a không áp**. Nhưng đây là vùng **chưa có tiền lệ**, và ⚠️ **văn bản điều luật hiện chỉ đọc được qua BẢN TÓM TẮT, không phải nguyên văn** (nguồn 403 / paywall) — xem [G-01](#41-năm-khoảng-trống--không-gán-score) |
| **2** | **Khoản 4 Điều 11 Luật TTNT 2025 — nghĩa vụ đánh dấu định dạng máy đọc áp cho _mọi_ nội dung AI, hay chỉ nội dung _"mô phỏng người thật hoặc sự kiện thực tế"_? SynthID của model provider có thoả nghĩa vụ này không?** | **Hai nguồn mô tả phạm vi khác nhau** (CF-7.7 `[OFF]`) và không đọc được nguyên văn. Chênh lệch phạm vi quyết định việc này là *một dòng metadata* hay *một hạng mục kỹ thuật ở export path* |
| **3** | **Nền tảng có được coi là "doanh nghiệp cung cấp dịch vụ trung gian" để hưởng miễn trừ Điều 198b không**, khi nó không chỉ **lưu trữ** mà còn **xử lý/biến đổi** nội dung của user? (tương đương ở luật Mỹ: DMCA §512(c) có phủ "hosting + AI processing"?) | NĐ 17 chỉ nói rõ về *"lưu trữ nội dung số theo yêu cầu"*. **Hosting thuần có safe harbour rõ; "hosting + processing" là vùng chưa test.** Đây là điều kiện tiên quyết của R-02 |

**Quy tắc quyết định — cứng:**

| Trạng thái RB-01 | Được làm | Không được làm |
|---|---|---|
| **Chưa engage luật sư** | MVP0 → MVP1 với **dữ liệu của chính anh** (CF-8.4–8.7). Xây đủ hồ sơ provenance (R-01) và checklist 198b (R-02) | Mở cho **người ngoài upload**; thu **bất kỳ khoản tiền nào** |
| **Đã hỏi, câu 1 trả lời "37a KHÔNG áp"** | Tiến tới thương mại hoá theo [MVP-Scope.md](./MVP-Scope.md) gate G0 | — |
| **Đã hỏi, câu 1 trả lời "37a CÓ áp"** | — | **Dừng thương mại hoá mô hình user-upload.** Đây là nhánh cần thiết kế lại từ gốc, không phải nhánh cần patch |

> **Chi phí một buổi tư vấn luật sư SHTT thấp hơn nhiều bậc độ lớn so với chi phí build sai rồi phải dỡ.** Và đặc biệt: R-01 (provenance) **không backfill được** — nghĩa là *"cứ build đi, xong rồi tính"* không phải một lựa chọn trung lập, nó là một lựa chọn có chi phí chìm.
>
> ⚠️ G0 (pháp lý) **chặn thương mại hoá nhưng KHÔNG chặn MVP0–MVP1** — xem [Roadmap.md](./Roadmap.md) §6. "Chờ luật sư mới được code" là cách hiểu sai.

---

## 4. Rủi ro đã biết là KHOẢNG TRỐNG

> [!IMPORTANT]
> Mục này tồn tại vì một lý do duy nhất: **gán một Score cho thứ chưa đo được là biến "không biết" thành "đã đánh giá".** Đó là loại sai tệ nhất trong tài liệu rủi ro — nó không làm anh sai, nó làm anh **tưởng mình đã biết**.
>
> Các mục dưới đây **không có Probability, không có Impact, không có Score**. Thay vào đó mỗi mục có: *chưa đo được cái gì* và *cái gì đóng được khoảng trống*.

### 4.1 Năm khoảng trống — không gán Score

| ID | Nguồn CF | Chưa đo được cái gì | Vì sao chưa đo được | Cái gì đóng được khoảng trống |
| :--- | :--- | :--- | :--- | :--- |
| **G-01** | **CF-7.4** | **Điều 37a có thực sự giới hạn TDM ở *"non-commercial purposes at the point of use"* theo đúng nghĩa đó không** — và nó có áp cho inference-time extraction không | ⚠️ **Chỉ có BẢN TÓM TẮT, KHÔNG PHẢI NGUYÊN VĂN.** thuvienphapluat/nhansu trả **403**, IAPP **paywall**. Không thể đọc câu chữ thật của điều luật | **Luật sư SHTT Việt Nam** (RB-01 câu 1) — đây là cách duy nhất. Không có lượng công sức tra cứu nào thay thế được |
| **G-02** | **CF-4.9** | **Liệu credit pack không hết hạn có thực sự né được GRR 23%** hay không | ⚠️ Đây là **lập luận logic** (doanh thu ghi nhận trước ⇒ không có churn theo nghĩa subscription), **KHÔNG PHẢI SỐ ĐO** `[EM]`. **Không tìm được dữ liệu retention nào cho mô hình credit pack** trong toàn bộ quá trình nghiên cứu | Cohort trả tiền đầu tiên của chính comic-studio: đo **tỉ lệ mua lại credit pack lần 2, lần 3** theo tháng. Không có đường tắt qua benchmark ngành vì benchmark không tồn tại |
| **G-03** | **CF-5.4** | **Constella đã ship hay còn là announcement**, và phạm vi rollout thực tế tới đâu | ⚠️ **Fetch nguồn FAIL.** Chỉ có mô tả thứ cấp `[TC]`. Không xác nhận được trạng thái sản phẩm | Theo dõi trực tiếp trang creator của WEBTOON theo lịch mục [5](#5-lịch-rà-soát). Đây là khoảng trống **đóng được bằng quan sát**, khác với G-01/G-02 |
| **G-04** | **CF-6.10** | **Tỉ lệ lỗi thật của speaker attribution.** Con số đang lưu hành — **30–50%** (3+ người) / **40–60%** (câu ngắn) — ⚠️ là `[EM]` **ước lượng, KHÔNG PHẢI SỐ ĐO** | Không có benchmark nào đo speaker attribution trên văn bản truyện chữ tiếng Việt ở cấu hình này. Con số được suy ra, không được đo | **MVP0/MVP1 tự đo** trên chính truyện của anh. Cho tới lúc đó, MVP2 giữ **human gate bắt buộc cho speaker attribution** (CF-8.8) — thiết kế như thể tỉ lệ lỗi ở cận trên |
| **G-05** | **CF-6.11** | **Độ phủ thật của Continuity Checker.** Con số **40–60% số panel** ⚠️ là `[EM]`, không phải số đo | Suy ra từ giới hạn của re-identification trên art cách điệu, không từ một lần chạy có đối chứng | **MVP0 đo human-reject rate sau VLM-select** (CF-8.5 — ⭐ *"chưa ai công bố con số này"*). Cho tới lúc đó: **phải nói rõ với user** rằng checker không phủ toàn bộ panel — để họ hiểu nhầm là được bảo vệ toàn diện thì tệ hơn không có checker |

### 4.2 Khoảng trống nằm BÊN TRONG một rủi ro đã được Score

> Khác với 4.1: các rủi ro dưới đây **đã có Score** vì bản thân sự tồn tại của rủi ro là quan sát được. Cái chưa đo được là **độ lớn**. Ghi lại để Score không bị đọc như một con số chắc chắn.

| ID | Gắn với | Cái chưa đo được |
| :--- | :--- | :--- |
| **G-06** | R-03 | **Phạm vi nghĩa vụ Luật TTNT 2025**: hai nguồn mô tả khác nhau (chỉ *"mô phỏng người thật"* vs **mọi** nội dung AI) — CF-7.7 `[OFF]`. Deadline **~01/03/2027** thì rõ; nội dung phải làm thì chưa |
| **G-07** | R-08, R-10 | **Số ảnh/chapter = 60** (15 page × 4 panel) ⚠️ là `[EM]` — **giả định của `researcher` run trước, KHÔNG PHẢI SỐ ĐO** (CF-3.3). Mọi con số chi phí/chapter, gồm cả **$12,06** `[EM tính từ OFF]`, kế thừa giả định này |
| **G-08** | R-23 | **Độ lớn ma sát onboarding BYOK**: findings §3.2 ghi thẳng *"KHÔNG CÓ SỐ LIỆU ĐỊNH LƯỢNG"*. Ngưỡng **~125 ảnh/tháng** (CF-2.5 `[TC]`) đến từ **vendor blog của bên bán managed** — được chấp nhận vì khuyến nghị **ngược chiều lợi ích của họ**, nhưng vẫn không phải số đo của comic-studio |
| **G-09** | R-11 | **Mâu thuẫn nguồn về Anifusion** (CF-4.5 `[TC]`): **$833 MRR** vs **$5.000/tháng**; giá **$9/mo** vs **€20/mo**. Neo của SOM `[EM]` chênh nhau **~6 lần** tuỳ chọn nguồn nào ⇒ **ghi cả hai, không chọn một** |
| **G-10** | R-17 | **Cache hit rate vài % tới ~10%** (CF-6.13) là `[EM]` do `architect` **tự khai là ước lượng** — chưa có traffic thật để đo |

---

## 5. Lịch rà soát

Ba gate G0/G1/G2 do [MVP-Scope.md](./MVP-Scope.md) §7 định nghĩa. Mục này chỉ trả lời: **rủi ro nào rà ở gate nào.**

### 5.1 Ánh xạ rủi ro → gate

| Gate | Thời điểm | Rủi ro / khoảng trống rà tại đây | Câu hỏi phải trả lời được khi rời gate |
| :--- | :--- | :--- | :--- |
| **G0 — Pháp lý** | Trước dòng code **thương mại** đầu tiên | **RB-01** · **G-01** · R-02 · R-03 · R-04 · R-05 · R-06 | Ba câu của RB-01 đã có câu trả lời từ luật sư SHTT VN, và **không câu nào chặn mô hình user-upload thương mại**. Checklist 198b (R-02) đã tick đủ 6 mục |
| **G1 — Kỹ thuật** (sau MVP0) | Cuối **09/2026** | R-08 · R-10 · R-12 · R-13 · R-15 · **G-04** · **G-05** · **G-07** | Ba chỉ số CF-8.5 có số thật; **multi-character 2–3 nhân vật** (R-12) có kết luận; cost thực/chapter đã gồm VLM call (R-08); số ảnh/chapter thật thay được cho giả định 60 `[EM]` |
| **G2 — Kinh tế** (sau MVP1) | Cuối **Q4/2026** | R-07 · R-09 · R-11 · R-16 · R-23 · **G-02** · **G-08** | Regen ratio p50/p90 đo được cho phép mô hình 3 tầng giữ margin trong dải **50–60%** `[BCN]` (CF-3.10); tỉ lệ mua lại credit pack lần 2 có số đầu tiên |

### 5.2 Rủi ro không chờ gate

| Nhịp | Rủi ro | Vì sao không chờ gate |
| :--- | :--- | :--- |
| **Tại PR/migration đầu tiên chạm schema** | **R-01** · R-14 · R-15 · R-16 | ⚠️ **R-01 không backfill được.** Kiểm ở gate là kiểm quá muộn — tới lúc đó dữ liệu thiếu hồ sơ đã tồn tại. Bốn rủi ro này đều là quyết định schema: sửa trước khi có dữ liệu thì rẻ, sau thì là migrate |
| **Hàng tuần** | R-22 | Golden-set eval chạy hàng tuần là cách **duy nhất** phát hiện silent model drift — theo định nghĩa nó không ném lỗi |
| **Hàng tháng** | R-18 · **RP-01 / G-03** · R-19 · R-20 | Rủi ro thị trường và nền tảng thay đổi theo nhịp của bên ngoài, không theo nhịp gate của dự án. **RP-01 chỉ quan sát được, không mitigate được** ⇒ tần suất quan sát chính là toàn bộ biện pháp |
| **Liên tục** | R-21 | Bus factor = 1 không có gate nào đóng được; dấu hiệu (2 tuần không commit) chỉ có ý nghĩa nếu được nhìn liên tục |
| **Khi có user trả tiền đầu tiên** | R-09 · R-23 · G-02 · G-08 | Ba khoảng trống retention/friction **chỉ đóng được bằng dữ liệu của chính mình** — không có benchmark ngành nào thay thế |

### 5.3 Quy tắc cập nhật tài liệu này

1. **Mỗi lần rà: cập nhật `Status` và `updated`**, không xoá hàng. Rủi ro `closed` giữ lại như dấu vết quyết định.
2. **Rủi ro mới phát sinh từ MVP0/MVP1**: thêm hàng, ID tiếp tục từ **R-24**.
3. **Khi một khoảng trống ở mục 4 được đóng bằng SỐ ĐO**: chuyển nó thành một hàng có Score ở mục 2, và ghi rõ số đo đến từ đâu. **Chỉ số đo mới được đổi chỗ — một lập luận thuyết phục hơn thì không.**
4. **Không hàng nào được để `Trigger` rỗng.** Một rủi ro không có dấu hiệu nhận biết là một rủi ro không quản lý được, chỉ là một nỗi lo được ghi ra giấy.

---

## Tài liệu liên quan

- [MVP-Scope.md](./MVP-Scope.md) — định nghĩa ba gate G0/G1/G2 và kill criteria
- [Charter-Comic-Studio.md](./Charter-Comic-Studio.md) — ràng buộc và giả định cấp dự án
- [Roadmap.md](./Roadmap.md) — mốc thời gian, phụ thuộc và đường găng
- [OKRs.md](./OKRs.md) — mục tiêu chu kỳ và anti-goals
- [Analysis-Comic-Studio-Concept.md](../050-Research/Analysis-Comic-Studio-Concept.md) — §5 (bảy vấn đề phải sửa trước khi viết code), §8 (rủi ro pháp lý & compliance), §9b (unit economics)
- [outline.md — bảng CANONICAL FACTS CF-1 → CF-9](./pm-runs/2026-08-23-khoi-tao-tai-lieu-planning-comic-studio/outline.md)
- [findings/researcher.md](./pm-runs/2026-08-23-khoi-tao-tai-lieu-planning-comic-studio/findings/researcher.md) — rủi ro thị trường, retention, BYOK

---

*Generated by TNMCORE-OS — role `security-auditor`.*
