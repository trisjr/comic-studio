# Findings — product-manager (lens do PM main loop tự làm)

> `pm-core.md` Nguyên tắc 1: vai trò Product Manager KHÔNG được delegate cho subagent
> `product-manager` (agent đó không có `Bash`, không có `Task`). Lens này do main loop tự thực hiện.
> Vì vậy file này không có mục *Kết luận của worker* — toàn bộ là kết luận của PM.

## 1. Ý tưởng này thực chất là gì

`Request.md` **không** phải một ý tưởng sản phẩm. Nó là một **thiết kế kiến trúc** cho một sản phẩm chưa được định nghĩa. Đây là quan sát quan trọng nhất của lens product, và nó định hình mọi thứ còn lại.

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

Từ "user" xuất hiện trong tài liệu đúng ở §14 (UI) và §18 (human approval) — cả hai lần đều với nghĩa *người vận hành công cụ*, không phải người có nhu cầu.

**Hệ quả**: không thể trả lời "ý tưởng có phù hợp hay chưa" theo nghĩa product-market fit, vì tài liệu chưa nêu market. Câu trả lời trung thực phải tách làm hai:
- **Phù hợp với tư cách một thiết kế kỹ thuật?** → Trả lời được, và đây là điều 3 lens fan-out đang làm.
- **Phù hợp với tư cách một sản phẩm?** → Chưa đủ dữ liệu để trả lời, và **đó chính là phát hiện**, không phải một khoảng trống cần lấp bằng suy đoán.

Đây không phải lời phê. Với một dự án cá nhân, bắt đầu từ "kiến trúc thú vị" là động lực hợp lệ. Nhưng nó phải được **gọi đúng tên**, vì hai loại dự án này có tiêu chí thành công khác nhau hoàn toàn, và cắt scope theo tiêu chí sai là cách hỏng phổ biến nhất.

## 2. Kiểm tra luận điểm "moat"

Tác giả kết luận (§ cuối): *"cái giúp nó không loạn nhân vật chính là Story Bible + Timeline State + Canonical References + Visual Prompt Compiler + Continuity Checker. Đây mới là moat của sản phẩm, chứ không phải bản thân việc gọi image model."*

Nửa đầu **đúng và sắc**: việc gọi image model là commodity, ai cũng gọi được. Nửa sau — gọi 5 thành phần đó là *moat* — cần phản biện, vì moat có định nghĩa hẹp hơn "thứ khó làm":

| Thành phần | Khó làm? | Đối thủ khó copy? | Là moat? |
|---|---|---|---|
| Story Bible (schema) | Không — là data model, viết ra được trong một tuần | Không | ❌ Không |
| Timeline State | Trung bình | Không — công khai trong chính tài liệu này | ❌ Không |
| Canonical References | Không | Không | ❌ Không |
| Visual Prompt Compiler | Trung bình | Không | ❌ Không |
| Continuity Checker | **Có** | Trung bình | ⚠️ Có thể |

**Kết luận của PM**: 5 thành phần này là **barrier to entry** (rào cản gia nhập — làm cho việc bắt chước tốn công), không phải **moat** (lợi thế tự củng cố theo thời gian). Khác biệt này quan trọng: barrier chỉ mua thời gian, moat mua vị thế.

Moat thật, nếu có, sẽ nằm ở chỗ khác — và cả ba đều **không** được nhắc trong `Request.md`:

1. **Dữ liệu tích luỹ**: mỗi lần user sửa panel là một nhãn preference. Sau 10.000 lần sửa, hệ thống biết đạo diễn thế nào cho vừa mắt người đọc — đối thủ mới không có dữ liệu đó. Đây là moat thật và nó **miễn phí**, chỉ cần thiết kế để ghi lại từ ngày đầu. **Đề xuất: log mọi hành vi chỉnh sửa của user như first-class data, ngay từ MVP1.** Bỏ qua ở MVP1 thì không lấy lại được.
2. **Switching cost qua Story Bible**: một tác giả đã xây Story Bible cho truyện 300 chapter thì không muốn làm lại ở nơi khác — với điều kiện Story Bible đủ giá trị và không export dễ.
3. **Thư viện style/character đã lock**: cùng lý do.

## 3. Rủi ro pháp lý — PM đánh giá đây là rủi ro số 1, trên cả rủi ro kỹ thuật

Xếp hạng này có thể gây bất ngờ, nên nói rõ lập luận: mọi rủi ro kỹ thuật trong tài liệu đều là *rủi ro về mức độ* (làm được tới đâu, tốn bao nhiêu) — chúng làm sản phẩm **kém hơn**. Rủi ro pháp lý là *rủi ro nhị phân* — nó làm sản phẩm **không tồn tại được**. Một rủi ro nhị phân chưa kiểm tra luôn phải xếp trên một rủi ro liên tục.

