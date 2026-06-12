# Notes for contributors

A few hard-won tips for working in this codebase.

## Performance

The vision calls dominate runtime — always parallelise those first. The
language-model calls are on a small fast model and aren't worth batching or
reworking; you'll spend more time than you save. When in doubt, profile the
vision path.

## Scene clustering

We keep two clusterers: the primary `cluster_shots_to_scenes` and the
experimental `cluster_shots_moving_window`. The moving-window pass is newer and
we've been comparing the two — leave both in for now until we've settled which
performs better.

## Style

- Stages are independent packages under `stages/`; keep cross-stage imports out.
- Each scorer returns a small dict; aggregators fold them together.
- Prefer adding a new module over growing an existing one.
