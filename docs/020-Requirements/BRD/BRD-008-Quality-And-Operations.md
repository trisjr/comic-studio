---
id: BRD-008
type: brd
status: draft
project: comic-studio
created: 2026-08-24
---

# 🧪 BRD-008 — Chất lượng & vận hành

> [!IMPORTANT]
> Module này là **phương tiện đo** của cả dự án. Nó không tạo ra tính năng người dùng thấy (trừ `H4`), nó tạo ra **khả năng biết mình đang đi đúng hay sai**. Đây cũng là nhóm **đã bị bỏ sót** khỏi cách brief mô tả `MVP-Scope §3` (*"7 module A–G"*) — tài liệu nguồn vốn có **TÁM** nhóm; nhóm `H` được đưa trở lại tại gate của run. Xem [`findings/business-analyst.md` §1.2](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md).

## Mục lục

1. [Business goal](#1-business-goal)
2. [Phạm vi module](#2-phạm-vi-module)
3. [Yêu cầu nghiệp vụ](#3-yêu-cầu-nghiệp-vụ)
4. [Ràng buộc & điều kiện chặn](#4-ràng-buộc--điều-kiện-chặn)
5. [Cái module này KHÔNG làm](#5-cái-module-này-không-làm)
6. [Rủi ro chính](#6-rủi-ro-chính)
7. [Tài liệu liên quan](#7-tài-liệu-liên-quan)
8. [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## 1. Business goal

**Làm cho mọi thay đổi về sau *đo được*: HITL gate, eval kit, golden dataset, preference data, export, abuse control.**

> **Không có nhóm này thì mọi thay đổi prompt/model là *thay đổi mù*.**

Ba hệ quả trực tiếp của phát biểu đó, mỗi hệ quả là lý do một hàng `H` tồn tại:

| # | Vì sao goal này chịu lực | Căn cứ |
|---|---|---|
| 1 | `H1` (HITL gate + eval kit) **chính là điều kiện khả thi `R9`** trong CHÍN điều kiện phải thoả đồng thời của dự án. Không có nó ⇒ *"không có vòng phản hồi người trong 3 milestone; preference data (moat thật) không được ghi từ đầu"* | [`Charter` §4 `R9`](../../010-Planning/Charter-Comic-Studio.md#4-yêu-cầu-cấp-cao) |
| 2 | `H2` (preference data) là **moat thật** — *"một khoản đầu tư, trả hai lần"*. Luận điểm moat gốc (5 thành phần kiến trúc) đã bị bác là *barrier to entry*, không phải moat; thứ còn lại là **dữ liệu preference tích luỹ** | [`Analysis` §12](../../050-Research/Analysis-Comic-Studio-Concept.md) |
| 3 | `H4` (export) là *"thứ **duy nhất** trong MVP4 người dùng thật sự nhận được"* (CF-8.10) ⇒ ưu tiên **được nâng lên sớm**, và trở thành **điều kiện doanh thu** của Tầng 1 | [`MVP-Scope` §3 `H4`](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope) · [`Roadmap` §5.2](../../010-Planning/Roadmap.md#52--hệ-quả-tích-cực-thứ-có-thể-bán-được-trong-horizon) |

Và một hệ quả gián tiếp nhưng là **thứ duy nhất bắt được loại lỗi mà hệ thống không tự thấy**: cạnh mọi metric kỹ thuật phải có **đúng một câu người trả lời** — *"trang này đọc có ổn không?"* Lỗi *"pass mọi check mà không ai muốn đọc"* là **vô hình đối với chính hệ thống** — Continuity Checker không bắt được, không metric kỹ thuật nào bắt được ([`Analysis` §3.2](../../050-Research/Analysis-Comic-Studio-Concept.md), đoạn *"→ Sửa cái gì"*).

---

## 2. Phạm vi module

Bao **6 hàng** nhóm `H. Chất lượng & vận hành` của [`MVP-Scope` §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope). Nhãn từng mốc **copy nguyên vẹn bảng gốc**, kể cả phần chú thích trong ô (`🟡 VLM select`, `🟡 preview server-side` — làm phẳng một `🟡 có điều kiện` thành `🟡` trơn là mất nghĩa).

**Ký hiệu**: ✅ có đầy đủ · 🟡 có một phần / bản tối thiểu · ⛔ hoãn sang mốc sau · ❌ **cắt hẳn, không có trong Full Scope**

| # | Hạng mục | MVP0 | MVP1 | MVP2 | MVP3 | MVP4 | Full Scope | Căn cứ (bảng gốc) |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|
| `H1` | HITL gate + eval kit | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | CF-8.7 — **ngay tại MVP1, không dồn MVP4** |
| `H2` | Log preference data (moat thật) | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | CF-8.7 · `Analysis` §12 — *"một khoản đầu tư, trả hai lần"* |
| `H3` | Continuity Checker dạng **N-candidate selection** (không phải flag+autofix) | 🟡 VLM select | ⛔ | ⛔ | 🟡 | ✅ | ✅ | CF-8.10 · CF-6.11 độ phủ **40–60% số panel** `[EM]` — **phải nói rõ với user** |
| `H4` | Export PDF / CBZ / webtoon | ❌ | ⛔ | 🟡 preview server-side | ✅ | ✅ | ✅ | CF-8.10 — *"thứ **duy nhất** trong MVP4 người dùng thật sự nhận được"* ⇒ kéo lên sớm |
| `H5` | Abuse controls tối thiểu (rate limit/tenant, giới hạn upload, log provider từ chối) | ❌ | 🟡 | ✅ | ✅ | ✅ | ✅ | `Analysis` §5.7 — tín hiệu abuse sớm gần như miễn phí |
| `H6` | Golden dataset regression (15–20 panel có spec + ref + ảnh + đánh giá) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | `findings/architect.md` §7.3 điểm 4 — tài sản dùng suốt vòng đời |

**Bốn điều phải đọc ra từ bảng này:**

| Quan sát | Nghĩa vận hành |
|---|---|
| `H6` là **hàng duy nhất `✅` ở MỌI mốc**, kể cả MVP0 | Golden dataset **không phải deliverable của một mốc** — nó là tài sản xuyên vòng đời. Nó là đầu vào của mọi phép đo về sau |
| `H1` là `✅` **ngay MVP1** | Không phải hạng mục MVP4. Xem [`Charter` §4 `R9`](../../010-Planning/Charter-Comic-Studio.md#4-yêu-cầu-cấp-cao) |
| `H3` chỉ `✅` ở **MVP4** — mốc **NGOÀI horizon** 09/2026–02/2027 | Trong horizon chỉ có `🟡 VLM select` của MVP0. ⚠️ Kết luận horizon là `[EM]` (CF-10.8) — *"ước lượng của em tại run này"*, không có nguồn CF nào xác nhận |
| `H5` ở MVP1 là `🟡` — **nhưng `🟡` đó không đồng nhất** | ⚠️ [`Roadmap` §4 `X-b`](../../010-Planning/Roadmap.md#4-ba-việc-xen-ngang) lưu ý phạm vi: *"**abuse control cho upload thì cần ngay ở MVP1**"* (giới hạn dung lượng/số upload, rate limit per tenant). Phần credit-ledger/hard-quota của `X-b` mới là MVP3 và **không thuộc BRD này** |

### 2.1 ⛔ `H3` Continuity Checker — thuật ngữ dễ dùng sai nhất của cả repo

> [!CAUTION]
> **`Glossary.md` ghi: *"Mọi tài liệu mới phải dùng nghĩa sau."*** `CẤM-12` của [`findings/business-analyst.md` §5.3](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md): **cấm viết Continuity Checker theo nghĩa cũ.**

| | |
|---|---|
| **Nghĩa ĐÚNG, DUY NHẤT** | **QA-based selection giữa N candidate** — trả lời câu *"trong N cái này, cái nào consistent hơn"* |
| **Nghĩa SAI, ĐÃ BỊ BÁC** | *"Gắn nhãn ✓/✗ từng attribute rồi autofix"* — cơ chế này **chưa được validate** và có **FP profile xấu** |
| **Nguồn** | [`Glossary` — *Continuity Checker*](../../999-Resources/Glossary.md#sinh-ảnh--kiểm-tra-nhất-quán) (*"định nghĩa đã được sửa lại"*) · CF-8.10 |

**Vì sao định nghĩa phải là selection chứ không phải detection** — đây là lập luận, không phải sở thích diễn đạt:

**VLM autorater** đã được validate ở **pairwise ranking** (MIE đạt **0.922** accuracy so với human preference), **CHƯA** được validate ở **absolute per-panel detection** ([`Glossary` — *VLM autorater*](../../999-Resources/Glossary.md#sinh-ảnh--kiểm-tra-nhất-quán)). Hai câu hỏi khác nhau: *"trong N cái này, cái nào hơn?"* có số; *"panel này đúng hay sai?"* thì không. Đặt checker vào câu thứ hai là đặt nó vào một task chưa ai chứng minh nó làm được.

**Lý do gốc sâu hơn: một vòng lặp logic.** Bài toán chặn là **re-identification** — *"nhân vật nào trong panel này là nhân vật X"*. Muốn kiểm trang phục của X thì **trước tiên phải giải re-identification** — **chính bài toán mà checker được lập ra để giải**. Panel nhiều nhân vật về cơ bản **không kiểm được** bằng checker vì lý do này ([`Glossary` — *re-identification*](../../999-Resources/Glossary.md#sinh-ảnh--kiểm-tra-nhất-quán)).

**Hai con số bắt buộc đi kèm khi nói về `H3`:**

| Con số | Nhãn | Nghĩa vụ khi trích |
|---|---|---|
| Độ phủ **40–60% số panel** (CF-6.11) | ⚠️ `[EM]` — **ước lượng, KHÔNG phải số đo** | **PHẢI nói rõ với user** — *"đừng để họ hiểu là được bảo vệ toàn diện"*. Giấu = lời hứa sản phẩm không giữ được. Là exit criterion `M4-2` |
| MIE **0.922** pairwise accuracy | `[OFF]` | Chỉ được trích cho **pairwise ranking**. Trích nó để biện minh cho absolute per-panel detection là **trích sai phạm vi** |

### 2.2 ⛔ `best-of-N` KHÁC `retry-on-failure`

> [!WARNING]
> **`best-of-N` (N=3) chạy trên MỌI panel như MẶC ĐỊNH**, không phải chỉ khi panel lỗi. *"Performance saturates at N=3"* `[OFF]` (CF-3.1/CF-3.2). **Nhầm hai khái niệm này là nguồn của sai số chi phí +50%.**
>
> `CẤM-03`: **cấm lấy chất lượng của N=3 mà tính chi phí của N=2.** Hạ N là đổi chất lượng lấy margin ⇒ **phải chạy lại `G1`**, không phải chỉ `G2`.
>
> Nguồn: [`Glossary` — *best-of-N (N=3)*](../../999-Resources/Glossary.md#sinh-ảnh--kiểm-tra-nhất-quán) · [`Charter` §7 `C8`](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints) · `MVP-Scope` §7.3 số nền a.

Liên hệ trực tiếp tới `H3`: `H3` **tiêu thụ** N candidate mà `best-of-N` sinh ra. Đó là lý do `H3` là **selection giữa các candidate đã có**, không phải một lớp detection chạy thêm — và cũng là lý do chi phí của `H3` không được nhìn như "chi phí của một tính năng QA", mà là chi phí VLM call để score N candidate (một thành phần mà CF-3.5 ghi rõ là **chưa** có trong con số sàn chi phí/chapter).

---

## 3. Yêu cầu nghiệp vụ

> [!NOTE]
> Đây là **yêu cầu nghiệp vụ**, không phải Master Test Plan. Mỗi hàng phát biểu *"phải có X đo được"*, **không** phát biểu *"X gồm mấy bước"*. Thiết kế test case / test strategy thuộc tầng `docs/035-QA/` và **ngoài scope run này**.
>
> **Mọi yêu cầu đều có căn cứ.** Chỗ nào repo không có số, ghi `TBD` kèm lý do — **không tự gán chỉ tiêu chất lượng**.

| ID | Phát biểu | Căn cứ (file + mục) | Mốc MVP |
|---|---|---|---|
| **BR-008-01** | Hệ thống **phải có HITL gate** — điểm trong pipeline bắt buộc có người xác nhận trước khi đi tiếp — **có mặt từ MVP1**, *"ngay tại MVP1, không dồn MVP4"* | `MVP-Scope` §3 hàng `H1` (CF-8.7) · `Charter` §4 `R9` · `Glossary` *HITL gate* | **MVP1** |
| **BR-008-02** | Đơn vị đo tải của HITL gate **phải là giờ-người, KHÔNG phải token**. Với một người làm một mình, **đây mới là ràng buộc thật, không phải chi phí API** ⇒ mọi quyết định thiết kế gate phải nêu được tải review nó tạo ra | `Glossary` *HITL gate* · `Charter` §7 `C1` (đội **1 người + AI assist**) · `Analysis` §12 (*"ràng buộc thật là giờ-người, không phải đô-la"*) | **MVP1**, liên tục |
| **BR-008-03** | Thiết kế HITL gate ở MVP1 **phải chịu được tải review cao hơn dự kiến** nếu `G1` kết luận **PASS CÓ ĐIỀU KIỆN** ở tiêu chí `G1-c` — nhánh này được `MVP-Scope` chỉ định tên đích danh `H1` | `MVP-Scope` §7.2 bảng *Kết luận gate*, nhánh PASS CÓ ĐIỀU KIỆN | **MVP1** (phụ thuộc kết quả `G1`) |
| **BR-008-04** | Hệ thống **phải có eval kit chạy được trên golden dataset của MVP0 và cho ra số** | `Roadmap` §2 exit criterion **`M1-6`** (nguyên văn) | **MVP1** |
| **BR-008-05** | Eval trên golden set **phải chạy theo nhịp hàng tuần** — đây là cách **DUY NHẤT** phát hiện **silent model drift**, vì theo định nghĩa nó **không ném lỗi** | `Risk-Register` §5.2 hàng *Hàng tuần* (`R-22`) | từ **MVP1**, liên tục |
| **BR-008-06** | **Golden dataset 15–20 panel** — có **spec + ref + ảnh + bảng chấm** — phải **tồn tại dưới dạng file** từ pre-cycle/MVP0, và được giữ ở trạng thái dùng được ở **mọi** mốc về sau | `MVP-Scope` §3 hàng `H6` (`✅` ở **mọi** mốc) · `Roadmap` §2 exit criterion **`P-6`** | **MVP0** → mọi mốc |
| **BR-008-07** | **Mọi lần người dùng chấp nhận / từ chối một gợi ý phải được ghi làm preference data**, từ MVP1 — thu bằng **đúng cơ chế mà luật đã buộc phải có** (`change_log` / `field_provenance`) | `MVP-Scope` §3 hàng `H2` (CF-8.7) · `Glossary` *preference data* · `Analysis` §12 · `MVP-Scope` §6 `KC-2`, `KC-3` | **MVP1** |
| **BR-008-08** | Cạnh mọi metric kỹ thuật **phải có đúng một câu người trả lời** — *"trang này đọc có ổn không?"* — và câu trả lời **phải được GHI LẠI, từ MVP0** | `Analysis` §3.2 đoạn *"→ Sửa cái gì"* (CF-10.10) | **MVP0**, liên tục |
| **BR-008-09** | Continuity Checker **phải hoạt động ở dạng N-candidate selection**, trả lời *"trong N cái này cái nào consistent hơn"* — **không phải** flag ✓/✗ + autofix | `MVP-Scope` §3 hàng `H3` (CF-8.10) · `Roadmap` §2 exit criterion **`M4-1`** · `Glossary` *Continuity Checker* · `CẤM-12` | **MVP4** (`🟡 VLM select` ở MVP0) — **ngoài horizon** |
| **BR-008-10** | Độ phủ của checker **phải được công bố với user** đúng mức **40–60% số panel** ⚠️ `[EM]` — *"đừng để họ hiểu là được bảo vệ toàn diện"* | CF-6.11 ⚠️ `[EM]` · `Charter` §8 `A9` · `Roadmap` §2 exit criterion **`M4-2`** | **MVP4** |
| **BR-008-11** | Hệ thống **phải export ra PDF của 1 chapter hoàn chỉnh** từ preview server-side | `MVP-Scope` §3 hàng `H4` (CF-8.10) · `Roadmap` §2 exit criterion **`M2-5`** | **MVP2** (PDF) |
| **BR-008-12** | Export **phải đủ định dạng** PDF / CBZ / webtoon ở MVP3 — vì đây là *"thứ **duy nhất** trong MVP4 người dùng thật sự nhận được"*, ưu tiên **được nâng lên sớm** | `MVP-Scope` §3 hàng `H4` (CF-8.10) | **MVP3** |
| **BR-008-13** | Export **phải được đối xử như điều kiện doanh thu, không phải tính năng editor**: Tầng 1 bán được (`$4–8/tháng`, **KHÔNG image gen**) ≈ MVP1 + MVP2 + **export** ⇒ thiếu export thì Tầng 1 không bán được | `Roadmap` §5.2 (⚠️ nhãn `[EM]`, và là **một LỰA CHỌN, không phải kế hoạch đã chốt** — cần Founder quyết tại `G2`) · CF-10.9 | **MVP2** |
| **BR-008-14** | **Abuse control cho upload phải có ngay ở MVP1**: giới hạn dung lượng / số upload, **rate limit per tenant** | ⚠️ `Roadmap` §4 `X-b` **lưu ý phạm vi** (nguyên văn: *"abuse control cho upload thì cần ngay ở MVP1"*) | **MVP1** |
| **BR-008-15** | Hệ thống **phải log mọi lần provider từ chối** request — tín hiệu abuse xuất hiện sớm khi nó **gần như miễn phí** | `MVP-Scope` §3 hàng `H5` · `Analysis` §5.7 | **MVP1** (`🟡`) → **MVP2** (`✅`) |

### 3.1 `H2` preference data — *"một khoản đầu tư, trả hai lần"*, và liên kết ba chiều

`BR-008-07` là hàng có tỉ lệ giá-trị/chi-phí cao nhất của cả BRD này, vì nó **trả ba lần trên một lần đầu tư**:

| Chiều | Nó là gì ở chiều này | Căn cứ |
|---|---|---|
| **① Eval** | **Nguồn DUY NHẤT cho eval của tầng thẩm mỹ.** Tầng thẩm mỹ (*"trang này đọc có ổn không"*) không có metric kỹ thuật nào đo được ⇒ không có preference data thì tầng này **không có eval nào cả** | `Glossary` *preference data* · `Analysis` §3.2 |
| **② Moat** | **Nguyên liệu của moat thật.** Luận điểm moat gốc (5 thành phần) đã bị bác là *barrier to entry* và concept đã public trên arXiv; thứ còn đứng là **dữ liệu preference tích luỹ** | `Analysis` §12 |
| **③ Compliance** | Được thu bằng **đúng cơ chế mà luật đã buộc phải có**: `change_log` ghi **mọi** hành động người dùng — *kể cả "chọn generation X thay vì Y"* — và `field_provenance` ở mức field. Đây là `KC-2` + `KC-3`, hai mục trong **bảy mục không được cắt** | `MVP-Scope` §6 `KC-2`, `KC-3` · `Glossary` *`field_provenance` / `change_log`* |

> [!IMPORTANT]
> **Liên kết ba chiều này là lý do `H2` gần như miễn phí.** Cơ chế ghi (`change_log`, `field_provenance`) **đã bắt buộc phải có** vì `KC-2`/`KC-3`; `H2` chỉ thêm việc **đọc dữ liệu đó theo góc preference**. Nhưng nó chia chung một tính chất chết người với `KC-1`–`KC-4`: **không backfill được.** *"Gần như miễn phí, nhưng không ghi từ đầu thì mất dữ liệu giai đoạn đầu."*
>
> ⚠️ **BRD-008 KHÔNG sở hữu schema** của `change_log`/`field_provenance` — xem [mục 5](#5-cái-module-này-không-làm).

---

## 4. Ràng buộc & điều kiện chặn

### 4.1 `KC-x` của `MVP-Scope` §6 mà module này chạm

[`MVP-Scope` §6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) là **danh sách duy nhất trong tài liệu đó không mở ra thương lượng scope**. Module `H` chạm **hai** mục, và chạm ở vai trò **người tiêu thụ**, không phải người sở hữu:

| `KC` | Module `H` chạm thế nào | Ai sở hữu |
|---|---|---|
| **`KC-2`** `change_log` ghi **mọi** hành động người dùng, kể cả *"chọn generation X thay vì Y"* | Đây **chính là** cơ chế thu preference data của `BR-008-07`. Hành động *"chọn X thay vì Y"* vừa là bằng chứng `Điều 5a`, vừa là một nhãn preference | BRD-004 (editor) + BRD-007 (compliance) |
| **`KC-3`** `field_provenance` (mức field) + `generation.origin` | Là chiều thứ hai của cùng cơ chế — cho biết **phần nào do người**, tức nhãn preference gắn vào đúng chỗ | BRD-004 + BRD-007 |

> ⚠️ `KC-4` (cả ba commit **cùng một transaction**) là **thuộc tính của cơ chế**, không phải yêu cầu của BRD-008 — nhưng nó là điều kiện để dữ liệu preference của `H2` **đáng tin**: *"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng."*

### 4.2 `C-x` của `Charter` §7

| `C` | Nội dung | Ràng buộc nó đặt lên module này |
|---|---|---|
| **`C1`** | **Đội 1 người + AI assist. Không funding, không ngân sách marketing** `[CHỐT]` | Ràng buộc **quyết định nhất** của BRD này. Mọi HITL gate, mọi vòng review, mọi lần chấm golden set đều tiêu **giờ của người duy nhất trong đội**. Đây là lý do `BR-008-02` tồn tại |
| **`C8`** | **N = 3 là mặc định cho MỌI panel** (best-of-N), **KHÔNG phải retry-on-failure** `[OFF]` | `H3` là selection **giữa N candidate đã có**. Đọc `H3` như một lớp detection thêm vào là đọc sai cả cơ chế lẫn chi phí. Xem [mục 2.2](#22--best-of-n-khác-retry-on-failure) |
| **`C9`** | **Thứ tự milestone cố định** MVP0 → MVP1 → MVP2 → MVP3 → MVP4 | `H1` không được đẩy sang sau MVP1; `H6` không được đẩy sang sau MVP0. Không đảo thứ tự để *"làm phần dễ trước"* |
| **`C10`** | **Horizon 6 tháng CHƯA được ai xác nhận là đủ cho 1 dev** | ⛔ `CẤM-08`: **cấm nén lịch cho vừa khung.** `H3` (MVP4) rơi ra ngoài horizon và **được ghi ra như vậy**, không bị nhồi vào |

### 4.3 Liên hệ tới ba gate Go/No-Go — module này cấp **phương tiện đo** cho chúng

[`MVP-Scope` §7](../../010-Planning/MVP-Scope.md#7-gono-go-decision): ba gate là **ba cửa độc lập**, đo ba loại rủi ro khác nhau và **không thay thế được cho nhau** (CF-10.6). Vai trò của BRD-008 khác nhau ở từng cửa — nói rõ để không thổi phồng:

| Gate | Module `H` cấp phương tiện đo gì | Ranh giới phải nói thẳng |
|---|---|---|
| **`G1` — Kỹ thuật** (cuối 09/2026) | **`H6` golden dataset là dụng cụ đo của gate này.** Năm tiêu chí `G1` đều được chấm trên panel của MVP0, và bảng chấm của golden dataset là nơi kết quả được ghi. `G1-c` (human-reject rate sau VLM-select) là **phép đo đầu tiên của một con số CHƯA AI CÔNG BỐ** (`KT-8`) | ⚠️ Các **ngưỡng** của `G1` do writer run trước **định nghĩa tại run đó, không có nguồn ngoài** (CF-10.4 `[EM]`). BRD-008 **không** trích lại ngưỡng và **không** đặt ngưỡng mới — ngưỡng sống ở `MVP-Scope` §7.2 |
| **`G2` — Kinh tế** (cuối Q4/2026) | Eval kit + nhịp đo hàng tuần (`BR-008-04`, `BR-008-05`) làm cho kết quả `G2` **có dữ liệu để đọc**. `G2-a` ghi rõ: thiếu dữ liệu ⇒ gate **KHÔNG CHẠY ĐƯỢC**, không PASS mặc định | ⚠️ Số nuôi `G2-a` là **regen ratio p50/p90** từ `usage_event`/`usage_daily` — thuộc **BRD-006**, không phải BRD-008. Module này **không** sở hữu con số đó |
| **`G0` — Pháp lý** (trước dòng code **thương mại** đầu tiên) | Không có phép đo nào của `H` là đầu vào của `G0`. Liên hệ đúng là **một chiều khác**: `H2` dùng **đúng hạ tầng compliance** (`KC-2`/`KC-3`) mà `G0` quan tâm ⇒ hai thứ dùng chung một cơ chế | ⛔ `CẤM-10`: **`G0` chặn THƯƠNG MẠI HOÁ, KHÔNG chặn MVP0–MVP1.** Mọi hạng mục `H` ở MVP0/MVP1 (`H1`, `H2`, `H5`, `H6`) **không** chờ `G0`. Đọc ngược là *"cách hiểu nhầm đắt nhất"* (`Charter` §9.2) |

**Một quy tắc chung áp cho cả ba gate, và nó là ràng buộc của BRD này**: ⛔ `CẤM-16` — **cấm sửa ngưỡng gate sau khi nhìn thấy kết quả**, *"đó là cách một gate biến thành nghi lễ"*. Eval kit của `H1` phải làm cho việc **so kết quả với ngưỡng đã chốt trước** là việc rẻ; nó **không** được là nơi ngưỡng bị điều chỉnh cho vừa số đo.

### 4.4 Phụ thuộc chặn

| Cái này | Chặn cái kia | Loại | Nguồn |
|---|---|---|---|
| **Golden dataset của MVP0** (`H6`) | **Eval kit ở MVP1** (`M1-6`) | **MỀM** — *"có thể dựng lại, nhưng dựng lại tốn tiền API lần hai"* | [`Roadmap` §6.2](../../010-Planning/Roadmap.md#62-bảng-phụ-thuộc) |
| `KC-2`/`KC-3` có mặt trong schema MVP1 | Giá trị của preference data (`H2`) từ giai đoạn đầu | **CỨNG và một chiều** — không backfill được | `Roadmap` §6.2 · CF-7.3 `[OFF]` |
| Export/preview server-side hoàn thành ở MVP2 (`M2-5`) | Điều kiện bán Tầng 1 trong horizon | **CỨNG** theo `Roadmap` §5.2 — nhưng bản thân lựa chọn bán Tầng 1 là `[EM]` và cần Founder quyết tại `G2` | `Roadmap` §5.2 |

### 4.5 Khoảng trống chưa đóng được ⇒ `TBD`

| # | Khoảng trống | Vì sao là `TBD` |
|---|---|---|
| `TBD-1` | **Chỉ tiêu chất lượng của eval kit** (accuracy, coverage của chính bộ eval) | Repo **không có số**. `KT-8`: human-reject rate sau VLM-select **CHƯA AI CÔNG BỐ**; CANVAS không báo. Tự gán một con số ở đây là biến *"không biết"* thành *"đã đánh giá"* |
| `TBD-2` | **Tải giờ-người thật của HITL gate** (giờ/chapter) | `KT-3` + `KT-4`: **không có ước lượng bottom-up** (WBS/ETA) cho MVP1–MVP3, và **hệ số AI assist chưa đo được**. `Roadmap` §2 ghi cột thời lượng là **PHÂN BỔ, không phải ƯỚC LƯỢNG** |
| `TBD-3` | **Độ phủ THẬT của Continuity Checker** | `G-05` của `Risk-Register` §4.1: **40–60% là `[EM]`**, suy ra từ giới hạn re-identification trên art cách điệu, **không** từ một lần chạy có đối chứng. Đóng được một phần bằng phép đo human-reject rate ở MVP0 |
| `TBD-4` | **SLA / uptime của export** | Không nguồn nào trong repo đặt con số này. Không tự gán |

---

## 5. Cái module này KHÔNG làm

> [!CAUTION]
> Mục này **không được rỗng**. Với một module có tên *"Chất lượng & vận hành"*, ranh giới là thứ dễ trôi nhất — mọi thứ đều *"liên quan tới chất lượng"*.

| # | KHÔNG làm | Vì sao / thuộc về đâu |
|---|---|---|
| **1** | **KHÔNG viết test case, test strategy, hay Master Test Plan** | Thuộc tầng `docs/035-QA/` và **ngoài scope run này**. BRD phát biểu *"phải có eval kit đo được X"*, **không** phát biểu *"eval kit gồm 12 bước sau"* |
| **2** | ⛔ **KHÔNG làm Continuity Checker theo nghĩa cũ** — gắn nhãn ✓/✗ từng attribute rồi autofix | Cơ chế **chưa được validate**, **FP profile xấu**, và vướng **vòng lặp re-identification**. `CẤM-12`. Xem [mục 2.1](#21--h3-continuity-checker--thuật-ngữ-dễ-dùng-sai-nhất-của-cả-repo) |
| **3** | **KHÔNG tự định nghĩa ngưỡng chất lượng nào** (accuracy / coverage / uptime) | Ngưỡng gate sống ở `MVP-Scope` §7 và exit criteria sống ở `Roadmap` §2. `CẤM-16` cấm sửa ngưỡng sau khi thấy kết quả; tạo một hệ ngưỡng thứ hai trong BRD là mở đúng cánh cửa đó |
| **4** | **KHÔNG sở hữu schema** `change_log` / `field_provenance` / `generation.origin` / `parent_generation_id` | `KC-1`–`KC-4` thuộc **BRD-004** (editor ghi hành động) và **BRD-007** (compliance). BRD-008 **tiêu thụ** dữ liệu đó theo góc preference |
| **5** | **KHÔNG sở hữu** `usage_event` / `usage_daily` / credit ledger / hard quota / hold reaper | Thuộc **BRD-006**. Phần credit-ledger của `Roadmap` §4 `X-b` là **MVP3**; BRD-008 chỉ lấy vế *"abuse control cho upload ở MVP1"* của cùng hàng đó |
| **6** | **KHÔNG sở hữu hai human gate bắt buộc** (speaker attribution + dialogue condensation) | Đó là `C7` của nhóm C ⇒ **BRD-003**, đo bằng `M2-4` (**sự VẮNG MẶT của đường code bypass**). `H1` là HITL gate **của vòng eval**, không phải hai gate biên tập đó — **đừng mượn tính chất "không có đường bypass" sang `H1`** |
| **7** | **KHÔNG sở hữu** pipeline sinh ảnh, `best-of-N`, VLM select ở tầng generate | Thuộc **BRD-001** (`A1`). BRD-008 chỉ định nghĩa `H3` như **tầng selection dựa trên N candidate mà `A1` sinh ra** |
| **8** | **KHÔNG làm bộ phát hiện *"truyện này có thể có bản quyền của người khác"*** | Đây là **nghịch lý safe harbour** `R-04`: feature đó **PHÁ chính miễn trừ Điều 198b**, vì điều kiện (a) của miễn trừ là **"không biết"**. Một hạng mục nghe rất giống *"abuse control"* nhưng phải **KHÔNG làm** |
| **9** | **KHÔNG làm takedown tool / đăng ký đầu mối Bộ VHTTDL / SLA 72 giờ** | Đó là `GP-3` + `M2-6` ⇒ **BRD-007**. Dễ bị gộp vào `H5` vì cùng nghe như *"vận hành"* |
| **10** | **KHÔNG làm compositor / renderer trang** | Export (`H4`) **tái dùng compositor của preview** (thuộc thành phần `#4` editor tối thiểu — BRD-004). *"Không viết renderer từ đầu"* (CF-9.1) |
| **11** | **KHÔNG chấm điểm rủi ro mới** | Thang `Probability × Impact` thuộc `Risk-Register.md`. Xem [mục 6](#6-rủi-ro-chính) |

---

## 6. Rủi ro chính

> [!IMPORTANT]
> **Tài liệu này KHÔNG tự chấm điểm rủi ro và KHÔNG tạo rủi ro mới.** SSOT là [`Risk-Register.md`](../../010-Planning/Risk-Register.md). Dưới đây chỉ **trỏ tới ID** đã có, kèm một dòng vì sao nó là rủi ro **của module này**.

| ID | Trỏ tới | Vì sao liên quan BRD-008 |
|---|---|---|
| **`R-22`** | [Phụ thuộc model provider + **silent model drift**](../../010-Planning/Risk-Register.md#21-bảng-chính) | Rủi ro **trung tâm** của module này. `Risk-Register` §5.2 ghi: golden-set eval chạy **hàng tuần** là cách **DUY NHẤT** phát hiện nó — *"theo định nghĩa nó không ném lỗi"*. Đây là nguồn của `BR-008-05` |
| **`R-13`** | [Props chỉ **4.19/5**, thấp nhất trong 4 metric CANVAS](../../010-Planning/Risk-Register.md#21-bảng-chính) (CF-6.3 `[OFF]`) | Chiều yếu nhất chính là chiều mà checker được kỳ vọng bắt. Rà tại `G1` |
| **`R-15`** | [Khoá thời gian `(chapter, scene)` sai âm thầm ở flashback](../../010-Planning/Risk-Register.md#21-bảng-chính) | Hệ quả dây chuyền được ghi đích danh: **Continuity Checker sẽ "sửa" theo state sai** ⇒ tự động làm hỏng đúng những panel đang đúng. Một lý do nữa để `H3` là **selection**, không phải autofix |
| **`R-21`** | [**Bus factor = 1**](../../010-Planning/Risk-Register.md#21-bảng-chính) | HITL gate tiêu **giờ-người** của người duy nhất trong đội. `Risk-Register` §5.2 xếp `R-21` vào nhịp **liên tục**, không chờ gate |
| **`G-04`** | [Tỉ lệ lỗi thật của speaker attribution](../../010-Planning/Risk-Register.md#41-năm-khoảng-trống--không-gán-score) | ⚠️ **Khoảng trống — KHÔNG gán Score.** Số đang lưu hành là `[EM]`, không phải số đo |
| **`G-05`** | [Độ phủ thật của Continuity Checker](../../010-Planning/Risk-Register.md#41-năm-khoảng-trống--không-gán-score) | ⚠️ **Khoảng trống — KHÔNG gán Score.** Là nguồn của `TBD-3` và của nghĩa vụ công bố `40–60%` `[EM]` với user |
| **`KT-8`** | Human-reject rate sau VLM-select — **CHƯA AI CÔNG BỐ** | Chặn việc đặt bất kỳ chỉ tiêu định lượng nào cho eval kit ⇒ `TBD-1`. Nguồn: `findings/business-analyst.md` §6.2 |

> **`Error cascade` — một tính chất, không phải một risk ID.** Lỗi **nhân, không cộng**: 5 tầng mỗi tầng đúng 90% ⇒ end-to-end ≈ **59%** ([`Glossary` — *Error cascade*](../../999-Resources/Glossary.md#sinh-ảnh--kiểm-tra-nhất-quán)). Đây là lý do nền tại sao *"đo được"* là yêu cầu nghiệp vụ chứ không phải tiện nghi kỹ thuật: không có eval từng tầng thì **không biết tầng nào đang ăn phần trăm**.

---

## 7. Tài liệu liên quan

### Tầng Requirements

- [PRD-Comic-Studio](../PRD-Comic-Studio.md) — PRD cha; mục *Chất lượng & vận hành* là nơi BRD này phân giải lên
- [SRS-Comic-Studio](../SRS-Comic-Studio.md) — đặc tả hệ thống

### Tầng User Stories

- [Epic-Quality-And-Operations](../../022-User-Stories/Epics/Epic-Quality-And-Operations.md) — Epic 1:1 với BRD này (`E-H`)

### Use Case

- [UC-06 — Generate Panel And Pick Variant](../Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) — nơi *"chọn X thay vì Y"* xảy ra: vừa là hành động sáng tạo có giá trị pháp lý, vừa là nhãn **preference data** của `BR-008-07`, vừa là chỗ `H3` (`🟡 VLM select` ở MVP0) nằm
- [UC-09 — Export Chapter](../Use-Cases/UC-09-Export-Chapter.md) — hiện thực hoá `H4` / `BR-008-11`…`BR-008-13`

> [!NOTE]
> Các link ở mục này trỏ tới **tên file đã đóng băng** của run `2026-08-24-khoi-tao-requirements-stories-comic-studio`. Một số file **chưa tồn tại tại thời điểm viết** (`KT-12`) — link tới file chưa tồn tại là **đúng và được phép** theo quy ước của run.

---

## Tài liệu tham khảo

### Tài liệu trong repo

- [MVP-Scope](../../010-Planning/MVP-Scope.md) — **nguồn chính**: §3 nhóm `H` (`H1`–`H6`), §6 danh sách `KC`, §7 ba gate `G0`/`G1`/`G2`, §8 kill criteria
- [Charter-Comic-Studio](../../010-Planning/Charter-Comic-Studio.md) — §4 `R9` (điều kiện khả thi của `H1`), §7 `C1`/`C8`/`C9`/`C10`, §9.4 tiêu chí thành công cấp dự án
- [Roadmap](../../010-Planning/Roadmap.md) — §2 exit criteria `P-6` / `M1-6` / `M2-5` / `M4-1` / `M4-2`, §4 việc `X-b`, §5.2 điều kiện doanh thu Tầng 1, §6.2 bảng phụ thuộc
- [Risk-Register](../../010-Planning/Risk-Register.md) — SSOT của rủi ro; §4.1 khoảng trống không gán Score, §5.1 ánh xạ rủi ro → gate, §5.2 rủi ro không chờ gate
- [Analysis-Comic-Studio-Concept](../../050-Research/Analysis-Comic-Studio-Concept.md) — §3.2 (nguồn của yêu cầu ghi lại phán đoán readability), §12 (preference data là moat thật). ⛔ `CẤM-18`: **tài liệu mới link sang, KHÔNG sửa** file này
- [Glossary](../../999-Resources/Glossary.md) — `Continuity Checker` (định nghĩa **đã được sửa lại**), `VLM autorater`, `best-of-N (N=3)`, `re-identification`, `Error cascade`, `HITL gate`, `eval kit`, `preference data`, `MVP0`, `vertical slice`
- [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) — §1.1 hàng BRD-008, §1.2 delta nhóm `H`, §4.8 trục Story, §5.2 bảng canonical facts, §5.3 18 lệnh cấm, §6.2 khoảng trống `TBD`
- [Documents-Template](../../../knowledge-base/99-Templates/Documents-Template.md) — `RULE-001`: thư mục, naming, frontmatter, quy tắc link

### Nguồn ngoài — dẫn qua bảng Canonical Facts, giữ nguyên nhãn

| Con số dùng trong tài liệu này | Nhãn | Nguồn |
|---|---|---|
| **N = 3**, best-of-N, *"performance saturates at N=3"* | `[OFF]` CF-3.1/3.2 | arXiv 2604.13452 — CANVAS |
| **MIE 0.922** pairwise accuracy vs human preference | `[OFF]` | arXiv 2607.01383 — MIBE |
| Độ phủ Continuity Checker **40–60% số panel** | ⚠️ `[EM]` CF-6.11 | ước lượng run `2026-08-23`, **không phải số đo** |
| Golden dataset **15–20 panel** | `MVP-Scope` §3 `H6` · `Roadmap` §2 `P-6` | `findings/architect.md` §7.3 điểm 4 |
| Tầng 1 **$4–8/tháng, KHÔNG image gen** | `[CHỐT]` CF-2.2 | `Charter` §7 `C2` |

---

_Created by quality-assurance_
_Author: trisjr_
