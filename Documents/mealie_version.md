# CỐ ĐỊNH PHIÊN BẢN HỆ THỐNG MỤC TIÊU (PIN VERSION)
## ĐỒ ÁN KIỂM THỬ PHẦN MỀM — NHÓM 6

---

### 📌 THÔNG TIN HỆ THỐNG
* **Tên hệ thống:** Mealie (Recipe Manager and Meal Planner)
* **Kho lưu trữ chính thức:** [https://github.com/mealie-recipes/mealie](https://github.com/mealie-recipes/mealie)
* **Release Tag cố định:** **`v3.28.0`**
* **Commit SHA cố định:** **`0552eaa4a80031b8572849cca0ed95d07f1be001`**
* **Ngày chốt phiên bản:** 06/10/2026
* **Đường dẫn kiểm tra phiên bản trên GitHub:** [https://github.com/mealie-recipes/mealie/tree/v3.28.0](https://github.com/mealie-recipes/mealie/tree/v3.28.0)

---

### 🛡️ LÝ DO CỐ ĐỊNH PHIÊN BẢN
1. **Tránh vỡ môi trường kiểm thử (Breaking Changes):** Dự án Mealie đang phát triển tích cực với các nhánh `mealie-next`. Việc cố định đúng tag `v3.28.0` đảm bảo mã nguồn và các dependency không bị thay đổi bất ngờ giữa kỳ làm sai lệch kết quả kiểm thử.
2. **Đảm bảo tính tái lập (Reproducibility):** Bất kỳ ai (đặc biệt là Giảng viên chấm bài) khi clone đúng commit SHA trên đều có thể tái hiện chính xác 100% môi trường và các ca kiểm thử PBT của nhóm.
3. **Phạm vi kiểm thử trọng tâm:** Tập trung vào các file trong module xử lý chuỗi và đơn vị:
   - `mealie/services/parser_services/ingredient_parser.py`
   - `mealie/services/parser_services/parser_utils/string_utils.py`
   - `mealie/services/parser_services/parser_utils/unit_utils.py`
