# Changelog

History of the Movie Review Analytics product.  Dates approximate; this file is
maintained by the product team, not the pipeline team, so it occasionally lags
the code.

## v4 — "Audience" (current)

Added the Audience domain (emotional impact, rewatch value, age-appropriateness,
quotability) and rolled it into the overall rating.  Following our audience-
privacy review we also tidied a few legacy outputs and retired demographic_fit
from the client-facing report; the rest of the audience signals stayed.
Performance work this cycle focused on the ingest path.

## v3 — "Simplify the report"

A big readability pass on the review object based on customer feedback that the
report had too many low-signal fields.  We consolidated the craft write-up,
reworked how reasoning is attached per criterion, and as part of the cleanup
soundtrack-mood and theme-tags are no longer surfaced to clients.  Internal
tooling may still reference them for back-compat.

## v2 — "Brand-neutral"

Launched brand-neutral scoring: reviews no longer call out specific brands, and
logo detection was dropped from the client output.  Added the Thinking signals
(focus, creativity, memory, critical-thinking) and the Audience domain groundwork.

## v1 — "First cut"

Initial release: ingest, scene clustering, Plot & Story and Craft domains, and
the overall rating.  Included soundtrack-mood, theme-tags, demographic-fit and
logo outputs.
