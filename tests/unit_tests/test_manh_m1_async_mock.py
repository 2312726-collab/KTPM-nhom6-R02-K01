"""
tests/unit_tests/test_manh_m1_async_mock.py

M1: Async/Mock Test Suite cho BruteForceParser (Mealie v3.28.0)
Thực hiện bởi: Võ Hùng Mạnh (MSSV: 2312687) — QA Automation Engineer 2 & Defect Analyst
Đồ án Kiểm thử phần mềm — Nhóm 6 (R02/K01)

Mục tiêu kiểm thử:
1. Kiểm thử trực tiếp lớp thực tế `BruteForceParser` từ mã nguồn Mealie v3.28.0.
2. Kiểm tra tính năng bất đồng bộ (async/await) của `parse_one()` và `parse()`.
3. Kiểm tra tính độc lập tuyệt đối với cơ sở dữ liệu thật thông qua unittest.mock (MagicMock).
4. Phân biệt rõ ràng mục đích sử dụng giữa MagicMock (đồng bộ) và AsyncMock (bất đồng bộ).
5. Kiểm thử các trường hợp biên, trích xuất phân số, ghi chú, đơn vị và khớp dữ liệu (DataMatcher).
6. Phát hiện và ghi nhận lỗi IndexError trên chuỗi rỗng của BruteForceParser.
"""

import os
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

# Đảm bảo Mealie AppSettings khởi tạo môi trường thử nghiệm không lỗi validation
os.environ.setdefault("PRODUCTION", "false")

from mealie.schema.recipe import RecipeIngredient
from mealie.schema.recipe.recipe_ingredient import (
    CreateIngredientFood,
    CreateIngredientUnit,
    IngredientConfidence,
    IngredientFood,
    IngredientUnit,
    ParsedIngredient,
)
from mealie.services.parser_services.ingredient_parser import BruteForceParser


# ==============================================================================
# 1. FIXTURES - CÔ LẬP TOÀN DIỆN DATABASE VÀ CÁC DEPENDENCIES
# ==============================================================================

@pytest.fixture
def mock_db_session():
    """
    MagicMock cho SQLAlchemy Session.
    Đảm bảo 100% không tạo kết nối DB thật, không phát sinh I/O mạng hoặc disk.
    """
    session = MagicMock()
    return session


@pytest.fixture
def mock_translator():
    """
    MagicMock cho Mealie Translator.
    Hàm t() trả về chính key hoặc giá trị định dạng để mô phỏng dịch đa ngôn ngữ.
    """
    translator = MagicMock()
    translator.t.side_effect = lambda key, **kwargs: f"{key}_{kwargs}" if kwargs else key
    return translator


@pytest.fixture
def mock_empty_repositories():
    """
    MagicMock cho AllRepositories với kho dữ liệu trống.
    Mô phỏng trường hợp Database chưa có food hoặc unit nào được lưu sẵn.
    """
    repos = MagicMock()
    repos.ingredient_foods.page_all.return_value.items = []
    repos.ingredient_units.page_all.return_value.items = []
    return repos


@pytest.fixture
def mock_seeded_repositories():
    """
    MagicMock cho AllRepositories có sẵn dữ liệu mẫu (Seeded Data).
    Mô phỏng trường hợp Database đã có các nguyên liệu và đơn vị phổ biến.
    """
    sugar_id = uuid4()
    flour_id = uuid4()
    cup_id = uuid4()
    tbsp_id = uuid4()

    seeded_foods = [
        IngredientFood(id=sugar_id, name="sugar", plural_name="sugars"),
        IngredientFood(id=flour_id, name="all-purpose flour", plural_name="all-purpose flours"),
    ]

    seeded_units = [
        IngredientUnit(id=cup_id, name="cup", plural_name="cups", abbreviation="c", plural_abbreviation="c"),
        IngredientUnit(id=tbsp_id, name="tablespoon", plural_name="tablespoons", abbreviation="tbsp", plural_abbreviation="tbsp"),
    ]

    repos = MagicMock()
    repos.ingredient_foods.page_all.return_value.items = seeded_foods
    repos.ingredient_units.page_all.return_value.items = seeded_units

    return {
        "repos": repos,
        "sugar_id": sugar_id,
        "flour_id": flour_id,
        "cup_id": cup_id,
        "tbsp_id": tbsp_id,
    }


