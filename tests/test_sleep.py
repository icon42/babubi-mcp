import httpx
import pytest
import respx

from babubi_mcp.tools.sleep import create_sleep, delete_sleep, list_sleep, update_sleep

BASE = "http://test-babubi"

SLEEP = {
    "id": 1,
    "child": 1,
    "start": "2024-01-15T21:00:00Z",
    "end": "2024-01-16T06:00:00Z",
    "nap": False,
}


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url=BASE, assert_all_called=False) as router:
        yield router


async def test_list_sleep(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/sleep/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "next": None, "previous": None, "results": [SLEEP]}
        )
    )
    result = await list_sleep()
    assert result[0]["nap"] is False


async def test_create_sleep(mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/sleep/").mock(return_value=httpx.Response(201, json=SLEEP))
    result = await create_sleep(
        child_id=1, start="2024-01-15T21:00:00", end="2024-01-16T06:00:00"
    )
    assert result["id"] == 1


async def test_create_sleep_with_nap(mock_api: respx.MockRouter) -> None:
    route = mock_api.post("/api/sleep/").mock(
        return_value=httpx.Response(201, json={**SLEEP, "nap": True})
    )
    await create_sleep(child_id=1, start="2024-01-15T13:00:00", end="2024-01-15T14:30:00", nap=True)
    assert b'"nap": true' in route.calls[0].request.content or b'"nap":true' in route.calls[0].request.content


async def test_update_sleep(mock_api: respx.MockRouter) -> None:
    mock_api.patch("/api/sleep/1/").mock(
        return_value=httpx.Response(200, json={**SLEEP, "notes": "good night"})
    )
    result = await update_sleep(1, notes="good night")
    assert result["notes"] == "good night"


async def test_delete_sleep(mock_api: respx.MockRouter) -> None:
    mock_api.delete("/api/sleep/1/").mock(return_value=httpx.Response(204))
    result = await delete_sleep(1)
    assert "1" in result
