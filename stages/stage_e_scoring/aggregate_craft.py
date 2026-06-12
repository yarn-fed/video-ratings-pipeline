"""Aggregate the Craft sub-scores into a single domain score."""

from __future__ import annotations

from typing import Any

from stages.common import rubric_score


def aggregate_craft(parts: dict[str, Any]) -> dict[str, Any]:
    score = rubric_score(
        "craft",
        parts["cinematography"],
        parts["editing"],
        parts["sound_design"],
        parts["lighting"],
    )
    details = {k: v for k, v in parts.items() if k.endswith("_reasoning")}
    # soundtrack_mood is carried through for legacy clients.
    details["soundtrack_mood"] = parts.get("soundtrack_mood")
    return {"craft_score": score, "craft_details": details}
