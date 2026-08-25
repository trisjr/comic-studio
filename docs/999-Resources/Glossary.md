---
id: GLOSSARY-001
type: glossary
status: live
created: 2026-02-04
updated: 2026-08-24
---

# Glossary (Từ điển Thuật ngữ)

## Mục lục

- [Xác thực & bảo mật](#xác-thực--bảo-mật)
- [Kiến trúc pipeline comic-studio](#kiến-trúc-pipeline-comic-studio)
- [Mô hình dữ liệu & thời gian](#mô-hình-dữ-liệu--thời-gian)
- [Sinh ảnh & kiểm tra nhất quán](#sinh-ảnh--kiểm-tra-nhất-quán)
- [Chữ & trình bày](#chữ--trình-bày)
- [Quy trình & vận hành](#quy-trình--vận-hành)
- [SaaS & multi-tenancy](#saas--multi-tenancy)
- [Planning, thị trường & quản trị](#planning-thị-trường--quản-trị)
- [Requirements & tài liệu hoá](#requirements--tài-liệu-hoá)
- [Backlog & Story engineering](#backlog--story-engineering)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## Xác thực & bảo mật

- **OTP (One-Time Password)**: Mật khẩu sử dụng một lần để xác thực người dùng.
- **OTP Expiry**: Thời gian hết hạn của mã OTP kể từ khi được tạo.
- **Rate Limit**: Cơ chế giới hạn số lượng yêu cầu (ví dụ: gửi OTP) trong một khoảng thời gian nhất định để bảo mật.

---

## Kiến trúc pipeline comic-studio

- **Story Bible**: Cơ sở dữ liệu trạng thái có cấu trúc của một tác phẩm — nhân vật, quan hệ, địa điểm, vật phẩm, sự kiện — được rút ra từ văn bản gốc và **truy vấn được theo thời điểm**. Phân biệt rõ với một bản tóm tắt văn xuôi: Story Bible là **dữ liệu**, không phải prose. Đây là tài sản tích luỹ theo thời gian của người dùng, nên cũng là switching cost và là ứng viên moat thật.
- **Comic IR (Comic Intermediate Representation)**: Tầng biểu diễn trung gian giữa văn bản gốc và ảnh — mô tả cấu trúc truyện tranh (trang, panel, nhân vật có mặt, hành động, thoại) dưới dạng dữ liệu có schema, **trước khi** bất kỳ ảnh nào được sinh. Luôn viết cả dạng đầy đủ ở lần dùng đầu tiên trong mỗi tài liệu.
- **Panel Specification**: Đơn vị dữ liệu mô tả đầy đủ một panel (bố cục, nhân vật, camera, ràng buộc thị giác, vùng an toàn cho chữ). Là *"dữ liệu chính"* của hệ thống — ảnh là output phái sinh, spec là thứ được lưu và sửa. Một trang có thể compile nhiều panel spec thành **một** prompt whole-page.
- **Visual Prompt Compiler**: Thành phần biến `Panel Specification` thành prompt cho model sinh ảnh. **Phải là code deterministic**, không phải LLM: bản chất là tra bảng `field value → cụm từ`, sắp thứ tự, dedup, xử lý xung đột theo precedence ladder, thực thi constraint budget và ghi log ràng buộc bị drop.
- **Layout Director**: Thành phần quyết định bố cục trang — panel nào lớn, panel nào nhỏ, thứ tự đọc. Cùng với Comic IR, output của nó là phần **được bảo hộ bản quyền** theo tiền lệ Zarya of the Dawn.
- **Precedence ladder**: Thang ưu tiên các ràng buộc thị giác trong compiler, dùng khi phải drop ràng buộc do vượt constraint budget. Identity refs ở bậc cao nhất (không bao giờ bị drop); camera angle / composition / props phụ bị drop đầu tiên.
- **Constraint budget**: Trần số ràng buộc thị giác mà một model thực sự tôn trọng đồng thời (ước lượng 5–8). Vượt trần thì thêm ràng buộc **làm giảm** chất lượng do instruction dilution, chứ không tăng.

---

## Mô hình dữ liệu & thời gian

- **syuzhet vs fabula**: Hai trục thời gian của một tác phẩm tự sự. **syuzhet** = thứ tự **người đọc gặp** sự kiện (`reading_order`); **fabula** = thứ tự sự kiện **thực sự xảy ra** trong thế giới truyện (`story_order`). Thuật ngữ lý thuyết văn học, không phải thuật ngữ kỹ thuật — nhưng bỏ qua nó là nguồn của lỗi mô hình dữ liệu nghiêm trọng nhất: dùng `(chapter, scene)` làm khoá thời gian sẽ sai âm thầm ở mọi flashback.
- **`timeline_id`**: Định danh nhánh thời gian, cho phép một tác phẩm có nhiều dòng thời gian song song (hồi tưởng, giấc mơ, tuyến phụ) mà không làm hỏng phép reduce trạng thái.
- **Identity vs Appearance**: Trục phân tách cốt lõi. **Identity** = cái làm một nhân vật là chính nhân vật đó, bất biến qua các chương (cấu trúc khuôn mặt, dấu hiệu nhận dạng). **Appearance** = cái thay đổi theo trạng thái (trang phục, vết thương, tóc). Gộp hai thứ này vào một field là nguyên nhân của phần lớn lỗi consistency.
- **Canonical Reference / Character Reference Sheet**: Bộ ảnh tham chiếu chuẩn của một nhân vật, dùng làm điều kiện đầu vào cho mọi lần sinh ảnh có nhân vật đó — chứ không chỉ mô tả bằng text prompt.
- **`Generation` / `parent_generation`**: Bảng và trường lưu **lineage** của từng lần sinh ảnh: prompt nào, input nào, ảnh nào là gốc của ảnh nào. Không chỉ là tiện lợi sản phẩm — theo NĐ 134/2026/NĐ-CP Điều 5a đây là **hồ sơ pháp lý bắt buộc** để chứng minh *"đóng góp trí tuệ đáng kể và mang tính quyết định"* của con người.
- **`field_provenance` / `change_log`**: Vết ghi lại **quyết định của con người** trên từng field — ai sửa gì, khi nào. Là phương tiện thoả nghĩa vụ "iterative, interactive process"; nghĩa vụ này nằm ở **tầng dữ liệu**, không phải ở công nghệ render UI.
- **attribute binding**: Việc model gắn đúng thuộc tính (trang phục, vật phẩm) cho đúng nhân vật trong panel nhiều người. Thất bại gần hoàn toàn từ 4 nhân vật trở lên — ảnh trông hợp lý nhưng gắn sai áo cho sai người.

---

## Sinh ảnh & kiểm tra nhất quán

- **best-of-N (N=3)**: Sinh **N phương án** cho mỗi panel rồi chọn cái tốt nhất. **Phân biệt tuyệt đối với retry-on-failure**: best-of-N chạy trên **mọi** panel như mặc định, không phải chỉ khi panel lỗi. Đây là setting mà CANVAS dùng để đạt điểm character 4.91/5, và paper ghi *"Performance saturates at N=3"*. Nhầm hai khái niệm này là nguồn của sai số chi phí **+50%**.
- **Continuity Checker**: Thành phần kiểm nhất quán xuyên panel. ⚠️ **Định nghĩa đã được sửa lại**: không phải "gắn nhãn ✓/✗ từng attribute rồi autofix" (cơ chế này chưa được validate và có FP profile xấu), mà là **QA-based selection giữa N candidate** — trả lời câu *"trong N cái này, cái nào consistent hơn"* thay vì *"panel này đúng hay sai"*. Mọi tài liệu mới phải dùng nghĩa sau.
- **re-identification**: Bài toán xác định *"nhân vật nào trong panel này là nhân vật X"*. Là lý do panel nhiều nhân vật về cơ bản không kiểm được bằng checker: muốn kiểm trang phục của X thì trước tiên phải giải re-identification — chính bài toán mà checker được lập ra để giải. Một vòng lặp logic.
- **Layout Score**: Điểm đánh giá bố cục trang. ⚠️ Cơ chế **số thực đã bị cắt** (không đo được, không calibrate được, tạo cảm giác chính xác giả); thay bằng **rubric rời rạc + emphasis quota**. Mục tiêu giữ, cơ chế bỏ.
- **VLM autorater**: Vision-Language Model dùng để đánh giá ảnh thay người. Đã được validate ở **pairwise ranking** (MIE đạt 0.922 accuracy so với human preference), **chưa** được validate ở absolute per-panel detection.
- **Error cascade**: Đặc tính lỗi **nhân, không cộng** qua các tầng pipeline. 5 tầng mỗi tầng đúng 90% → end-to-end ≈ 59%. Muốn end-to-end 90% thì mỗi tầng phải ≈ 98% — mức mà không tầng LLM nào đạt zero-shot. Cách duy nhất thắng phép nhân này là chuyển vài tầng lên **100%** bằng code deterministic.

---

## Chữ & trình bày

- **typeset layer**: Tầng chữ **tách khỏi ảnh**, không nướng vào pixel. Ảnh được sinh không có chữ (`text, letters, watermark, speech bubble` vào negative prompt), bubble và thoại render bằng code lên trên. Không có tầng này thì sửa một câu thoại = một lần regenerate ảnh.
- **`text_safe_zone`**: Vùng trong panel được giữ trống để đặt bubble, khai báo ngay trong `Panel Specification`. Thiếu nó thì bubble che mặt nhân vật và phải sinh lại toàn bộ ảnh đã làm.
- **dialogue condensation**: Bước nén thoại gốc (thường 30–80 từ với web-novel dịch) xuống mức bubble đọc thoải mái (~8–20 từ), tức hệ số **2–5×**. Là **hành vi biên tập có mất** ⇒ cần LLM **và** cần người review. Phải chạy **sau** layout, vì `text_budget` phụ thuộc diện tích panel.
- **speaker attribution**: Việc gán mỗi dòng thoại cho đúng nhân vật nói. Lỗi ước lượng 30–50% (3+ người có tự sự chen) và 40–60% (câu ngắn / thán từ) nếu không có anchor + constrained decoding. Chi phí lỗi **bất đối xứng** — một dòng gán sai làm hỏng cả trang trong mắt người đọc.

---

## Quy trình & vận hành

- **HITL gate (Human-in-the-loop gate)**: Điểm trong pipeline bắt buộc có người xác nhận trước khi đi tiếp. Đơn vị đo của nó là **giờ-người**, không phải token — và với một người làm một mình, đây mới là ràng buộc thật, không phải chi phí API.
- **human gate**: Cách gọi cụ thể — trong `UC-04`/`UC-05` và `Roadmap` exit criterion **M2-4** — cho **hai HITL gate bắt buộc, không bypass được** của luồng chữ: xác nhận **speaker attribution** và xác nhận **dialogue condensation**. Quan hệ với `HITL gate`: `HITL gate` là khái niệm **chung** (mọi điểm cần người xác nhận); `human gate` là **hai thực thể cụ thể** của khái niệm đó, với ràng buộc riêng là *"không tồn tại đường code nào xuất bản page mà chưa qua cả hai"* — không phải mọi HITL gate trong hệ thống đều là human gate theo nghĩa hẹp này.
- **MVP0**: Vertical slice **trước** MVP1 — một chapter duy nhất, Story Bible và panel script viết tay, chỉ code đúng một việc (sinh panel với reference + N candidate + VLM select). Mục đích **không** phải có sản phẩm mà để biết tiền đề còn đứng, sau 1–2 tuần thay vì sau 4 tháng. Một tên duy nhất cho khái niệm này — không dùng "phase 0", "spike", "PoC".
- **vertical slice**: Một lát cắt xuyên hết mọi tầng của hệ thống ở phạm vi nhỏ nhất, đối lập với làm xong từng tầng theo chiều ngang. Dùng để kiểm tiền đề rủi ro nhất trước.
- **eval kit**: Bộ dữ liệu và script đo chất lượng output, có từ sớm để mọi thay đổi sau đó đo được. Thuộc MVP1, không phải MVP4.
- **preference data**: Nhãn thu được mỗi lần người dùng chấp nhận/từ chối một gợi ý. Là nguồn duy nhất cho eval của tầng thẩm mỹ, và là nguyên liệu của moat thật.

---

## SaaS & multi-tenancy

- **`tenant_id`**: Định danh khách hàng. Phải là **cột đầu tiên** của mọi composite index, `NOT NULL`, có từ ngày đầu. Thêm sau là một cuộc migration xuyên toàn bộ schema.
- **RLS (Row-Level Security)**: Cơ chế Postgres chặn truy cập ở tầng DB theo hàng, thay vì tin vào điều kiện `WHERE` của tầng ứng dụng. Với một dev không có code review, đây là **bảo hiểm rẻ nhất tồn tại**. ⚠️ Giới hạn: RLS **không** bảo vệ được join thực hiện phía application — đó là lý do tách 2 database làm mất lớp phòng thủ này.
- **BYOK (Bring Your Own Key)**: Người dùng tự cung cấp API key của model provider. Xoá hoàn toàn rủi ro COGS và làm biến mất xung đột giữa tính năng cốt lõi và margin. ⚠️ Đánh đổi: friction cao với người dùng non-technical ⇒ onboarding flow trở thành rủi ro sản phẩm số 1.
- **credit ledger + hold**: Sổ tín dụng có cơ chế **reserve trước khi enqueue**. Check-rồi-gọi là race condition: 10 job đồng thời đều thấy đủ số dư. Với best-of-N thì hold phải reserve **3 credit/panel**, không phải 1.
- **hold reaper**: Job dọn các hold quá hạn (`expires_at`). Thiếu nó là rỉ chậm thành *"có credit mà không generate được"* — loại lỗi khó chẩn đoán nhất.
- **`usage_event`**: Bảng append-only ghi mọi lần tiêu tài nguyên. Append-only là điều kiện để nó dùng được làm căn cứ đối soát.
- **seam kinh tế vs seam kỹ thuật**: Đường cắt hệ thống theo **chi phí và fairness** (worker process riêng, fairness per-tenant khi claim job, `usage_event` tách bạch) khác với đường cắt theo **module kỹ thuật** (microservices). Với một dev, seam kinh tế đáng làm; seam kỹ thuật thì không.
- **GRR (Gross Revenue Retention)**: Tỉ lệ giữ doanh thu, chưa tính upsell. Ở phân khúc AI-native band `<$50/tháng`, con số đo được là **23%** (NRR 32%) `[OFF]` — ChartMogul, ~3.500 công ty, dữ liệu **2025** — thấp tới mức làm subscription trở thành mô hình sai với một dev không có ngân sách marketing.
  > ⚠️ **Ba caveat bắt buộc đi kèm con số 23%, trích nó mà bỏ ba dòng này là trích sai:** (a) cohort AI-native chỉ **~200 công ty** và band `<$50` là một tập con, **n của riêng band không được công bố**; (b) bộ lọc **≥$250K ARR loại bỏ toàn bộ quy mô indie** — tức loại đúng nhóm `comic-studio` thuộc về; (c) đây là **dữ liệu 2025**. Kết luận chịu lực không phải *"AI churn"* mà là **giá**: cùng dataset, sản phẩm AI trên $250/tháng đạt GRR **70%**. Chi tiết: [Analysis-Market-Competitor-Landscape §5.1](../050-Research/Analysis-Market-Competitor-Landscape.md#51-23-grr--chartmogul-và-ba-caveat-bắt-buộc).

---

## Planning, thị trường & quản trị

*Nhóm này được bổ sung ở run `2026-08-23-khoi-tao-tai-lieu-planning-comic-studio`, khi tầng 010-Planning được khởi tạo.*

- **TAM / SAM / SOM**: Ba tầng quy mô thị trường. **TAM** = toàn bộ thị trường; **SAM** = phần thị trường sản phẩm thực sự phục vụ được; **SOM** = phần thực tế chiếm được. ⚠️ Với `comic-studio`, ba con số này chênh nhau **3–4 bậc độ lớn** vì TAM webtoon đo **tiêu thụ nội dung** còn sản phẩm bán **công cụ cho tác giả**. Dùng TAM để biện minh cho một dự án bán công cụ là **lỗi logic**, không phải sự lạc quan.
- **NRR (Net Revenue Retention)**: Tỉ lệ giữ doanh thu **đã tính** upsell/expansion. Khác **GRR** ở chỗ NRR có thể vượt 100%, GRR thì không.
- **payer retention**: Tỉ lệ người trả tiền còn ở lại sau một khoảng thời gian. ⚠️ **KHÔNG phải GRR** — GRR đo *đồng doanh thu*, payer retention đo *đầu người*. Hai metric này không cộng, không lấy trung bình, không so trực tiếp; gộp chúng là một lỗi đọc số phổ biến.
- **RACI**: Ma trận phân vai — **R**esponsible (người làm) · **A**ccountable (người chịu trách nhiệm cuối, chỉ một) · **C**onsulted (được hỏi ý kiến) · **I**nformed (được thông báo). ⚠️ Với đội một người, RACI dễ suy biến thành "Founder ở mọi ô" — khi đó giá trị của nó nằm ở việc **nêu thẳng lỗ hổng** (bus factor = 1, vai trò C không tồn tại) chứ không ở bảng.
- **OKR / Objective / Key Result**: **Objective** định tính, mô tả thành công trông như thế nào; **Key Result** định lượng, có số + cách đo + tần suất đo. Một Objective là con số thì đó là KR bị đặt sai chỗ.
- **anti-goal**: Điều **cố ý không làm** trong một chu kỳ, kèm lý do. Khác với "chưa ưu tiên" — anti-goal là quyết định đã cân nhắc, ghi ra để không ai âm thầm làm nó.
- **Go/No-Go gate**: Điểm quyết định có tiêu chí **đo được** và hành động định sẵn cho **cả hai** nhánh. Một gate không có nhánh FAIL thì không phải gate.
- **kill criteria**: Điều kiện dừng hẳn dự án. Đây là mục mà tài liệu planning hay né nhất, và cũng là mục làm cho các gate còn lại có nghĩa.
- **canonical facts**: Bảng sự thật chung được PM chốt trước khi nhiều writer chạy song song, để mọi tài liệu copy từ **một nguồn** thay vì mỗi người tự suy ra số của mình. Mỗi số đi kèm **nhãn nguồn** như một cặp không tách rời.
- **nhãn nguồn `[OFF]` / `[BCN]` / `[TC]` / `[EM]`**: Hạng của một con số — official · báo cáo ngành · thứ cấp · **ước lượng/phép nhân**. ⚠️ Nhãn `[EM]` **phải đi theo con số qua mọi phép tính**; bỏ nhãn khi nhân một con số ước lượng sẽ **rửa sạch** khoảng trống và biến giả định thành sự thật đo được.
- **rủi ro nhị phân**: Rủi ro mà trả lời sai không làm sản phẩm *kém hơn* mà làm nó **bất hợp pháp hoặc không tồn tại**. Nó không nằm chung thang Probability × Impact với rủi ro thường, vì thang đó giả định hậu quả liên tục.
- **bus factor**: Số người rời khỏi dự án là dự án dừng. Với `comic-studio` con số đó là **1**.
- **build-in-public**: Chiến lược phân phối bằng cách công khai quá trình xây sản phẩm trên mạng xã hội. Với sản phẩm indie, đây là kênh có tiền lệ đạt doanh thu ở **$0 marketing spend**.
- **disclosure-first positioning**: Nêu rõ sản phẩm dùng AI ngay từ đầu thay vì để bị phát hiện. Với ngách comic, đây **không phải lựa chọn đạo đức mà là ràng buộc phân phối** — cộng đồng đã có tiền lệ boycott khi phát hiện AI không được khai báo.

---

*Nhóm này và nhóm kế tiếp được bổ sung ở run `2026-08-24-khoi-tao-requirements-stories-comic-studio`, khi tầng 020-Requirements và 022-User-Stories được khởi tạo.*

## Requirements & tài liệu hoá

- **BRD (Business Requirement Document)**: Tài liệu yêu cầu nghiệp vụ ở **cấp module** — 8 file `BRD-001…008`, mỗi file ánh xạ đúng một nhóm module A–H của `MVP-Scope §3`. Cấu trúc 7 mục cố định: Business goal · Phạm vi module · Yêu cầu nghiệp vụ (bảng `BR-{NNN}-{nn}`) · Ràng buộc & điều kiện chặn · Cái module này KHÔNG làm · Rủi ro chính · Tài liệu liên quan. Độc giả đích là Founder khi quyết định *"module này có đáng làm ở mốc này không"*.
- **Use Case (UC)**: Tài liệu mô tả một luồng tương tác actor–hệ thống theo mục tiêu, không phải một trang UI. Cấu trúc 6 mục: Thông tin (actor, mốc MVP, BRD module, điều kiện tiên quyết) · Mục tiêu · Main flow (mỗi bước ghi rõ actor) · Alternative flow · Exception flow · Tài liệu liên quan. **Exception flow rỗng là không đạt** — mọi UC phải có ≥1 nhánh exception. 11 UC trong repo (`UC-01…UC-11`).
- **Mức độ rắn**: Hệ nhãn 4 giá trị dùng trong SRS để phân loại **độ cứng của quyết định** cho từng hàng requirement — khác với `nhãn nguồn` (đo *chất lượng bằng chứng* của một con số). Bốn giá trị: **`CHỐT`** — đã quyết, không mở lại; **`MẶC ĐỊNH`** — đã chọn nhưng có đường lui ghi rõ thành văn; **`CHƯA QUYẾT`** — phải ghi `TBD`, cấm tự gán số; **`LAI`** — cơ chế đã `CHỐT` nhưng một tham số bên trong nó còn `MẶC ĐỊNH` hoặc `CHƯA QUYẾT` (ví dụ: seam adapter provider ảnh là `CHỐT`, nhưng provider chính mặc định là `MẶC ĐỊNH`). ⚠️ `[CHỐT]` còn được dùng như một **nhãn nguồn thứ năm** (bên cạnh `[OFF]`/`[BCN]`/`[TC]`/`[EM]` đã có ở nhóm *Planning, thị trường & quản trị*), nghĩa là *"quyết định của Founder tại gate"* — cùng một ký hiệu, hai hệ phân loại khác nhau (độ cứng của một **hàng requirement** vs chất lượng bằng chứng của một **con số**); đọc theo đúng ngữ cảnh bảng đang đứng.
- **negative requirement**: Requirement viết dưới dạng **phủ định** — mô tả tường minh một cơ chế/tính năng **đã bị cắt hẳn** (không phải hoãn), lý do cắt, và (nếu có) điều kiện mở lại. Phải xuất hiện thành mục riêng trong SRS (mục 6), **không được im lặng**: một SRS im lặng về thứ đã bị cắt sẽ bị đọc nhầm là *"chưa quyết"*. Hai bẫy hay gặp khi viết negative requirement: cắt **cơ chế** nhưng vẫn giữ **mục tiêu** (ví dụ Layout Score 5 số thực bị cắt, mục tiêu layout theo narrative importance vẫn giữ), và cắt **UI** nhưng không được lẫn sang cắt **cột dữ liệu** (cắt UI cây generation không đồng nghĩa cắt `parent_generation_id`).

---

## Backlog & Story engineering

- **Epic**: Nhóm Story cấp cao, cắt theo **module A–H** (không cắt theo mốc MVP0–MVP4). Cấu trúc 6 mục: Implements (một dòng link tới đúng anchor mục 4 của PRD) · Mục tiêu Epic · Story trong horizon (bảng có link, mốc, `I`/`S`, trạng thái) · Story ngoài horizon — chưa có file · Definition of Done cấp Epic · Tài liệu liên quan (BRD cha + UC liên quan). 8 Epic trong repo, mỗi Epic ánh xạ 1:1 với một BRD.
- **User Story (Story)**: Đơn vị backlog nhỏ nhất, mở đầu bằng một câu chuẩn duy nhất *"Là `<actor>`, tôi muốn `<hành động>`, để `<giá trị>`"* — câu này phải **copy nguyên văn** từ bảng nguồn, không diễn giải lại. Cấu trúc 6 mục: Story · Part of (Epic cha + BRD + UC liên quan) · Bối cảnh & nguồn (≥1 anchor `MVP-Scope §3` **và** ≥1 exit criterion `Roadmap`) · Acceptance Criteria · Ước lượng (`E_build`/`E_hitl`) · INVEST.
- **Acceptance Criteria (AC)**: Khuôn **checklist 4 khối**, **KHÔNG dùng Gherkin** (`Given/When/Then`) — vì exit criteria của `Roadmap` đã ở dạng checklist assertion sẵn, và với đội một người không tồn tại ranh giới BA↔QA↔dev mà Gherkin được sinh ra để phục vụ. Bốn khối theo đúng thứ tự: **AC-1** `### Xác minh được` — mỗi dòng `- [ ]` là một assertion nhị phân kèm cách đo ngay trong dòng, **không được rỗng**; **AC-2** `### Đường không hạnh phúc (unhappy path)` — ≥1 dòng cho failure mode/edge case/race condition, rỗng ⇒ **không Ready**; **AC-3** `### Ràng buộc cứng không được vi phạm` — trích `KC-x`/`C-x`/`AG-x`, không có thì ghi `—`; **AC-4** `### Story này KHÔNG làm` — chống scope creep, không được rỗng. Luật viết dòng AC-1: mỗi dòng phải **thất bại được** — *"insert panel 4 nhân vật bị từ chối"* hợp lệ, *"schema hỗ trợ giới hạn nhân vật"* không hợp lệ vì không có cách nào chứng minh sai.
- **INVEST**: Chuẩn INVEST **đã được diễn giải lại** cho một đội một người, chưa có dòng code nào, chưa có velocity — không dùng nghĩa sách giáo khoa. **Independent**: độc lập về *deliverable*, không đòi độc lập tuyệt đối về schema (1 dev/1 monolith/1 DB); phụ thuộc phải được khai tường minh, không giả vờ không có. **Negotiable**: bị giới hạn — Story chạm `KC-1…KC-7` là **không negotiable**. **Valuable**: hai lớp, phải khai rõ đang thoả lớp nào — `Valuable-U` (giá trị người dùng thấy được, khuôn `Là actor, tôi muốn... để...`) hoặc `Valuable-I` (giá trị là **chi phí không đảo ngược tránh được**, khuôn `Nếu KHÔNG làm ở {mốc}, thì {hậu quả không đảo ngược cụ thể}` — cấm các cụm mơ hồ như *"để code sạch hơn"*). **Estimable** và **Small**: đo bằng **giờ-người** (xem `E_build`/`E_hitl`), không phải story point, không phải ngày công. **Testable**: tương đương AC-1 — checklist assertion nhị phân có cách đo, không phải đánh giá chủ quan. ⚠️ **INVEST KHÔNG áp dụng** cho 5 Story thuộc `[MVP0]` (DoD của chúng lấy từ 5 tiêu chí gate G1 thay vì từ INVEST); các Story vỡ `Independent`/`Small` phải ghi `⚠️` kèm nguyên lý do không cắt được theo đường nào, không được im lặng bỏ qua.
- **Definition of Ready (DoR)** / **Definition of Done (DoD)**: Hai bộ tiêu chí tối thiểu, mỗi bộ 5 mục, áp cho mọi Story. **DoR** (Story chưa đủ 5 mục thì không được đưa vào `Active-Sprint/`): có `Anchor` đầy đủ · `Valuable` đã khai lớp · `E_build ≤ 16` giờ-người **và** `E_hitl ≤ 2` giờ-người/chapter (hoặc có lý do vượt trần ghi thành văn) · AC đủ 4 khối với AC-2 và AC-4 không rỗng · không vi phạm `AG-1…AG-8` và không nằm trong ô `❌ cắt hẳn` của `MVP-Scope §3`. **DoD**: mọi dòng AC-1/AC-2 đã tick kèm bằng chứng cạnh dòng · Story chạm `KC-1…KC-7` phải có **test** chứng minh, không chỉ có code · hành động thay đổi dữ liệu người dùng phải sinh một `change_log` row · không làm lùi exit criterion nào đã đạt của mốc hiện tại · cập nhật `Stories-MOC.md` và hàng tương ứng ở `Backlog-Priority.md`.
- **`E_build`**: Số giờ-người **Founder** cần để implement một Story, gồm cả thời gian điều phối AI agent. Trần **≤ 16 giờ-người** ⚠️ `[EM]` — **neo mềm** vào thời lượng duy nhất có nguồn trong bảng canonical facts (MVP0 = 1–2 tuần, `CF-8.4`), không phải một số đo. Mặc định **phải split Story** khi vượt trần; **chỉ giữ nguyên** khi không tồn tại sub-slice nào "xong" mà có nghĩa **và** lý do vượt trần được **ghi thành văn** (DoR R3) — ví dụ đã có trong repo: `Story-Tenant-Id-And-RLS-Everywhere` ghi nhận `E_build ~24h`, vượt trần, kèm lý do bằng văn bản, "được phép theo quy ước cắt lô".
- **`E_hitl`**: Số giờ-người **con người** phải bỏ ra **mỗi lần chạy / mỗi chapter** để đi qua HITL gate mà Story đó tạo ra hoặc tiêu thụ — đơn vị là **giờ-người/chapter**, không phải một lần duy nhất. Trần **≤ 2 giờ-người/chapter** ⚠️ `[EM]` **— placeholder, không có căn cứ nguồn ngoài.** Phải được **hiệu chỉnh bằng số đo thật của MVP0** (tỉ lệ human-reject sau VLM-select, tiêu chí `G1-c`); trước khi MVP0 chạy, **đừng đối xử với con số 2h này như một ngưỡng đã kiểm chứng**. Vượt trần thì **KHÔNG split được** (split không giảm nghĩa vụ lặp lại), phải **escalate cho Founder**. ⛔ **`E_build` và `E_hitl` là hai đại lượng khác nhau, cấm cộng hoặc trừ vào nhau** — cùng loại lỗi mà `CF-6.7`/`CF-6.8` đã cảnh báo (hai mẫu số khác nhau).
- **UNLOCK-ORDER**: Khung xếp hạng backlog được chọn **thay cho RICE và MoSCoW** (cả hai đều không dùng được — RICE thiếu mẫu số Reach lẫn Effort; MoSCoW trùng lặp và *lossy* so với `Scope-Label` đã có). Gồm một cột kế thừa (`Mốc`, `Scope-Label` — chấm một lần ở nguồn, cấm chấm lại) cộng một `Rank` **lexicographic 3 khoá**, chỉ so sánh trong phạm vi **một mốc**, không có điểm tổng: **1. `I` (Irreversibility)** — `I2` không backfill được · `I1` sửa sau được nhưng là migration trên dữ liệu thật · `I0` sửa sau gần như miễn phí; **2. `B` (Blocking degree)** — `B2` chặn cứng ≥1 exit criterion của mốc · `B1` chặn Story khác nhưng không chặn exit criterion · `B0` không chặn gì; **3. `G` (Gate proximity)** — `G2` chính là một exit criterion/tiêu chí gate · `G1` cần thiết để exit criterion đó đo được · `G0` không nằm trên đường tới gate nào. Khi cả 3 khoá bão hoà (nhiều Story cùng `I2/B2/G2`), dùng tie-break theo thứ tự **T1** phụ thuộc kỹ thuật trực tiếp → **T2** `E_hitl` thấp trước → **T3** `E_build` thấp trước → **T4** Founder quyết, ghi đúng một dòng lý do.
- **`Scope-Label`**: Nhãn `✅`/`🟡`/`⛔`/`❌` tại ô giao (hạng mục × mốc) của `MVP-Scope §3`, dùng làm **cột kế thừa** trong bảng backlog — chấm đúng một lần ở `MVP-Scope.md`, **cấm chấm lại** ở nơi khác. Lệch giá trị nghĩa là hàng backlog sai, không phải `MVP-Scope` sai.
- **`Rank`**: Cột thứ tự (`#`) trong bảng `Backlog-Priority.md`, tính theo `UNLOCK-ORDER`, **reset về 1 ở mỗi mốc** — không có rank xuyên mốc, vì thứ tự mốc `MVP0→MVP1→MVP2→MVP3→MVP4` đã `[CHỐT]` và không mở lại.

---

## Tài liệu tham khảo

- [Analysis-Comic-Studio-Concept](../050-Research/Analysis-Comic-Studio-Concept.md) — nguồn của toàn bộ thuật ngữ domain trong file này; mỗi term đều truy được về một mục cụ thể ở đó.
- [Analysis-Market-Competitor-Landscape](../050-Research/Analysis-Market-Competitor-Landscape.md) — nguồn của nhóm *Planning, thị trường & quản trị*.
- [Request.md](./Request.md) — thiết kế ý tưởng gốc, nơi phần lớn thuật ngữ được đặt tên lần đầu.
- [Documents-Template.md](../../knowledge-base/99-Templates/Documents-Template.md) — RULE-001, quy ước tài liệu của dự án.
