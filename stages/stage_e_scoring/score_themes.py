"""Tag the episode's themes."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def score_themes(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    prompt = (
        "List the dominant themes as tags.\n"
        f"summary={content['summary'][:64]}\nfantastical={content.get('fantastical_intensity')}"
    )
    theme_tags = client.llm_large(prompt, output_schema="theme_tags_v1")
    return {"theme_tags": theme_tags}
