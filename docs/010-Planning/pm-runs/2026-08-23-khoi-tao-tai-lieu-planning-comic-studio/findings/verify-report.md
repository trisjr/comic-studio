# Verify Report — Bước 6

> **Run**: `2026-08-23-khoi-tao-tai-lieu-planning-comic-studio` · **Role**: `context-auditor` (verifier)
> **Phạm vi**: 6 deliverable + `docs/000-Index.md` + cấu trúc Dewey. Read-only tuyệt đối, không sửa deliverable nào.
> **Ngày verify**: 2026-08-23

## Kết luận một dòng

**0 CRITICAL · 4 MAJOR · 5 MINOR.** Không có lỗi nào chặn việc đóng run. Bốn MAJOR đều là **lỗi nhất quán chéo tài liệu**, sửa được bằng edit cục bộ (mỗi cái ≤ 5 dòng), không cần viết lại mục nào. **Đóng được run** sau khi PM xử lý 4 MAJOR ở close-step, hoặc ghi chúng vào *Nợ lại* nếu chọn đóng ngay.

---

## Bảng điểm theo sáu tiêu chí

| # | Tiêu chí | Kết quả | Ghi chú |
|---|---|---|---|
| 1 | Completeness | ✅ **ĐẠT** | Mọi ngưỡng định lượng đều vượt. Hai file sửa stub giữ đúng `id`/`created` và có `updated` |
| 2 | Correctness | ⚠️ **ĐẠT CÓ ĐIỀU KIỆN** | 1 MAJOR (M-2): hai con số margin dẫn từ Analysis mà **không gắn `[EM]`** |
| 3 | Coherence | ⚠️ **ĐẠT CÓ ĐIỀU KIỆN** | 1 MAJOR (M-4) va chạm tên `G1/G2`; 0 đoạn trùng lặp với `Analysis-Comic-Studio-Concept.md` |
| 4 | Connectivity | ✅ **ĐẠT** | 0 link chết · 0 wiki-link · 0 orphan |
| 5 | ⭐ Cross-doc consistency | ⚠️ **ĐẠT CÓ ĐIỀU KIỆN** | 2 MAJOR (M-1, M-3). **Cả hai cạm bẫy đã biết đều KHÔNG dính** |
| 6 | ⭐ Sweep khuyến nghị bị rơi | ✅ **ĐẠT — 0 khuyến nghị bị rơi** | Quét cơ học toàn bộ outline + `findings/researcher.md`; xem §6 |

---

## Tiêu chí 1 — Completeness

### 1.1 Frontmatter — ĐẠT 7/7

| File | `id` | `type` | `status` | `created` | `updated` | Verdict |
|---|---|---|---|---|---|---|
| `Charter-Comic-Studio.md:1-6` | `CHARTER-001` | `charter` | `draft` | `2026-08-23` | — (file mới) | ✅ |
| `MVP-Scope.md:1-6` | `MVPSCOPE-001` | `mvp-scope` | `draft` | `2026-08-23` | — | ✅ |
| `Roadmap.md:1-7` | `ROADMAP-001` ✅ **giữ** | `roadmap` | `draft` | `2026-02-04` ✅ **giữ** | `2026-08-23` ✅ | ✅ **Không dính failure mode ghi đè stub** |
| `OKRs.md:1-7` | `OKRS-001` ✅ **giữ** | `okrs` | `draft` | `2026-02-04` ✅ **giữ** | `2026-08-23` ✅ | ✅ **Không dính failure mode ghi đè stub** |
| `Risk-Register.md:1-10` | `RISK-001` | `risk-register` | `draft` | `2026-08-23` | `2026-08-23` | ✅ (thêm `owner`/`tags`/`linked-to`, additive) |
| `Analysis-Market-...md:1-10` | `RESEARCH-002` | `research` | `draft` | `2026-08-23` | `2026-08-23` | ✅ |
| `000-Index.md:1-8` | `INDEX-000` | `index` | `live` | `2026-08-23` | `2026-08-23` | ✅ |

### 1.2 Ngưỡng định lượng — ĐẠT 7/7

| Ngưỡng outline | Yêu cầu | Thực tế | Verdict |
|---|---|---|---|
| Charter — ràng buộc | ≥6 | **10** (`Charter:201-210`, C1→C10), đủ cả 6 ràng buộc bắt buộc | ✅ |
| Charter — RACI | ≥8 hàng × 5 cột | **9 hàng × 5 cột** (`Charter:177-187`); `C` cho Luật sư SHTT ở hàng 4 kèm *"CHƯA ENGAGE"* (`Charter:182`) | ✅ |
| Risk Register — số rủi ro | ≥16 | **23 có Score** (R-01→R-23) + **RP-01** + **RB-01** + **10 khoảng trống** | ✅ |
| Risk Register — `Trigger` | **mọi hàng không rỗng** | Kiểm từng hàng `Risk-Register:74-96` và `:115` — **24/24 hàng có Trigger quan sát được** | ✅ |
| Research Notes — URL | ≥25 | **41 URL unique**. Đối chiếu tập URL với `findings/researcher.md`: **41 ↔ 41, `comm -23` trả về rỗng** ⇒ không URL nào bị rơi | ✅ |
| Research Notes — mục | 7 mục + tham khảo | §1→§7 + `## Tài liệu tham khảo` | ✅ |
| OKRs — anti-goal | ≥4 | **8** (`OKRs:235-242`, AG-1→AG-8) | ✅ |

### 1.3 Cấu trúc Dewey + Index — ĐẠT

- `find docs -type d` = **44 thư mục** (12 tầng Dewey + 32 thư mục con), **32 `.gitkeep`**.
- **Đã đối chiếu 1:1 với khối *Required Folder Structure*** (`knowledge-base/99-Templates/Documents-Template.md:136-210`): RULE-001 yêu cầu **12 tầng** (`010 · 020 · 022 · 030 · 035 · 040 · 050 · 060 · 070 · 080 · 090 · 999`) và **32 thư mục con** (010:3 · 020:2 · 022:3 · 030:4 · 035:5 · 040:4 · 050:3 · 060:2 · 070:2 · 080:2 · 090:0 · 999:2). **Khớp 100%, không thừa không thiếu.** `pm-runs/` là thư mục run-state nằm ngoài khối bắt buộc (additive, được `Planning-MOC.md` khai báo).
- 11 MOC bắt buộc đều tồn tại; `000-Index.md` tồn tại. ⚠️ `Specs-MOC.md` và `Design-MOC.md` là **0 byte** — đã được ghi nhận là nợ **ngoài scope** run này.
- Validation Checklist của RULE-001 (`knowledge-base/99-Templates/Documents-Template.md:251-256`): **6/6 mục pass** cho cả 6 deliverable.
- Ripple đã xong: `Documents-Template.md:84` đã có hàng `MVP Scope → docs/010-Planning/MVP-Scope.md`; `Documents-Template.md:11` ghi changelog 2026-08-23.

