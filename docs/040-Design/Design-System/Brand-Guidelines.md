---
id: DS-001
type: design-system
status: draft
project: comic-studio
owner: "@trisjr"
tags: [design-system, phase-3]
created: 2026-08-30
updated: 2026-08-30
---

# Brand Guidelines

> **Part of:** [Design MOC](../Design-MOC.md)
> **Nguồn màu & tone:** quyết định `G-1` của anh tại gate run `2026-08-30-brand-guidelines-va-design-system-comic-studio`.
> **Vị trí tài liệu:** quyết định `G-4` — map vào hàng `Design System` của [RULE-001](../../../knowledge-base/99-Templates/Documents-Template.md), ⛔ không sửa RULE-001.

> [!IMPORTANT]
> Đây là **tầng trên cùng của cùng một token graph**, ⛔ không phải một brand book độc lập. Màu thương hiệu ở đây là **nguồn** của vai trò *nhấn chính* trong [Color Tokens](./Color-Tokens.md); tone ở đây là **nguồn** của microcopy trong tầng component.
> ⭐ File này phát biểu **hướng và ranh giới**. Nó ⛔ **không đặt một giá trị nào** (hex, font, spacing) — giá trị sống ở đúng một chỗ, xem [Hệ này quản gì](#hệ-này-quản-gì---không-quản-gì).

## Mục lục

- [Hệ này quản gì / ⛔ không quản gì](#hệ-này-quản-gì---không-quản-gì)
- [Tên hiển thị](#tên-hiển-thị)
- [Audience có căn cứ](#audience-có-căn-cứ)
- [Tone & personality](#tone--personality)
- [Hướng màu chủ đạo](#hướng-màu-chủ-đạo)
- [⛔ Điều CẤM tuyệt đối trong mọi biểu đạt thương hiệu](#-điều-cấm-tuyệt-đối-trong-mọi-biểu-đạt-thương-hiệu)
- [Bề mặt takedown công khai — nghĩa vụ pháp lý, ⛔ không phải điểm chạm marketing](#bề-mặt-takedown-công-khai--nghĩa-vụ-pháp-lý--không-phải-điểm-chạm-marketing)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## Hệ này quản gì / ⛔ không quản gì

| ✅ File này **quản** | Phát biểu ở mục nào |
|---|---|
| Đối tượng được phép neo vào khi viết bất kỳ text nào của sản phẩm | [Audience có căn cứ](#audience-có-căn-cứ) |
| Tone & personality của mọi chữ trong app shell | [Tone & personality](#tone--personality) |
| **Hướng** màu chủ đạo — định tính, ⛔ không phải giá trị | [Hướng màu chủ đạo](#hướng-màu-chủ-đạo) |
| Ngôn ngữ hình ảnh được phép và bị cấm | [Tone & personality](#tone--personality) |
| ⭐ Danh sách biểu đạt **bị cấm tuyệt đối** vì lý do pháp lý | [Điều CẤM](#-điều-cấm-tuyệt-đối-trong-mọi-biểu-đạt-thương-hiệu) |
| Quy tắc brand cho bề mặt takedown công khai | [Bề mặt takedown](#bề-mặt-takedown-công-khai--nghĩa-vụ-pháp-lý--không-phải-điểm-chạm-marketing) |

| ⛔ File này **KHÔNG quản** | Ai quản |
|---|---|
| Giá trị màu cụ thể (hex / OKLCH), thang màu, cặp `-foreground`, cột dark | [Color Tokens](./Color-Tokens.md) *(file thuộc lô sau — link có chủ ý)* |
| Font, thang cỡ chữ, line-height | [Typography](./Typography.md) *(lô sau)* |
| Thang spacing, radius, breakpoint, z-index | [Spacing & Layout](./Spacing-And-Layout.md) *(lô sau)* |
| Component, ma trận state, microcopy theo từng state | [Components](./Components.md) *(lô sau)* |
| Kiến trúc token, hợp đồng phát biểu token, chuẩn a11y | [Foundations](./Foundations.md) |
| ⭐ **Wordmark · logo · favicon · OG image · avatar** | ⛔ **Bị chặn** bởi `TBD` tên hiển thị — xem [Tên hiển thị](#tên-hiển-thị) |
| Landing page / marketing site | Tài sản **tĩnh riêng**, ⛔ không dùng lại app — [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) §Consequences tiêu cực #6(a). Brand này phục vụ **app shell sau đăng nhập** trước |
| Photography style · illustration system · motion/sonic branding · merchandising · co-branding · print spec | ⛔ **Cắt khỏi phạm vi**. Lý do: đội **1 người + AI assist, ⛔ không ngân sách marketing** ([Charter](../../010-Planning/Charter-Comic-Studio.md) §7 `C1`) — mỗi mục trên đòi một tài sản phải sản xuất và bảo trì mà ⛔ không có surface nào tiêu thụ |

---

## Tên hiển thị

> [!CAUTION]
> ⛔⛔ **`TBD` — chủ: Founder (`@trisjr`).**
> ⛔ **Tài liệu này KHÔNG đề xuất bất kỳ tên nào, và ⛔ không được ai điền hộ.**

**`comic-studio` là *project name*** — [Charter](../../010-Planning/Charter-Comic-Studio.md) §1. Nó ⛔ **KHÔNG phải tên sản phẩm**, ⛔ không phải tên thương mại, ⛔ không phải wordmark. Dùng nó như **định danh repo/project**: viết thường, có gạch nối, ⛔ không viết hoa như một brand, ⛔ không đặt vào câu marketing.

**Vì sao để trống thay vì đề xuất** (`E7` của run): tên thương mại là quyết định **kinh doanh + pháp lý** (khả năng đăng ký nhãn hiệu), ⛔ ngoài thẩm quyền của cả PM lẫn agent. Bịa một tên rồi để nó lan vào wordmark + favicon + microcopy thì **đắt gấp nhiều lần** một mục phải sửa lại.

**Hệ quả dây chuyền — ⛔ tất cả đều bị chặn theo:**

| Bị chặn | Vì sao |
|---|---|
| Wordmark, logo, favicon | ⛔ Không suy ra được từ một cái tên chưa có |
| Tagline, tên miền, tên tài khoản X/Discord | Cùng lý do |
| Typography thương hiệu (font của logo) | ⛔ Không phải font UI; nó là hệ quả của wordmark |
| Bộ tài sản tối thiểu (wordmark · favicon · OG image · avatar) | Cả bốn đều phái sinh từ tên |

**Điều kiện đóng**: Founder chốt tên bằng văn bản ⇒ mở lại đúng mục này, rồi mới mở lô asset. ⛔ Không có đường tắt nào khác.

---

## Audience có căn cứ

> [!CAUTION]
> ⛔⛔ **File này có 0 dòng persona — cố ý.**
> Repo ⛔ **không có persona, không có JTBD, không có định nghĩa *"đủ tốt"***: [PRD](../../020-Requirements/PRD-Comic-Studio.md) §3.3 khai tường minh `TBD-1`…`TBD-5`, và `docs/000-Index.md` `L76` xác nhận lại. **0 user interview** (`TBD-4`), **0 willingness-to-pay study** (`TBD-5`), **0 Design partner** ([Charter](../../010-Planning/Charter-Comic-Studio.md) §6 — *"chưa có ai"*).
> ⭐ Brand Guidelines là tài liệu **dễ bịa persona nhất** trong toàn bộ SDLC, vì nó *cần* một audience để neo và một audience bịa ra **đọc rất trôi chảy**. Một persona bịa ở đây sẽ thành **nền móng giả cho cả tầng 040** — mọi Wireframe / User Flow / UI Spec sau này sẽ neo vào nó mà ⛔ không ai kiểm lại nguồn.

### Bốn actor CÓ ANCHOR — và chỉ bốn actor này

⛔ Đây **không phải persona**. Đây là danh sách *"ai đã xuất hiện trong một tài liệu có thật, kèm anchor"*. **Qualifier ở cột cuối là phần bắt buộc đọc** — nó là thứ giữ cho bốn dòng này ⛔ không bị đọc thành bốn persona.

| # | Actor | Loại | UC / tài liệu chứng minh | ⚠️ Qualifier ⛔ không được bỏ |
|---|---|---|---|---|
| **A-1** | ⭐ **Tác giả truyện chữ (writer) KHÔNG biết vẽ** | **Primary actor** của mọi UC người dùng | Primary actor ở `UC-01`…`UC-10` (**10/11 UC**); [PRD](../../020-Requirements/PRD-Comic-Studio.md) §3.1, §3.2 | `[CHỐT]` `CF-1.5`. ⛔ `CẤM-17`: **cấm đặt requirement cho phân khúc hoạ sĩ**. Đây là **phân khúc + loại trừ**, ⛔ không phải chân dung người |
| **A-2** | **Founder ở vai operator** (và vai architect) | **Secondary actor** — vận hành | `UC-01` `EXC-1` · `UC-02` `ALT-1` · `UC-03` `ALT-1` · `UC-06` `AF-1` · `UC-09` `AF-2` · `UC-10` `AF-3/AF-4/EF-3/EF-5` · `UC-11` b5–b9 | [Charter](../../010-Planning/Charter-Comic-Studio.md) §6 RACI: **A ở cả 9 nhóm hoạt động** ⇒ `bus factor = 1`. ⇒ Design System phải **rẻ để duy trì**, ⛔ không phải đẹp để trình bày |
| **A-3** | ⭐ **Chủ sở hữu quyền — BÊN NGOÀI HỆ THỐNG** | **Primary actor** của đúng **1 UC** | `UC-11` — UC **duy nhất** có primary actor là người ngoài hệ thống | ⚠️ **Chưa từng đăng ký tài khoản**, **có thể không bao giờ đăng ký**, ⛔ không thuộc tenant nào. [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `GP-3` |
| **A-4** | **Độc giả / cơ quan quản lý** | ⚠️ **⛔ KHÔNG tương tác trực tiếp với hệ thống** | Actor của `Story-AI-Disclosure-Article-11` §1; [PRD](../../020-Requirements/PRD-Comic-Studio.md) §3.2 hàng 4 | ⭐ ⛔ **Không có surface riêng.** Nó là **lý do tồn tại** của nghĩa vụ AI disclosure, ⛔ **không phải người dùng** của nghĩa vụ đó. [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `GP-4` |

### Ba thứ trông giống actor mà ⛔ KHÔNG phải actor

| ⛔ Không phải actor | Vì sao | Nguồn |
|---|---|---|
| ⚠️ **"Power user"** | *"⛔ **không phải một persona mới**… nó là **một trạng thái sử dụng**"* — người vượt ngưỡng ~125 ảnh/tháng | `UC-10` §1 |
| **Vendor billing** | *"là **hệ thống ngoài**, ⛔ không phải actor người"* | `UC-10` §1 |
| **Model provider** (Google / BFL) | *"⛔ **không phải participant**… là ràng buộc ngoài, ⛔ không đàm phán được"* | [Charter](../../010-Planning/Charter-Comic-Studio.md) §6 |

### ⛔ Bốn thứ KHÔNG được neo vào — kể cả khi câu văn nghe hợp lý

| # | ⛔ Cấm neo vào | Vì sao |
|---|---|---|
| 1 | Tuổi · giới tính · thu nhập · vị trí địa lý của người dùng | `TBD-1` — ⛔ **không tồn tại trong repo** |
| 2 | *"Người dùng của chúng ta thích phong cách X"* | `TBD-3` — ⛔ không ngưỡng nào do **người ngoài** đặt |
| 3 | *"Người dùng chấp nhận chờ Y giây"* | [PRD](../../020-Requirements/PRD-Comic-Studio.md) §3.3 hệ quả 1 nêu **đích danh** câu này là câu ⛔ không có căn cứ để viết |
| 4 | ⭐ Bất kỳ tone-of-voice nào **suy ra từ một chân dung người dùng** | Sẽ tạo **nguồn sự thật giả ở tầng 040 mà tầng 020 ⛔ không có**. ⇒ Tone ở file này neo vào `G-1` (**quyết định của anh**), ⛔ không neo vào audience — xem [Tone & personality](#tone--personality) |

**Proxy duy nhất repo có** cho *"đủ tốt"* — và nó ⛔ **không** đóng `TBD-1/2/3`: cạnh **mọi** metric kỹ thuật phải có **đúng một câu người trả lời**: ***"trang này đọc có ổn không?"*** ([PRD](../../020-Requirements/PRD-Comic-Studio.md) §3.3 · `SRS-NFR-18`). ⚠️ PRD nói thẳng: *"Proxy này **KHÔNG phải persona**. Nó là một ngưỡng chấp nhận do **chính người build** đưa ra."*

**Cơ chế đã được thiết kế sẵn để đóng khoảng trống**: **KR4.3** ([OKRs](../../010-Planning/OKRs.md) §3) — **20 cuộc trò chuyện 1-1 có ghi chép** với tác giả, trước **31/12/2026**. *"Đầu ra của KR4.3 là đầu vào để viết lại mục 3"* của PRD. ⇒ ⛔ Không lấp khoảng trống bằng cách viết văn; lấp bằng KR4.3.

---

## Tone & personality

> **Nguồn: `G-1` — quyết định của anh tại gate.** ⛔ Không suy ra từ đặc điểm người dùng (bị cấm ở [bảng trên](#audience-có-căn-cứ), mục 4).

**Ba tính từ:** **điềm tĩnh** · **tin cậy** · **⛔ không ồn ào**.

**Lý do neo — ⛔ không phải sở thích thẩm mỹ**: sản phẩm **luôn hiển thị artwork comic nhiều màu** ngay trong editor và preview. Giọng UI to — chữ lớn, câu cảm thán, màu mạnh, animation nhiều — **cạnh tranh với chính nội dung người dùng đang đánh giá**. Người dùng mở màn hình này để trả lời *"trang này đọc có ổn không?"*; mọi thứ khác phải lùi lại.

| ✅ Nên | ⛔ Không |
|---|---|
| Câu ngắn, động từ trước, nói đúng chuyện đang xảy ra | Câu cảm thán, dấu chấm than, *"Tuyệt vời!"*, *"Xin chúc mừng!"* |
| Nói thẳng khi có chi phí phát sinh, ⛔ không làm mềm | Uyển ngữ che chi phí (*"chỉ vài credit thôi"*) |
| ⭐ Nói thẳng khi người dùng đang tương tác với AI | Giấu, gộp vào ToS, hoặc ghi mờ ở chân trang |
| Gọi đúng tên thứ hệ thống thực sự làm | Nhân cách hoá AI (*"trợ lý của bạn đã suy nghĩ và…"*) |
| Trung tính khi báo lỗi: chuyện gì xảy ra + làm gì tiếp | Đổ lỗi cho người dùng, hoặc xin lỗi dài dòng |
| ⛔ Không hứa điều chưa kiểm | Bất kỳ khẳng định tuân thủ nào — xem [Điều CẤM](#-điều-cấm-tuyệt-đối-trong-mọi-biểu-đạt-thương-hiệu) |

> ⭐ **Disclosure-first là một phần của brand, ⛔ không phải một dòng chân trang.** [Charter](../../010-Planning/Charter-Comic-Studio.md) §7 `C5` + `SRS-FR-40` (user **phải nhận biết** đang tương tác với hệ thống AI). Đây là chỗ **brand và compliance trùng nhau**: AI-disclosure indicator hiển thị **tại điểm tương tác** và ⛔ **không được có biến thể ẩn/tắt được** — component đặc tả ở [Components](./Components.md) *(lô sau)*.
> ⚠️ ⛔ **Đừng gộp** *"AI disclosure"* (nghĩa vụ theo Điều 11) với *"disclosure-first positioning"* (định vị). Cùng chữ, **hai khái niệm** — cảnh báo có sẵn trong [Glossary](../../999-Resources/Glossary.md).

**Ngôn ngữ hình ảnh:**

| ⛔ Cấm | Vì sao |
|---|---|
| Mượn code hình của **công cụ vẽ**: brush stroke, palette hoạ sĩ, canvas texture, bút cảm ứng, bảng vẽ | Positioning **bắt buộc** là *"nhắm writer, ⛔ không nhắm artist"* ([Charter](../../010-Planning/Charter-Comic-Studio.md) §7 `C5`). Một brand trông như công cụ vẽ là **tự đặt mình vào cộng đồng đã có tiền lệ tẩy chay** (`CF-5.6`: Naver Webtoon bị boycott; BlueLine Studio bị buộc vẽ lại) |
| Nói với / marketing vào **cộng đồng hoạ sĩ**; tagline kiểu *"dành cho người sáng tạo hình ảnh"* | [Charter](../../010-Planning/Charter-Comic-Studio.md) §7 `C5` (*"cấm marketing vào cộng đồng hoạ sĩ"*) + [OKRs](../../010-Planning/OKRs.md) §6 `AG-2` (*"kênh cộng đồng là kênh **CÓ RỦI RO NGƯỢC**, ⛔ không trung tính"*) — **CHỐT** |

**Thứ tự bề mặt phải trông tốt** (⛔ không phải thứ tự ngẫu nhiên): **app shell sau đăng nhập** → **screenshot** → **OG image / avatar** → landing page. Kênh đã có bằng chứng là build-in-public và cộng đồng tác giả; toàn bộ sản phẩm nằm **sau đăng nhập** ([ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) §Alternatives **E**: *"SEO không phải yêu cầu"*).
⚠️ Mọi screenshot chứa ảnh do AI sinh **phải kèm disclosure** — hệ quả trực tiếp của `SRS-FR-39`/`SRS-FR-40`, áp cả cho ảnh dùng ngoài sản phẩm.

---

## Hướng màu chủ đạo

> **`G-1` — chốt tại gate:** nền **trung tính**, accent **lạnh (xanh / indigo)**.

**Ba lý do — mỗi lý do đủ để giữ hướng này:**

| # | Lý do |
|---|---|
| **1** | ⭐ **Artwork là nội dung; chrome phải lùi.** Editor và preview **luôn** hiển thị comic nhiều màu. UI màu mạnh **cạnh tranh với chính nội dung người dùng đang đánh giá** |
| **2** | **Accent lạnh tách bạch được với dải màu cảnh báo.** Hệ alert ba mức xuất hiện ở **13 surface** — nếu accent thương hiệu rơi vào dải hổ phách/đỏ/xanh lá của trạng thái, người dùng ⛔ không phân biệt được *"đây là hành động chính"* với *"đây là cảnh báo"* |
| **3** | **Preview trang comic có nền trắng giấy** (`G-2`). Nền chrome trung tính giữ cho cảm nhận độ sáng/tương phản của trang ⛔ không bị lệch |

**Câu hỏi kiểm bắt buộc** cho **mọi** lựa chọn màu ở lô sau — hỏi trước khi chốt một giá trị:
> ***"Màu này có cạnh tranh với artwork mà người dùng đang đánh giá không? Nó có bị nhầm với một mức cảnh báo không?"***

**Ràng buộc kế thừa xuống [Color Tokens](./Color-Tokens.md)** *(file thuộc lô sau — link có chủ ý)*:

1. Accent thương hiệu là **nguồn** của vai trò *nhấn chính* (`--primary` — ⚠️ tên biến là **quyết định Phase 3**, hợp đồng đặt tên ở [Foundations](./Foundations.md)).
2. ⛔ **Không** dùng dải màu của trạng thái (success / warning / danger) làm accent thương hiệu.
3. ⛔ **Không** dùng màu bão hoà cao cho bề mặt lớn của chrome.
4. Mọi giá trị phải khai **đủ cặp light/dark** (`G-2`) và **đủ cặp nền/chữ** — luật hình dạng ở [Foundations](./Foundations.md).

> ⛔ **File này KHÔNG đặt một giá trị màu nào.** Hex/OKLCH, thang primitive, semantic mapping, cột dark, bảng audit contrast — **tất cả** ở [Color Tokens](./Color-Tokens.md). Định nghĩa trùng chỗ = hai nơi phải đồng bộ cho cùng một giá trị.

---

## ⛔ Điều CẤM tuyệt đối trong mọi biểu đạt thương hiệu

> [!CAUTION]
> ⛔⛔ **`SRS-NFR-15` — mức độ rắn CHỐT.** Hệ thống **KHÔNG được** có bộ phát hiện *"truyện này có thể có bản quyền của người khác"* — ⛔ copyright detection, ⛔ plagiarism check, ⛔ similarity scan, ⛔ chấm điểm/gắn cờ *"nghi vấn bản quyền"* — **trước khi có xác nhận của luật sư**.
> ⇒ **Hệ quả lên tầng biểu đạt**: ⛔ **không được tồn tại bề mặt UI hay câu marketing nào biểu đạt phán đoán bản quyền.** Nguồn: [Spec-Security-Legal-Compliance](../../030-Specs/Security/Spec-Security-Legal-Compliance.md) §5.

### Sáu thứ bị cấm ĐÍCH DANH

| # | ⛔ Cấm | Trông như thế nào khi bị vi phạm |
|:--:|---|---|
| **1** | Badge / nhãn ***"đã kiểm bản quyền"*** (và mọi biến thể: *"đã rà soát bản quyền"*, *"copyright checked"*) | Một badge xanh cạnh trang truyện |
| **2** | **Icon shield** / `shield-check` / dấu tick ***"verified"*** gán nghĩa bản quyền | Icon set có `shield-check` dùng cho ngữ cảnh bản quyền |
| **3** | Nhãn ***"Original"*** (kể cả *"100% Original"*) | Badge *"Original"* trong bảng component |
| **4** | Messaging ***"an tâm về bản quyền"*** — và mọi câu trấn an cùng nghĩa | Tagline *"an tâm về bản quyền"* trên landing/OG image |
| **5** | Điểm rủi ro · phần trăm tương đồng · cảnh báo *"nội dung có thể trùng"* | Thanh score, nhãn *"85% similar"* |
| **6** | Khẳng định tuân thủ: *"đã tuân thủ Luật TTNT 2025"*, *"watermark hợp chuẩn"*, *"đạt chuẩn"* | Một dòng trấn an trong Brand Guidelines hoặc footer |

### ⭐ Vì sao — lý do pháp lý, ⛔ không phải khẩu vị thiết kế

Điều kiện **(a)** của miễn trừ trách nhiệm theo **Điều 198b** là ***"không biết"***.

⇒ Xây một bộ phát hiện — hoặc **hứa** rằng đã có một bộ phát hiện — **tạo ra đúng cái tri thức mà luật đang miễn trừ cho việc KHÔNG CÓ** ⇒ ⭐ **tự phá miễn trừ của chính mình** ([Spec-Security-Legal-Compliance](../../030-Specs/Security/Spec-Security-Legal-Compliance.md) §5.1).

⚠️ **Đây là chỗ phản xạ nghề nghiệp làm ngược.** Nguồn nói thẳng: *"Một dev sẽ làm ngược điều này theo bản năng, vì **'chủ động kiểm tra' nghe như hành vi có trách nhiệm**"*. Với brand thì cám dỗ còn mạnh hơn — *"an tâm về bản quyền"* là câu bán hàng dễ viết nhất của cả ngách này. **Ở hệ thống này, chính câu đó gây thiệt hại.**

⇒ Xử lý khi có đề xuất kiểu này ở bất kỳ lô nào sau: **từ chối tại review**, ⛔ **không thương lượng phạm vi** — nó là **VI PHẠM một requirement CHỐT**, ⛔ không phải một cải tiến (§5.2 quy tắc **2**).

Riêng mục **6** (khẳng định tuân thủ): phạm vi khoản 4 Điều 11 vẫn là `TBD` (hai cách đọc HẸP/RỘNG, ghi cả hai, ⛔ không chọn một), và `SRS-NFR-16` (SynthID có thoả nghĩa vụ đánh dấu máy đọc không) **CHƯA QUYẾT** — *"phải verify, ⛔ không giả định"*. Khẳng định tuân thủ là **hứa thay cho luật sư**.

### ✅ Ranh giới ĐƯỢC PHÉP — phân biệt bắt buộc

⭐ **Lệnh cấm áp cho *phán đoán* và *trấn an* do hệ thống tạo ra. Nó ⛔ KHÔNG áp cho việc *tiếp nhận thông tin từ bên ngoài*.**

| Việc | Cho phép? | Vì sao |
|---|:--:|---|
| Tiếp nhận và xử lý **thông báo takedown từ chủ quyền** | ✅ **ĐƯỢC** | Tri thức đến **từ bên ngoài**; xử lý trong 72h chính là điều kiện **(c)** của miễn trừ. Xem [mục dưới](#bề-mặt-takedown-công-khai--nghĩa-vụ-pháp-lý--không-phải-điểm-chạm-marketing) |
| Đọc **opt-out signal do chính chủ quyền gắn vào file** | ✅ **ĐƯỢC** | ⭐ *"Đọc nhãn ⛔ không tạo ra tri thức suy đoán."* ⚠️ **Nhưng copy phải gọi đúng tên**: *"phát hiện opt-out signal do chủ sở hữu gắn"*, ⛔ **không** đặt tên/viết thành *"kiểm tra vi phạm"* |
| Hiển thị **AI disclosure** tại điểm tương tác | ✅ **BẮT BUỘC** | `SRS-FR-40` (CHỐT); ⛔ không được có biến thể ẩn/tắt được |
| Tự **suy đoán** một nội dung *"có thể"* thuộc về ai đó | ⛔ **KHÔNG** | Là **tri thức do hệ thống tạo ra** — đúng thứ phá điều kiện (a) |

> ⚠️ **Cách kiểm — ⛔ KHÔNG phải quy tắc *"0 hit"*.**
> `grep -rniE "bản quyền|copyright|plagiar|similarity|tương đồng|đạo văn|original|shield|verified" docs/040-Design/` ⇒ ⭐ **mọi hit phải đọc lại nghĩa**, ⛔ không lướt. Hit hợp lệ **chỉ** thuộc ba loại ở bảng trên. Đặt quy tắc *"0 hit"* sẽ xoá mất chính mục takedown — thứ bắt buộc phải có.

---

## Bề mặt takedown công khai — nghĩa vụ pháp lý, ⛔ không phải điểm chạm marketing

> **`E4` của run:** hoãn quyết định *thương hiệu*, ⛔ **KHÔNG hoãn ràng buộc**.

**Bề mặt này là gì**: form takedown **CÔNG KHAI, ⛔ không cần tài khoản** (`SRS-FR-38`), ⛔ không có tenant context, chạy dưới role riêng chỉ `INSERT` ([Spec-Security-Legal-Compliance](../../030-Specs/Security/Spec-Security-Legal-Compliance.md) §6.1). Primary actor là **A-3 — người ngoài hệ thống**, ⚠️ **chưa từng đăng ký và có thể không bao giờ đăng ký**.

| Quy tắc | Nội dung |
|---|---|
| **TD-B1** | ⛔ **Không áp brand voice marketing** lên bề mặt này: ⛔ không tagline, ⛔ không CTA đăng ký, ⛔ không upsell, ⛔ không *"khám phá sản phẩm"* |
| **TD-B2** | ⛔⛔ **Không mang messaging trấn an về bản quyền** dưới bất kỳ hình thức nào (`SRS-NFR-15` — xem [Điều CẤM](#-điều-cấm-tuyệt-đối-trong-mọi-biểu-đạt-thương-hiệu)). Đây là bề mặt **cám dỗ nhất**, vì nó đang nói chuyện với đúng người quan tâm bản quyền |
| **TD-B3** | ⛔ **Không quét / flag / chấm điểm nghi vấn bản quyền** ở luồng này — §5.2 quy tắc **4** gọi đây là **cấm tuyệt đối** của luồng takedown |
| **TD-B4** | Ngôn ngữ: **rõ ràng, thủ tục, trung tính**. Người điền form có thể chưa từng nghe tên sản phẩm ⇒ ⛔ không dùng thuật ngữ nội bộ, ⛔ không giả định người đọc biết sản phẩm là gì |
| **TD-B5** | Con số **duy nhất** được viết ở bề mặt này: **SLA 72 giờ** (`CF-7.6` `[OFF]`). ⛔ Không thêm bất kỳ con số nào khác — xem `ARC-35` |
| **TD-B6** | ⚠️ **`TBD` có chủ**: bề mặt này dùng **logo/màu nào** — hoãn theo `E4`, và phụ thuộc `TBD` [tên hiển thị](#tên-hiển-thị) (chủ: **Founder**) |

> ⚠️ **Bề mặt operator ⛔ NGOÀI SCOPE** (`E5`): hai endpoint admin takedown **đang BỊ CHẶN** cho tới khi mô hình quyền được sửa (`app_operator` chưa tồn tại). ⛔ Không đặc tả UI cho một mô hình quyền chưa tồn tại — [Components](./Components.md) *(lô sau)* ⛔ không khai component operator nào.

---

## Tài liệu tham khảo

> ⚠️ **Ghi nhận minh bạch (`X-3`)**: tại **2026-08-30**, các tài liệu neo bên dưới (`ADR-001`, `ADR-013`, `SDD`, `SRS`) đều ở `status: draft`. Design System này là tài liệu tầng 040 neo vào một nền **chưa `approved`**. ⛔ Không phải việc của file này để đổi status.

**Trong Design System** *(4 file dưới thuộc lô sau — link có chủ ý, chưa tồn tại tại thời điểm viết)*:

- [Foundations](./Foundations.md) — kiến trúc token · hợp đồng phát biểu token · light/dark · chuẩn a11y
- [Color Tokens](./Color-Tokens.md) — **nguồn duy nhất** của mọi giá trị màu
- [Typography](./Typography.md) · [Spacing & Layout](./Spacing-And-Layout.md) · [Components](./Components.md)

**Ngoài Design System**:

- [Design MOC](../Design-MOC.md) — bản đồ tầng 040
- [Spec-Security-Legal-Compliance](../../030-Specs/Security/Spec-Security-Legal-Compliance.md) — §5 (`SRS-NFR-15`, anti-feature) · §5.3 ranh giới được phép · §6 bề mặt takedown
- [ADR-001 — Backend & Frontend Tech Stack](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) — §Alternatives **E** · §Consequences tiêu cực **#6(a)**
- [Charter — Comic Studio](../../010-Planning/Charter-Comic-Studio.md) — §1 (project name) · §6 RACI · §7 `C1`, `C5`
- [PRD — Comic Studio](../../020-Requirements/PRD-Comic-Studio.md) — §3.1 · §3.2 · §3.3 (`TBD-1`…`TBD-5`)
- [SRS — Comic Studio](../../020-Requirements/SRS-Comic-Studio.md) — `SRS-FR-38/39/40` · `SRS-NFR-15/16/18`
- [MVP Scope](../../010-Planning/MVP-Scope.md) — §3 `GP-3`, `GP-4` · §5.2
- [OKRs](../../010-Planning/OKRs.md) — §3 `KR4.3` · §6 `AG-2`
- [Glossary](../../999-Resources/Glossary.md) — *AI disclosure (Điều 11)* · *opt-out signal*
- [RULE-001 — Documents Template](../../../knowledge-base/99-Templates/Documents-Template.md) — §Document Type Mapping hàng **Design System** · quy tắc **#5** (⛔ không wiki-link)

**Hồ sơ quyết định của run** (`2026-08-30-brand-guidelines-va-design-system-comic-studio`):

- [run-plan.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/run-plan.md) — §Gate `G-1`…`G-4`
- [escalations.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/escalations.md) — `E2` (độc giả đích) · `E4` (takedown) · `E5` (operator) · `E7` (tên hiển thị)
- [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/findings/business-analyst.md) — §4.2 bốn actor · §4.4 bảng ⛔ không được neo vào
- [findings/product-designer.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/findings/product-designer.md) — §1.2 `B-1`…`B-4` · §2.1 bảy mục
- [findings/architect.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/findings/architect.md) — `ARC-28`…`ARC-34`
