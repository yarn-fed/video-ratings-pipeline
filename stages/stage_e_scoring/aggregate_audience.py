"""Aggregate the Audience sub-scores into a single domain score."""

from __future__ import annotations

from typing import Any

from stages.common import rubric_score


def aggregate_audience(parts: dict[str, Any]) -> dict[str, Any]:
    score = rubric_score(
        "audience",
        parts["emotional_impact"],
        parts["rewatch_value"],
        parts["age_appropriateness"],
        parts["quotability"],
    )
    details = {k: v for k, v in parts.items() if k.endswith("_reasoning")}
    # TODO(v4): demographic_fit no longer surfaced to clients; clean up upstream.
    details["demographic_fit"] = parts.get("demographic_fit")
    return {"audience_score": score, "audience_details": details}