---

## Tiêu chí 2 — Correctness

### 🟠 MAJOR M-2 — Hai con số margin dẫn từ Analysis mà KHÔNG gắn `[EM]`

**File**: `docs/010-Planning/MVP-Scope.md` · **Dòng 427 và 428**

> `427`: `1. ⭐ **Đổi granularity render sang whole-page.** Analysis §9b.3: per-panel @N=3 cho margin **−141%**; whole-page @N=3 cho **+40%**.`
> `428`: `> ⚠️ **Nói thẳng giới hạn của đường lui này**: whole-page @N=3 cho **+40%**, vẫn **dưới** dải kỳ vọng **50–60%** `[BCN]` (CF-3.10).`

**Đã xác minh nguồn**: hai con số có thật — `docs/050-Research/Analysis-Comic-Studio-Concept.md:878-879` (bảng: `1 ảnh/panel → −141% ❌` · `1 ảnh/page → +40% ✅`). **Không phải bịa.**

**Vấn đề**: cả hai là **margin tính ra từ giả định** (thừa hưởng CF-3.3 `60 ảnh/chapter` `[EM]` và CF-3.1 `N=3`), tức đúng loại số mà quy tắc CF #3 bắt phải mang `[EM]`. Ở dòng 428 chúng còn được **đặt cạnh và so trực tiếp** với `50–60%` `[BCN]` — một số đo ngành có nhãn. Đọc lướt sẽ thấy hai con số cùng hạng.

**Đối chứng nội bộ chứng minh đây là bỏ sót chứ không phải quy ước**: `Roadmap.md:67` xử lý một trường hợp y hệt (số ngoài CF, dẫn trực tiếp từ Analysis) **đúng cách**:
> `| Pipeline lõi ... | **35–45%** | `[EM]` ước lượng của lens kiến trúc, [Analysis §5.7] — ⚠️ **con số này KHÔNG có trong bảng CF**, dẫn trực tiếp từ nguồn |`

**Đề xuất sửa** (2 chỗ, cùng một pattern):
- Dòng 427 → `... per-panel @N=3 cho margin **−141%** `[EM]`; whole-page @N=3 cho **+40%** `[EM]` — ⚠️ **hai con số này KHÔNG có trong bảng CF**, dẫn trực tiếp từ [Analysis §9b.3](../050-Research/Analysis-Comic-Studio-Concept.md), và kế thừa giả định 60 ảnh/chapter (CF-3.3 `[EM]`).`
- Dòng 428 → thêm `[EM]` ngay sau `**+40%**`.

### 2.2 Phần còn lại của Tiêu chí 2 — ĐẠT

Đã grep từng con số CF dùng chung qua cả 6 file. **Không tìm thấy trường hợp nào khác** một số `[EM]` mất nhãn, hoặc một phép nhân/chia sinh số mới mà kết quả không mang `[EM]`:

| Con số | Xuất hiện tại | Nhãn ở mọi nơi |
|---|---|---|
| `$12,06` | `Charter:207`, `Charter:221`, `MVP-Scope:404`, `OKRs:219`, `Risk-Register:81` | `[EM tính từ OFF]` **+ caveat "là SÀN không phải trần" ở cả 5 chỗ** ✅ |
| `−262%` | `Charter:118`, `Charter:264`, `MVP-Scope:406`, `MVP-Scope:416`, `Risk-Register:80` | `[EM]` ở cả 5 chỗ ✅ |
| `$36.18` (phép nhân mới) | `Risk-Register:80` | `[EM]` — *"3 × $12,06 `[EM tính từ OFF]`"*, **chuỗi suy dẫn được giữ nguyên** ✅ |
| `35–50%` / `70–95%` (phép cộng mới) | `Roadmap:66`, `Roadmap:68` | `[EM]` + ghi thẳng *"phép cộng của em"* ✅ |
| `11–17%` (phép cộng mới) | `Roadmap:105` | `[EM]` + *"phép cộng của em từ CF-6.7"* ✅ |
| `180 ảnh` | `Charter:222`, `MVP-Scope:408`, `MVP-Scope:417`, `OKRs:220`, `Risk-Register:80`, `Analysis-Market:294` | `[EM]` ở cả 6 chỗ ✅ |
| `~125 ảnh/tháng` | `Charter:143`, `MVP-Scope:157`, `MVP-Scope:417`, `OKRs:220`, `Risk-Register:80`, `Risk-Register:175`, `Analysis-Market:284` | `[TC]` ở cả 7 chỗ ✅ |
| TAM `$14B` | `Charter:54-63`, `Risk-Register:84`, `OKRs:239` (AG-5), `Analysis-Market:112-116` | Chỉ xuất hiện **để bị bác bỏ**. **0 lần dùng làm căn cứ biện minh** ✅ |

---

## Tiêu chí 3 — Coherence

### 🟠 MAJOR M-4 — `G1` / `G2` mang hai nghĩa khác nhau **bên trong cùng một file**

**File**: `docs/010-Planning/Charter-Comic-Studio.md` · **Dòng 94-98 vs dòng 238**

Charter §3 đặt ID cho **năm mục tiêu dự án** là `G1`…`G5`:
> `94`: `| **G1** | **Biết tiền đề còn đứng hay không, trong 1–2 tuần và ~$12** | ...`
> `95`: `| **G2** | **Đo được thứ chưa ai đo: human-reject rate sau VLM-select** | ... | Ngưỡng PASS: `TBD` (định tại [MVP-Scope.md](./MVP-Scope.md) **gate G1**) |`

Trong khi cùng file, dòng 238 dùng `G1`/`G2` cho **ba gate** do `MVP-Scope.md` §7 định nghĩa:
> `238`: `**Chi tiết ba gate (G0 pháp lý · G1 kỹ thuật sau MVP0 · G2 kinh tế sau MVP1) và kill criteria nằm ở [MVP-Scope.md](./MVP-Scope.md).**`

