# Verdict: 2026-08-30-brand-guidelines-va-design-system-comic-studio

> **Trạng thái: ✅ ĐÓNG ĐƯỢC** — sau **verify pass 2** (2026-08-30). Cả **2 CRITICAL đã đóng**, kiểm lại bằng đúng phép đếm của pass 1.
> Lịch sử: **pass 1** → 2 CRITICAL · 4 WARNING · 3 SUGGESTION → *Quay lại Bước 5*. **pass 2** → 2 CRITICAL **đóng**, 1 WARNING **đóng**, **1 WARNING MỚI** phát sinh từ chính bản vá (⛔ không chặn), 3 WARNING + 3 SUGGESTION **còn treo** (⛔ không chặn).
> ⛔ **Mô tả lỗi gốc ⛔ không bị xoá** — mọi mục đã đóng đều giữ nguyên văn lỗi cũ kèm bằng chứng đóng.

| Khía cạnh | Trạng thái |
|-----------|-----------|
| Completeness | **9/9 hạng mục** có mặt. Frontmatter đủ trường, `id` đúng `DS-001`…`DS-006` như outline cấp cứng. `updated: 2026-08-30` đã bump ở **cả hai** file sửa (`Glossary.md`, `000-Index.md`) — xác nhận bằng `git diff`. Mục lục + Tài liệu tham khảo đủ ở 7/7 file mới. |
| Correctness | **`V-1`…`V-8` PASS toàn bộ**, mỗi mục có bằng chứng cơ học bên dưới. ⭐ **Tính lại 15/27 hàng contrast — khớp tuyệt đối, delta 0.00**, ⛔ 0 sai ngưỡng PASS/FAIL. Mọi trích dẫn nguyên văn `ADR-001` / `SDD-HG-01.1` / `API-HG-6` đã đối chiếu về tận file nguồn — ⛔ 0 câu bịa. **2 CRITICAL** là lỗi **đếm sai**, ⛔ không phải lỗi nội dung kỹ thuật — ✅ **cả hai đã đóng ở pass 2**. |
| Coherence | ⛔ **0 mâu thuẫn giữa 6 file.** Hợp đồng token ⛔ không bị vi phạm: hex chỉ tồn tại ở `Color-Tokens.md` (144 hit) và **0 hit ở 5 file kia**; `--space-*` chỉ ở `Spacing-And-Layout.md`; `--text-*` chỉ ở `Typography.md`. `K-8` PASS — `theme.extend` **0 hex**, toàn `var(--…)`. **33/33 mục Glossary mới** trỏ tới định nghĩa **có thật**; 90 headword cũ **⛔ không bị đụng một ký tự** (`git diff`: dòng bị xoá duy nhất của cả file là `-updated: 2026-08-29`). |
| Connectivity | **Mọi link tương đối trong 9 file phân giải được — 0 link gãy.** ⛔ 0 wiki-link thật. ⛔ **0 file orphan**: cả 6 file được `Design-MOC.md` trỏ tới và mỗi file trỏ ngược `../Design-MOC.md`. Bảng link bắt buộc của outline **đạt đủ**. **`K-1`…`K-14`: 14/14 PASS.** |

---

## CRITICAL — ✅ CẢ HAI ĐÃ ĐÓNG (xác nhận ở **verify pass 2**)

> ⛔ **Mô tả lỗi gốc giữ nguyên bên dưới để truy vết** — ⛔ không xoá lịch sử. Bằng chứng đóng ghi ngay sau mỗi mục, kiểm bằng **đúng phép đếm đã dùng ở pass 1**.

