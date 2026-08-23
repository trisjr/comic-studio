# Escalations: 2026-08-23-danh-gia-y-tuong-comic-studio

> Append-only. Không sửa entry cũ.

## E1 — Gate trả về đáp án làm vô hiệu một phần giả định A1

- **Tầng**: 3 → 2 (anh đã trả lời ở gate; PM tự xử lý hệ quả trong phạm vi `brief.md`)
- **Thời điểm**: 2026-08-23, ngay sau GATE, trước phase 5
- **Bối cảnh**: cả 4 lens của phase 2 chạy dưới **Assumption A1 = "dự án cá nhân, 1 dev, công cụ cho chính mình"**. Prompt dispatch của cả ba subagent đều nêu rõ giả định này.

### Đáp án của anh tại gate

| Câu | Đáp án |
|---|---|
| Duyệt plan | **Duyệt như plan** — một tài liệu Analysis, không làm Risk Register |
| Nguồn truyện (OQ1) | **Nền tảng cho người khác tự upload truyện của họ** |
| Mục tiêu (OQ2) | **Sản phẩm thương mại / SaaS** |
| Quy mô (A1) | **Đúng — 1 mình anh + AI assist** |

### Vì sao đây là escalation, không phải một tick đơn giản

Ba đáp án đầu **giữ nguyên** phần "1 dev" của A1 nhưng **thay thế** phần "công cụ cá nhân" bằng "**SaaS thương mại multi-tenant**". Đó là một tổ hợp khác hẳn: *một dev đơn lẻ xây một nền tảng thương mại*. Nó đảo chiều hoặc làm yếu **bốn** kết luận mà các lens đã chốt:

| # | Kết luận cũ (dưới A1 cá nhân) | Ảnh hưởng của đáp án mới |
|---|---|---|
| 1 | `architect`: **cắt canvas editor §14** (50-60% effort), *"cả 3 tương tác §14 nêu ra đều không cần canvas"* | ⚠️ **YẾU ĐI ĐÁNG KỂ.** Với công cụ cá nhân, editor là tiện nghi. Với **SaaS bán cho tác giả**, editor *chính là sản phẩm* — nó là thứ khách hàng trả tiền để dùng, và là nơi Zarya-style "iterative, interactive process" tạo ra phần được bảo hộ bản quyền. Cắt nó khỏi một SaaS là cắt mất sản phẩm. **Cần `architect` xét lại.** |
| 2 | `researcher`: **chi phí không phải rào cản** ($400–1.600 / 100 chapter) | ⚠️ **ĐẢO CHIỀU HOÀN TOÀN.** Là chi phí cá nhân một lần thì không đáng kể. Là **COGS trên mỗi khách hàng** thì phải đặt cạnh trần giá $10–20/tháng mà chính `researcher` đo được (Dashtoon ~$10/mo, Anifusion $9/mo) → sinh ra một bài toán **unit economics** mà không lens nào xét. PM tự tính ở mục *Phân tích bổ sung của PM* bên dưới. |
| 3 | `researcher` §4.1: rủi ro bản quyền input là **của anh** | 🔄 **CHUYỂN DẠNG, không biến mất.** Rủi ro sơ cấp chuyển sang người upload. Nhưng nền tảng phát sinh nghĩa vụ mới: điều khoản buộc user cam kết có quyền, cơ chế takedown, và — điểm chưa ai xét — **NĐ 134/2026 Điều 37a giới hạn TDM ở "non-commercial purposes at the point of use"**. Một nền tảng **thương mại** chạy extraction trên truyện có bản quyền của user có rơi vào giới hạn đó không? Cùng với Điều 37c (*"royalty payment obligations may arise"*). **Cần `researcher` tra.** |
| 4 | Lens PM: moat "dữ liệu preference tích luỹ" là moat thật nhưng **miễn phí** | ✅ **MẠNH LÊN.** Multi-tenant nghĩa là preference data từ *nhiều* tác giả, không phải một. Moat này chuyển từ "đáng làm" sang "**lý do tồn tại của sản phẩm**". Khuyến nghị log từ MVP1 giữ nguyên và tăng mức ưu tiên. |

### Quyết định của PM

**Không đổi tier, không đổi lane, không chạy lại phase 2.** Ba lens vẫn đúng ở phần kỹ thuật thuần (data model, pipeline AI, năng lực image model) — những phần đó **bất biến** với mô hình kinh doanh. Chỉ bốn kết luận trên bị ảnh hưởng, và chúng khoanh vùng được.

**Hành động — ba việc, chạy trước phase 5:**