⇒ Dòng 95 là chỗ va chạm rõ nhất: **hàng mang ID `G2` (mục tiêu) lại trỏ tới `gate G1`**. Một người đọc bảng §3 rồi đọc §9 sẽ có hai hệ ký hiệu chồng lên nhau. Bốn tài liệu còn lại đều dùng `G0/G1/G2` **chỉ** theo nghĩa gate — nên Charter là file duy nhất lệch.

**Đề xuất sửa**: đổi ID mục tiêu ở `Charter:94-98` từ `G1…G5` sang `MT-1…MT-5` (hoặc `OBJ-1…OBJ-5`), và cập nhật hai chỗ trỏ ngược: `Charter:100` (*"G1 là mục tiêu bao trùm"*) và `Charter:269` (*"năm mục tiêu ở mục 3"* — chỗ này không cần đổi). **Không đổi tên gate** — gate là canon của `MVP-Scope.md` §7.

### 3.2 Trùng lặp với `Analysis-Comic-Studio-Concept.md` — ĐẠT, 0 đoạn trùng thực chất

Đã kiểm cả hai chiều:
- **Nội dung mới**: `grep 'GlobalComix|Constella|ChartMogul|RevenueCat'` trên `Analysis-Comic-Studio-Concept.md` ⇒ **0 hit**. Toàn bộ §3 (GlobalComix + INKR, Constella) và §5 (retention benchmark) là nội dung **mới hoàn toàn**.
- **Nội dung cũ được link thay vì lặp**: `Analysis-Market:195` (*"Bảng đối thủ nền ... nằm ở Analysis-Comic-Studio-Concept.md — **không lặp lại ở đây**"*), `:226` (*"Phần unit economics ... §9b. Mục này **không nhắc lại** các con số đó"*), `:439` (*"Khoảng trống công nghệ và pháp lý nằm ở ... §11 — **không lặp lại ở đây**"*).
- Ràng buộc *"mâu thuẫn Anifusion phải xuất hiện dưới dạng mâu thuẫn"*: ✅ `Analysis-Market:165-177` có bảng hai cột Nguồn A / Nguồn B, trạng thái *"❌ Chưa phân xử"* cho cả giá lẫn doanh thu.

### 3.3 Mâu thuẫn nhỏ khác

Xem MINOR m-1, m-2, m-3 ở §7.

---

## Tiêu chí 4 — Connectivity

| Kiểm | Kết quả |
|---|---|
| **Wiki-link `[[...]]`** | **0**. Hit duy nhất là `000-Index.md:151` — nằm trong **code span** của câu phát biểu quy tắc (`... **KHÔNG** dùng wiki-link `[[...]]`.`), không phải một link. ✅ |
| **Markdown link phân giải được** | Trích 80 relative link từ 7 file, đối chiếu với `find`. **0 dead link.** Bao gồm cả `../knowledge-base/00-Index.md` và `../knowledge-base/99-Templates/Documents-Template.md` (đều tồn tại) ✅ |
| **Bảng *Markdown link phải tạo* của outline** | 8/8 quan hệ đều có mặt ✅ |
| **Orphan** | 0. Cả 6 deliverable đều được `000-Index.md` liệt kê (dòng 46-52 và 62-66) **và** MOC tầng tương ứng (`Planning-MOC.md`, `Research-MOC.md`) ✅ |
| **MOC được cập nhật** | `Planning-MOC.md` (5 tài liệu + sửa mô tả `pm-runs` + `updated: 2026-08-23`) · `Research-MOC.md` (thêm Analysis mới + gỡ cảnh báo placeholder) · `Resources-MOC.md` (21 relative link, **0 dead**) ✅ |

---

## ⭐ Tiêu chí 5 — Cross-doc consistency

### 5.1 Hai cạm bẫy đã biết — **KHÔNG dính cái nào**

| Cạm bẫy | Kết quả kiểm | Bằng chứng |
|---|---|---|
| **CF-6.7 (20–25%, mẫu số SaaS) trừ CF-6.8 (50–60%, mẫu số công cụ cá nhân)** | ✅ **KHÔNG tài liệu nào thực hiện phép trừ.** `grep '25–40\|25-40'` chỉ ra **đúng một hit**, và đó là **lời cấm** | `MVP-Scope:249`: *"Phép tính `50–60% − 20–25% = 25–40% tiết kiệm` là **SAI về mặt số học**"*. `MVP-Scope:241-253` có khối cảnh báo mẫu số đầy đủ. `Charter:225` (A6) nhắc lại lệnh cấm. `Risk-Register:89` (R-16, cột Residual) nhắc lại lần ba |
| **CF-4.6 (GRR ChartMogul) gộp với CF-4.8 (payer retention RevenueCat)** | ✅ **KHÔNG tài liệu nào gộp/so trực tiếp** | `Risk-Register:82` (R-09): *"Xác nhận độc lập **cùng chiều** (không phải cùng metric) ... **KHÔNG gộp với CF-4.6**"*. `Analysis-Market:376-383` có khối `[!WARNING]` riêng: *"nói '23% và 21,1% khớp nhau' là **sai**"*. `Charter` và `OKRs` không nhắc `21,1%` ở đâu cả |

### 5.2 Giá trị CF dùng chung — ĐẠT toàn bộ

Với mỗi con số CF xuất hiện ở ≥2 tài liệu, đã grep và đọc ngữ cảnh từng hit:

