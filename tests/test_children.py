import httpx
import pytest
import respx

from babubi_mcp.tools.children import create_child, get_child, list_children, update_child

BASE = "http://test-babubi"

CHILD = {
    "id": 1,
    "first_name": "Alice",
    "last_name": "Smith",
    "birth_date": "2024-01-01",
    "slug": "alice-smith",
}


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url=BASE, assert_all_called=False) as router:
        yield router


async def test_list_children(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/children/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "next": None, "previous": None, "results": [CHILD]}
        )
    )
    result = await list_children()
    assert len(result) == 1
    assert result[0]["first_name"] == "Alice"


async def test_list_children_with_filters(mock_api: respx.MockRouter) -> None:
    route = mock_api.get("/api/children/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "next": None, "previous": None, "results": [CHILD]}
        )
    )
    await list_children(last_name="Smith", ordering="-birth_date")
    request = route.calls[0].request
    assert request.url.params["last_name"] == "Smith"
    assert request.url.params["ordering"] == "-birth_date"


async def test_get_child_by_slug(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/children/alice-smith/").mock(
        return_value=httpx.Response(200, json=CHILD)
    )
    result = await get_child("alice-smith")
    assert result["id"] == 1


async def test_create_child_required_fields(mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/children/").mock(return_value=httpx.Response(201, json=CHILD))
    result = await create_child("Alice", "Smith", "2024-01-01")
    assert result["first_name"] == "Alice"


async def test_create_child_with_birth_time(mock_api: respx.MockRouter) -> None:
    route = mock_api.post("/api/children/").mock(
        return_value=httpx.Response(201, json=CHILD)
    )
    await create_child("Alice", "Smith", "2024-01-01", birth_time="14:30:00")
    body = route.calls[0].request.content
    assert b"birth_time" in body


async def test_update_child_by_slug(mock_api: respx.MockRouter) -> None:
    mock_api.patch("/api/children/alice-smith/").mock(
        return_value=httpx.Response(200, json={**CHILD, "first_name": "Alicia"})
    )
    result = await update_child("alice-smith", first_name="Alicia")
    assert result["first_name"] == "Alicia"


async def test_update_child_no_fields_sends_empty_patch(mock_api: respx.MockRouter) -> None:
    route = mock_api.patch("/api/children/alice-smith/").mock(
        return_value=httpx.Response(200, json=CHILD)
    )
    await update_child("alice-smith")
    assert route.called
