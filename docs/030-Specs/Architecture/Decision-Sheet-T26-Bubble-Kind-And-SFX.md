---
id: DS-T26
type: decision-sheet
status: open
project: comic-studio
created: 2026-09-04
updated: 2026-09-04
---

# Phiếu quyết định `T-26` — Danh mục kiểu bubble & hình dạng dữ liệu của SFX / Caption

Closes: [`T-26`](./SDD-Comic-Studio.md) · Unblocks: DDL của [`DB-Entity-Typeset-Layer`](../Schema/DB-Entity-Typeset-Layer.md)

> [!CAUTION]
> ⭐ **Phiếu này ⛔ KHÔNG tự chốt gì cả.** Nó bày **option kèm hệ quả DDL** để Founder ký.
> [`ARC-13`](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/findings/architect.md) cấm tuyệt đối việc Agent **phát minh** danh mục kiểu bubble hay hình dạng SFX / narration box / caption. ⇒ Mọi option dưới đây đều **truy được về một nguồn**, và nguồn được ghi ngay cạnh option.

> [!IMPORTANT]
> ⭐ **Vì sao phiếu này gấp**: `T-26` là **hàng duy nhất** đang **chặn DDL** của typeset layer. `DB-Entity-Typeset-Layer` ⛔ không viết được chừng nào chưa biết `comic.bubble` có cột `kind` không và `dialogue_line_id` có nullable không.

## Mục lục

