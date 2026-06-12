"""Aggregate the Plot & Story sub-scores into a single domain score."""

from __future__ import annotations

from typing import Any

from stages.common import rubric_score


def aggregate_plot(parts: dict[str, Any]) -> dict[str, Any]:
    score = rubric_score(
        "plot",
        parts["plot_coherence"],
        parts["pacing"],
        parts["dialogue_quality"],
        parts["character_arc"],
        parts["subtext"],
    )
    details = {k: v for k, v in parts.items() if k.endswith("_reasoning")}
    return {"plot_score": score, "plot_details": details}
