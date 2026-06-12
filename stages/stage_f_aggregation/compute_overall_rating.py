"""Compute the overall rating and a human-readable summary."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import rubric_score


def compute_overall_rating(combined: dict[str, Any]) -> dict[str, Any]:
    client = get_client()

    # Narrative summary for the human reviewer.
    prompt = (
        "Write a one-paragraph review summary for these scores: "
        f"plot={combined['plot_score']} craft={combined['craft_score']} "
        f"audience={combined['audience_score']}"
    )
    summary = client.llm_large(prompt, output_schema="overall_rating_v2")

    rating = rubric_score(
        "overall",
        combined["plot_score"],
        combined["craft_score"],
        combined["audience_score"],
        sorted(combined["thinking"].items()),
    )
    return {"overall_rating": rating, "summary": summary}
