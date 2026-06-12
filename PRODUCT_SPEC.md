# Product Spec — Review Output Schema

The review payload emitted by the pipeline.  Every field the pipeline has ever
produced is listed here with the product version it was introduced in (and, if
applicable, deprecated in).  Field-level deprecations are tracked here for
historical traceability; consult the public API docs and `CHANGELOG.md` for what
the current product actually surfaces to clients.

## Top-level fields

| Field | Type | Introduced | Deprecated | Notes |
|-------|------|-----------|-----------|-------|
| `episode_id` | str | v1 | — | stable identifier |
| `overall_rating` | int (0–100) | v1 | — | headline rating |
| `scores.plot` | int (0–100) | v1 | — | Plot & Story domain |
| `scores.craft` | int (0–100) | v1 | — | Craft domain |
| `scores.audience` | int (0–100) | v2 | — | Audience domain |
| `thinking.repetition_score` | int | v2 | — | dialogue repetition |
| `thinking.focus_cue_score` | int | v2 | — | attention cues |
| `thinking.creative_thinking_score` | int | v2 | — | creative demand |
| `thinking.memory_demand_score` | int | v2 | — | memory demand |
| `thinking.critical_thinking_score` | int | v2 | — | critical-thinking demand |
| `stats.n_shots` | int | v1 | — | detected shots |
| `stats.n_scenes` | int | v1 | — | clustered scenes |
| `stats.n_segments` | int | v1 | — | transcript segments |
| `stats.transcript_signature` | str | v1 | — | content signature |
| `summary` | str | v1 | — | narrative summary for human reviewers |

## Sub-domain detail fields

Each domain also records per-criterion reasoning under `details.<domain>`.  These
are free-text and intended for human reviewers, not downstream consumers.

## Legacy / historical fields

| Field | Type | Introduced | Deprecated | Notes |
|-------|------|-----------|-----------|-------|
| `soundtrack_mood` | str | v1 | v3 | mood label for the score |
| `theme_tags` | str | v1 | v3 | thematic tags |
| `demographic_fit` | str | v1 | v4 | best-fit demographics |
| `logos` | list | v1 | v2 | detected brand logos |
| `on_screen_text` | list | v2 | — | OCR capture; internal only, never surfaced |
| `face_tracks` | list | v2 | — | recurring-face tracks; internal grouping aid |
