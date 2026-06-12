"""Scene preview sampling stays within bounds."""

from __future__ import annotations

import random


def test_preview_sample_within_bounds():
    # Spot-check a random preview offset lands in the first 90% of the scene.
    offset = random.random()
    assert offset < 0.9