- ⭐ **`docs/040-Design/Design-System/Color-Tokens.md:400` — tiêu đề khẳng định SAI SỰ THẬT về chính bảng ngay dưới nó.**
  Tiêu đề: `### ⛔ Hai màu KHÔNG đạt 3:1 — và vì sao vẫn được dùng`. Bảng bên dưới (dòng **404–406**) có **BA** hàng, ⛔ không phải hai: `#E2E8F0` (1.23:1) · `#CBD5E1` (1.48:1) · `#94A3B8` (2.56:1).
  Đếm cơ học: `sed -n '402,408p' | grep -c '^| \`#'` → **3**.
  ⚠️ Đây là hàng `#94A3B8` (chữ disabled) — hàng **mang hệ quả a11y lớn nhất** trong ba hàng — bị tiêu đề đếm rơi ra ngoài. Người đọc lướt tiêu đề sẽ tưởng chỉ có hai màu bị loại trừ.
  ✅ **ĐÃ ĐÓNG.** `Color-Tokens.md:400` nay đọc `### ⛔ **Ba màu** KHÔNG đạt 3:1 — và vì sao vẫn được dùng`. Đếm lại bảng phụ: header `404`, separator `405`, **3** hàng dữ liệu `406–408` — khớp tiêu đề mới. *(Số dòng dịch +2 so với pass 1 vì callout mới chèn ở `402`.)* `grep -c '❌'` toàn file vẫn = **0**; bảng audit vẫn chạy đúng `1…27`.

- ⭐ **`docs/040-Design/Design-MOC.md:48` + `docs/000-Index.md:119` — PM khẳng định sai cấu trúc bảng contrast, ở HAI file.**
  Cả hai ghi: *"**27 hàng audit contrast có số**, gồm 3 hàng **FAIL có chủ ý**"*.
  Kiểm cơ học trên `Color-Tokens.md`:
  - Bảng audit đánh số chạy đúng `1 2 3 … 27` — **27 hàng**;
  - `grep -c '❌'` trên toàn file → **0**;
  - toàn bộ 27 hàng đều mang **✅**.
  ⇒ **⛔ Không hàng nào trong 27 hàng đó FAIL.** Ba màu ⛔ không đạt ngưỡng nằm ở một **bảng KHÁC** (`Color-Tokens.md:400–406`) và ⛔ **không được đánh số trong 27**. Phát biểu đúng là *"27 hàng đều đạt + 3 màu ⛔ không đạt 3:1 được liệt kê riêng kèm phạm vi được phép dùng"*.
  ⚠️ Đây **⛔ không cùng gốc** với CRITICAL #1: sửa tiêu đề `Hai` → `Ba` **⛔ không** làm câu của PM đúng lên, vì lỗi của PM là **gộp nhầm hai bảng làm một**. Phải sửa **cả ba chỗ**.
  ⚠️ Ghi nhận: đây đúng là chỗ brief cảnh báo — **file PM ⛔ không có ai khác nhìn vào**. Hai câu này là **câu tóm tắt duy nhất** về bảng contrast mà một agent sau sẽ đọc thay vì mở `Color-Tokens.md`.
  ✅ **ĐÃ ĐÓNG — cả hai chỗ, đọc lại nguyên văn:**
  - `Design-MOC.md:48` → *"**27 hàng audit contrast có số — cả 27 đều ĐẠT ngưỡng**; riêng **3 màu cố ý KHÔNG đạt 3:1** nằm ở một **bảng tách biệt**, kèm phạm vi hẹp được phép dùng"*.
  - `000-Index.md:119` → *"**27 hàng audit contrast có số — cả 27 đều ĐẠT**; 3 màu cố ý không đạt 3:1 nằm ở **bảng tách biệt** kèm phạm vi hẹp"*.
  ⇒ Hai câu nay **phát biểu đúng cấu trúc**: 27 hàng ĐẠT, ba màu ⛔ không đạt ở bảng **tách biệt**. PM còn thêm một callout chặn tái phát tại `Color-Tokens.md:402` (*"⛔ Đừng gộp hai bảng khi trích dẫn"*) — đúng hướng, ⚠️ **nhưng bản thân callout có một lỗi trỏ cột, xem WARNING mới bên dưới**.

---

## WARNING

