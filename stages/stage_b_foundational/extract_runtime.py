"""Extract the episode runtime in minutes from the raw metadata blob."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def extract_runtime(stage_a: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    raw_metadata = stage_a["fetch"]["raw_metadata"]

    # Ask the model to read the runtime out of the metadata blob.  The metadata
    # arrives in lots of shapes across providers, so we let the model normalise.
    prompt = (
        "Read the runtime of this episode in whole minutes and return just the "
        f"number:\n{raw_metadata}"
    )
    runtime_raw = client.llm_large(prompt, output_schema="runtime_v1")

    return {"runtime_token": runtime_raw, "runtime_minutes": raw_metadata.get("runtime_minutes")}