1. [Bằng chứng cơ học — dữ liệu MVP0 đã trả lời một phần](#1-bằng-chứng-cơ-học--dữ-liệu-mvp0-đã-trả-lời-một-phần)
2. [`Q1` — Danh mục kiểu bubble](#q1--danh-mục-kiểu-bubble)
3. [`Q2` — Caption / narration box: có trong horizon MVP0–MVP2 không](#q2--caption--narration-box-có-trong-horizon-mvp0mvp2-không)
4. [`Q3` — SFX: cùng đường với caption hay tách riêng](#q3--sfx-cùng-đường-với-caption-hay-tách-riêng)
5. [Hệ quả dây chuyền sau khi ký](#5-hệ-quả-dây-chuyền-sau-khi-ký)
6. [Ô ký](#6-ô-ký)
7. [Tài liệu tham khảo](#7-tài-liệu-tham-khảo)

---

## 1. Bằng chứng cơ học — dữ liệu MVP0 đã trả lời một phần

⭐ **`T-26` ⛔ không còn là câu hỏi lý thuyết.** Kiểm kê cơ học `mvp0/panel-script-ch1.yaml` + `panel-script-ch2.yaml` (`2026-09-04`) cho thấy **10 dòng thoại** đã dùng khoá `bubble_type` với **ba** giá trị:

| Giá trị đã dùng | Số dòng | Nó thật sự là gì |
|---|:--:|---|
| `speech` | **4** | Bong bóng thoại thường, có đuôi trỏ về người nói |
| `voice_no_speaker` | **3** | ⭐ Giọng Tà Thần — nhân vật ⛔ **không có thân thể**, giọng vang trong linh hồn. Nguyên văn `typeset_note`: *"Bubble này ⛔ không có đuôi trỏ về người nói"* |
| `system_panel` | **3** | ⭐ Bảng trạng thái `[Tà Thần Chi Nhãn đã thức tỉnh.]`. Nguyên văn `typeset_note`: *"Bảng trạng thái là **GIAO DIỆN**, ⛔ không phải lời thoại"* |

> [!WARNING]
> ⚠️ **6 trong 10 dòng ⛔ KHÔNG phải speech bubble thường** — và cả 6 đang được biểu diễn bằng một **speaker giả**:
> `voice_no_speaker` gán `speaker: "ta_than"` (một thực thể ⛔ không có thân thể), `system_panel` gán `speaker: "system"` (⛔ không phải nhân vật nào cả, ⛔ không có trong Story Bible).
>
> ⇒ Với DDL hiện tại (`comic.bubble.dialogue_line_id` **`NOT NULL`**), ba dòng `system_panel` chỉ tồn tại được nếu ta tạo một `dialogue_line` mang speaker `"system"`. Hệ quả **⛔ không phải giả định**: dòng đó sẽ chảy vào **human gate 1 — speaker attribution**, và người dùng bị bắt *"xác nhận ai đang nói"* cho một ô chữ ⛔ **không có người nói**.

⇒ Đây là dữ kiện mà `UC-07` `AF-6` ⛔ chưa có khi nó viết *"⛔ không thiết kế thêm ở tầng UC này"*. Phiếu này đưa dữ kiện đó ra để Founder quyết.

---

## `Q1` — Danh mục kiểu bubble

**Câu hỏi**: `comic.bubble` có cột phân loại kiểu không, và danh mục gồm những giá trị nào?

| | Option | Nguồn | Hệ quả DDL |
|:--:|---|---|---|
| ⭐ **A1** | **3 giá trị đã dùng thật**: `speech` · `voice_no_speaker` · `system_panel` | ⭐ **Kiểm cơ học** dữ liệu MVP0 (§1) — ⛔ không phát minh giá trị nào | `kind TEXT NOT NULL` + `CHECK (kind IN (…))`. Thêm giá trị về sau = **migration thuần cộng thêm**, ⛔ không đụng row đã có |
| **A2** | **4 kiểu quy ước ngành**: `speech` · `thought` · `shout` · `whisper` | Enum **lịch sử** ở [findings/architect §8](../../010-Planning/pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio/findings/architect.md) — ⚠️ dẫn như **dấu vết**, ⛔ **không** phải đề xuất của Comic Studio | Như trên. ⚠️ **Vấn đề**: **6/10** dòng thoại thật ⛔ **không khớp** giá trị nào trong danh mục này |
| **A3** | **Hợp nhất A1 + A2** — 6 giá trị | Cả hai nguồn trên | Như trên. ⚠️ 3 giá trị (`thought`/`shout`/`whisper`) ⛔ **chưa có một dòng dữ liệu nào** dùng tới |
| **A4** | ⛔ **Không có cột `kind`** — mọi bubble như nhau ở MVP1–MVP2 | `UC-07` bước 6 *"chọn kiểu"* là `BR-004-04` — ⚠️ chọn option này là **mâu thuẫn** với requirement đó | ⛔ Không thêm cột. Nhưng `voice_no_speaker` và `system_panel` mất thông tin **đã có trong data** |

> ⭐ **Comic Studio đề xuất `A1`** — lý do là **dữ kiện thực nghiệm**, ⛔ không phải *"nó có nguồn đặc tả"*: **6/10** dòng thoại thật ⛔ không khớp danh mục ngành. Đó là **quan sát**, ⛔ không phải thiết kế. Ba giá trị `thought`/`shout`/`whisper` của `A2` là **quy ước ngành có thật**, nhưng ⛔ **chưa có** dòng dữ liệu nào trong repo cần tới ⇒ thêm bây giờ là *"thiết kế cho một yêu cầu chưa tồn tại"* (nguyên văn cảnh báo ở [`DB-Entity-Typeset-Layer`](../Schema/DB-Entity-Typeset-Layer.md)). Đường mở rộng đã sẵn và **rẻ**: enum thêm giá trị là migration cộng thêm.

> [!WARNING]
> ⚠️ **Căng thẳng phải nói ra, ⛔ không được im lặng** — cùng là dữ liệu MVP0, nhưng [`T-31`](./SDD-Comic-Studio.md) lại ghi *"⛔ không được đóng bằng cách chép khoá `rows` của MVP0 — dữ liệu đó là **nguyên liệu viết tay**"*. Vì sao ở đây `bubble_type` lại dùng được?
>
> ⇒ Vì hai khoá đó **khác loại**: `rows` là **cách người viết chọn để bố cục** — một trong nhiều cách, ⛔ không có gì bắt buộc nó đúng. Còn `bubble_type` ghi lại **thứ tác phẩm đòi**: Tà Thần ⛔ **không có thân thể** nên bubble ⛔ **không thể** có đuôi trỏ — đó là ràng buộc của **nội dung**, ⛔ không phải sở thích của người phân cảnh.
>
> ⭐ Nói gọn: `rows` là **cách làm** (thay được), `bubble_type` là **yêu cầu** (⛔ không thay được mà không đổi truyện). Danh mục `A1` lấy từ vế thứ hai.

---

## `Q2` — Caption / narration box: có trong horizon MVP0–MVP2 không

**Câu hỏi**: một ô chữ ⛔ **không gắn với người nói** (bảng trạng thái, lời dẫn chuyện, ghi chú thời gian/địa điểm) có được biểu diễn trong horizon này không?

| | Option | Hệ quả DDL — ⭐ đây là thứ Architect cần |
|:--:|---|---|
| ⭐ **B1** | ✅ **Có** — theo đúng đường mà nguồn đã chỉ định sẵn | ① Nới `comic.bubble.dialogue_line_id` thành **nullable** ② thêm cột **phân loại vai trò** ③ `CHECK`: vai trò `speech` ⇒ `dialogue_line_id IS NOT NULL`. ⭐ Đây ⛔ **không phải** *"nới cho chắc"* — [`DB-Entity-Typeset-Layer`](../Schema/DB-Entity-Typeset-Layer.md) đã viết sẵn: *"việc phải làm là một migration **có chủ đích**: nới `dialogue_line_id` + thêm cột phân loại vai trò"* |
| **B2** | ⛔ **Không** — giữ `NOT NULL`, để ngoài horizon | ⛔ Không đụng DDL. ⚠️ **Giá phải trả đã đo được**: 3 dòng `system_panel` tiếp tục sống bằng speaker giả `"system"`, và chúng **chảy vào human gate 1** — người phải xác nhận người nói cho ô chữ ⛔ không có người nói. `SDD-HG-01` ⛔ không có đường miễn trừ nào cho việc này |
| **B3** | Bảng riêng `comic.caption` | ⚠️ ⛔ **KHÔNG CÓ NGUỒN** — Comic Studio nêu cho đủ phương án, ⛔ không đề xuất. Hệ quả: compositor phải quét **hai** bảng, và `ix_bubble_panel_order` ⛔ **không còn phủ hết** thứ tự đọc trong panel — đúng chỗ [ADR-013](./ADR-013-Typeset-Layer-Separate-From-Art.md) gọi là *"đường nóng của compositor"* |

> ⭐ **Comic Studio đề xuất `B1`** — lý do ⛔ không phải *"cho đầy đủ tính năng"*, mà là: nhu cầu này **đã có trong dữ liệu** (3 dòng, §1), và `B2` đẩy chi phí sang **human gate** — nơi đắt nhất của hệ thống. `B1` cũng là đường mà nguồn **đã viết sẵn cách làm**, nên nó ⛔ không phải một thiết kế mới.

---

## `Q3` — SFX: cùng đường với caption hay tách riêng

**Câu hỏi**: chữ tượng thanh cách điệu (*Bùm*, *Rầm*, *Vút*) nằm trong khung tranh — biểu diễn thế nào?

⚠️ **Khác `Q2` ở một điểm quyết định**: dữ liệu MVP0 có **0 dòng SFX** — ⛔ không như caption vốn đã có 3 dòng.

| | Option | Hệ quả |
|:--:|---|---|
| ⭐ **C1** | **Cùng đường với `Q2`** — SFX là một giá trị của cột phân loại vai trò | ⛔ Không thêm DDL ngoài `B1`. SFX chỉ là một vai trò nữa trong cùng bảng |
| **C2** | ⛔ **Ngoài horizon** — quyết sau khi có dữ liệu thật | ⛔ Không đụng DDL. ⭐ **Nhất quán với `A1`**: ⛔ không thiết kế cho thứ chưa có dòng dữ liệu nào |
| **C3** | Cơ chế riêng (SFX là **hình vẽ**, ⛔ không phải chữ) | ⚠️ ⛔ **KHÔNG CÓ NGUỒN**. ⛔ Comic Studio không đề xuất |

> ⭐ **Comic Studio đề xuất `C1`** — với **một ràng buộc đi kèm phải ký cùng**: dù chọn `C1` hay `C2`, SFX **thuộc typeset layer**, ⛔ **tuyệt đối không** để model nướng chữ vào pixel ([ADR-013](./ADR-013-Typeset-Layer-Separate-From-Art.md), `G1-e`). Đây ⛔ không phải option — nó **đã chốt**, ghi ra để ⛔ không ai đọc `C2` thành *"vậy cứ để model vẽ chữ tượng thanh"*.
>
> ⚠️ Nếu anh thấy `C2` đúng hơn (nhất quán với `A1`), đó là lựa chọn **chặt chẽ về kỷ luật** — em đề xuất `C1` chỉ vì nó ⛔ **không tốn thêm gì** một khi `B1` đã mở đường.

---

## 5. Hệ quả dây chuyền sau khi ký

Ký phiếu này mở khoá **bốn** chỗ đang chờ:

| Chỗ bị chặn | Mở khoá điều gì |
|---|---|
| [`DB-Entity-Typeset-Layer`](../Schema/DB-Entity-Typeset-Layer.md) | ⭐ **DDL viết được** — `TBD-BUBBLE-KIND` và `TBD-SFX-NARRATION` cùng đóng |
| [`Endpoint-Bubble-Typeset`](../API/Endpoint-Bubble-Typeset.md) | `E-BT-2` — có chấp nhận `dialogue_line_id = null` hay trả `400` |
| [`Components`](../../040-Design/Design-System/Components.md) `C-05` | Control *"chọn kiểu bubble"* hiện khai **danh mục rỗng chờ nguồn** — điền được |
| [`SDD §9.1`](./SDD-Comic-Studio.md) `T-26` | Chuyển trạng thái sang ✅ **ĐÃ ĐÓNG** |

⚠️ **Việc phải làm ngay sau khi ký** — ⛔ không được quên, nếu không phiếu này thành giấy chết: Architect ghi kết quả vào `DB-Entity-Typeset-Layer` + `Endpoint-Bubble-Typeset`, rồi đánh dấu `T-26` ở `SDD §9.1`.

---

## 6. Ô ký

| Câu hỏi | Option đã chọn | Ngày ký | Ghi chú của Founder |
|---|:--:|:--:|---|
| `Q1` — Danh mục kiểu bubble | ⬜ `A1` ⭐ · ⬜ `A2` · ⬜ `A3` · ⬜ `A4` | | |
| `Q2` — Caption / narration box | ⬜ `B1` ⭐ · ⬜ `B2` · ⬜ `B3` | | |
| `Q3` — SFX | ⬜ `C1` ⭐ · ⬜ `C2` · ⬜ `C3` | | |

- [ ] **Founder xác nhận** ràng buộc ⛔ **không nướng chữ vào pixel** vẫn giữ nguyên với **mọi** option (`ADR-013` · `G1-e`)

---

## 7. Tài liệu tham khảo

- [SDD-Comic-Studio §9.1](./SDD-Comic-Studio.md) — hàng `T-26`, `T-30`, `T-31`
- [ADR-013 — Typeset Layer Separate From Art](./ADR-013-Typeset-Layer-Separate-From-Art.md) — bảng `TBD`
- [DB-Entity-Typeset-Layer](../Schema/DB-Entity-Typeset-Layer.md) — `TBD-BUBBLE-KIND`, `TBD-SFX-NARRATION`, ghi chú nullability
- [Endpoint-Bubble-Typeset](../API/Endpoint-Bubble-Typeset.md) — `E-BT-2`
- [UC-07 — Edit Bubble And Dialogue In Panel](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) — bước 6, `AF-6`
- [Components — Design System](../../040-Design/Design-System/Components.md) — `C-05`
- `mvp0/panel-script-ch1.yaml` · `mvp0/panel-script-ch2.yaml` — nguồn của kiểm kê §1

---

_Created by Comic Studio_
_Author: trisjr_
