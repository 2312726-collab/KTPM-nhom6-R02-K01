"""
Cấu hình dùng chung cho Pytest & Hypothesis — Đồ án Kiểm thử phần mềm (Nhóm 6).
Đề tài: Mealie (v3.28.0) + Property-Based Testing (Hypothesis).
Phụ trách: Trần Ngọc Bảo Phước (MSSV: 2312719) — QA Automation Engineer 1
"""

import importlib
import importlib.util
import logging
import os
import sys
import tempfile
import types
from pathlib import Path
import pytest
from hypothesis import settings, Verbosity
from unittest.mock import MagicMock

# Đảm bảo đường dẫn thư mục gốc và mealie_src luôn được Python nhận diện
PROJECT_ROOT = Path(__file__).parent.parent
MEALIE_SRC = PROJECT_ROOT / "mealie_src"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if MEALIE_SRC.exists() and str(MEALIE_SRC) not in sys.path:
    sys.path.insert(0, str(MEALIE_SRC))

# Cô lập cấu hình môi trường test cho Mealie (dùng logconf.test.json và DATA_DIR có quyền ghi)
os.environ.setdefault("TESTING", "true")
os.environ.setdefault("PRODUCTION", "false")
os.environ.setdefault("DATA_DIR", str(Path(tempfile.gettempdir()) / "mealie_test_data"))

STRING_UTILS_MODULE = "mealie.services.parser_services.parser_utils.string_utils"
_PARSER_REQUIRED_DEPS = ("pydantic_settings", "sqlalchemy", "fastapi", "rapidfuzz", "slugify", "humps", "isodate")

# Nếu môi trường host tối giản thiếu dependencies nặng của parser_services.__init__.py
# (khi chạy riêng P1/P5), cô lập nhẹ namespace parser_services để cả P1 và P5 đều nạp
# đúng canonical module name `mealie.services.parser_services.parser_utils.string_utils`.
if (
    "mealie.services.parser_services" not in sys.modules
    and MEALIE_SRC.exists()
    and any(importlib.util.find_spec(dep) is None for dep in _PARSER_REQUIRED_DEPS)
):
    _parser_pkg_path = MEALIE_SRC / "mealie" / "services" / "parser_services"
    if _parser_pkg_path.exists():
        _pkg = types.ModuleType("mealie.services.parser_services")
        _pkg.__path__ = [str(_parser_pkg_path)]
        sys.modules["mealie.services.parser_services"] = _pkg


def isolate_mealie_recipe_parser():
    """Load the real parser and ingredient schema without booting the application."""
    from pydantic import BaseModel, UUID4

    class IsolatedRecipe(BaseModel):
        id: UUID4
        name: str = "Sub-recipe"
        recipe_ingredient: list = []

    for name, attributes in {
        "mealie.schema.recipe": {"__path__": [str(MEALIE_SRC / "mealie/schema/recipe")]},
        "mealie.schema.recipe.recipe": {"Recipe": IsolatedRecipe, "RecipeSummary": IsolatedRecipe},
        "mealie.services.parser_services": {
            "__path__": [str(MEALIE_SRC / "mealie/services/parser_services")],
        },
        "mealie.core.root_logger": {"get_logger": logging.getLogger},
        "mealie.core.config": {"get_app_settings": MagicMock(), "get_app_dirs": MagicMock()},
        "mealie.repos.all_repositories": {"get_repositories": MagicMock()},
        "mealie.repos.repository_factory": {"AllRepositories": object},
    }.items():
        if name not in sys.modules:
            module = types.ModuleType(name)
            module.__dict__.update(attributes)
            sys.modules[name] = module

    # The scaling suite can load its lightweight DataMatcher stub first.
    parser_base = "mealie.services.parser_services._base"
    if parser_base in sys.modules and not hasattr(sys.modules[parser_base], "ABCIngredientParser"):
        del sys.modules[parser_base]
    db_recipe = sys.modules.get("mealie.db.models.recipe")
    if db_recipe is not None and not hasattr(db_recipe, "__path__"):
        db_recipe.__path__ = [str(MEALIE_SRC / "mealie/db/models/recipe")]

    recipe = sys.modules["mealie.schema.recipe"]
    if not hasattr(recipe, "RecipeIngredient"):
        schema = importlib.import_module("mealie.schema.recipe.recipe_ingredient")
        recipe.RecipeIngredient = schema.RecipeIngredient


def load_mealie_string_utils():
    """
    Helper dùng chung (P1 & P5) nạp module `string_utils.py` thật của Mealie v3.28.0
    theo đúng tên canonical `mealie.services.parser_services.parser_utils.string_utils`.
    Tránh dùng tên module giả để pytest-cov đo và cộng gộp coverage chính xác, không sinh CoverageWarning.
    """
    if STRING_UTILS_MODULE in sys.modules:
        return sys.modules[STRING_UTILS_MODULE]

    try:
        return importlib.import_module(STRING_UTILS_MODULE)
    except Exception:
        parser_pkg_name = "mealie.services.parser_services"
        parser_pkg_path = MEALIE_SRC / "mealie" / "services" / "parser_services"
        if parser_pkg_name not in sys.modules and parser_pkg_path.exists():
            pkg = types.ModuleType(parser_pkg_name)
            pkg.__path__ = [str(parser_pkg_path)]
            sys.modules[parser_pkg_name] = pkg
            return importlib.import_module(STRING_UTILS_MODULE)

        target_file = parser_pkg_path / "parser_utils" / "string_utils.py"
        if target_file.exists():
            spec = importlib.util.spec_from_file_location(STRING_UTILS_MODULE, str(target_file))
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                sys.modules[STRING_UTILS_MODULE] = mod
                spec.loader.exec_module(mod)
                return mod

        raise ImportError(f"Không tìm thấy {STRING_UTILS_MODULE} trong {MEALIE_SRC}")


# ==============================================================================
# CẤU HÌNH CÁC PROFILE HYPOTHESIS DÙNG CHUNG CHO CẢ 5 THÀNH VIÊN
# ==============================================================================

def _register_profile_safe(name: str, **kwargs) -> None:
    """Đăng ký profile Hypothesis an toàn ngay cả khi module conftest được import lại."""
    try:
        settings.get_profile(name)
    except Exception:
        settings.register_profile(name, **kwargs)


# Profile 'dev': Chạy nhanh khi phát triển cục bộ trên máy (50 ví dụ)
_register_profile_safe(
    "dev",
    max_examples=50,
    deadline=None,
    verbosity=Verbosity.normal,
)

# Profile 'ci': Chạy kiểm tra kỹ hơn trước khi nộp bài / nghiệm thu (300 ví dụ)
_register_profile_safe(
    "ci",
    max_examples=300,
    deadline=None,
    verbosity=Verbosity.normal,
)

# Profile 'thorough': Kiểm thử vét cạn / đo độ bền tìm edge cases (1000 ví dụ)
_register_profile_safe(
    "thorough",
    max_examples=1000,
    deadline=None,
    verbosity=Verbosity.verbose,
)

# Mặc định kích hoạt profile 'dev' khi gõ lệnh 'pytest'
settings.load_profile("dev")
