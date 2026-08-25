# Findings — Lens PRODUCT OWNER (backlog priority & Story contract)

## Table of Contents

1. [Phạm vi & quy ước của lens](#phạm-vi--quy-ước-của-lens)
2. [Mục 1 — RICE hay MoSCoW hay cả hai?](#mục-1--rice-hay-moscow-hay-cả-hai)
3. [Mục 2 — Ranh giới `Backlog-Priority.md` (block copy nguyên vào `outline.md`)](#mục-2--ranh-giới-backlog-prioritymd-block-copy-nguyên-vào-outlinemd)
4. [Mục 3 — Cấu trúc `Backlog-Priority.md`](#mục-3--cấu-trúc-backlog-prioritymd)
5. [Mục 4 — INVEST + Definition of Ready/Done](#mục-4--invest--definition-of-readydone)
6. [Cảnh báo cho PM](#cảnh-báo-cho-pm)

---

## Phạm vi & quy ước của lens

| | |
|---|---|
| **Lens** | `product-owner` — read-only. Trả lời 2 câu hỏi PM phải chốt **trước** khi writer chạm file |
| **Role memory** | `knowledge-base/45-Role-Memory/product-owner/` **KHÔNG tồn tại** (verified bằng Glob: **10 role khác / 13 file**, không có `product-owner`). Không có preference lịch sử nào để kế thừa |
| **Role definition** | `.agent/roles/product-owner.md` **KHÔNG tồn tại** (Glob `.agent/roles/*` = 0 file). Lens chạy trên role card nạp qua system prompt |
| **Ghi đúng 1 file** | `docs/010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/product-owner.md` |

**Quy ước nhãn** — mượn nguyên hệ nhãn của tầng Planning để mọi con số trong file này đọc được cùng một cách:

| Nhãn | Nghĩa trong file này |
|---|---|
| `[SRC]` | Sự thật trích từ repo — **có anchor file + mục**. Kiểm tra được |
| `[PO]` | **Phán đoán nghề nghiệp của em.** Không có nguồn trong repo. Anh được phép bác bỏ |
| `[EM]` | Ước lượng/ngưỡng em tự định nghĩa — cùng nghĩa với `[EM]` của tầng Planning: **không phải số đo** |
| `TBD` | Chưa có dữ liệu, và em **không bịa** ra |

> [!IMPORTANT]
> **Một lệch có ý thức với role card của chính em.** Role card `product-owner` ghi *"Write and refine Acceptance Criteria (Gherkin format)"*. Mục 4(c) của file này **cố ý ghi đè** hướng dẫn đó cho bối cảnh này, và nêu lý do tại chỗ. Đây là quyết định, không phải nhầm.

---

## Mục 1 — RICE hay MoSCoW hay cả hai?

### 1.1 Trả lời dứt khoát

> **KHÔNG dùng RICE. KHÔNG dùng MoSCoW.**
> Cấu hình chốt là **`UNLOCK-ORDER`**: một cột nhãn **kế thừa** (không chấm lại) + một `Rank` **lexicographic 3 khoá** trong phạm vi **một mốc**.

Nhãn của kết luận: `[PO]`. Đây là phán đoán nghề nghiệp của em, không phải sự thật trích từ repo. Nhưng **các lý do bên dưới đều là `[SRC]`.**

### 1.2 Vì sao RICE không dùng được — cả tử số VÀ mẫu số đều không tồn tại

| Biến RICE | Đo bằng gì ở dự án này | Trạng thái | Anchor |
|---|---|---|---|
| **Reach** | "số người dùng bị ảnh hưởng / đơn vị thời gian" | ⛔ **MẪU SỐ KHÔNG TỒN TẠI.** Chưa có dòng code nào; chưa có tenant nào; **chưa có Design partner nào** — *"mọi phán đoán về 'đủ tốt' đang do chính người build đưa ra"* | `[SRC]` MVP-Scope §1.2 CF-1.3 · Charter §6 cảnh báo 2 + "Ba lỗ hổng" |
| **Impact** | thang 0.25–3 gán bằng tay | 🟡 Gán được, nhưng **không kiểm chứng được** với 0 user. Suy biến thành *"cái tôi thấy quan trọng"* | `[PO]` |
| **Confidence** | % tự tin | 🟡 Repo **đã có** hệ nhãn tốt hơn cho việc này (`[OFF]`/`[BCN]`/`[TC]`/`[EM]`/`[CHỐT]`). Thêm `Confidence %` là hệ thứ hai đo cùng một thứ | `[SRC]` MVP-Scope khối `[!IMPORTANT]` đầu file |
| **Effort** | person-month | ⛔ **MẪU SỐ KHÔNG TỒN TẠI.** Roadmap tự khai: *"chưa có WBS hay ETA cho MVP1/MVP2/MVP3"*, *"Tổng tuần-người: `TBD`"* (cả 4 mốc), *"Hệ số AI assist chưa biết → `TBD`"* | `[SRC]` Roadmap §1.3 + cột *Effort ước tính* bảng §2 |

**Kết luận về RICE**: RICE là một **phân số**. Ở đây **tử số không có mẫu số dân số** và **mẫu số không có đơn vị effort**. Nhân bốn số `TBD`/`[EM]` với nhau rồi chia cho một số `TBD` cho ra **một con số trông như đo được** — đúng thứ mà tầng Planning của repo này bỏ nhiều công để chống: *"Mọi con số mang nhãn `[EM]` là khoảng trống dữ liệu được thừa nhận, không phải sự thật đã đo"* `[SRC]` MVP-Scope khối `[!IMPORTANT]`.

Thêm một lý do độc lập, và nó là lý do quyết định: trong horizon 09/2026–02/2027, **phần lớn hạng mục là hạ tầng/nền dữ liệu**, không phải tính năng người dùng thấy. `Reach` của Story *"`tenant_id NOT NULL` mọi bảng"* = **0 user hôm nay và 100% user mãi mãi**. Một biến cho cùng một giá trị ở mọi hàng thì **không phân biệt được gì** — nó chỉ làm loãng ba biến còn lại. `[SRC]` MVP-Scope §3 khối E + KC-5 · `[PO]` cho phần lập luận.

### 1.3 Vì sao MoSCoW không dùng được — nó **trùng lặp** hệ nhãn đã tồn tại

`MVP-Scope.md` §3 đã gán nhãn cho **43 hạng mục A1…H6**, dùng hệ ký hiệu: `✅` có đầy đủ · `🟡` có một phần/bản tối thiểu · `⛔` hoãn sang mốc sau · `❌` **cắt hẳn, không có trong Full Scope** `[SRC]` MVP-Scope §3 dòng "Ký hiệu".

Ánh xạ trùng lặp — **1:1, không còn chỗ cho giá trị mới**:

| MoSCoW | Nhãn đã tồn tại ở MVP-Scope §3 | Trùng lặp kiểu gì |
|---|---|---|
| **Must** | `✅` tại cột mốc đang xét | Trùng hoàn toàn |
| **Should** | `🟡` (có một phần / bản tối thiểu) | Trùng hoàn toàn |
| **Could** | `⛔` (hoãn sang mốc sau) | Trùng hoàn toàn |
| **Won't** | `❌` + **cắt hẳn** (C4, D6, E6 — *"loại khỏi thiết kế, không phải bị hoãn"*) | Trùng hoàn toàn, **và MVP-Scope còn phân biệt tinh hơn**: `❌ ở mốc này` khác `❌ ở cột Full Scope` |

**Hai lý do bác MoSCoW, cái thứ hai nặng hơn:**

1. **Trùng lặp = mầm mâu thuẫn.** Hai hệ nhãn cho cùng một hạng mục nghĩa là hai nơi phải sửa khi scope đổi. Với **bus factor = 1** `[SRC]` Glossary term `bus factor`, không có ai đối chiếu. Hệ nhãn thứ hai sẽ lệch, và lệch âm thầm.
2. ⭐ **MoSCoW LOSSY hơn hệ đang có.** MVP-Scope §3 gán nhãn **theo từng mốc — 5 cột** (MVP0…MVP4) + 1 cột Full Scope. MoSCoW là **một nhãn vô hướng**. Chuyển từ 6 chiều xuống 1 chiều là **mất thông tin**, không phải thêm quyết định. Ví dụ cụ thể trong repo: hạng mục **D1** = `❌ | 🟡 #5 | 🟡 +#3+#4 | ✅ | ✅` — MoSCoW không có cách nào biểu diễn hàng này mà không mất mát.
3. **Bằng chứng nó SẼ lệch, đã có sẵn trong repo**: `G1-d` FAIL ⇒ *"cứng hoá ≤2 nhân vật/panel thay vì ≤3 (đổi C5 ở bảng mục 3)"* `[SRC]` MVP-Scope §7.2 bảng kết luận gate. Nhãn của C5 **đổi theo verdict gate**. Một nhãn MoSCoW gán bằng tay ở tài liệu thứ tư sẽ không đổi theo — và không ai biết nó đã lệch.

### 1.4 Cấu hình CHỐT — `UNLOCK-ORDER`

`[PO]` toàn bộ mục 1.4 là thiết kế của em; các thang điểm đều **dẫn xuất từ nguyên tắc đã có trong repo**, không phát minh tiêu chí mới.

#### (a) Cột kế thừa — CHẤM MỘT LẦN Ở NGUỒN, COPY Ở ĐÂY

| Cột | Giá trị | Nguồn duy nhất | Quy tắc |
|---|---|---|---|
| `Scope-Label` | `✅` \| `🟡` \| `⛔` \| `❌` | `MVP-Scope.md` §3, **ô giao (hạng mục × mốc)** | **CẤM chấm lại.** Lệch ⇒ hàng backlog sai, không phải MVP-Scope sai |
| `Mốc` | `Pre-cycle/MVP0` \| `MVP1` \| `MVP2` \| `MVP3` \| `MVP4` | `MVP-Scope.md` §1.3 + §3 | **CẤM chấm lại.** Thứ tự mốc là `[CHỐT]` CF-8.3, *"cố định, không mở lại"* |

#### (b) `Rank` — LEXICOGRAPHIC 3 KHOÁ, **chỉ trong phạm vi một mốc**

Không nhân, không cộng, **không có điểm tổng**. So khoá 1 trước; bằng nhau thì so khoá 2; bằng nữa thì khoá 3.

| Khoá | Thang | Định nghĩa | Nguyên tắc nguồn |
|---|---|---|---|
| **1. `I` — Irreversibility** | `I2` | **Không backfill được.** Không làm bây giờ ⇒ dữ liệu/quyền quá khứ mất **vĩnh viễn** | `[SRC]` MVP-Scope NT-3 vế 2 (*"giữ cái rẻ-mà-không-backfill-được"*) + mục 6 KC-1…KC-7 (*"rẻ khi làm từ đầu, không thể sửa về sau"*) |
| | `I1` | Sửa sau **được**, nhưng là migration trên dữ liệu thật | `[SRC]` KC-5 (*"migration đắt nhất tồn tại"* là ví dụ mẫu của bậc trên) |
| | `I0` | Sửa sau gần như miễn phí | |
| **2. `B` — Blocking degree** | `B2` | Chặn **cứng** ≥1 exit criterion của mốc (Roadmap §6.2 cột *Loại phụ thuộc* = "Cứng") | `[SRC]` Roadmap §6.2 bảng phụ thuộc + §6.3 đường găng |
| | `B1` | Chặn ≥1 Story khác, nhưng không chặn exit criterion | |
| | `B0` | Không chặn gì | |
| **3. `G` — Gate proximity** | `G2` | Story **chính là** một exit criterion (`P-x`/`M1-x`/`M2-x`) hoặc một tiêu chí gate (`G1-a…e`, `G2-a…d`) | `[SRC]` Roadmap §2 cột *Điều kiện ra* · MVP-Scope §7 |
| | `G1` | Cần thiết **để exit criterion đó đo được** (ví dụ: `usage_daily` để G2-a có số) | `[SRC]` Roadmap §6.2 hàng *regen ratio p50/p90 → G2* |
| | `G0` | Không nằm trên đường tới gate/exit criterion nào của mốc | |

#### (c) ⚠️ Tie-break — **nói thẳng chỗ thang này sẽ bão hoà**

Trong `MVP1`, **rất nhiều Story sẽ cùng ra `I2/B2/G2`**: `tenant_id` + RLS (KC-5), 5 hạng mục provenance (KC-1…KC-4), sửa khoá thời gian, opt-out Điều 37b (KC-6) — cả nhóm đều không backfill được, đều chặn cứng, đều là exit criterion `M1-x`. `[SRC]` Roadmap §2 hàng MVP1 + §6.2. Không giấu điều này: **đúng ở mốc quan trọng nhất, thang gần như không phân biệt được.**

Thứ tự dư (residual order), áp theo đúng trình tự này:

| # | Tie-break | Nội dung | Anchor |
|---|---|---|---|
| **T1** | **Phụ thuộc kỹ thuật trực tiếp** | A chặn B ⇒ A trước B. Đây là quan hệ **quan sát được**, không phải chấm điểm. Ví dụ đã có trong repo: *sửa khoá thời gian* chặn *mọi bảng timeline của MVP1* | `[SRC]` Roadmap §6.2 |
| **T2** | **`E_hitl` thấp trước** | Story tạo ra ít nghĩa vụ **giờ-người** vĩnh viễn hơn thì đi trước — vì đó là ràng buộc thật của đội một người | `[SRC]` Glossary term `HITL gate` |
| **T3** | **`E_build` thấp trước** | Rẻ hơn thì trước — chỉ dùng khi T1, T2 vẫn bằng nhau | `[PO]` |
| **T4** | **Founder quyết**, ghi **đúng một dòng lý do** vào cột `Ghi chú` | Không có tie-break thứ năm. Founder là `A` ở cả 9 hàng RACI ⇒ đây là nơi hợp pháp để dừng thuật toán | `[SRC]` Charter §6 |

#### (d) Ai chấm, khi nào chấm lại

| | |
|---|---|
| **Ai đề xuất** | `product-owner` (lens/agent). Charter §6 hàng 1: AI Agent là **C** — *"`product-owner` phản biện định vị & phân khúc"* `[SRC]` |
| **Ai chốt** | **Founder.** Charter §6 hàng 1 = **A, R** `[SRC]`. Không có ô nào khác quyết được |
| **Chấm lại tại đúng 4 trigger** | (1) **Sau verdict mỗi gate** G0/G1/G2 — vì verdict đổi được cả `Scope-Label` (ví dụ G1-d ⇒ C5) `[SRC]` MVP-Scope §7.2 · (2) khi `MVP-Scope.md` hoặc `Roadmap.md` **thay đổi** · (3) khi **thêm Story mới** vào backlog · (4) **rà hàng tháng, ngày cuối tháng** — dùng **đúng nhịp đã có** ở OKRs §1.2, **không tạo nhịp mới** `[SRC]` |
| **KHÔNG chấm lại** | Hàng tuần. Nhịp tuần của OKRs §1.2 chỉ hỏi *"số đã nhúc nhích chưa"* — không phải nhịp xếp lại thứ tự `[SRC]` |

#### (e) ⛔ Ba thứ cấu hình này CỐ Ý không có

| Bỏ | Vì sao `[PO]` |
|---|---|
| **Điểm tổng (composite score)** | Một số thực gộp 3 khoá sẽ che mất **khoá nào đang quyết định**. Lexicographic giữ được tính truy vết: đọc hàng là biết vì sao nó đứng đó |
| **`Confidence %`** | Repo đã có hệ nhãn nguồn `[OFF]`/`[BCN]`/`[TC]`/`[EM]`/`[CHỐT]` `[SRC]`. Thêm % là hệ thứ hai đo cùng thứ |
| **Rank xuyên mốc (global rank 1…N)** | Thứ tự mốc **đã cố định** `[CHỐT]` CF-8.3 `[SRC]`. Một global rank sẽ **cho phép** biểu diễn thứ tự vi phạm CF-8.3 ⇒ chính là tạo nguồn sự thật thứ tư |

---

## Mục 2 — Ranh giới `Backlog-Priority.md` (block copy nguyên vào `outline.md`)

> [!NOTE]
> **Block dưới đây là self-contained.** PM copy nguyên từ đầu §2.1 tới hết §2.3 vào mục *Nguồn sự thật* của hạng mục #7 trong `outline.md` — không cần đọc phần nào khác của file này.
>
> ⚠️ **Một sửa duy nhất khi copy — relative path đổi độ sâu.** File này ở `findings/` (sâu hơn `outline.md` một cấp). Khi dán vào `outline.md`, đổi `../../../` → `../../` ở cả 3 link của bảng §2.1. Khi dán vào chính `Backlog-Priority.md` (`docs/022-User-Stories/`), đổi thành `../010-Planning/`.

### 2.1 Bảng bốn tài liệu — khuôn của `MVP-Scope.md` §1.1

| Tài liệu | Trả lời câu hỏi gì | **KHÔNG** trả lời câu hỏi gì |
|---|---|---|
| [Roadmap.md](../../../Roadmap.md) | **Khi nào, theo thứ tự nào, exit criteria từng mốc** | Lý do cắt một hạng mục |
| [MVP-Scope.md](../../../MVP-Scope.md) | **Cái gì vào MVP0–MVP4, cái gì bị cắt/hoãn, và điều kiện Go/No-Go** | Ngày tháng, thứ tự thời gian, phân bổ effort theo lịch |
| [OKRs.md](../../../OKRs.md) | **Thành công trông như thế nào ở cuối mỗi chu kỳ** — Objective (định tính) + Key Result (định lượng) | Khi nào làm gì; ranh giới scope; ngưỡng gate |
| **Backlog-Priority.md** *(tài liệu thứ tư)* | **Trong MỘT mốc đã cho: làm Story nào TRƯỚC Story nào, và Story nào là MVP Story** | **Mốc nào chứa Story nào** (→ MVP-Scope) · **Story xong khi nào / bất kỳ ngày tháng nào** (→ Roadmap) · **ngưỡng thành công** (→ OKRs) · **nội dung + Acceptance Criteria của Story** (→ `Story-{Title}.md`) |

*Ba hàng đầu là trích near-verbatim từ tự-mô-tả của chính từng tài liệu*: MVP-Scope §1.1 (hàng 1–2) và OKRs §1.1 (hàng 3) `[SRC]`.

**Tính chất thiết kế của hàng 4**: `Backlog-Priority` **không chia sẻ câu hỏi nào** với ba tài liệu trên. Nó lấp đúng một khoảng trống mà cả ba đều không lấp: *"MVP1 chứa 20 Story, làm cái nào trước?"* — Roadmap dừng ở mức **mốc**, MVP-Scope dừng ở mức **hạng mục A1…H6**, OKRs dừng ở mức **KR**. Không ai xếp thứ tự **Story**.

### 2.2 Xung đột: cái nào thắng

> [!CAUTION]
> **`Roadmap.md` THẮNG. Luôn luôn. Không có ngoại lệ.**
>
> `Backlog-Priority.md` là **VIEW XẾP HẠNG DẪN XUẤT** (derived ranking view), **KHÔNG** phải nguồn độc lập.
>
> **Nếu `Backlog-Priority` và `Roadmap`/`MVP-Scope` nói khác nhau ⇒ HÀNG BACKLOG ĐÓ SAI, không phải `Roadmap` sai.** Xử lý = sửa hoặc **xoá hàng đó**. Không bao giờ sửa `Roadmap.md` để khớp bảng backlog.

Khuôn này **mượn nguyên** một pattern đã có trong repo, không phát minh: OKRs §1.1 khối `[!NOTE]` ghi *"Mọi mốc thời gian trong tài liệu này lấy từ Roadmap.md, không mốc nào được tạo mới ở đây. […] Nếu một KR cần mốc khác, **KR đó sai — không phải Roadmap sai**"* `[SRC]`. Tài liệu thứ tư dùng **cùng một luật**, để repo chỉ có một cơ chế phân xử chứ không phải bốn.

### 2.3 Bốn cơ chế giữ đồng bộ — cứng, không phải lời hứa

| # | Cơ chế | Nội dung | Phát hiện lệch bằng cách nào |
|---|---|---|---|
| **S1** | **Cột `Anchor` bắt buộc, không được trống** | Mỗi hàng backlog phải trích **≥1 hàng `MVP-Scope §3`** (dạng `A1`…`H6`) **VÀ ≥1 exit criterion `Roadmap`** (dạng `P-x`/`M1-x`/`M2-x`/`G1-x`) | Hàng không trích được anchor ⇒ **hàng đó không hợp lệ**, xoá hoặc đưa vào mục *Story chưa xếp được* |
| **S2** | **Hai cột kế thừa, CẤM chấm lại** | `Mốc` và `Scope-Label` là **copy** từ MVP-Scope §3, không phải phán đoán mới | Đối chiếu cơ học ô giao (hạng mục × mốc). Lệch ⇒ sửa bảng backlog |
| **S3** | ⭐ **CẤM ngày tháng** | `Backlog-Priority.md` **không được chứa một ngày, tháng, quý hay tuần nào**. Chỉ chứa **tên mốc**. Ngày tháng là độc quyền của `Roadmap.md` | Grep tài liệu tìm `/2026`, `/2027`, `Q4`, `tuần` — có kết quả nghĩa là đã drift |
| **S4** | **Cùng nhịp rà với OKR, không thêm nhịp** | Rà lại tại 4 trigger của Mục 1.4(d): verdict gate · MVP-Scope/Roadmap đổi · thêm Story · rà cuối tháng (OKRs §1.2) | Không có nhịp riêng ⇒ không có cơ hội trôi lệch pha |

---

## Mục 3 — Cấu trúc `Backlog-Priority.md`

> Repo **không có template** cho loại tài liệu này (verified: RULE-001 *Document Type Mapping* không có hàng nào cho *Prioritized Backlog*; `docs/022-User-Stories/` chỉ có `Stories-MOC.md` + 3 `.gitkeep`) `[SRC]`. Mục này là **contract cấu trúc duy nhất** cho writer. Nhãn: `[PO]`.

### 3.1 Frontmatter (RULE-001 quy tắc #3 — bắt buộc)

```yaml
---
id: BACKLOG-001
type: backlog-priority
status: draft
owner: "@trisjr"
linked-to: "../010-Planning/Roadmap.md"
created: 2026-08-24
---
```

`status: draft` — theo Assumption #4 của `brief.md` (Charter §9 còn 3 điều kiện chặn chưa gỡ) `[SRC]`.

### 3.2 Danh sách heading cấp 1–2

| Cấp | Heading | Nội dung bắt buộc |
|---|---|---|
| **H1** | `# Prioritized Backlog — comic-studio` | — |
| — | *(khối `> [!IMPORTANT]`)* | Quy ước nhãn `[OFF]`/`[BCN]`/`[TC]`/`[EM]`/`[CHỐT]` + **câu "tài liệu này là view dẫn xuất, Roadmap thắng"** |
| **H2** | `## Mục lục` | Theo `.claude/rules/create-file-markdown.md` (*tài liệu kiến thức có Table of Contents ở đầu file, Tài liệu tham khảo ở cuối*) — **không** phải RULE-001; RULE-001 không nói gì về TOC |
| **H2** | `## 1. Mục đích & ranh giới` | **Copy nguyên bảng 4 hàng của Mục 2.1 + khối `[!CAUTION]` của Mục 2.2 + bảng S1–S4 của Mục 2.3** |
| **H2** | `## 2. Cách đọc bảng backlog` | Schema cột (§3.3) + định nghĩa thang `I`/`B`/`G` + trình tự tie-break T1→T4 + **định nghĩa "MVP Story"** (§3.4) |
| **H2** | `## 3. Backlog theo mốc` | Bảng chính, **chia H3 theo mốc** (xem §3.5). `Rank` reset về 1 ở mỗi H3 |
| **H2** | `## 4. MVP Stories — danh sách rút gọn` | Chỉ các hàng có `⭐`, **link lại chứ không copy dữ liệu** (chống lệch nội bộ) |
| **H2** | `## 5. Story chưa xếp được` | Story thiếu anchor hoặc ở mốc ngoài horizon ⇒ `TBD` **kèm lý do**. Mục này tồn tại để writer **không bịa rank** |
| **H2** | `## 6. Lịch chấm lại` | 4 trigger của Mục 1.4(d) + **câu "không chấm lại hàng tuần"** |
| **H2** | `## 7. Tài liệu tham khảo` | Markdown link tới Roadmap · MVP-Scope · OKRs · Charter · Stories-MOC · Glossary |

### 3.3 Schema chính xác của bảng backlog

Thứ tự cột là **cố định**. Writer không được thêm, bớt, hay đổi thứ tự cột.

| # | Cột | Ý nghĩa | Kiểu giá trị | Bắt buộc |
|---|---|---|---|:--:|
| 1 | `#` | `Rank` **trong mốc**. Reset về `1` ở mỗi H3 | `integer` ≥ 1, **unique trong mốc** | ✅ |
| 2 | `Story` | Link tới Story | **markdown link relative**: `[Story-{Title}](./Backlog/Story-{Title}.md)` | ✅ |
| 3 | `Epic` | Epic cha | **markdown link relative**: `[Epic-{Title}](./Epics/Epic-{Title}.md)` | ✅ |
| 4 | `Mốc` | Mốc chứa Story — **kế thừa, cấm chấm lại** | enum: `Pre-cycle/MVP0` \| `MVP1` \| `MVP2` \| `MVP3` \| `MVP4` | ✅ |
| 5 | `MVP` | Đánh dấu MVP Story | `⭐` hoặc **để trống** (không dùng `—`, không dùng bold) | ✅ |
| 6 | `Hạng mục` | ID hạng mục MVP-Scope §3 | enum: `A1`…`A7` \| `B1`…`B5` \| `C1`…`C7` \| `D1`…`D7` \| `E1`…`E8` \| `F1`…`F6` \| `GP-1`…`GP-5` \| `H1`…`H6`. Nhiều giá trị: phân tách bằng `, ` | ✅ |
| 7 | `Scope-Label` | Nhãn tại ô giao (hạng mục × mốc) — **kế thừa, cấm chấm lại** | enum: `✅` \| `🟡` \| `⛔` \| `❌` | ✅ |
| 8 | `I` | Irreversibility | enum: `I2` \| `I1` \| `I0` | ✅ |
| 9 | `B` | Blocking degree | enum: `B2` \| `B1` \| `B0` | ✅ |
| 10 | `G` | Gate proximity | enum: `G2` \| `G1` \| `G0` | ✅ |
| 11 | `E_build` | Giờ-người Founder để implement (gồm cả điều phối AI agent) | `integer` **giờ-người**, hoặc `TBD` | ✅ |
| 12 | `E_hitl` | Giờ-người **người** để chạy qua HITL gate mà Story này tạo ra/tiêu thụ, **mỗi lần chạy / chapter** | `số` **giờ-người/chapter**, `0`, hoặc `TBD` | ✅ |
| 13 | `Anchor` | Căn cứ nguồn (cơ chế **S1**) | `MVP-Scope §3 {ID}` + `Roadmap {exit-criterion}`. Ví dụ: `MVP-Scope §3 E1 · Roadmap M1-1` | ✅ |
| 14 | `Ràng buộc cứng` | Ràng buộc không được vi phạm | list: `KC-1`…`KC-7` \| `C1`…`C10` \| `AG-1`…`AG-8` \| `—` | ✅ |
| 15 | `Ghi chú` | **Chỉ dùng cho tie-break T4**: một dòng lý do Founder quyết. Không dùng làm chỗ viết mô tả Story | text ≤ 1 dòng, hoặc trống | — |

> [!WARNING]
> **Cột 11 và 12 là hai đại lượng KHÁC NHAU, cấm cộng vào nhau.** `E_build` là chi phí **một lần**; `E_hitl` là nghĩa vụ **lặp lại vĩnh viễn** cho người duy nhất trong đội. Đây là chính xác cùng loại lỗi mà MVP-Scope §5.1 cảnh báo với CF-6.7 vs CF-6.8: *"hai mẫu số khác nhau, CẤM TRỪ CHO NHAU"* `[SRC]`. Hai cột này khớp 1:1 với `E_build`/`E_hitl` của Mục 4(b), nên **DoR R3 kiểm được trực tiếp từ bảng**.

### 3.4 Cách đánh dấu MVP Stories — **suy ra được từ cột, không phán đoán**

| | |
|---|---|
| **Ký hiệu** | `⭐` ở cột 5 (`MVP`). Ô không phải MVP Story **để trống** |
| **Định nghĩa (mechanical rule)** | `⭐` ⟺ `Mốc ∈ {Pre-cycle/MVP0, MVP1, MVP2}` **VÀ** `Scope-Label ∈ {✅, 🟡}` **VÀ** `G ∈ {G2, G1}` |
| **Nghĩa** | *"Story bắt buộc phải xong để một exit criterion của một mốc **trong horizon** đạt được"* |
| **Vì sao dừng ở MVP2** | Roadmap §1.2 kết luận tường minh: horizon 09/2026–02/2027 chứa **MVP0 + MVP1 + MVP2**; **MVP3 và MVP4 rơi ra ngoài** `[SRC]` Roadmap §1.2 + §5.1 |
| **Nhãn** | `[PO]` cho quy tắc; `[SRC]` cho ranh giới horizon |
| **Kiểm tra chéo bắt buộc** | Mọi `⭐` phải có `Anchor` chứa **ít nhất một** exit criterion `P-x`/`M1-x`/`M2-x`. `⭐` mà không có ⇒ sai |

> [!WARNING]
> ⭐ **Điều kiện `G ∈ {G2, G1}` CỐ Ý loại một số hàng `✅`/`🟡` trong horizon — đây là thiết kế, không phải lỗi bỏ sót.** Hai ví dụ thật trong repo: **H2** (log preference data — `✅` ở MVP1 nhưng **không** ứng với exit criterion `M1-x` nào) và **H5** (abuse controls tối thiểu — `🟡` ở MVP1, chỉ được nhắc trong ghi chú của Roadmap §4 X-b) `[SRC]` MVP-Scope §3 khối H · Roadmap §2 + §4.
>
> Nghĩa đúng: hai Story đó **vẫn phải làm ở MVP1** (nhãn `✅`/`🟡` là bắt buộc), nhưng **không** là *MVP Story* theo định nghĩa hẹp ở trên vì **không có exit criterion nào FAIL nếu chúng chậm**. Writer và PM đừng "sửa" bằng cách thêm `⭐` — nếu muốn chúng có `⭐`, cách đúng là **thêm exit criterion vào `Roadmap.md`**, không phải đổi cột ở bảng backlog (luật §2.2: Roadmap thắng).



⚠️ **Từ "MVP" ở đây nhập nhằng và PM phải chốt** — xem [Cảnh báo #6](#cảnh-báo-cho-pm).

### 3.5 Link relative path — chuẩn RULE-001 quy tắc #5

Tài liệu đứng tại `docs/022-User-Stories/Backlog-Priority.md`. Mọi link tính từ đó:

| Đích | Path **ĐÚNG** | Sai (cấm) |
|---|---|---|
| Story | `[Story-Tenant-Isolation](./Backlog/Story-Tenant-Isolation.md)` | `[[Story-Tenant-Isolation]]` |
| Active Story | `[Story-Tenant-Isolation](./Active-Sprint/Story-Tenant-Isolation.md)` | `[[...]]` |
| Epic | `[Epic-Multi-Tenancy](./Epics/Epic-Multi-Tenancy.md)` | `[[Epic-Multi-Tenancy]]` |
| MOC cùng cấp | `[Stories-MOC](./Stories-MOC.md)` | |
| Roadmap | `[Roadmap](../010-Planning/Roadmap.md)` | |
| MVP-Scope | `[MVP-Scope](../010-Planning/MVP-Scope.md)` | |
| OKRs | `[OKRs](../010-Planning/OKRs.md)` | |
| Charter | `[Charter-Comic-Studio](../010-Planning/Charter-Comic-Studio.md)` | |
| Glossary | `[Glossary](../999-Resources/Glossary.md)` | |

**Anchor tới mục con** dùng đúng dạng đã có trong repo: `[MVP-Scope §3](../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope)` `[SRC]` — dạng này đang được dùng khắp Roadmap/OKRs.

> RULE-001 quy tắc #5: *"**BẮT BUỘC** sử dụng standard markdown links `[Display Name](./relative-path/file.md)`. **KHÔNG** dùng wiki-links `[[...]]`"* `[SRC]`. Lưu ý: khối *Luồng quyết định* của chính RULE-001 (bước 4) và `pm-doc.md` bước 5 vẫn ghi "Wiki-links" — **quy tắc #5 thắng**, khớp Assumption #5 của `brief.md` `[SRC]`.

---

## Mục 4 — INVEST + Definition of Ready/Done

> Đây là block PM dán vào **mọi** prompt dispatch của writer Story. Nhãn: `[PO]` cho khuôn; `[SRC]` cho từng anchor.

### 4.1 INVEST diễn giải lại cho đội một người, chưa có code

| Chuẩn | Diễn giải BẮT BUỘC trong bối cảnh này | Anchor |
|---|---|---|
| **I**ndependent | Độc lập **về deliverable**, không cần độc lập về schema. Với 1 dev/1 monolith/1 DB, đòi độc lập tuyệt đối sẽ sinh Story giả. Thay bằng: **phụ thuộc phải được KHAI TƯỜNG MINH** ở tie-break T1 | `[SRC]` MVP-Scope E5 (modular monolith 1 DB) |
| **N**egotiable | ⚠️ **BỊ GIỚI HẠN.** Story chạm `KC-1…KC-7` là **KHÔNG negotiable** — MVP-Scope mục 6 là *"danh sách duy nhất không mở ra thương lượng scope"* | `[SRC]` MVP-Scope §6 khối `[!CAUTION]` |
| **V**aluable | **Hai lớp — xem §4.2** | |
| **E**stimable | Estimable bằng **giờ-người**, không bằng story point — xem §4.3 | `[SRC]` Glossary `HITL gate` |
| **S**mall | Trần theo **giờ-người** — xem §4.3 | |
| **T**estable | Testable = **checklist assertion nhị phân có cách đo** — xem §4.4 | `[SRC]` MVP-Scope §7 (*"đo được, không phải đánh giá chủ quan"*) |

### 4.2 (a) `Valuable` khi giá trị là *"về sau không phải migrate"*

Story PASS chuẩn `Valuable` nếu thoả **≥1** trong hai lớp, và **PHẢI khai rõ đang thoả lớp nào**:

| Lớp | Định nghĩa | Khuôn viết bắt buộc | Anchor |
|---|---|---|---|
| **`Valuable-U`** (user value) | Người dùng cuối **thấy** hoặc **nhận** được gì | `Là {actor}, tôi muốn {hành động} để {kết quả người dùng nhận được}` | Chuẩn User Story thường |
| ⭐ **`Valuable-I`** (irreversibility value) | Giá trị **không phải là tính năng**, mà là **chi phí không đảo ngược tránh được** | `Nếu KHÔNG làm ở {mốc}, thì {hậu quả cụ thể không đảo ngược được}` | `[SRC]` MVP-Scope NT-3 vế 2 + cột *"Không giữ thì hỏng thế nào"* của KC-1…KC-7 |

**Khuôn `Valuable-I` đã có mẫu sẵn trong repo — dùng lại, không sáng tác**: cột thứ năm của bảng MVP-Scope §6 chính là cột `Valuable-I` viết đúng cách. Ví dụ KC-5: *"Retrofit `tenant_id` vào schema đã có dữ liệu thật là một trong những migration đắt nhất tồn tại […] và **không có cách nào xác minh đã sửa hết**. Bỏ sót một chỗ = rò rỉ dữ liệu chéo tenant = **sự cố tồn vong**"* `[SRC]`.

**Ba luật cứng cho `Valuable-I`:**

| # | Luật |
|---|---|
| V1 | **CẤM để trống.** Story không khai được lớp nào ⇒ **không Ready**, không phải "Story hạ tầng nên miễn" |
| V2 | **CẤM** các cụm *"để code sạch hơn"*, *"để dễ maintain"*, *"để đúng best practice"*. Đó **không phải** `Valuable-I` — chúng đều đảo ngược được. `Valuable-I` phải nêu **thứ mất vĩnh viễn** hoặc **migration cụ thể phải chạy** |
| V3 | Story khai `Valuable-I` **phải** trích được ≥1 trong: `KC-1…KC-7`, `NT-3`, hoặc một hàng `Roadmap §6.2` có `Loại phụ thuộc = Cứng và một chiều` `[SRC]` |

**Vì sao lớp này bắt buộc tồn tại**: trong horizon, `MVP1` gồm `tenant_id` + RLS, 5 hạng mục provenance, opt-out Điều 37b, sửa khoá thời gian, `usage_event` — **không hạng mục nào trong số này người dùng cuối thấy được**, nhưng cả năm đều là điều kiện chặn cứng `[SRC]` Roadmap §2 hàng MVP1 + §6.2. Ép chúng vào khuôn `As a user…` sẽ sinh ra **actor giả** — và một actor giả trong Story là một mệnh đề không kiểm chứng được.

### 4.3 (b) `Small` neo vào **GIỜ-NGƯỜI**, không story point, không ngày công

**Quyết định**: neo vào **giờ-người**, và tách thành **hai** đại lượng.

| Đại lượng | Định nghĩa | Trần | Vượt trần thì làm gì |
|---|---|---|---|
| **`E_build`** | Giờ-người **Founder** để implement, gồm cả thời gian điều phối AI agent | **≤ 16 giờ-người** ⚠️ `[EM]` | **Split Story.** Không xin ngoại lệ |
| **`E_hitl`** | Giờ-người **người** phải bỏ ra **mỗi lần chạy / mỗi chapter** để đi qua HITL gate mà Story này tạo ra hoặc tiêu thụ | **≤ 2 giờ-người/chapter** ⚠️ `[EM]` | ⛔ **KHÔNG split được** — split không giảm nghĩa vụ lặp lại. Phải **escalate cho Founder**: Story đang tạo ra nghĩa vụ vận hành **vĩnh viễn** cho người duy nhất trong đội |

**Vì sao giờ-người, không phải story point / ngày công:**

| # | Lý do | Anchor |
|---|---|---|
| 1 | ⭐ **Glossary định nghĩa thẳng**: *"HITL gate […] Đơn vị đo của nó là **giờ-người, không phải token** — và với một người làm một mình, **đây mới là ràng buộc thật**, không phải chi phí API"* | `[SRC]` Glossary term `HITL gate` |
| 2 | **Story point cần velocity để dịch ra thời gian. Velocity không tồn tại**: chưa có sprint nào chạy, *"chưa có dòng code nào"* | `[SRC]` MVP-Scope §1.2 CF-1.3 |
| 3 | **Không có hệ số hiệu chỉnh**: *"Hệ số AI assist chưa biết […] `TBD`. **Không được dùng 'có AI nên nhanh hơn' làm lý do rút ngắn lịch**"* | `[SRC]` Roadmap §1.3 |
| 4 | **Ngày công che mất phần đắt nhất**: Charter A8 — speaker attribution lỗi 30–50% ⇒ human gate *"chuyển từ 'kiểm tra' sang 'làm lại từ đầu' — và đúng vào **ràng buộc thật của dự án là giờ-người**"* | `[SRC]` Charter §8 A8 |

⚠️ **Cả hai trần là `[EM]` do em định nghĩa, không có nguồn ngoài.**
- **16 giờ-người**: neo mềm vào thời lượng **duy nhất** có nguồn trong toàn bộ CF — MVP0 = **1–2 tuần** (CF-8.4) `[SRC]` Roadmap §1.2 bước 1 — chia thành ~8–12 Story. `[EM]`
- **2 giờ-người/chapter**: **placeholder, không có căn cứ.** Nó **phải được hiệu chỉnh bằng số đo thật của MVP0**: `G1-c` human-reject rate sau VLM-select (`≤30%` PASS / `30–50%` có điều kiện / `>50%` FAIL) `[SRC]` MVP-Scope §7.2. Trước khi MVP0 chạy, đừng đối xử với con số này như một ngưỡng.

### 4.4 (c) Khuôn Acceptance Criteria — **CHECKLIST**, không Gherkin

> **CHỌN: checklist `- [ ]`.** Không dùng Gherkin `Given/When/Then` cho bất kỳ Story nào của run này.

**Ba lý do, cái thứ nhất là quyết định:**

| # | Lý do | Anchor |
|---|---|---|
| 1 | ⭐ **Exit criteria trong repo ĐÃ ở dạng checklist assertion, không ở dạng Gherkin.** Ví dụ `M2-2`: *"≤3 nhân vật/panel là CHECK constraint ở tầng DB — đo bằng: **insert panel 4 nhân vật bị từ chối, không phải bị cảnh báo**"*; `M1-1`: *"test rò rỉ chéo tenant PASS (query của tenant A không trả về 1 row nào của tenant B)"*. Bọc chúng vào `Given/When/Then` **thêm ngữ pháp mà không thêm một bit thông tin** — và làm mất khả năng đối chiếu 1:1 giữa AC của Story và exit criterion của mốc | `[SRC]` Roadmap §2 cột *Điều kiện ra* |
| 2 | **Gherkin có giá khi nó là contract GIỮA BA BÊN** (BA ↔ QA ↔ dev). Ở đây Founder là **A** ở cả 9 hàng RACI, không có ranh giới đó tồn tại | `[SRC]` Charter §6 + Glossary `bus factor` = 1 |
| 3 | **Story hạ tầng không có actor**: `tenant_id NOT NULL trên mọi bảng` viết theo Gherkin buộc phải bịa ra một actor. Actor giả ⇒ AC không kiểm chứng được | `[PO]` |

**Khuôn AC bắt buộc — đúng 4 khối, đúng thứ tự này:**

| Khối | Heading trong Story | Nội dung | Rỗng được không |
|---|---|---|---|
| **AC-1** | `### Xác minh được` | Mỗi dòng `- [ ]` = **một** assertion **nhị phân**, và **cách đo ghi ngay trong dòng đó** (mượn cột *Cách đo* của MVP-Scope §7) | ❌ **≥1 dòng** |
| **AC-2** | `### Đường không hạnh phúc (unhappy path)` | ≥1 dòng `- [ ]` cho **failure mode / edge case / race condition**. Đây là chỗ ép edge case mà không cần Gherkin | ❌ **≥1 dòng.** Rỗng ⇒ **không Ready** |
| **AC-3** | `### Ràng buộc cứng không được vi phạm` | Trích ID: `KC-x` / `C-x` / `AG-x`. Không có thì ghi `—` | 🟡 ghi `—` được |
| **AC-4** | `### Story này KHÔNG làm` | Chống scope creep. Mượn đúng khuôn cột *"KHÔNG trả lời"* của MVP-Scope §1.1 | ❌ **≥1 dòng** |

**Luật viết dòng AC-1** — mỗi dòng phải **thất bại được**: *"insert panel 4 nhân vật bị từ chối"* là AC hợp lệ; *"schema hỗ trợ giới hạn nhân vật"* là **không hợp lệ** (không có cách nào chứng minh sai). `[PO]`, khuôn mượn `[SRC]` MVP-Scope §7.1 (*"tiêu chí là **sự tồn tại của một artifact** + phân loại nhị phân […] Không có chỗ nào cho 'cảm thấy ổn'"*).

### 4.5 (d) Definition of Ready — 5 mục, tối thiểu

Story chưa đủ 5 mục ⇒ **không được đưa vào `Active-Sprint/`**.

| # | DoR | Kiểm bằng gì | Anchor |
|---|---|---|---|
| **R1** | Có **anchor**: ≥1 hạng mục `MVP-Scope §3` **VÀ** ≥1 exit criterion `Roadmap` | Cột `Anchor` của bảng backlog không trống | `[SRC]` `brief.md` Assumption #2 (*"mọi requirement phải truy được về một mục cụ thể"*) |
| **R2** | `Valuable` đã **khai lớp** (`Valuable-U` hay `Valuable-I`); nếu `Valuable-I` thì nêu **hậu quả không đảo ngược cụ thể**, thoả V1–V3 | Đọc mục Valuable của Story | §4.2 |
| **R3** | `E_build ≤ 16` giờ-người **VÀ** `E_hitl ≤ 2` giờ-người/chapter — hoặc có **lý do vượt trần ghi thành văn** | Đọc **trực tiếp cột 11 + 12** của bảng backlog | §4.3 |
| **R4** | AC đủ **4 khối**; `AC-2` (unhappy path) có **≥1 dòng**; `AC-4` có **≥1 dòng** | Đếm heading + đếm dòng `- [ ]` | §4.4 |
| **R5** | Không vi phạm `AG-1…AG-8` (OKRs §6) **VÀ** không nằm trong ô `❌ cắt hẳn` của MVP-Scope §3 (`C4`, `D6`, `E6`) | Đối chiếu 2 danh sách | `[SRC]` OKRs §6 · MVP-Scope §3 |

### 4.6 (d) Definition of Done — 5 mục, tối thiểu

| # | DoD | Đo bằng gì | Anchor |
|---|---|---|---|
| **D1** | **Mọi** dòng `- [ ]` của AC-1 và AC-2 đã tick, **kèm bằng chứng** ghi cạnh dòng đó (số đo, output, hoặc **tên test**) | Không có bằng chứng ⇒ chưa Done. *"Thiếu dữ liệu không phải bằng chứng tốt"* | `[SRC]` MVP-Scope §7.3 (G2 `KHÔNG CHẠY ĐƯỢC`) · OKRs §1.3 |
| **D2** | Story chạm ≥1 trong `KC-1…KC-7` ⇒ **có test chứng minh**, không phải có code | Mẫu đã có: `M1-5` yêu cầu *"**test** chứng minh chúng commit CÙNG MỘT transaction với artifact"* | `[SRC]` Roadmap §2 hàng MVP1 |
| **D3** | Story tạo/đổi dữ liệu do người dùng tác động ⇒ **có `change_log` row sinh ra** — *"kể cả hành động chỉ là 'chọn ảnh này thay vì ảnh kia'"* | Test/kiểm tay 1 hành động | `[SRC]` MVP-Scope §5.2 khối ràng buộc xuyên suốt + KC-2 |
| **D4** | Story **không làm lùi** exit criterion nào đã đạt của mốc hiện tại | Đối chiếu danh sách `P-x`/`M1-x`/`M2-x` đã tick | `[SRC]` Roadmap §2 |
| **D5** | Cập nhật `Stories-MOC.md` **VÀ** hàng tương ứng trong `Backlog-Priority.md` | RULE-001 quy tắc #4: *"BẮT BUỘC cập nhật file MOC tương ứng"* | `[SRC]` RULE-001 |

### 4.7 ⛔ Cái em CỐ TÌNH bỏ — và vì sao

> Constraint của run: *không đề xuất một quy trình Scrum đầy đủ.* Bảng này là phần thực thi constraint đó, ghi thẳng thay vì im lặng.

| Bỏ | Lý do bỏ | Thay bằng gì |
|---|---|---|
| **Story point + planning poker** | Poker cần **≥2 người estimate độc lập**. Bus factor = 1 `[SRC]`. Một người "poker" với chính mình là nghi thức rỗng | `E_build` / `E_hitl` bằng **giờ-người** (§4.3) |
| **Velocity** | Cần ≥3 sprint lịch sử. Chưa có sprint nào; *"chưa có dòng code nào"* `[SRC]` CF-1.3 | Không thay. `TBD` cho tới khi có ≥10 Story đã Done có số thực đo |
| **Burndown / burn-up chart** | Vẽ trên velocity không tồn tại ⇒ **một đường dốc bịa**. Roadmap §1.3 đã tự khai *"không có ước lượng bottom-up"* `[SRC]` | Đếm exit criterion đã tick / tổng exit criterion của mốc — **đã có sẵn** ở Roadmap §2 |
| **4 sprint ceremony** (planning / daily standup / review / retro) | Founder là **A** ở cả 9 hàng RACI `[SRC]` Charter §6 ⇒ 4 buổi họp với chính mình | **Một** nhịp duy nhất: rà **cuối tháng** đã có ở OKRs §1.2 `[SRC]`. Không thêm nhịp |
| **Sprint goal / sprint commitment** | Đã có **exit criteria mốc** (Roadmap §2) và **KR** (OKRs §3). Thêm sprint goal = **nguồn sự thật thứ năm** | Không thay |
| **Sprint số (`Sprint-{NNN}.md`)** | Với 1 người, ranh giới sprint 2 tuần không tạo ra quyết định nào mà **ranh giới mốc** chưa tạo ra | Dùng **mốc** (`Pre-cycle/MVP0`…`MVP4`) làm đơn vị lập kế hoạch |
| **`Assignee` / story owner** | Bus factor = 1. Mọi Story cùng một owner ⇒ cột hằng số | Bỏ cột |
| **RICE score** | Mục 1.2 — cả tử số và mẫu số không tồn tại | `UNLOCK-ORDER` (Mục 1.4) |
| **MoSCoW label** | Mục 1.3 — trùng lặp và **lossy** so với MVP-Scope §3 | Cột `Scope-Label` **kế thừa** |

---

## Cảnh báo cho PM

| # | Cảnh báo | Mức | Ai quyết |
|---|---|---|---|
| **W1** | ⛔ **RULE-001 CHẶN CỨNG việc tạo `Backlog-Priority.md`.** *Prioritized Backlog* **không có** trong bảng *Document Type Mapping* — verified: khối `022-User-Stories` của bảng chỉ có **đúng 3 hàng** (`Epic` → `Epics/Epic-{Title}.md`, `User Story` → `Backlog/Story-{Title}.md`, `Active Story` → `Active-Sprint/Story-{Title}.md`), không hàng nào cho loại tài liệu này. Và quy tắc #7 ghi *"**KHÔNG ĐƯỢC** tạo tài liệu mà không kiểm tra bảng Ánh xạ trước"*. RULE-001 có `status: approved`. **Tiền lệ có sẵn**: comment nhật ký đầu RULE-001 ghi hàng `MVP Scope` được thêm **additive** và *"Được duyệt tại gate của run `2026-08-23`"* `[SRC]`. ⇒ Cần **một hàng additive** `Prioritized Backlog \| docs/022-User-Stories/ \| Backlog-Priority.md` được anh duyệt tại gate **trước** khi writer chạy | **Chặn** | ⚠️ **Anh chủ dự án.** PO không sửa được doc `approved` |
| **W2** | ⚠️ **Cấu hình em chốt LỆCH khỏi mô tả hạng mục #7 của `brief.md`** (*"Backlog đã sắp xếp ưu tiên (RICE/MoSCoW)"*). Em bác **cả hai** framework đó (Mục 1). Nếu anh vẫn muốn giữ chữ *RICE* hoặc *MoSCoW* trong tài liệu vì lý do ngoài kỹ thuật (trao đổi với người ngoài, quen thuộc), phải nói **trước** khi writer chạy — không phải sau | **Chặn hạng mục #7** | ⚠️ **Anh** |
| **W3** | **Open question #2 của `brief.md` chưa trả lời** (Story cho Full Scope hay chỉ horizon) **làm rỗng cột `#` (Rank)** cho MVP3/MVP4: rank *"trong một mốc"* vô nghĩa khi mốc đó **chưa có ngày và chỉ có 2 exit criterion** (`M4-1`, `M4-2`) `[SRC]` Roadmap §2. **Em đề xuất**: chỉ rank trong horizon (`Pre-cycle/MVP0`, `MVP1`, `MVP2`); Story `MVP3`/`MVP4` đưa vào H2 mục 5 *"Story chưa xếp được"* với `TBD` + lý do | **Chặn §3.2 + §3.3** | ⚠️ **Anh** |
| **W4** | **Open question #3 (Epic theo module A–G hay theo mốc MVP0–MVP4) đổi schema của em.** Nếu Epic cắt **theo mốc**, cột 3 (`Epic`) và cột 4 (`Mốc`) **trùng nhau** ⇒ dư một cột và mất khả năng biểu diễn *"một Epic trải nhiều mốc"* (đúng trường hợp `D1`, `GP-1`, `E1`). **Em đề xuất Epic theo module A–G**, khớp Assumption #3 của `brief.md` | **Chặn §3.3** | PO đề xuất → **Anh chốt** |
| **W5** | ⚠️ **Đường dẫn hạng mục #7 có thể sai TẦNG.** `Backlog-Priority.md` trả lời câu hỏi **trình tự** — cùng loại câu hỏi với `Roadmap.md` (tầng `010-Planning`), không cùng loại với `Story-{Title}.md` (tầng `022`). Đặt ở `022` là hợp lý về **quan hệ dữ liệu** (nó link tới Story) nhưng lệch về **loại câu hỏi**. `[PO]` — em **không** đề xuất đổi (đổi thì phá link của Stories-MOC), chỉ nêu để anh biết mình đang chọn gì khi duyệt W1 | Thông tin | **Anh**, cùng lúc với W1 |
| **W6** | ⚠️ **Chữ "MVP" trong "MVP Stories" NHẬP NHẰNG** và không giải được ở tầng PO: các **mốc** được đặt tên `MVP0`…`MVP4`, nên *"MVP Story"* có **hai nghĩa hợp lệ**: (a) Story thuộc **horizon** MVP0–MVP2, hay (b) Story thuộc **mọi** mốc `MVP*` gồm cả MVP3/MVP4 ngoài horizon. Em chọn **(a)** ở §3.4 và ghi rõ, nhưng đây là **câu hỏi gate**, không phải quyền của PO | **Chặn §3.4** | ⚠️ **Anh** |
| **W7** | ⛔ **Chỗ plan này SẼ vỡ — ước lượng do một người tự chấm cho chính mình.** `E_build`/`E_hitl` không có second estimator: Charter §6 hàng 6 ghi *"hiện chỉ có **một cặp mắt**, đây là khoảng trống đã biết"* `[SRC]`. Sai số sẽ **hệ thống theo một hướng** (lạc quan), không phải nhiễu ngẫu nhiên. **Không có cách chữa** trong đội một người. Cách rẻ nhất còn lại: **ghi số THỰC ĐO sau mỗi Story** cạnh số ước lượng; sau **~10 Story** mới có hệ số hiệu chỉnh. Đừng lập kế hoạch như thể hai cột này là dữ liệu — đúng cảnh báo `[EM]` của tầng Planning | **Rủi ro đã biết** | PO ghi lại, **anh chấp nhận** |
| **W8** | ⚠️ **Trần `E_hitl ≤ 2 giờ-người/chapter` là ngưỡng em BỊA RA, không có nguồn.** Nó chỉ có nghĩa **sau khi** MVP0 đo `G1-c` (human-reject rate sau VLM-select) `[SRC]` MVP-Scope §7.2. Trước MVP0: **placeholder**, không phải ngưỡng chặn. Nếu writer dùng nó để split/reject Story trước 09/2026, đó là dùng sai | **Rủi ro** | PO, hiệu chỉnh sau MVP0 |
| **W9** | **DoR R1 không thoả được cho phần lớn Story `MVP4`** vì `Roadmap` chỉ có **2** exit criterion cho MVP4 (`M4-1`, `M4-2`) `[SRC]`. ⇒ Nếu viết Story cho Full Scope, một khối lớn Story sẽ có `Anchor = TBD` **theo cấu trúc**, không phải do writer lười. Đây là lý do **thứ hai, độc lập** để giới hạn phạm vi Story trong horizon (W3) | **Chặn** cùng W3 | ⚠️ **Anh** |
| **W10** | **Em cố ý ghi đè role card của chính em** (*"Acceptance Criteria (Gherkin format)"*) bằng checklist, lý do ở §4.4. Nếu anh muốn giữ Gherkin, hệ quả phải biết trước: **mất đối chiếu 1:1** giữa AC của Story và exit criterion `M1-x`/`M2-x`/`G1-x` — vì các exit criterion đó **đã được viết ở dạng assertion**, không ở dạng `Given/When/Then` | Thông tin | **Anh** |
| **W11** | **Không có role memory cho `product-owner`** (`knowledge-base/45-Role-Memory/product-owner/` không tồn tại) và **không có `.agent/roles/product-owner.md`**. ⇒ Mọi preference PO của anh từ các run trước **không được kế thừa** vào lens này. Sau khi run này chốt, nên `/memo` để lần sau không phải quyết lại 4 thứ: framework, khuôn AC, đơn vị `Small`, và luật "Roadmap thắng" | Thông tin | PO đề xuất `/memo` |

---

## Tài liệu tham khảo

### Nguồn trong repo đã đọc và trích

| Tài liệu | Mục đã dùng |
|---|---|
| [MVP-Scope.md](../../../MVP-Scope.md) | §1.1 ranh giới ba tài liệu (khuôn Mục 2) · §1.2 CF-1.2/1.3 · §1.3 thứ tự mốc · §2 NT-1…NT-4 · §3 bảng + hệ nhãn `✅🟡⛔❌` · §3.1 · §4.1 · §5.1 cảnh báo mẫu số · §5.2 ràng buộc `change_log` · §6 KC-1…KC-7 · §7 G0/G1/G2 + G1-c/G1-d · §8 K1–K5 |
| [Roadmap.md](../../../Roadmap.md) | §1.1 · §1.2 CF-8.13 (horizon không chứa MVP3) · §1.3 (`TBD` bottom-up, hệ số AI assist) · §2 bảng lộ trình + exit criteria `P-x`/`M1-x`/`M2-x`/`M3-x`/`M4-x` · §4 X-a/X-b/X-c · §5.1 · §6.2 bảng phụ thuộc · §6.3 đường găng |
| [OKRs.md](../../../OKRs.md) | §1.1 (tự mô tả + luật *"KR đó sai, không phải Roadmap sai"*) · §1.2 nhịp review · §1.3 ba trạng thái chấm · §6 AG-1…AG-8 |
| [Charter-Comic-Studio.md](../../../Charter-Comic-Studio.md) | §6 RACI + ba lỗ hổng (bus factor = 1, một cặp mắt) · §7 C1–C10 · §8 A6–A12 |
| [Glossary.md](../../../../999-Resources/Glossary.md) | `HITL gate` (giờ-người) · `MVP0` · `vertical slice` · `anti-goal` · `Go/No-Go gate` · `bus factor` · `RACI` |
| [Documents-Template.md](../../../../../knowledge-base/99-Templates/Documents-Template.md) (RULE-001) | Quy tắc #3/#4/#5/#7 · Document Type Mapping · Linking Rules · Frontmatter |
| [brief.md](../brief.md) | Hạng mục #7 · Triage Q2/Q3 · Assumptions #2/#3/#4/#5 · Open questions #2/#3/#4/#5 |

### Nguồn KHÔNG tồn tại (verified, ảnh hưởng tới độ tin của lens)

| Đường dẫn | Trạng thái |
|---|---|
| `.agent/roles/product-owner.md` | **Không tồn tại** — Glob `.agent/roles/*` trả về 0 file |
| `knowledge-base/45-Role-Memory/product-owner/` | **Không tồn tại** — Glob trả về **10 role / 13 file** (architect, business-analyst, context-auditor, devops-engineer, product-designer, product-manager, quality-assurance, researcher, senior-ai-engineer, software-engineer), **không có `product-owner`** |
| Template cho *Prioritized Backlog* | **Không tồn tại** trong `knowledge-base/99-Templates/` ⇒ Mục 3 là contract duy nhất |
