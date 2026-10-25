import httpx
import pytest
import respx

from babubi_mcp.tools.timers import (
    create_timer,
    delete_timer,
    get_timer,
    list_timers,
    restart_timer,
    update_timer,
)

BASE = "http://test-babubi"

TIMER = {"id": 1, "name": "Feeding", "start": "2024-01-15T10:00:00Z", "child": 1}


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url=BASE, assert_all_called=False) as router:
        yield router


async def test_list_timers(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/timers/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "next": None, "previous": None, "results": [TIMER]}
        )
    )
    result = await list_timers()
    assert result[0]["name"] == "Feeding"


async def test_get_timer(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/timers/1/").mock(return_value=httpx.Response(200, json=TIMER))
    result = await get_timer(1)
    assert result["id"] == 1


async def test_create_timer(mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/timers/").mock(return_value=httpx.Response(201, json=TIMER))
    result = await create_timer(name="Feeding", child_id=1)
    assert result["name"] == "Feeding"


async def test_create_timer_no_args(mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/timers/").mock(return_value=httpx.Response(201, json=TIMER))
    result = await create_timer()
    assert result["id"] == 1


async def test_update_timer(mock_api: respx.MockRouter) -> None:
    mock_api.patch("/api/timers/1/").mock(
        return_value=httpx.Response(200, json={**TIMER, "name": "Sleep"})
    )
    result = await update_timer(1, name="Sleep")
    assert result["name"] == "Sleep"


async def test_list_timers_name_filter(mock_api: respx.MockRouter) -> None:
    route = mock_api.get("/api/timers/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "next": None, "previous": None, "results": [TIMER]}
        )
    )
    await list_timers(name="Feeding")
    assert route.calls[0].request.url.params["name"] == "Feeding"
    await list_timers(name_contains="feed")
    assert route.calls[1].request.url.params["name__icontains"] == "feed"


async def test_restart_timer(mock_api: respx.MockRouter) -> None:
    route = mock_api.patch("/api/timers/1/restart/").mock(
        return_value=httpx.Response(200, json={**TIMER, "start": "2024-01-15T12:00:00Z"})
    )
    result = await restart_timer(1)
    assert route.called
    assert result["id"] == 1


async def test_delete_timer(mock_api: respx.MockRouter) -> None:
    mock_api.delete("/api/timers/1/").mock(return_value=httpx.Response(204))
    result = await delete_timer(1)
    assert "1" in result


async def test_create_timer_with_kind(mock_api: respx.MockRouter) -> None:
    route = mock_api.post("/api/timers/").mock(
        return_value=httpx.Response(201, json={**TIMER, "kind": "sleep"})
    )
    result = await create_timer(kind="sleep", child_id=1)
    assert b'"kind":"sleep"' in route.calls[0].request.content.replace(b" ", b"")
    assert result["kind"] == "sleep"


async def test_update_timer_kind(mock_api: respx.MockRouter) -> None:
    route = mock_api.patch("/api/timers/1/").mock(
        return_value=httpx.Response(200, json={**TIMER, "kind": "feeding"})
    )
    await update_timer(1, kind="feeding")
    assert b'"kind":"feeding"' in route.calls[0].request.content.replace(b" ", b"")