- 🆕 **`docs/040-Design/Design-System/Color-Tokens.md:402` — callout MỚI của PM trỏ SAI cột.** *(phát hiện ở verify pass 2; đây là văn bản mới chưa ai kiểm)*
  Callout viết: *"...chỉ hợp lệ trong **phạm vi hẹp đã ghi ở cột cuối**"*.
  Header bảng ngay dưới (`:404`): `| Màu | Nền | Tỷ lệ | Được dùng cho | ⛔ CẤM dùng cho |` ⇒ **cột cuối là *"⛔ CẤM dùng cho"*** — cột **phạm vi BỊ CẤM**. Phạm vi **được phép** nằm ở **cột 4** (*"Được dùng cho"*).
  ⇒ Callout trỏ người đọc sang cột mang nghĩa **ngược lại**. ⛔ Không phải lỗi nội dung (bảng vẫn đúng, ý callout vẫn đúng) nên ⛔ không nâng lên CRITICAL, nhưng sửa `cột cuối` → `cột *Được dùng cho*` là một chữ.
  ⚠️ Đáng ghi nhận: câu tóm tắt PM viết ở `Design-MOC.md:48` (*"kèm phạm vi hẹp được phép dùng"*, ⛔ không nêu cột) thì **đúng** — chỉ riêng callout tại nguồn sai.

- ✅ **ĐÃ ĐÓNG — `Components.md` nay đã được commit.** `git status` chỉ còn **đúng một dòng**: ` M docs/030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md`. `DS-006` nằm trong commit `5d8eba4`; ⭐ **xác nhận `ADR-001` ⛔ KHÔNG có mặt trong cả `4e7c3af` lẫn `5d8eba4`** (kiểm bằng `git show --stat` từng commit) ⇒ file của Founder được giữ ngoài scope đúng như `E1`.
  *(Mô tả gốc: `Components.md` là deliverable duy nhất còn untracked, ⛔ không thể đóng run khi nó chưa vào lịch sử.)*

- **`outline.md` §*Hạng mục 7* — chuẩn nghiệm thu của Lô 5 dựng trên baseline SAI.** ⏳ **CHƯA xử lý** (`outline.md:109` vẫn nguyên văn *"append một nhóm mới vào cấu trúc 10 nhóm sẵn có. ⛔ Không sửa 69 thuật ngữ đang có."*).
  Outline ghi *"append một nhóm mới vào cấu trúc **10 nhóm** sẵn có"* và *"⛔ **Không sửa 69 thuật ngữ** đang có"*. Thực tế trước run: **90 thuật ngữ** (123 − 33 = 90), 10 nhóm. Con số `69` được chép lại từ `000-Index.md` bản cũ vốn đã lạc hậu.
  ⇒ ⛔ **Không gây thiệt hại** — `git diff` chứng minh Lô 5 giữ nguyên đủ **90** headword. Nhưng tiêu chí *"⛔ không sửa 69 thuật ngữ"* **⛔ không kiểm được** vì con số sai. PM đã tự sửa đúng ở `000-Index.md:157` (`123 thuật ngữ, 11 nhóm`, kèm ghi rõ *"đếm cơ học … ⛔ không trích lại"* — cách xử lý đúng), nhưng **outline vẫn còn số cũ**.

- **`docs/040-Design/Design-MOC.md:17` mâu thuẫn với `Design-MOC.md` §*Còn thiếu gì* (dòng 76–78) — trong cùng một file.** ⏳ **CHƯA xử lý** (đọc lại `:17` ở pass 2 — vẫn nguyên văn *"Ba artifact còn lại"*).
  Dòng 17: *"**Ba** artifact còn lại của Phase 3 — **Wireframes**, **User Flow**, **UI Specs** — thuộc run sau"*.
  Bảng §*Còn thiếu gì* lại liệt kê **ba thư mục**: `Wireframes/` (76) · `Specs/` (77 — User Flow **+** UI Spec) · **`Assets/`** (78 — Images, Icons, Illustrations).
  ⇒ `Assets/` là hạng mục **thứ tư** ⛔ không được câu ở dòng 16 tính đến. Hai cách đếm cùng ra *"ba"* nhưng **đếm hai thứ khác nhau** (artifact vs thư mục), che mất `Assets/`.

- **`docs/040-Design/Design-MOC.md:32` — hàng quan trọng nhất của bảng *"Đọc theo thứ tự nào"* trỏ SAI đích.** ⏳ **CHƯA xử lý** (đọc lại `:32` ở pass 2 — vẫn là `[Foundations](#1-design-system--6-file)`).
  Hàng *"AI assist sắp sinh code UI"* viết `[Foundations](#1-design-system--6-file)` — trỏ vào **anchor trong chính MOC**, ⛔ không trỏ `./Design-System/Foundations.md`. Cả **4 hàng còn lại** của bảng đều trỏ thẳng file.
  ⇒ ⛔ Không phải link gãy (anchor phân giải được), nhưng độc giả đích số một của cả tầng — AI assist — làm theo chỉ dẫn *"đọc Foundations trước tất cả"* sẽ **rơi vào một cái bảng**, ⛔ không vào tài liệu.

