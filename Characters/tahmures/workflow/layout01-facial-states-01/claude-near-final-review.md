# Claude — near-final facial-state prototype review

MODE = VERIFY_AND_ACCEPT

PHASE = LAYOUT01_FACIAL_STATE_PROTOTYPE_01

Codex owns architecture, implementation and corrections. You provide one
independent **read-only near-final check**. Use a fresh session; do not implement
repairs or certify your own implementation. No provider generation, spending,
new scope, approval metadata, commit or publication. Write only the report.

## Exact scope and input authority

Read the live media/review/narrative/editorial skills as needed and:

- `Characters/tahmures/workflow/layout01-facial-states-01/phase-brief.md`;
- `Characters/tahmures/workflow/approvals/layout01-v7-human-approval.json`;
- source v7 manifest/index and source-phase `final-review-03.md` as needed;
- `Characters/tahmures/prototypes/layout01-facial-states-01/README.md`,
  `implementation-report.md`, `manifest.json`, `validation.json`, code and
  actual artifacts;
- this phase's `reviewed-candidate-snapshot.json`, `reproducibility.json` and
  `make-check.log`.

Source v7 is explicitly human-approved **input**, not automatic approval of
the new eyelid/brow artwork. It remains unchanged. This is a front-view local
prototype: blink, one-pixel thinking/brow pose and existing mouth-state switch.
It is not the later Godot/body/pointing/TTS/lip-sync/final-video phase. Do not
reopen the approved neck or original mouth work without a proven regression.

Candidate: `Characters/tahmures/prototypes/layout01-facial-states-01/`.
Manifest SHA-256:
`b081e9190f5ddf1e8eff643863b1bbee5ab7b4a176179a26703b1c4ad32e4ba4`.
Index SHA-256:
`6135d7b65239919ebb2834913aa20b93d391d16d40f2a35c4a499e337b1cea21`.
128 indexed files. Check binding against the snapshot before adjudication.

## Image and playback preflight

Actually open `previews/state-contact-sheet.png` and
`previews/eye-brow-zoom.png`. If PNG viewing is unavailable, stop with
`IMAGE_ACCESS_PREFLIGHT_BLOCKED`; do not produce a visual verdict from counts.

Inspect raw `states/{neutral,blink_closed,thinking,open_test,mouthless}.png`,
`previews/eye-components.png`, `previews/thinking_underlay_qa_only.png`, new
assets/masks/provenance and source eye/brow sprites. The underlay is QA only.

Preview: `previews/facial-states.gif` and `facial-states.webp`, 8 seconds,
96 frames, silent. If your tool shows only the first animation frame, say so
and inspect actual PNG frames/timeline instead; do not claim to have watched
the animation. Example frames: 000 neutral, 018/019 closed blink, 030/040
thinking, 062 small-open test, 080 mouthless and 095 neutral. Review additional
frames around transitions if useful. Decoder/timing evidence is in validation.

## Questions to resolve independently

1. Are the closed eyelids source-faithful and natural at intended scale,
   without old pupils/white eyeballs/circular outlines, rectangular covers,
   harsh skin seams or changed identity? Full eye surfaces are replaced by
   local reconstructed patches; do not expect only a mouth-like thin lid PNG.
2. Does the one-pixel upward shift of the anatomical-left brow remain visually
   coherent, exposing no baked old brow/double outline? It is intentionally a
   subtle motion test, not final expressive acting or a larger head movement.
3. Are neutral, small-open and mouthless states the exact approved v7 poses,
   with source silhouettes/pivots/layer order preserved? No speech-viseme claim.
4. Are the local changes/provenance honest, exact masks valid, source v7 and
   approved master unchanged, and no unapproved body/capability work implied?
5. Do the actual frame/animation outputs support the declared state cycle,
   readable fixed composition, brief blink and honest silent-preview label?
   Cosmetic polish alone is not a production blocker at this prototype gate.

Do not accept art only because 51 tests pass. Distinguish concrete ghosting,
identity or geometry defects from human taste. Do not require intermediate
blink phases, speech, MP4 or Godot: those are outside this released scope.

## Focused checks

You may run the validator with its report redirected outside the package:

```bash
rtk proxy /usr/bin/python3 Characters/tahmures/prototypes/layout01-facial-states-01/code/validate.py \
  --report /tmp/tahmures-facial-state-independent-validation.json
```

With `--report`, no candidate file is written. Never execute `render.py` in the
submitted package during review. Additional inspection outputs belong in `/tmp`
or the assigned report folder. Full book checks are not required again for this
near-final read-only check unless concrete new evidence warrants them.

Validation independently recomposes all raw states, checks pose coverage,
change locality and old-eye/brow residue, and decodes all GIF/WebP frames.
GIF is checked against its saved shared palette; WebP is exact RGB. Prior
Codex verification is evidence, not your visual authority.

## Output

Write only:
`Characters/tahmures/workflow/layout01-facial-states-01/reports/claude/final-review-01.md`.
Include package binding, independence/image-access confirmation, actually
viewed files/playback method, blink and thinking decisions, source preservation,
provenance/timing assessment, limits, concrete blockers and verdict. For each
blocker give file/frame/coordinates and minimum correction. Do not repair it;
Codex will do so. Human approval of new pose art remains separate.

Finish with exactly one after an actual review:

`CLAUDE_FACIAL_STATE_PROTOTYPE_01_ACCEPTED`

`CLAUDE_FACIAL_STATE_PROTOTYPE_01_REVISION_REQUIRED`

`CLAUDE_FACIAL_STATE_PROTOTYPE_01_OWNER_DECISION_REQUIRED`
