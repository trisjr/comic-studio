# Escalations: 2026-08-30-brand-guidelines-va-design-system-comic-studio

> Append-only. ⛔ Không sửa entry cũ.
> `E1`–`E5` là **Tầng 2** — PM tự quyết trong phạm vi `brief.md`, ghi ra để anh soi lại và bác nếu thấy sai. `E6`+ là **Tầng 3** — anh quyết tại gate.

## E1 — Coi thay đổi ADR-001 (chưa commit) là đã chốt?

- **Tầng**: 2 (PM tự quyết)
- **Nguồn**: `brief.md` `Q-C`; BA phát hiện thêm mâu thuẫn `X-5`
- **Vấn đề**: `ADR-001` được bổ sung `shadcn/ui + Tailwind CSS` nhưng **chưa commit** ở checkout gốc. Worktree tạo từ base ref ⇒ nhận bản cũ. Toàn bộ tầng token neo vào quyết định này.
- **Quyết định**: **Coi là đã chốt.** PM đã copy bản mới nhất vào worktree làm **input read-only**.
- **Lý do**: đây là thay đổi anh **chủ động viết**, nằm trong file anh sở hữu, và nội dung nó tự nhất quán (thêm cả dòng ở `## Consequences` giải thích tích hợp Zod). Coi là nháp bỏ đi thì run này ⛔ không có stack nào để neo, mà `SRS-NFR-09` vẫn `TBD` ⇒ bế tắc.
- **Hành động**: ⛔ **KHÔNG commit `ADR-001` cùng run này** — anh giữ quyền commit ở checkout gốc. Mọi writer được cấp `[CONTEXT]` nêu rõ bản trong worktree là bản đúng (`grep -c shadcn` = 2).
- **Sai thì hỏng ở đâu**: anh revert thay đổi đó ⇒ `Foundations.md` + `Color-Tokens.md` phải viết lại phần hợp đồng token. Hai file, ⛔ không phải cả run.

## E2 — Độc giả đích của Design System

- **Tầng**: 2
- **Nguồn**: `brief.md` `Q-E`
- **Quyết định**: Design System viết cho **AI assist sinh code là độc giả CHÍNH**, người đọc là độc giả phụ.
- **Lý do**: `ADR-001` chọn stack với lý do tường minh *"tối ưu cho AI assist (`R1`)"* và *"TypeScript + NestJS + React là vùng có mật độ dữ liệu huấn luyện cao nhất"*. Đội là **1 người + AI assist** — ⛔ không có designer thứ hai để tài liệu này thuyết phục.
- **Hệ quả cho writer**: ưu tiên **giá trị cụ thể, tên token chính xác, bảng tra được** hơn văn xuôi giải thích triết lý thiết kế. Mỗi quyết định phải máy đọc được.
- **Sai thì hỏng ở đâu**: nếu thật ra anh cần tài liệu để thuyết phục nhà đầu tư / designer thuê ngoài, các file sẽ **đúng nhưng khô** — sửa được bằng cách thêm phần mở đầu, ⛔ không phải viết lại.

## E3 — `Glossary.md` có trong scope không

- **Tầng**: 2
- **Nguồn**: `brief.md` `Q-D`
- **Quyết định**: **Có** — thành **Lô 5**, chạy **sau** khi cả 6 file Design System đã đóng.
- **Lý do**: Design System sinh ra một lớp thuật ngữ mà `Glossary.md` (69 thuật ngữ, 10 nhóm) ⛔ không có nhóm nào phủ. Bỏ qua ⇒ tầng 040 dùng một bộ từ vựng ⛔ không đăng ký ở đâu, đúng loại drift mà tiêu chí *Coherence* ở Bước 6 phải bắt.
- **Vì sao xếp cuối, ⛔ không song song**: thuật ngữ phải rút từ **file đã viết xong**, ⛔ không phải từ dự đoán. Chạy sớm là bịa.
- **Vì sao giao `business-analyst` chứ ⛔ không phải PM tự làm**: PM đắt **gấp 2,75 lần** worker mỗi turn (đo run `2026-08-28`), và tới lô này context PM đã phình.

## E4 — Nhóm 11 (takedown công khai) có mang cùng brand không

