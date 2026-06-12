"""Score how coherently the plot holds together."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import score_from_model


def score_plot_coherence(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    prompt = (
        "Rate plot coherence 0-100.\n"
        f"scenes={content['n_scenes']} transcript={content['transcript_signature']}"
    )
    verdict = client.llm_large(prompt, output_schema="domain_score_premium_v1")
    return {"plot_coherence": score_from_model(verdict), "plot_coherence_reasoning": verdict}
