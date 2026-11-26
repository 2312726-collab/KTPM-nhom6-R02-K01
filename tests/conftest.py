"""
Cấu hình dùng chung cho Pytest & Hypothesis — Đồ án Kiểm thử phần mềm (Nhóm 6).
Đề tài: Mealie (v3.28.0) + Property-Based Testing (Hypothesis).
Phụ trách: Trần Ngọc Bảo Phước (MSSV: 2312719) — QA Automation Engineer 1
"""

import importlib
import importlib.util
import os
import sys
import tempfile
import types
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


def ensure_mealie_parser_isolated():
    """
    Chỉ kích hoạt cô lập nhẹ khi chạy trên Python < 3.14 (do Mealie v3.28.0 dùng PEP 649
    ở settings.py/ai_providers.py) hoặc môi trường host thiếu dependencies nặng (fastapi, sqlalchemy...).
    Trên môi trường chuẩn Python >= 3.14 cài đủ requirements-test.txt, hàm giữ nguyên module thật 100%.
    """
    needs_isolation = sys.version_info < (3, 14) or any(
        importlib.util.find_spec(dep) is None
        for dep in ("fastapi", "sqlalchemy", "pydantic_settings", "text_unidecode")
    )
    if not needs_isolation:
        return

    import string
    from typing import Any
    from unittest.mock import MagicMock
    from pydantic import BaseModel, ConfigDict, UUID4

    class _MealieRecipeStub(BaseModel):
        model_config = ConfigDict(from_attributes=True)
        id: UUID4
        name: str = "Sub-recipe"
        recipe_ingredient: list[Any] = []

    norm_punct = string.punctuation.replace("'", "").replace('"', "")
    norm_table = str.maketrans(norm_punct, " " * len(norm_punct))

    class _NormalizedModelStub:
        @classmethod
        def normalize(cls, val: str) -> str:
            try:
                from text_unidecode import unidecode
                cleaned = unidecode(val)
            except Exception:
                cleaned = val
            return cleaned.translate(norm_table).lower().strip()[:255]

    if "fastapi" not in sys.modules:
        f_mod = types.ModuleType("fastapi")
        f_mod.Header = MagicMock()
        sys.modules["fastapi"] = f_mod

    if "mealie.core.root_logger" not in sys.modules:
        l_mod = types.ModuleType("mealie.core.root_logger")
        l_mod.get_logger = MagicMock(return_value=MagicMock())
        sys.modules["mealie.core.root_logger"] = l_mod

    if "mealie.db.models.recipe" not in sys.modules:
        db_rec = types.ModuleType("mealie.db.models.recipe")
        db_rec.__path__ = []
        db_rec.IngredientFoodModel = _NormalizedModelStub
        db_rec.IngredientFoodSubstitutionModel = MagicMock()
        db_rec.RecipeModel = MagicMock()
        sys.modules["mealie.db.models.recipe"] = db_rec

    if "mealie.db.models.recipe.ingredient" not in sys.modules:
        db_ing = types.ModuleType("mealie.db.models.recipe.ingredient")
        db_ing.IngredientFoodModel = _NormalizedModelStub
        db_ing.IngredientUnitModel = _NormalizedModelStub
        sys.modules["mealie.db.models.recipe.ingredient"] = db_ing

    if "mealie.repos" not in sys.modules:
        repos_pkg = types.ModuleType("mealie.repos")
        repos_pkg.__path__ = []
        sys.modules["mealie.repos"] = repos_pkg

    if "mealie.repos.all_repositories" not in sys.modules:
        all_repos = types.ModuleType("mealie.repos.all_repositories")
        all_repos.get_repositories = MagicMock()
        all_repos.AllRepositories = MagicMock()
        sys.modules["mealie.repos.all_repositories"] = all_repos

    if "mealie.repos.repository_factory" not in sys.modules:
        repo_fac = types.ModuleType("mealie.repos.repository_factory")
        repo_fac.AllRepositories = Any
        sys.modules["mealie.repos.repository_factory"] = repo_fac

    if "mealie.schema.recipe" not in sys.modules and MEALIE_SRC.exists():
        rec_pkg = types.ModuleType("mealie.schema.recipe")
        rec_pkg.__path__ = [str(MEALIE_SRC / "mealie" / "schema" / "recipe")]
        sys.modules["mealie.schema.recipe"] = rec_pkg

    if "mealie.schema.recipe.recipe" not in sys.modules:
        rec_mod = types.ModuleType("mealie.schema.recipe.recipe")
        rec_mod.Recipe = _MealieRecipeStub
        rec_mod.RecipeSummary = _MealieRecipeStub
        sys.modules["mealie.schema.recipe.recipe"] = rec_mod

    from mealie.schema.recipe.recipe_ingredient import RecipeIngredient
    if "mealie.schema.recipe" in sys.modules and not hasattr(sys.modules["mealie.schema.recipe"], "RecipeIngredient"):
        sys.modules["mealie.schema.recipe"].RecipeIngredient = RecipeIngredient


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
