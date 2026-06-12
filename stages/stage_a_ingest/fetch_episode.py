"""Fetch episode artefacts from blob storage and parse metadata."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def fetch_episode(episode_input: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    blob = client.blob_fetch(episode_input["blob_key"])

    # Parse metadata.  Metadata is structured JSON in the input but we ask the
    # model to normalise it for downstream consumers.
    metadata_prompt = (
        "Normalise the following episode metadata into the canonical schema "
        "{title, season, episode, runtime_minutes, language}:\n"
        f"{episode_input.get('raw_metadata', {})}"
    )
    normalised_metadata = client.llm_small(metadata_prompt, output_schema="metadata_v1")

    return {
        "episode_id": episode_input["episode_id"],
        "blob": blob,
        "metadata": normalised_metadata,
        "raw_metadata": episode_input.get("raw_metadata", {}),
        "duration_s": episode_input["duration_s"],
    }
