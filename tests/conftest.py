"""
Cấu hình dùng chung cho Pytest & Hypothesis — Đồ án Kiểm thử phần mềm (Nhóm 6).
Đề tài: Mealie (v3.28.0) + Property-Based Testing (Hypothesis).
"""

import sys
from pathlib import Path
import pytest
from hypothesis import settings, Verbosity

# Đảm bảo đường dẫn thư mục gốc và mealie_src luôn được Python nhận diện
PROJECT_ROOT = Path(__file__).parent.parent
MEALIE_SRC = PROJECT_ROOT / "mealie_src"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if MEALIE_SRC.exists() and str(MEALIE_SRC) not in sys.path:
    sys.path.insert(0, str(MEALIE_SRC))


# ==============================================================================
# CẤU HÌNH CÁC PROFILE HYPOTHESIS DÙNG CHUNG CHO CẢ 5 THÀNH VIÊN
# ==============================================================================

# Profile 'dev': Chạy nhanh khi phát triển cục bộ trên máy (100 ví dụ)
settings.register_profile(
    "dev",
    max_examples=100,
    deadline=None,
    verbosity=Verbosity.normal,
)

# Profile 'ci': Chạy kiểm tra kỹ hơn trước khi nộp bài / nghiệm thu (300 ví dụ)
settings.register_profile(
    "ci",
    max_examples=300,
    deadline=None,
    verbosity=Verbosity.normal,
)

# Profile 'thorough': Kiểm thử vét cạn / đo độ bền tìm edge cases (1000 ví dụ)
settings.register_profile(
    "thorough",
    max_examples=1000,
    deadline=None,
    verbosity=Verbosity.verbose,
)

# Mặc định kích hoạt profile 'dev' khi gõ lệnh 'pytest'
settings.load_profile("dev")
