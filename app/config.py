"""Runtime configuration for the retrieval service."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Tunables, overridable via environment variables."""

    base_url: str = os.environ.get(
        "KB_BASE_URL", "https://handbook.thimbleby-toollibrary.org"
    )
    default_top_k: int = int(os.environ.get("KB_DEFAULT_TOP_K", "5"))
    max_top_k: int = int(os.environ.get("KB_MAX_TOP_K", "25"))
    chunk_tokens: int = int(os.environ.get("KB_CHUNK_TOKENS", "80"))
    chunk_overlap: int = int(os.environ.get("KB_CHUNK_OVERLAP", "20"))
    candidate_pool: int = int(os.environ.get("KB_CANDIDATE_POOL", "30"))


settings = Settings()
