import httpx
import pytest
import respx

from babubi_mcp.tools.tummy_times import (
    create_tummy_time,
    delete_tummy_time,
    list_tummy_times,
    update_tummy_time,
)

BASE = "http://test-babubi"

TUMMY = {"id": 1, "child": 1, "start": "2024-01-15T10:00:00Z", "end": "2024-01-15T10:15:00Z"}


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url=BASE, assert_all_called=False) as router:
        yield router


async def test_list_tummy_times(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/tummy-times/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "next": None, "previous": None, "results": [TUMMY]}
        )
    )
    result = await list_tummy_times()
    assert result[0]["id"] == 1


async def test_create_tummy_time(mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/tummy-times/").mock(return_value=httpx.Response(201, json=TUMMY))
    result = await create_tummy_time(
        child_id=1, start="2024-01-15T10:00:00", end="2024-01-15T10:15:00"
    )
    assert result["id"] == 1


async def test_create_tummy_time_with_milestone(mock_api: respx.MockRouter) -> None:
    route = mock_api.post("/api/tummy-times/").mock(
        return_value=httpx.Response(201, json={**TUMMY, "milestone": "Lifted head"})
    )
    await create_tummy_time(
        child_id=1,
        start="2024-01-15T10:00:00",
        end="2024-01-15T10:15:00",
        milestone="Lifted head",
    )
    assert b"milestone" in route.calls[0].request.content


async def test_update_tummy_time(mock_api: respx.MockRouter) -> None:
    mock_api.patch("/api/tummy-times/1/").mock(
        return_value=httpx.Response(200, json={**TUMMY, "milestone": "Rolled over"})
    )
    result = await update_tummy_time(1, milestone="Rolled over")
    assert result["milestone"] == "Rolled over"


async def test_delete_tummy_time(mock_api: respx.MockRouter) -> None:
    mock_api.delete("/api/tummy-times/1/").mock(return_value=httpx.Response(204))
    result = await delete_tummy_time(1)
    assert "1" in result
