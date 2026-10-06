# QUY ƯỚC ĐẶT TÊN COMMIT VÀ PHỐI HỢP GIT (NHÓM 6)

---

### 1. CẤU TRÚC COMMIT MESSAGE
Mỗi commit message phải tuân thủ chuẩn Conventional Commits:

```text
<loại_commit>(<phạm_vi>): <mô tả ngắn gọn bằng tiếng Anh hoặc tiếng Việt>
```

### 2. CÁC LOẠI TIỀN TỐ (PREFIXES)
* **`docs:`** Thêm, chỉnh sửa hoặc hoàn thiện tài liệu báo cáo (Phần A -> Phần H, lộ trình, quy tắc).
  * *Ví dụ:* `docs: add theoretical foundation for PBT Phan D`
* **`feat(test):`** Thêm kịch bản hoặc mã kiểm thử mới với Hypothesis.
  * *Ví dụ:* `feat(test): add PBT Property 1 idempotence string utils`
* **`fix(test):`** Sửa lỗi trong mã kiểm thử hoặc sửa cú pháp assertion.
  * *Ví dụ:* `fix(test): adjust floating point precision tolerance to 1e-4`
* **`chore:`** Cấu hình môi trường, dependencies, cập nhật `.gitignore`, Dockerfile.
  * *Ví dụ:* `chore: setup pytest harness and hypothesis multi-profile configuration`
* **`test:`** Thực thi kiểm thử tổng thể, lưu file log thực thi hoặc báo cáo coverage.
  * *Ví dụ:* `test: execute full pbt suite and collect html coverage report`

---

### 3. NGUYÊN TẮC PHỐI HỢP NHÁNH (BRANCHING STRATEGY)
1. **`main`:** Nhánh ổn định, chỉ chứa các phiên bản báo cáo và mã kiểm thử đã được Trưởng nhóm duyệt và nghiệm thu.
2. **`develop`:** Nhánh tích hợp chính của cả nhóm trong quá trình thực hiện các Sprint.
3. **`feat/<tên-thành-viên>-<tính-năng>`:** Các nhánh làm việc cá nhân khi phát triển mã kiểm thử hoặc viết báo cáo.
   * *Ví dụ:* `feat/phuoc-property-1`, `feat/nam-property-4`, `feat/hieu-property-2`, `feat/manh-property-3`.
4. Mọi merge vào `develop` và `main` phải qua Pull Request và có sự thẩm định của Trưởng nhóm.