| CF | Giá trị | Số tài liệu | Giá trị khớp? | Nhãn/caveat sống sót? |
|---|---|---|---|---|
| CF-3.5 `$12,06` | `$12,06` | 5 | ✅ (kể cả dấu phẩy thập phân, **không có biến thể `$12.06`**) | ✅ 5/5 có `[EM tính từ OFF]` + *"là SÀN"* |
| CF-3.7 `−262%` | `−262%` | 5 | ✅ | ✅ 5/5 `[EM]` |
| CF-4.6 `23% GRR / 32% NRR` | `23% / 32%` | 4 (+ Glossary — xem M-1) | ✅ | ⚠️ **4/4 deliverable OK, Glossary KHÔNG** — xem M-1 |
| CF-4.4 `$4–14K ARR` | `$4K–14K ARR ≈ $300–1.200 MRR, 30–80 user` | 5 | ✅ | ✅ 5/5 `[EM]` |
| CF-4.5 Anifusion | `$833 MRR` **+ mâu thuẫn `$5.000/tháng`** | 5 (`Charter:74`, `Roadmap:268`, `OKRs:156/195/238`, `Risk-Register:84/176`, `Analysis-Market:160-175`) | ✅ | ✅ **5/5 giữ nguyên cả hai con số kèm nhãn mâu thuẫn** — không nơi nào chọn một |
| CF-2.5 `~125 ảnh/tháng` | `~125` | 5 | ✅ | ✅ 5/5 `[TC]` |
| CF-6.5 `≤3 nhân vật/panel` | `42.33 → 27.21 → 2.67 → 0.52` | 4 | ✅ (cả 4 số phụ đều khớp) | ✅ 4/4 `[OFF]` |
| CF-3.1 `N=3` | `N=3`, *"saturates at N=3"* | 6 | ✅ | ✅ 6/6 `[OFF]` + phân biệt với retry-on-failure |
| CF-6.7 `20–25%` | `~20–25%` | 4 | ✅ | ✅ 4/4 `[EM]` + ghi rõ mẫu số SaaS |
| CF-3.10 `50–60%` | `50–60%` | 3 | ✅ | ✅ 3/3 `[BCN]` + ICONIQ 52% / Bessemer |

### 5.3 Mốc thời gian — ĐẠT

`Roadmap.md` là nguồn mốc duy nhất và **hai tài liệu kia tuyên bố điều đó tường minh**: `OKRs:42` (*"Mọi mốc thời gian trong tài liệu này lấy từ Roadmap.md, không mốc nào được tạo mới ở đây"* + liệt kê tập mốc hợp lệ). Đối chiếu:

| Mốc | `Roadmap.md` | `MVP-Scope.md` | `OKRs.md` | Khớp |
|---|---|---|---|---|
| Pre-cycle / MVP0 | 09/2026, 1–2 tuần (`:103`) | — | 09/2026, không OKR (`:69`) | ✅ |
| G1 | Cuối 09/2026 (`:317`) | Cuối **09/2026** (`:315`, `:364`) | trỏ link (`:86`) | ✅ |
| MVP1 | 10–12/2026 (`:104`) | — | 10–12/2026 (`:96`) | ✅ |
| G2 | Cuối Q4/2026, hạn cứng 31/12/2026 (`:303`, `:323`) | Cuối **Q4/2026** (`:316`, `:394`) | *"trước 31/12/2026"* (`:145`) | ✅ |
| MVP2 | 01–02/2027 (`:105`) | — | 01–02/2027 (`:172`) | ✅ |
| MVP3 | **03/2027 — NGOÀI HORIZON** (`:106`, `:249`) | — | *"từ 03/2027"* (`:104`) | ✅ |

### 5.4 Ba gate G0/G1/G2 — ĐẠT, không tài liệu nào tự định nghĩa lại

| Tài liệu | Cách tham chiếu | Verdict |
|---|---|---|
| `Roadmap.md:15` | *"Ba gate G0/G1/G2 ... được **định nghĩa tại MVP-Scope.md mục 7**; ở đây chỉ tham chiếu, không định nghĩa lại"* | ✅ tuyên bố tường minh |
| `OKRs.md:251` | *"MVP-Scope.md — **định nghĩa ba gate G0/G1/G2** (mục 7)"*; §2.2 (`:81`) *"ngưỡng cố tình **không chép lại**, để trong toàn bộ kho tài liệu chỉ có **đúng một nơi** sửa được ngưỡng"* | ✅ **mẫu mực** |
| `Risk-Register.md:183` | *"Ba gate G0/G1/G2 do MVP-Scope.md §7 định nghĩa. Mục này chỉ trả lời: rủi ro nào rà ở gate nào"* | ✅ |

Nội dung gate cũng khớp: G0 = pháp lý / trước dòng code thương mại / không chặn MVP0–MVP1 (nhất quán ở `MVP-Scope:324`, `Roadmap:280-291`, `OKRs:90`, `Risk-Register:146`, `Charter:257`). G1 = kỹ thuật sau MVP0. G2 = kinh tế sau MVP1.

### 🟠 MAJOR M-1 — `23% GRR` mất **toàn bộ ba caveat** khi sang Glossary

**File**: `docs/999-Resources/Glossary.md` · **Dòng 96** (file `updated: 2026-08-23`, tức được chạm trong run này)

> `96`: `- **GRR (Gross Revenue Retention)**: Tỉ lệ giữ doanh thu, chưa tính upsell. **Ở phân khúc AI budget-tier con số ngành là 23%** — thấp tới mức làm subscription trở thành mô hình sai với một dev không có ngân sách marketing.`

**Vấn đề — đúng failure mode mà Tiêu chí 5 được dựng ra để bắt:**
1. **Không có nhãn** `[OFF]`, không có tên nguồn (ChartMogul).
2. **Mất cả ba caveat bắt buộc CF-4.7**: (a) cohort AI-native chỉ ~200 công ty, n của band không công bố; (b) lọc ≥$250K ARR ⇒ **loại đúng nhóm indie mà comic-studio thuộc về**; (c) dữ liệu 2025.
3. Diễn đạt *"con số ngành là 23%"* trình bày nó như **một hằng số ngành đã đo**, trong khi bốn deliverable đều mô tả nó là *"tín hiệu về hướng, không phải dự báo cho comic-studio"* (`Risk-Register:104`).

**Đối chứng — bốn deliverable đều làm ĐÚNG:**

| File | Dòng | Ba caveat có mặt? |
|---|---|---|
| `Charter-Comic-Studio.md` | `224` (A5) | ✅ đủ (a)(b)(c) inline |
| `MVP-Scope.md` | — | không dùng con số này (đúng, ngoài phạm vi tài liệu) |
| `OKRs.md` | `221` (M-6) | ✅ đủ (a)(b)(c) |
| `Risk-Register.md` | `82` (R-09) + khối `99-104` | ✅ khối `[!WARNING]` riêng, *"không được tách khỏi con số"* |
| `Analysis-Market-...md` | `346-351` | ✅ khối `[!WARNING]`, *"Trích 23% mà bỏ ba dòng này là trích sai"* |

⇒ Glossary là **nơi duy nhất** con số đi trần trụi — và là nơi người đọc tra định nghĩa, tức nơi con số dễ bị copy đi nhất.

