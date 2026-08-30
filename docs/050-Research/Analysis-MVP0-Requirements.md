---
id: RESEARCH-003
type: research
status: draft
project: comic-studio
owner: "@trisjr"
tags: [comic-studio, mvp0, requirements-analysis, gate-g1, execution-readiness, doc-consistency]
created: 2026-08-30
updated: 2026-08-30
---

# Phân tích Yêu cầu MVP0 — comic-studio

> Tài liệu này trả lời **đúng hai câu hỏi**: *(1) MVP0 đã đủ điều kiện bắt đầu chưa?* và *(2) yêu cầu MVP0 nằm rải ở bốn tầng tài liệu có mâu thuẫn nhau chỗ nào?*
>
> ⛔ **Đây KHÔNG phải nguồn sự thật mới.** Mọi con số dưới đây đều trỏ về anchor gốc. Nếu một ô ở đây lệch với nguồn, **nguồn đúng** — và ô đó là một bug của chính tài liệu này.

## Mục lục

- [1. Ranh giới tài liệu](#1-ranh-giới-tài-liệu)
- [2. MVP0 là gì — hợp nhất từ bốn tầng](#2-mvp0-là-gì--hợp-nhất-từ-bốn-tầng)
- [3. Điều kiện ra — hai lớp không thay thế nhau](#3-điều-kiện-ra--hai-lớp-không-thay-thế-nhau)
- [4. Ma trận truy vết Story × tiêu chí](#4-ma-trận-truy-vết-story--tiêu-chí)
- [5. Sẵn sàng thực thi](#5-sẵn-sàng-thực-thi)
  - [5.4 Phiếu chọn chapter — tiêu chí `C-1…C-8`](#54-phiếu-chọn-chapter--tiêu-chí-c-1c-8)
- [6. Nhất quán tài liệu — 7 phát hiện](#6-nhất-quán-tài-liệu--7-phát-hiện)
- [7. Câu hỏi mở cần Founder đóng](#7-câu-hỏi-mở-cần-founder-đóng)
- [8. Tài liệu tham khảo](#8-tài-liệu-tham-khảo)

---

## 1. Ranh giới tài liệu

| Câu hỏi | Tài liệu trả lời |
|---|---|
| Cái gì vào MVP0, cái gì bị cắt | [MVP-Scope §3](../010-Planning/MVP-Scope.md) |
| Khi nào, theo thứ tự nào, exit criteria | [Roadmap §2, §3.1](../010-Planning/Roadmap.md) |
| Story nào, rank nào, tốn bao nhiêu giờ | [Backlog-Priority §3.1](../022-User-Stories/Backlog-Priority.md) |
| **MVP0 bắt đầu được chưa, và tài liệu có tự mâu thuẫn không** | **Tài liệu này** |

⛔ Tài liệu này **không** đặt ngưỡng mới, **không** chấm lại `Scope-Label`, **không** sửa `E_build`. Nó chỉ **đối chiếu** và **báo lệch**.

---

## 2. MVP0 là gì — hợp nhất từ bốn tầng

### 2.1 Định nghĩa canon

MVP0 là **vertical slice trước MVP1** — mục đích **không phải có sản phẩm** mà để biết **tiền đề còn đứng không**, sau 1–2 tuần thay vì sau 4 tháng ([Glossary](../999-Resources/Glossary.md) headword `MVP0`).

> ⛔ **`CẤM-11`**: chỉ dùng tên **MVP0**. Không *"phase 0"*, không *"spike"*, không *"PoC"*.

### 2.2 Phạm vi — cái gì có, cái gì dứt khoát không

| | Nội dung | Neo |
|---|---|---|
| **Có** | **1 chapter duy nhất** · Story Bible 2–3 nhân vật **viết tay** · panel script **~8–30 panel viết tay** | `Roadmap §3.1` việc 2 |
| **Có** | Code làm **đúng một việc**: generate panel với reference + **N=3** candidate + VLM select | `MVP-Scope §1.3` · `CF-8.4` |
| **Có** | Trang composite **có speech bubble** (overlay layer) | `Roadmap §2` deliverable (2) · `G1-e` |
| ⛔ **Không** | **Không database** — ô `A5 = ❌` tại MVP0 là **chủ ý**, không phải sót | `MVP-Scope §3.1` |
| ⛔ **Không** | **Không UI** — script + file phẳng | `Roadmap §3.1` việc 2 |
| 🟡 **Bán phần** | Provenance `GP-1 = 🟡`: MVP0 chỉ ghi tay ra CSV/file đủ để đo. *"Generation đầu tiên"* có nghĩa pháp lý = **MVP1** | `MVP-Scope §3.1` |

### 2.3 Kỷ luật bắt buộc — và cách nhận ra khi đang vi phạm

> **Code của MVP0 KHÔNG phải nền của sản phẩm — viết để trả lời câu hỏi rồi bỏ, giữ lại kết luận và dữ liệu.** (`MVP-Scope §3.1` · `Roadmap §3.1`)

| Rủi ro | Dấu hiệu sớm (`Roadmap §3.1`) | Xử lý |
|---|---|---|
| Spike biến thành nền móng | Bắt đầu viết migration, config loader, abstraction cho provider | Dừng. MVP0 không có DB |
| Tràn ngân sách | Chi vượt **~$25** mà chưa đủ 8 panel liền nhau để chấm | Trần thực tế **~$50**. Vượt ⇒ dừng, kết luận với dữ liệu đang có |
| Chấm consistency bằng cảm tính | Không có bảng chấm, chỉ có ấn tượng | Ngưỡng đã định nghĩa sẵn ở `G1`. **Định nghĩa trước, đo sau** |
| Bỏ qua typeset | Trang composite không có speech bubble | `CF-8.11c`: typeset nổ ngay ở panel có thoại **đầu tiên** ⇒ nằm trong MVP0 |

### 2.4 Ngân sách

**~$12** `[EM tính từ OFF]` (`CF-3.11`, ở giá standard $0.134; ~$6 nếu batch, nhưng lấy **số cao làm trần an toàn** vì cần vòng lặp nhanh) · trần thực tế **~$50** (`Analysis §10`) · thời lượng **1–2 tuần** (`CF-8.4` — ⭐ **mốc duy nhất có thời lượng đến từ nguồn**, `Roadmap §2`).

---

## 3. Điều kiện ra — hai lớp không thay thế nhau

MVP0 bị ràng buộc bởi **hai bộ tiêu chí khác loại**. Nhầm lẫn hai bộ này là cách dễ nhất để tưởng mình đã xong.

### 3.1 Lớp artifact — `P-1…P-6` (`Roadmap §2`)

Nghĩa vụ **tạo ra vật thể**. Đo bằng: *nó có tồn tại không?*

| # | Nội dung | Ai/cái gì tạo ra |
|---|---|---|
| `P-1` | 3/3 câu `CF-7.8` đã gửi tới **một luật sư SHTT VN có tên**, có xác nhận đã nhận | Founder — ⛔ không phải Story nào |
| `P-2` | `G1` có **SỐ cho cả 5 tiêu chí** + verdict được ghi | 5 Story `[MVP0]` cộng lại |
| `P-3` | Regen ratio **p50 và p90** có giá trị số | `Story-Generate-Panel-With-Reference-And-VLM-Select` |
| `P-4` | Khoá thời gian thay `(chapter, scene)` viết ra dưới dạng **schema draft** | `Story-Fix-Narrative-Time-Key` |
| `P-5` | Danh sách phải-có-trong-schema **chốt = 7 mục `KC-1…KC-7`** | Founder + Architect — ⭐ **chỉ CHỐT DANH SÁCH**, không implement (`KC-1…KC-6` từ MVP1, `KC-7` từ MVP3) |
| `P-6` | Golden dataset tồn tại dưới dạng file (spec + ref + ảnh + bảng chấm) | `Story-Golden-Dataset-For-Regression` |

### 3.2 Lớp ngưỡng — `G1-a…G1-e` (`MVP-Scope §7.2`)

Nghĩa vụ **đạt ngưỡng đã định nghĩa TRƯỚC khi đo**.

| # | Ngưỡng PASS | Nhãn nguồn |
|---|---|---|
| `G1-a` | **≥70%** panel nhận ra là cùng một nhân vật, không cần retry | đề xuất lens kiến trúc run trước |
| `G1-b` | **N ≤ 3** | `findings/architect.md §7.3` + `CF-3.1` `[OFF]` *"saturates at N=3"* |
| `G1-c` | **≤30%** PASS · **30–50%** PASS CÓ ĐIỀU KIỆN · **>50%** FAIL | ⚠️ **`[EM]` — không có nguồn ngoài.** Chỉ số này **chưa ai công bố** |
| `G1-d` | Panel **2 nhân vật ≥60%** (đúng identity **VÀ** đúng attribute binding); panel 3 nhân vật **đo và báo cáo, không đặt ngưỡng chặn** | ⚠️ **`[EM]`.** `CF-6.5` `[OFF]`: ID-Sim sụp 42.33 (2 người) → 27.21 (3) ⇒ đặt cùng ngưỡng cho cả hai là đặt sai |
| `G1-e` | **100%** panel có thoại dùng overlay; **0** panel nhờ model render chữ | `findings/architect.md §7.3` · `Analysis §4.2` |

⭐ **Đo thêm, không chặn nhưng bắt buộc có số**: regen ratio **p50/p90**. Thiếu nó ⇒ **`G2` KHÔNG CHẠY ĐƯỢC**, ⛔ không PASS mặc định (`Roadmap §6.2`).

> [!IMPORTANT]
> **`G0` (gate pháp lý) ⛔ KHÔNG chặn MVP0.** Không có người ngoài upload ⇒ không phát sinh nghĩa vụ safe harbour; không thu tiền ⇒ không phải khai thác thương mại (`Roadmap §6.1`). `G0` được **khởi động song song** vì thời gian chờ luật sư nằm ngoài tầm kiểm soát.

---

## 4. Ma trận truy vết Story × tiêu chí

| Story | Rank | `E_build` `[EM]` | Sở hữu tiêu chí | ⭐ |
|---|:-:|---|---|:-:|
| [Fix-Narrative-Time-Key](../022-User-Stories/Backlog/Story-Fix-Narrative-Time-Key.md) | 1 | 8h | `P-4` | ⭐ |
| [Record-Readability-Human-Judgement](../022-User-Stories/Backlog/Story-Record-Readability-Human-Judgement.md) | 2 | ~4h | *(không tiêu chí G1 nào)* — DoD riêng: 100% panel MVP0 có bản ghi readability | |
| [Golden-Dataset-For-Regression](../022-User-Stories/Backlog/Story-Golden-Dataset-For-Regression.md) | 3 | ~6h | `P-6` — nguyên liệu đo của cả 5 tiêu chí | ⭐ |
| [Comic-IR-Panel-Specification](../022-User-Stories/Backlog/Story-Comic-IR-Panel-Specification.md) | 4 | ~20h ⚠️ vượt trần | nền cho `G1-d` (spec để chấm) | ⭐ |
| [Generate-Panel-With-Reference-And-VLM-Select](../022-User-Stories/Backlog/Story-Generate-Panel-With-Reference-And-VLM-Select.md) | 5 | ~24h ⚠️ vượt trần | ⭐ **`G1-a` · `G1-b` · `G1-c` · `G1-d` · `P-3`** | ⭐ |
| [Typeset-Layer-And-Bubble-Overlay](../022-User-Stories/Backlog/Story-Typeset-Layer-And-Bubble-Overlay.md) | 6 | ~8h | **`G1-e`** | ⭐ |
| [Deterministic-Visual-Prompt-Compiler](../022-User-Stories/Backlog/Story-Deterministic-Visual-Prompt-Compiler.md) | 7 | ~14h | hỗ trợ `G1-d` (spec sai vs hệ thống ngẫu nhiên) | ⭐ |
| [Image-Provider-Adapter](../022-User-Stories/Backlog/Story-Image-Provider-Adapter.md) | 8 | ~6h | hỗ trợ `G1-a`/`G1-c`, ⛔ không tự nó là con số đo | |

**Tổng `E_build` khai báo: ~90 giờ-người** — xem [F-1](#f-1--90-giờ-người-vs-12-tuần-con-số-không-so-sánh-trực-tiếp-được).

⭐ **4/5 tiêu chí `G1` do MỘT Story sở hữu.** `Story-Generate-Panel-With-Reference-And-VLM-Select` là điểm đơn nhất quyết định gate — trượt Story này là trượt cả MVP0.

---

## 5. Sẵn sàng thực thi

### 5.1 Điều kiện tiên quyết — trạng thái thực tế

| # | Điều kiện tiên quyết | Trạng thái (kiểm cơ học `2026-08-30`) | Chặn |
|:-:|---|---|:-:|
| 1 | **1 chapter truyện chữ có bản quyền rõ ràng** (`Roadmap §3.1` Input) | ⛔ **Không tìm thấy tài liệu nào trong repo xác nhận chapter đã được chọn** | 🔴 Cứng |
| 2 | Story Bible 2–3 nhân vật **viết tay** | ⛔ Chưa tồn tại — phái sinh từ #1 | 🔴 Cứng |
| 3 | Panel script ~8–30 panel **viết tay** | ⛔ Chưa tồn tại — phái sinh từ #1, #2 | 🔴 Cứng |
| 4 | **Image provider đã chọn** | ⚠️ [ADR-016](../030-Specs/Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) `status: draft`, chốt **hình dạng seam**, còn **5 ô `TBD`** | 🟡 Mềm |
| 5 | **VLM provider đã chọn** | ⚠️ [ADR-007](../030-Specs/Architecture/ADR-007-VLM-Provider-For-QA-Select.md) `status: draft` — nguyên văn: *"chốt hình dạng, **chưa chốt vendor**"*, còn **5 ô `TBD`** | 🟡 Mềm |
| 6 | **Họ font render tiếng Việt** cho `G1-e` | ⛔ **`TBD` có chủ** — Architect + Founder, đóng **sau MVP0, trước gate `G1-e`** ([Typography](../040-Design/Design-System/Typography.md)) | 🟡 Mềm |
| 7 | Ngưỡng `[EM]` (`G1-c`, `G1-d`) được ký nhận trước khi đo | ⛔ Không tìm thấy dấu vết ký nhận | 🔴 Cứng — xem [F-4](#f-4--ba-ngưỡng-em-chưa-có-dấu-vết-ký-nhận) |
| 8 | Tài khoản/API key provider + ngân sách ~$12–50 | ⛔ Không kiểm được từ repo (nằm ngoài tài liệu) | — |

⚠️ **Kết luận sẵn sàng: MVP0 CHƯA bắt đầu được.** Ba điều kiện cứng (#1, #2, #3) đều phái sinh từ **một quyết định chưa ai ra**: chọn chapter nào. Đây là quyết định của **Founder**, ⛔ không có Story nào sở hữu nó và ⛔ không có exit criterion nào bắt nó phải xong.

### 5.2 Trạng thái nền kiến trúc

**7/8 ADR** mà MVP0 chạm tới còn `status: draft`; chỉ [ADR-001](../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) đã `accepted`.

| ADR | Status | Liên quan MVP0 |
|---|---|---|
| `ADR-001` Tech stack | ✅ `accepted` | Nghiệm thu tiếng Việt `#5` là **tiền đề của `G1-e`** |
| `ADR-007` VLM provider | ⚠️ `draft` | Vendor **chưa chốt** ⇒ `G1-b`, `G1-c` chưa có đối tượng đo |
| `ADR-016` Image provider | ⚠️ `draft` | Vendor **chưa chốt** ⇒ `G1-a`, `G1-d` chưa có đối tượng đo |
| `ADR-013` Typeset layer | ⚠️ `draft` · **13 ô `TBD`** | Sở hữu `TBD-FONT` chặn mềm `G1-e` |
| `ADR-014` Compiler + best-of-N · `ADR-012` Comic IR · `ADR-011` Time key · `ADR-008` LLM | ⚠️ `draft` | Nền của Story rank 1, 4, 7 |

> ⭐ **Điều này KHÔNG tự động chặn MVP0.** Kỷ luật `MVP-Scope §3.1` nói code MVP0 bị vứt ⇒ nó ⛔ không cần ADR `accepted` để chạy. Nhưng `G1-a`…`G1-d` là **phép đo trên một provider cụ thể**: đo trên provider A rồi sản phẩm chạy provider B thì **số đo không chuyển giao được**. ⇒ #4 và #5 là **mềm về code, cứng về giá trị của phép đo**.

### 5.3 Thứ tự thực thi suy ra từ chuỗi phụ thuộc

```text
[Founder] Chọn chapter + Story Bible + panel script viết tay   ← 🔴 chưa có chủ, chưa có exit criterion
        │
        ├─► [Founder+Architect] Ký nhận ngưỡng [EM] G1-c, G1-d  ← 🔴 "định nghĩa TRƯỚC, đo SAU"
        │
        ├─► [Founder+Architect] Chốt vendor image + VLM          ← 🟡 quyết định giá trị phép đo
        │
        ▼
Rank 4  Comic-IR (bản YAML viết tay)  ──┐
Rank 7  Compiler                       ─┤─► Rank 5  Generate + VLM select ──► G1-a,b,c,d · P-3
Rank 8  Image-Provider-Adapter         ─┘            │
                                                     ▼
                                        Rank 6  Typeset overlay ──► G1-e
                                                     │
                                                     ▼
                                        Rank 3  Golden dataset ──► P-6
                                        Rank 2  Readability (chạy liên tục, song song)

Rank 1  Fix-Narrative-Time-Key ──► P-4   (⭐ ĐỘC LẬP với nhánh sinh ảnh — chạy song song được)
```

⭐ **`Story-Fix-Narrative-Time-Key` không nằm trên đường găng sinh ảnh.** Nó phục vụ `P-4` và chặn **mọi bảng timeline của MVP1**, ⛔ không chặn `G1`. Xếp nó rank 1 là đúng theo `UNLOCK-ORDER`, nhưng ⛔ **không có nghĩa phải làm xong trước** khi bắt đầu nhánh sinh ảnh.


### 5.4 Phiếu chọn chapter — tiêu chí `C-1…C-8`

> Soạn để đóng [`Q-1`](#7-câu-hỏi-mở-cần-founder-đóng). ⭐ **Mỗi tiêu chí rút ra từ một tiêu chí `G1` cụ thể** — ⛔ không tiêu chí nào là sở thích biên tập. Chapter trượt `C-1`…`C-5` ⇒ MVP0 vẫn chạy được nhưng **gate `G1` thiếu tiêu chí đo**, tức `P-2` ⛔ không đạt.

| # | Chapter phải có | Phục vụ | Trượt thì hỏng gì |
|:-:|---|---|---|
| **C-1** | **≥2 nhân vật xuất hiện trong CÙNG một cảnh**, lặp lại đủ nhiều lần để chấm được tỉ lệ | `G1-d` (panel 2 nhân vật **≥60%**) | ⛔ `G1-d` **không có dữ liệu để đo** ⇒ gate thiếu 1/5 tiêu chí. Đây là **hàng load-bearing** (`CF-6.4`) |
| **C-2** | **≥1 cảnh có 3 nhân vật** cùng khung | `G1-d` phần *"đo và báo cáo, không đặt ngưỡng chặn"* | Không có ⇒ phải **ghi rõ là không đo được**, ⛔ không được im lặng bỏ qua. `CF-6.5` `[OFF]`: ID-Sim sụp 42.33 → 27.21 khi lên 3 người — đây chính là chỗ cần số |
| **C-3** | **2–3 nhân vật tái xuất hiện xuyên chapter**, đủ để có **8 panel liền nhau** cùng một nhân vật | `G1-a` (**≥70%**) — cách đo nguyên văn là *"nhìn 8 panel liền nhau"* | Nhân vật chỉ xuất hiện một lần ⇒ ⛔ **không đo được consistency**, vì consistency là thuộc tính **giữa các lần xuất hiện** |
| **C-4** | **Có thoại** — đối thoại thật, ⛔ không phải chapter thuần tự sự | `G1-e` (**100%** panel có thoại dùng overlay) | Chapter không thoại ⇒ `G1-e` đạt **một cách rỗng** (0/0 = 100%). `CF-8.11c`: typeset *"nổ ngay ở panel có thoại đầu tiên"* — không có thoại thì rủi ro ⛔ **không bị chạm tới**, chỉ bị hoãn |
| **C-5** | Thoại chứa **dấu chồng hai tầng** (`ế`, `ữ`, `ợ`) | Nghiệm thu bắt buộc của [ADR-001](../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Consequences` **#5**: corpus **cả NFC và NFD**, render 300 DPI, kiểm (a) ký tự ⛔ không tách khỏi dấu khi xuống dòng · (b) dấu ⛔ không bị mép bubble cắt cụt · (c) NFD và NFC cho **cùng** kết quả ngắt dòng | Corpus không có dấu chồng ⇒ ba phép kiểm (a)(b)(c) **chạy qua mà không chạm lỗi** ⇒ `TBD-FONT` bị đóng trên dữ liệu ⛔ không đại diện |
| **C-6** | **Kể trọn trong ≤30 panel** | `Roadmap §2` (~8–30 panel) + quyết định phủ trọn | ⭐ **Phần thưởng kèm theo**: cho ra **số panel/chapter THẬT**, thay được giả định **60 ảnh/chapter** `[EM]` `CF-3.3` — *"thừa số gốc của toàn bộ mô hình chi phí"* (`Charter §8 A1`), đóng luôn `G-07` của [Risk-Register](../010-Planning/Risk-Register.md) |
| **C-7** | Nội dung ⛔ **không chạm content policy** của provider (bạo lực đồ hoạ, tình dục, nhân vật có thật) | `G1-c` `reject_rate` sạch | Provider từ chối nhiều ⇒ `reject_rate` **trộn hai nguyên nhân khác loại** (VLM chọn tệ vs provider chặn) ⇒ verdict `G1-c` mất nghĩa. `D-67` ([SRS](../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-20`) bắt **ghi lại mọi lần từ chối** — nhưng ghi lại ⛔ không sửa được một mẫu đã nhiễm |
| **C-8** | ⭐ **Bằng chứng đồng ý bằng văn bản của tác giả**, lưu **cùng chỗ** với golden dataset | Nghĩa vụ phái sinh từ `H6` | Xem cảnh báo ngay dưới |

> [!IMPORTANT]
> ⭐ **Phạm vi đồng ý phải phủ việc DÙNG LẠI, ⛔ không chỉ việc chạy thử một lần.**
>
> Kỷ luật MVP0 nói **code bị vứt** — nhưng golden dataset thì ⛔ **không**: `MVP-Scope §3` hạng mục **`H6` = `✅` ở MỌI mốc MVP0–MVP4**, và [Epic-Quality-And-Operations](../022-User-Stories/Epics/Epic-Quality-And-Operations.md) gọi nó là *"tài sản dùng suốt vòng đời, không phải artifact của MVP0"*. `Roadmap §6.2` xác nhận nó là đầu vào của **eval kit `M1-6`**.
>
> ⇒ Chapter của người khác sẽ **sống trong repo lâu hơn chính MVP0**. Một lời đồng ý miệng cho *"thử một lần"* ⛔ **không** phủ được việc dataset đó còn được đọc ở MVP1, MVP2 và mọi lần chạy regression về sau. ⚠️ Đây ⛔ **không phải** câu hỏi `G0`: `G0` đo rủi ro **thương mại hoá** (`Roadmap §6.1` — MVP0 không có khách, không thu tiền). Đây là rủi ro **tài sản**: nếu đồng ý bị rút, thứ mất đi là **baseline đo lường** của mọi mốc sau.

**Cách dùng phiếu**: chấm `C-1`…`C-8` **trước** khi viết dòng Story Bible đầu tiên. `C-1`, `C-3`, `C-4` là **ba tiêu chí không thương lượng** — trượt bất kỳ cái nào thì đổi chapter, ⛔ đừng đổi ngưỡng.

---

## 6. Nhất quán tài liệu — 7 phát hiện

> Mọi phát hiện dưới đây đều kèm **bằng chứng kiểm được bằng lệnh**. ⛔ Không suy diễn.

### F-1 — ~90 giờ-người vs "1–2 tuần": con số không so sánh trực tiếp được

**Bằng chứng**: cộng cột `E_build` của `Backlog-Priority §3.1` = `8 + 4 + 6 + 20 + 24 + 8 + 14 + 6` = **~90 giờ-người**. `CF-8.4` chốt MVP0 = **1–2 tuần** (≈40–80h cho một người).

**Vấn đề thật ⛔ không phải "vượt trần"** mà là: `Backlog-Priority` ⛔ **không tách** `E_build` của *lát cắt MVP0* khỏi `E_build` của *toàn Story*. Rõ nhất ở `Story-Comic-IR` (~20h, nhưng AC mục 4 mô tả **schema MVP1 có DB**) và `Story-Fix-Narrative-Time-Key` (8h, gồm cả *"cập nhật mọi bảng liên quan trong schema `story`"* — việc của MVP1).

⇒ **Hiện không có nguồn nào trong repo cho biết lát cắt MVP0 tốn bao nhiêu giờ.** Chủ: **PM + Founder**.

### F-2 — `Backlog-Priority §3.1` có 8 Story, §4 rút gọn chỉ 6

**Bằng chứng**: §3.1 liệt kê 8 hàng; §4 *"Pre-cycle/MVP0 (6)"* thiếu `Story-Record-Readability-Human-Judgement` và `Story-Image-Provider-Adapter`.

⛔ **Đây KHÔNG phải lỗi** — đúng theo quy tắc `⭐` ở §2.3 (hai Story kia có `G = G0`). Nhưng tiêu đề *"MVP Stories — danh sách rút gọn"* ⛔ không nói điều đó, và người lập kế hoạch thực thi từ §4 sẽ **bỏ sót 2/8 Story**. ⇒ Đề xuất: thêm một dòng chú thích *"⛔ đây là danh sách `⭐`, KHÔNG phải toàn bộ Story của mốc"*.

### F-3 — Tầng Epic ghi `chưa có file` trong khi 41 file Story đã tồn tại

**Bằng chứng**: `grep -h "chưa có file" docs/022-User-Stories/Epics/*.md | wc -l` → **47** · `ls docs/022-User-Stories/Backlog/*.md | wc -l` → **41**. Cả 8 Story MVP0 đều tồn tại, `status: draft`.

⇒ Cột *Trạng thái* của tầng Epic đã **drift khỏi filesystem**. Ảnh hưởng trực tiếp tới MVP0: 6/8 Story MVP0 bị Epic cha báo là chưa có file. Chủ: **PO**.

### F-4 — Ba ngưỡng `[EM]` chưa có dấu vết ký nhận

`G1-c` (≤30%/30–50%/>50%), `G1-d` (≥60% panel 2 nhân vật), và trần `E_hitl ≤2h/chapter` đều mang nhãn *"ngưỡng do em định nghĩa, không có nguồn ngoài"*.

`MVP-Scope §7` ghi nguyên tắc: *"mọi ngưỡng được định nghĩa **TRƯỚC** khi đo. Không sửa ngưỡng sau khi nhìn thấy kết quả — đó là cách một gate biến thành nghi lễ."* ⇒ Nguyên tắc có, nhưng ⛔ **không tìm thấy artifact nào ghi nhận Founder đã ký nhận ba ngưỡng này**. Chủ: **Founder**.

### F-5 — AC của `Story-Comic-IR` mô tả schema MVP1, ⛔ không thực thi được ở MVP0

**Bằng chứng**: mục 4 của Story yêu cầu *"Panel Specification được lưu như dữ liệu chính (bản ghi trong DB/schema `comic`)"* và *"insert thiếu trường bị **DB từ chối**"*. Nhưng `MVP-Scope §3.1` chốt **MVP0 không có database**.

Story ⛔ không sai — nó đã tách DoD của lát MVP0 xuống mục 6 và ghi rõ *"bốn khối AC bên dưới mô tả phần vượt khỏi MVP0"*. Rủi ro là **thứ tự đọc**: AC nằm ở mục 4, cảnh báo nằm chìm trong callout, DoD thật nằm ở mục 6. ⇒ Đề xuất: nâng cảnh báo lên đầu mục 4 dạng `[!WARNING]`.

### F-6 — Năm Story `[MVP0]` dùng **chung một DoD**, ⛔ không Story nào "xong" được một mình

**Bằng chứng**: mục 6 của cả năm Story `n/a [MVP0]` đều liệt kê **cùng 5 tiêu chí `G1-a…G1-e`** làm Definition of Done, kèm chú thích ai *sở hữu* tiêu chí nào.

**Hệ quả vận hành**: tiến độ MVP0 ⛔ **không theo dõi được ở tầng Story** — một Story chỉ chuyển `done` khi cả gate `G1` có số. ⇒ Đơn vị theo dõi đúng của MVP0 là **gate `G1` + `P-1…P-6`**, ⛔ không phải bảng Story. Đây là hệ quả trực tiếp của kỷ luật *"MVP0 mua thông tin, không giao tính năng"* — ghi ra đây để ⛔ không ai cố ép Story MVP0 vào một sprint board thông thường.


### F-7 — Chữ *"spike"* có 3 cách dùng khác nhau; chỉ **7 chỗ** thật sự nằm trong vùng `CẤM-11` phải phán

`CẤM-11` ([Glossary](../999-Resources/Glossary.md) headword `MVP0`): *"Một tên duy nhất cho khái niệm này — không dùng **'phase 0'**, **'spike'**, **'PoC'**."*

**Bằng chứng** — grep toàn `docs/`, ⛔ **trừ `pm-runs/`** (là *"sổ tay điều phối của PM, không phải deliverable"*, `pm-runs/README.md`). ⛔ Không hit nào cho *"phase 0"* hay *"PoC"* ngoài chính các dòng ban lệnh cấm.

| Nhóm | Cách dùng | Số chỗ | Phán được ngay chưa |
|:-:|---|:-:|---|
| **C** | *"một **spike riêng**"* (canvas — `MVP-Scope §5.3` #6, `PRD` `D2`, `UC-08`), *"**nghiệm thu spike**"* (verify vendor Clerk — `ADR-003`, `SRS-NFR-08`) | ~13 | ✅ **Ngoài phạm vi.** Đây là **spike KHÁC**, ⛔ không phải MVP0 — `CẤM-11` cấm gọi *MVP0* là spike, ⛔ không cấm từ *"spike"* tồn tại trong repo |
| **B** | *"**code của spike** KHÔNG phải nền của sản phẩm"*, *"MVP0 **là spike bị vứt**"* (`MVP-Scope §3.1`, `Roadmap §3.1`, `SRS:153,291`, `PRD:336`, `BRD-007:77`, `Spec-Security-Legal-Compliance:346`) | 8 | ✅ **Hợp lệ — có bằng chứng nội tại**, xem ngay dưới |
| **A** | ⭐ *"**spike MVP0**"* / *"**Spike MVP0**"* / *"Sau **spike MVP0**"* — dùng như một **cụm định danh** | **7** | ⚠️ **Vùng mờ — cần phán** |

> [!NOTE]
> ⭐ **Vì sao nhóm B hợp lệ, ⛔ không cần ai phán**: `SRS-Comic-Studio.md` dòng `153` dùng cụm *"code của spike"* **ngay bên trong chính câu ban lệnh cấm** — nguyên văn: *"Đây là chủ ý: **'code của spike KHÔNG phải nền của sản phẩm'**. […] ⛔ Không dùng tên khác cho MVP0 — không 'phase 0', không 'spike', không 'PoC' (`CẤM-11`)."*
>
> ⇒ Chính tác giả `CẤM-11` đọc *"code của spike"* là **danh từ chung mô tả tính chất**, ⛔ không phải một tên gọi thay thế. ⇒ Nhóm B **đóng**, ⛔ không mở lại.

**Bảy chỗ thuộc nhóm A** (4 file): [`ADR-001`](../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `:67`, `:69`, `:127` · [`SRS`](../020-Requirements/SRS-Comic-Studio.md) `:258` · [`Spec-Security-Threat-Model`](../030-Specs/Security/Spec-Security-Threat-Model.md) `:293`, `:522` · [`Typography`](../040-Design/Design-System/Typography.md) `:259` *(trích lại từ `ADR-001`)*.

⛔ **Tài liệu này KHÔNG kết luận đây là vi phạm** — hai cách đọc đều đứng được, và chọn giữa chúng ⛔ không thuộc thẩm quyền của một tài liệu phân tích:

| Đọc chặt | Đọc lỏng |
|---|---|
| *"Một tên duy nhất"* ⇒ **`spike MVP0` là tên thứ hai** cho cùng khái niệm, đúng thứ `CẤM-11` sinh ra để chặn | Tên **MVP0 vẫn nguyên vẹn**; *"spike"* chỉ là danh từ mô tả đứng trước — cùng loại với nhóm B đã được chính tác giả chấp nhận |

**Chủ**: **PO** hoặc **context-auditor**.

⭐ **Điều quan trọng hơn cả kết luận**: dù phán theo hướng nào, kết quả phải được **ghi thành ngoại lệ tường minh tại headword `MVP0` của `Glossary`**. Nếu không, lần rà nhất quán tiếp theo sẽ **tốn lại đúng công này** và có thể ra kết luận ngược — đó mới là chi phí thật. Chi phí sửa nếu phán là vi phạm: **7 chỗ / 4 file**, thấp; `Typography:259` là **trích dẫn** nên sửa `ADR-001` trước, ⛔ đừng sửa rời.

---

## 7. Câu hỏi mở cần Founder đóng

| # | Câu hỏi | Vì sao chặn | Chủ |
|:-:|---|---|---|
| **Q-1** | **Chapter nào?** Truyện nào, bản quyền thuộc ai, bao nhiêu chữ | Ba điều kiện tiên quyết cứng đều phái sinh từ đây; ⛔ không Story nào sở hữu. ⇒ Chấm bằng **phiếu `C-1…C-8`** tại [§5.4](#54-phiếu-chọn-chapter--tiêu-chí-c-1c-8) | **Founder** |
| **Q-2** | Ký nhận ba ngưỡng `[EM]` (`G1-c`, `G1-d`, `E_hitl`) **trước** khi đo | `MVP-Scope §7`: ngưỡng chốt sau khi nhìn kết quả ⇒ gate thành nghi lễ | **Founder** |
| **Q-3** | Chốt **vendor** image + VLM cho MVP0 | Số đo trên provider A ⛔ không chuyển giao sang provider B ⇒ mất giá trị của cả `G1` | **Founder + Architect** |
| **Q-4** | `E_build` của **riêng lát cắt MVP0** là bao nhiêu | ~90h khai báo ⛔ không so được với trần 1–2 tuần (`F-1`) | **PM + Founder** |
| **Q-5** | VLM-select ở MVP0 có chịu cổng chất lượng `SRS-FR-21` không? | [ADR-007](../030-Specs/Architecture/ADR-007-VLM-Provider-For-QA-Select.md) `Q3` đặt **report-only** làm mặc định cho *"mọi check"*, và [SRS](../020-Requirements/SRS-Comic-Studio.md) dòng `SRS-FR-21` đòi **≥100 panel dán nhãn tay** trước khi bật. MVP0 chỉ có **8–30 panel**. ⚠️ **Chưa kết luận đây là mâu thuẫn** — cổng đó neo vào Continuity Checker, còn VLM-select là bước khác. Cần Architect phân định | **Architect** |

---

## 8. Tài liệu tham khảo

### 8.1 Nguồn trong repo

| Tài liệu | Mục được dùng |
|---|---|
| [MVP-Scope.md](../010-Planning/MVP-Scope.md) | §1.3 thứ tự mốc · §3.1 ba ô đáng chú ý · §6 `KC-1…KC-7` · §7.0 ba gate · **§7.2 gate `G1`** |
| [Roadmap.md](../010-Planning/Roadmap.md) | §2 bảng lộ trình + `P-1…P-6` · **§3.1 ba việc pre-cycle** · §6.1 `G0` không chặn MVP0 · §6.2 bảng phụ thuộc |
| [Backlog-Priority.md](../022-User-Stories/Backlog-Priority.md) | §2.3 quy tắc `⭐` · **§3.1 tám Story MVP0** · §4 danh sách rút gọn |
| [Glossary.md](../999-Resources/Glossary.md) | `MVP0` · `E_build` · `E_hitl` · `Rank` · `TBD có chủ` · `INVEST` |
| [Story-*.md](../022-User-Stories/Backlog/) × 8 | mục 4 AC · mục 5 ước lượng · mục 6 INVEST/DoD |
| [ADR-001](../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) · [ADR-007](../030-Specs/Architecture/ADR-007-VLM-Provider-For-QA-Select.md) · [ADR-013](../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) · [ADR-016](../030-Specs/Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) | status + ô `TBD` |
| [SRS-Comic-Studio.md](../020-Requirements/SRS-Comic-Studio.md) | `SRS-FR-21` cổng chất lượng check |
| [Typography.md](../040-Design/Design-System/Typography.md) | `TBD-FONT` có chủ, đóng sau MVP0 trước `G1-e` |
| [Analysis-Comic-Studio-Concept.md](./Analysis-Comic-Studio-Concept.md) | §4.2 typeset · §5.1 khoá thời gian · §10 trần ngân sách |

### 8.2 Nguồn ngoài — dẫn qua bảng Canonical Facts

⛔ Tài liệu này ⛔ **không** dẫn trực tiếp nguồn ngoài nào. Mọi nhãn `[OFF]` / `[EM]` / `[CHỐT]` được **copy nguyên** từ tài liệu nguồn trong repo (`CF-1.x`, `CF-3.x`, `CF-6.x`, `CF-7.x`, `CF-8.x`, `CF-9.x`) — xem bảng Canonical Facts tại `findings/` của các run tương ứng.

---

_Created by business-analyst_
_Author: trisjr_
