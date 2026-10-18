# Receiving the GLM result

Historical GLM workflow. The owner changed routing on 2026-10-09: Codex is the
primary architect/implementer; Claude checks near-final work only. Current
instructions are in `receive-review-output.md` and `../README.md`. Preserve this
file as history; do not use its GLM correction routing by default.

## What the owner returns to Codex

Paste GLM's final response and the path to its implementation report, manifest,
candidate directory and validation results. Keep output files in this workspace;
if generated elsewhere, supply a ZIP and its SHA-256 for import into a new
version directory. Do not replace the imported v2 package or loose images.

## Codex technical gate

1. Read the issued prompt, current status and acceptance criteria; inspect the
   actual returned files rather than treating the GLM token as proof.
2. Recheck the original ZIP/master hashes and protected source files. Compare
   actual changed files to the issued allow-list and recorded baseline.
3. Run from the repository root using `/usr/bin/python3` (system Pillow;
   the book venv may shadow the `python3` command). Use the active candidate
   path recorded in phase-status; revision 2 targets v5:

   ```bash
   rtk proxy /usr/bin/python3 Characters/tahmures/workflow/tools/validate_submission.py \
     --candidate Characters/tahmures/versions/layout01-v5 \
     --baseline Characters/tahmures/versions/layout01-v2
   ```

   Save stdout and exit code as a new `reports/codex/` verification artifact.
   This script reads inputs only and does not advance a status or approve art.
   In particular, opacity passes do not prove removal of a baked moustache,
   a residual smile, or a misplaced opening. See verification-01's exact
   findings and captures, and verification-02's dark remnant, colour-seam
   tears and neck bands; repeat visual QA of those interfaces. Equality to
   a moustache-free underlay does not establish that the underlay is clean.
4. Independently composite components and repeat the documented stress
   transforms. Compare unadorned preview bytes. Inspect every actual PNG/mask,
   the three state composites and source comparison at 100% and 2–4×, on
   light/dark/checker backgrounds. Count-only success is insufficient.
5. Assess each criterion in `acceptance-criteria.json`: `PASS`, `FAIL`, or
   `NOT_VERIFIED`, with evidence. Classify defects as `BLOCKER`, `NONBLOCKING`,
   or `OWNER_ART_DECISION`. Record the exact candidate hash set and findings.
6. Record actual validation scope; `git diff --check` and the repository gate
   must stay healthy. Do not repair unrelated failures in this asset phase.

## Routing the outcome

Any open technical/visual blocker: update the phase record to
`GLM_REVISION_PENDING`, append a history event, and create
`prompts/glm-layout01-revision-N.md` containing only exact open defects, their
locations, minimum repairs and tests. At most two internal correction prompts
before escalating unresolved art/identity ambiguity. Never erase older reports.

All Codex criteria pass: save `reports/codex/technical-acceptance-N.md`, mark
Codex technical acceptance true with its evidence, create the final independent
`prompts/claude-layout01-final-review.md`, and a `prompts/glm-next-phase-draft.md`
marked `NOT_RELEASED`. The Claude packet includes original master, editable
sprites, masks/provenance, previews A–E, stress samples, test results, actual
GLM summary, Codex report and honest limitations. Require independent review
and one of the three Claude tokens; do not invoke an unconfigured CLI/provider.

Claude rejection becomes a bounded GLM prompt using its actual findings. Claude
acceptance requires an actual saved response bound to the submitted files;
only then request human visual approval. Record that explicit owner's decision
with date and candidate hashes before approving/freezing an asset version or
releasing any next-phase task. This task has no Claude result or human puppet
approval to record yet.