**Đề xuất sửa** (`Glossary.md:96`, PM sở hữu file này):
> `- **GRR (Gross Revenue Retention)**: Tỉ lệ giữ doanh thu, chưa tính upsell. Band AI-native `<$50/tháng`: **23% GRR / 32% NRR** `[OFF]` ChartMogul (~3.500 công ty). ⚠️ **Ba caveat bắt buộc, không tách khỏi con số**: (a) cohort AI-native chỉ ~200 công ty, n của riêng band này không công bố; (b) lọc ≥$250K ARR ⇒ loại đúng nhóm indie mà `comic-studio` thuộc về; (c) dữ liệu 2025. Chi tiết: [Analysis-Market-Competitor-Landscape §5.1](../050-Research/Analysis-Market-Competitor-Landscape.md#51-23-grr--chartmogul-và-ba-caveat-bắt-buộc).`

### 🟠 MAJOR M-3 — Checklist safe harbour Điều 198b: **3 mục hay 6 mục?**

Cùng một tiêu chí đo được, ba tài liệu ghi hai con số khác nhau:

| File | Dòng | Nguyên văn | Số mục |
|---|---|---|---|
| `Risk-Register.md` | `75` (R-02, Mitigation) | *"**Checklist 6 mục** (Analysis §8.3): form + `copyright@`, đăng ký đầu mối, **soft-delete + disable-access** cấp project ..., user warrant, opt-out check"* | **6** |
| `Risk-Register.md` | `189` (§5.1, cột *Câu hỏi phải trả lời khi rời G0*) | *"Checklist 198b (R-02) đã **tick đủ 6 mục**"* | **6** |
| `OKRs.md` | `187` (KR6.2, cột *Cách đo*) | *"Checklist **tick đủ 3 mục** + có xác nhận đăng ký"* | **3** |
| `MVP-Scope.md` | `162` (GP-3) | *"takedown, đăng ký đầu mối Bộ VHTTDL, SLA 72 giờ"* (theo CF-7.6) | **3** |
| `Roadmap.md` | `235` (X-a) | *"công cụ takedown · đăng ký đầu mối với Bộ VHTTDL · SLA 72 giờ"* (theo CF-7.6) | **3** |

**Vì sao là MAJOR chứ không phải MINOR**: `KR6.2` là một **Key Result có ngưỡng đếm được**, và `R-02` là **điều kiện rời gate G0**. Hai tài liệu đang đo cùng một artifact bằng hai thước khác nhau — chấm KR6.2 "ĐẠT" ở 3 mục sẽ để lọt 3 mục mà Risk Register coi là bắt buộc (soft-delete + disable-access, user warrant, opt-out check).

**Nguyên nhân gốc**: CF-7.6 chỉ liệt kê **3** mục; `Analysis §8.3` liệt kê **6**. Writer `security-auditor` dùng nguồn rộng hơn, ba writer kia dùng CF. Đây là hệ quả trực tiếp của việc chạy song song.

**Đề xuất sửa** (chọn 6 làm chuẩn vì nó bao trùm và có nguồn):
- `OKRs.md:187` → `Checklist tick đủ **6 mục** ([Risk-Register R-02](./Risk-Register.md#21-bảng-chính)) + có xác nhận đăng ký đầu mối`
- `MVP-Scope.md:162` và `Roadmap.md:235` → giữ nguyên 3 mục **cốt lõi của CF-7.6** nhưng thêm `... — danh sách đầy đủ 6 mục ở [Risk-Register R-02](./Risk-Register.md)`.

---

## ⭐ Tiêu chí 6 — Sweep khuyến nghị bị rơi

**Phương pháp**: quét cơ học từng dòng `outline.md` chứa *"bắt buộc"* / *"phải có"* / *"BẮT BUỘC có mặt"*, cộng từng khuyến nghị và từng khoảng trống trong `findings/researcher.md`, rồi `grep` từng mục vào deliverable tương ứng.

**Kết quả: 0 khuyến nghị bị rơi.** Chi tiết:

### 6.1 Risk Register — 5 nhóm rủi ro bắt buộc: **17/17 mục có mặt**

| Nhóm | Outline yêu cầu | Có mặt tại | ✓ |
|---|---|---|---|
| Pháp lý (4) | Điều 37a TDM (CF-7.4) | `Risk-Register:132` (RB-01 câu 1) + `:161` (G-01). **Cố ý không đặt trong Risk Log**, lý do ghi rõ tại `:65` | ✅ |
| | Safe harbour 198b (CF-7.6) | `:75` (R-02) | ✅ |
| | Deadline TTNT ~01/03/2027 (CF-7.7) | `:76` (R-03) | ✅ |
| | Không lưu provenance ⇒ không backfill (CF-7.3) | `:74` (R-01, Score 9) | ✅ |
| Kinh tế (3) | Power user −262% (CF-3.7) | `:80` (R-07) | ✅ |
| | GRR 23% **+ ba caveat** (CF-4.6/4.7) | `:82` (R-09) + khối caveat `:99-104` | ✅ |
| | $12,06 là **sàn** (CF-3.5) | `:81` (R-08) | ✅ |
| Kỹ thuật (4) | Multi-character 2–3 nhân vật (CF-6.4) | `:85` (R-12) | ✅ |
| | Props 4.19/5 (CF-6.3) | `:86` (R-13) | ✅ |
| | Speaker attribution (CF-6.10) | `:164` (G-04) — **đúng nơi outline chỉ định** (mục 4, không gán Score) | ✅ |
| | Checker phủ 40–60% (CF-6.11) | `:165` (G-05) — **đúng nơi outline chỉ định** | ✅ |
| Thị trường (3) | GlobalComix + INKR (CF-5.2/5.3) | `:91` (R-18) | ✅ |
| | Constella — **hàng RIÊNG** | `:115` (RP-01, §2.2 bảng riêng, không gán Score) | ✅ **đúng yêu cầu "hàng riêng"** |
| | Backlash cộng đồng (CF-5.6) | `:92` (R-19) | ✅ |
| Vận hành (3) | Bus factor = 1 (CF-1.2) | `:94` (R-21) | ✅ |
| | Model provider + silent drift | `:95` (R-22) | ✅ |
| | Onboarding BYOK không đo được (CF-2.5 caveat) | `:96` (R-23) + `:175` (G-08) | ✅ |

