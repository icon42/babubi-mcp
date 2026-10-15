import httpx
import pytest
import respx

from babubi_mcp.tools.pumping import (
    create_pumping,
    delete_pumping,
    list_pumping,
    update_pumping,
)

BASE = "http://test-babubi"

PUMPING = {"id": 1, "child": 1, "start": "2024-01-15T08:00:00Z", "end": "2024-01-15T08:20:00Z", "amount": 3.5}


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url=BASE, assert_all_called=False) as router:
        yield router


async def test_list_pumping(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/pumping/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "next": None, "previous": None, "results": [PUMPING]}
        )
    )
    result = await list_pumping()
    assert result[0]["amount"] == 3.5


async def test_create_pumping(mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/pumping/").mock(return_value=httpx.Response(201, json=PUMPING))
    result = await create_pumping(
        child_id=1, start="2024-01-15T08:00:00", end="2024-01-15T08:20:00", amount=3.5
    )
    assert result["id"] == 1


async def test_update_pumping(mock_api: respx.MockRouter) -> None:
    mock_api.patch("/api/pumping/1/").mock(
        return_value=httpx.Response(200, json={**PUMPING, "amount": 4.0})
    )
    result = await update_pumping(1, amount=4.0)
    assert result["amount"] == 4.0


async def test_delete_pumping(mock_api: respx.MockRouter) -> None:
    mock_api.delete("/api/pumping/1/").mock(return_value=httpx.Response(204))
    result = await delete_pumping(1)
    assert "1" in result