*(Khoản `Components.md` chưa commit đã chuyển lên đầu mục này với trạng thái ✅ ĐÃ ĐÓNG.)*

---

## SUGGESTION

- **Token budget của tầng 040 đã tới ngưỡng cần chú ý.** Sáu file ≈ **208 KB / 2 093 dòng** (`Components.md` 55 KB là file lớn nhất). Một agent nạp cả sáu file tốn **~55–70k token** trước khi viết dòng code đầu tiên. Bảng *"Đọc theo thứ tự nào"* của MOC đã là biện pháp giảm tải đúng hướng — đề xuất **nói thẳng trong MOC rằng ⛔ không cần nạp cả sáu**, chỉ `Foundations.md` (27 KB) + đúng một file theo việc đang làm.
- **Cân nhắc rút một `Template-Design-System.md`.** Sáu file tự dựng cấu trúc vì `999-Resources/Templates/` ⛔ không có khuôn phù hợp (PM đã ghi đúng vào *Nợ kỹ thuật* mục 8 của `000-Index.md`). Cấu trúc sáu file này **rất nhất quán** (Mục lục → nội dung → Tài liệu tham khảo; số mục lục = số H2 − 1 ở **cả sáu** file) ⇒ đã đủ ổn định để rút khuôn.
- **`Foundations.md` §*Cách kiểm* nên ghi rõ `K-4` và `K-7` là kiểm THỦ CÔNG.** 12/14 mục chạy được bằng `grep`; riêng `K-4` (*"liệt kê mọi số có đơn vị"*) và `K-7` (*"với mỗi token nền, tìm token chữ đi kèm"*) cần đọc bằng mắt. Ghi nhãn giúp người nghiệm thu sau ⛔ không tưởng đã tự động hoá được 14/14.

---

## Bằng chứng cho các mục báo PASS

> ⚠️ Ghi ở đây vì một verdict báo PASS mà ⛔ không nêu **lệnh đã chạy** thì ⛔ không kiểm chứng được.

**⭐ Bảng contrast — tính lại 15/27 hàng bằng công thức relative luminance WCAG** (sRGB linearize, hệ số `0.2126/0.7152/0.0722`, làm tròn **xuống** 2 chữ số), qua `awk`:

| Hàng | Cặp màu | Lô 2 khai | Em tính lại | Δ |
|:--:|---|:--:|:--:|:--:|
| 1 | `#0F172A` / `#FFFFFF` | 17.85 | 17.8525 | **0.00** |
| 4 | `#0F172A` / `#E2E8F0` | 14.48 | 14.4815 | **0.00** |
| 7 | `#FFFFFF` / `#4F46E5` | 6.28 | 6.2875 | **0.00** |
| 10 | `#FFFFFF` / `#DC2626` | 4.82 | 4.8294 | **0.00** |
| 11 | `#B91C1C` / `#FEF2F2` | 5.91 | 5.9146 | **0.00** |
| 13 | `#92400E` / `#FFFBEB` | 6.83 | 6.8370 | **0.00** |
| 14 | `#FFFFFF` / `#B45309` | 5.02 | 5.0216 | **0.00** |
| 16 | `#FFFFFF` / `#64748B` | 4.75 | 4.7588 | **0.00** |
| 17 | `#15803D` / `#F0FDF4` | 4.79 | 4.7914 | **0.00** |
| 18 | `#FFFFFF` / `#15803D` | 5.01 | 5.0156 | **0.00** |
| 21 | `#64748B` / `#FFFFFF` | 4.75 | 4.7588 | **0.00** |
| 23 | `#4F46E5` / `#F8FAFC` | 6.00 | 6.0094 | **0.00** |
| 24 | `#DC2626` / `#FEF2F2` | 4.41 | 4.4148 | **0.00** |
| 25 | `#B45309` / `#FFFBEB` | 4.84 | 4.8424 | **0.00** |
| 26 | `#64748B` / `#F1F5F9` | 4.34 | 4.3439 | **0.00** |

