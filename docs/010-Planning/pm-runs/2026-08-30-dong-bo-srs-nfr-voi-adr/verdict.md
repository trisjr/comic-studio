---
id: VERDICT-2026-08-30-DONG-BO-SRS-NFR-VOI-ADR
type: run-verdict
run: 2026-08-30-dong-bo-srs-nfr-voi-adr
lane: doc
verifier: context-auditor
status: not-closeable-as-is
created: 2026-08-30
---

# Verdict — Lô VERIFY run đồng bộ `SRS` (020) ↔ `ADR` (030)

> [!IMPORTANT]
> Lô này **READ-ONLY** trên `docs/`. Mọi phát hiện dưới đây **chỉ báo cáo**, ⛔ không tự vá. File này là **file duy nhất** lô VERIFY ghi.

## Mục lục

- [Kết luận nhanh](#kết-luận-nhanh)
- [1. COMPLETENESS](#1-completeness--pass)
- [2. CORRECTNESS](#2-correctness--pass)
- [3. COHERENCE](#3-coherence--pass-có-điều-kiện)
- [4. CONNECTIVITY](#4-connectivity--pass)
- [5. Soi kỹ 6 điểm PM tự sửa](#5-soi-kỹ-6-điểm-pm-tự-sửa)
- [6. Danh sách phát hiện](#6-danh-sách-phát-hiện)
- [7. Kết luận](#7-kết-luận)

## Kết luận nhanh

| Tiêu chí | Kết quả |
|---|:--:|
| 1. COMPLETENESS | ✅ **PASS** |
| 2. CORRECTNESS | ✅ **PASS** |
| 3. COHERENCE | ⚠️ **PASS có điều kiện** — 2 WARNING |
| 4. CONNECTIVITY | ✅ **PASS** |
| Phần PM tự sửa (6 điểm) | ⚠️ **4/6 ĐẠT · 2/6 WARNING** |

**CRITICAL: 0 · WARNING: 3 · SUGGESTION: 4**

⭐ **Cả 5 cái bẫy mà brief/escalations dựng sẵn đều KHÔNG sập**: `55` đứng yên · `21` đứng yên · `C-10` vẫn mở · vendor billing vẫn `TBD` · `ADR-001:16`/`:70`/`:173` còn nguyên. Bốn chỗ khoá số khớp **cả bốn**.

---

## 1. COMPLETENESS — ✅ PASS

### 1.1 Đủ hạng mục trong `outline.md`

`git diff --numstat` (15 file) + commit `f77b922` (1 file) — đối chiếu từng dòng bảng hạng mục:

| Lô | Outline khai | Đếm cơ học từ diff | Khớp |
|---|---|---|:--:|
| Lô 1 — `SRS` | 21 điểm + frontmatter | `22 22 docs/020-Requirements/SRS-Comic-Studio.md` ⇒ 22 dòng đổi, trừ 1 dòng `updated:` = **21 điểm nội dung** | ✅ |
| Lô 2a — Security · API · Schema · Integration | 7/7 | `Threat-Model:293`, `:522` · `Endpoint-Preview-Export:201`, `:250` · `DB-Entity-Tenancy:96`, `:313` · `Spec-Integration-Auth-Provider:190` = **7** | ✅ |
| Lô 2b — Architecture | 9/9 + 4 frontmatter | 4 status flip (`ADR-001`…`004`) + `ADR-010:177` · `SDD:457` · `SDD:812` · `ADR-006:257` · `ADR-006:258` · `ADR-015:272` = **4 + 6** | ⚠️ *(xem `W-1`)* |
| Lô 3 — PM | 6 | `Specs-MOC:13` · `Index:96` · `Index:220` · `Index:178` · `ADR-002:85` · `Specs-MOC` frontmatter = **6** | ✅ |

⭐ Hạng mục **nguy hiểm nhất mà brief cảnh báo tuyệt đối không được bỏ sót** — `SDD-Comic-Studio.md:812` (*"năm hàng LAI"* hard-code) — **ĐÃ SỬA** ✅.

### 1.2 `updated: 2026-08-30` ở MỌI file chạm — K-5

```
grep -c '^updated: 2026-08-30' <15 file bị chạm>
```
→ **15/15 file trả về `1`**. ✅ K-5 ĐẠT tuyệt đối.

| File | `updated` |
|---|:--:|
| `docs/000-Index.md` | ✅ 1 |
| `docs/020-Requirements/SRS-Comic-Studio.md` | ✅ 1 |
| `docs/030-Specs/Specs-MOC.md` | ✅ 1 |
| `ADR-001` · `ADR-002` · `ADR-003` · `ADR-004` | ✅ 1 mỗi file |
| `ADR-006` · `ADR-010` · `ADR-015` · `SDD` | ✅ 1 mỗi file |
| `DB-Entity-Tenancy` · `Spec-Security-Threat-Model` | ✅ 1 mỗi file |
| `Endpoint-Preview-Export` · `Spec-Integration-Auth-Provider` | ✅ 1 mỗi file |

> [!NOTE]
> `docs/000-Index.md` ⛔ **không có hunk frontmatter** trong `git diff` — nó đã mang `updated: 2026-08-30` sẵn từ run `2026-08-30-brand-guidelines...` cùng ngày. Kết quả **đúng**, nhưng K-5 ⛔ **không thực sự được áp** cho file này ⇒ `S-4`.

### 1.3 Frontmatter đủ trường

`grep -rh '^status:' docs/030-Specs/ | sort | uniq -c` → `4 accepted · 53 draft · 1 live`. ⛔ Không file nào thiếu `status`. `Specs-MOC.md` có đủ `id`/`type`/`status: live`/`project`/`created`/`updated`. ✅

---

## 2. CORRECTNESS — ✅ PASS

### 2.1 ⭐⭐ BỐN CHỖ KHOÁ SỐ — đã ĐẾM LẠI TẠI NGUỒN, ⛔ không trích lại

Đây là hạng mục dự án đã ship lỗi **hai lần** (`E9`, `E10` run trước). Em ⛔ **không đọc con số từ `findings/architect.md`**; mọi số dưới đây suy ra bằng `grep`/`awk` trên bảng thật.

```
sed -n '60p' SRS-Comic-Studio.md   | grep -oE 'SRS-(FR|NFR)-[0-9]+' | sort
sed -n '812p' SDD-Comic-Studio.md  | grep -oE 'SRS-(FR|NFR)-[0-9]+' | sort
```

**Kết quả — hai danh sách GIỐNG HỆT NHAU, từng mã một:**

```
SRS-FR-20 SRS-FR-23 SRS-FR-26 SRS-NFR-07 SRS-NFR-08 SRS-NFR-09 SRS-NFR-17 SRS-NFR-20
```

| # | Chỗ khoá | Nguyên văn tại nguồn | Đếm thật | Khớp |
|:--:|---|---|:--:|:--:|
| 1 | `SRS:58` | `#### b. Tám hàng **LAI** — cơ chế CHỐT, tham số bên trong chưa quyết` | chữ **Tám** | ✅ |
| 2 | `SRS:60` | danh sách 8 mã ở trên | **8** | ✅ |
| 3 | `SRS:345` | `tổng hàng LAI = 3 + 5 = 8` (lai 3 trong rổ MẶC ĐỊNH + lai 5 trong rổ `TBD`) | **8** | ✅ |
| 4 | `SDD-Comic-Studio.md:812` | `là **tám hàng LAI**` + đúng 8 mã | **8** | ✅ |

⭐ **KHỚP CẢ BỐN.** ⛔ Không còn dấu vết *"năm hàng LAI"* ở bất kỳ đâu.

### 2.2 Phép tính `55 + 7 + 6 = 68`

```
sed -n '343p' SRS-Comic-Studio.md
| **TỔNG** | `SRS-FR-01`…`42` + `SRS-NFR-01`…`26` | **68** |
```

`SRS:345` ghi: **CHỐT** thuần **55** · **MẶC ĐỊNH** **7** (thuần 4 + lai 3) · `TBD` **6** (thuần 1 + lai 5).

| Phép kiểm | Kết quả |
|---|:--:|
| `55 + 7 + 6` | `68` = TỔNG ở `SRS:343` ✅ |
| `4 + 3` | `7` = con số MẶC ĐỊNH ✅ |
| `1 + 5` | `6` = con số `TBD` ✅ |
| `3 + 5` | `8` = danh sách LAI ở `SRS:60` ✅ |
| **Kiểm chéo độc lập `55`**: `68 − 4` (MẶC ĐỊNH thuần) `− 1` (`TBD` thuần) `− 8` (LAI) | `= 55` ✅ |

### 2.3 ⛔ HAI CON SỐ PHẢI ĐỨNG YÊN — `K-2` / `E4`

| Con số | Vị trí | Verify độc lập | Kết quả |
|---|---|---|:--:|
| **`55`** | `SRS:345` — CHỐT thuần | Phép trừ ở §2.2 ra đúng `55`; `git diff` cho thấy chuỗi `**CHỐT** thuần **55**` xuất hiện **nguyên văn ở cả dòng `-` lẫn dòng `+`** | ✅ **ĐỨNG YÊN** |
| **`21`** | `SRS:437` — số hàng ở lại `TBD` | `awk` đếm hàng bảng §5.2: dòng **441→461**, đúng **ROW1…ROW21**, hàng 21 = `b-7`, hàng 22 trở đi thuộc bảng §5.3 khác | ✅ **ĐỨNG YÊN** |

```
awk 'NR>=441 && NR<=475 {if ($0 ~ /^\|/) {n++; printf "%d ROW%d\n", NR, n}}' SRS-Comic-Studio.md
441 ROW1  ... 455 ROW15(b-1) 456 ROW16(b-2) 457 ROW17(b-3) 458 ROW18(b-4)
459 ROW19(b-5) 460 ROW20(b-6) 461 ROW21(b-7)   ← hết bảng
463 = "### 5.3 Hai con số [EM] KHÔNG được nâng thành NFR"
```

Nguyên văn `SRS:437`: *"**Hai mươi mốt hàng** dưới đây **ở lại `TBD`**"* — ✅ **đúng, và cả 5 hàng `b-1`/`b-2`/`b-5`/`b-6`/`b-7` chỉ đổi mệnh đề lý do, ⛔ không đổi trạng thái.**

### 2.4 Câu đếm `53 draft + 4 accepted = 57`

```
grep -rln '^status: accepted' docs/030-Specs/ | wc -l   →  4
grep -rln '^status: draft'    docs/030-Specs/ | wc -l   → 53
find docs/030-Specs -name '*.md' | wc -l                → 58
grep -rh '^status:' docs/030-Specs/ | sort | uniq -c    → 4 accepted · 53 draft · 1 live
```

⭐ **Mẫu số đúng**: 58 file `.md` = 57 tài liệu + `Specs-MOC.md` (`status: live`, là MOC ⛔ không phải tài liệu spec). ⇒ `53 + 4 = 57` **khớp chính xác** ✅ ở **cả hai** chỗ: `Specs-MOC.md:13` và `000-Index.md:96`.

### 2.5 Đối chiếu phát biểu mới của `SRS` với ADR nguồn *(spot-check các mệnh đề chịu lực)*

| Phát biểu ở `SRS` | Nguồn | Kết quả |
|---|---|:--:|
| `:258` *"tầng CHỐT của `ADR-001` gồm **8 điều**"* | `ADR-001` §Tầng CHỐT — đánh số `1.`…`8.` | ✅ |
| `:258` *"**ba điều** … KHÔNG có đường lui"* | `ADR-001:139`: *"⛔ **Ba dòng CHỐT** (một ngôn ngữ TypeScript · SQL thô là nguồn sự thật schema · API là hợp đồng duy nhất) **không có đường lui**"* — trùng đúng 3 điều `SRS` nêu | ✅ |
| `:258` thang đường lui *"Fastify · Kysely hoặc `pg` thuần · đổi riêng frontend"* | `ADR-001:131-138` — bảng Đường lui đúng **3 hàng**, đúng 3 nội dung đó | ✅ |
| `:258` *"**pnpm workspace** và **ESLint boundary rule** … ⛔ CHƯA có đường lui ghi rõ"* | `ADR-001` tầng MẶC ĐỊNH có **5 hàng**, bảng Đường lui chỉ có **3** — thiếu đúng pnpm + ESLint | ✅ ⭐ khớp `E7` #1 |
| `:256` thang `1.` Fly.io `2.` GCP Cloud Run + Cloud SQL (`asia-southeast1`) `3.` AWS ECS Fargate + RDS (`ap-southeast-1`) | `ADR-002:72-74` — trùng khít | ✅ |
| `:256` *"**3 hạng mục** phải verify trước khi mua"* | `ADR-002:66` — `(a)` region Singapore `(b)` PITR/backup thuộc gói nào `(c)` giới hạn cron job = **3** | ✅ |
| `:257` thang auth `1.` Auth0 `2.` Supabase Auth / WorkOS `3.` Keycloak/Ory self-host | `ADR-003:67` — trùng khít | ✅ |
| `:257` *"**3 tiêu chí** nghiệm thu spike"* | `ADR-003:62`: *"**Ba tiêu chí nghiệm thu bắt buộc của spike**"* | ✅ |
| `:257` thang storage `1.` AWS S3 `2.` Backblaze B2 `3.` object storage của chính PaaS | `ADR-004:73` — trùng khít | ✅ |
| `:386` *"**4 hạng mục** phải verify trước khi mua"* (R2) | `ADR-004:76` — `(a)(b)(c)(d)` = **4** | ✅ |
| `:257` *"vendor billing … chặn bởi **quốc gia của pháp nhân bán hàng**, ⛔ không phải vì thiếu phân tích kỹ thuật"* | `ADR-003:74` — **nguyên văn cùng lập luận**; `:78` owner = **Founder** + dev | ✅ |

⭐ **⛔ Không tìm thấy một thang đường lui bịa, một con số bịa, hay một tên vendor bịa nào.**

---

## 3. COHERENCE — ⚠️ PASS có điều kiện

### 3.1 Còn chỗ nào ở tầng 030 viện dẫn *"vì `SRS-NFR-07/08/09` còn `TBD`"* làm **lý do**?

```
grep -rn 'SRS-NFR-0[789]' docs/030-Specs/     → 36 hit / 16 file
```

Phân xử **từng hit**:

| Nhóm | Hit | Phán quyết |
|---|---|:--:|
| **Đã sửa trong lô này** | `TM:293`, `TM:522`, `PE:201`, `PE:250`, `Auth-Provider:190`, `ADR-006:257`, `ADR-006:258`, `ADR-010:177`, `ADR-015:272`, `Tenancy:96`, `Tenancy:313`, `SDD:457`, `SDD:812`, `ADR-002:85`, `Specs-MOC:13` | ✅ **SẠCH** |
| **Trạng thái ĐẦU VÀO (`E1`)** — ⛔ không phải lỗi | `ADR-001:16`, `:173` · `ADR-002:16`, `:190` · `ADR-003:20`, `:174` · `ADR-004:23`, `:172` | ✅ **ĐÚNG như đang có** |
| **Vẫn ĐÚNG sau đồng bộ** | `Object-Storage:128` (*"R2 là **mặc định**, ⛔ không phải đã mua"* + 4 mục verify) · `Billing-Provider:65` (*"Ở lại `TBD` **có chủ đích**… quốc gia pháp nhân bán hàng"*) · `Auth-Provider:93` (*"Clerk là **mặc định**, ⛔ không phải đã mua"*) · `ADR-003:176` · `SDD:725` (tiêu đề nhóm) · `Tenancy:28`, `:329` · `ADR-006:218` | ✅ **KHÔNG cần sửa** |
| **Còn sót** | `ADR-006:270` | ⚠️ **`W-3`** |
| **Trôi lý do (nhẹ)** | `SDD:778` · `DB-Entity-Generation:486` · `TM:86` | 💡 **`S-1`** |

⭐ ⛔ **Không còn một dòng nào viết thẳng *"vì `SRS-NFR-09` còn `TBD`"* làm lý do.** Bốn chỗ mang lý do đó (`TM:293`, `TM:522`, `PE:201`, `PE:250`) đều đã được viết lại đúng.

### 3.2 ⛔ KHÔNG ĐƯỢC ĐÓNG HỘ — `K-3` / `E5`

#### (a) `C-10` — cơ chế render an toàn của compositor: **VẪN MỞ** ✅

| Vị trí | Trạng thái sau lô | Lý do mới |
|---|---|---|
| `Spec-Security-Threat-Model.md:293` | ✅ vẫn là hàng ràng buộc **MỞ** | *"⛔ **không phải** vì `SRS-NFR-09` … Cái còn mở là `ADR-001` §`TBD`: **thư viện compositor + sinh PDF** và **`worker_threads` hay tách hẳn thành job**"* |
| `Spec-Security-Threat-Model.md:522` | ✅ vẫn nằm trong bảng **câu hỏi mở** | như trên |
| `Endpoint-Preview-Export.md:201` | ✅ *"**File này ⛔ KHÔNG chốt cơ chế**"* | như trên |
| `Endpoint-Preview-Export.md:250` | ✅ vẫn nằm trong mục **`TBD` còn lại** | như trên |

⭐ **Verify lý do mới TẠI NGUỒN `ADR-001`** — ⛔ không tin văn bản trích:

```
ADR-001:67  | Thư viện compositor + sinh PDF (shaping tiếng Việt, 300 DPI) | ... | Dev | **Spike MVP0** |
ADR-001:69  | Compositor chạy trong `worker_threads` hay tách hẳn thành job | Phụ thuộc số đo chưa có | Dev | Sau spike MVP0 |
```

✅ **Cả hai hạng mục có thật, đúng chủ (Dev), đúng mốc (Spike MVP0)** ⇒ lý do mới **có cơ sở**, mốc *"MVP0 (spike)"* thay cho *"Phase 4"* là **đúng nguồn**, ⛔ không phải PM tự chế.

#### (b) Vendor billing: **VẪN `TBD`** ✅

| Vị trí | Nguyên văn |
|---|---|
| `SRS:257` | *"⭐ **CHƯA QUYẾT** → `TBD`: **vendor billing** — chặn bởi **quốc gia của pháp nhân bán hàng**"* |
| `SRS:263` | *"⭐ **Phần duy nhất còn `TBD` thật là vendor billing**"* |
| `SRS:385` | *"⭐ **vendor billing vẫn `TBD`**"* |
| `ADR-006:257` | *"⛔ phần **billing vẫn `TBD`**"* |
| `Spec-Integration-Auth-Provider.md:190` | *"`SRS-NFR-08` (vendor auth = MẶC ĐỊNH, billing `TBD`)"* |

✅ **`SRS-NFR-08` ⛔ KHÔNG bị ghi MẶC ĐỊNH thuần ở bất kỳ đâu.** Nó được xếp vào rổ **`TBD` (lai)** ở `SRS:345` — đúng quy tắc *"thành phần yếu nhất"*.

### 3.3 ⭐ `ADR-001:16` · `:70` · `:173` — PHẢI CÒN NGUYÊN (`K-4` / `E1`)

`git diff` `ADR-001` = `2 1` (⇒ **chỉ frontmatter**: `status: draft`→`accepted` + thêm `updated:`). ⛔ **Không một dòng body nào bị chạm.** Đọc lại tận nơi để ghi nguyên văn:

| Dòng | Nguyên văn hiện tại | Phán quyết |
|---|---|:--:|
| `ADR-001:16` (`## Context`) | *"`SRS-NFR-09` (…) là **`CHƯA QUYẾT` → `TBD`** — SRS §3.E ghi rõ *'Không anchor được'*…"* | ✅ **CÒN NGUYÊN — ĐẠT** |
| `ADR-001:70` (dòng chịu lực `b-6`/`b-7`) | *"`SRS` §5.2 hàng `b-6`, `b-7` ghi rõ hai hạng mục này **phụ thuộc `SRS-NFR-09`** … ⚠️ **ADR này đóng việc CHỌN ngôn ngữ/framework, ⛔ KHÔNG đóng hai hàng đó.**"* | ✅ **CÒN NGUYÊN — ĐẠT** |
| `ADR-001:173` (bảng *cố ý để mở*) | `` | Ngôn ngữ / framework backend & frontend, ORM & migration tool | `SRS-NFR-09` (`CHƯA QUYẾT` → `TBD`) | `SRS` §3.E … | `` | ✅ **CÒN NGUYÊN — ĐẠT** |

> [!NOTE]
> ⛔ **Em ⛔ KHÔNG báo ba dòng này là lệch.** Theo `E1` chúng mô tả **trạng thái ĐẦU VÀO**. Kiểm chéo: cột trace của `SRS:460` (`b-6`) = `SRS-FR-16`, `SRS-NFR-09` và `SRS:461` (`b-7`) = `SRS-NFR-20`, `SRS-FR-25`, `SRS-NFR-09` ⇒ khẳng định của `ADR-001:70` **vẫn đúng với bản `SRS` mới**.

### 3.4 `SDD-Comic-Studio.md:63` (`R-6`) — cố ý KHÔNG sửa

`git diff` `SDD` = 3 hunk duy nhất: frontmatter · `:457` · `:812`. Dòng 63 ⛔ không nằm trong hunk nào. Đọc tận nơi:

```
| **R-6** | **Một ngôn ngữ** cho api + worker + web; **một** hợp đồng API | Không context-switch
giữa ba runtime cho một người — [ADR-001](./ADR-001-...md) | `SRS-NFR-09` |
```

✅ **CÒN NGUYÊN.** Nó chỉ **neo** `R-6` vào `SRS-NFR-09`, ⛔ không khẳng định `TBD` ⇒ sau đồng bộ nó **đúng hơn trước**. ĐẠT.

---

## 4. CONNECTIVITY — ✅ PASS

### 4.1 Link mới của `SRS` trỏ vào tầng 030 (hệ quả `G-2`)

```
grep -oE '\(\.\./030-Specs/[^)#]+\)' SRS-Comic-Studio.md | sort | uniq -c
   6 (../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md)
   8 (../030-Specs/Architecture/ADR-002-Hosting-Platform-And-Region.md)
   3 (../030-Specs/Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md)
   4 (../030-Specs/Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md)
```

**Tổng 21 link, 4 đường dẫn phân biệt.** `ls` từ `docs/020-Requirements/` → **cả 4 file tồn tại thật** ✅. ⛔ Không có link nào trỏ ra ngoài `ADR-001`…`ADR-004` ⇒ đúng chính sách mới ở `SRS:15`/`:72` (*"chỉ link ở những hàng đã được đóng bằng ADR"*).

Link mới ở `000-Index.md:178` → `./010-Planning/pm-runs/2026-08-30-dong-bo-srs-nfr-voi-adr/escalations.md` — `ls` ✅ **tồn tại**.

### 4.2 Mâu thuẫn chính sách nội tại đã được gỡ (`G-2`)

| Dòng | Trước | Sau |
|---|---|---|
| `SRS:15` | *"SRS này **không tạo bất kỳ link nào** trỏ vào đó"* | *"SRS này **được phép link** vào `ADR-001`…`ADR-004` ở **những hàng đã được đóng**"* ✅ |
| `SRS:39` | *"mọi thứ thuộc 030-Specs được nêu bằng văn bản thuần, **không link**"* | *"SRS **dẫn chiếu** quyết định của 030-Specs …, nhưng **không tự ra quyết định thay**"* ✅ |
| `SRS:72` | *"⛔ **Tài liệu này không chứa link nào tới `docs/030-Specs/`.**"* | *"✅ **Tài liệu này được phép link tới `docs/030-Specs/`**"* ✅ |

⭐ **Cả BA dòng tự cấm đều được gỡ.** ⛔ Không sót dòng nào ⇒ ⛔ **không tạo mâu thuẫn nội tại mới** — đúng cái rủi ro #1 của brief.

### 4.3 RULE-001 — cấm wiki-link `[[...]]`

```
grep -c '\[\[' SRS-Comic-Studio.md          → 0
grep -rc '\[\[' docs/030-Specs/ | grep -v ':0' | wc -l  → 0
```

✅ **0 wiki-link** ở toàn bộ tầng 020 + 030.

> [!WARNING]
> `grep -rc '\[\[' docs/` **KHÔNG trả về 0** (~20 file có hit). Em đã mở từng hit trong file lô này chạm: `000-Index.md:191` = *"⛔ **KHÔNG** dùng wiki-link `[[...]]`"* — tức **câu văn phát biểu chính luật**, ⛔ **không phải** wiki-link thật. `Requirements-MOC.md:78` y hệt. Còn lại nằm ở `pm-runs/` và `Epics/` — ⛔ ngoài phạm vi lô này. ⇒ **RULE-001 ĐẠT về thực chất**, nhưng lệnh grep trần sinh false positive ⇒ `S-3`.

---

## 5. Soi kỹ 6 điểm PM tự sửa

⭐ Phần này ⛔ **không writer nào review**. Run trước, đúng loại điểm này sinh ra 1 CRITICAL + 1 WARNING.

### 5.1 `ADR-002:85` — mệnh đề về `b-1`/`b-5`/`b-7` ✅ **ĐÚNG**

**PM viết**: *"`SRS` §5.2: hàng `b-1` và `b-5` neo vào **`SRS-NFR-07`** — tức neo vào chính ADR này; hàng `b-7` thì ⛔ **không** neo vào `SRS-NFR-07` …, nhưng ADR này vẫn được nêu tên ở đó vì nó **tuyên bố ⛔ không đóng** hàng ấy."*

**Verify tại nguồn — đọc CỘT TRACE CUỐI của từng hàng `SRS` §5.2:**

| Hàng | Dòng | Cột trace cuối (nguyên văn) | Có `SRS-NFR-07`? |
|:--:|:--:|---|:--:|
| `b-1` | `SRS:455` | `` `SRS-FR-02`, `SRS-NFR-07`, `SRS-NFR-08` `` | ✅ **CÓ** |
| `b-5` | `SRS:459` | `` `SRS-NFR-02`, `SRS-NFR-07`, `SRS-FR-26` `` | ✅ **CÓ** |
| `b-7` | `SRS:461` | `` `SRS-NFR-20`, `SRS-FR-25`, `SRS-NFR-09` `` | ⛔ **KHÔNG** |

✅ **Phát biểu của PM chính xác từng hàng một.** Kiểm thêm mệnh đề phụ: `SRS:461` (`b-7`) có nêu tên `ADR-002` không? — CÓ: *"**Cả `ADR-001` lẫn `ADR-002` đều tuyên bố tường minh ⛔ KHÔNG đóng hàng này**"* ✅. Và trích dẫn *"chưa ai phát biểu observability thành một hạng mục"* là **nguyên văn** từ `SRS:461` ✅.

⭐ Đây chính là chỗ dễ sai nhất của lô (mệnh đề 3 vế, không writer review) — và nó **ĐẠT**.

### 5.2 `Specs-MOC.md:13` — câu đếm 53/4/57 ✅ **ĐÚNG** *(bằng chứng §2.4)*

### 5.3 `000-Index.md:96` — câu đếm tương tự ✅ **ĐÚNG** *(bằng chứng §2.4)*

⭐ PM còn tự dán **lệnh kiểm** vào chính câu văn: *"(đếm cơ học `grep -rln '^status: accepted' docs/030-Specs/` ngày 2026-08-30, ⛔ không trích lại)"* — em đã chạy đúng lệnh đó, ra đúng `4`. Ghi lệnh vào văn bản là **thói quen tốt**, nên giữ.

### 5.4 `000-Index.md:220` — hàng nợ số 5 ⚠️ **WARNING `W-2`**

| Mệnh đề | Verify | Kết quả |
|---|---|:--:|
| *"✅ **ĐÓNG** ở run `2026-08-30-dong-bo-srs-nfr-voi-adr`"* | Đúng — hàng nợ này chính là việc lô làm | ✅ |
| *"Phạm vi thật rộng hơn: **cả ba** `SRS-NFR-07`/`08`/`09` cùng lệch ⇒ đồng bộ chung"* | `SRS:256`/`:257`/`:258` đều đổi | ✅ |
| *"`ADR-001` xếp `shadcn/ui + Tailwind` ở tầng **MẶC ĐỊNH** … ⛔ không phải CHỐT"* | `ADR-001:59` — hàng *Frontend & UI* nằm trong bảng **Tầng MẶC ĐỊNH** | ✅ |
| *"nên `SRS` nay ghi nhãn **LAI**, ⛔ cố ý không ghi CHỐT"* | `SRS:258` mở đầu bằng **`LAI`** | ✅ |
| *"tầng **MẶC ĐỊNH có đường lui**"* | ⚠️ **xung đột với `escalations.md` `E7` #2 của CHÍNH RUN NÀY** | ⚠️ **`W-2`** |

### 5.5 `000-Index.md:178` — hàng run-state ⚠️ **WARNING `W-1`**

| Mệnh đề | Đếm lại từ `git diff` thật | Kết quả |
|---|---|:--:|
| *"**21 điểm ở `SRS`**"* | `numstat` = `22 22` ⇒ 22 dòng đổi − 1 dòng `updated:` = **21** | ✅ **ĐÚNG** |
| *"**16 điểm ripple tầng 030**"* | Đếm cơ học = **14** (nội dung, ngoài `Specs-MOC`) / **15** (kể `Specs-MOC:13`) / **18** (kể 4 status flip) | ⚠️ **KHÔNG khớp** |
| *"**3 điểm MOC/Index**"* | `Specs-MOC:13` + `Index:96` + `Index:220` = 3, nhưng **thiếu chính hàng `Index:178`** ⇒ thật là **4** | ⚠️ **Thiếu 1** |
| *"**3 lô writer**"* | Lô 1 `business-analyst` · Lô 2a `security-auditor` · Lô 2b `architect` = **3** (Lô 3 là PM, Lô 4 là verify) | ✅ **ĐÚNG** |

### 5.6 `Specs-MOC.md` frontmatter — PM thêm `updated:` ✅ **ĐÚNG**

`created: 2026-08-30` + `updated: 2026-08-30`, thứ tự trường khớp mẫu của các file tầng 030 khác. ✅

---

## 6. Danh sách phát hiện

### 🔴 CRITICAL — **0**

⭐ ⛔ **Không có.** Cụ thể, cả 5 điều được cảnh báo là CRITICAL nếu vi phạm đều **KHÔNG vi phạm**: `55` đứng yên · `21` đứng yên · `C-10` vẫn mở · vendor billing vẫn `TBD` · `ADR-001:16`/`:70`/`:173` còn nguyên.

### 🟠 WARNING — 3

#### `W-1` · `docs/000-Index.md:178` — con số *"16 điểm ripple tầng 030"* ⛔ không đếm lại được

> **Nguyên văn**: *"**21 điểm ở `SRS` + 16 điểm ripple tầng 030 + 3 điểm MOC/Index**"*

**Vì sao sai** — enumerate đầy đủ 030 từ `git diff` (⛔ không trích từ `outline.md`):

| # | `file:line` | |
|:--:|---|---|
| 1–2 | `Endpoint-Preview-Export.md:201`, `:250` | Lô 2a |
| 3 | `Spec-Integration-Auth-Provider.md:190` | Lô 2a |
| 4–5 | `DB-Entity-Tenancy.md:96`, `:313` | Lô 2a |
| 6–7 | `Spec-Security-Threat-Model.md:293`, `:522` | Lô 2a |
| 8–9 | `SDD-Comic-Studio.md:457`, `:812` | Lô 2b |
| 10–11 | `ADR-006:257`, `:258` | Lô 2b |
| 12 | `ADR-010:177` | Lô 2b |
| 13 | `ADR-015:272` | Lô 2b |
| 14 | `ADR-002:85` | Lô 3 (PM) |
| *(15)* | `Specs-MOC.md:13` | *thuộc rổ MOC/Index* |
| *(+4)* | `ADR-001`…`ADR-004` `status:` flip | *frontmatter, ⛔ không phải "điểm nội dung"* |

⇒ **14** · **15** · **18** · **19** — ⛔ **không cách đếm nào ra `16`**. Con số `16` = `7 + 9` lấy từ header Lô 2a/2b của `outline.md`, nhưng bảng liệt kê của chính Lô 2b chỉ có **6 điểm nội dung + 4 status flip**, và `ADR-002:85` thuộc Lô 3 chứ ⛔ không thuộc rổ ripple.

**Kèm theo**: *"3 điểm MOC/Index"* bỏ sót **chính hàng `Index:178`** (một dòng MỚI trong `git diff`) ⇒ số thật là **4**.

> [!CAUTION]
> ⭐ Đây **đúng loại lỗi `E9`/`E10`** mà `K-1` dựng lên để chặn: **trích lại số từ nguồn thứ cấp (`outline.md`) thay vì đếm tại nguồn (`git diff`)** — và nó xảy ra ở chính dòng PM dùng để ghi số. Nó nằm ở `000-Index.md`, tài liệu **thường trực** nhất của kho.

**Đề xuất vá (1 dòng)**: `**21 điểm ở SRS + 14 điểm ripple nội dung tầng 030 (+ 4 ADR chuyển accepted) + 4 điểm MOC/Index**`.

#### `W-2` · `docs/000-Index.md:220` ⟷ `escalations.md` `E7` #2 — mâu thuẫn nội bộ CÙNG MỘT RUN

> **`000-Index.md:220`**: *"`ADR-001` xếp `shadcn/ui + Tailwind` ở tầng **MẶC ĐỊNH có đường lui**, ⛔ **không phải CHỐT**"*
>
> **`escalations.md` `E7` #2**: *"`shadcn/ui + Tailwind` chưa có **đường lui** lẫn **alternatives** — chỉ xuất hiện ở `ADR-001:58` và `:117`; `## Alternatives considered` ⛔ không cân nhắc UI kit nào khác"*

**Vì sao sai**: hai artifact của **cùng một run, cùng một ngày** khẳng định **ngược nhau** về **cùng một đối tượng**. Tại nguồn `ADR-001:131-138`, bảng Đường lui có 3 hàng và hàng frontend là *"**Nếu** Vite/React không đủ cho editor → chỉ đổi **frontend**"* — đó là đường lui cho **cả cụm frontend**, ⛔ **không** là đường lui riêng cho UI kit. `E7` #2 nói đúng ở mức chi tiết đó, và `E7` là hạng mục **report-only cố ý để lại**.

**Rủi ro thật**: `000-Index.md` là nơi lô sau đọc **đầu tiên**. Nó sẽ đọc ra *"shadcn có đường lui rồi"* và **đóng mất** một khoản nợ mà run này cố ý ghi nhận là **CHƯA đóng**.

**Đề xuất vá (1 mệnh đề)**: đổi thành *"ở tầng **MẶC ĐỊNH** (⛔ không phải CHỐT); đường lui chỉ có ở mức **đổi cả cụm frontend** — riêng UI kit ⛔ chưa có đường lui, xem `escalations.md` `E7` #2"*.

#### `W-3` · `docs/030-Specs/Architecture/ADR-006-RLS-Tenant-Context-Injection.md:270` — sót `TBD` cũ, tự mâu thuẫn trong CÙNG MỘT FILE

> **Nguyên văn `:270`** (bảng *"Đã quyết ở đâu"*):
> `` | Mua auth, ⛔ không tự viết (vendor `TBD`) | `D-12` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-03` · `SRS-NFR-08` | ``

**Vì sao sai**: chính lô này đã sửa `ADR-006:257` thành *"`SRS-NFR-08` phần **auth = MẶC ĐỊNH (Clerk)** theo `ADR-003`, ⛔ chưa mua"*. Cách `:270` chỉ **13 dòng**, file vẫn khẳng định `` vendor `TBD` ``. ⇒ **một file, hai phát biểu ngược nhau về cùng `SRS-NFR-08`**, và nó ⛔ **không** nằm trong bảng *Ripple* của `outline.md` (⛔ không ai kiểm).

⚠️ Đây là **đúng rủi ro đặc trưng của Shape B** mà brief tự nêu: *"sửa nửa vời ⇒ kho docs mâu thuẫn với chính nó"*.

**Đề xuất vá (1 dòng)**: `` | Mua auth, ⛔ không tự viết (vendor auth = MẶC ĐỊNH Clerk theo ADR-003, ⛔ chưa mua) | `D-12` | … | ``

### 💡 SUGGESTION — 4

#### `S-1` · Ba chỗ còn neo `b-2`/`T-27` vào `SRS-NFR-08` sau khi `SRS:456` đã đổi lý do

- `docs/030-Specs/Architecture/SDD-Comic-Studio.md:778` — *"Phụ thuộc `SRS-NFR-08` (vendor + nơi giữ secret)"*
- `docs/030-Specs/Schema/DB-Entity-Generation.md:486` — *"nó phụ thuộc `SRS-NFR-08` (vendor + nơi giữ secret)"*
- `docs/030-Specs/Security/Spec-Security-Threat-Model.md:86` — *"⚠️ Phụ thuộc `b-1` và `SRS-NFR-08`"*

`SRS:456` (`b-2`) nay quy lý do về **`ADR-002` điều 6 cấm SDK secret manager** + *"⭐ Đóng đúng nghĩa **cần một ADR MỚI**"*. ⛔ **Không phải lỗi cứng** — cột trace của `b-2` vẫn liệt kê `SRS-NFR-08`, và cả ba chỗ đều đã tự nói *"cần một ADR mới"*. Nhưng phần *"vendor"* của `SRS-NFR-08` nay ⛔ **không còn `TBD`** (auth = Clerk, storage = R2) ⇒ mệnh đề đã **trôi** so với tầng 020. `outline.md` xếp `SDD:778` và `DB-Entity-Generation:486` vào nhóm *"đã kiểm, đang đúng"* — em ⛔ không đồng ý hoàn toàn, nhưng **⛔ không đề nghị sửa trong run này** (thuộc `b-2`/BYOK, ngoài phạm vi gate).

#### `S-2` · `escalations.md` `E1` chỉ bảo vệ `ADR-001` — nên mở rộng cho `ADR-002`…`ADR-004`

Chú thích **trạng thái ĐẦU VÀO** y hệt còn ở: `ADR-002:16`, `:190` · `ADR-003:20`, `:174` · `ADR-004:23`, `:172`. Lô sau `diff` hai dòng sẽ thấy **6 chỗ nữa** trông như lệch và ⛔ `E1` hiện ⛔ không phủ chúng. Chi phí mở rộng = **1 dòng** trong `E1`, chặn được đúng cái `E1` sinh ra để chặn.

#### `S-3` · Lệnh kiểm RULE-001 sinh false positive

`grep -rc '\[\['` trên `docs/` ⛔ không ra 0, vì các dòng **phát biểu chính luật** (`000-Index.md:191`, `Requirements-MOC.md:78`) chứa chuỗi `[[...]]` trong ngoặc mã. Đề xuất chuẩn hoá lệnh kiểm thành `grep -rnE '\[\[[A-Za-z0-9./]' docs/` để tránh lô verify sau báo nhầm.

#### `S-4` · `K-5` ⛔ không thực sự được áp cho `000-Index.md`

`git diff` `000-Index.md` = `3 2`, ⛔ **không có hunk frontmatter**. `updated: 2026-08-30` đúng chỉ vì run `2026-08-30-brand-guidelines...` cùng ngày đã set. Lần sau khác ngày sẽ hỏng. Nên đưa `000-Index.md` vào checklist `K-5` tường minh.

---

## 7. Kết luận

### Bảng tổng

| | Số lượng | Chặn đóng run? |
|---|:--:|:--:|
| 🔴 CRITICAL | **0** | — |
| 🟠 WARNING | **3** (`W-1`, `W-2`, `W-3`) | ✅ **Có** |
| 💡 SUGGESTION | **4** (`S-1`…`S-4`) | ⛔ Không |

### Phán quyết: ⚠️ **NOT CLOSEABLE nguyên trạng** → ✅ **CLOSEABLE sau 3 patch một dòng của PM**

**Chất lượng lõi của lô là TỐT.** Việc khó nhất — đồng bộ 21 điểm ở `SRS` + 14 điểm ripple mà ⛔ không đóng hộ `C-10`, ⛔ không đóng hộ vendor billing, ⛔ không xê dịch `55` và `21`, ⛔ không chạm `ADR-001`, và giữ **bốn chỗ khoá số khớp cả bốn** — **đã làm đúng**. Toàn bộ thang đường lui và mọi con số spot-check đều truy được về `file:line` trong ADR nguồn; ⛔ **không phát hiện một chi tiết bịa nào**.

⭐ **Cả 3 WARNING đều nằm ở phần PM tự sửa, ⛔ không writer nào review** — đúng như dự đoán của brief. ⛔ **Không cần mở lại lô writer nào**; ba chỗ đều là sửa **một dòng**:

| # | `file:line` | Việc |
|:--:|---|---|
| 1 | `docs/000-Index.md:178` | Sửa `16 điểm ripple` → `14 điểm ripple nội dung (+4 ADR accepted)`; `3 điểm MOC/Index` → `4` |
| 2 | `docs/000-Index.md:220` | Bỏ/làm rõ mệnh đề *"có đường lui"* cho `shadcn/ui + Tailwind`, trỏ về `E7` #2 |
| 3 | `docs/030-Specs/Architecture/ADR-006-...md:270` | `` (vendor `TBD`) `` → `(vendor auth = MẶC ĐỊNH Clerk, ⛔ chưa mua)` |

Sau 3 patch trên, run **ĐỦ ĐIỀU KIỆN ĐÓNG**. `S-2` nên làm cùng lúc (1 dòng, chi phí gần 0, giá trị phòng ngừa cao).

### Ngân sách

**27/60 tool call.** ⛔ Không chạm trần. **Cả 4 tiêu chí được phủ đầy đủ**, ⛔ không có hạng mục nào bỏ dở.

---

_Created by TNMCORE-OS (context-auditor)_
_Author: trisjr_

---

## Verify pass 2

> [!NOTE]
> Instance **mới**, ⛔ chưa viết gì trước mục này. Phạm vi hẹp: **chỉ soi bản vá của PM** (`P-1`…`P-5`), ⛔ không verify lại toàn run — pass 1 đã kết luận **0 CRITICAL** và 4 tiêu chí PASS.
> ⛔ **READ-ONLY trên `docs/`** — mọi phát hiện dưới đây chỉ **báo cáo**, PM vá.
> ⭐ **Quy ước số dòng**: toàn bộ mục này dùng **số dòng post-image** (file hiện tại trên đĩa), ⛔ không dùng số pre-image. Pass 1 lẫn hai loại (`SDD:457` là pre-image, `:812` là post-image) — mục này ⛔ không kế thừa cách đó.

### Bảng kết quả nhanh

| # | Điểm soi | Kết quả |
|:--:|---|:--:|
| `P-1` | `000-Index.md:178` — bốn con số run-state | ❌ **FAIL** (1 con số sai) |
| `P-2` | `000-Index.md:220` — mệnh đề đường lui / alternatives | ✅ **PASS** |
| `P-3` | `ADR-006:270` — vendor auth = MẶC ĐỊNH Clerk | ✅ **PASS** |
| `P-4` | `escalations.md` `E1` — bảng 6 hàng `file:line` + `ADR-006:218` | ⚠️ **PASS có điều kiện** (bảng đúng 6/6, nhưng phần prose bao quanh sai dòng) |
| `P-5` | Bản vá có sinh mâu thuẫn MỚI không | ❌ **FAIL** (2 phát hiện mới) |

---

### `P-1` · `docs/000-Index.md:178` — ❌ **FAIL**

**Nguyên văn sau vá**: *"**21 điểm ở `SRS` + 14 điểm ripple nội dung tầng 030 + 4 ADR chuyển `accepted` + 4 điểm MOC/Index** (đếm cơ học từ `git diff` ngày 2026-08-30, ⛔ không trích lại)"*.

**Lệnh đã chạy** (⛔ không trích lại từ `outline.md` hay từ pass 1):

```
git diff --numstat
git diff -U0 -- docs/030-Specs/ docs/000-Index.md
git diff -U0 -- docs/030-Specs/API/Spec-Integration-Auth-Provider.md docs/030-Specs/Architecture/ADR-015-Job-Queue-In-Postgres.md
```

**Enumerate lại toàn bộ điểm nội dung tầng 030** (⛔ loại dòng frontmatter `updated:` và 4 dòng `status:`; `Specs-MOC` tính sang rổ MOC/Index):

| # | `file:line` (post-image) | Thuộc |
|:--:|---|---|
| 1–2 | `Endpoint-Preview-Export.md:201`, `:250` | Lô 2a |
| 3 | `Spec-Integration-Auth-Provider.md:190` | Lô 2a |
| 4–5 | `DB-Entity-Tenancy.md:96`, `:313` | Lô 2a |
| 6–7 | `Spec-Security-Threat-Model.md:293`, `:522` | Lô 2a |
| 8–9 | `SDD-Comic-Studio.md:458`, `:812` | Lô 2b |
| 10–11 | `ADR-006:257`, `:259` | Lô 2b |
| 12 | `ADR-010:177` | Lô 2b |
| 13 | `ADR-015:273` | Lô 2b |
| 14 | `ADR-002:85` | PM (close-step) |
| ⭐ 15 | `ADR-006:270` | ⭐ **PM — chính patch #3 của pass 1** |

⇒ **15**, ⛔ **không phải 14**.

**Kiểm chứng chéo bằng `numstat`** (mỗi file `030` đều có đúng 1 dòng `updated:` thêm mới ⇒ *số điểm nội dung = del − (1 nếu có flip `status:`)*):
`Endpoint-Preview-Export 3/2` → 2 · `Spec-Integration-Auth-Provider 2/1` → 1 · `ADR-001 2/1` → 0 · `ADR-002 3/2` → 1 · `ADR-003 2/1` → 0 · `ADR-004 2/1` → 0 · `ADR-006 4/3` → 3 · `ADR-010 2/1` → 1 · `ADR-015 2/1` → 1 · `SDD 3/2` → 2 · `DB-Entity-Tenancy 3/2` → 2 · `Spec-Security-Threat-Model 3/2` → 2. **Tổng = 15.** ✅ Hai cách đếm độc lập cùng ra 15.

**Vì sao phép cộng của PM hụt 1** — theo brief, PM khai `14 = 7 (Lô 2a) + 6 (Lô 2b) + 1 (ADR-002:85)`. *(Phép cộng này ⛔ không xuất hiện trong file nào; nguồn là brief, ⛔ không phải tài liệu repo.)* Hai số hạng đầu **ĐÚNG**: Lô 2a = 7 (hàng 1–7 ở trên) ✅, Lô 2b = 6 (hàng 8–13) ✅. Số hạng thứ ba **SAI**: PM ở close-step chạm **2** điểm nội dung chứ ⛔ không phải 1 — `ADR-002:85` **và** `ADR-006:270`.

⭐ **`ADR-006:270` chính là patch #3 mà pass 1 kê ở bảng remediation.** Bảng enumerate của pass 1 (`verdict.md:355-368`) liệt kê **14** hàng và ⛔ **không** có `:270` — đúng, vì lúc đó `:270` còn nguyên bản `` (vendor `TBD`) ``, và pass 1 gọi nó là `W-3`. Khi PM thi hành `W-3`, `:270` **trở thành điểm ripple thứ 15**. PM lấy nguyên con số `14` mà pass 1 đề xuất ở `verdict.md:445` và ⛔ **không đếm lại sau khi chính mình vá thêm**.

> [!CAUTION]
> ⭐ **Tình tiết tăng nặng, đúng như brief dự đoán.** Dòng này nay tự dán nhãn *"đếm cơ học từ `git diff` ngày 2026-08-30, ⛔ không trích lại"* — nhưng nó **chính là một lần trích lại**, từ nguồn thứ cấp là `verdict.md:445` của pass 1. Đây đúng anti-pattern `K-1`/`E9`/`E10` mà `W-1` dựng lên để chặn, **tái phát ở đúng dòng vừa được vá để chặn nó**, và nay ⛔ **khó phát hiện hơn** vì đã mang nhãn đã-kiểm.

**Ba con số còn lại — ✅ ĐÚNG cả ba** (bằng chứng dương):

| Mệnh đề | Đếm lại | |
|---|---|:--:|
| *"21 điểm ở `SRS`"* | `numstat SRS = 22 22` ⇒ 22 dòng đổi − 1 dòng frontmatter `updated:` = **21**. Patch của PM ⛔ không chạm `SRS` ⇒ số này ⛔ không đổi từ pass 1 | ✅ |
| *"4 ADR chuyển `accepted`"* | `git diff` cho đúng 4 hunk `-status: draft` / `+status: accepted`: `ADR-001`, `ADR-002`, `ADR-003`, `ADR-004`. ⛔ Không ADR nào khác flip | ✅ |
| *"4 điểm MOC/Index"* | `Specs-MOC.md:13` + `000-Index.md:96` + `000-Index.md:178` (hàng MỚI) + `000-Index.md:220` = **4**. Khớp `numstat`: `Specs-MOC 2/1` → 1 nội dung; `000-Index 3/2` → 3 điểm | ✅ |

**Mức**: 🟠 **WARNING** (`N-1`). ⛔ Không phải CRITICAL — nó ⛔ không làm hỏng một quyết định chịu lực nào; nhưng nó nằm ở `000-Index.md`, tài liệu **thường trực nhất**, và **chặn đóng run** theo đúng quy ước của pass 1.

**Đề xuất vá (1 token)**: `14 điểm ripple nội dung tầng 030` → `15 điểm ripple nội dung tầng 030`.

---

### `P-2` · `docs/000-Index.md:220` — ✅ **PASS**

**Lệnh đã chạy**: `sed -n '53,62p'`, `sed -n '131,140p'`, `sed -n '115,119p'`, `grep -n "^## \|^### "` trên `ADR-001-Backend-And-Frontend-Tech-Stack.md`; `sed -n '113,160p'` trên `escalations.md`.

**Mệnh đề 1 — *"đường lui của `ADR-001` chỉ có ở mức đổi cả cụm frontend"*** → ✅ **ĐÚNG**.
Bảng `### Đường lui đã ghi rõ (cho tầng MẶC ĐỊNH)` (`ADR-001:131`, thân bảng `:134-137`) có đúng **3 hàng**: `NestJS → Fastify` · `Drizzle → Kysely/pg` · *"Vite/React không đủ cho editor"* → *"**Chỉ đổi frontend**; API và hợp đồng không đổi"*. ⭐ Hàng thứ ba là **mức cụm**, ⛔ không tách riêng UI kit. Trong khi đó hàng `Frontend & UI` của tầng MẶC ĐỊNH (`ADR-001:59`) gộp **Vite + React + TS · TanStack Query · shadcn/ui + Tailwind** vào **một** ô ⇒ ⛔ **không có đường lui riêng cho UI kit**. Khớp nguyên văn `:220`.

**Mệnh đề 2 — *"riêng UI kit ⛔ chưa có ... alternatives"*** → ✅ **ĐÚNG**.
`## Alternatives considered` là `ADR-001:72`, thân chạy tới `:109` (mục kế `## Consequences` ở `:110`). Sáu phương án: **A** Python+FastAPI · **B** Go · **C** full-stack monolith · **D** Prisma thay Drizzle · **E** Next.js full-stack · **F** job runtime ra ngoài. ⭐ ⛔ **Không phương án nào cân nhắc một UI kit khác** (MUI / Mantine / Radix trần / Chakra…). Khớp nguyên văn `:220`.

**Mệnh đề 3 — còn mâu thuẫn với `E7` #2 không?** → ✅ **HẾT MÂU THUẪN** — `W-2` **đã đóng**.
`E7` #2 (`escalations.md:120`) phát biểu: *"`shadcn/ui + Tailwind` chưa có **đường lui** lẫn **alternatives**"*. `000-Index:220` sau vá phát biểu **cùng nội dung, cùng chiều**. ⭐ Câu *"tầng MẶC ĐỊNH có đường lui"* (nguồn của `W-2`) đã bị gỡ bỏ hoàn toàn.

**Link `[escalations.md E7 #2](./010-Planning/pm-runs/2026-08-30-dong-bo-srs-nfr-voi-adr/escalations.md)`** → ✅ **phân giải được**. File tồn tại; anchor ⛔ không được dùng (chỉ trỏ file + chú thích `E7 #2` bằng chữ) ⇒ ⛔ không có nguy cơ anchor gãy.

---

### `P-3` · `ADR-006-RLS-Tenant-Context-Injection.md:270` — ✅ **PASS**

**Lệnh đã chạy**: `sed -n '257p'`, `sed -n '270p'`, `sed -n '218p'`, `ls -la ./ADR-003-Auth-And-Billing-Vendor-Selection.md`.

| Kiểm | Kết quả |
|---|:--:|
| **Nhất quán `:270` ⟷ `:257`** (nguồn của `W-3`) | ✅ **ĐÃ NHẤT QUÁN**. `:257` = *"`SRS-NFR-08` phần **auth = MẶC ĐỊNH (Clerk)** theo `ADR-003`, ⛔ chưa mua; ⛔ phần **billing vẫn `TBD`**"*. `:270` = *"vendor auth = **MẶC ĐỊNH Clerk** theo `ADR-003`, ⛔ **chưa mua**"*. Cùng nhãn, cùng cảnh báo *chưa mua*. ⭐ `W-3` **đóng** |
| **Đường dẫn `./ADR-003-Auth-And-Billing-Vendor-Selection.md`** | ✅ **TỒN TẠI** — `ls` từ `docs/030-Specs/Architecture/` trả về file thật (19 433 byte). Relative path đúng, ⛔ không dùng wiki-link |
| **Cột trace `SRS-FR-03 · SRS-NFR-08` còn khớp cột 1?** | ✅ **CÒN KHỚP**. Hàng này là quyết định `D-12` *"Mua auth, ⛔ không tự viết"* — **phạm vi chỉ auth**. `SRS-NFR-08` là **requirement nguồn** (phủ cả auth lẫn billing), nên trace vẫn hợp lệ. Việc `:270` ⛔ không nhắc *"billing vẫn `TBD`"* như `:257` là **đúng phạm vi**, ⛔ không phải thiếu sót |

**Mệnh đề PM thêm về `ADR-006:218`** → ✅ **ĐÚNG NGUYÊN VĂN**. Dòng `:218` (mục `### (D) Bơm context ở tầng connection pool`, thuộc `## Alternatives`) có **đủ ba** lý do: **(i)** *"hosting/PaaS còn `TBD` (`ADR-002`, `SRS-NFR-07`)"* — lý do nay lạc hậu; **(ii)** *"suy biến về (C) và thừa kế trọn bốn vấn đề của (C)"*; **(iii)** *"đặt lớp bảo vệ vào một tiến trình mà test của Story AC ⛔ không chạm tới được"*. ⭐ Quyết định loại phương án (D) **đứng vững trên (ii) và (iii)** kể cả khi bỏ (i). Ghi chú của PM chính xác.

---

### `P-4` · `escalations.md` `E1` — ⚠️ **PASS có điều kiện**

**Lệnh đã chạy**: `grep -n "CHƯA QUYẾT"` trên `ADR-001`…`ADR-004`; `sed -n '22,25p'` trên `ADR-004`; `sed -n '14,17p'`, `sed -n '68,71p'`, `sed -n '171,174p'` trên `ADR-001`.

**Bảng 6 hàng của `E1` — ✅ ĐÚNG 6/6** (bằng chứng dương, kiểm từng hàng ở đúng số dòng):

| `file:line` khai báo | Nội dung thật tại đúng dòng đó | |
|---|---|:--:|
| `ADR-002:16` | `grep` ra `CHƯA QUYẾT` tại **đúng `:16`** — `` `SRS-NFR-07` (*"Hos…"*) … **`CHƯA QUYẾT` → `TBD`** `` | ✅ |
| `ADR-002:190` | `grep` ra tại **đúng `:190`** — hàng `Hosting / PaaS /…` | ✅ |
| `ADR-003:20` | `grep` ra tại **đúng `:20`** — *"Cái còn mở là…"* | ✅ |
| `ADR-003:174` | `grep` ra tại **đúng `:174`** — hàng `**Vendor a…`  | ✅ |
| `ADR-004:172` | `grep` ra tại **đúng `:172`** — hàng `**Vendo…` | ✅ |
| ⚠️ `ADR-004:23` | `sed -n '22,25p'` cho `:23` = *"Cái còn mở: **vendor** (`SRS-NFR-08` — …), **thời hạn signed URL**…"*. ⭐ **`grep "CHƯA QUYẾT"` trên `ADR-004` chỉ ra `:172`, ⛔ KHÔNG ra `:23`** | ✅ |

⭐ **Ghi chú tự phát hiện của PM về `ADR-004:23` là ĐÚNG** — dòng đó thật sự ⛔ không chứa cụm `CHƯA QUYẾT`, đúng số dòng, và vẫn cùng bản chất *"ảnh chụp trước quyết định"*. Đây là điểm sáng của bản vá: PM tự bắt được ngoại lệ của chính mình.

**⚠️ Nhưng phần prose bao quanh bảng thì SAI SỐ DÒNG** — xem `N-2` dưới.

---

### `P-5` · Bản vá có sinh mâu thuẫn MỚI không — ❌ **FAIL (2 phát hiện)**

**`grep -rn "16 điểm" docs/` và `grep -rn "3 điểm MOC" docs/`** → ✅ **SẠCH**. Hit duy nhất nằm ở **chính `verdict.md` này** (`:333`, `:334`, `:351`, `:353`, `:373`, `:445`) — đó là **trích dẫn của pass 1 về con số cũ**, ⛔ không phải con số đang sống. ⛔ **Không tài liệu sống nào (`000-Index`, `Specs-MOC`, tầng 030) còn sót `16 điểm` hay `3 điểm MOC`.**

**`000-Index.md:220` nói *"MẶC ĐỊNH"* — mâu thuẫn nội bộ?** → ✅ **KHÔNG**. Hàng nợ `#7` của cùng file cũng dùng nhãn `MẶC ĐỊNH` nhưng cho **`D-45` (polling 2s)** — chủ đề khác, ⛔ không giao nhau. `Design-MOC.md` ⛔ không có chỗ nào gán nhãn `CHỐT`/`MẶC ĐỊNH` cho UI kit.

**`outline.md` — `Lô 3`** → ⚠️ xem `N-4`. `grep -n "…\|điểm"` trên `outline.md` cho thấy **chuỗi `điểm` ⛔ KHÔNG xuất hiện ở đâu trong file** ⇒ ⛔ **không có phát biểu *"6 điểm"* nào để đối chiếu**. Bảng `## Lô 3 — Close-step (PM)` (`outline.md:121-128`) có **4 hàng**.

---

### 🟠 WARNING mới — 2

#### `N-1` · `docs/000-Index.md:178` — con số ripple nay là **15**, ⛔ không phải `14`

Toàn bộ bằng chứng ở `P-1`. **Chặn đóng run.** Vá: `14` → `15`.

#### `N-2` · Số dòng trỏ tới `ADR-001` bị lệch **+1** — và `E1` nay **tự mâu thuẫn với chính nó**

Toàn bộ tầng 030 được thêm một dòng `updated: 2026-08-30` ở **dòng 7** ⇒ mọi số dòng ≥ 7 dịch **+1**. Trạng thái file **hiện tại**:

| Nơi khai | Khai là | Thực tế tại dòng đó | Dòng đúng |
|---|:--:|---|:--:|
| `escalations.md` `E1` tiêu đề + bảng hàng 1 | `ADR-001:15` | ⛔ **DÒNG TRỐNG** (`:14` = `## Context`) | **`:16`** |
| `escalations.md` `E1` bảng hàng 2 | `ADR-001:172` | ⛔ **dòng phân cách bảng** `\|---\|---\|---\|` | **`:173`** |
| `escalations.md` `E1` đoạn cuối | `ADR-001:69` | hàng *"Compositor chạy trong `worker_threads`…"* — ⛔ **không phải** dòng chịu lực `b-6`/`b-7` | **`:70`** |
| ⭐ `000-Index.md:178` — **chính dòng vừa được vá** | `ADR-001:15`/`:172` | như trên | **`:16`/`:173`** |

> [!CAUTION]
> ⭐ **`E1` nay tự mâu thuẫn.** Bảng 6 hàng (`ADR-002:16`, `:190`, `ADR-003:20`, `:174`, `ADR-004:172`, `:23`) dùng số dòng **post-shift ĐÚNG** — đã kiểm 6/6 ở `P-4`. Nhưng **tiêu đề và prose của cùng mục `E1`** vẫn dùng số dòng **pre-shift** cho `ADR-001`. Hai nửa của một mục đếm theo hai hệ toạ độ khác nhau.
>
> ⚠️ Và mục `## 6` của pass 1 (`verdict.md:349`) đã viết đúng là `` `ADR-001:16`/`:70`/`:173` ``, brief của pass 2 cũng vậy. ⇒ **`E1` + `000-Index:178` là hai nơi duy nhất còn dùng số cũ.**

**Vì sao đáng chặn**: `E1` **tồn tại để làm rào chắn** — bảo lô sau *"⛔ đừng sửa dòng này"*. Một rào chắn trỏ vào **dòng trống** và **dòng phân cách bảng** thì ⛔ không bảo vệ được `ADR-001:16` và `:173` — đúng hai dòng nó sinh ra để bảo vệ. ⭐ Đây **cùng họ** với phát hiện của pass 2 run trước (callout trỏ sai cột bảng).

**Mức**: 🟠 **WARNING**. **Chặn đóng run.** Vá: `E1` (tiêu đề + 2 chỗ prose) và `000-Index.md:178` → `:16` / `:70` / `:173`.

### 💡 SUGGESTION mới — 2

#### `N-3` · Lệch `+1` cùng nguyên nhân còn ở các artifact của run — ⛔ không chặn

`E7` #1: `ADR-001:59`/`:60` → thật là **`:60`/`:61`**. `E7` #2: `ADR-001:58`/`:117` → thật là **`:59`** (hàng `Frontend & UI` chứa `shadcn/ui + Tailwind`) và **`:118`**; `## Alternatives considered (:71-107)` → thật là **`:72-109`**. `E7` #3: `ADR-015:15` → nhiều khả năng **`:16`** (⛔ chưa mở kiểm, ngoài phạm vi). `outline.md:126`: `000-Index.md:219` → nay là **`:220`**; `outline.md:134`: `SDD:457`, `:811` là số **pre-image**.
⭐ **Không chặn** — đây là artifact của run (⛔ không phải tài liệu sống), và ⛔ không đóng vai rào chắn như `E1`. Nhưng nếu PM vá `N-2` thì nên quét luôn một lượt: nguyên nhân giống hệt.

#### `N-4` · `outline.md` `Lô 3` ⛔ không phản ánh khối lượng PM thật sự làm

Bảng `## Lô 3 — Close-step (PM)` có **4 hàng** (`Specs-MOC:12` · `000-Index:96` · `000-Index:219` · `escalations.md`). Thực tế PM chạm **7** chỗ: 4 hàng đó **+ `000-Index:178` (hàng run-state MỚI) + `ADR-002:85` + `ADR-006:270`**. ⭐ Ghi nhận trung thực: **chuỗi *"6 điểm"* ⛔ KHÔNG tồn tại trong `outline.md`** (`grep` chuỗi `điểm` ⛔ không ra hit nào) ⇒ ⛔ không có phát biểu nào để bác. Vấn đề thật là bảng **thiếu 3 hàng**. ⛔ Không chặn — `outline.md` là kế hoạch, `git diff` mới là nguồn sự thật.

#### *(kèm)* Ghi nhận, ⛔ không tính là phát hiện — `Design-MOC.md:51`

`DS-006` mô tả `Components.md` có *"ánh xạ **shadcn**/Radix"* cho 16 component. ⇒ Design System **đã neo vào shadcn** rồi, trong khi `000-Index:220` ghi UI kit mới ở tầng **MẶC ĐỊNH** và ⛔ **chưa có đường lui**. ⛔ **Không mâu thuẫn** (`Design-MOC` ⛔ không hề gọi shadcn là `CHỐT`), nhưng nó nâng **giá thật** của món nợ mà `:220` mô tả là *"để mở có chủ đích"*. Đáng thêm một vế vào hàng nợ khi có dịp.

---

### Bằng chứng dương — cái gì đã kiểm và ✅ **ĐÚNG**

1. `ADR-001:16`/`:70`/`:173` **còn nguyên**, ⛔ không bị bản vá đụng vào (`git diff ADR-001` chỉ có 2 hunk: `status:` và `updated:`).
2. **4 hunk `status: draft → accepted`** đúng `ADR-001`…`ADR-004`, ⛔ không dư ADR nào.
3. `E1` bảng 6 hàng: **6/6 đúng dòng, đúng nội dung**, kể cả ngoại lệ `ADR-004:23` PM tự khai.
4. `ADR-006:218` có **đủ (i)/(ii)/(iii)** — mệnh đề PM thêm chính xác.
5. `ADR-006:257` ⟷ `:270` **nhất quán** ⇒ `W-3` đóng; đường dẫn `./ADR-003-…md` **tồn tại thật**; cột trace `SRS-NFR-08` vẫn hợp lệ.
6. `ADR-001` bảng đường lui (3 hàng) + `Alternatives` (A–F) **xác nhận đúng** cả hai mệnh đề của `000-Index:220` ⇒ `W-2` đóng.
7. Ba trong bốn con số của `000-Index:178` (**21** `SRS` · **4** `accepted` · **4** MOC/Index) **đếm lại ra đúng**.
8. `grep "16 điểm"` / `"3 điểm MOC"` trên `docs/`: ⛔ **0 hit ở tài liệu sống**.
9. `Design-MOC.md` / `000-Index.md` ⛔ **không có mâu thuẫn nhãn `MẶC ĐỊNH`** nào với `:220`.

---

### Kết luận pass 2

| | Số lượng | Chặn đóng run? |
|---|:--:|:--:|
| 🔴 CRITICAL mới | **0** | — |
| 🟠 WARNING mới | **2** (`N-1`, `N-2`) | ✅ **Có** |
| 💡 SUGGESTION mới | **2** (`N-3`, `N-4`) | ⛔ Không |

**Phán quyết: ⚠️ NOT CLOSEABLE nguyên trạng → ✅ CLOSEABLE sau 2 patch một dòng.**

| # | `file:line` | Việc |
|:--:|---|---|
| 1 | `docs/000-Index.md:178` | `14 điểm ripple nội dung` → **`15`**; đồng thời `ADR-001:15`/`:172` → **`:16`/`:173`** |
| 2 | `escalations.md` `E1` (tiêu đề · bảng hàng 1–2 · đoạn cuối) | `ADR-001:15`/`:172`/`:69` → **`:16`/`:173`/`:70`** |

> [!IMPORTANT]
> ⭐ **Hai patch này ⛔ KHÔNG tự làm sai lại con số** — đây chính là cái bẫy đã sinh ra `N-1`:
> `000-Index.md:178` **đã** nằm trong rổ *"4 điểm MOC/Index"* (sửa lại nó ⛔ không tạo điểm thứ 5), và `escalations.md` nằm ở `010-Planning/pm-runs/`, ⛔ **không thuộc** rổ ripple tầng 030 lẫn rổ MOC/Index. ⇒ Sau hai patch, cả bốn con số **đứng yên**: `21 · 15 · 4 · 4`.

**Chất lượng bản vá — nhận định cân bằng.** 3/3 hạng mục pass 1 giao đều **đúng nội dung** (`W-1` đúng hướng nhưng lệch 1 đơn vị, `W-2` và `W-3` đóng sạch), và PM còn **tự phát hiện** ngoại lệ `ADR-004:23` — dấu hiệu đọc thật, ⛔ không đoán. Hai WARNING còn lại đều là **lỗi đếm/toạ độ**, ⛔ không lỗi phán đoán kiến trúc: một là hệ quả của việc chính bản vá làm thay đổi cái nó đang đếm, một là hệ quả của dòng `updated:` mà run này chèn vào. ⛔ **Không cần mở lại lô writer nào.**

### Ngân sách pass 2

**22/25 tool call.** ⛔ Không chạm trần. Cả 5 điểm `P-1`…`P-5` được phủ đầy đủ, ⛔ không hạng mục nào bỏ dở.

---

_Verify pass 2 — created by TNMCORE-OS (context-auditor)_
_Author: trisjr_

---

## ✅ Đóng run — PM ghi sau verify pass 2

> [!IMPORTANT]
> ⭐ Mục này ghi **sau** khi pass 2 kết luận *"NOT CLOSEABLE nguyên trạng"*. Kết luận đó **đúng tại thời điểm nó được viết**; PM đã thi hành các patch bên dưới. ⛔ Đừng dừng ở dòng cuối của pass 2.

| Phát hiện | Patch đã thi hành | Vị trí |
|---|---|---|
| `N-1` — số ripple phải là **15**, ⛔ không phải `14` | Sửa thành `15`; **tự đếm lại**: Lô 2a `7` + Lô 2b `6` + PM `2` (`ADR-002:85` **và** `ADR-006:270`) = **15** | `000-Index.md:178` |
| `N-2` — `E1` dùng toạ độ **pre-shift**; rào chắn trỏ vào **dòng trống** | Đổi `:15`→`:16`, `:172`→`:173`, `:69`→`:70` ở **6 chỗ** (mục lục · tiêu đề · prose · 2 hàng bảng · câu `:70`); thêm callout giải thích **nguồn của dịch `+1`** là `updated:` chèn ở dòng 7 | `escalations.md` `E1` · `000-Index.md:178` |
| `N-3` — lệch `+1` lan sang `E7` | Verify tại nguồn rồi sửa: shadcn `:59` + `:118` · `pnpm workspace` `:60` · `ESLint boundary` `:61` · `## Alternatives considered` `:72-109` (**sáu** phương án A–F) | `escalations.md` `E7` |
| `N-4` — bảng `Lô 3` thiếu hàng | Mở rộng **4 → 8 hàng**, tách cột *Nguồn* để phân biệt hạng mục **trong plan** với hạng mục **do chính run sinh ra** | `outline.md` §Lô 3 |

**PM tự nghiệm thu sau patch** (chạy thật, kết quả rỗng = đạt):

```
grep -rn "14 điểm ripple\|16 điểm ripple\|3 điểm MOC" docs/000-Index.md docs/030-Specs/ docs/020-Requirements/   → rỗng ✅
grep -rn "ADR-001:15\b\|ADR-001:172\|ADR-001:69" docs/000-Index.md …/escalations.md                            → rỗng ✅
```

> [!NOTE]
> `outline.md` **cố ý giữ** toạ độ pre-shift ở `K-4`, `A3`, `A4` — đó là **ảnh chụp tại thời điểm lập plan**, và `K-4` nay mang chú thích chỉ sang toạ độ post-shift. Cùng nguyên tắc mà `E1` dùng để bảo vệ `ADR-001` `## Context`.

⇒ **KẾT LUẬN: ✅ CLOSEABLE — run ĐÓNG.** 0 CRITICAL · 5 WARNING đã vá hết · 4 SUGGESTION còn mở có chủ đích (`S-1`, `S-3`, `S-4` của pass 1 — đã ghi nhận, ⛔ không thuộc phạm vi gate).

_Đóng bởi TNMCORE-OS (PM) — 2026-08-30_
