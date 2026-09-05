---
id: ADR-013
type: adr
status: draft
project: comic-studio
created: 2026-08-29
updated: 2026-08-30
---

# ADR-013: Typeset layer tách khỏi art — chữ không bao giờ nằm trong pixel

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

## Context

> [!IMPORTANT]
> ⛔ **ADR này là RECORD-ONLY.** Nó **đóng băng** năm quyết định đã CHỐT ở Phase 1 (`D-28`, `D-29`, `D-30`, `D-32`, `D-33`), ⛔ **không** quyết gì mới. Đặc biệt: phần tech stack cho wrap tiếng Việt **đã chốt ở [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md)** — ADR này **trỏ tới**, ⛔ **không chọn lại thư viện**.

Trang truyện thành phẩm có **hai tầng dữ liệu**, không phải một:

1. **Art** — ảnh do model sinh, ⛔ **không chứa chữ**.
2. **Typeset layer** — bubble, đuôi trỏ, thoại; là **dữ liệu**, render bằng **code**.

Thành phẩm chỉ tồn tại **sau khi composite**. [UC-09](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) nói thẳng: *"Export là bước **COMPOSITE**, không phải bước 'lấy ảnh gốc ra'… trước đó nó không phải một file, mà là **hai tầng dữ liệu**"*.

### Vì sao tách — ba lý do độc lập, mỗi lý do đủ để chốt

| # | Lý do | Hệ quả nếu KHÔNG tách |
|---|---|---|
| 1 | **Sửa một câu thoại không được phép tốn tiền sinh ảnh** | Mỗi lần sửa dấu phẩy = một lần gọi image API = mất tiền và mất luôn ảnh cũ |
| 2 | **Model render chữ tiếng Việt không đáng tin** | Dấu chồng (`ế`, `ữ`, `ượ`) hỏng âm thầm trong pixel — ⛔ không sửa được, chỉ sinh lại được |
| 3 | **Cùng dữ liệu phải render được thumbnail VÀ bản in 300 DPI** | Chữ nướng vào pixel bị khoá cứng vào một độ phân giải |

### ⚠️ `D-30` là ràng buộc THẬT, không phải chi tiết nhỏ

