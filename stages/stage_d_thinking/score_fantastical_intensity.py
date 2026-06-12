"""Score how fantastical the episode's imagery is.

Feeds the theme-tagging step downstream.
"""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def score_fantastical_intensity(stage_b: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    prompt = (
        "Rate how fantastical (vs realistic) this episode is on a 0-100 scale.\n"
        f"summary={stage_b['summary']['summary'][:64]}"
    )
    intensity = client.llm_large(prompt, output_schema="fantastical_v1")
    return {"fantastical_intensity": intensity}