**⭐ Kiểm câu PM viết về chính phạm vi em đã làm** (`000-Index.md:218`, nợ #4, hạ **Trung bình → Thấp**) — PM ghi: *"Verify pass đã **tính lại độc lập 15/27 hàng** (chọn mọi hàng sát ngưỡng: 4.34 · 4.41 · 4.75 · 4.79 · 4.82) — **khớp delta 0.00, 0 sai ngưỡng**. Vẫn nên chạy lại bằng công cụ tự động khi init cho **12 hàng còn lại**…"*.
⇒ ✅ **⛔ KHÔNG overclaim — mô tả đúng.** `15/27` đúng số hàng em tính (1·4·7·10·11·13·14·16·17·18·21·23·24·25·26); `12 hàng còn lại` = 27 − 15 ✓; cả năm giá trị sát ngưỡng liệt kê đều nằm trong bộ em chạy; `delta 0.00` và `0 sai ngưỡng` đúng nguyên văn kết quả. PM cũng **giữ đúng phần chưa kiểm** (12 hàng còn lại · màu chồng alpha · text trên ảnh preview) thay vì tuyên bố đã phủ hết ⇒ mức **Thấp** là hợp lý.
⚠️ **Sắc thái duy nhất cần biết** (nghiêng về phía **có lợi cho việc kiểm**, ⛔ không phải overclaim): trong 12 hàng *"còn lại"* có **2 hàng thực chất đã được phủ** vì trùng đúng cặp màu với hàng em đã tính — hàng **27** (`#15803D`/`#F0FDF4`) trùng hàng 17, và hàng **22** (`#4F46E5`/`#FFFFFF`) trùng hàng 7. ⇒ Trên thực tế **17/27 hàng** đã có số kiểm chứng; con số `15` PM ghi là **thận trọng**, ⛔ không thổi phồng.

Đã cố ý chọn **mọi hàng sát ngưỡng**: hàng 24 (`4.41`) và 26 (`4.34`) đối chiếu ngưỡng **3:1** phi-text ⇒ ✅ **đúng**; hàng 16/21 (`4.75`), 17 (`4.79`), 10 (`4.82`) đối chiếu **4.5:1** ⇒ ✅ **đúng**. ⛔ **0 sai ngưỡng PASS/FAIL.** Hai hàng đảo chiều nhau (16 và 21, cùng cặp `#64748B`/`#FFFFFF`) khai **cùng một số** ⇒ nội bộ nhất quán. ⇒ **Lô 2 tính tay chính xác.**

| Mã | Kết luận | Bằng chứng |
|---|---|---|
| **`V-1`** | ✅ PASS | Hai H2 riêng: `Typography.md:113` *Hệ 1 — Font UI*, `:205` *Hệ 2 — Font render vào ảnh*. Có H3 nguyên văn *"Nó ⛔ KHÔNG phải CSS variable — nó là **tham số config của `apps/api`**"* kèm bảng ⛔ **Cấm**: *"khai thành CSS variable · đưa vào Tailwind theme · nạp bằng webfont ở `apps/web`"*. `R-1` (`:245`) = **đơn trị**, *"⛔ không dấu phẩy, ⛔ không generic family"*. |
| **`V-2`** | ✅ PASS | `grep` 20 tên họ font phổ biến (Inter, Roboto, Noto, Be Vietnam, IBM Plex, Geist…) trên **cả 6 file** → chỉ **3 hit**, tất cả ở `Typography.md:130,145` và đều là `system-ui`/`sans-serif` **của font UI** (hệ được phép fallback). Ô font render: `Typography.md:217` `⛔ TBD` · chủ **Architect + Founder** · *"sau MVP0, trước gate `G1-e`"*. ⛔ **0 lấn quyền `ADR-013`.** |
| **`V-3`** | ✅ PASS | `grep -oE '\-\-[a-z][a-z0-9-]*' ADR-001` → ⛔ **0 hit**. `ADR-001` chỉ chốt *"shadcn/ui + Tailwind CSS"* (dòng 58) và ⛔ **không nêu một tên biến CSS nào** — đúng như `Foundations.md:113–114` tự phát biểu. Nhãn *"quyết định Phase 3"* xuất hiện **8·1·4·8·7·7** lần trên sáu file. `K-9` PASS. |
| **`V-4`** | ✅ PASS | `Components.md:245` `HG-C1` cấm *"Duyệt cả trang"* / bulk / batch approve (neo `API-HG-6`, đã verify tại `030-Specs/API/Endpoint-Human-Gates.md:165`). `Components.md:249` `HG-C5` cấm **mọi control pre-selected**, trích **nguyên văn** `SDD-HG-01.1` — đối chiếu `SDD-Comic-Studio.md:412`: **khớp từng chữ**. ⛔ Không component nào trong `C-01`…`C-16` là bulk approve. |
| **`V-5`** | ✅ PASS **hai chiều** | `Brand-Guidelines.md:191–195` liệt kê **đích danh** cả bốn: badge *"đã kiểm bản quyền"* · icon **shield**/`shield-check`/tick *"verified"* · nhãn *"Original"* · messaging *"an tâm về bản quyền"* — cộng thêm hàng 5 (điểm rủi ro / % tương đồng). `Components.md:346` cấm **mọi dashboard copyright detection**. **Chiều ngược lại**: chạy `K-5` (`grep` 9 từ khoá trên **toàn** `docs/040-Design/`) → mọi hit đều là **câu cấm** hoặc **bề mặt takedown** (nghĩa vụ pháp lý). ⛔ **0 chỗ vô tình đề xuất.** |
| **`V-6`** | ✅ PASS | `C-10` **AI-disclosure indicator** ở `Components.md:75` (inventory, 5 surface) + đặc tả `:105–115` với `AD-1`…`AD-3`; `AD-2` cấm mọi biến thể ẩn/tắt được. `Brand-Guidelines.md:218` đánh dấu ✅ **BẮT BUỘC** (`SRS-FR-40`, CHỐT). |
| **`V-7`** | ✅ PASS | `Brand-Guidelines.md:59–67`: *"⛔⛔ **`TBD` — chủ: Founder (`@trisjr`)**"*, giải thích vì sao ⛔ không đề xuất tên; ⛔ **0 tên nào được nêu**. Persona: `grep -i 'persona'` toàn `docs/040-Design/` → mọi hit là **phủ định/meta** (`:85` *"File này có **0 dòng persona** — cố ý"*, `:91` *"Đây ⛔ không phải persona"*). `K-14` PASS. |
| **`V-8`** | ✅ PASS | `grep -oE '[0-9]+ ?(ms\|giây\|s\|phút\|giờ\|MB…)'` trên 6 file → **chỉ 4 hit**: *72 giờ* (SLA takedown — neo `CF-7.6`, tồn tại thật ở `SRS-Comic-Studio.md:413` + `Spec-Security-Legal-Compliance.md`) · *2 giây* (`Components.md:214`, quy cho `ADR-015` `CT-POLL-2S` **kèm lệnh ⛔ không hardcode**) · *0 s* (`Typography.md:284` — chính là dòng khai **"⛔ KHÔNG. 0 số."**). *300 DPI* ở `Typography.md` là **trích nguyên văn** `ADR-001:126` — đã đối chiếu, **khớp từng chữ**. ⛔ **0 số tự điền.** Ngưỡng `4.5:1`/`3:1`/`24×24` được dán nhãn **hằng số quy phạm WCAG**, ⛔ không mang `[EM]` — đúng ngoại lệ hợp lệ. |

**Checklist 14 mục của chính `Foundations.md` — chạy thật, `14/14 PASS`.** Đáng chú ý: `K-1` (⛔ 0 wiki-link trong `docs/040-Design/` — **0 hit**), `K-8` (`theme.extend` tại `Color-Tokens.md:210–240`: **0 hex**, toàn `var(--…)`), `K-11` (`P-3` tại `Components.md:299–320` đặc tả **thật** `DR-1`…`DR-4`, có nút nudge cho người ⛔ không kéo được), `K-13` (`Spacing-And-Layout.md:231` cấm tường minh dùng px cho hình học panel/bubble).

**Hai *"link gãy"* đã bị em loại vì là dương tính giả** — ⛔ không đưa vào CRITICAL: `000-Index.md:190` chứa `[[...]]` và `](./path.md)` nhưng **cả hai nằm trong backtick** của chính câu phát biểu quy ước RULE-001 #5 (*"⛔ KHÔNG dùng wiki-link"*). Đó là **ví dụ minh hoạ**, ⛔ không phải link.

**Ranh giới của lần verify này** (nêu ra để ⛔ không ai tưởng đã phủ 100%): đã tính lại **15/27** hàng contrast, ⛔ không phải cả 27 — 12 hàng còn lại đều là hàng tỷ lệ **cao, xa ngưỡng** (≥ 5.9:1). Anchor **trong cùng file** được kiểm bằng đối chiếu **số mục lục = số H2 − 1** (đúng ở **cả 6 file**) + spot-check thuật toán slug, ⛔ không phải kiểm từng anchor một; ⛔ **0 link có anchor trỏ sang file khác** nên ⛔ không có rủi ro anchor liên file.

---

**Người verify**: context-auditor — **KHÁC** agent đã implement (⛔ không viết dòng nào trong 9 deliverable; chỉ ghi đúng file `verdict.md` này). Cả **hai pass** đều do agent này chạy, ⛔ **không** do PM tự tuyên bố.

**Kết luận (pass 2)**: ✅ **ĐÓNG ĐƯỢC.**

Căn cứ đóng — mỗi mục kiểm lại **tại nguồn**, ⛔ không trích lại mô tả của PM:

| Mục | Bằng chứng đóng |
|---|---|
| CRITICAL #1 | `Color-Tokens.md:400` = *"**Ba màu** KHÔNG đạt 3:1"*; bảng phụ đếm được **3** hàng dữ liệu (`406–408`); `grep -c '❌'` = **0**; bảng audit vẫn `1…27` |
| CRITICAL #2 | `Design-MOC.md:48` và `000-Index.md:119` nay đều phát biểu *"cả 27 đều ĐẠT … 3 màu ⛔ không đạt ở **bảng tách biệt**"* |
| WARNING `Components.md` | `git status` còn **đúng một dòng** (` M …ADR-001…`); `DS-006` trong `5d8eba4`; **`ADR-001` ⛔ không có trong cả hai commit** |
| Nợ #4 (`000-Index.md:218`) | Câu mô tả phạm vi verify **⛔ không overclaim** — đối chiếu từng con số với việc em thật sự đã chạy |

⏳ **Còn treo, ⛔ KHÔNG chặn đóng run** (⛔ đừng xoá, chuyển sang *Nợ* để run sau nhặt): **4 WARNING** — `Color-Tokens.md:402` trỏ sai cột *(mới)* · `outline.md:109` baseline `69/10` sai · `Design-MOC.md:17` *"Ba artifact"* bỏ sót `Assets/` · `Design-MOC.md:32` link Foundations trỏ anchor thay vì file — và **3 SUGGESTION**. Cả bảy đều là **độ chính xác diễn đạt / điều hướng**, ⛔ không phải khẳng định sai về kiến trúc, pháp lý, hay số đo.

⭐ Ghi nhận tổng: phần **kỹ thuật** của run này ⛔ **không có lỗi nào ở cả hai pass** — 8/8 điểm `V-*`, 14/14 checklist tự đặt, 15/15 hàng contrast tính tay khớp delta `0.00`, ⛔ 0 link gãy, ⛔ 0 trích dẫn bịa, ⛔ 0 số tự điền. Cả hai CRITICAL đều là **câu tóm tắt đếm sai một bảng vốn đúng**, và đều đã được vá tại nguồn.
⚠️ **Bài học nên đưa vào `/memo`**: cả hai CRITICAL **và** WARNING mới đều sinh ra ở **câu tóm tắt một bảng**, ⛔ không ở bảng. Quy tắc rút ra: *mọi con số trong MOC/Index phải đếm tại nguồn ngay lúc viết, ⛔ không trích lại* — đúng thứ PM đã tự áp cho Glossary (`000-Index.md:157`) nhưng ⛔ chưa áp cho bảng contrast.
