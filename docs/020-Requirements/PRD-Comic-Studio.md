---
id: PRD-001
type: prd
status: draft
project: comic-studio
created: 2026-08-24
---

# Product Requirements Document — comic-studio

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn từ bảng Canonical Facts của tầng Planning — **số và nhãn là một cặp không tách rời**):
> `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> Nếu anh copy một con số từ tài liệu này sang ticket hay tài liệu khác, **copy cả nhãn và cả caveat đi kèm**.

> [!NOTE]
> **Trạng thái tài liệu: `draft`.** Các điều kiện chặn tại [Charter mục 9](../010-Planning/Charter-Comic-Studio.md#9-tiêu-chí-thành-công--gono-go) — **BLOCKER-01** (ba câu hỏi luật sư SHTT) cùng ba blocker phụ **BLOCKER-02 / 03 / 04** — đều **chưa được gỡ**. Đặt `approved` lúc này là một tuyên bố sai.
>
> **Tài liệu này còn một khoảng trống đã biết và được thừa nhận tường minh**: [mục 3](#3-người-dùng--vấn-đề) chưa có persona / JTBD / định nghĩa *"đủ tốt"*, vì **toàn repo không có**.

## Mục lục

1. [Executive Summary](#1-executive-summary)
2. [Bối cảnh & mục tiêu](#2-bối-cảnh--mục-tiêu)
3. [Người dùng & vấn đề](#3-người-dùng--vấn-đề)
4. [Yêu cầu chức năng theo 8 module](#4-yêu-cầu-chức-năng-theo-8-module)
5. [Yêu cầu phi chức năng](#5-yêu-cầu-phi-chức-năng)
6. [Ranh giới scope](#6-ranh-giới-scope)
7. [Success metrics](#7-success-metrics)
8. [Tài liệu liên quan](#8-tài-liệu-liên-quan)

---

## 1. Executive Summary

**comic-studio là một nền tảng SaaS thương mại multi-tenant** biến truyện chữ thành comic pages, để **người khác tự upload truyện của họ** và sinh ra trang truyện tranh `[CHỐT]` CF-1.1. Đây không phải một công cụ cá nhân, cũng không phải một content studio tự sản xuất nội dung.

Sản phẩm không đặt cược vào chất lượng ảnh — nó đặt cược vào **ba tầng dữ liệu mà đối thủ không làm rẻ được**: **Story Bible** (trạng thái tác phẩm truy vấn được theo thời điểm), **Comic IR (Comic Intermediate Representation)** (cấu trúc trang/panel có schema, tồn tại *trước* khi sinh bất kỳ ảnh nào), và **provenance chain** (hồ sơ chứng minh đóng góp của con người). Ảnh là output phái sinh; **spec là dữ liệu chính**.

Bốn sự thật nền chi phối mọi yêu cầu trong tài liệu này:

| Sự thật nền | Giá trị | Nhãn | Hệ quả lên requirement |
|---|---|---|---|
| Quy mô đội | **1 người + AI assist**, không funding, không ngân sách marketing | `[CHỐT]` CF-1.2 | Mọi scope phải chia được cho một người. Phần lớn quyết định cắt scope ở đây **không đúng** với đội 5 người |
| Trạng thái code | **Chưa có dòng nào** | `[OFF]` CF-1.3 | Không có legacy, nhưng cũng không có gì đã được kiểm chứng bằng chạy thật |
| Rủi ro lớn nhất | **Rủi ro nhị phân pháp lý** — sản phẩm có thể **bất hợp pháp**, không phải "kém hơn" | CF-7.9 | Module G không phải một nhóm tính năng, nó là **điều kiện tồn tại** |
| Ràng buộc kinh tế | Gross margin kỳ vọng **50–60%**, không phải 80% | `[BCN]` CF-3.10 | Chi phí phải đo được **trước khi** nó xảy ra ⇒ module F có mặt từ MVP1 |

**Tài liệu này trả lời đúng một câu hỏi**: *sản phẩm phải làm được những gì*. Nó **không** trả lời *"khi nào"* ([Roadmap.md](../010-Planning/Roadmap.md)), **không** trả lời *"cái gì vào MVP nào"* ([MVP-Scope.md](../010-Planning/MVP-Scope.md) là nguồn duy nhất của câu đó — tài liệu này **trích** cột mốc, không định nghĩa lại nó), và **không** đặc tả yêu cầu kỹ thuật ([SRS-Comic-Studio.md](./SRS-Comic-Studio.md)).

---

## 2. Bối cảnh & mục tiêu

### 2.1 Problem Statement

**Vấn đề nghiệp vụ**: một tác giả truyện chữ có tác phẩm nhiều chương và **không biết vẽ** `[CHỐT]` CF-1.5. Chuyển tác phẩm đó thành comic hiện đòi hoặc thuê hoạ sĩ (chi phí ngoài tầm), hoặc tự học vẽ (thời gian ngoài tầm). Công cụ sinh ảnh AI phổ thông không giải được bài toán này vì chúng sinh **từng ảnh rời**, trong khi một chương truyện đòi **nhất quán xuyên hàng trăm panel**: cùng một nhân vật, đúng trang phục của đúng thời điểm, thoại gán cho đúng người.

**Bốn điểm vỡ đã được xác định, và chúng là lý do tồn tại của bốn module đầu:**

| # | Điểm vỡ | Vì sao công cụ phổ thông không giải được | Module giải |
|---|---|---|---|
| 1 | **Consistency nhân vật xuyên panel** | Model sinh ảnh không có bộ nhớ; mô tả bằng text prompt không đủ ⇒ phải dùng `Canonical Reference` + best-of-N | A |
| 2 | **Trạng thái theo thời điểm** | Dùng `(chapter, scene)` làm khoá thời gian **sai âm thầm ở mọi flashback** (`syuzhet` vs `fabula`) | B |
| 3 | **Attribute binding trong panel nhiều người** | Thất bại gần hoàn toàn từ 4 nhân vật: ảnh trông hợp lý nhưng **gắn sai trang phục cho sai người** `[OFF]` CF-6.5 | C |
| 4 | **Chữ tiếng Việt và quyết định của con người** | Model render chữ vào ảnh ⇒ sửa một câu thoại = một lần regenerate ảnh (đốt tiền), và **mất phần được bảo hộ bản quyền** | A + D |

**Vấn đề pháp lý — và đây là điểm khác biệt bản chất so với một sản phẩm AI thông thường.** Theo **Nghị định 134/2026/NĐ-CP** hiệu lực **09/04/2026**, **Điều 5a**: tác phẩm AI-assisted **chỉ** được bảo hộ nếu con người có *"substantial and decisive intellectual contribution"*; tác phẩm **do AI tạo hoàn toàn KHÔNG được bảo hộ**, kèm nghĩa vụ lưu **prompts, inputs, intermediate drafts** `[OFF]` CF-7.1–7.3. ⇒ Bảng `Generation` và `change_log` **không phải feature engineering, mà là compliance artifact**, và chúng **không backfill được**.

### 2.2 Goals

Năm mục tiêu dưới đây **trích nguyên** từ [Charter mục 3](../010-Planning/Charter-Comic-Studio.md#3-mục-tiêu-dự-án). PRD **không đặt mục tiêu mới**.

| # | Mục tiêu | Chỉ số | Ngưỡng | Nhãn |
|---|---|---|---|---|
| **MT-1** | Biết tiền đề còn đứng hay không, trong **1–2 tuần** và **~$12** | MVP0 chạy xong 1 chapter, trả lời được cả ba chỉ số CF-8.5 | Hoàn thành **1–2 tuần**, chi phí **≤ ~$12** | `[EM tính từ OFF]` CF-3.11 |
| **MT-2** | Đo được thứ **chưa ai đo**: human-reject rate sau VLM-select | Tỷ lệ panel bị người bác bỏ sau khi VLM đã chọn | Ngưỡng PASS định tại gate **G1** | ⭐ **chưa ai công bố con số này** |
| **MT-3** | Xác nhận hàng load-bearing: multi-character panel **2–3 nhân vật** | Đo trực tiếp trên panel có 2–3 nhân vật | Ngưỡng PASS định tại gate **G1** | `[OFF]` CF-6.4 — **không benchmark độc lập nào đo frontier model ở mức này** |
| **MT-4** | Hạ N tối thiểu — mỗi bậc N giảm được là **~33% COGS** | N nhỏ nhất còn giữ chất lượng; regen ratio **p50/p90** | Mặc định **N=3**; mục tiêu là **đo**, không phải giả định giảm được | `[OFF]` CF-3.1 |
| **MT-5** | Doanh thu năm 1 nằm **trong dải SOM**, không vượt ra ngoài | MRR và số paying user | Thang **trăm đô/tháng**, không phải nghìn — dải cụ thể ở [OKRs](../010-Planning/OKRs.md#4-preview-q12027) | ⚠️ `[EM]` CF-4.4 |

**Chín điều kiện khả thi (R1–R9)** — verdict thẩm định là **KHẢ THI CÓ ĐIỀU KIỆN, chín điều kiện phải thoả ĐỒNG THỜI** (CF-6.1). Chúng là **ràng buộc trên requirement**, không phải requirement, và nằm ở [Charter mục 4](../010-Planning/Charter-Comic-Studio.md#4-yêu-cầu-cấp-cao). Bảng dưới chỉ ánh xạ chúng vào module để truy vết:

| Điều kiện | Nội dung ngắn | Module thực thi |
|---|---|---|
| **R1** | ≤3 nhân vật/panel, cứng hoá trong Comic IR | C |
| **R2** | Chữ đi qua **typeset layer** riêng, không nhúng vào ảnh AI | A + D |
| **R3** | User warrant + indemnify + safe harbour Điều 198b (**SLA 72 giờ** `[OFF]`) | G |
| **R4** | AI disclosure — nghĩa vụ **nội địa Việt Nam** | G |
| **R5** | Pricing metered / BYOK, **không** subscription phẳng | F |
| **R6** | Tư vấn luật sư SHTT **TRƯỚC khi thương mại hoá** | G (ngoài phạm vi code) |
| **R7** | Budget COGS ở hệ số **N=3**, không 2× | F |
| **R8** | Deterministic hoá bốn transform — ranh giới LLM / code tất định | A + B |
| **R9** | HITL gate + eval kit ở **MVP1**, không phải MVP4 | H |

> ⚠️ [Analysis §4.1](../050-Research/Analysis-Comic-Studio-Concept.md) đặt tiêu đề *"BẢY điều kiện"* — đó là số của **một lens**. **Số phải thoả là CHÍN.** Đếm bảy khi lập kế hoạch là bỏ sót hai điều kiện.

### 2.3 Non-Goals

Đây là những thứ **cố ý không làm**, kèm lý do. Khác với *"chưa ưu tiên"* — non-goal là quyết định đã cân nhắc, ghi ra để không ai âm thầm làm nó.

| # | KHÔNG làm | Vì sao | Neo |
|---|---|---|---|
| **NG-1** | **Nhắm phân khúc hoạ sĩ (artist)** | Phân khúc đã chốt là tác giả truyện chữ **không biết vẽ**; cộng đồng vẽ có tiền lệ **boycott** và **buộc vẽ lại** tác phẩm dính AI `[TC]` | `[CHỐT]` CF-1.5 · CF-5.6 · CẤM-17 |
| **NG-2** | **Subscription phẳng unlimited; free tier kiểu *"100 ảnh/ngày"*** | ⛔ Mâu thuẫn trực tiếp với R5. Một power user xoá margin của bốn user thường | ⛔ CF-2.7 |
| **NG-3** | **Trở thành content studio** (tự sản xuất và phát hành truyện) | Khác loại hình. Đó là mô hình Dashtoon — và **không dùng giá Dashtoon làm neo pricing** | `[TC]` CF-5.1 |
| **NG-4** | **Huấn luyện model riêng trên nội dung user** | Không tạo model mới, không lưu nội dung vào weights — đây **chính là** lập luận pháp lý của dự án. Phá nó là phá luôn phòng tuyến TDM | [Analysis §8.5](../050-Research/Analysis-Comic-Studio-Concept.md) |
| **NG-5** | **Render text tiếng Việt trực tiếp vào ảnh AI** | Loại trừ theo R2, **kể cả khi model làm được** | `[Charter §5.2](../010-Planning/Charter-Comic-Studio.md#52-scope-out--không-thuộc-về-sản-phẩm)` |
| **NG-6** | **Đua trục editor với đối thủ có funding** | Họ đánh trục **editor**; comic-studio đánh trục **Story Bible + Timeline State + Continuity** — trục duy nhất mà quy mô 1 dev có lợi thế | `[TC]` CF-5.2–5.3 · [OKRs AG-6](../010-Planning/OKRs.md#6-anti-goals) |
| **NG-7** | **Hạ N=3 xuống thấp hơn để cứu margin** | **best-of-N ≠ retry-on-failure.** *Không thể lấy chất lượng của N=3 mà tính chi phí của N=2* `[OFF]`. Hạ N ⇒ **phải chạy lại G1**, không chỉ G2 | `[OFF]` CF-3.1/3.2 · CẤM-03 |
| **NG-8** | **Dùng TAM làm căn cứ biện minh hoặc neo cho bất kỳ requirement nào** | TAM webtoon đo **tiêu thụ nội dung**; comic-studio **không lấy tiền từ độc giả**. Trích nó là **lỗi logic**, không phải sự lạc quan | ⛔ CẤM-02 · [OKRs AG-5](../010-Planning/OKRs.md#6-anti-goals) |

> Tám anti-goal đầy đủ ở [OKRs mục 6](../010-Planning/OKRs.md#6-anti-goals). Bảng trên là các anti-goal **có hệ quả trực tiếp lên requirement**; PRD không lặp lại các anti-goal thuần về kênh phân phối.

---

## 3. Người dùng & vấn đề

> [!CAUTION]
> **Đọc mục 3.3 TRƯỚC khi dùng mục 3.1 và 3.2.** Mục này là **khoảng trống lớn nhất của cả tầng Requirements**, và nó được ghi ra tường minh thay vì được lấp bằng phỏng đoán.

### 3.1 Phân khúc — đã chốt

| | |
|---|---|
| **Phân khúc** | **Tác giả truyện chữ (writer) KHÔNG biết vẽ** |
| **Nhãn** | `[CHỐT]` CF-1.5 |
| **Loại trừ tường minh** | ***không* nhắm hoạ sĩ (artist)** — xem [NG-1](#23-non-goals) |
| **Hệ quả cứng lên tầng Requirements** | **Primary actor của MỌI Use Case người dùng là actor này.** ⛔ **Cấm** viết Use Case cho actor *"hoạ sĩ"* (CẤM-17) |

> [!WARNING]
> **Phân khúc ≠ persona.** *"Tác giả truyện chữ không biết vẽ"* trả lời câu **ai không phải khách hàng**. Nó **không** trả lời: người đó bao nhiêu tuổi, viết trên nền tảng nào, đã trả tiền cho công cụ gì, một chương của họ dài bao nhiêu, họ chấp nhận bỏ bao nhiêu phút cho một trang, và **họ gọi cái gì là "đủ tốt"**. Bốn thứ sau là đầu vào bắt buộc của Acceptance Criteria — và repo không có.

### 3.2 Bốn actor đã xuất hiện trong repo

Bảng dưới chỉ liệt kê actor **đã có mặt trong một tài liệu có thật của repo**, kèm anchor. Không actor nào được suy ra.

| Actor | Vai trò trong hệ thống | Xuất hiện ở đâu trong repo |
|---|---|---|
| **Tác giả truyện chữ** (không biết vẽ) | **Primary actor** của toàn bộ luồng nghiệp vụ: upload chapter → duyệt Story Bible → duyệt panel script → sinh panel & chọn variant → hai human gate → typeset → export | `[CHỐT]` CF-1.5 · [MVP-Scope §1.2](../010-Planning/MVP-Scope.md#12-bối-cảnh-không-được-quên-khi-đọc) |
| **Founder** — ở vai **operator** và vai **architect** | Vận hành hệ thống (job queue, fairness, hold reaper, quota, incident) và quyết định kiến trúc/dữ liệu. **Là `A` (Accountable) ở cả 9 nhóm hoạt động** ⇒ `bus factor = 1` | [Charter §6 RACI](../010-Planning/Charter-Comic-Studio.md#6-stakeholder-matrix-raci) |
| **Chủ sở hữu quyền (bên ngoài)** | Gửi yêu cầu hạ nội dung; **không** phải người dùng của sản phẩm nhưng **có quyền tạo nghĩa vụ** cho nền tảng trong **SLA 72 giờ** `[OFF]` | `MVP-Scope §3` hàng **GP-3** · CF-7.6 · Charter **BLOCKER-02** |
| **Độc giả / cơ quan quản lý** | Người/tổ chức mà nghĩa vụ **AI disclosure** hướng tới. Không tương tác trực tiếp với hệ thống, nhưng là lý do tồn tại của `FR-G-04` | `MVP-Scope §3` hàng **GP-4** · `[OFF]` CF-7.7 · Charter **C4** |

> **Founder ở vai operator/architect là actor thật, không phải một quy ước trình bày.** Nhiều yêu cầu trong [mục 4](#4-yêu-cầu-chức-năng-theo-8-module) — job queue, fairness per tenant, hold reaper, RLS, adapter provider — có actor là Founder, **không** phải tác giả truyện chữ. Gán sai actor cho các yêu cầu này sẽ sinh ra Use Case và Story sai đối tượng.

### 3.3 ⭐ `TBD` — persona, JTBD và định nghĩa *"đủ tốt"*

> [!CAUTION]
> **Trạng thái: `TBD`. Không có nguồn nào trong repo trả lời được ba câu dưới đây, và điều đó đã được xác minh.**

| # | Cái đang thiếu | Bằng chứng khoảng trống trong repo |
|---|---|---|
| **TBD-1** | **Persona** — không có một persona nào cho sản phẩm này | [Analysis §3.2](../050-Research/Analysis-Comic-Studio-Concept.md) gọi thẳng: thiết kế gốc *"có data model 13 entity và không có một dòng nào về **ai là người dùng**, **vấn đề gì đang được giải**, và **'đủ tốt' nghĩa là gì**"* |
| **TBD-2** | **JTBD (Jobs To Be Done)** — không có mô tả công việc thật mà người dùng đang cố hoàn thành, cũng không có công cụ hiện tại họ đang dùng thay thế | Cùng nguồn trên · [Analysis §11 OQ3](../050-Research/Analysis-Comic-Studio-Concept.md) |
| **TBD-3** | **Định nghĩa *"đủ tốt"*** — không có ngưỡng chấp nhận nào do **người ngoài** đặt ra | [Charter §6](../010-Planning/Charter-Comic-Studio.md#6-stakeholder-matrix-raci) ba lỗ hổng: *"không Design partner nghĩa là **mọi phán đoán về 'đủ tốt' đang do chính người build đưa ra**"* |
| **TBD-4** | **Không có Design partner, không có một user interview nào** | [Charter §6](../010-Planning/Charter-Comic-Studio.md#6-stakeholder-matrix-raci): *"chưa có ai"* · `docs/050-Research/User-Interviews/` **rỗng** |
| **TBD-5** | **Không có willingness-to-pay study** cho tác giả web novel với tool adapt truyện | [Analysis §11](../050-Research/Analysis-Comic-Studio-Concept.md): *"khoảng trống nằm dưới nền của câu 'bán được không'"* |

**Cần gì để đóng `TBD` này**: **user interview với tác giả truyện chữ thật**. Repo đã có một cơ chế được thiết kế sẵn cho việc đó — **KR4.3** ở [OKRs §3](../010-Planning/OKRs.md#3-q42026--chu-kỳ-chính) yêu cầu **20 cuộc trò chuyện 1-1 có ghi chép** với tác giả trước **31/12/2026**, mỗi cuộc ghi *họ đang dùng gì, trả bao nhiêu, đau ở đâu*. ⇒ **Đầu ra của KR4.3 là đầu vào để viết lại mục 3 này.**

**Hệ quả của việc thiếu — nói thẳng, bốn hệ quả:**

| # | Hệ quả | Ảnh hưởng tới tài liệu nào |
|---|---|---|
| 1 | **Mọi Use Case phải để `Preconditions` ở mức phân khúc, không ở mức persona.** Không có căn cứ để viết *"người dùng đã quen với X"* hay *"người dùng chấp nhận chờ Y giây"* | 11 Use Case, mục *Preconditions* |
| 2 | **Acceptance Criteria không có ngưỡng usability do người ngoài đặt.** Mọi ngưỡng UX trong tầng này là ngưỡng **tự đặt**, phải mang nhãn `[EM]` | Toàn bộ AC của Story · SRS/NFR mục usability |
| 3 | **Không phân biệt được *"tính năng thiếu"* với *"tính năng không ai cần"*.** Đây đúng là failure mode mà [Analysis §3.2](../050-Research/Analysis-Comic-Studio-Concept.md) chỉ ra: sản phẩm **pass mọi check mà không ai muốn đọc** — lỗi **vô hình đối với chính hệ thống** | Ưu tiên backlog |
| 4 | **Rủi ro thiết kế theo cái mình muốn build.** Founder là `A` ở cả 9 hàng RACI và không có `C` nào tồn tại ở hàng *Định hướng sản phẩm* và *Kiểm thử & nghiệm thu* | Cấp dự án — thuộc [Risk-Register.md](../010-Planning/Risk-Register.md) |

**Proxy tạm dùng cho tới khi có persona thật** — đây là thứ gần nhất mà repo có với một định nghĩa *"đủ tốt"*, và nó **được ghi từ MVP0**:

> Cạnh **mọi** metric kỹ thuật phải có **đúng một câu người trả lời**: ***"trang này đọc có ổn không?"*** — và câu trả lời **được ghi lại từ MVP0**. Lỗi *"pass mọi check mà không ai muốn đọc"* là **vô hình đối với chính hệ thống**: Continuity Checker không bắt được, và không metric kỹ thuật nào bắt được. Nó vừa là metric chất lượng thật, **vừa** là preference data cho moat.
>
> — nguồn: [Analysis §3.2](../050-Research/Analysis-Comic-Studio-Concept.md), thực thi tại `FR-H-06` và `FR-H-02`

⚠️ **Proxy này KHÔNG phải persona.** Nó là một ngưỡng chấp nhận do **chính người build** đưa ra. Nó **giảm nhẹ** hệ quả số 3 ở bảng trên, **không** đóng `TBD-1` / `TBD-2` / `TBD-3`.

---

## 4. Yêu cầu chức năng theo 8 module

### 4.0 Cách đọc mục này — bốn quy ước

**1. Nguồn.** Mọi hàng trong tám bảng dưới đây truy về **[MVP-Scope §3 — Bảng MVP vs Full Scope](../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope)**. PRD **không tạo yêu cầu mới** và **không định nghĩa lại mốc MVP** — cột *Mốc MVP* là bản trích.

**2. Ký hiệu mốc** (giữ nguyên của `MVP-Scope §3`): ✅ có đầy đủ · 🟡 có một phần / bản tối thiểu · ⛔ hoãn sang mốc sau · ❌ chưa có ở mốc đó. **Horizon** là **09/2026 → 02/2027** `[CHỐT]` CF-8.1, và theo `[EM]` CF-10.8 nó chứa được **MVP0 · MVP1 · MVP2**; **MVP3 và MVP4 rơi ra ngoài** ⇒ cột *Mốc MVP* ghi `NGOÀI horizon` cho các hàng hoàn tất ở MVP3/MVP4.

**3. Quy tắc phân chia — viết ra để không ai phải tự suy lại:**

| Điều kiện của một hàng `MVP-Scope §3` | Xử lý |
|---|---|
| Có **✅** hoặc **🟡** ở **bất kỳ** mốc MVP0–MVP4 | ⇒ sinh yêu cầu chức năng, nằm ở bảng của module tương ứng |
| **Chỉ** có ❌ / ⛔ xuyên suốt MVP0–MVP4 | ⇒ **không** sinh yêu cầu, ghi tại [mục 6](#6-ranh-giới-scope) |

**Kiểm đếm**: `MVP-Scope §3` có **51 hàng** → **42 hàng** vào tám bảng dưới (sinh **48 FR**, vì `D1` tách thành 5 theo [MVP-Scope §5.2](../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas) và `C7` tách thành 2, cộng một FR cho ràng buộc xuyên suốt của editor) · **9 hàng** vào [mục 6](#6-ranh-giới-scope). **Không hàng nào rơi im lặng** — mỗi bảng có một dòng *Ánh xạ hàng nguồn* ngay bên dưới.

**4. Cấu trúc tám H3 dưới đây là contract cứng.** 8 Epic trỏ vào anchor của tám heading này bằng `Implements:`. **Đổi tên hoặc đổi thứ tự H3 ⇒ 8 link Epic chết.**

---

### A. Pipeline sinh ảnh

> **BRD**: [BRD-001-Image-Generation-Pipeline](./BRD/BRD-001-Image-Generation-Pipeline.md) · **Epic**: [Epic-Image-Generation-Pipeline](../022-User-Stories/Epics/Epic-Image-Generation-Pipeline.md)
>
> *Business goal*: sinh được panel có nhân vật nhất quán từ một `Panel Specification`, ở chi phí và chất lượng cho phép bán được. Đây là module **duy nhất** tạo ra artifact mà khách hàng nhìn thấy.

| ID | Yêu cầu | Mô tả | Mốc MVP | Căn cứ |
|---|---|---|---|---|
| **FR-A-01** | Generate panel: reference + N candidate + VLM select | Sinh **N=3** ứng viên cho **mọi** panel từ `Canonical Reference` của nhân vật, rồi để VLM autorater chọn 1. ⚠️ **best-of-N, KHÔNG phải retry-on-failure** — chạy trên mọi panel như mặc định, không chỉ khi panel lỗi. Nhầm hai khái niệm này là nguồn của sai số chi phí **+50%** | MVP0 ✅ (spike) → MVP1–2 ⛔ → MVP3 ✅ (**NGOÀI** horizon) | `MVP-Scope §3` **A1** · CF-8.4 (*"code MVP0 làm đúng một việc này"*) · **N=3** `[OFF]` CF-3.1/3.2 — *"performance saturates at N=3"* |
| **FR-A-02** | Typeset layer + bubble overlay | Thoại render bằng **tầng chữ tách khỏi ảnh**, không nướng vào pixel. Ảnh được sinh **không có chữ** (`text, letters, watermark, speech bubble` vào negative prompt); bubble và thoại render bằng code lên trên. Không có tầng này thì sửa một câu thoại = một lần regenerate ảnh | MVP0 🟡 thô → MVP1–2 🟡 → MVP3 ✅ (**NGOÀI** horizon) | `MVP-Scope §3` **A2** · CF-8.11c — *"nổ ngay ở panel có thoại đầu tiên, tức trong MVP0"* · điều kiện khả thi **R2** |
| **FR-A-03** | Visual Prompt Compiler **deterministic** | Biến `Panel Specification` thành prompt bằng **code tất định**, không LLM ở runtime: tra bảng `field value → cụm từ`, sắp thứ tự, dedup, xử lý xung đột theo **precedence ladder**, thực thi **constraint budget**, ghi log ràng buộc bị drop. Cùng một spec **luôn** cho ra cùng một prompt ⇒ panel sai là do spec sai, không do hệ thống ngẫu nhiên | MVP0 🟡 script → MVP1–2 🟡 → MVP3 ✅ (**NGOÀI** horizon) | `MVP-Scope §3` **A3** · [Analysis §5.5](../050-Research/Analysis-Comic-Studio-Concept.md) — compiler deterministic là **điều kiện cần** để bảng `Generation` có nghĩa · **R8** |
| **FR-A-04** | Adapter đa provider | Đổi image provider bằng cách thay **adapter**, không sửa lõi. Giá đầu vào **do provider đặt, không đàm phán được** ⇒ đổi giá không được khoá cứng sản phẩm | MVP0 🟡 1 adapter → MVP1–2 ⛔ → MVP3 ✅ (**NGOÀI** horizon) | `MVP-Scope §3` **A4** · [Analysis §6.2](../050-Research/Analysis-Comic-Studio-Concept.md) seam #4 · `[OFF]` CF-3.4 |
| **FR-A-05** | Job queue trong Postgres | Enqueue job **trong cùng transaction** với dữ liệu nghiệp vụ; claim bằng `FOR UPDATE SKIP LOCKED`. Không job mồ côi, và không thêm một hạ tầng queue riêng | MVP0 ❌ (không có database) → **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **A5** · CF-9.2 · [Analysis §6.2](../050-Research/Analysis-Comic-Studio-Concept.md) — MVP0 là script + file phẳng |
| **FR-A-06** | Fairness per tenant trong câu CLAIM job | Một tenant **không** chiếm hết worker; tenant khác không thấy sản phẩm treo | MVP0–2 ⛔ → MVP3 ✅ (**NGOÀI** horizon) | `MVP-Scope §3` **A6** · [Analysis §6.2](../050-Research/Analysis-Comic-Studio-Concept.md) *seam kinh tế* — *"nhồi vào sau là sửa đúng câu SQL nóng nhất"* |
| **FR-A-07** | **Whole-page render granularity** | Compile **nhiều** panel spec thành **MỘT** prompt whole-page. Là **đường lui đã thiết kế sẵn** của gate G2: `Panel Specification` không mất giá trị vì nó là *spec*, không bắt buộc mỗi panel một lần gọi model ⇒ **data model KHÔNG phải đổi** | MVP0–2 ⛔ → MVP3 🟡 tuỳ chọn → MVP4 ✅ (**NGOÀI** horizon) | `MVP-Scope §3` **A7** · [MVP-Scope §7.3](../010-Planning/MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1) đường lui #1 · [Analysis §9b.3](../050-Research/Analysis-Comic-Studio-Concept.md) |

> **Ánh xạ hàng nguồn**: `A1 → FR-A-01` · `A2 → FR-A-02` · `A3 → FR-A-03` · `A4 → FR-A-04` · `A5 → FR-A-05` · `A6 → FR-A-06` · `A7 → FR-A-07`. **7/7 hàng nhóm A có mặt.**

---

### B. Story Intelligence

> **BRD**: [BRD-002-Story-Intelligence](./BRD/BRD-002-Story-Intelligence.md) · **Epic**: [Epic-Story-Intelligence](../022-User-Stories/Epics/Epic-Story-Intelligence.md)
>
> *Business goal*: biến văn bản truyện thô thành **Story Bible** truy vấn được **theo thời điểm** — tài sản tích luỹ của người dùng, switching cost, và ứng viên moat thật.

| ID | Yêu cầu | Mô tả | Mốc MVP | Căn cứ |
|---|---|---|---|---|
| **FR-B-01** | Chapter parse + **text clean** | Loại rác của đời thật (quảng cáo, lời tác giả cuối chương, *"xin ủng hộ phiếu đề cử"*) bằng regex/heuristic **tất định**, **trước khi** extraction chạy — nếu không, Story Bible sinh entity giả. Đây là **bước ĐẦU TIÊN** của pipeline | MVP0 ❌ (viết tay) → **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **B1** · CF-8.7 — *"text clean là bước ĐẦU TIÊN"* |
| **FR-B-02** | Story Bible extraction tự động | Rút **character · location · costume** từ chapter, để người dùng chỉ phải **sửa**, không phải khai tay toàn bộ. Phải tách **Identity** (bất biến qua chương) khỏi **Appearance** (thay đổi theo trạng thái) — gộp hai thứ này vào một field là nguyên nhân của phần lớn lỗi consistency | MVP0 ❌ (viết tay) → **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **B2** · CF-8.4 (*"không code extraction"* ở MVP0) · CF-8.7 |
| **FR-B-03** | Timeline state resolver `state_at(N) = reduce(events)` | Truy được trạng thái nhân vật tại **một thời điểm bất kỳ** ⇒ panel ở chương 40 dùng đúng trang phục của chương 40. Ranh giới bắt buộc: **code sở hữu state, LLM chỉ phát event** | MVP0 ❌ (viết tay) → **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **B3** · [Analysis §5.5](../050-Research/Analysis-Comic-Studio-Concept.md) · **R8** |
| **FR-B-04** | **Khoá thời gian đúng** — `timeline_id` + `story_order` thay cho `(chapter, scene)` | Phân tách **`syuzhet`** (thứ tự người đọc gặp sự kiện) khỏi **`fabula`** (thứ tự sự kiện thực sự xảy ra). Dùng `(chapter, scene)` làm khoá thời gian **sai âm thầm ở MỌI flashback**. ⚠️ **Phải sửa TRƯỚC dòng code đầu tiên** — làm sau MVP1 là migration toàn bộ | **pre-cycle 09/2026** (schema draft) → **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **B4** · [Analysis §5.1](../050-Research/Analysis-Comic-Studio-Concept.md) · [Glossary](../999-Resources/Glossary.md) *syuzhet vs fabula*, *`timeline_id`* |

> **Ánh xạ hàng nguồn**: `B1 → FR-B-01` · `B2 → FR-B-02` · `B3 → FR-B-03` · `B4 → FR-B-04` · **`B5` (pgvector / vector search) → [mục 6.3](#63-hoãn-ngoài-mvp--kèm-điều-kiện-mở-lại)** (chỉ ❌/⛔ xuyên MVP0–MVP4). **5/5 hàng nhóm B có mặt.**

---

### C. Comic Director & Layout

> **BRD**: [BRD-003-Comic-Director-And-Layout](./BRD/BRD-003-Comic-Director-And-Layout.md) · **Epic**: [Epic-Comic-Director-And-Layout](../022-User-Stories/Epics/Epic-Comic-Director-And-Layout.md)
>
> *Business goal*: chuyển scene → page → panel dưới dạng **Comic IR (Comic Intermediate Representation)**, và **khoá cứng ràng buộc kỹ thuật vào schema thay vì vào prompt**.

| ID | Yêu cầu | Mô tả | Mốc MVP | Căn cứ |
|---|---|---|---|---|
| **FR-C-01** | **Comic IR / `Panel Specification`** — spec là dữ liệu chính | Panel được lưu dưới dạng **spec có schema**, không dưới dạng ảnh: bố cục, nhân vật có mặt, camera, ràng buộc thị giác, vùng an toàn cho chữ. Ảnh là **output phái sinh** ⇒ sửa một field thay vì re-roll cả ảnh | MVP0 🟡 (YAML viết tay) → **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **C1** · [Analysis §4.2](../050-Research/Analysis-Comic-Studio-Concept.md) — hàng **rủi ro thấp nhất** của bảng khả thi |
| **FR-C-02** | Director tự động **scene → page → panel** | Hệ thống tự chia scene thành page và panel, thay cho panel script viết tay | MVP0 ❌ (viết tay) → MVP1 ⛔ → **MVP2 ✅** (TRONG horizon) | `MVP-Scope §3` **C2** · CF-8.8 |
| **FR-C-03** | Layout: **rubric `beat_type` + emphasis quota** | Panel quan trọng được cấp diện tích lớn hơn theo một **bảng tra rời rạc, tất định**, cộng quota nhấn mạnh theo chapter. ⚠️ Đây là **cơ chế thay thế**: mục tiêu *"layout theo narrative importance"* **được giữ**; cơ chế **Layout Score 5 số thực bị cắt hẳn** (xem [mục 6.2](#62-cắt-hẳn--không-có-trong-full-scope)) | MVP0–1 ❌/⛔ → **MVP2 ✅** (TRONG horizon) | `MVP-Scope §3` **C3** · [MVP-Scope §4.3](../010-Planning/MVP-Scope.md#4-cắt-gì-và-vì-sao) · CF-9.3 |
| **FR-C-04** | Cứng hoá **≤3 nhân vật/panel** trong schema Comic IR | Panel có 4 nhân vật bị **DB TỪ CHỐI**, không phải bị cảnh báo. Đây là ràng buộc **sản phẩm**, không phải tuỳ chọn kỹ thuật: `attribute binding` thất bại gần hoàn toàn từ 4 người — *"near-complete failure beyond three subjects"* `[OFF]`. Cảnh đông người giải bằng **shot xa / silhouette / crop**. ⚠️ Ngưỡng **có thể siết xuống ≤2** nếu tiêu chí `G1-d` dưới ngưỡng | MVP0 🟡 (kỷ luật tay) → MVP1 ⛔ → **MVP2 ✅** (TRONG horizon) | `MVP-Scope §3` **C5** · `[OFF]` CF-6.5 (CogCanvas ID-Sim: **42.33** ở 2 người → **27.21** ở 3 → **2.67** ở 4 → **0.52** ở 5) · Charter **C3** · **R1** |
| **FR-C-05** | **`text_safe_zone`** trong panel spec | Panel spec **chừa sẵn vùng đặt bubble**. Thiếu nó thì bubble che mặt nhân vật và phải sinh lại toàn bộ ảnh đã làm | MVP0–1 ⛔ → **MVP2 ✅** (TRONG horizon) | `MVP-Scope §3` **C6** · CF-8.8 · [Glossary](../999-Resources/Glossary.md) *`text_safe_zone`* |
| **FR-C-06** | **Human gate bắt buộc #1 — speaker attribution** | Người dùng **phải** xác nhận mỗi dòng thoại được gán đúng người nói trước khi trang được xuất bản. ⚠️ **KHÔNG phải tuỳ chọn, không dồn sang MVP4.** Đo bằng **sự VẮNG MẶT của đường code bypass**. Lỗi tham chiếu **30–50%** (3+ người có tự sự chen) / **40–60%** (câu ngắn, thán từ) — ⚠️ `[EM]`, **ước lượng, KHÔNG phải số đo**. Chi phí lỗi **bất đối xứng**: một dòng gán sai làm hỏng cả trang | MVP0 ❌ → MVP1 ⛔ → **MVP2 ✅** (TRONG horizon) | `MVP-Scope §3` **C7** · CF-8.8 · ⚠️ `[EM]` CF-6.10 · Charter **A8** |
| **FR-C-07** | **Human gate bắt buộc #2 — dialogue condensation** | Người dùng **phải** xác nhận thoại đã nén vừa bubble mà không mất nghĩa. Nén thoại gốc (**30–80 từ** với web-novel dịch) xuống mức đọc thoải mái (**~8–20 từ**), hệ số **2–5×**. Là **hành vi biên tập CÓ MẤT** ⇒ cần LLM **và** cần người review. **Phải chạy SAU layout**, vì `text_budget` phụ thuộc diện tích panel | MVP0 ❌ → MVP1 ⛔ → **MVP2 ✅** (TRONG horizon) | `MVP-Scope §3` **C7** · CF-8.8 · [Glossary](../999-Resources/Glossary.md) *dialogue condensation* |

> **Ánh xạ hàng nguồn**: `C1 → FR-C-01` · `C2 → FR-C-02` · `C3 → FR-C-03` · `C5 → FR-C-04` · `C6 → FR-C-05` · `C7 → FR-C-06` **và** `FR-C-07` (một hàng nguồn, hai gate độc lập — chúng chỉ *"xong"* cùng nhau) · **`C4` (Layout Score 5 số thực) → [mục 6.2](#62-cắt-hẳn--không-có-trong-full-scope)**. **7/7 hàng nhóm C có mặt.**

---

### D. Editor & UI

> **BRD**: [BRD-004-Minimum-Editor](./BRD/BRD-004-Minimum-Editor.md) · **Epic**: [Epic-Minimum-Editor](../022-User-Stories/Epics/Epic-Minimum-Editor.md)
>
> *Business goal*: cho người dùng thực hiện — **và ghi lại** — quyết định sáng tạo của con người, ở mức tối thiểu đủ để (a) sản phẩm dùng được, (b) thoả **Điều 5a NĐ 134/2026**.

> [!IMPORTANT]
> **Nguyên tắc chi phối cả module**: nghĩa vụ pháp lý *"iterative, interactive process"* đặt lên **tầng DỮ LIỆU (audit event), KHÔNG đặt lên tầng CANVAS**. Một form editor có ghi vết đầy đủ thoả nghĩa vụ đó **y hệt** một canvas editor. ⇒ **UI được tự do chọn cái rẻ; dữ liệu provenance thì không được cắt một dòng nào.** (CF-9.1 · [MVP-Scope §2 NT-2](../010-Planning/MVP-Scope.md#2-nguyên-tắc-cắt-scope))
>
> Năm thành phần `FR-D-01`…`FR-D-05` là **editor tối thiểu ~20–25%** effort `[EM]` CF-6.7, **mẫu số SaaS** (đã bao gồm multi-tenancy, billing, auth, moderation). ⚠️ Cộng năm khoảng thành phần ở [MVP-Scope §5.2](../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas) ra **20–30%** — chênh lệch **có từ nguồn** và được ghi lại thay vì âm thầm sửa; đọc **biên trên 25% như một ước lượng lạc quan**, cần con số thận trọng khi lập ngân sách thời gian thì dùng **30%** (CF-10.3).

| ID | Yêu cầu | Mô tả | Mốc MVP | Căn cứ |
|---|---|---|---|---|
| **FR-D-01** | **Panel card**: form spec + ảnh preview + `Regenerate` + **variant picker** | Chính là vòng lặp *iterative*. **Variant picker là hành động sáng tạo rẻ nhất mà giá trị pháp lý cao nhất** — *chọn* = authorship, và nó ghi được vào `change_log` | MVP3 ✅ (**NGOÀI** horizon) · effort **5–7%** `[EM]` | [MVP-Scope §5.2](../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas) thành phần **#1** (thuộc hàng `D1`) |
| **FR-D-02** | **Bubble/text overlay editor trong phạm vi MỘT panel** | Kéo bubble, sửa thoại, chọn kiểu, kéo đuôi trỏ. Ba lý do **độc lập**: (a) thoại do người viết là phần **được bảo hộ**; (b) bubble che mặt là lỗi **không thể tự động tránh**; (c) không sửa được thoại thì mọi lần sửa chữ thành một lần regenerate ảnh — **đốt tiền**. Đây là *"canvas bị giới hạn trong một khung"*, **không** phải scene graph tự do | MVP2 (bắt đầu) → MVP3 ✅ hoàn tất (**vắt biên** horizon) · effort **5–8%** `[EM]` | [MVP-Scope §5.2](../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas) thành phần **#2** (thuộc hàng `D1`) · **R2** |
| **FR-D-03** | **Page**: chọn **template layout**, đổi chỗ / swap panel giữa các ô, reorder | *Selection & arrangement* là quyết định sáng tạo của con người — và là phần **được bảo hộ**. Chỉ cần **rời rạc**, không cần hình học liên tục. **Đường nâng cấp không mất mát**: layout lưu dưới dạng **toạ độ chuẩn hoá 0–1** trong `page_layout JSONB` ngay từ MVP; template chỉ là preset ghi vào **cùng** schema ⇒ nếu sau này lên canvas thật thì **không phải migrate dữ liệu** | **MVP2 ✅** (TRONG horizon) · effort **3–4%** `[EM]` | [MVP-Scope §5.2](../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas) thành phần **#3** (thuộc hàng `D1`) · [MVP-Scope §4.1](../010-Planning/MVP-Scope.md#4-cắt-gì-và-vì-sao) |
| **FR-D-04** | **Preview trang + chapter render server-side** (composite PNG/PDF), read-only | Khách phải **thấy thành phẩm mới trả tiền**. Rẻ vì **tái dùng compositor của export** (`FR-H-04`) | **MVP2 ✅** (TRONG horizon) · effort **3–5%** `[EM]` | [MVP-Scope §5.2](../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas) thành phần **#4** (thuộc hàng `D1`) |
| **FR-D-05** | **Story Bible editor** (form: character, costume, location, state theo event) | Đây mới là **nơi moat lộ ra với khách hàng**. Vẫn chỉ là form + list — không cần canvas | **MVP1 ✅** (TRONG horizon) · effort **4–6%** `[EM]` | [MVP-Scope §5.2](../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas) thành phần **#5** (thuộc hàng `D1`) |
| **FR-D-06** | **Ràng buộc xuyên suốt: mọi hành động trong editor sinh một `change_log` row** | Kể cả khi hành động chỉ là *"chọn ảnh này thay vì ảnh kia"*. ⚠️ **Đây là điều kiện làm cho việc cắt canvas trở nên HỢP PHÁP** — không có nó thì cắt canvas biến thành cắt luôn lá chắn pháp lý. Là **điểm cưỡng chế** của `FR-G-01` ở tầng UI, áp cho **cả năm** thành phần `FR-D-01`…`FR-D-05`. Về bản chất là **Definition of Done của module D**, không phải một tính năng rời | Theo mốc của từng thành phần: **MVP1** trở đi | [MVP-Scope §5.2](../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas) *ràng buộc thiết kế xuyên suốt* · `MVP-Scope §6` **KC-2** |
| **FR-D-07** | Expression sheet mỗi nhân vật | Bộ biểu cảm/góc nhìn chuẩn của nhân vật. **Bản tối thiểu: 3 góc + 3 biểu cảm**; bộ đầy đủ chỉ ở Full Scope | MVP0 ❌ → MVP1–2 ⛔ → MVP3 🟡 (**NGOÀI** horizon) → Full Scope ✅ | `MVP-Scope §3` **D7** · [Analysis §6.3](../050-Research/Analysis-Comic-Studio-Concept.md) |

> **Ánh xạ hàng nguồn**: `D1 → FR-D-01 … FR-D-05` (năm thành phần bắt buộc của [MVP-Scope §5.2](../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas)) · `D7 → FR-D-07` · **`D2` · `D3` · `D4` · `D5` → [mục 6.3](#63-hoãn-ngoài-mvp--kèm-điều-kiện-mở-lại)** · **`D6` → [mục 6.2](#62-cắt-hẳn--không-có-trong-full-scope)**. `FR-D-06` là ràng buộc xuyên suốt, không map 1:1 với một hàng `§3`. **7/7 hàng nhóm D có mặt.**

---

### E. Multi-tenancy & hạ tầng

> **BRD**: [BRD-005-Multi-Tenancy-And-Platform](./BRD/BRD-005-Multi-Tenancy-And-Platform.md) · **Epic**: [Epic-Multi-Tenancy-And-Platform](../022-User-Stories/Epics/Epic-Multi-Tenancy-And-Platform.md)
>
> *Business goal*: nền multi-tenant an toàn **từ commit đầu tiên**, trên kiến trúc **modular monolith**. Khối này chiếm **15–25%** effort `[EM]` CF-6.9 mà thiết kế ý tưởng gốc **không nhắc một dòng** — ước thiếu thì *"nó không lấy chỗ của tính năng, nó lấy chỗ của thời gian không tồn tại"*.

| ID | Yêu cầu | Mô tả | Mốc MVP | Căn cứ |
|---|---|---|---|---|
| **FR-E-01** | `tenant_id NOT NULL` mọi bảng + là **cột ĐẦU TIÊN** mọi composite index + **Postgres RLS** | Retrofit `tenant_id` vào schema **đã có dữ liệu thật** là một trong những migration đắt nhất tồn tại: phải sửa mọi bảng, mọi query, mọi index, và **không có cách nào xác minh đã sửa hết**. Bỏ sót một chỗ = **rò rỉ dữ liệu chéo tenant** = **sự cố tồn vong**. RLS là **lớp phòng thủ thứ hai** — với 1 dev **không có code review**, đây là bảo hiểm rẻ nhất tồn tại. ⚠️ **Definition of Done là test rò rỉ chéo tenant PASS, KHÔNG phải số bảng đã sửa** | **MVP1 ✅ — ngày đầu** (TRONG horizon) | `MVP-Scope §3` **E1** · `MVP-Scope §6` **KC-5** · CF-8.7 · `[EM]` CF-6.9 |
| **FR-E-02** | `tenant` / `user` / `membership` là **ba entity riêng** | Kể cả khi quan hệ hiện tại là 1:1 (1 user = 1 tenant ở bản đầu). Đây là thứ chuẩn bị sẵn cho ngày bán **gói team** | **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **E2** · [Analysis §5.7](../050-Research/Analysis-Comic-Studio-Concept.md) quyết định #2 |
| **FR-E-03** | Object storage `tenant/{tenant_id}/{sha256}`, **KHÔNG dedup chéo tenant** | Content-addressed trong phạm vi một tenant. ⚠️ **Dedup chéo tenant mâu thuẫn TRỰC TIẾP với lập luận bản quyền** của dự án | **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **E3** · [Analysis §5.7](../050-Research/Analysis-Comic-Studio-Concept.md) #4 |
| **FR-E-04** | **Mua** auth + billing, **không tự viết** | *"Tự viết auth là cách nhanh nhất để một dev đốt hai tháng và vẫn có lỗ hổng."* Hệ quả lên tầng Requirements: luồng signup/tenant-creation do **vendor sở hữu** ⇒ không viết Use Case luồng người dùng cho nó, chỉ có yêu cầu **cấu hình** | **MVP1 ✅ auth** (TRONG horizon) → MVP3 ✅ **+billing** (NGOÀI horizon) | `MVP-Scope §3` **E4** · [Analysis §5.7](../050-Research/Analysis-Comic-Studio-Concept.md) |
| **FR-E-05** | **Modular monolith**: 1 process · 1 PostgreSQL · 3 schema (`story` / `comic` / `generation`) | Luật module bắt buộc: `comic` gọi `story` **chỉ qua** `resolveState()` và `getBible()`, **cưỡng chế bằng lint rule**. Ba lý do khiến quyết định này **MẠNH LÊN dưới SaaS**: (1) **RLS không bảo vệ được join phía ứng dụng**, và state resolution là truy vấn **xuyên** `story` ↔ `comic`; (2) nghĩa vụ audit đòi **một** transaction boundary — *"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"*; (3) ngân sách effort đã bị multi-tenancy ăn **15–25%** `[EM]` | **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **E5** · [MVP-Scope §4.2](../010-Planning/MVP-Scope.md#4-cắt-gì-và-vì-sao) · CF-9.2 |
| **FR-E-06** | Worker là process triển khai riêng, **CÙNG codebase** (2 entrypoint) | Worker chết mà API vẫn sống ⇒ khách không thấy sản phẩm chết ⇒ không churn. Là **seam kinh tế**, không phải seam kỹ thuật | MVP1–2 ⛔ → MVP3 ✅ (**NGOÀI** horizon) | `MVP-Scope §3` **E7** · [Analysis §6.2](../050-Research/Analysis-Comic-Studio-Concept.md) *seam kinh tế* |

> **Ánh xạ hàng nguồn**: `E1 → FR-E-01` · `E2 → FR-E-02` · `E3 → FR-E-03` · `E4 → FR-E-04` · `E5 → FR-E-05` · `E7 → FR-E-06` · **`E6` (microservices + Vector DB riêng) → [mục 6.2](#62-cắt-hẳn--không-có-trong-full-scope)** · **`E8` (SSO/SAML, custom domain, white-label, multi-region) → [mục 6.3](#63-hoãn-ngoài-mvp--kèm-điều-kiện-mở-lại)**. **8/8 hàng nhóm E có mặt.**

---

### F. Kinh tế & credit

> **BRD**: [BRD-006-Credit-And-Unit-Economics](./BRD/BRD-006-Credit-And-Unit-Economics.md) · **Epic**: [Epic-Credit-And-Unit-Economics](../022-User-Stories/Epics/Epic-Credit-And-Unit-Economics.md)
>
> *Business goal*: **đo và cưỡng chế chi phí TRƯỚC KHI nó xảy ra**. Không có tầng này thì một power user xoá margin của bốn user thường.

> **Mô hình ba tầng — `[CHỐT]`, không mở lại trong horizon này** (CF-2.1–2.4 · Charter **C2**): **Tầng 1** *$4–8/tháng, **KHÔNG** có image gen, margin ~90%, không cần API key* · **Tầng 2** *credit pack **không hết hạn**, managed inference, cho user dưới ngưỡng **~125 ảnh/tháng*** `[TC]` CF-2.5 · **Tầng 3** *BYOK là **tuỳ chọn MỞ KHOÁ**, **KHÔNG** phải điều kiện để dùng sản phẩm*. ⇒ Kiến trúc billing / ledger / onboarding phải thiết kế cho **ba** tầng ngay từ đầu, **không retrofit**.

| ID | Yêu cầu | Mô tả | Mốc MVP | Căn cứ |
|---|---|---|---|---|
| **FR-F-01** | `usage_event` **append-only** + rollup `usage_daily` | Append-only là **điều kiện** để nó dùng được làm căn cứ đối soát. **regen ratio là metric first-class**, không phải chỉ số phụ — nó là *biến quyết định của cả mô hình tài chính* và là **đầu vào bắt buộc của gate G2** | MVP0 🟡 log tay → **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **F1** · CF-8.6 — *"đo muộn nghĩa là định giá trong bóng tối hàng tháng"* |
| **FR-F-02** | `cost_usd` + `model_id` + `model_version` + `attempt_no` trên **mọi** `generation` | ⚠️ **Không backfill được.** Thiếu bốn cột này thì COGS phải ước lượng lại vĩnh viễn. `model_version` có mặt vì **silent model drift** là sự cố mà dự án không kiểm soát được, chỉ phát hiện được | MVP0 🟡 CSV → **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **F2** · [Analysis §5.7](../050-Research/Analysis-Comic-Studio-Concept.md) #3 |
| **FR-F-03** | **Credit ledger append-only + HOLD trước khi enqueue** + `CHECK (available >= 0)` ở tầng DB + **hold reaper** | ⚠️ **Bộ ba không tách rời — ship 2/3 sinh ra lỗi tệ hơn không ship.** (a) **Check-rồi-gọi là race condition**: 10 job đồng thời đều thấy đủ số dư và đều chạy → vượt trần. (b) **Hold reserve phải là 3 credit/panel**, vì **N=3 là mặc định cho MỌI panel**, không phải retry-on-failure — reserve 1 credit rồi tính sau = **hợp lệ hoá số dư âm**. (c) Thiếu **hold reaper** cho `expires_at`: job crash sau khi hold ⇒ hold treo **vĩnh viễn** ⇒ khách *"có credit mà không generate được"* — loại lỗi **khó chẩn đoán nhất** | MVP1–2 ⛔ → MVP3 ✅ (**NGOÀI** horizon) — **trước bản trả phí có image gen** | `MVP-Scope §3` **F3** · `MVP-Scope §6` **KC-7** · CF-6.12 · `[OFF]` CF-3.1 |
| **FR-F-04** | **Hard quota cưỡng chế TRƯỚC khi enqueue** (không đếm sau) | Đếm sau nghĩa là đã tiêu tiền rồi mới biết. Là **BLOCKER-03** của [Charter §9.3](../010-Planning/Charter-Comic-Studio.md#9-tiêu-chí-thành-công--gono-go): chặn **bản trả phí đầu tiên** | MVP1–2 ⛔ → MVP3 ✅ (**NGOÀI** horizon) | `MVP-Scope §3` **F4** · CF-8.11b · Charter **BLOCKER-03** |
| **FR-F-05** | **BYOK — tuỳ chọn MỞ KHOÁ**, không phải điều kiện dùng sản phẩm | Người dùng tự cung cấp API key ⇒ COGS không còn là của nền tảng. Ngưỡng phân tuyến **~125 ảnh/tháng** `[TC]` CF-2.5 (nguồn là **bên bán managed** nhưng khuyến nghị **ngược chiều lợi ích của họ** ⇒ chấp nhận được, **không nâng lên `[OFF]`**). ⚠️ Đánh đổi đã biết: **friction cao với người dùng non-technical** ⇒ onboarding flow trở thành **rủi ro sản phẩm số 1** của tầng này | MVP0–1 ❌ → MVP2–3 ⛔ → MVP4 ✅ (**NGOÀI** horizon) | `MVP-Scope §3` **F5** · `[CHỐT]` CF-2.4 · `[TC]` CF-2.5 · [Glossary](../999-Resources/Glossary.md) *BYOK* |
| **FR-F-06** | **Tầng 1 bán được**: Story Bible + Comic IR + layout + versioning + export, **KHÔNG image gen** | Margin **~90%**, **không cần API key** ⇒ đây là thứ **duy nhất** có thể bán được mà không phụ thuộc COGS của provider. ⚠️ **Điều kiện doanh thu**: cần `FR-H-04` (export) + `FR-G-03` (safe harbour) + **G0 PASS** | MVP1 ⛔ → MVP2 🟡 *khả dĩ* (TRONG horizon) → MVP3 ✅ | `MVP-Scope §3` **F6** · `[CHỐT]` CF-2.2 · ⚠️ `[EM]` CF-10.9 — *"là một LỰA CHỌN, không phải kế hoạch đã chốt"*, cần Founder quyết tại **G2** |

> **Ánh xạ hàng nguồn**: `F1 → FR-F-01` · `F2 → FR-F-02` · `F3 → FR-F-03` · `F4 → FR-F-04` · `F5 → FR-F-05` · `F6 → FR-F-06`. **6/6 hàng nhóm F có mặt.**

---

### G. Pháp lý & compliance

> **BRD**: [BRD-007-Legal-And-Compliance](./BRD/BRD-007-Legal-And-Compliance.md) · **Epic**: [Epic-Legal-And-Compliance](../022-User-Stories/Epics/Epic-Legal-And-Compliance.md)
>
> *Business goal*: giữ được **bảo hộ bản quyền cho tác phẩm của Founder VÀ của khách hàng**, và giữ được **miễn trừ trung gian**. Đây là nhóm chứa **rủi ro nhị phân duy nhất** của cả dự án.

> [!WARNING]
> **Hai hệ đánh số, cấm để lẫn vào nhau** (CẤM-14): `FR-G-xx` ở bảng này là **yêu cầu compliance**, truy về hàng nguồn **`GP-1`…`GP-5`** của `MVP-Scope §3`. Còn **`G0` / `G1` / `G2`** là **ba gate Go/No-Go** do [MVP-Scope §7](../010-Planning/MVP-Scope.md#7-gono-go-decision) định nghĩa. Trong mọi BRD / Use Case / Story: viết `GP-n` cho hàng compliance và `G0`/`G1`/`G2` cho gate — **không viết tắt `G1` cho `GP-1`**.

| ID | Yêu cầu | Mô tả | Mốc MVP | Căn cứ |
|---|---|---|---|---|
| **FR-G-01** | **Provenance chain**: `parent_generation_id` + `relation_kind ENUM('retry','variation','refine','continuity_fix')` + `change_log` + `field_provenance` + `generation.origin ENUM('ai','ai_edited','human')` — và cả năm **commit CÙNG MỘT TRANSACTION** với artifact mà chúng chứng minh | ⚠️ **Là hồ sơ pháp lý bắt buộc, KHÔNG phải một feature — và KHÔNG BACKFILL ĐƯỢC.** Không lưu từ generation đầu tiên thì **vĩnh viễn** không có. **Prompt một mình không chứng minh được *"decisive contribution"***; cái chứng minh được là *người đã chọn X thay vì Y, đã sửa thoại, đã đổi camera, đã kéo bubble*. Thiếu `field_provenance` thì **không xác định được ranh giới phần được bảo hộ**. Và *"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"* ⇒ ràng buộc **cùng transaction** là bắt buộc. Là **BLOCKER-04 — chặn MỌI THỨ**. ⚠️ Diễn giải *"generation đầu tiên"* = generation đầu tiên của **sản phẩm thật, tức MVP1** (vì MVP0 là spike bị vứt) — nhãn `[EM]`, **diễn giải của tài liệu `MVP-Scope`, không có trong bảng CF** | MVP0 🟡 ghi tay → **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **GP-1** · `MVP-Scope §6` **KC-1 · KC-2 · KC-3 · KC-4** · `[OFF]` CF-7.1/7.2/7.3 · Charter **BLOCKER-04** |
| **FR-G-02** | Kiểm **opt-out signal Điều 37b** ngay trong bước **ingest** | Chi phí **~0** `[OFF]`. Bước ingest là nơi **DUY NHẤT** file của user lần đầu đi vào hệ thống — kiểm ở chỗ khác nghĩa là **đã xử lý nội dung có opt-out trước khi biết**. Chi phí bằng 0 mà bỏ qua là lựa chọn **không có lý do nào biện minh** | MVP0 ❌ → **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **GP-2** · `MVP-Scope §6` **KC-6** · `[OFF]` CF-7.5 |
| **FR-G-03** | **Checklist safe harbour Điều 198b**: công cụ takedown · đăng ký đầu mối với **Bộ VHTTDL** · **SLA 72 giờ** · **KHÔNG chủ động rà soát nội dung** · user warrant + indemnify trong ToS · kiểm opt-out trước khi xử lý | Sáu mục, tick đủ **6/6**. ⚠️ Neo vào **TRIGGER** — *trước lần đầu mở cho người ngoài upload* — **KHÔNG neo vào một ngày**. Một lần upload của người ngoài mà chưa có đường takedown là **nghĩa vụ không rút lại được**. Là **BLOCKER-02**: chặn việc mở cho người ngoài upload (không chặn dùng nội bộ) | MVP0 ❌ → MVP1 🟡 → **MVP2 ✅** (TRONG horizon), *hoặc sớm hơn nếu trigger đến sớm* | `MVP-Scope §3` **GP-3** · `[OFF]` CF-7.6 · Charter **BLOCKER-02** · **R3** |
| **FR-G-04** | **AI disclosure** (Luật TTNT 2025) | Nghĩa vụ **nội địa Việt Nam**, không phải chuyện thị trường nước ngoài. Deadline tuân thủ **~01/03/2027** `[OFF]` — nằm **ngay sau** horizon. ⚠️ **HAI NGUỒN MÔ TẢ PHẠM VI KHÁC NHAU**: nguồn A nói chỉ áp cho nội dung *"mô phỏng người thật hoặc sự kiện thực tế"*, nguồn B nói áp cho **mọi** nội dung AI ⇒ **thiết kế theo diễn giải RỘNG cho tới khi luật sư chốt**. Phạm vi thật là **`TBD`**, và nó là **câu Q2 của gate G0** | MVP0 ❌ → MVP1–2 🟡 → MVP3 ✅ (**NGOÀI** horizon) — ⚠️ nhưng **deadline pháp lý ~01/03/2027 không dịch theo lịch dự án** | `MVP-Scope §3` **GP-4** · `[OFF]` CF-7.7 · Charter **C4** · **R4** |
| **FR-G-05** | **ToS + user warrant + `ON DELETE CASCADE` + đường hard-delete tenant ĐÃ KIỂM THỬ** | Takedown **sẽ** đến — không phải *"nếu"*. Và *"đường thoát phải được xây cùng lúc với đường vào"*: khi kill có trật tự, mỗi tenant phải xuất được **cả `change_log` + `field_provenance`**, vì đó là hồ sơ chứng minh quyền tác giả **của khách** | **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **GP-5** · [Analysis §5.7](../050-Research/Analysis-Comic-Studio-Concept.md) #5 · [MVP-Scope §8.2](../010-Planning/MVP-Scope.md#8-điều-kiện-thoát-kill-criteria) |

> **Ánh xạ hàng nguồn**: `GP-1 → FR-G-01` · `GP-2 → FR-G-02` · `GP-3 → FR-G-03` · `GP-4 → FR-G-04` · `GP-5 → FR-G-05`. **5/5 hàng nhóm G có mặt.**

> [!CAUTION]
> **Hai giới hạn hiểu biết phải mang theo khi viết bất kỳ requirement nào của module này:**
> 1. ⛔ **CẤM viết requirement như thể phạm vi Điều 37a đã rõ.** Hiểu biết hiện tại dựa trên **bản tóm tắt, KHÔNG phải nguyên văn** — nguồn gốc trả `403` hoặc paywall. **Luật sư phải đọc nguyên văn.** (CẤM-13 · CF-7.4)
> 2. ⚠️ **`TBD`: Điều 198b có áp cho SaaS *xử lý/biến đổi* nội dung** (không phải hosting thuần) hay không — chưa ai trả lời. Đây là **câu Q3 của G0**.
>
> **Và một điều dễ đọc sai nhất của cả bộ tài liệu**: ⛔ **BLOCKER-01 / gate G0 chặn THƯƠNG MẠI HOÁ, KHÔNG chặn MVP0–MVP1.** Đọc thành *"phải chờ luật sư mới được viết dòng code đầu tiên"* là **cách hiểu nhầm đắt nhất** mà tài liệu này có thể gây ra. (CẤM-10 · [Charter §9.2](../010-Planning/Charter-Comic-Studio.md#9-tiêu-chí-thành-công--gono-go))

---

### H. Chất lượng & vận hành

> **BRD**: [BRD-008-Quality-And-Operations](./BRD/BRD-008-Quality-And-Operations.md) · **Epic**: [Epic-Quality-And-Operations](../022-User-Stories/Epics/Epic-Quality-And-Operations.md)
>
> *Business goal*: làm cho mọi thay đổi về sau **đo được**. Không có module này thì mọi thay đổi prompt/model là **thay đổi mù**.

| ID | Yêu cầu | Mô tả | Mốc MVP | Căn cứ |
|---|---|---|---|---|
| **FR-H-01** | **HITL gate + eval kit** | Điểm trong pipeline **bắt buộc có người xác nhận** trước khi đi tiếp, cộng bộ dữ liệu + script đo chất lượng output **sinh ra SỐ**, không chấm bằng ấn tượng. ⚠️ **Ngay tại MVP1, KHÔNG dồn MVP4** — đây là điều kiện khả thi **R9**. Đơn vị đo của HITL gate là **giờ-người**, không phải token: với một người làm một mình, **đây mới là ràng buộc thật**, không phải chi phí API | MVP0 ❌ → **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **H1** · CF-8.7 · **R9** |
| **FR-H-02** | **Log preference data** | Ghi nhãn mỗi lần người dùng **chấp nhận / từ chối** một gợi ý. Là **nguồn duy nhất** cho eval của tầng thẩm mỹ, và là nguyên liệu của **moat thật** — *"một khoản đầu tư, trả hai lần"*. Gần như miễn phí, nhưng **không ghi từ đầu thì mất vĩnh viễn dữ liệu giai đoạn đầu** | MVP0 ❌ → **MVP1 ✅** (TRONG horizon) | `MVP-Scope §3` **H2** · CF-8.7 · [Analysis §12](../050-Research/Analysis-Comic-Studio-Concept.md) |
| **FR-H-03** | **Continuity Checker** dạng **N-candidate selection** | ⚠️ **Định nghĩa canon**: **QA-based selection giữa N candidate** — trả lời câu *"trong N cái này, cái nào consistent hơn"*. ⛔ **KHÔNG phải** *"gắn nhãn ✓/✗ từng attribute rồi autofix"* — cơ chế đó chưa được validate và có FP profile xấu (CẤM-12). Lý do sâu hơn: kiểm trang phục của nhân vật X đòi giải **re-identification** trước, mà đó **chính là** bài toán checker được lập ra để giải — một vòng lặp logic. ⚠️ Độ phủ **40–60% số panel** `[EM]` — **ước lượng, KHÔNG phải số đo** — và **PHẢI nói rõ với user**: *"đừng để họ hiểu là được bảo vệ toàn diện"*. Giấu điều này = **lời hứa sản phẩm không giữ được** | MVP0 🟡 (VLM select) → MVP1–2 ⛔ → MVP3 🟡 → MVP4 ✅ (**NGOÀI** horizon) | `MVP-Scope §3` **H3** · CF-8.10 · ⚠️ `[EM]` CF-6.11 · Charter **A9** · [Glossary](../999-Resources/Glossary.md) *Continuity Checker*, *re-identification* |
| **FR-H-04** | **Export PDF / CBZ / webtoon** | *"Thứ **DUY NHẤT** trong MVP4 mà người dùng thật sự nhận được"* ⇒ đã được **kéo lên sớm**. ⚠️ Đây **không** phải một tính năng editor — nó là **điều kiện doanh thu** của `FR-F-06`: không có export ở MVP2 thì Tầng 1 không bán được, và horizon 6 tháng khép lại với **$0** | MVP0 ❌ → MVP1 ⛔ → MVP2 🟡 *preview server-side* (TRONG horizon) → MVP3 ✅ đủ định dạng | `MVP-Scope §3` **H4** · CF-8.10 · [OKRs §3.0](../010-Planning/OKRs.md#3-q42026--chu-kỳ-chính) |
| **FR-H-05** | **Abuse controls tối thiểu** | Rate limit per tenant · giới hạn upload · log mỗi lần provider từ chối. Tín hiệu abuse sớm **gần như miễn phí** | MVP0 ❌ → MVP1 🟡 → **MVP2 ✅** (TRONG horizon) | `MVP-Scope §3` **H5** · [Analysis §5.7](../050-Research/Analysis-Comic-Studio-Concept.md) |
| **FR-H-06** | **Golden dataset regression** — 15–20 panel có spec + reference + ảnh + bảng đánh giá của con người | Tài sản dùng **suốt vòng đời** sản phẩm, không phải một artifact của MVP0. Là nơi đặt câu hỏi *"trang này đọc có ổn không?"* thành **dữ liệu**, và là proxy hiện có duy nhất cho định nghĩa *"đủ tốt"* đang `TBD` ở [mục 3.3](#33--tbd--persona-jtbd-và-định-nghĩa-đủ-tốt) | **MVP0 ✅** và **✅ ở mọi mốc sau** (TRONG horizon) | `MVP-Scope §3` **H6** · CF-10.10 · [Analysis §3.2](../050-Research/Analysis-Comic-Studio-Concept.md) |

> **Ánh xạ hàng nguồn**: `H1 → FR-H-01` · `H2 → FR-H-02` · `H3 → FR-H-03` · `H4 → FR-H-04` · `H5 → FR-H-05` · `H6 → FR-H-06`. **6/6 hàng nhóm H có mặt.**

---

### 4.9 Bảng kiểm đếm — 51 hàng `MVP-Scope §3`, 0 hàng rơi

| Module | Hàng `§3` | Số FR | Ở [mục 6](#6-ranh-giới-scope) |
|---|:--:|:--:|---|
| **A** Pipeline sinh ảnh | 7 | **7** | — |
| **B** Story Intelligence | 5 | **4** | `B5` |
| **C** Comic Director & Layout | 7 | **7** | `C4` |
| **D** Editor & UI | 7 | **7** | `D2` `D3` `D4` `D5` `D6` |
| **E** Multi-tenancy & hạ tầng | 8 | **6** | `E6` `E8` |
| **F** Kinh tế & credit | 6 | **6** | — |
| **G** Pháp lý & compliance | 5 | **5** | — |
| **H** Chất lượng & vận hành | 6 | **6** | — |
| **Tổng** | **51** | **48** | **9 hàng** |

> **48 FR** ≠ **42 hàng vào bảng** vì: `D1` tách thành **5** FR theo năm thành phần bắt buộc của [MVP-Scope §5.2](../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas) (+4), `C7` tách thành **2** gate độc lập (+1), và `FR-D-06` là ràng buộc xuyên suốt của editor (+1).

---

## 5. Yêu cầu phi chức năng

**Mục này CỐ Ý ngắn.** Toàn bộ yêu cầu phi chức năng và mọi yêu cầu kỹ thuật chi tiết thuộc **[SRS-Comic-Studio.md](./SRS-Comic-Studio.md)** — tài liệu đó là **nguồn duy nhất** cho tầng này. PRD **không** lặp lại nội dung SRS: một yêu cầu kỹ thuật xuất hiện ở hai nơi sẽ lệch nhau ngay lần đầu một trong hai được sửa.

Bảy trục phi chức năng có mặt trong sản phẩm này, nêu **tên trục** và **lý do tồn tại**, không nêu ngưỡng:

| # | Trục | Vì sao nó là NFR của dự án này, không phải một tuỳ chọn |
|---|---|---|
| 1 | **Tenant isolation** | Rò rỉ chéo tenant là **sự cố tồn vong** với một SaaS, không phải một bug |
| 2 | **Auditability & lineage** | Với closed API, mục tiêu đúng của bảng `Generation` **không phải reproducibility mà là AUDITABILITY + LINEAGE**: bit-exact replay không đạt được (nhiều API không cho set seed; provider cập nhật weights dưới cùng một tên model — **silent model drift**) ⇒ `seed` là **provenance metadata**, không phải replay key |
| 3 | **Determinism** | `FR-A-03` và `FR-B-03` phải tất định để bảng `Generation` có nghĩa và để **error cascade** không nhân lỗi qua các tầng |
| 4 | **Cost observability** | COGS phải đo được **trước** khi định giá, không sau |
| 5 | **Chất lượng typeset tiếng Việt** | ⚠️ **`TBD`** — không có benchmark định lượng render tiếng Việt có dấu cho bất kỳ image model nào; đặc biệt thiếu số cho chữ chồng hai dấu (*"ế"*, *"ữ"*, *"ượ"*). Đây cũng là một lý do độc lập của `FR-A-02` |
| 6 | **Usability** | ⚠️ **`TBD`** — không có ngưỡng nào do người ngoài đặt, vì [mục 3.3](#33--tbd--persona-jtbd-và-định-nghĩa-đủ-tốt) chưa đóng. Mọi ngưỡng UX trong tầng này là ngưỡng **tự đặt** và phải mang nhãn `[EM]` |
| 7 | **Compliance** | Ba giới hạn hiểu biết pháp lý ở cuối [mục 4 nhóm G](#g-pháp-lý--compliance) đi kèm, không tách rời |

Thiết kế kỹ thuật chi tiết (schema, API, ADR) **sẽ được đặc tả tại tầng `030-Specs`** — tầng đó hiện **rỗng** và nằm ngoài phạm vi của run này.

---

## 6. Ranh giới scope

> [!IMPORTANT]
> Mục này là **phạm vi SẢN PHẨM**. Câu hỏi *"hạng mục nào vào mốc MVP nào"* là câu hỏi khác và thuộc **[MVP-Scope.md](../010-Planning/MVP-Scope.md)** — PRD **không** phân xử lại nó.

### 6.1 Scope In — thuộc về sản phẩm

Trích [Charter §5.1](../010-Planning/Charter-Comic-Studio.md#51-scope-in--thuộc-về-sản-phẩm), kèm ánh xạ sang FR để truy vết:

| Hạng mục | Neo | FR thực thi |
|---|---|---|
| Nền tảng **SaaS multi-tenant** để tác giả bên ngoài **tự upload** truyện chữ và sinh comic pages | `[CHỐT]` CF-1.1 | `FR-E-01` … `FR-E-06` |
| **Story Bible editor + Comic IR + layout + versioning + export** — lõi giá trị, có mặt **cả ở tầng không-image-gen** | `[CHỐT]` CF-2.2 | `FR-B-*` · `FR-C-01`…`03` · `FR-D-03`…`05` · `FR-H-04` |
| **Managed inference** (credit pack không hết hạn) cho user dưới ngưỡng **~125 ảnh/tháng** `[TC]` | `[CHỐT]` CF-2.3 · CF-2.5 | `FR-F-01` … `FR-F-04` |
| **BYOK** như **tuỳ chọn MỞ KHOÁ** cho power user | `[CHỐT]` CF-2.4 | `FR-F-05` |
| **Typeset layer + speech bubble overlay** — **tự build** (thư viện có sẵn chưa có auto-placement) | **R2** · CF-8.11c | `FR-A-02` · `FR-D-02` |
| **Provenance / audit trail** phục vụ nghĩa vụ pháp lý **và** làm nền cho preference data | `[OFF]` CF-7.3 | `FR-G-01` · `FR-D-06` · `FR-H-02` |
| **Compliance layer**: takedown tool, opt-out check Điều 37b tại ingest, AI disclosure | CF-7.5 · CF-7.6 · CF-7.7 | `FR-G-02` … `FR-G-05` |
| **Editor tối thiểu** (**~20–25%** effort `[EM]`, **mẫu số SaaS**) | `[EM]` CF-6.7 | `FR-D-01` … `FR-D-06` |

### 6.2 Cắt hẳn — KHÔNG có trong Full Scope

> ❌ ở cột **Full Scope** của `MVP-Scope §3` nghĩa là hạng mục bị **loại khỏi thiết kế**, không phải bị hoãn. **Ba hạng mục, và chỉ ba.**

| Hàng nguồn | Hạng mục cắt hẳn | Lý do cắt | Điều kiện mở lại |
|---|---|---|---|
| **`C4`** | **Layout Score 5 số thực** | Hạng mục **không có prior art**, **không kiểm chứng được đúng/sai**, và có **phương án thay thế rẻ hơn cả chục lần với chất lượng cao hơn ở MVP** — *"chưa ai làm vì không đáng"*. Đó là định nghĩa của thứ nên cắt sớm. Cơ chế số thực tạo **cảm giác chính xác giả** | ⛔ **KHÔNG có.** ⚠️ Nhưng **MỤC TIÊU được GIỮ**: *layout theo narrative importance* → thay bằng rubric `beat_type` rời rạc + emphasis quota = **`FR-C-03`**. **Đừng viết requirement như thể cả mục tiêu bị cắt** (CF-9.3) |
| **`D6`** | **UI duyệt CÂY generation** (tree view / diff / branch-merge) | Flat list theo `created_at` + `approved_generation_id` đủ **95% giá trị** với chi phí nhỏ hơn nhiều bậc | ⛔ **KHÔNG mở lại.** ⚠️⚠️ **CẤM-09 — trích nguyên**: *"CẤM gộp **cắt UI cây generation (D6)** với **cắt lineage (KC-1)**. Hai quyết định độc lập và **TRÁI CHIỀU**."* ⇒ **Cắt UI, KHÔNG cắt cột dữ liệu** — `parent_generation_id` vẫn là bắt buộc tại `FR-G-01`. `MVP-Scope §6.1` xếp việc gộp hai thứ này là một trong **ba hiểu nhầm hay gặp**, và gộp nhầm thì **mất bảo hộ bản quyền** |
| **`E6`** | **Microservices (3 service) + 2 PostgreSQL + Vector DB riêng + Job Queue riêng** | Hai lý do **cứng**: (1) **hai DB = mất transaction boundary**, mà nghĩa vụ audit đòi `INSERT generation` + `INSERT change_log` + `INSERT usage_event` commit **cùng nhau**; (2) **RLS không bảo vệ được join phía ứng dụng**, và state resolution là truy vấn xuyên `story` ↔ `comic` ⇒ lớp phòng thủ thứ hai biến mất **đúng ở đường dẫn dữ liệu nóng nhất** | ⛔ **KHÔNG có.** Thay bằng **modular monolith** = `FR-E-05`. Năm **seam ĐÚNG chỗ** vẫn được giữ và miễn phí trong monolith (CF-9.2) |

### 6.3 Hoãn ngoài MVP — kèm điều kiện mở lại

> Sáu hạng mục này **có** trong Full Scope hoặc còn để mở, nhưng **không** sinh yêu cầu trong MVP0–MVP4. Cột cuối là điều kiện mở lại **đã được ghi tại nguồn** — nơi nào nguồn không ghi, ghi `KHÔNG CÓ ĐIỀU KIỆN Ở NGUỒN`.

| Hàng nguồn | Hạng mục | Lý do hoãn | Điều kiện mở lại |
|---|---|---|---|
| **`B5`** | `pgvector` / vector search | *"**Story Bible LÀ index của mình**"* — SQL + FTS trên dữ liệu đã có schema đủ dùng, và thêm một hạ tầng tìm kiếm là thêm một thứ phải vận hành | ✅ **Khi có bằng chứng SQL + FTS không đủ** (Full Scope 🟡 có điều kiện) |
| **`D2`** | Infinite canvas, zoom/pan cả chapter, hình học panel tự do, panel xoay / không chữ nhật | **Chi phí LỚN NHẤT, giá trị tăng thêm NHỎ NHẤT** ở bản trả phí đầu. Và canvas là software engineering thuần — **không AI nào viết hộ được phần khó** (state machine, perf với hàng trăm ảnh, undo trên side-effect không hoàn lại, race khi user sửa spec trong lúc generation đang bay) | ✅ **Có bằng chứng ĐO ĐƯỢC rằng khách rời đi vì thiếu nó.** Khi làm: dùng thư viện có sẵn sau một spike riêng — ⛔ **KHÔNG viết renderer từ đầu**. `FR-D-03` đã chuẩn bị đường nâng cấp không mất mát (toạ độ chuẩn hoá 0–1) |
| **`D3`** | Undo/redo xuyên toàn bộ state phân tán | Chỉ undo **cục bộ** trong form + vị trí bubble. **Không undo qua generation** — một `Regenerate` **tiêu tiền thật và không hoàn lại được** | ⛔ **KHÔNG mở lại theo dạng này.** Đúng hơn là **làm rõ UX** rằng generation không undo được |
| **`D4`** | Realtime collaboration | **1 user = 1 tenant** ở bản đầu | ✅ **Khi bán gói team** — mà `FR-E-02` (`membership` là entity riêng) đã chuẩn bị sẵn cho ngày đó |
| **`D5`** | Inpainting brush / drawing tools | Cần, nhưng **không phải để bán được bản đầu** | ✅ Khi làm: **bắt buộc** set `generation.origin='ai_edited'` (`FR-G-01`) |
| **`E8`** | SSO/SAML, custom domain, white-label, multi-region | *"Hoãn được"* — không hạng mục nào trong đây là điều kiện để bán bản đầu | `KHÔNG CÓ ĐIỀU KIỆN Ở NGUỒN` — Full Scope ⛔ |

### 6.4 Scope Out — KHÔNG thuộc về sản phẩm

Khác với 6.2/6.3 (ranh giới **bên trong** thiết kế), mục này là ranh giới **bên ngoài**: những thứ nằm ngoài định nghĩa sản phẩm ở **mọi** thời điểm. Đã liệt kê tại [mục 2.3 Non-Goals](#23-non-goals) `NG-1`…`NG-8`; nguồn đầy đủ ở [Charter §5.2](../010-Planning/Charter-Comic-Studio.md#52-scope-out--không-thuộc-về-sản-phẩm).

### 6.5 Bảy hạng mục KHÔNG ĐƯỢC CẮT — danh sách cứng

> [!CAUTION]
> Đây là **danh sách duy nhất trong toàn bộ tầng Requirements không mở ra thương lượng scope**. Mỗi mục có chung một tính chất: **rẻ khi làm từ đầu, KHÔNG THỂ SỬA VỀ SAU**. Nếu một run nào đó sau này đề xuất cắt một trong bảy mục, câu trả lời mặc định là **KHÔNG**, và người đề xuất phải bác được cột *"không giữ thì hỏng thế nào"* của [MVP-Scope §6](../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng).

| KC | Nội dung | FR thực thi |
|---|---|---|
| **KC-1** | `parent_generation_id` + `relation_kind` | `FR-G-01` |
| **KC-2** | `change_log` ghi **MỌI** hành động người dùng — kể cả *"chọn generation X thay vì Y"* | `FR-G-01` + `FR-D-06` |
| **KC-3** | `field_provenance` (mức field) + `generation.origin` | `FR-G-01` |
| **KC-4** | Cả ba mục trên **commit CÙNG MỘT TRANSACTION** với artifact chúng chứng minh | `FR-G-01` (đòi `FR-E-05` — một DB) |
| **KC-5** | `tenant_id NOT NULL` mọi bảng + cột **đầu tiên** mọi composite index + **RLS** | `FR-E-01` |
| **KC-6** | Kiểm **opt-out signal Điều 37b** ngay tại **ingest** | `FR-G-02` |
| **KC-7** | Credit ledger + **HOLD trước enqueue** + **reserve 3 credit/panel** + `CHECK (available >= 0)` + **hold reaper** | `FR-F-03` |

---

## 7. Success metrics

> [!IMPORTANT]
> **PRD KHÔNG đặt Key Result mới.** Mục này **mượn nguyên** hệ Objective/KR từ **[OKRs.md](../010-Planning/OKRs.md)** — tài liệu đó là **nguồn duy nhất**. Ở đây chỉ giữ **ID + ý định một dòng + link**, cố tình **không chép lại con số**, để trong toàn bộ kho tài liệu chỉ có **đúng một nơi** sửa được ngưỡng.
>
> **Cách chấm điểm** — ba trạng thái, **không** chấm bằng phần trăm hoàn thành: **ĐẠT** (số đo được và đạt ngưỡng) · **KHÔNG ĐẠT** (số đo được nhưng dưới ngưỡng) · **KHÔNG CHẠY ĐƯỢC** (**không có số để chấm** ⇒ *không phải* "tạm đạt"). Với đội 1 người, chấm *"70% xong"* là cách rẻ nhất để tự lừa mình.

### 7.1 Q4/2026 — chu kỳ chính (4 Objective · 13 KR)

Nguồn: **[OKRs §3](../010-Planning/OKRs.md#3-q42026--chu-kỳ-chính)**. Phạm vi 10–12/2026 = **MVP1 Story Intelligence**, đóng lại bằng gate **G2**.

| Objective | KR | Ý định | FR liên quan |
|---|---|---|---|
| **O1** — Đặt nền dữ liệu mà về sau không ai phải quay lại sửa | **KR1.1** | Không có đường rò rỉ chéo tenant | `FR-E-01` |
| | **KR1.2** | Bằng chứng pháp lý **không thể thiếu ngẫu nhiên** (5/5 hạng mục provenance + test cùng transaction) | `FR-G-01` |
| | **KR1.3** | Mọi file vào hệ thống đều đi qua **cửa pháp lý** (opt-out Điều 37b) | `FR-G-02` |
| **O2** — Dạy hệ thống tự đọc truyện, thay vì mình đọc hộ nó | **KR2.1** | Pipeline **nuốt được rác của đời thật** (text clean là bước đầu tiên) | `FR-B-01` |
| | **KR2.2** | Extraction đủ tốt để con người **chỉ phải sửa, không phải viết lại**. ⚠️ Ngưỡng của KR này mang nhãn `[EM]` — do writer `Roadmap` định nghĩa, **không có nguồn ngoài** | `FR-B-02` |
| | **KR2.3** | Mọi thay đổi về sau **không còn là thay đổi mù** (eval kit **cho ra số**) | `FR-H-01` · `FR-H-06` |
| **O3** — Trả lời câu hỏi kinh tế bằng số thật, trước khi tiêu thêm một đồng | **KR3.1** | Biến quyết định của cả mô hình tài chính (**regen ratio p50/p90**) **có giá trị số**. ⚠️ Không có dữ liệu ⇒ **G2 KHÔNG CHẠY ĐƯỢC**, không phải PASS mặc định | `FR-F-01` |
| | **KR3.2** | Gate kinh tế **chạy đúng lịch** — verdict G2 được **ghi ra văn bản** | `FR-F-01` · `FR-F-02` |
| | **KR3.3** | **COGS không bao giờ phải ước lượng lại** (4 cột không NULL) | `FR-F-02` |
| **O4** — Có sẵn một hàng người chờ trước khi có thứ để bán | **KR4.1** | Build-in-public — kênh **$0 spend** | *ngoài phạm vi code* |
| | **KR4.2** | SEO listicle / comparison. ⚠️ Neo bằng chứng của KR này là **quan sát SERP**, mang nhãn `[EM]`, **không phải số traffic đo được** | *ngoài phạm vi code* |
| | **KR4.3** | ⭐ **Trò chuyện 1-1 CÓ GHI CHÉP với tác giả** — đồng thời là **cách đóng `TBD` của [mục 3.3](#33--tbd--persona-jtbd-và-định-nghĩa-đủ-tốt)** và lấp khoảng trống willingness-to-pay | *đầu vào để viết lại mục 3* |
| | **KR4.4** | **Positioning bắt buộc**: nêu rõ AI-assisted + nhắm **writer**, không nhắm artist | `FR-G-04` · [NG-1](#23-non-goals) |

> ⚠️ **Chu kỳ này KHÔNG có KR doanh thu, và đó là chủ ý.** Ba mắt xích: (1) thứ bán được trong horizon là **Tầng 1 không có image gen**; (2) nội dung Tầng 1 ≈ MVP1 + MVP2 + **export**, mà export là exit criterion của **MVP2**, tức 01–02/2027 — Q4/2026 chỉ có MVP1; (3) **G0 chặn cứng việc bật thanh toán**, và thời gian chờ luật sư là `TBD` **nằm ngoài tầm kiểm soát của Founder**. ⇒ Đặt một KR doanh thu ở Q4/2026 là **đặt một con số không thể đúng**.

### 7.2 Q1/2027 — PREVIEW (3 Objective · 8 KR)

Nguồn: **[OKRs §4](../010-Planning/OKRs.md#4-preview-q12027)**.

> [!NOTE]
> **Đây là PREVIEW, KHÔNG phải cam kết.** Ba Objective dưới đây **sẽ được chốt lại vào cuối Q4/2026**, sau khi có verdict **G2** và sau khi biết MVP1 có vừa ba tháng hay không. Rủi ro đã biết trước: **MVP1 có thể tràn khỏi Q4/2026**; nếu vậy **MVP2 bị đẩy ra ngoài horizon** và toàn bộ mục này phải **viết lại** — ⛔ **không nén cho vừa khung** (CF-8.13 · CẤM-08).

| Objective | KR | Ý định | FR liên quan |
|---|---|---|---|
| **O5** — Biến Comic IR thành thứ người ngoài nhìn thấy được | **KR5.1** | Director tự động **thay cho panel script viết tay** | `FR-C-02` |
| | **KR5.2** | **Khách thấy được thành phẩm** (export PDF 1 chapter từ preview server-side) | `FR-D-04` · `FR-H-04` |
| | **KR5.3** | Trần nhân vật là **ràng buộc DB**, không phải lời khuyên trong prompt. ⚠️ Nếu `G1-d` dưới ngưỡng, trần **siết xuống ≤2** | `FR-C-04` |
| **O6** — Sẵn sàng nhận đồng tiền đầu tiên một cách hợp pháp | **KR6.1** | Rủi ro nhị phân duy nhất **có câu trả lời bằng văn bản**. ⚠️ KR này đo **TRẠNG THÁI, không đo tốc độ** | `FR-G-04` (câu Q2) · *chủ yếu ngoài phạm vi code* |
| | **KR6.2** | **Không tạo nghĩa vụ pháp lý không rút lại được** — checklist safe harbour đủ 6/6 **trước lần đầu mở cho người ngoài upload** | `FR-G-03` |
| | **KR6.3** | **Hai human gate không bypass được** — đo bằng **sự VẮNG MẶT của đường code bypass**, không đo bằng cấu hình | `FR-C-06` · `FR-C-07` |
| **O7** — Có người trả tiền thật, ở đúng thang mà số liệu cho phép | **KR7.1** | **Đồng tiền đầu tiên** ở Tầng 1. ⚠️ **Hai điều kiện tiên quyết**: (a) **G0 PASS** — chặn cứng; (b) Founder **chọn** bán Tầng 1 tại G2 — đây là **một lựa chọn, không phải kế hoạch đã chốt** | `FR-F-06` · `FR-E-04` |
| | **KR7.2** | **MRR được báo cáo đúng thang, không đúng ước mơ** — mỗi tháng đối chiếu với dải SOM năm 1. ⚠️ Dải đó là mục tiêu của **cả năm 1 tính từ bản trả phí đầu tiên**, **không** phải mục tiêu của hai tháng 01–02/2027. Con số và nhãn: xem [OKRs KR7.2](../010-Planning/OKRs.md#4-preview-q12027) | `FR-F-06` |

### 7.3 Chỉ số theo dõi — KHÔNG phải KR

Nguồn: **[OKRs §5](../010-Planning/OKRs.md#5-chỉ-số-theo-dõi-không-phải-kr)**.

> **Ranh giới, một câu**: **sự tồn tại của phép đo là KR; GIÁ TRỊ của phép đo thì KHÔNG có mục tiêu**, vì chưa có baseline nào để đặt mục tiêu một cách trung thực. Bảy chỉ số dưới đây **được đo và được ghi lại**, nhưng **không ai bị chấm KHÔNG ĐẠT vì nó**. Đặt ngưỡng cho chúng bây giờ là **bịa**.

| # | Chỉ số theo dõi | Vì sao **chưa** đặt mục tiêu | FR sinh ra dữ liệu |
|---|---|---|---|
| **M-1** | Regen ratio **p50 / p90** | Chưa có baseline. Ngưỡng đặt trước khi đo là ngưỡng bịa | `FR-F-01` |
| **M-2** | ⭐ **Human-reject rate sau VLM-select** | ⚠️ **Chưa ai công bố con số này.** Có ngưỡng **một lần** tại `G1-c` cho MVP0; từ Q4/2026 trở đi chỉ là **xu hướng** | `FR-A-01` · `FR-H-01` |
| **M-3** | Tỉ lệ panel đạt ở **multi-character 2–3 nhân vật** | **KHÔNG benchmark độc lập nào đo frontier model ở mức này** `[OFF]` ⇒ mọi mục tiêu đặt ra sẽ là **ước lượng đội lốt dữ liệu**. ⇒ **MVP0 là phép đo ĐẦU TIÊN** | `FR-C-04` · `FR-H-06` |
| **M-4** | `cost_usd` **thực đo** / chapter | ⚠️ Con số đối chiếu là **SÀN, không phải trần** (chưa tính VLM call để score 3 candidate) — *"một mục tiêu đặt trên một sàn là mục tiêu sai hướng"*. ⛔ CẤM dùng nó như chi phí thực tế mà không nêu nó là sàn (CẤM-04) | `FR-F-02` |
| **M-5** | Tỉ lệ user vượt **~125 ảnh/tháng** `[TC]` | Chỉ đo được khi có user thật. ⚠️ Hệ quả phải ghi lại: **1 chapter @N=3 vượt ngưỡng ngay ở chapter đầu tiên** `[EM]` ⇒ dự kiến phần lớn user hoạt động sẽ vượt, và khi đó **BYOK có thể không còn là *"tuỳ chọn mở khoá"* trên thực tế** — đó là **một phát hiện phải ghi lại, KHÔNG phải một lỗi đo** | `FR-F-01` · `FR-F-05` |
| **M-6** | Retention / GRR | Band tham chiếu của ngành **dùng sai dataset cho dự án này** — bộ lọc quy mô của nó **loại đúng nhóm indie mà comic-studio thuộc về**. Con số, nhãn và **ba caveat bắt buộc** đi kèm: xem [OKRs M-6](../010-Planning/OKRs.md#5-chỉ-số-theo-dõi-không-phải-kr) và [Glossary *GRR*](../999-Resources/Glossary.md) — ⛔ **trích con số mà bỏ ba caveat là TRÍCH SAI** (CẤM-06) | *khi có user thật* |
| **M-7** | Speaker attribution error rate | Con số tham chiếu mang nhãn ⚠️ `[EM]` — **ước lượng, KHÔNG phải số đo** | `FR-C-06` |

### 7.4 Ba gate là thước cuối cùng — không thay thế được cho nhau

Nguồn: **[MVP-Scope §7](../010-Planning/MVP-Scope.md#7-gono-go-decision)**. PRD **không** định nghĩa lại ngưỡng.

| Gate | Đo cái gì | Nếu FAIL |
|---|---|---|
| **G0** — Pháp lý | Rủi ro **nhị phân**. ⚠️ Chặn **thương mại hoá**, **KHÔNG** chặn MVP0–MVP1 | Dừng thương mại hoá; đường ra: cấu trúc lại mô hình rồi chạy lại G0 |
| **G1** — Kỹ thuật (cuối 09/2026, sau MVP0) | Tiền đề sản phẩm còn đứng không | Đổi cách tiếp cận — và **biết sau 2 tuần thay vì 4 tháng**. ⚠️ **FAIL ≠ huỷ dự án** |
| **G2** — Kinh tế (cuối Q4/2026, sau MVP1) | Mô hình giá có sống được không | Đường lui đã thiết kế sẵn: whole-page (`FR-A-07`) → per-panel trả phí → BYOK (`FR-F-05`). ⛔ **Đường KHÔNG được đi: hạ N từ 3 xuống 1** |

> *"Một sản phẩm hợp pháp mà không consistency thì vô dụng; consistency tốt mà lỗ mỗi lần dùng thì không sống được; ngon và có lãi mà bất hợp pháp thì không được tồn tại."*
>
> ⛔ **CẤM sửa ngưỡng gate sau khi nhìn thấy kết quả** — *"đó là cách một gate biến thành nghi lễ"* (CẤM-16).

---

## 8. Tài liệu liên quan

### 8.1 Tám BRD — chi tiết hoá từng module của [mục 4](#4-yêu-cầu-chức-năng-theo-8-module)

| Module PRD | BRD |
|---|---|
| [A. Pipeline sinh ảnh](#a-pipeline-sinh-ảnh) | [BRD-001-Image-Generation-Pipeline](./BRD/BRD-001-Image-Generation-Pipeline.md) |
| [B. Story Intelligence](#b-story-intelligence) | [BRD-002-Story-Intelligence](./BRD/BRD-002-Story-Intelligence.md) |
| [C. Comic Director & Layout](#c-comic-director--layout) | [BRD-003-Comic-Director-And-Layout](./BRD/BRD-003-Comic-Director-And-Layout.md) |
| [D. Editor & UI](#d-editor--ui) | [BRD-004-Minimum-Editor](./BRD/BRD-004-Minimum-Editor.md) |
| [E. Multi-tenancy & hạ tầng](#e-multi-tenancy--hạ-tầng) | [BRD-005-Multi-Tenancy-And-Platform](./BRD/BRD-005-Multi-Tenancy-And-Platform.md) |
| [F. Kinh tế & credit](#f-kinh-tế--credit) | [BRD-006-Credit-And-Unit-Economics](./BRD/BRD-006-Credit-And-Unit-Economics.md) |
| [G. Pháp lý & compliance](#g-pháp-lý--compliance) | [BRD-007-Legal-And-Compliance](./BRD/BRD-007-Legal-And-Compliance.md) |
| [H. Chất lượng & vận hành](#h-chất-lượng--vận-hành) | [BRD-008-Quality-And-Operations](./BRD/BRD-008-Quality-And-Operations.md) |

### 8.2 Tám Epic — trục backlog, cắt theo **module A–H**, KHÔNG theo mốc MVP

| Module PRD | Epic |
|---|---|
| [A. Pipeline sinh ảnh](#a-pipeline-sinh-ảnh) | [Epic-Image-Generation-Pipeline](../022-User-Stories/Epics/Epic-Image-Generation-Pipeline.md) |
| [B. Story Intelligence](#b-story-intelligence) | [Epic-Story-Intelligence](../022-User-Stories/Epics/Epic-Story-Intelligence.md) |
| [C. Comic Director & Layout](#c-comic-director--layout) | [Epic-Comic-Director-And-Layout](../022-User-Stories/Epics/Epic-Comic-Director-And-Layout.md) |
| [D. Editor & UI](#d-editor--ui) | [Epic-Minimum-Editor](../022-User-Stories/Epics/Epic-Minimum-Editor.md) |
| [E. Multi-tenancy & hạ tầng](#e-multi-tenancy--hạ-tầng) | [Epic-Multi-Tenancy-And-Platform](../022-User-Stories/Epics/Epic-Multi-Tenancy-And-Platform.md) |
| [F. Kinh tế & credit](#f-kinh-tế--credit) | [Epic-Credit-And-Unit-Economics](../022-User-Stories/Epics/Epic-Credit-And-Unit-Economics.md) |
| [G. Pháp lý & compliance](#g-pháp-lý--compliance) | [Epic-Legal-And-Compliance](../022-User-Stories/Epics/Epic-Legal-And-Compliance.md) |
| [H. Chất lượng & vận hành](#h-chất-lượng--vận-hành) | [Epic-Quality-And-Operations](../022-User-Stories/Epics/Epic-Quality-And-Operations.md) |

> **Quan hệ ba tầng là 1:1:1** — mỗi module PRD ↔ đúng một BRD ↔ đúng một Epic. Nhờ vậy traceability là **một link**, không phải một ma trận.
>
> **Cấu trúc tám H3 của [mục 4](#4-yêu-cầu-chức-năng-theo-8-module) là contract cứng**: mỗi Epic trỏ vào anchor của heading tương ứng bằng `Implements:`. ⛔ **Đổi tên hoặc đổi thứ tự tám H3 đó ⇒ 8 link Epic chết.**

### 8.3 Tài liệu cùng tầng Requirements

- **[SRS-Comic-Studio.md](./SRS-Comic-Studio.md)** — **nguồn duy nhất** của yêu cầu kỹ thuật và yêu cầu phi chức năng. [Mục 5](#5-yêu-cầu-phi-chức-năng) của PRD **chỉ trỏ sang đây, không lặp lại nội dung.**

> Thiết kế kỹ thuật (schema, API, ADR) **sẽ được đặc tả tại tầng `030-Specs`** — tầng đó hiện rỗng và **ngoài phạm vi run này**, nên PRD **không** link tới nó.

### 8.4 Tài liệu tham khảo

#### Tầng Planning — nguồn của mọi nội dung trong PRD này

| Tài liệu | PRD trích mục nào của nó |
|---|---|
| [MVP-Scope.md](../010-Planning/MVP-Scope.md) | **§3** bảng 8 nhóm A–H (nguồn của [mục 4](#4-yêu-cầu-chức-năng-theo-8-module)) · **§4** cắt gì vì sao · **§5** editor tối thiểu (chi tiết module D) · **§6** KC-1…KC-7 · **§7** ba gate · **§8** kill criteria |
| [Charter-Comic-Studio.md](../010-Planning/Charter-Comic-Studio.md) | **§3** năm mục tiêu MT-1…MT-5 · **§4** chín điều kiện khả thi R1–R9 · **§5.1/§5.2** Scope In–Out · **§6** RACI (nguồn của actor Founder và của ba lỗ hổng ở [mục 3.3](#33--tbd--persona-jtbd-và-định-nghĩa-đủ-tốt)) · **§7** ràng buộc C1–C10 · **§9** blocker |
| [OKRs.md](../010-Planning/OKRs.md) | **§3 · §4 · §5 · §6** — nguồn **DUY NHẤT** của [mục 7](#7-success-metrics) và của các anti-goal ở [mục 2.3](#23-non-goals) |
| [Roadmap.md](../010-Planning/Roadmap.md) | Nguồn mốc thời gian và exit criteria. PRD **không** trả lời câu *"khi nào"* |
| [Risk-Register.md](../010-Planning/Risk-Register.md) | Sổ rủi ro, rà soát theo gate G0/G1/G2 |

#### Căn cứ thẩm định và quy ước

| Tài liệu | Vai trò với PRD |
|---|---|
| [Analysis-Comic-Studio-Concept.md](../050-Research/Analysis-Comic-Studio-Concept.md) | **Nguồn thẩm định gốc.** §3.2 là nguồn xác nhận khoảng trống persona ở [mục 3.3](#33--tbd--persona-jtbd-và-định-nghĩa-đủ-tốt) · §4.2 bảng khả thi · §5.1/5.5/5.7 · §6 ba thứ nên cắt · §8.5 ba câu luật sư · §9b.3 · §11 khoảng trống dữ liệu · §12. ⛔ Đây là **dấu vết quyết định tại thời điểm viết — KHÔNG sửa nó** (CẤM-18); tài liệu mới **link sang** |
| [Analysis-Market-Competitor-Landscape.md](../050-Research/Analysis-Market-Competitor-Landscape.md) | Nguồn của các con số thị trường / retention / pricing được dẫn **qua bảng Canonical Facts**, không trích trực tiếp |
| [Glossary.md](../999-Resources/Glossary.md) | **Ubiquitous Language.** PRD dùng **đúng tên đã có** và **không đặt tên mới**: `Story Bible` · `Comic IR (Comic Intermediate Representation)` · `Panel Specification` · `Visual Prompt Compiler` · `Layout Director` · `precedence ladder` · `constraint budget` · `syuzhet vs fabula` · `timeline_id` · `Identity vs Appearance` · `Canonical Reference` · `attribute binding` · `best-of-N (N=3)` · `Continuity Checker` · `re-identification` · `Layout Score` · `VLM autorater` · `error cascade` · `typeset layer` · `text_safe_zone` · `dialogue condensation` · `speaker attribution` · `HITL gate` · `MVP0` · `vertical slice` · `eval kit` · `preference data` · `tenant_id` · `RLS` · `BYOK` · `credit ledger + hold` · `hold reaper` · `usage_event` · `seam kinh tế vs seam kỹ thuật` |
| [Documents-Template.md](../../knowledge-base/99-Templates/Documents-Template.md) | **RULE-001** — naming convention, frontmatter, và quy tắc #5: **standard markdown link**, ⛔ **KHÔNG wiki-link** |
| [Template-PRD.md](../999-Resources/Templates/Template-PRD.md) | Khuôn tham khảo. PRD này **mở rộng** khuôn đó: tách `Non-Goals` ra khỏi mục 2 thành [mục 6.4](#64-scope-out--không-thuộc-về-sản-phẩm), tách `Ranh giới scope` thành mục riêng, và thu gọn mục *Non-Functional Requirements* thành một con trỏ sang SRS |

#### Nguồn ngoài — dẫn lại **qua bảng Canonical Facts**, không tra lại

> ⛔ **CẤM tự tra lại hoặc tự tính lại một con số đã có trong bảng CF.** Nhân/chia hai số CF để tạo số thứ ba **phải gắn nhãn `[EM]`** cho kết quả (CẤM-15).

| Nội dung | Nguồn | Nhãn |
|---|---|---|
| **N=3** best-of-N — *"performance saturates at N=3"* | [arXiv 2604.13452](https://arxiv.org/html/2604.13452v1) | `[OFF]` |
| CogCanvas **ID-Sim** theo số nhân vật — *"near-complete failure beyond three subjects"* | [arXiv 2606.15867](https://arxiv.org/html/2606.15867) | `[OFF]` |
| **Nghị định 134/2026/NĐ-CP** — Điều 5a · Điều 37a · Điều 37b (hiệu lực 09/04/2026) | [Cục Bản quyền tác giả](https://cov.gov.vn/tin-tuc/gioi-thieu-nghi-dinh-so-1342026ndcp-quy-dinh-ve-quyen-tac-gia-quyen-lien-quan-168925.html) · [Baker McKenzie](https://www.bakermckenzie.com/en/insight/publications/2026/05/vietnam-redefining-copyright-for-ai) | `[OFF]` — ⚠️ **Điều 37a hiện chỉ biết qua bản TÓM TẮT, không phải nguyên văn** |
| **Luật SHTT sửa đổi 2022 — Luật số 07/2022/QH15** — Điều 198b (miễn trừ trung gian, chuyển hoá từ Điều 12.55 EVFTA) | xem bảng canon tại [BRD-007 §3](./BRD/BRD-007-Legal-And-Compliance.md#3-yêu-cầu-nghiệp-vụ) | `[OFF]` |
| **Luật Trí tuệ nhân tạo 2025 — Luật số 134/2025/QH15** — Điều 11 · khoản 4 Điều 11 · Điều 8 (hiệu lực 01/03/2026) | xem bảng canon tại [BRD-007 §3](./BRD/BRD-007-Legal-And-Compliance.md#3-yêu-cầu-nghiệp-vụ) | `[OFF]` |

> ⛔ **BA văn bản pháp lý riêng biệt, KHÔNG được gộp — hai trong số đó cùng số 134.** `NĐ 134/2026/NĐ-CP` (Điều 5a/37a/37b) ≠ `Luật số 134/2025/QH15` (Điều 11, khoản 4 Điều 11, Điều 8) ≠ `Luật số 07/2022/QH15` (Điều 198b). **Điều 198b KHÔNG thuộc NĐ 134/2026** — bảng này từng gộp nó vào hàng NĐ 134/2026 và đã được sửa sau verify L23. Nguồn canon duy nhất cho ánh xạ điều luật ↔ văn bản là [BRD-007](./BRD/BRD-007-Legal-And-Compliance.md); mọi tài liệu khác **dẫn lại**, không tự gán.
| Kỳ vọng gross margin **50–60%** | ICONIQ 52% · Bessemer 50–60% | `[BCN]` |

---

_Generated by Comic Studio — role `business-analyst`._
_Author: trisjr_
