import httpx
import pytest
import respx

from babubi_mcp.tools.profile import get_profile

BASE = "http://test-babubi"

PROFILE = {
    "user": {"id": 1, "username": "parent", "email": "parent@example.com"},
    "language": "en",
    "timezone": "America/New_York",
    "api_key": "abc123",
}


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url=BASE, assert_all_called=False) as router:
        yield router


async def test_get_profile_no_trailing_slash(mock_api: respx.MockRouter) -> None:
    route = mock_api.get("/api/profile").mock(
        return_value=httpx.Response(200, json=PROFILE)
    )
    result = await get_profile()
    assert route.called
    assert result["timezone"] == "America/New_York"
    assert result["api_key"] == "abc123"
