from typing import Annotated

from fastmcp import FastMCP

from ..client import QueryParams, api_delete, api_list, api_patch, api_post

mcp = FastMCP("feedings")

_TYPES = "breast milk, formula, fortified breast milk, solid food"
_METHODS = "bottle, left breast, right breast, both breasts, parent fed, self fed"


@mcp.tool
async def list_feedings(
    child_id: Annotated[int | None, "Filter by child ID. Use list_children to get IDs."] = None,
    start: Annotated[str | None, "Filter by exact start time, ISO 8601"] = None,
    start_min: Annotated[str | None, "Earliest start time, ISO 8601"] = None,
    start_max: Annotated[str | None, "Latest start time, ISO 8601"] = None,
    end: Annotated[str | None, "Filter by exact end time, ISO 8601"] = None,
    end_min: Annotated[str | None, "Earliest end time, ISO 8601"] = None,
    end_max: Annotated[str | None, "Latest end time, ISO 8601"] = None,
    feeding_type: Annotated[str | None, f"Filter by type: {_TYPES}"] = None,
    method: Annotated[str | None, f"Filter by method: {_METHODS}"] = None,
    tags: Annotated[list[str] | None, "Filter by tag names (records having all listed tags)"] = None,
    ordering: Annotated[str | None, "Order by field, e.g. 'start' or '-start' (descending)"] = None,
    limit: Annotated[int, "Maximum number of records to return"] = 50,
) -> list[dict[str, object]]:
    """List feeding records with optional filters."""
    params: QueryParams = {"limit": limit}
    if child_id is not None:
        params["child"] = child_id
    if start is not None:
        params["start"] = start
    if start_min is not None:
        params["start_min"] = start_min
    if start_max is not None:
        params["start_max"] = start_max
    if end is not None:
        params["end"] = end
    if end_min is not None:
        params["end_min"] = end_min
    if end_max is not None:
        params["end_max"] = end_max
    if feeding_type is not None:
        params["type"] = feeding_type
    if method is not None:
        params["method"] = method
    if tags:
        params["tags"] = ",".join(tags)
    if ordering is not None:
        params["ordering"] = ordering
    return await api_list("feedings", params)


@mcp.tool
async def create_feeding(
    child_id: Annotated[int, "ID of the child. Use list_children to get IDs."],
    start: Annotated[str, "Start time in ISO 8601 format (e.g. 2024-01-15T14:30:00)"],
    end: Annotated[str, "End time in ISO 8601 format"],
    feeding_type: Annotated[str, f"Type of feeding: {_TYPES}"],
    method: Annotated[str, f"Feeding method: {_METHODS}"],
    amount: Annotated[float | None, "Amount fed (units depend on babubi settings)"] = None,
    notes: Annotated[str | None, "Optional notes"] = None,
    timer_id: Annotated[
        int | None,
        "Use a running timer instead of explicit start/end times. Use list_timers to find active timers.",
    ] = None,
) -> dict[str, object]:
    """Record a feeding session."""
    data: dict[str, object] = {
        "child": child_id,
        "start": start,
        "end": end,
        "type": feeding_type,
        "method": method,
    }
    if amount is not None:
        data["amount"] = amount
    if notes is not None:
        data["notes"] = notes
    if timer_id is not None:
        data["timer"] = timer_id
    return await api_post("feedings", data)


@mcp.tool
async def update_feeding(
    feeding_id: Annotated[int, "ID of the feeding record to update"],
    start: Annotated[str | None, "New start time in ISO 8601 format"] = None,
    end: Annotated[str | None, "New end time in ISO 8601 format"] = None,
    feeding_type: Annotated[str | None, f"New type: {_TYPES}"] = None,
    method: Annotated[str | None, f"New method: {_METHODS}"] = None,
    amount: Annotated[float | None, "New amount"] = None,
    notes: Annotated[str | None, "New notes"] = None,
) -> dict[str, object]:
    """Update an existing feeding record. Only provided fields are changed."""
    data: dict[str, object] = {}
    if start is not None:
        data["start"] = start
    if end is not None:
        data["end"] = end
    if feeding_type is not None:
        data["type"] = feeding_type
    if method is not None:
        data["method"] = method
    if amount is not None:
        data["amount"] = amount
    if notes is not None:
        data["notes"] = notes
    return await api_patch("feedings", feeding_id, data)


@mcp.tool
async def delete_feeding(
    feeding_id: Annotated[int, "ID of the feeding record to permanently delete"],
) -> str:
    """Delete a feeding record. This action is permanent."""
    await api_delete("feedings", feeding_id)
    return f"Feeding {feeding_id} deleted successfully."
