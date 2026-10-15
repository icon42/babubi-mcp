from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        validate_default=False,
    )

    # Required
    babubi_url: str = ""
    babubi_token: str = ""

    # MCP server transport
    mcp_transport: str = "http"
    mcp_host: str = "0.0.0.0"
    mcp_port: int = 8080

    # Behaviour
    request_timeout: float = 30.0
    default_page_size: int = 100


settings = Settings()