Ba lớp chồng nhau, mỗi lớp độc lập:

**Lớp 1 — Bản quyền truyện gốc (input).** Chuyển truyện chữ của tác giả khác thành comic là *derivative work*, cần license. Đây là câu **OQ1** đang chờ anh trả lời tại GATE. Ba nhánh:

- *Truyện của chính anh* → lớp này biến mất hoàn toàn.
- *Truyện của người khác* → dùng cá nhân là vùng xám; phát hành hoặc thương mại hoá là vi phạm rõ ràng. Nếu đây là nhánh thật, phần lớn giá trị "moat" mất ý nghĩa vì không đến được thị trường.
- *Sản phẩm cho người khác tự upload truyện của họ* → rủi ro chuyển sang họ, nhưng nền tảng vẫn cần cơ chế và điều khoản. Đây là nhánh dễ sống nhất về pháp lý.

**Lớp 2 — Bản quyền ảnh AI (output).** Lens `researcher` đang tra tiền lệ. Nếu output không được bảo hộ, hệ quả cho business model là trực tiếp: không thể bán quyền, chỉ có thể bán **công cụ** hoặc **dịch vụ**. Điều này lại củng cố hướng "bán tool cho tác giả" thay vì "sản xuất comic để bán".

**Lớp 3 — Điều khoản của image model provider.** Có cho phép output thương mại không, có cấm dùng ảnh tham chiếu có bản quyền không. Lens `researcher` đang tra.

**Khuyến nghị của PM**: bất kể nhánh nào, kiểm tra lớp 1 **trước khi viết dòng code đầu tiên**. Đây là loại rủi ro càng phát hiện muộn càng đắt, và chi phí kiểm tra gần bằng không so với chi phí build.

## 4. Phản biện thứ tự 4 MVP (§18) dưới góc product

Tác giả xếp: MVP1 Story Intelligence (*"Chưa cần generate ảnh"*) → MVP2 Comic Director → MVP3 Visual Generation → MVP4 Production.

Thứ tự này **hợp lý về mặt kiến trúc** (xây nền trước) nhưng **rủi ro cao về mặt product**, vì hai lý do:

1. **Rủi ro lớn nhất bị đẩy về sau.** Câu hỏi sống-chết của cả ý tưởng là *"ảnh sinh ra có đủ consistency để đọc như một bộ comic không?"*. Câu đó chỉ được trả lời ở **MVP3**. Nghĩa là anh có thể build xong hai milestone — phần lớn công sức — rồi mới phát hiện tiền đề sai. Nguyên tắc product ngược lại: **kiểm tra giả định đắt nhất bằng thí nghiệm rẻ nhất, sớm nhất.**
2. **MVP1 không tự đứng được như một sản phẩm.** Một Story Bible không có comic thì giá trị cho ai? Nó là *artifact trung gian*, không phải deliverable người dùng thấy giá trị. MVP đúng nghĩa phải giao được một giá trị dùng ngay, dù nhỏ.

**Đề xuất thay thế — MVP0 (1–2 tuần, làm thủ công phần lớn):**

> Lấy **một chapter duy nhất**. Tự tay viết Story Bible cho 2 nhân vật (không cần code extraction). Tự tay viết panel script cho ~8 panel (không cần code director). Rồi **chỉ** dùng code cho đúng một việc: generate 8 panel đó với character reference, và tự mắt đánh giá consistency.
>
> **Tiêu chí pass/fail đo được**: nhìn 8 panel liền nhau, có nhận ra đó là cùng một nhân vật mà không cần được nhắc không? Nếu **không** → toàn bộ ý tưởng cần đổi cách tiếp cận, và anh biết điều đó sau 2 tuần thay vì sau 4 tháng.

Đây là *vertical slice* xuyên cả 4 layer, đâm thẳng vào rủi ro lớn nhất trước, và tốn ít hơn MVP1 một bậc độ lớn. Lens `architect` và `senior-ai-engineer` đang được hỏi cùng câu này một cách độc lập — nếu cả ba lens hội tụ về cùng kết luận thì đây là khuyến nghị mạnh nhất của cả run.

## 5. Định giá lại phạm vi theo giả định A1 (1 dev)

Nếu A1 đúng (dự án cá nhân, 1 dev + AI assist), đối chiếu tham vọng của tài liệu với năng lực:

