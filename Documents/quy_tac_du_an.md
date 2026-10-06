# BỘ QUY TẮC CHUẨN DỰ ÁN KIỂM THỬ PHẦN MỀM (NHÓM 6)
> *Được tinh chỉnh dựa trên triết lý **Ponytail** (Tư duy của Kỹ sư Cấp cao Tối ưu / Lazy Senior Developer)*  
> **Phương châm cốt lõi:** *"Dòng code tốt nhất là dòng code không bao giờ phải viết. Hiệu quả tối đa, không cẩu thả."*

---

## 🎯 PHẦN I: TRIẾT LÝ VÀ "CHIẾC THANG 7 BẬC" TRƯỚC KHI VIẾT CODE

Trước khi viết bất kỳ dòng mã nguồn hay kịch bản kiểm thử nào, tất cả thành viên trong nhóm phải dừng lại ở **bậc thang đầu tiên có thể giải quyết được vấn đề**:

1. **Có thực sự cần làm cái này không? (YAGNI - You Aren't Gonna Need It):**
   - Đừng ôm đồm toàn bộ hệ thống Mealie. Hãy giới hạn phạm vi chặt chẽ vào đúng module mục tiêu (ví dụ: `parser_services`).
2. **Codebase của Mealie đã có sẵn hàm/helper này chưa?**
   - Tái sử dụng các tiện ích có sẵn trong `mealie/services/parser_services/parser_utils/`, không tự viết lại logic parse chuỗi hay regex từ đầu.
3. **Thư viện chuẩn của Python (Standard Library) có hỗ trợ không?**
   - Dùng `fractions.Fraction`, `re`, `unicodedata`, `dataclasses` có sẵn của Python thay vì cài thêm thư viện ngoài.
4. **Tính năng sẵn có của nền tảng/Docker/Pytest có giải quyết được không?**
   - Tận dụng `docker-compose` có sẵn của Mealie và runner `pytest` thay vì dựng script chạy phức tạp.
5. **Thư viện phụ thuộc đã cài (`Hypothesis`, `Pydantic`) có giải quyết được không?**
   - Tận dụng tối đa các strategy có sẵn của Hypothesis (`st.text()`, `st.integers()`, `st.floats()`, `st.sampled_from()`).
6. **Có thể viết tối giản và súc tích trong 1 vài dòng không?**
   - Ưu tiên sự tinh gọn, dễ đọc, dễ hiểu.
7. **Chỉ khi các bậc trên không thỏa mãn: Mới bắt đầu viết code mới.**

---

## ⚖️ PHẦN II: CÁC NGUYÊN TẮC BẮT BUỘC TRONG DỰ ÁN

### 1. Không phát sinh những thứ thừa thãi
- **Không tạo cấu trúc trừu tượng (No Abstractions):** Không tạo class cha, helper trung gian nếu không thực sự cần thiết hoặc không ai yêu cầu.
- **Không cài thêm thư viện ngoài (Dependencies) vô tội vạ:** Càng ít phụ thuộc, môi trường chạy test càng ổn định và giảng viên càng dễ chấm bài.
- **Xóa bỏ ưu tiên hơn Thêm vào (Deletion over Addition):** Ít file nhất có thể, diff code ngắn nhất có thể. Code đơn giản, tường minh luôn đánh bại code "thông minh" mà phức tạp.

### 2. Sửa lỗi tận gốc, không sửa ở ngọn (Root Cause over Symptom)
- Khi kiểm thử phát hiện lỗi (ví dụ: Hypothesis tìm thấy 1 chuỗi ký tự làm crash parser của Mealie):
  - Lỗi hiển thị chỉ là **hiện tượng** (symptom).
  - Phải truy vết (trace) vào tận hàm xử lý gốc trong Mealie để tìm ra **nguyên nhân cốt lõi (Root Cause)**: lỗi do chia cho 0, do regex backtracking, hay do thiếu ép kiểu dữ liệu?
  - Sửa một lần ở hàm gốc sẽ giải quyết triệt để vấn đề cho tất cả các nơi gọi.

### 3. Những điều TUYỆT ĐỐI KHÔNG ĐƯỢC "LƯỜI BIẾNG"
*Triết lý tối ưu nghĩa là loại bỏ việc vô nghĩa, KHÔNG PHẢI cẩu thả. Nhóm bắt buộc phải kỹ lưỡng ở 5 điểm sau:*
1. **Hiểu thấu đáo bài toán:** Đọc kỹ mã nguồn Mealie và hiểu rõ luồng nghiệp vụ trước khi viết test. Một đoạn test ngắn mà không hiểu nghiệp vụ là sự cẩu thả, không phải tối ưu.
2. **Xác thực dữ liệu tại ranh giới (Trust Boundaries):** Mọi input từ người dùng, API, file công thức import đều phải được kiểm tra tính hợp lệ.
3. **Không để mất dữ liệu và tránh Crash (Robustness):** Hàm xử lý không bao giờ được phép quăng ra unhandled exception (500 Error) khi gặp input bất thường.
4. **Kiểm thử tự động là bắt buộc (No test = Unfinished):**
   - Bất kỳ tính chất (Property) nào được định nghĩa đều phải có **1 script test chạy được độc lập (executable check)** bằng `pytest`.
   - Test phải chạy tự động 100%, không phụ thuộc vào thao tác tay của con người.
5. **Đảm bảo tính tái lập (Reproducibility):** Mọi cấu hình, dữ liệu mẫu (seed data) và lệnh chạy phải được viết vào `README.md` sao cho bất kỳ ai (đặc biệt là giảng viên) chỉ cần chạy 1 lệnh là ra kết quả y hệt.

---

## 🛠️ PHẦN III: QUY TẮC CỤ THỂ CHO TỔ HỢP R02 (MEALIE) & K01 (HYPOTHESIS)

### 1. Quy tắc giới hạn phạm vi (Scope Boundary)
- **Khu vực mục tiêu:** Tập trung kiểm thử vào bộ phân tích nguyên liệu và đơn vị:
  - `mealie/services/parser_services/ingredient_parser.py`
  - `mealie/services/parser_services/parser_utils/string_utils.py`
  - `mealie/services/parser_services/parser_utils/unit_utils.py`
- Không lãng phí thời gian vào việc test giao diện Vue phức tạp hoặc các API không liên quan trực tiếp đến nghiệp vụ xử lý dữ liệu.

### 2. Quy tắc viết Test với Hypothesis
- Mỗi property phải kiểm tra một **tính chất bất biến toán học/logic rõ ràng**:
  - *Tính lũy đẳng (Idempotence):* `f(f(x)) == f(x)`
  - *Tính bảo toàn hai chiều (Round-trip):* `decode(encode(x)) == x`
  - *Tính bền vững (Crash-free):* Không bao giờ phát sinh crash với mọi chuỗi `st.text()`.
- Tận dụng tính năng **Shrinking** của Hypothesis để thu nhỏ ca lỗi thành phản ví dụ ngắn gọn nhất trước khi đưa vào báo cáo.

---

## 👥 PHẦN IV: QUY TẮC PHỐI HỢP NHÓM & QUẢN LÝ GIT

1. **Commit nhỏ, rõ ràng, minh bạch:**
   - Mỗi commit giải quyết đúng 1 vấn đề cụ thể (Atomic commit).
   - Format tin nhắn commit bằng tiếng Việt chuẩn: `thêm:`, `sửa:`, `cấu hình:`, `dọn dẹp:`.
2. **Mọi thành viên đều có dấu ấn trên Git:**
   - Điểm số phụ thuộc vào lịch sử đóng góp thực tế trên Git. Cả 5 thành viên đều phải tự commit phần việc của mình từ máy cá nhân.
3. **Ghi chép và lưu vết:**
   - Mọi giả định kỹ thuật hoặc giải pháp tạm thời phải được ghi chú rõ ràng với tiền tố `# note(ponytail): <lý do và hướng nâng cấp sau>`.

---

## 🤖 PHẦN V: NGUYÊN TẮC LÀM VIỆC DỰ ÁN DÀNH CHO AI ASSISTANT

Tất cả các hành vi của AI Assistant trong dự án này PHẢI TUÂN THỦ NGHIÊM NGẶT 4 NGUYÊN TẮC SAU:

### 1. Quy tắc tạo nhánh (Branching):
- TUYỆT ĐỐI KHÔNG làm việc trực tiếp trên nhánh `main` hay `develop`.
- Trước khi thực hiện bất kỳ công việc/tính năng nào, LUÔN LUÔN kiểm tra xem nhánh đang làm có đúng không.
- **Mô hình phân nhánh (QUAN TRỌNG):**
  Các nhánh công việc là NHÁNH ĐỘC LẬP, KHÔNG PHẢI nhánh con của `develop`.
  Chúng được tạo từ `develop` nhưng tồn tại độc lập và merge ngược lại vào `develop` qua Pull Request.
```text
  main          <- chỉ nhận merge từ develop khi đã ổn định
    ^
  develop       <- chỉ nhận merge từ các nhánh công việc qua Pull Request
    ^
Vai trò từng nhánh:
  - Nhánh công việc: Viết code, hoàn toàn độc lập nhau. Merge về develop qua PR khi xong.
  - develop: Gộp code từ các nhánh công việc. Kiểm tra ổn định tổng thể.
  - main: Chỉ nhận khi develop đã ổn định hoàn toàn.
```
- Commit message PHẢI viết bằng TIẾNG VIỆT theo cấu trúc:
  `thêm:` / `sửa:` / `cấu hình:` / `dọn dẹp:`

### 2. Kiểm soát nhánh `main` và đẩy code:
- Mọi hành động merge, push lên nhánh `main` BẮT BUỘC phải thông qua sự kiểm tra và đồng ý rõ ràng của USER.
- Không tự ý thực hiện `git push origin main`.
- Mọi hành động merge vào `develop` cũng phải qua Pull Request và được USER duyệt.

### 3. Phân tích kỹ & Chia nhỏ công việc (Incremental workflow):
- Luôn luôn phân tích vấn đề thật kỹ càng trước khi bắt đầu.
- Chia nhỏ các đầu việc thành từng phần cụ thể, rõ ràng.
- Thực hiện xong chức năng nào thì DỪNG LẠI, đợi USER kiểm tra và commit lên Git rồi mới tiếp tục làm chức năng tiếp theo.
- Chỉ push lên GitHub sau khi toàn bộ các bước trong 1 nhóm công việc đã hoàn thành (Lựa chọn A).

### 4. Quyền thực thi & Phạm vi công việc:
- CHỈ KHI USER yêu cầu và cho phép bắt đầu code thì AI mới được phép viết mã trong đúng phạm vi được giao.
- KHÔNG TỰ Ý suy diễn hoặc tự tiện thêm các tính năng nằm ngoài phạm vi được giao.
- Mọi ý tưởng hoặc đề xuất bổ sung phải được thảo luận và nhận được sự đồng ý của USER trước khi làm.

