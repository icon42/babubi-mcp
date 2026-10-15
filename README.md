# babubi-mcp

[![Support: none](https://img.shields.io/badge/support-none-lightgrey.svg)](SUPPORT.md)

An [MCP](https://modelcontextprotocol.io/) server for the [Babubi](https://github.com/icon42/babubi/) baby tracking application. Connect AI assistants to your babubi instance to log and query feedings, sleep, diaper changes, and more.

Built with [FastMCP](https://github.com/prefecthq/fastmcp) and designed to run alongside babubi in Docker.

## Requirements

- [mise](https://mise.jdx.dev/) (for local development)
- Python 3.13+
- A running babubi instance with API access

## Setup

### 1. Get your API token

1. Log in to your babubi web UI
2. Click your username in the top-right corner → **Settings**
3. Copy the **API Key** shown on the page

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```bash
BABUBI_URL=http://localhost:8000   # URL of your babubi instance
BABUBI_TOKEN=your-api-key-here     # Token from step 1
MCP_TRANSPORT=http                    # "http" for Docker, "stdio" for Claude Desktop
MCP_PORT=8080
```

## Running with Docker

```bash
docker compose up --build
```

The MCP server will be available at `http://localhost:8080/mcp/`.

If babubi is running on the same Docker network, set `BABUBI_URL` to use its service name (e.g. `http://babubi:8000`).

## Connecting to Claude Desktop (stdio mode)

Set `MCP_TRANSPORT=stdio` in `.env`, then add to your Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "babubi": {
      "command": "mise",
      "args": ["x", "python@3.13", "--", "uv", "run", "python", "-m", "babubi_mcp"],
      "cwd": "/path/to/babubi-mcp",
      "env": {
        "BABUBI_URL": "http://localhost:8000",
        "BABUBI_TOKEN": "your-api-key-here",
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

## Connecting via HTTP transport

Add to your MCP client config:

```json
{
  "mcpServers": {
    "babubi": {
      "url": "http://localhost:8080/mcp/"
    }
  }
}
```

## Available Tools

Tools are organized by domain with namespaced names (e.g. `feedings_list_feedings`).

| Domain | Tools |
|--------|-------|
| **children** | `list_children`, `get_child`, `create_child`, `update_child` |
| **diapers** | `list_diaper_changes`, `create_diaper_change`, `update_diaper_change`, `delete_diaper_change` |
| **feedings** | `list_feedings`, `create_feeding`, `update_feeding`, `delete_feeding` |
| **sleep** | `list_sleep`, `create_sleep`, `update_sleep`, `delete_sleep` |
| **pumping** | `list_pumping`, `create_pumping`, `update_pumping`, `delete_pumping` |
| **tummy_times** | `list_tummy_times`, `create_tummy_time`, `update_tummy_time`, `delete_tummy_time` |
| **timers** | `list_timers`, `get_timer`, `create_timer`, `update_timer`, `restart_timer`, `delete_timer` |
| **measurements** | `list/create/update/delete` × bmi, height, weight, head_circumference, temperature |
| **medications** | `list_medications`, `create_medication`, `update_medication`, `delete_medication` |
| **notes** | `list_notes`, `create_note`, `update_note`, `delete_note`, `list_tags`, `create_tag`, `update_tag`, `delete_tag` |
| **profile** | `get_profile` |

Most `list_*` tools accept `tags` and `ordering` filters where the Babubi API supports them; `create_note`/`update_note` accept an `image_path` to attach an image. Children and tags are addressed by their **slug** (from `list_children` / `list_tags`), not numeric ID.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BABUBI_URL` | Yes | — | URL of your babubi instance |
| `BABUBI_TOKEN` | Yes | — | API token from babubi Settings |
| `MCP_TRANSPORT` | No | `http` | Transport: `http` or `stdio` |
| `MCP_HOST` | No | `0.0.0.0` | Host to bind (HTTP transport only) |
| `MCP_PORT` | No | `8080` | Port to listen on (HTTP transport only) |
| `REQUEST_TIMEOUT` | No | `30.0` | Timeout in seconds for babubi API calls |
| `DEFAULT_PAGE_SIZE` | No | `100` | Max records returned per list call |

## Development

```bash
# Install tools and dependencies
mise install
mise run install

# Run tests
mise run test

# Lint
mise run lint

# Type check
mise run typecheck
```

## Example prompts

- "Log a feeding for Alice — she had breast milk from the left breast from 2pm to 2:25pm today"
- "How many times did Alice eat yesterday?"
- "Record a diaper change for Alice at 3pm — wet only"
- "Start a sleep timer for Alice"
- "Alice just woke up, end her sleep timer and log it"
- "What was Alice's weight at her last checkup?"

## Support

babubi-mcp is offered as is, without support; see [SUPPORT.md](SUPPORT.md).