- **Tầng**: 2 (BA đề nghị Tầng 3; PM hạ xuống 2 — xem lý do)
- **Nguồn**: `findings/business-analyst.md` §6.2 `Q-BA-2`
- **Quyết định**: **Hoãn quyết định thương hiệu, nhưng ⛔ KHÔNG hoãn ràng buộc.** `Brand-Guidelines.md` ghi một mục ngắn: bề mặt takedown công khai (`C-15`) là **nghĩa vụ pháp lý, ⛔ không phải điểm chạm marketing** ⇒ ⛔ không áp brand voice lên nó, và ⛔ tuyệt đối không mang messaging trấn an về bản quyền (`SRS-NFR-15`). Việc nó dùng logo nào để `TBD`.
- **Lý do hạ xuống Tầng 2**: phần **có hệ quả** (cấm messaging bản quyền) đã bị `SRS-NFR-15` quyết sẵn, ⛔ không cần anh quyết lại. Phần còn lại (logo/màu của một form chưa ai vẽ) ⛔ không chặn file nào trong run này.

## E5 — Nhóm 12 (operator) có trong scope Design System không

- **Tầng**: 2
- **Nguồn**: `findings/business-analyst.md` §6.2 `Q-BA-3`; `architect` nợ Phase 2 #2
- **Quyết định**: **Ngoài scope run này.**
- **Lý do**: ⛔ **Không UC nào mô tả** nhóm này, và `000-Index.md` §Nợ kỹ thuật #2 ghi rõ hai endpoint admin takedown (`TD-2`/`TD-3`) **đang BỊ CHẶN** cho tới khi mô hình quyền được sửa (`app_operator` chưa có trong `SDD` §7.4 và `ADR-006`). Thiết kế UI cho một mô hình quyền chưa tồn tại là xây trên nền chưa đổ.
- **Hành động**: ghi vào *Nợ* của run; `Components.md` ⛔ không đặc tả component operator nào.

## E6 — Bốn câu Tầng 3 trình anh tại gate

- **Tầng**: 3 (anh quyết)
- **Nguồn**: tổng hợp `brief.md` `Q-A`/`Q-B` + `product-designer` §2.3 + `business-analyst` §6.2 `Q-BA-1`
- **Bốn câu**: (1) hướng brand — tone + màu chủ đạo · (2) light hay dark là default · (3) chuẩn accessibility & thiết bị đích · (4) vị trí `Brand-Guidelines.md` trong RULE-001.
- **Vì sao ⛔ không tự quyết**: (1) và (2) ⛔ không có một dòng căn cứ nào trong repo — agent chọn = agent bịa audience, và đây là *"chỗ ảo giác dễ trông có thẩm quyền nhất"*. (3) là **cam kết có chi phí thật**, sẽ thành chuẩn nghiệm thu của tầng QA. (4) là **đổi contract** một tài liệu `status: approved`.
- **Kết quả**: ✅ **Anh duyệt 4/4 theo đúng phương án PM đề xuất**, ⛔ không điều chỉnh. Chi tiết `G-1`…`G-4` ghi ở `run-plan.md` §Gate.

## E7 — Tên hiển thị thương mại vẫn TBD sau gate

- **Tầng**: 2 (PM quyết cách xử lý khoảng trống, ⛔ không quyết nội dung)
- **Bối cảnh**: Gate chốt được tone và màu, nhưng **tên hiển thị** ⛔ không nằm trong 4 câu đã hỏi (hết slot AskUserQuestion, và nó là câu **free-form**, ⛔ không phải lựa chọn).
- **Quyết định**: `Brand-Guidelines.md` ghi `TBD` **có chủ** (Founder) tại mục tên hiển thị, và ⛔ **không** suy ra logo/wordmark/typography thương hiệu từ một cái tên chưa có.
- **Lý do**: `comic-studio` là **project name** (`Charter` §1), ⛔ không phải tên sản phẩm. Tên thương mại là quyết định **kinh doanh + pháp lý** (khả năng đăng ký nhãn hiệu), ⛔ ngoài thẩm quyền của cả PM lẫn agent. Bịa tên ⇒ mọi asset phái sinh sau này phải làm lại.
- **Sai thì hỏng ở đâu**: nếu anh thật ra đã có tên trong đầu, `Brand-Guidelines.md` chỉ cần sửa **một mục** — rẻ. Ngược lại, bịa một tên rồi để nó lan vào wordmark + favicon + microcopy thì đắt gấp nhiều lần.
