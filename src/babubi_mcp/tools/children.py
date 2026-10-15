from typing import Annotated

from fastmcp import FastMCP

from ..client import QueryParams, api_get, api_list, api_patch, api_post

mcp = FastMCP("children")


@mcp.tool
async def list_children(
    first_name: Annotated[str | None, "Filter by exact first name"] = None,
    last_name: Annotated[str | None, "Filter by exact last name"] = None,
    birth_date: Annotated[str | None, "Filter by birth date, YYYY-MM-DD"] = None,
    ordering: Annotated[
        str | None, "Order by field, e.g. 'birth_date' or '-birth_date' (descending)"
    ] = None,
) -> list[dict[str, object]]:
    """List child profiles. Always call this first to get child IDs and slugs needed by other tools."""
    params: QueryParams = {}
    if first_name is not None:
        params["first_name"] = first_name
    if last_name is not None:
        params["last_name"] = last_name
    if birth_date is not None:
        params["birth_date"] = birth_date
    if ordering is not None:
        params["ordering"] = ordering
    return await api_list("children", params or None)


@mcp.tool
async def get_child(
    slug: Annotated[str, "Slug of the child to retrieve (the 'slug' field from list_children)"],
) -> dict[str, object]:
    """Get a single child profile by slug. Children are keyed by slug, not numeric ID."""
    return await api_get(f"children/{slug}")


@mcp.tool
async def create_child(
    first_name: Annotated[str, "Child's first name"],
    last_name: Annotated[str, "Child's last name"],
    birth_date: Annotated[str, "Date of birth in YYYY-MM-DD format (e.g. 2024-01-15)"],
    birth_time: Annotated[str | None, "Time of birth in HH:MM:SS format (optional)"] = None,
) -> dict[str, object]:
    """Add a new child profile."""
    data: dict[str, object] = {
        "first_name": first_name,
        "last_name": last_name,
        "birth_date": birth_date,
    }
    if birth_time is not None:
        data["birth_time"] = birth_time
    return await api_post("children", data)


@mcp.tool
async def update_child(
    slug: Annotated[str, "Slug of the child to update (the 'slug' field from list_children)"],
    first_name: Annotated[str | None, "New first name"] = None,
    last_name: Annotated[str | None, "New last name"] = None,
    birth_date: Annotated[str | None, "New birth date in YYYY-MM-DD format"] = None,
    birth_time: Annotated[str | None, "New birth time in HH:MM:SS format"] = None,
) -> dict[str, object]:
    """Update a child's profile by slug. Only provided fields are changed."""
    data: dict[str, object] = {}
    if first_name is not None:
        data["first_name"] = first_name
    if last_name is not None:
        data["last_name"] = last_name
    if birth_date is not None:
        data["birth_date"] = birth_date
    if birth_time is not None:
        data["birth_time"] = birth_time
    return await api_patch("children", slug, data)