Ngoài ra outline yêu cầu **11 cột** Risk Log — `Risk-Register:72` có đủ 11 cột đúng thứ tự; **công thức Score nêu tường minh** — `:38-49` (`Score = P × I`, dải 1–9, và `:53` nói rõ chỉ có 6 giá trị hợp lệ `1·2·3·4·6·9`); **`Owner` là vai trò TNMCORE-OS** — 24/24 hàng ghi `architect`/`security-auditor`/`business-analyst`/`product-owner`/`senior-ai-engineer`/`pm`, **0 hàng ghi "Founder"** ✅.

### 6.2 OKRs — 4 anti-goal bắt buộc: **4/4 có mặt** (tổng 8)

| Outline yêu cầu | Có mặt |
|---|---|
| Không Show HN/Product Hunt làm kênh chính (CF-5.8) | `OKRs:235` AG-1 ✅ |
| Không marketing vào cộng đồng hoạ sĩ (CF-5.6–5.7) | `OKRs:236` AG-2 ✅ |
| Không build canvas editor đầy đủ (CF-9.1) | `OKRs:237` AG-3 ✅ |
| Không mục tiêu doanh thu thang nghìn đô năm 1 | `OKRs:238` AG-4 ✅ |
| *(bonus)* AG-5 TAM · AG-6 đua editor GlobalComix · AG-7 hạ N · AG-8 free tier có image gen | `OKRs:239-242` |

Các ràng buộc OKRs khác: 3–4 Objective/chu kỳ ✅ (Q4: 4 Obj/13 KR — `OKRs:161`; Q1: 3 Obj/8 KR — `:200`); mọi KR có **số + cách đo + tần suất đo** ✅ (cả 21 KR đều có 3 cột đó); **0 KR trích TAM** ✅ (grep `TAM` trên `OKRs.md` ⇒ chỉ 2 hit, đều ở AG-5 với nghĩa cấm); KR doanh thu nằm trong dải CF-4.4 ✅ (`OKRs:195` KR7.2); KR kênh **giữ nguyên cột neo lý do** từ `findings/researcher.md` ✅ (`OKRs:152` tuyên bố, `:156-159` giữ nguyên cột *Neo bằng chứng*).

### 6.3 Research Notes §7 — **23/23 khoảng trống, 5/5 nhóm**

| Nhóm | Outline | Thực tế | ✓ |
|---|---|---|---|
| 1 (1.a–1.d) | 4 | `Analysis-Market:445-448` — 4 mục | ✅ |
| 2 (2.a–2.e) | 5 | `:454-458` — 5 mục | ✅ |
| 3 (3.a–3.e) | 5 | `:464-468` — 5 mục | ✅ |
| 4 (4.a–4.d) | 4 | `:474-477` — 4 mục | ✅ |
| 5 (5.a–5.e) | 5 | `:483-487` — 5 mục | ✅ |
| ⭐ **5.e — kênh thị trường Việt Nam** | **bắt buộc** | `Analysis-Market:487` — có mặt, và **được nâng cấp**: *"khoảng trống **có thể lấp được** ... **phải là ưu tiên của vòng nghiên cứu kế tiếp**, vì comic-studio chịu ràng buộc pháp lý Việt Nam nhưng chưa có một dòng dữ liệu nào về kênh đi tới người dùng Việt Nam"* | ✅ **vượt yêu cầu** |

### 6.4 Charter — **CHÍN** điều kiện khả thi (không phải bảy)

`Charter:112-122` liệt kê **R1→R9**, và `Charter:109-110` có khối `[!IMPORTANT]` giải thích tại sao Analysis §4.1 ghi *"BẢY"*: *"đó là số của một lens (`researcher`) và được giữ để truy vết. **Số điều kiện phải thoả là CHÍN**"*. ✅ **Đúng yêu cầu, và xử lý đúng cách mâu thuẫn nguồn.**

### 6.5 MVP-Scope — mục 6 và mục 8

| Outline yêu cầu | Thực tế |
|---|---|
| Mục 6 *"Không được cắt"* — 4 nhóm | ✅ **7 mục KC-1…KC-7** (`MVP-Scope:286-292`), phủ đủ 4 nhóm: provenance 5 trường (KC-1/2/3 + KC-4 transaction) · `tenant_id` (KC-5) · opt-out 37b (KC-6) · hold reserve 3 credit/panel (KC-7). Mỗi mục có cột *"Không giữ thì hỏng thế nào"* ✅ |
| Mục 8 *kill criteria* — tồn tại và không rỗng | ✅ `MVP-Scope:438-473` — **K1→K5** + §8.2 *"dừng có trật tự"* + §8.3 *"ba thứ KHÔNG phải kill"* |
| Ba gate có tiêu chí **đo được**, không gate nào ghi *"đánh giá chủ quan"* | ✅ G0 = 3 trạng thái 🟢/🟡/🔴 trên artifact văn bản (`:338-352`); G1 = 5 tiêu chí G1-a…G1-e có ngưỡng số (`:372-376`); G2 = G2-a…G2-d có công thức (`:414-417`). **Mọi ngưỡng do writer tự đặt đều tự khai `[EM]`** (`:374`, `:375`, `:452`, `:453`, `:455`) ✅ |
| Bảng mục 3 phủ MVP0–MVP4 | ✅ 33 hàng × 8 nhóm A→H (`:111-171`) |
| Mục 5 nêu rõ CF-6.7 ≠ CF-6.8, cấm trừ | ✅ `:241-253` |
| CF-9.4 trình bày như **tự thu hồi** | ✅ `:215-233` — giữ nguyên hình dạng *"khuyến nghị ban đầu — và nó SAI"* |

### 6.6 Roadmap — CF-8.13 và các mục bắt buộc

