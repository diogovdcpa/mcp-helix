from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def load_project_env() -> None:
    root = Path(__file__).resolve().parents[2]
    load_dotenv(root / ".env", override=False)
    load_dotenv(root.parent / ".env", override=False)


@dataclass(frozen=True)
class Settings:
    client_id: str
    client_secret: str
    api_key: str
    token_endpoint: str
    api_base_url: str
    timeout_seconds: int = 60
    log_level: str = "INFO"


def get_settings() -> Settings:
    load_project_env()

    return Settings(
        client_id=os.getenv("TRELLIX_CLIENT_ID", "").strip(),
        client_secret=os.getenv("TRELLIX_CLIENT_SECRET", "").strip(),
        api_key=os.getenv("TRELLIX_API_KEY", "").strip(),
        token_endpoint=os.getenv(
            "TRELLIX_TOKEN_ENDPOINT",
            "https://iam.cloud.trellix.com/iam/v1.0/token",
        ).strip(),
        api_base_url=os.getenv("API_BASE_URL", "https://apps.fireeye.com").strip(),
        timeout_seconds=int(os.getenv("TIMEOUT_SECONDS", "60")),
        log_level=os.getenv("MCP_HELIX_LOG_LEVEL", "INFO").strip().upper(),
    )


def configure_logging() -> None:
    settings = get_settings()
    level = getattr(logging, settings.log_level, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