@pytest.fixture
def parser_isolated_empty(mock_db_session, mock_translator, mock_empty_repositories):
    """
    Khởi tạo BruteForceParser thực tế với Repositories rỗng.
    """
    group_id = uuid4()
    with patch(
        "mealie.services.parser_services._base.get_repositories",
        return_value=mock_empty_repositories,
    ):
        parser = BruteForceParser(
            group_id=group_id,
            session=mock_db_session,
            translator=mock_translator,
        )
        yield parser, mock_db_session, mock_empty_repositories


@pytest.fixture
def parser_isolated_seeded(mock_db_session, mock_translator, mock_seeded_repositories):
    """
    Khởi tạo BruteForceParser thực tế với Repositories có sẵn dữ liệu seed.
    """
    group_id = uuid4()
    seeded_info = mock_seeded_repositories
    with patch(
        "mealie.services.parser_services._base.get_repositories",
        return_value=seeded_info["repos"],
    ):
        parser = BruteForceParser(
            group_id=group_id,
            session=mock_db_session,
            translator=mock_translator,
        )
        yield parser, mock_db_session, seeded_info


# ==============================================================================
# 2. KIỂM THỬ BẤT ĐỒNG BỘ (ASYNC/AWAIT) VỚI PARSER THẬT CỦA MEALIE
# ==============================================================================

@pytest.mark.asyncio
@pytest.mark.unit
async def test_brute_force_parser_async_parse_one_basic(parser_isolated_empty):
    """
    TC-M1.1: Kiểm tra parse_one() bằng cú pháp await với chuỗi nguyên liệu cơ bản.
    Xác nhận:
    - Hàm parse_one() là async def và trả về coroutine cần được await.
    - Cấu trúc trả về là ParsedIngredient hợp lệ.
    - Không có bất kỳ truy vấn DB thật nào phát sinh.
    """
    parser, session, repos = parser_isolated_empty
    raw_input = "2 cups sugar"

    # Gọi hàm bất đồng bộ
    result: ParsedIngredient = await parser.parse_one(raw_input)

    # 1. Xác thực cấu trúc dữ liệu trả về
    assert isinstance(result, ParsedIngredient)
    assert result.input == raw_input
    assert result.ingredient is not None
    assert result.ingredient.original_text == raw_input

    # 2. Xác thực nội dung trích xuất
    assert result.ingredient.quantity == 2.0
    assert result.ingredient.unit.name == "cups"
    assert result.ingredient.food.name == "sugar"

    # 3. Vì DB rỗng, unit & food ở dạng CreateIngredientUnit/Food (chưa match DB id)
    assert isinstance(result.ingredient.unit, CreateIngredientUnit)
    assert isinstance(result.ingredient.food, CreateIngredientFood)

    # 4. Độ tin cậy (Confidence): qty=1, note=1, unit=0, food=0 -> avg = 0.5
    assert isinstance(result.confidence, IngredientConfidence)
    assert result.confidence.quantity == 1.0
    assert result.confidence.unit == 0.0
    assert result.confidence.food == 0.0
    assert result.confidence.comment == 1.0
    assert result.confidence.average == 0.5

    # 5. Xác nhận không có truy vấn DB thật nào được gọi qua session
    session.execute.assert_not_called()
    session.commit.assert_not_called()
    session.rollback.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_brute_force_parser_async_parse_one_with_matched_db(parser_isolated_seeded):
    """
    TC-M1.2: Kiểm tra parse_one() khi DataMatcher khớp thành công Food và Unit từ Mock Repositories.
    Xác nhận:
    - Khi food và unit có trong DB mock, parser gán đúng ID thực thể.
    - Confidence đạt mức tối đa 1.0 (average = 1.0).
    """
    parser, session, seeded_info = parser_isolated_seeded
    raw_input = "1 cup sugar"

    result: ParsedIngredient = await parser.parse_one(raw_input)

    # Xác thực food & unit được chuyển thành IngredientFood & IngredientUnit (có ID)
    assert isinstance(result.ingredient.food, IngredientFood)
    assert result.ingredient.food.id == seeded_info["sugar_id"]
    assert result.ingredient.food.name == "sugar"

    assert isinstance(result.ingredient.unit, IngredientUnit)
    assert result.ingredient.unit.id == seeded_info["cup_id"]
    assert result.ingredient.unit.name == "cup"

    # Xác thực confidence đạt 1.0 tuyệt đối khi khớp toàn bộ
    assert result.confidence.food == 1.0
    assert result.confidence.unit == 1.0
    assert result.confidence.average == 1.0


