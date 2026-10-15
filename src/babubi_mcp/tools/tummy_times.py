from typing import Annotated

from fastmcp import FastMCP

from ..client import QueryParams, api_delete, api_list, api_patch, api_post

mcp = FastMCP("tummy_times")


@mcp.tool
async def list_tummy_times(
    child_id: Annotated[int | None, "Filter by child ID. Use list_children to get IDs."] = None,
    start: Annotated[str | None, "Filter by exact start time, ISO 8601"] = None,
    start_min: Annotated[str | None, "Earliest start time, ISO 8601"] = None,
    start_max: Annotated[str | None, "Latest start time, ISO 8601"] = None,
    end: Annotated[str | None, "Filter by exact end time, ISO 8601"] = None,
    end_min: Annotated[str | None, "Earliest end time, ISO 8601"] = None,
    end_max: Annotated[str | None, "Latest end time, ISO 8601"] = None,
    tags: Annotated[list[str] | None, "Filter by tag names (records having all listed tags)"] = None,
    ordering: Annotated[str | None, "Order by field, e.g. 'start' or '-start' (descending)"] = None,
    limit: Annotated[int, "Maximum number of records to return"] = 50,
) -> list[dict[str, object]]:
    """List tummy time session records with optional filters."""
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
    if tags:
        params["tags"] = ",".join(tags)
    if ordering is not None:
        params["ordering"] = ordering
    return await api_list("tummy-times", params)


@mcp.tool
async def create_tummy_time(
    child_id: Annotated[int, "ID of the child. Use list_children to get IDs."],
    start: Annotated[str, "Start time in ISO 8601 format (e.g. 2024-01-15T10:00:00)"],
    end: Annotated[str, "End time in ISO 8601 format"],
    milestone: Annotated[str | None, "Optional milestone achieved during this session"] = None,
    notes: Annotated[str | None, "Optional notes"] = None,
    timer_id: Annotated[
        int | None,
        "Use a running timer instead of explicit start/end times. Use list_timers to find active timers.",
    ] = None,
) -> dict[str, object]:
    """Record a tummy time session."""
    data: dict[str, object] = {
        "child": child_id,
        "start": start,
        "end": end,
    }
    if milestone is not None:
        data["milestone"] = milestone
    if notes is not None:
        data["notes"] = notes
    if timer_id is not None:
        data["timer"] = timer_id
    return await api_post("tummy-times", data)


@mcp.tool
async def update_tummy_time(
    tummy_time_id: Annotated[int, "ID of the tummy time record to update"],
    start: Annotated[str | None, "New start time in ISO 8601 format"] = None,
    end: Annotated[str | None, "New end time in ISO 8601 format"] = None,
    milestone: Annotated[str | None, "New milestone text"] = None,
    notes: Annotated[str | None, "New notes"] = None,
) -> dict[str, object]:
    """Update an existing tummy time record. Only provided fields are changed."""
    data: dict[str, object] = {}
    if start is not None:
        data["start"] = start
    if end is not None:
        data["end"] = end
    if milestone is not None:
        data["milestone"] = milestone
    if notes is not None:
        data["notes"] = notes
    return await api_patch("tummy-times", tummy_time_id, data)


@mcp.tool
async def delete_tummy_time(
    tummy_time_id: Annotated[int, "ID of the tummy time record to permanently delete"],
) -> str:
    """Delete a tummy time record. This action is permanent."""
    await api_delete("tummy-times", tummy_time_id)
    return f"Tummy time record {tummy_time_id} deleted successfully."