1. **PM tự làm**: phân tích unit economics (mục dưới). Đây là lens product, thuộc remit của main loop theo `pm-core.md` Nguyên tắc 1.
2. **Resume `architect`** bằng `SendMessage` với đúng một câu hỏi delta: kiến trúc đổi gì khi mục tiêu là SaaS multi-tenant 1 dev, và khuyến nghị cắt §14 còn đứng không.
   → **Lý do dùng `SendMessage` thay vì spawn mới**: agent đó đã có toàn bộ context (`Request.md` + findings của nó). Spawn mới tốn ~23.6k overhead + phải đọc lại tất cả. `pm-core.md` Nguyên tắc 3 cấm *phụ thuộc* vào SendMessage, không cấm *dùng* nó như tiện ích — nếu thất bại, PM spawn `architect` mới.
3. **Resume `researcher`** bằng `SendMessage`: tra NĐ 134/2026 Điều 37a/37c cho nền tảng thương mại, nghĩa vụ nền tảng với user-uploaded copyrighted content, và mô hình pricing/unit economics của đối thủ.

**Ownership**: cả hai giữ nguyên ownership cũ (`findings/architect.md`; `researcher` không có Write → trả text, PM append). Không có va chạm.

**Rủi ro của quyết định này**: nếu delta lớn hơn dự kiến — ví dụ `architect` kết luận SaaS multi-tenant đòi kiến trúc khác hẳn — thì phần *Ba thứ nên cắt* của outline phải viết lại chứ không chỉ điều chỉnh. PM chấp nhận rủi ro đó vì phương án thay thế (chạy lại cả phase 2 dưới giả định mới) đắt hơn nhiều lần mà phần lớn kết quả sẽ trùng.

---

## Phân tích bổ sung của PM — Unit economics, hệ quả trực tiếp của đáp án gate

Đây là phân tích **mới**, không lens nào làm, vì nó chỉ tồn tại khi mô hình là SaaS thương mại. Số liệu đầu vào lấy từ `findings/researcher.md` §5.1, §5.3, §3.4.

### Bài toán

| Đại lượng | Giá trị | Nguồn |
|---|---|---|
| Ảnh / chapter | 60 (15 page × 4 panel) | giả định của `researcher` §5.3 |
| Giá rẻ nhất còn giữ được consistency (Gemini 3 Pro Image, **batch**) | **$0.067 / ảnh** | official, `researcher` §5.1 |
| Giá thay thế (FLUX.2 pro) | **$0.03 / ảnh** | official, `researcher` §5.1 |
| Hệ số regenerate | **không có dữ liệu ngành** — tham số hoá 1x / 2x / 3x | `researcher` §5.2 |
| Trần giá thị trường tool cá nhân | **$9–10 / tháng** (Dashtoon ~$10, Anifusion $9) | `researcher` §3.4 |

### Chi phí biến đổi mỗi chapter, chỉ tính image inference

| Model | 1x | 2x | 3x |
|---|---|---|---|
| Gemini 3 Pro Image batch ($0.067) | **$4,02** | **$8,04** | **$12,06** |
| FLUX.2 pro ($0.03) | $1,80 | $3,60 | $5,40 |

### Kết luận: mô hình subscription phẳng $10/tháng KHÔNG SỐNG ĐƯỢC

Ở mức giá đối thủ đang thu ($9–10/tháng) và ở model chất lượng cao nhất (Gemini batch), **một khách hàng làm đúng 1 chapter/tháng với regen 2x đã tiêu $8,04 trên $10 doanh thu** — chưa trừ chi phí LLM cho Layer 1/2, chưa trừ storage cho reference + panel image, chưa trừ hạ tầng, chưa tính chiết khấu cổng thanh toán. Khách hàng làm 2 chapter/tháng thì **lỗ**.

Đây là mâu thuẫn thật, không phải suy đoán: nó chỉ dùng số official của nhà cung cấp và giá công khai của đối thủ.

**Hệ quả — bốn đường ra, PM xếp theo mức khuyến nghị:**

1. ⭐ **Credit-based pricing, không phải subscription phẳng.** Đây chính là mô hình ComicInk đang dùng (`researcher` §2.1: credit ~150 cho 50 trang, ~500 cho 200 trang, **art tính riêng**). Không phải trùng hợp — ComicInk có cùng cấu trúc chi phí và đã tới cùng kết luận. Đây là bằng chứng thị trường mạnh nhất có được.
2. **Bring-your-own-key.** User tự gắn API key của họ; nền tảng thu tiền cho *phần mềm và workflow*, không cho inference. Xoá sạch rủi ro COGS, và khớp với phân khúc mà `researcher` đánh giá khả năng cao nhất (tác giả có ngân sách sẵn). Nhược điểm: ma sát onboarding cao.
3. **Phân tầng model**: FLUX.2 pro ($0.03) cho tier thấp, Gemini batch ($0.067) cho tier cao. Kiến trúc §16 Visual Prompt Compiler **đã hỗ trợ sẵn** việc này — đây là lần đầu abstraction đó chứng minh được giá trị kinh tế cụ thể, không chỉ giá trị kỹ thuật.
4. **Giá cao hơn thị trường**, định vị vào tác giả chuyên nghiệp thay vì hobbyist.

