import pytest
import respx

from babubi_mcp import client as client_module
from babubi_mcp.config import settings


@pytest.fixture(autouse=True)
def mock_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "babubi_url", "http://test-babubi")
    monkeypatch.setattr(settings, "babubi_token", "test-token")


@pytest.fixture(autouse=True)
def reset_client() -> None:
    """Reset the shared httpx client between tests."""
    client_module._client = None


@pytest.fixture
def mock_api() -> respx.MockRouter:
    """Provide a respx router pre-configured for the test babubi instance."""
    with respx.mock(base_url="http://test-babubi", assert_all_called=False) as router:
        yield router


def paginated(results: list[object]) -> dict[str, object]:
    """Wrap results in DRF pagination envelope."""
    return {"count": len(results), "next": None, "previous": None, "results": results}