| Outline yêu cầu | Thực tế |
|---|---|
| CF-8.13 trả lời **tường minh** | ✅ `Roadmap:46`: **"Câu trả lời: KHÔNG. Khung 09/2026–02/2027 KHÔNG chứa hết MVP0–MVP3."** Kèm 4 bước lập luận kiểm tra được (`:54-72`) và nhãn `[EM]` cho chính kết luận (`:52`) |
| Nói thẳng **cái gì rơi ra** | ✅ `:51` và §5.1 (`:247-253`) — MVP3, MVP4, mọi gói trả phí có image gen, credit ledger |
| **Cấm nén lịch** | ✅ `:72` *"Nhét thêm MVP3 vào cùng hai tháng đó chính là hành vi mà CF-8.13 gọi tên ... Tài liệu này **không làm điều đó**"* |
| Mục 6 nêu rõ G0 **không** chặn MVP0–MVP1 | ✅ `:279-293` — đặt làm §6.1 *"Điều dễ hiểu nhầm nhất của cả tài liệu"*, có bảng 4 hoạt động |
| Pre-cycle 09/2026 đủ **ba việc** | ✅ `:124-154` — luật sư · MVP0 · sửa khoá thời gian + chốt KC-1…KC-7 |
| CF-8.11 ba việc xen ngang, **neo vào trigger** | ✅ `:233-237` — X-a/X-b/X-c, mỗi việc có cột *Trigger* |
| Mọi mốc có **exit criteria đo được** | ✅ P-1…P-6 · M1-1…M1-7 · M2-1…M2-6 · M3-1…M3-4 · M4-1…M4-2 |

### 6.7 `findings/researcher.md` §B — 7/7 khuyến nghị PM đã vào deliverable

| # | Khuyến nghị (`researcher.md:314-320`) | Landed tại |
|---|---|---|
| 1 | TAM **không** được vào Charter; neo SOM | `Charter:50-69` (§2.1 đặt **trước** §2.2 có chủ ý) ✅ |
| 2 | Cấu hình 3 tầng kiểu Novelcrafter | `Charter:202` (C2) · `Analysis-Market:298-306` ✅ |
| 3 | Ngưỡng 125 ảnh/tháng là quy tắc phân tuyến code được | `MVP-Scope:417` (G2-d) · `OKRs:220` (M-5) ✅ |
| 4 | GlobalComix + INKR **phải vào Risk Register** | `Risk-Register:91` (R-18) ✅ |
| 5 | Constella là **hàng riêng** trong Risk Register | `Risk-Register:115` (RP-01, bảng riêng §2.2) ✅ |
| 6 | Positioning *"writer, không artist"* phải là **constraint trong Charter** | `Charter:205` (C5) ✅ |
| 7 | Anifusion $833 MRR sau ~2 năm là neo doanh thu | `OKRs:195/198` · `MVP-Scope:454` (K4) · `Risk-Register:84` ✅ |

Bốn mâu thuẫn §C của `researcher.md` cũng được xử đúng: Anifusion ghi cả hai ✅ · Dashtoon là content studio, không dùng làm neo pricing ✅ (`Charter:154`, `Analysis-Market:210-213`) · *"credit pack né 23% GRR"* ghi là lập luận không phải số đo ✅ (`Charter:224` A5, `Risk-Register:162` G-02) · cấu hình hybrid không tồn tại ⇒ dùng cấu hình A ✅ (`Analysis-Market:265-275`).

---

## §7 — Danh sách issue đầy đủ theo mức độ

### 🔴 CRITICAL — 0

Không có.

### 🟠 MAJOR — 4

| ID | File:dòng | Vấn đề | Tiêu chí |
|---|---|---|---|
| **M-1** | `docs/999-Resources/Glossary.md:96` | `23% GRR` mất nhãn `[OFF]` **và mất cả ba caveat CF-4.7**, trình bày như *"con số ngành"* | 5 |
| **M-2** | `docs/010-Planning/MVP-Scope.md:427,428` | `−141%` và `+40%` (margin dẫn từ Analysis §9b.3) **không gắn `[EM]`**, dòng 428 còn so trực tiếp với `50–60%` `[BCN]` | 2 |
| **M-3** | `docs/010-Planning/Risk-Register.md:75,189` ↔ `docs/010-Planning/OKRs.md:187` | Checklist safe harbour 198b: **6 mục** vs **3 mục** — hai thước cho cùng một điều kiện rời gate G0 | 5 |
| **M-4** | `docs/010-Planning/Charter-Comic-Studio.md:94-98` ↔ `:238` | ID mục tiêu `G1…G5` va chạm tên gate `G0/G1/G2`; dòng 95 (hàng **G2**) trỏ tới *"gate G1"* | 3 / 5 |

### 🟡 MINOR — 5

| ID | File:dòng | Vấn đề | Đề xuất sửa |
|---|---|---|---|
| **m-1** | `MVP-Scope.md:136` ↔ `MVP-Scope.md:259-263` ↔ `Roadmap.md:105` | Phân bổ thành phần editor ở MVP2 lệch **ba chiều**: hàng D1 ghi `🟡 +#3 template`; §5.2 cột *Mốc* đặt #3 **và** #4 ở MVP2, #2 ở MVP2–MVP3; Roadmap ghi *"Thành phần **#2, #3, #4** editor tối thiểu (**11–17%** `[EM]`)"* | Sửa ô D1/MVP2 (`:136`) thành `🟡 +#3, #4, #2 (một phần)` để khớp §5.2 và Roadmap. Con số 11–17% của Roadmap đúng theo §5.2 (5–8 + 3–4 + 3–5), nên **Roadmap là bên đúng** |
| **m-2** | `MVP-Scope.md:289` | KC-4 ghi *"Cả **bốn** mục KC-1…KC-3"* — `KC-1…KC-3` là **ba** mục | Đổi thành *"Cả **ba** mục KC-1…KC-3"*. (`:282` ghi *"bảy mục"* cho KC-1…KC-7 là **đúng**) |
| **m-3** | `Analysis-Market-Competitor-Landscape.md:302` | `Margin ~90%` mang nhãn `[EM]`, trong khi `Charter:202` (C2), `MVP-Scope:158` (F6), `OKRs:194` (KR7.1) đều mang `[CHỐT]` CF-2.2 | Không phải rửa khoảng trống (Analysis **chặt hơn** CF, không lỏng hơn), nhưng nên thống nhất. Đề xuất: dùng `[CHỐT]` CF-2.2 kèm ghi chú *"phần `~90%` là ước lượng `[EM]` bên trong một quyết định `[CHỐT]`"* — hoặc PM sửa chính CF-2.2 ở run sau |
| **m-4** | `Charter-Comic-Studio.md:231` (A12) | A12 nêu giả định *"Horizon 6 tháng đủ cho MVP0–MVP3"* và giao Roadmap trả lời — nhưng `Roadmap.md:46` **đã trả lời KHÔNG**. Charter để người đọc treo ở một giả định đã có kết luận | Thêm một câu vào cột *"Sai thì hỏng ở đâu"*: *"⇒ [Roadmap §1.2](./Roadmap.md#12--cf-813--trả-lời-tường-minh-trước-khi-anh-đọc-bất-cứ-dòng-nào-phía-dưới) đã trả lời **KHÔNG**: MVP3 và MVP4 rơi ra ngoài horizon."* Đây là hệ quả tự nhiên của việc chạy song song, không phải lỗi của writer |
| **m-5** | `docs/999-Resources/Glossary.md` (54 term) | Glossary đã tăng từ 40 → **54 term** và phủ tốt (BYOK, GRR, NRR, payer retention, RACI, best-of-N, TAM/SAM/SOM, anti-goal, credit ledger + hold, `field_provenance`, HITL gate…). **Còn thiếu 6 thuật ngữ mà bộ Planning dùng nhiều lần** | Đề xuất bổ sung: **`regen ratio` (p50/p90)** — biến quyết định của G2, dùng ở 4/6 file · **`gate G0/G1/G2`** — cần một chỗ định nghĩa ngắn trỏ về `MVP-Scope` §7 · **`kill criteria` vs `PIVOT`** — `MVP-Scope:443-445` phân biệt hai thứ, đáng chuẩn hoá · **`safe harbour` / `Điều 198b`** · **`opt-out signal` / `Điều 37b`** · **`horizon`** (09/2026–02/2027) |