Wrap thoại tiếng Việt **phải dùng thư viện hiểu Unicode combining marks**. [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Context` xếp nó là ràng buộc bao trùm `R3` và ghi rõ lý do:

> *"bubble là sản phẩm cuối mà người đọc nhìn thấy; wrap sai dấu tiếng Việt là **hỏng sản phẩm**, không phải lỗi cosmetic."*

⇒ **Phần kỹ thuật đã đóng ở [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Decision` điều 8.** ADR-013 ghi lại **ràng buộc**, ⛔ **không** đề xuất, so sánh, hay đặt lại câu hỏi về thư viện. Bất kỳ run nào muốn đổi thư viện wrap phải sửa **ADR-001**, không phải file này.

---

## Decision

### Tầng CHỐT — ⛔ bất biến, không đổi mà không viết ADR mới

**1. Art sinh ra KHÔNG chứa chữ (`D-29`).**
Bốn token `text`, `letters`, `watermark`, `speech bubble` nằm trong **negative prompt** cho **100%** panel có thoại. ⛔ **Không nướng chữ vào pixel** trong bất kỳ trường hợp nào.

**2. Bubble là LAYER DỮ LIỆU riêng, toạ độ chuẩn hoá 0–1 (`D-29`).**
Cùng hệ toạ độ với `page_layout` và `text_safe_zone` ([ADR-012](./ADR-012-Comic-IR-Spec-As-Primary-Data.md) `## Decision` điều 5 và điều 9). Cùng dữ liệu render được **thumbnail** và **bản in 300 DPI** (`SRS-FR-11`).

**3. Bubble + thoại render bằng CODE, ⛔ không phải bằng model (`D-29`).**
Pipeline composite phải có **bước render text riêng, tách khỏi bước gọi model sinh ảnh** — đo được bằng cách kiểm cấu trúc pipeline, không phải bằng cách nhìn ảnh.

**4. Vi phạm được ĐO, không được bỏ qua (`D-29`).**
Nếu model vẫn sinh chữ trong ảnh dù đã có negative prompt, panel đó **không** được tính vào tử số **100%** của gate `G1-e`; phải **ghi nhận là vi phạm và loại khỏi bộ đã duyệt** ([Story-Typeset-Layer-And-Bubble-Overlay](../../022-User-Stories/Backlog/Story-Typeset-Layer-And-Bubble-Overlay.md) AC). ⛔ Không có nhánh *"chữ mờ nên cho qua"*.

**5. HAI field cho thoại, ⛔ không phải một (`D-28`).**

| Field | Tính chất | Ai ghi |
|---|---|---|
| `dialogue_source` | ⭐ **BẤT BIẾN**, kèm `source_span` trỏ về văn bản gốc | Hệ thống, lúc ingest |
| `dialogue_rendered` | Bản đã nén, **người sửa được** | LLM đề xuất → **người duyệt** |

⭐ **Edit của người phải KHOÁ LẠI khỏi bị re-run ghi đè.** Đây là phần dễ mất nhất của `D-28`: một lần chạy lại condensation pipeline mà không tôn trọng khoá sẽ **xoá âm thầm** công người dùng đã bỏ ra. `dialogue_source` bất biến là thứ giữ cho `field_provenance` và `change_log` có nghĩa — không có nó thì không chứng minh được bản nén *nén từ đâu*.

**6. Wrap tiếng Việt hiểu Unicode combining marks (`D-30`).**
⛔ **Không chọn lại thư viện ở đây** — xem [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Decision` điều 8. Ràng buộc được ghi lại:
- Wrap phải chạy ở **cùng runtime với compositor** — ⛔ không wrap ở frontend rồi gửi kết quả xuống.
- Wrap phải đo bằng **chính font sẽ render** — ⛔ không wrap bằng font khác.
- Chuẩn hoá **NFC** ngay tại biên ingest.

**7. Auto-placement bubble PHẢI TỰ BUILD, và luôn có đường kéo tay (`D-30`).**
MVP là **heuristic**: gần speaker, tránh vùng có mặt, đúng thứ tự đọc — **cộng** với cho user **kéo tay**. ⛔ Không mua, và ⛔ không coi heuristic là đủ một mình. Lý do không mua: đây **không** phải trục cạnh tranh của sản phẩm (`R-18`).

**8. ⭐ Compositor DÙNG CHUNG cho preview và export (`D-32`).**
⛔ **KHÔNG viết renderer/compositor thứ hai.** Preview là composite **render server-side, read-only**; export **tái dùng đúng compositor đó** ([UC-09](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) callout: *"⛔ KHÔNG viết renderer/compositor mới"*).

Hệ quả ràng buộc — ⚠️ **phải giữ đúng biên**: preview **read-only** và **KHÔNG mở đường xuất bản**. Trang chỉ xuất bản được khi **cả hai** human gate PASS. Preview **được phép chạy trước** khi hai gate PASS vì nó không đưa nội dung ra ngoài hệ thống ⇒ nó **không** là đường bypass của `M2-4` ([UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) bước 13 + callout). Ranh giới: `M2-4` chặn **xuất bản page**, ⛔ không chặn **xem trước**.

**9. ⭐ QUY TẮC RESET GATE KHI `text_budget` ĐỔI (`D-33`) — hai trigger, ⛔ không được bỏ cái nào.**

`text_budget` **phụ thuộc diện tích panel** (`BR-003-12`). Đó là lý do `SRS-FR-15` xếp **dialogue condensation nằm SAU layout**. Vì vậy:

| Trigger | Điều gì xảy ra | Phạm vi reset | Neo |
|---|---|---|---|
| **T1 — diện tích panel đổi** (đổi template, swap, reorder) | **Tính lại `text_budget`** cho các panel bị ảnh hưởng. Nếu dòng thoại nào thuộc panel đó **đã PASS** human gate #2 ⇒ **reset gate #2 về `OPEN`** | ⭐ **mọi dòng thuộc panel bị ảnh hưởng** | [UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) **bước 8** + **EX-2** |
| **T2 — nội dung thoại bị sửa** sau khi dòng đó đã PASS gate #2 | **Reset gate #2 của ĐÚNG DÒNG ĐÓ về `OPEN`** và yêu cầu xác nhận lại | ⭐ **đúng một dòng** — ⛔ không lan sang dòng khác | [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) **bước 10** + **EX-6** |

⛔ **Thiếu reset = tạo ra một đường bypass ⇒ `M2-4` FAIL.** Nguyên văn [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) **EX-6**:

> *"Đây là một **khiếm khuyết của pipeline xuất bản**, không phải một lựa chọn của người dùng… `M2-4` đo **'không tồn tại đường code nào xuất bản page mà chưa qua cả hai gate'**, chứ **không** đo sự tồn tại của màn hình gate."*

⚠️ Đọc kỹ hệ quả: **màn hình gate vẫn hiển thị đầy đủ mà `M2-4` vẫn FAIL**, nếu trạng thái PASS cũ được giữ lại trên một `text_budget` đã đổi. Bản nén được duyệt trên ràng buộc cũ thì **không còn được duyệt trên đúng ràng buộc** ([UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) **EX-2**).

⚠️ Trường hợp biên đã ký: sửa thoại **trước khi** gate #2 chạy lần đầu ⇒ **không có gì để reset**, nhưng bản do người viết **vẫn phải đi qua gate** — ⛔ không có nhánh tự động PASS ([UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) **AF-5**).

⚠️ Và: khi thoại vượt `text_budget`, một trong ba đường xử lý hợp lệ là **cấp cho panel diện tích lớn hơn** — đường đó **kích hoạt lại T1** ([UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) **EX-2** đường (c)). Reset không phải một sự kiện hiếm; nó là **một vòng lặp bình thường** của luồng biên tập.

### `TBD` — ⛔ lô này KHÔNG đóng

| Khoảng trống | Vì sao chưa đóng được | **Ai đóng** | Khi nào |
|---|---|---|---|
| **Danh mục kiểu bubble** (speech / thought / shout / whisper…) | [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) bước 6 chỉ ghi *"chọn kiểu bubble"*; ⛔ **danh mục cụ thể chưa được định nghĩa ở đâu trong repo** — `findings/architect.md` §7 **`G9`** | **PM hỏi Founder**; Architect ghi vào `DB-Entity-Typeset-Layer` + `Endpoint-Bubble-Typeset` sau khi có câu trả lời | Trước khi viết DDL của typeset layer |
| **SFX / narration box / caption** | [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) **AF-6** xếp chúng **NGOÀI** bốn thao tác được liệt kê ⇒ chưa có hình dạng dữ liệu | **PM hỏi Founder** | Cùng lúc trên |
| ⭐ **Font sẽ render** — phải thoả **cả BỐN** ràng buộc `R-1`…`R-4` [ngay dưới](#-bốn-ràng-buộc-mà-font-render-phải-thoả-khi-tbd-này-đóng) | Story ghi lỗi *"font không đủ glyph"* là một rủi ro phải phát hiện **bằng kiểm thủ công**, vì ⛔ **không có benchmark định lượng nào** cho trường hợp này | **Architect + Founder**, sau MVP0 | Trước gate `G1-e` |

### ⭐ Bốn ràng buộc mà font render phải thoả (khi `TBD` này đóng)

> [!IMPORTANT]
> ⛔ **Bảng này ⛔ KHÔNG chọn font.** Nó ghi **điều kiện nghiệm thu** mà bất kỳ font nào cũng phải vượt qua trước khi được ghi vào config của `apps/backend`.
> ⚠️ Trước bản `2026-08-30`, ADR này chỉ nêu **hai** hạng mục (họ font + glyph coverage) trong khi tầng 040 đã ghi **bốn** ⇒ `R-3` và `R-4` **chỉ tồn tại ở tầng 040**, nơi lô DB Schema và lô API ⛔ **không đọc tới**. Đưa đủ bốn về đây là để hợp đồng nằm ở **tầng mà người implement đọc**.

| # | Ràng buộc | Suy ra từ đâu |
|:--:|---|---|
| **R-1** | ⭐ **Đơn trị** — **một** họ font, resolve ra **một** file font xác định. ⛔ Không dấu phẩy, ⛔ không generic family, ⛔ không *"nếu thiếu thì dùng cái kia"* | Điều **6** ở trên (*wrap phải đo bằng **chính font sẽ render***) + [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Decision` điều **8**. Fallback stack ⇒ ⛔ không biết trước font nào thực sự đo ⇒ wrap ⛔ không tái lập được ⇒ phá điều **8** ở trên (*preview **là** export*) |
| **R-2** | ⭐ **Phủ đủ dấu tiếng Việt**, gồm **dấu chồng hai tầng** (`ế`, `ữ`, `ợ`) — phủ bằng **glyph dựng sẵn hoặc mark positioning đúng**, ⛔ không phải vẽ chồng tuỳ ý | §*Vì sao tách* lý do **#2** + nghiệm thu MVP0 của [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Consequences` **#5** (corpus có dấu chồng, cả NFC và NFD) |
| **R-3** | 🆕 **License cho phép NHÚNG và dùng SERVER-SIDE** trong image được phân phối | Hệ quả bắt buộc của [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Decision` điều **8** (font phải nằm **cùng runtime** với compositor — nhắc lại ở điều **6** của ADR này) + [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Decision` điều **2** (*một image, hai command* — file font đi theo image, build một lần, push lên registry) ⇒ đây là **nhúng server-side**, ⛔ **không phải webfont**. ⚠️ Có license font cho phép dùng trên web nhưng **hạn chế** nhúng vào sản phẩm phân phối ⇒ ⛔ không suy ra *"miễn phí ⇒ dùng được"* |
| **R-4** | 🆕 ⭐ **Metric ổn định giữa các version**, và version font **PHẢI ĐƯỢC PIN**. Đổi version xử lý **như đổi font** | Font là **tham số đầu vào của thuật toán wrap** ([ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Consequences` **#5**: *wrap đúng = segmentation **+** đo bằng chính font sẽ render*). Một bản cập nhật đổi advance width hay vertical metric làm **mọi phép đo cũ hết hiệu lực IM LẶNG** — mọi bubble đã duyệt phải đo lại |

⚠️ **`R-4` là ràng buộc mà ⛔ KHÔNG đường reset gate nào chạm tới được.**

⛔ **Đừng đọc thành *"ba ràng buộc kia đều lộ ra lúc build"*** — ⛔ không đúng, và mỗi cái hỏng ở một thời điểm khác nhau:

| | Hỏng khi nào | Ai/cái gì bắt được |
|---|---|---|
| `R-1` | Lúc composite | ⚠️ **Chỉ khi đã tuân thủ `R-1`.** Nếu bị vi phạm (có fallback stack) thì đúng là ⛔ **không báo lỗi** — nó âm thầm rơi xuống font kế tiếp và đo sai. Đó chính là lý do `R-1` tồn tại |
| `R-2` | Lúc render panel đầu tiên có dấu chồng | ⚠️ **Kiểm THỦ CÔNG từng panel** — hàng `TBD` ở trên ghi rõ ⛔ **không có benchmark định lượng nào** |
| `R-3` | Lúc review pháp lý, hoặc lúc nhận thư khiếu nại | ⛔ **`docker build` không thẩm định license.** Đây là ràng buộc lộ ra **muộn nhất** trong bốn |
| ⭐ `R-4` | Lúc một lần `docker build` kéo về patch version mới | ⛔ **Không gì cả** — ⛔ không lỗi, ⛔ không test đỏ, chỉ có bubble ngắt dòng **khác đi so với lần người dùng đã duyệt** |

⭐ **`R-4` khác ba cái kia ở chỗ: nó là ca DUY NHẤT mà trạng thái human gate #2 đã `PASS` trở nên sai mà ⛔ không trigger nào của điều 9 chạy.** `T1` kích hoạt khi **diện tích panel** đổi; ở đây diện tích ⛔ **không đổi một pixel** — thứ đổi là **phép đo**. ⇒ Bản nén vẫn mang `PASS` trên một phép đo **đã khác** — đúng hình dạng mà điều **9** gọi là *"khẳng định một điều nó không còn biết là đúng"*.

⇒ **Hai việc bắt buộc, ⛔ không phải khuyến nghị** — lấy nguyên khuôn của [ADR-016](./ADR-016-Image-Provider-Adapter-And-Version-Pinning.md), nơi **cùng hình dạng vấn đề này đã được giải cho image provider**:

1. **Pin version font tường minh** — hạng mục của **Dockerfile**. ⛔ Không alias, ⛔ không "bản mới nhất". Đối chiếu [ADR-016](./ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) §Alternatives **(d)** (*⛔ LOẠI alias `latest`*).
2. ⭐ **Ghi `font_version` vào provenance** để **truy vết được** khi nghi ngờ drift. [ADR-016](./ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) `## Decision` chốt đúng cơ chế này cho `model_version`, với lý do nguyên văn: *"để **phát hiện được silent model drift**"* — provider đổi weights dưới cùng một tên model thì hệ thống ⛔ không tự phát hiện được, *"nhưng adapter phải ghi `model_version` để về sau **có thể truy vết**"*. **Font drift là cùng một bài toán**, và `R-4` ⛔ không được chỉ lấy nửa đầu.

⚠️ Nếu buộc phải đổi version font: xử lý **như đổi font** — đo lại toàn bộ, ⛔ không giữ trạng thái gate cũ.

> ⚠️ **Nguồn đối chiếu ở tầng 040**: [Typography](../../040-Design/Design-System/Typography.md) §*Bốn ràng buộc mà font render phải thoả* phát biểu **cùng bốn ràng buộc này**. ⛔ **Không phải hai nguồn sự thật** — **ADR-013 sở hữu `TBD`**, tầng 040 **trỏ về đây**. Lệch nhau ⇒ sửa **cả hai trong cùng một run**, ⛔ không sửa một bên.

### ⭐ Thứ tự đóng hai `TBD` — `TBD-FONT` TRƯỚC, `T-PL-BUDGET-UNIT` SAU

> [!WARNING]
> **Cỡ chữ trong bubble phụ thuộc CẢ HAI `TBD`**, và trước bản `2026-08-30` ⛔ **không tài liệu nào nói ra thứ tự giữa chúng**. Mục này nói ra.

| `TBD` | Nội dung | Chủ | Hạn |
|---|---|---|---|
| **`TBD-FONT`** — ADR này sở hữu | Họ font · glyph coverage · leading của bubble | **Architect + Founder** | Sau MVP0, **trước `G1-e`** (cuối 09/2026) |
| **`T-PL-BUDGET-UNIT`** — [Endpoint-Page-Layout](../API/Endpoint-Page-Layout.md) sở hữu | **Đơn vị** của `text_budget` (ký tự hay từ) **+ hàm tính từ diện tích panel** | **BA + Architect** | Trước gate **`M2-3`** (01–02/2027) |

**Phụ thuộc — tách làm hai nửa, ⛔ không gộp:**

1. **Phần *đơn vị*** (ký tự hay từ) **gần như độc lập với font** — chốt được trước, bất kỳ lúc nào.
   ⚠️ ⛔ **Không phải độc lập tuyệt đối**: với font **tỷ lệ** (proportional), *"ký tự"* là proxy tồi cho diện tích (`i` và `W` rộng khác nhau); với font **đều** (monospace) thì tuyến tính. ⇒ **Loại** font vẫn ảnh hưởng gián tiếp lên việc chọn đơn vị. ⛔ Không đủ để lật thứ tự bên dưới, nhưng ⛔ đừng đọc thành *"đơn vị chốt xong là xong"*.
2. ⭐ **Phần *hàm tính từ diện tích* PHỤ THUỘC metric của font.** Câu hỏi *"bao nhiêu ký tự vừa trong diện tích này"* ⛔ không trả lời được nếu chưa biết **một ký tự chiếm bao nhiêu** — mà đó chính là advance width và vertical metric của **font sẽ render** (`R-4` ở trên). ⇒ **Hàm tính phải đóng SAU `TBD-FONT`.**

✅ **Lịch hiện tại đã đúng chiều phụ thuộc** — `G1-e` (cuối 09/2026) đứng trước `M2-3` (01–02/2027). ⚠️ Ghi ra đây vì nó **đúng do trùng hợp về lịch, ⛔ không do ai ràng buộc**; ⛔ không có gì ngăn một run sau chốt hàm tính sớm cho tiện.

⛔ **Hệ quả nếu đóng ngược thứ tự:**
hàm tính `text_budget` calibrate trên một font giả định ⇒ khi `TBD-FONT` đóng thật, hàm **phải calibrate lại** ⇒ **`text_budget` của mọi panel đổi giá trị**.

⚠️ **Thiệt hại thật phụ thuộc lúc đó đã có dòng nào PASS gate #2 chưa** — ⛔ đừng đọc thành một mức duy nhất:

| Kịch bản | Thiệt hại |
|---|---|
| ⭐ **Nhiều khả năng hơn** — đóng sớm trong 10–12/2026, khi hai human gate **chưa được cưỡng chế** (`M2-4` thuộc MVP2, 01–02/2027) | ⛔ Chưa có dòng nào để reset. Thiệt hại là **calibration sai bị nướng vào spec và code**, rồi mọi thứ dựng lên trên nó |
| Đóng sau khi gate #2 đã chạy thật | Theo đúng lập luận của điều **9** (`T1` + [UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) **EX-2**), bản nén đã duyệt **không còn được duyệt trên đúng ràng buộc** ⇒ mọi dòng đã `PASS` gate #2 phải **reset về `OPEN`** |
⚠️ **Sắc thái phải đọc kỹ**: `T1` được phát biểu cho **diện tích panel đổi**. Ở đây diện tích ⛔ **không đổi** — thứ đổi là **hàm**. ⇒ Đây là **cùng lập luận, ⛔ không phải cùng trigger**; ⛔ **không có đường code nào tự động bắt được ca này**, đúng như `R-4`.

⇒ **Quy tắc rút ra**: đóng `TBD-FONT` trước. Nếu vì lý do nào đó phải chốt hàm tính trước, thì hàm đó mang nhãn **tạm**, ⛔ không được để `text_budget` sinh ra từ nó đi qua human gate #2.

---

## Alternatives considered

> ⛔ Ghi lại **vì sao các phương án kia bị LOẠI**, để không phải tranh luận lại.

### (a) Để model render chữ thẳng vào ảnh — ⛔ LOẠI

**Vì sao có vẻ hợp lý**: một bước thay vì hai; không cần compositor; frontier model đã render được chữ tiếng Anh khá tốt.

**Vì sao bị loại**:
1. **Sửa một câu thoại = sinh lại cả ảnh.** Trực tiếp phá nguyên tắc *"spec là dữ liệu chính"* ([ADR-012](./ADR-012-Comic-IR-Spec-As-Primary-Data.md)) và phá luôn luận điểm giá trị của editor.
2. **Tiếng Việt có dấu chồng.** `ế`, `ữ`, `ượ` hỏng trong pixel là **không sửa được** — chỉ sinh lại được, và lần sinh lại cũng không đảm bảo đúng.
3. **Gate `G1-e` đo điều ngược lại.** Tiêu chí nghiệm thu là **100%** panel có thoại dùng overlay và **0** panel nhờ model render chữ. Phương án này cho kết quả `0%`/`100%` — FAIL theo định nghĩa.
4. **Khoá cứng vào một độ phân giải.** Không còn cùng dữ liệu cho thumbnail và bản in 300 DPI.
5. **Không kiểm chứng được.** Không có cách nào assert *"chữ này đúng"* trên một mảng pixel; overlay thì so string được.

### (b) Một field thoại duy nhất (ghi đè bản gốc bằng bản nén) — ⛔ LOẠI

**Vì sao có vẻ hợp lý**: đơn giản hơn, một nguồn sự thật, không phải đồng bộ hai field.

**Vì sao bị loại**:
1. **Mất `source_span` ⇒ mất provenance.** Không chứng minh được bản nén nén **từ đâu** trong văn bản gốc; `field_provenance` mất neo.
2. **Nén là hàm MẤT MÁT.** Ghi đè bản gốc là **không đảo ngược được** — nén lại lần hai sẽ nén trên đầu vào đã nén, sai tích luỹ.
3. **Không có chỗ khoá công người dùng.** Nếu chỉ có một field, một lần re-run pipeline ghi đè thẳng lên bản người đã sửa. `D-28` đòi **edit của người phải khoá lại**; điều đó cần một field **không** thuộc quyền ghi của pipeline.

### (c) Mua / tích hợp engine typesetting comic có sẵn — ⛔ LOẠI

**Vì sao có vẻ hợp lý**: auto-placement bubble là bài toán đã có người giải; tự build tốn thời gian của một team **1 dev + AI assist**.

**Vì sao bị loại**: `D-30` chốt **tự build**. Lý do gốc là định vị: sản phẩm **không cạnh tranh ở trục typesetting** (`R-18`) ⇒ chỉ cần *"đủ tốt + kéo tay được"*, ⛔ không cần *"tốt nhất"*. Mua một engine cho một trục không cạnh tranh nghĩa là nhận một dependency nặng, một mô hình dữ liệu ngoại lai, và một ràng buộc runtime — trong khi yêu cầu thật chỉ là heuristic + drag.

⚠️ Loại **việc mua**, ⛔ **không** loại việc dùng thư viện cho **phần wrap Unicode** — phần đó [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) đã chốt và **phải** dùng thư viện, ⛔ không tự viết.

### (d) Auto-placement thuần tuý, ⛔ không cho kéo tay — ⛔ LOẠI

**Vì sao có vẻ hợp lý**: ít UI hơn, ít state hơn; nếu heuristic tốt thì không ai cần kéo.

**Vì sao bị loại**: heuristic **sẽ** sai ở panel bố cục lạ, và khi nó sai thì **không có lối thoát nào khác**. Đây là cùng một khuôn với `SRS-FR-10` (*"đổi layout template bằng một click — lối thoát khi rubric chấm sai"*): mọi bước tự động trong hệ thống này đều phải có một đường người can thiệp. `D-30` viết *"heuristic **+** cho user kéo tay"* — dấu cộng là bắt buộc.

### (e) Renderer riêng cho preview, renderer riêng cho export — ⛔ LOẠI

**Vì sao có vẻ hợp lý**: preview cần nhanh và nhẹ (PNG màn hình), export cần đúng và nặng (PDF/CBZ 300 DPI). Tối ưu riêng cho từng ca trông hợp lý.

**Vì sao bị loại**:
1. **Hai renderer = hai định nghĩa của "trang thành phẩm".** Người dùng duyệt trên preview rồi nhận một file khác — đó là lỗi **không phát hiện được** cho tới khi khách hàng phàn nàn.
2. **Chi phí gấp đôi cho mọi thay đổi typeset về sau.** Với `1 dev + AI assist`, đây là chi phí thường trực, không phải chi phí một lần.
3. **`M2-5` đòi ngược lại.** Export ở MVP2 gated on *"preview server-side đã chạy được — vì compositor của export **LÀ** compositor của preview"* ([UC-09](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) điều kiện tiên quyết (3)).
4. Nguyên văn `CF-9.1`: *"không viết renderer từ đầu"*.

### (f) Preview render client-side — ⛔ LOẠI

**Vì sao có vẻ hợp lý**: rẻ hơn (không tốn CPU server), phản hồi tức thì khi kéo bubble.

**Vì sao bị loại**: preview client-side **không thể** là compositor của export (export chạy server-side) ⇒ rơi thẳng vào phương án (e). Ngoài ra `D-30` đòi wrap chạy **cùng runtime với compositor** và đo bằng **chính font sẽ render**; wrap ở browser rồi gửi kết quả xuống là đường đã bị [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Decision` điều 8 cấm tường minh.

⚠️ Điều này **không** cấm việc hiển thị bubble trong editor ở client — đó là **lớp tương tác** trong phạm vi **một panel** (thành phần #2 của editor tối thiểu), khác với **preview trang/chapter** (thành phần #4). Hai thứ khác nhau, ⛔ không gộp.

### (g) Giữ trạng thái gate #2 khi diện tích panel đổi (⛔ không reset) — ⛔ LOẠI

**Vì sao có vẻ hợp lý**: reset gây phiền — user vừa duyệt xong 40 dòng thoại, đổi một template là phải duyệt lại. Nghe như một tối ưu UX rõ ràng.

**Vì sao bị loại**: ⛔ **Đây không phải một đánh đổi UX. Đây là một đường bypass.** `text_budget` đổi ⇒ bản nén đã duyệt **không còn được duyệt trên đúng ràng buộc**. Giữ trạng thái PASS cũ nghĩa là hệ thống **khẳng định một điều nó không còn biết là đúng**. `M2-4` được đo bằng **sự VẮNG MẶT của đường code bypass**, nên phương án này làm `M2-4` **FAIL** trong khi mọi màn hình gate vẫn trông hoàn hảo — đúng kiểu hỏng nguy hiểm nhất.

Ràng buộc cứng `layout → dialogue condensation` (`BR-003-12`) **không phải một tối ưu hoá**, và reset là hình dạng bắt buộc của nó.

---

## Consequences

### ⭐ Hợp đồng mà lô DB Schema và lô API kế thừa

| # | Ràng buộc bắt buộc | Neo |
|---|---|---|
| 1 | `dialogue_source` là cột **bất biến** (⛔ không có đường `UPDATE` từ pipeline), kèm `source_span` | `D-28` |
| 2 | `dialogue_rendered` có **cờ khoá** đánh dấu *"người đã sửa"*; pipeline re-run ⛔ **không được ghi đè** khi cờ bật | `D-28` |
| 3 | Typeset layer là **bảng/JSONB riêng**, toạ độ **0–1**, ⛔ không nằm trong bảng ảnh | `D-29` |
| 4 | Trạng thái human gate #2 lưu **ở mức DÒNG THOẠI**, ⛔ không phải mức panel hay mức page — vì `T2` reset đúng một dòng | `D-33` |
| 5 | Có đường ghi *"reset gate #2 về `OPEN`"* được **kích hoạt bởi thay đổi layout**, không chỉ bởi thay đổi thoại | `D-33` · [UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) bước 8 |
| 6 | ⛔ **Không tồn tại** endpoint / cột / cờ nào cho phép xuất bản page khi một trong hai gate chưa PASS | `M2-4` |
| 7 | Endpoint preview và đường export **gọi cùng một compositor**; ⛔ không hai code path | `D-32` |
| 8 | Mọi thao tác typeset của người dùng (kéo bubble, sửa thoại, đổi kiểu) sinh **một `change_log` row** | `SRS-FR-35` (ghi ở lô ADR-017) |

### Tích cực

1. **Sửa thoại là thao tác MIỄN PHÍ.** [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) ghi rõ: *"⛔ không có secondary actor nào là image provider trong UC này — mọi thao tác ở đây **không gọi image generation**"*. Đây là khác biệt lớn nhất so với công cụ AI image thông thường.
2. **Chữ tiếng Việt sửa được, so được, test được** — vì nó là string, không phải pixel.
3. **Một compositor ⇒ preview đúng bằng export.** Cái người dùng duyệt **là** cái họ nhận.
4. **Độc lập DPI.** Thumbnail và bản in 300 DPI từ cùng một dữ liệu.
5. **Reset gate làm `M2-4` trở thành sự thật kiểm chứng được**, không phải một màn hình.

### Tiêu cực — cái gì trở nên KHÓ HƠN

1. ⚠️ **Thành phẩm KHÔNG tồn tại sẵn ở đâu.** Trước khi composite, nó là hai tầng dữ liệu. Mọi thứ cần *"file trang truyện"* — chia sẻ, thumbnail, kiểm duyệt, takedown — đều phải đi qua compositor. Đây là một **đường nóng**, và nó là **đường duy nhất**.
2. ⚠️ **Reset gate gây phiền có chủ đích.** Đổi layout sau khi đã duyệt thoại ⇒ duyệt lại. Phiền này là **giá của `M2-4`**, ⛔ không phải một bug cần tối ưu. Lối giảm đau hợp lệ: sắp thứ tự công việc đúng (`SRS-FR-15`: condensation **sau** layout) — ⛔ không phải bỏ reset.
3. **Auto-placement tự build sẽ sai ở panel bố cục lạ.** Đường kéo tay là bắt buộc, và nó tốn UI.
4. **Wrap đúng = segmentation **+** đo bằng font thật.** [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Consequences` cảnh báo tường minh: thư viện cho ranh giới grapheme/word đúng chuẩn nhưng **không** biết chữ rộng bao nhiêu pixel. ⇒ compositor phải sở hữu cả hai nửa.
5. **Lỗi font thiếu glyph ⛔ không có benchmark định lượng** — chỉ phát hiện được bằng kiểm thủ công từng panel.

### Điều KHÔNG được suy ra từ ADR này

- ⛔ Không suy ra rằng ADR này chọn thư viện wrap — [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) chọn.
- ⛔ Không suy ra rằng preview là một dạng xuất bản (preview **read-only**, ⛔ không mở đường xuất bản).
- ⛔ Không suy ra rằng preview bị chặn bởi hai gate (preview **được phép** chạy trước; `M2-4` chặn **xuất bản**).
- ⛔ Không suy ra rằng reset gate là tuỳ chọn cấu hình được.
- ⛔ Không suy ra danh mục kiểu bubble — đó là `TBD` có chủ.

---

## Đã quyết ở đâu

> ⛔ Mọi hàng dưới đây **đã CHỐT ở Phase 1**. Neo bằng **mã requirement**, ⛔ không neo bằng số dòng.

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|:--:|---|
| **HAI field cho thoại**: `dialogue_source` (nguyên văn + `source_span`, ⭐ **BẤT BIẾN**) và `dialogue_rendered` (bản nén, người sửa được, ⭐ **edit của người phải KHOÁ LẠI** khỏi bị re-run ghi đè) | `D-28` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-12`** (§3.D) · `Analysis §5.4` |
| **Chữ đi qua typeset layer riêng**: art sinh ⛔ **KHÔNG có chữ** (`text, letters, watermark, speech bubble` vào **negative prompt**); bubble là **layer dữ liệu riêng** toạ độ **0–1**; ⛔ **không nướng chữ vào pixel**; cùng dữ liệu render thumbnail **và** bản in 300 DPI | `D-29` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-11`** (§3.A) · `MVP-Scope §3 A2` (`CF-8.11c`) · `Charter §4 R2` · `Analysis §5.4` · [UC-06](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) bước 3 · [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) bước 7 · `Glossary` mục *typeset layer* |
| Tiêu chí nghiệm thu của `D-29`: **100%** panel có thoại dùng overlay · **0** panel nhờ model render chữ · negative prompt cho **100%** panel có thoại · panel vi phạm **loại khỏi tử số** `G1-e` | `D-29` | [Story-Typeset-Layer-And-Bubble-Overlay](../../022-User-Stories/Backlog/Story-Typeset-Layer-And-Bubble-Overlay.md) AC-1…AC-4 · exit criterion **`G1-e`**, **`X-c`**, `P-2` |
| **Auto-placement bubble phải TỰ BUILD** (⛔ không mua): MVP là heuristic (gần speaker, tránh vùng có mặt, thứ tự đọc) **+** cho user **kéo tay** | `D-30` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-16`** (§3.D) · `Analysis §5.4` · `R-18` (⛔ không cạnh tranh ở typesetting) |
| ⭐ **Wrap tiếng Việt phải dùng thư viện hiểu Unicode combining marks** — ⛔ **tech stack đã chốt ở nơi khác, ADR này KHÔNG chọn lại** | `D-30` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-16`** · ⭐ **[ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md)** `## Context` ràng buộc **`R3`** + `## Decision` **điều 8** + `## Consequences` (segmentation ≠ đo) |
| Rủi ro *"font không đủ glyph"* với dấu chồng (`ế`, `ữ`, `ượ`) ⇒ phát hiện bằng **kiểm thủ công**, vì ⛔ **không có benchmark định lượng nào** | `D-30` | [Story-Typeset-Layer-And-Bubble-Overlay](../../022-User-Stories/Backlog/Story-Typeset-Layer-And-Bubble-Overlay.md) §Edge case · `findings/business-analyst.md` `KT-9` |
| ⭐ **Preview server-side TÁI DÙNG compositor của export** — ⛔ **không phải renderer thứ hai**; preview **read-only** và ⛔ **KHÔNG mở đường xuất bản** | `D-32` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.D *"Phạm vi editor tối thiểu"* **thành phần #4** (⚠️ **không mang mã `SRS-FR` riêng**) · `MVP-Scope §5.2` · `BR-004-03` · [UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) **bước 11**, **bước 13**, **AF-3**, **AF-4** · [UC-09](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) callout (*"⛔ KHÔNG viết renderer/compositor mới"*) + điều kiện tiên quyết (3) · `CF-9.1` |
| ⭐ **`T1` — diện tích panel đổi ⇒ tính lại `text_budget` ⇒ reset gate #2 về `OPEN`** cho mọi dòng thuộc panel bị ảnh hưởng | `D-33` | [UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) **bước 8** + **EX-2** · `BR-003-12` · [UC-05](../../020-Requirements/Use-Cases/UC-05-Human-Gate-Dialogue-Condensation.md) **EX-4** — ⚠️ **không có hàng `SRS-FR` nào phát biểu riêng quy tắc reset**; UC step là neo |
| ⭐ **`T2` — sửa nội dung thoại ⇒ reset gate #2 của ĐÚNG DÒNG ĐÓ** về `OPEN` | `D-33` | [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) **bước 10** + **EX-6** + trạng thái kết thúc thành công · `BR-003-13` · `M2-4` |
| ⛔ **Thiếu reset = đường bypass ⇒ `M2-4` FAIL**, kể cả khi màn hình gate vẫn tồn tại | `D-33` | [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) **EX-6** (nguyên văn) · [UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) **EX-2** · `BR-003-13` |
| Ràng buộc thứ tự làm `D-33` là hệ quả bắt buộc: **dialogue condensation nằm SAU layout** vì `text_budget` phụ thuộc diện tích panel | ngữ cảnh của `D-33` (`D-27` — ⛔ **không thuộc lô này**) | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-15`** (§3.C) — ⚠️ nhắc để đọc `D-33` không mất ngữ cảnh, ⛔ **không** phải hàng ADR-013 đóng băng |

### Khoảng trống — ⛔ ADR này KHÔNG đóng

| Khoảng trống | Nguồn ghi nhận | **Ai đóng** |
|---|---|---|
| **Danh mục kiểu bubble** cụ thể | [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) bước 6 · `findings/architect.md` §7 **`G9`** | **PM hỏi Founder** → Architect ghi vào lô DB Schema / API |
| **SFX / narration box / caption** — hình dạng dữ liệu | [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) **AF-6** · `findings/architect.md` §7 **`G9`** | **PM hỏi Founder** |
| ⭐ **Font render** — `TBD-FONT`, phải thoả **cả bốn** `R-1`…`R-4` (§*[Bốn ràng buộc](#-bốn-ràng-buộc-mà-font-render-phải-thoả-khi-tbd-này-đóng)*) | [Story-Typeset-Layer-And-Bubble-Overlay](../../022-User-Stories/Backlog/Story-Typeset-Layer-And-Bubble-Overlay.md) §Edge case · [Typography](../../040-Design/Design-System/Typography.md) §*Hệ 2* | **Architect + Founder**, sau đo MVP0 — ⭐ **đóng TRƯỚC `T-PL-BUDGET-UNIT`**, xem §*[Thứ tự đóng](#-thứ-tự-đóng-hai-tbd--tbd-font-trước-t-pl-budget-unit-sau)* |

---

_Ghi lại bởi System Architect — lô L6 (record-only), Phase 2._
_Author: trisjr_
