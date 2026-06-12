"""Detect hard-cut markers from the subtitle cue stream."""

from __future__ import annotations

import re
from typing import Any


def detect_shot_changes(stage_a: dict[str, Any]) -> dict[str, Any]:
    subtitle_blob = stage_a["fetch"]["raw_metadata"].get("subtitles_raw", "")
    lines = subtitle_blob.splitlines()

    markers = []
    for i, line in enumerate(lines):
        # Cue timestamps look like "00:00:01,000 --> 00:00:03,500".
        pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})")
        m = pattern.search(line)
        if m:
            markers.append({"line": i, "start": m.group(1), "end": m.group(2)})

    return {"shot_change_markers": markers}
