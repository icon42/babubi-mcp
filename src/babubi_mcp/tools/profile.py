from fastmcp import FastMCP

from ..client import api_get_raw

mcp = FastMCP("profile")


@mcp.tool
async def get_profile() -> dict[str, object]:
    """Get the current authenticated user's profile: user details, language, timezone, and API key."""
    return await api_get_raw("profile")
