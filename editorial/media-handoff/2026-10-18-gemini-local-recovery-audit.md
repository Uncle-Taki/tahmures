# Gemini handoff: local execution and corrected claims

The supplied response is treated as an implementation proposal and received
artifact inventory, not evidence that the local repository changed. The original
root ZIP and extra extracted copies are preserved. The maintained candidate is
`Characters/godot-character-library-recovery-01/`.

## Findings and repairs actually performed

| Received problem | Local result |
|---|---|
| Builder fails at line 190 with an unterminated string literal. | Fixed the newline serialization; ran the builder locally for ten sources. |
| Validator fails at line 90 with the same syntax defect. | Replaced it with fail-closed validation and reran it. |
| Builder preserves background RGB under alpha zero, causing its own exact-array recomposition assertion to fail. | Canonical transparent RGB; existing partial alpha retained. Boundary/partial-alpha regression tests added. |
| Validator silently skips missing source files/component maps and does not actually verify all claimed frozen approval checks. | Required input/output existence, all source hashes, both full indexes and approval bindings, 17 copied head hashes, layer masks/provenance/stats and exact composites now checked. |
| Component coordinates and readiness labels are presented as measured/ready without establishing actual anatomy. | Local measurements recorded in component maps. Received measurements are labelled as claims. All new body partitions marked as candidates requiring anatomical review. |
| Generic rig advertises blink/gaze/gestures without valid separated features or underlap art. | Those states disabled. Neutral and whole-pose idle/reset remain; no false anatomical capability. |
| Head/body sprites use centered coordinates despite full source-canvas assets. | Source coordinates corrected. Accepted Tahmures head shown separately without falsely certifying a new body/head assembly. |
| Gallery's checker option uses a solid dark color and state selection suggests unimplemented capabilities. | Real checker/light/dark rendering, explicit capability labels, reset and accepted-head inspector. |
| Missing or malformed runtime maps may leave a partial/empty actor. | Godot positive tests and expected nonzero missing/malformed-resource tests added and executed. |
| Godot initially hits sandbox user-data/config/socket errors. | Reran with approved normal Godot access. Actual import and runtime results recorded, rather than relying on exit code alone. |
| Proposed Phase C helper recursively deletes an existing candidate and substitutes complete cutout textures while claiming layered-rig integration. | Replaced with non-mutating planning only. No source/rejected chapter project is deleted, patched or promoted. |

The original ten source identities and frozen approval-bound package bytes match
their records. No original PNG, accepted package, approval, book chapter,
translation hash or live phase-status record was changed by this local repair.

## Actual evidence and limits

- `validation.json` and `evidence/local-checks.json` inside the maintained candidate.
- Seven focused Python regressions, plus ten-rig/head runtime assertions.
- Expected nonzero exits for missing and malformed resources; they are passing
  negative tests, not unresolved command failures.
- Actual Godot captures for ten neutral source-pose candidates, one whole-pose
  idle sample, and the accepted head's neutral/thinking/blink states.
- Source-versus-layer, isolated-component and light/dark/checker plates built
  from local outputs. The received gallery is retained separately.
- Python formatting/lint checks for the maintained recovery scripts and exchange
  packager, plus `git diff --check`.

Visual inspection confirms useful source-faithful neutral candidates, not
completed anatomical rigs. Akvan's rectangular face/prop cuts and Tahmures's
empty neck partition demonstrate the remaining work. Neutral pixel equality
alone cannot certify joints or expose missing surfaces. No new final-art,
character-readiness or narrated-chapter approval is inferred from the tests.

The repository gate was actually rerun and remains red: **789 passed, eight
failed**, from stale Persian Chapters 01–04 source hashes. It stops at Python
tests, so subsequent `make check` stages are not claimed as run/passing. Those
failures require the separate current-revision editorial review and authorized
reconciliation; this media task does not silently mark English sources final.

## Next work and transfer

The immediate AI Studio task is Akvan anatomical extraction only. The owner
selected **Google AI Studio Build mode**. The roadmap, exact task, result template
and a selected local source snapshot are prepared under `editorial/media-handoff/`.
Codex remains the local acceptance checker; the owner retains art/voice decisions.
No GitHub remote is configured and no commit, push, cloud call or deployment was
performed. The historical Gemini upload ZIPs were not refreshed by this new task;
the new `ai-studio-exchange.zip` is the next-phase baseline.