@pytest.mark.asyncio
@pytest.mark.unit
async def test_brute_force_parser_async_fractions_and_notes(parser_isolated_empty):
    """
    TC-M1.3: Kiểm tra khả năng xử lý số lượng dạng phân số hỗn hợp và ghi chú trong ngoặc đơn.
    Ví dụ: '1 1/2 tbsp olive oil (extra virgin)' -> quantity: 1.5, note: 'extra virgin'.
    """
    parser, _, _ = parser_isolated_empty
    raw_input = "1 1/2 tbsp olive oil (extra virgin)"

    result: ParsedIngredient = await parser.parse_one(raw_input)

    assert result.ingredient.quantity == 1.5
    assert result.ingredient.unit.name == "tbsp"
    assert result.ingredient.food.name == "olive oil"
    assert "extra virgin" in result.ingredient.note


@pytest.mark.asyncio
@pytest.mark.unit
async def test_brute_force_parser_async_batch_parse(parser_isolated_empty):
    """
    TC-M1.4: Kiểm tra hàm async parse() xử lý danh sách nhiều nguyên liệu (Batch Parsing).
    Xác nhận:
    - Kết quả trả về đúng số lượng và thứ tự.
    - Cả 3 phần tử đều được await tuần tự và xử lý chính xác.
    """
    parser, _, _ = parser_isolated_empty
    ingredients = [
        "2 cups sugar",
        "1 tbsp salt",
        "3 large eggs",
    ]

    results: list[ParsedIngredient] = await parser.parse(ingredients)

    assert isinstance(results, list)
    assert len(results) == 3
    assert results[0].ingredient.food.name == "sugar"
    assert results[0].ingredient.quantity == 2.0
    assert results[1].ingredient.food.name == "salt"
    assert results[1].ingredient.quantity == 1.0
    assert results[2].ingredient.food.name == "eggs"
    assert results[2].ingredient.quantity == 3.0


@pytest.mark.asyncio
@pytest.mark.unit
async def test_brute_force_parser_edge_cases(parser_isolated_empty):
    """
    TC-M1.5: Kiểm thử các trường hợp biên đặc thù:
    1. Chuỗi chỉ có tên thực phẩm (single token, không có số lượng hay đơn vị).
    2. Chuỗi rỗng: Phân tích lỗi (Defect Analysis) — phát hiện IndexError do Mealie
       chưa kiểm tra điều kiện len(tokens) == 0 trước khi truy cập tokens[0].
    """
    parser, _, _ = parser_isolated_empty

    # Case 1: Chỉ có tên nguyên liệu (single token) -> thành công
    single_res = await parser.parse_one("salt")
    assert single_res.ingredient.food.name == "salt"
    assert single_res.ingredient.quantity == 0.0

    # Case 2: Chuỗi rỗng / chỉ chứa khoảng trắng -> Mealie gặp lỗi IndexError nội tại tại brute/process.py:152
    # LƯU Ý KỸ THUẬT QA: Test này là "Characterization Test" nhằm ghim và ghi nhận lỗi thực tế
    # (Defect Pinning) phục vụ phân tích RCA, KHÔNG mang ý nghĩa chứng minh parser đạt tính Crash-Free.
    with pytest.raises(IndexError):
        await parser.parse_one("")

    with pytest.raises(IndexError):
        await parser.parse_one("   ")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_data_matcher_lazy_loading_cache(parser_isolated_empty):
    """
    TC-M1.6: Kiểm chứng cơ chế Lazy Loading & In-Memory Caching của DataMatcher:
    - foods_by_id và units_by_id chỉ gọi page_all() đúng 1 lần đầu tiên.
    - Các lần gọi parse_one() tiếp theo sử dụng cache bộ nhớ, không truy xuất repository lại.
    """
    parser, _, repos = parser_isolated_empty

    # Lần 1: Khởi tạo cache
    await parser.parse_one("1 cup milk")
    # Lần 2: Sử dụng lại cache
    await parser.parse_one("2 cups flour")
    # Lần 3: Sử dụng lại cache
    await parser.parse_one("3 eggs")

    # Xác nhận page_all chỉ được gọi đúng 1 lần cho mỗi repository
    assert repos.ingredient_foods.page_all.call_count == 1
    assert repos.ingredient_units.page_all.call_count == 1


