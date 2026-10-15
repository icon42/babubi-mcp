from typing import Annotated

from fastmcp import FastMCP

from ..client import (
    QueryParams,
    api_delete,
    api_get,
    api_list,
    api_patch,
    api_patch_action,
    api_post,
)

mcp = FastMCP("timers")


@mcp.tool
async def list_timers(
    child_id: Annotated[int | None, "Filter by child ID. Use list_children to get IDs."] = None,
    name: Annotated[str | None, "Filter by exact timer name"] = None,
    ordering: Annotated[str | None, "Order by field, e.g. 'start' or '-start' (descending)"] = None,
) -> list[dict[str, object]]:
    """List active and recent timers. Use timer IDs when creating feedings, sleep, pumping, or tummy time records."""
    params: QueryParams = {}
    if child_id is not None:
        params["child"] = child_id
    if name is not None:
        params["name"] = name
    if ordering is not None:
        params["ordering"] = ordering
    return await api_list("timers", params)


@mcp.tool
async def get_timer(
    timer_id: Annotated[int, "ID of the timer to retrieve"],
) -> dict[str, object]:
    """Get a specific timer to see its name, start time, and elapsed duration."""
    return await api_get(f"timers/{timer_id}")


@mcp.tool
async def create_timer(
    name: Annotated[str | None, "Optional name for the timer (e.g. 'Feeding', 'Nap')"] = None,
    child_id: Annotated[int | None, "ID of the child to associate with this timer"] = None,
) -> dict[str, object]:
    """Start a new timer. Use the returned ID when finishing a feeding, sleep, pumping, or tummy time session."""
    data: dict[str, object] = {}
    if name is not None:
        data["name"] = name
    if child_id is not None:
        data["child"] = child_id
    return await api_post("timers", data)


@mcp.tool
async def update_timer(
    timer_id: Annotated[int, "ID of the timer to update"],
    name: Annotated[str | None, "New name for the timer"] = None,
    child_id: Annotated[int | None, "New child ID to associate with this timer"] = None,
) -> dict[str, object]:
    """Update a timer's name or child association."""
    data: dict[str, object] = {}
    if name is not None:
        data["name"] = name
    if child_id is not None:
        data["child"] = child_id
    return await api_patch("timers", timer_id, data)


@mcp.tool
async def restart_timer(
    timer_id: Annotated[int, "ID of the timer to restart"],
) -> dict[str, object]:
    """Restart a timer, resetting its start time to now while keeping the same timer."""
    return await api_patch_action("timers", timer_id, "restart")


@mcp.tool
async def delete_timer(
    timer_id: Annotated[int, "ID of the timer to stop and delete"],
) -> str:
    """Stop and delete a timer. Use create_feeding/create_sleep/etc. with timer_id first to log the session."""
    await api_delete("timers", timer_id)
    return f"Timer {timer_id} deleted successfully."