| Hạng mục trong `Request.md` | Đánh giá của PM |
|---|---|
| Story Bible + Timeline state | Giữ — đây là phần đúng nhất và rẻ nhất của tài liệu |
| Comic IR (§4) | Giữ — chi phí thấp, giá trị debug cao |
| Character reference sheet (§8) | Giữ — điều kiện cần của consistency |
| Identity/Appearance split (§9) | Giữ — abstraction đúng, gần như miễn phí |
| `Generation` lineage (§13) | Giữ **tối giản** — log prompt/model/seed/refs. Bỏ cây `parent_generation` ở MVP |
| Layout Score 5 chiều (§5) | **Hoãn** — chờ phản biện của lens AI về việc LLM sinh số thực có nghĩa hay không |
| 3 microservice + Vector DB (§12) | **Cắt** — over-engineering cho 1 dev. Monolith + 1 Postgres |
| Web canvas editor kiểu Figma (§14) | **Cắt khỏi MVP** — lens architect đang định lượng, nhưng đây gần chắc là hạng mục đắt nhất và ít rủi ro nhất (đắt nhưng biết chắc làm được ⇒ không đáng làm sớm) |
| Continuity Checker (§15) | **Hoãn tới khi có bằng chứng** — chờ lens AI đánh giá false positive rate |
| Export PDF/CBZ/Webtoon (§18 MVP4) | Nâng ưu tiên — đây là thứ *duy nhất* trong MVP4 mà người dùng thật sự nhận được |
| Text/speech bubble lên ảnh | **Tài liệu bỏ sót hoàn toàn** — mà comic không có chữ thì không phải comic. Lens researcher đang tra khả năng render tiếng Việt |

## 6. Điều PM lo nhất mà tài liệu không lo

**Tài liệu đo thành công bằng "hệ thống chạy đúng", không bằng "comic đọc được".**

Toàn bộ 894 dòng nói về tính đúng đắn cơ học: state khớp, costume khớp, vũ khí không mất. Không có dòng nào về việc trang comic đó có **hay** không — pacing có nhịp, panel có đáng vẽ, người đọc có muốn lật trang. Một comic mà mọi nhân vật đều consistent nhưng nhịp truyện chán thì hệ thống *pass mọi check* và *thất bại hoàn toàn*.

Đây là failure mode nguy hiểm nhất, vì nó **vô hình đối với chính hệ thống**. Continuity Checker không bắt được nó. Không metric nào trong tài liệu bắt được nó.

**Đề xuất**: ngay từ MVP0, cạnh mọi metric kỹ thuật phải có đúng một câu hỏi con người trả lời — *"trang này đọc có ổn không?"* — và câu trả lời đó được ghi lại. Nó vừa là metric chất lượng thật, vừa là dữ liệu preference cho moat ở mục 2.

## 7. Kết luận lens Product

- **Ý tưởng có phù hợp?** Với tư cách **thiết kế kỹ thuật**: có, và ở mức trên trung bình đáng kể — nguyên tắc "spec là dữ liệu chính, ảnh là cache" là quyết định chín chắn hơn phần lớn dự án AI cùng loại. Với tư cách **sản phẩm**: chưa xác định được, vì tài liệu chưa có người dùng, chưa có vấn đề, chưa có tiêu chí thành công.
- **Rủi ro số 1**: pháp lý (nhị phân, chặn đường ra thị trường). **Rủi ro số 2**: image consistency chưa được kiểm chứng nhưng bị lên lịch kiểm chứng muộn nhất (MVP3). **Rủi ro số 3**: scope vượt xa năng lực 1 dev, đặc biệt §12 và §14.
- **Ba việc PM khuyến nghị làm trước khi viết code**: (1) trả lời OQ1 về bản quyền truyện gốc; (2) chạy MVP0 vertical slice 1 chapter/8 panel để kiểm chứng consistency; (3) viết đúng một câu định nghĩa "xong nghĩa là gì" và một tiêu chí đo được cho nó.
- **Điều đáng khen, nói rõ để không bị hiểu là phê phán một chiều**: quyết định kiến trúc ở mục cuối tài liệu (spec là dữ liệu chính) là loại quyết định mà đa số dự án bỏ qua rồi trả giá về sau. Nhận ra nó **trước** khi viết code là dấu hiệu tư duy hệ thống tốt. Vấn đề của tài liệu không phải tư duy sai, mà là **thiết kế đi trước xác thực** — và đó là thứ sửa được rẻ, ngay bây giờ.

## Mâu thuẫn với lens khác

- *(Chờ 3 lens fan-out trả về. PM sẽ điền sau khi đối chiếu — đặc biệt: định lượng effort §14 của `architect`, phản biện Layout Score của `senior-ai-engineer`, và dữ liệu consistency + pháp lý của `researcher`.)*