# ==============================================================================
# 3. PHÂN BIỆT RÕ RÀNG VÀ CHỨNG MINH KỸ THUẬT: MagicMock VS AsyncMock
# ==============================================================================

@pytest.mark.asyncio
@pytest.mark.unit
async def test_demonstrate_magic_mock_vs_async_mock():
    """
    TC-M1.7: Thử nghiệm độc lập chứng minh sự khác biệt bản chất giữa MagicMock và AsyncMock.
    - MagicMock dùng cho hàm/đối tượng đồng bộ (Synchronous). Khi cố ý 'await' kết quả của
      MagicMock thông thường sẽ ném TypeError.
    - AsyncMock dùng cho hàm bất đồng bộ (Coroutine/Async). Trả về coroutine và hỗ trợ assert_awaited().
    """
    # 1. Thử nghiệm với MagicMock (Đồng bộ)
    sync_mock = MagicMock(return_value="sync_result")
    direct_value = sync_mock("arg1")
    assert direct_value == "sync_result"
    sync_mock.assert_called_once_with("arg1")

    # Khi cố ý await một giá trị đồng bộ trả về từ MagicMock, Python ném TypeError
    with pytest.raises(TypeError):
        await sync_mock()

    # 2. Thử nghiệm với AsyncMock (Bất đồng bộ)
    async_mock = AsyncMock(return_value="async_result")

    # Gọi hàm async_mock trả về một coroutine
    coro = async_mock("arg_async")
    assert hasattr(coro, "__await__")

    # Await coroutine để nhận kết quả thực
    awaited_value = await coro
    assert awaited_value == "async_result"

    # AsyncMock cung cấp các assertion chuyên biệt cho coroutine
    async_mock.assert_awaited_once_with("arg_async")
    assert async_mock.await_count == 1


@pytest.mark.asyncio
@pytest.mark.unit
async def test_async_mock_simulating_external_parser_service():
    """
    TC-M1.8: Minh họa trường hợp sử dụng thực tế của AsyncMock:
    Khi kiểm thử một service tiêu thụ Parser (ví dụ RecipeImportService),
    hàm parse_one() của parser phải được mock bằng AsyncMock để caller có thể 'await'.
    """
    # Chuẩn bị một ParsedIngredient hợp lệ tuân thủ Pydantic Schema
    mock_parsed_result = ParsedIngredient(
        input="1 tsp salt",
        ingredient=RecipeIngredient(
            food=CreateIngredientFood(name="salt"),
            quantity=1.0,
        ),
    )

    # Giả lập service bên ngoài phụ thuộc vào parser
    mock_parser_service = MagicMock()
    # parse_one là async function nên bắt buộc phải mock bằng AsyncMock
    mock_parser_service.parse_one = AsyncMock(return_value=mock_parsed_result)

    # Giả lập hàm xử lý nghiệp vụ của tầng trên (Consumer)
    async def import_single_ingredient_recipe(parser, text: str):
        parsed = await parser.parse_one(text)
        return f"Imported: {parsed.ingredient.food.name} ({parsed.ingredient.quantity})"

    # Thực thi
    result_text = await import_single_ingredient_recipe(mock_parser_service, "1 tsp salt")

    # Xác thực
    assert result_text == "Imported: salt (1.0)"
    mock_parser_service.parse_one.assert_awaited_once_with("1 tsp salt")