**Điều này thêm một hạng mục vào deliverable**: mục 9 của outline không còn là *"chi phí không phải rào cản"* mà phải trở thành ***"chi phí không phải rào cản cho công cụ cá nhân, nhưng là ràng buộc thiết kế trung tâm cho SaaS"***, kèm bảng trên và bốn đường ra.

**Và nó đổi thứ tự ưu tiên của MVP0**: MVP0 vốn được thiết kế để đo *consistency có đủ tốt không*. Với mô hình SaaS, MVP0 phải đo thêm một thứ nữa, và thứ đó quan trọng ngang bằng: **tỉ lệ regenerate thực tế** — vì đó là biến quyết định unit economics, và `researcher` xác nhận **không có dữ liệu ngành nào** về nó. MVP0 là cơ hội rẻ nhất để tự đo con số đó ($12–50).

---

## E2 — PM tự sửa phép tính unit economics: hệ số là 3x, không phải 2x

- **Tầng**: 2 (PM tự quyết, tự sửa)
- **Thời điểm**: 2026-08-23, sau delta của `researcher`
- **Nguồn phát hiện**: `findings/researcher-delta.md` Câu 4

### Sai ở đâu

Mục *Phân tích bổ sung của PM* ở E1 dùng hệ số regenerate **2x** làm kịch bản trung tâm, và tham số hoá 1x/2x/3x theo cách trình bày của `researcher` ở báo cáo gốc §5.2 — nơi ghi rõ *"không có dữ liệu ngành"*.

Delta tra ra được con số thật: **CANVAS dùng N = 3 candidate mỗi shot**, *"Performance saturates at N=3, providing the best balance between quality and computation."* ([arXiv 2604.13452v1](https://arxiv.org/html/2604.13452v1)).

**Và điều quan trọng hơn con số: bản chất của nó khác hẳn giả định của PM.** PM hiểu 2x là *"generate, nếu lỗi thì generate lại"* (retry-on-failure). Thực tế N=3 là **best-of-N**: generate 3 candidate cho **mọi** panel rồi để VLM chọn 1, **mặc định, không có ngoại lệ**. Đó chính là setting để đạt con số `character 4.91/5` mà cả verdict "khả thi" đang dựa vào. Không thể lấy con số chất lượng của N=3 mà tính chi phí của N=2.

### Con số đã sửa

| | PM tính ở E1 (2x) | **Đúng (N=3)** | Lệch |
|---|---|---|---|
| Chi phí/chapter, Gemini 3 Pro batch $0.067 | $8,04 | **$12,06** | **+50%** |
| 100 chapter | ~$804 | **~$1.206** | +50% |
| Margin trên $9.99 với 1 chapter/tháng | −$1,95 hoà gần vốn | **−21%** | tệ hơn |
| Power user 3 chapter/tháng | — | **−262%** | — |

Chưa tính chi phí VLM call để score 3 candidate — `researcher` không tính được vì không biết token cost prompt QA của CANVAS. ⇒ **Con số $12,06 là sàn, không phải trần.**

### Kết luận vẫn giữ, và mạnh hơn

Kết luận ở E1 — *"subscription phẳng $10/tháng không sống được"* — **không đổi, và giờ có căn cứ chắc hơn**. Nhưng hai thứ trong E1 phải sửa:

1. **Nguyên nhân gốc không phải pricing mà là kiến trúc.** `researcher` reverse-engineer giá ComicInk ($0.333/page) và chứng minh họ generate **1 ảnh cho cả TRANG**, không phải 1 ảnh/panel — vì 1 ảnh/panel ở N=3 cho margin **−141%**, còn 1 ảnh/trang cho **+40%**. PM đã đi tìm câu trả lời ở tầng giá, trong khi nó nằm ở tầng kiến trúc.
2. **Bốn đường ra ở E1 vẫn đúng nhưng thứ tự đổi.** BYOK lên vị trí số 1 (từ số 2), vì delta cấp thêm **ba** căn cứ độc lập cho nó: (a) 23% GRR ở AI budget-tier khiến subscription là mô hình sai với 1 dev không budget marketing; (b) power user ở −262% không thể chặn bằng pricing phẳng; (c) xung đột M13 giữa per-panel generation và margin **biến mất hoàn toàn** dưới BYOK. Ba lập luận từ ba hướng khác nhau hội tụ về cùng một khuyến nghị.

### Điều đáng ghi lại cho lần sau

PM đã tự tính một con số quan trọng từ dữ liệu *có ghi rõ là không đầy đủ* (`researcher` §5.2: "không có dữ liệu ngành về tỉ lệ regenerate") mà **không đánh dấu con số kết quả là ước lượng**. Đúng ra phải viết "$8,04 — dựa trên hệ số 2x giả định, chưa có căn cứ" chứ không phải "$8,04". Bài học: khi input đã được đánh dấu là khoảng trống, output tính từ nó phải mang cùng cảnh báo — nếu không, khoảng trống bị **rửa sạch** qua một phép nhân.
