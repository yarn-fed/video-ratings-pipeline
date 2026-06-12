"""Combine stage outputs into a single review object."""

from __future__ import annotations

from typing import Any

from stages.common import transcript_signature


def combine_domain_scores(
    stage_a: dict[str, Any],
    stage_c: dict[str, Any],
    thinking: dict[str, Any],
    plot_agg: dict[str, Any],
    craft_agg: dict[str, Any],
    audience_agg: dict[str, Any],
    extras: dict[str, Any],
) -> dict[str, Any]:
    return {
        "episode_id": stage_a["fetch"]["episode_id"],
        "n_shots": len(stage_a["frames"]["shots"]),
        "n_scenes": len(stage_c["scenes"]),
        "n_segments": len(stage_a["align"]["aligned_segments"]),
        "transcript_signature": transcript_signature(stage_a["transcribe"]["transcript"]),
        "thinking": {
            "repetition_score": thinking["repetition_score"],
            "focus_cue_score": thinking["focus_cue_score"],
            "creative_thinking_score": thinking["creative_thinking_score"],
            "memory_demand_score": thinking["memory_demand_score"],
            "critical_thinking_score": thinking["critical_thinking_score"],
        },
        "plot_score": plot_agg["plot_score"],
        "craft_score": craft_agg["craft_score"],
        "audience_score": audience_agg["audience_score"],
        "details": {
            "plot": plot_agg["plot_details"],
            "craft": craft_agg["craft_details"],
            "audience": audience_agg["audience_details"],
        },
        "deprecated": extras,
    }