### ❓ Cần PM tự kiểm (nghi ngờ, **không** xác minh được bằng quy tắc có sẵn — cố ý KHÔNG xếp vào MAJOR)

1. **Deliverable link thẳng vào `pm-runs/**`.** `Charter:14,293,294,295` · `MVP-Scope:486,487` · `Roadmap:355,356` · `OKRs:256` · `Risk-Register:20`. Bảng *Markdown link phải tạo* của outline **không kê** các link này, và `Planning-MOC.md` ghi rõ `pm-runs` *"không phải deliverable, và không được chuẩn hoá"*. Deliverable `draft` đang phụ thuộc điều hướng vào run-state bị đóng băng. **Không có quy tắc nào trong RULE-001 cấm điều này**, nên em không xếp nó là lỗi — nhưng PM nên quyết định đây là pattern muốn giữ hay không, vì nó sẽ lặp lại ở mọi run sau.
2. **`outline.md` trích `findings/researcher.md §A.5`** (mục *Nguồn sự thật* của OKRs và của Research Notes). File `researcher.md` **không có heading `A.5`** — nó đánh số `Câu 1`…`Câu 5` bên trong khối `A`. Nội dung được trỏ tới (bảng KR kênh phân phối) có thật ở `researcher.md:290-298`, nên **không ảnh hưởng deliverable**; chỉ là citation lỏng trong outline. `outline.md` ngoài phạm vi sửa của em.
3. **Cách đếm thư mục Dewey trong outline** *(đã đóng — chỉ còn là vấn đề diễn đạt)*. `find docs -type d` cho **44** thư mục, đối chiếu `Documents-Template.md:136-210` thì RULE-001 đòi đúng **12 tầng + 32 con = 44**, và cả 44 đều có mặt. Outline ghi *"32 thư mục"* vì đếm **thư mục con** (khớp với 32 `.gitkeep`). **Không có sai lệch cấu trúc nào** — chỉ đề nghị PM thống nhất cách phát biểu ở run sau để khỏi ai phải đếm lại.

---

## §8 — Ba điều đáng ghi nhận (để run sau lặp lại)

1. **Đối sách chống rửa nhãn đã hoạt động.** Failure mode E2 của run trước (*"khoảng trống bị rửa sạch qua một phép nhân"*) **không tái diễn ở bất kỳ deliverable nào**. Ba phép tính mới sinh ra trong run này — `$36.18` (`Risk-Register:80`), `35–50%`/`70–95%` (`Roadmap:66,68`), `11–17%` (`Roadmap:105`) — đều tự gắn `[EM]` **và** tự khai *"phép cộng/phép nhân của em"*. Lỗ hổng duy nhất còn lại (M-1) nằm ở **Glossary**, tức ở tài liệu **ngoài** danh sách 5 deliverable Planning — đúng chỗ mà quy tắc "copy cả số và nhãn" chưa được dispatch tới.
2. **Cả hai cạm bẫy được cảnh báo trước đều bị chặn bằng lời cấm tường minh**, không phải bằng may mắn: `MVP-Scope:241-253` (mẫu số) và `Analysis-Market:376-383` (GRR ≠ payer retention). Pattern đáng nhân bản: **viết lệnh cấm vào chính tài liệu, ở chỗ người đọc sẽ gặp con số**.
3. **`OKRs.md:81` là mẫu mực chống trôi ngưỡng**: *"ngưỡng cố tình **không chép lại**, để trong toàn bộ kho tài liệu chỉ có **đúng một nơi** sửa được ngưỡng."* Đây là lý do §5.4 của báo cáo này không tìm ra một sai lệch nào về nội dung gate.

---

## §9 — Khuyến nghị đóng run

**Đóng được run.** Không có CRITICAL. Bốn MAJOR đều là edit cục bộ:

| Thứ tự | Việc | File | Ước lượng |
|---|---|---|---|
| 1 | Sửa M-1 (Glossary GRR) | `docs/999-Resources/Glossary.md:96` | 1 dòng — **PM sở hữu, làm ngay ở close-step** |
| 2 | Sửa M-3 (checklist 3↔6) | `docs/010-Planning/OKRs.md:187` (+ chú thích ở `MVP-Scope:162`, `Roadmap:235`) | 3 dòng |
| 3 | Sửa M-2 (nhãn `[EM]`) | `docs/010-Planning/MVP-Scope.md:427,428` | 2 dòng |
| 4 | Sửa M-4 (đổi `G1…G5` → `MT-1…MT-5`) | `docs/010-Planning/Charter-Comic-Studio.md:94-100` | 6 dòng |
| 5 | 5 MINOR | xem §7 | tuỳ chọn, có thể ghi *Nợ lại* |

**Không cần quay lại Bước 5.** Không deliverable nào phải viết lại mục nào; không có khuyến nghị nào bị rơi; không có khẳng định vô căn cứ nào.

---

*Generated by TNMCORE-OS — role `context-auditor` (verifier). Read-only: không deliverable nào bị sửa trong quá trình verify.*
*Author: trisjr*
