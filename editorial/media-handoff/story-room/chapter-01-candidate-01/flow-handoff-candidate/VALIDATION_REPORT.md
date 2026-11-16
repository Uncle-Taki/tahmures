**NOT APPROVED FOR PRODUCTION / NOT AUTHORIZED FOR FLOW GENERATION**

# Candidate validation and remaining production gates

[PROPOSAL] Technical bookkeeping PASS; independent writing second pass GO FOR OWNER REVIEW. All production/Flow generation remains BLOCKED. No movie/frame/voice was generated or newly rendered and no approval was assigned automatically.

## Actually executed

- [PROPOSAL] `rtk proxy python3 story-room/scripts/validate_skill_bundle.py .` — twelve skill files checked, zero errors.
- [PROPOSAL] `rtk proxy python3 editorial/media-handoff/story-room/chapter-01-candidate-01/scripts/validate_candidate.py` — PASS; machine results in manifests/candidate-validation.json. Negative traversal/absolute/missing-path fixtures rejected.
- [PROPOSAL] `make check PYTHON=.venv/bin/python` — observed exit 0, 797 Python tests, Go tests, formatting/lint, chapter/continuity/translation/editorial validation, all offline experiments, parity and both strict MkDocs builds. Full captured log: ../checks/repository-check.log. Six existing Persian `Agentها` metadata warnings were inspected in the prior source review and remain outside candidate scope; no translation change was made.
- [PROPOSAL] `git diff --check` — observed exit 0. It covers tracked differences; the candidate validator separately checks these newly created artifacts.

## Scope of candidate validation

[PROPOSAL] Hash audit covers 989 protected input files including canonical source, timeline, status/approval data and original Flow handoff files. Existing handoff snapshot separately checks all its noncache files. Source WAV hashes/durations, retained versus new/replaced words, null missing-recording paths, scene locators, all 48 cards, asset pointers/copies, cue/punch/change references, 53 impact rows, all candidate time fields and gate banners are checked. Source punch percentages use only the verified 251.3s baseline. New exact word/action landings remain TBD. No original image bytes were edited; two reference copies have candidate filenames and status sidecars. Forty-nine other image/vector assets are source pointers, not new masters.

[UNKNOWN] Local source existence is not external-upload rights, new art approval, actual Character registration, model availability or account credit balance. Candidate prompts inherit dated public-doc capabilities; remote UI was not accessed. No providers or Flow service were called. Public scholarly pages were read solely to ground the broad craft lens.

## Explicit conflicts and unresolved decisions

- [CONFLICT] New S05 cost line cannot fit the source 0.513333s tail by assumption; extension/read-through and total length TBD.
- [CONFLICT] Candidate Akvan wording needs a new recording/alignment; source D-S07-2 WAV is not relabelled. Source approval is performance only; human lip-sync approval remains pending.
- [CONFLICT] Prior proportional Flow cut times do not locate current speaking/framing accurately, particularly S04. Candidate cuts are TBD, not silently corrected in production.
- [UNKNOWN] New open-hand/released Chapar, king response, correction inscription hold and treaty coda exact frames/poses/rights need owner review. Missing pictures are blockers, not generated placeholders.
- [CONFLICT] SR05 is sourced in the manuscript hook but absent from current voiced ending; the animation messenger/Mirror role transition, coda art/voice/timing must be explicitly accepted. The missing promises remain unverified; “obvious” is the character’s claim.
- [PROPOSAL] Agent reconciliation retains the single existing visual authority; story/performance/pacing entries are candidate additions only. Stable-pose/audio restrictions remain until exact action/voice scope is approved. Source scene prerequisites are not repeated as actions in every short clip.
- [UNKNOWN] No table read, muted animatic observation, new phonetic/perceptual listening review or full candidate moving render was performed. Script rubrics and deterministic checks cannot supply those results.

[PROPOSAL] Promotion requires accepted change IDs/wordings, exact identity/art/action/rights references, authorised recording/performance, measured edit timings and final picture/lip-sync decisions. Follow HANDOFF_DIFF_AND_PROMOTION; prepare a NEW official revision locally only after evidence exists. No provider/upload/generation/spend/commit/push/deploy follows from writing acceptance.
