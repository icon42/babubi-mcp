import httpx
import pytest
import respx

from babubi_mcp.tools.feedings import (
    create_feeding,
    delete_feeding,
    list_feedings,
    update_feeding,
)

BASE = "http://test-babubi"

FEEDING = {
    "id": 1,
    "child": 1,
    "start": "2024-01-15T10:00:00Z",
    "end": "2024-01-15T10:30:00Z",
    "type": "breast milk",
    "method": "left breast",
}


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url=BASE, assert_all_called=False) as router:
        yield router


async def test_list_feedings_no_filters(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/feedings/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "next": None, "previous": None, "results": [FEEDING]}
        )
    )
    result = await list_feedings()
    assert len(result) == 1
    assert result[0]["type"] == "breast milk"


async def test_list_feedings_with_child_filter(mock_api: respx.MockRouter) -> None:
    route = mock_api.get("/api/feedings/").mock(
        return_value=httpx.Response(
            200, json={"count": 0, "next": None, "previous": None, "results": []}
        )
    )
    await list_feedings(child_id=2)
    params = dict(route.calls[0].request.url.params)
    assert params["child"] == "2"


async def test_create_feeding_required_fields(mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/feedings/").mock(return_value=httpx.Response(201, json=FEEDING))
    result = await create_feeding(
        child_id=1,
        start="2024-01-15T10:00:00",
        end="2024-01-15T10:30:00",
        feeding_type="breast milk",
        method="left breast",
    )
    assert result["id"] == 1


async def test_create_feeding_with_timer(mock_api: respx.MockRouter) -> None:
    route = mock_api.post("/api/feedings/").mock(return_value=httpx.Response(201, json=FEEDING))
    await create_feeding(
        child_id=1,
        start="2024-01-15T10:00:00",
        end="2024-01-15T10:30:00",
        feeding_type="breast milk",
        method="left breast",
        timer_id=42,
    )
    assert b'"timer": 42' in route.calls[0].request.content or b'"timer":42' in route.calls[0].request.content


async def test_update_feeding_partial(mock_api: respx.MockRouter) -> None:
    mock_api.patch("/api/feedings/1/").mock(
        return_value=httpx.Response(200, json={**FEEDING, "notes": "updated"})
    )
    result = await update_feeding(1, notes="updated")
    assert result["notes"] == "updated"


async def test_delete_feeding(mock_api: respx.MockRouter) -> None:
    mock_api.delete("/api/feedings/1/").mock(return_value=httpx.Response(204))
    result = await delete_feeding(1)
    assert "1" in result


async def test_list_feedings_type_filter(mock_api: respx.MockRouter) -> None:
    route = mock_api.get("/api/feedings/").mock(
        return_value=httpx.Response(
            200, json={"count": 0, "next": None, "previous": None, "results": []}
        )
    )
    await list_feedings(feeding_type="formula")
    params = dict(route.calls[0].request.url.params)
    assert params["type"] == "formula"
