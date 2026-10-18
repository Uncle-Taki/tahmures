# Layout 01 v5 — Codex completion of GLM revision 2

Owner authorized Codex to continue after GLM reached its limit. GLM created
four analysis/helper files but no output sprites. Those files were retained
unchanged. Codex implemented the bounded completion in
`code/build_codex_completion.py`, using v4 exported layers and the immutable
v2 master/extraction as inputs. Earlier versions are read-only.

## Local repairs

- R2-01: remove detached old notch/lip ink from the moustache lower edge and
  make its receiver continuous beard material. Retain the upper source
  contour; construct a small supersampled smooth lower contour. Newly drawn
  colours and changed alpha are reconstructed artwork.
- R2-02: use an opaque foreground interior and a shared irregular upper
  patch overlap with a deliberately smooth hidden skin field. Remove old
  mottled ink/skin fragments. Keep the existing actual lip line and the
  59-pixel restrained open test; do not add facial states.
- R2-03: replace damaged local neck wedges with a continuous brown hair field
  following a curved vertical direction. Preserve source neck skin and all
  original alpha. No alternating scanline recolouring or torso extraction.

Detailed changed-pixel counts: `code/completion-metrics.json`. All source and
reconstruction ownership masks are recomputed for the actual files. Previous
reconstructed pixels stay classified as reconstructed; modified RGB/alpha
and new hidden coverage are never labeled original source pixels.

## Actual deliverables and reproduction

14 full-canvas RGBA components, matching L alpha masks, two ownership masks per
component, immutable head-domain mask, manifest, raw A/B/C states, 18 declared
stress renders and actual light/dark/checkerboard inspection plates. Model B,
1086×1448 canvas, original pivots/anchor and layer order remain. Eyes, brows,
nose, ears and diadem sprites are unchanged from v4. No whole-head source
underlay belongs to any puppet group.

From repository root:

```bash
rtk proxy /usr/bin/python3 Characters/tahmures/versions/layout01-v5/code/build_codex_completion.py
rtk proxy /usr/bin/python3 Characters/tahmures/versions/layout01-v5/code/finalize_validation.py
```

The builder only writes v5 outputs. The finalizer hashes all candidate files
except the index itself and invokes the unchanged read-only supervisor checker.
`validation-results.json` records the actual result; independent evidence is
in `workflow/layout01-mouthless-repair/reports/codex/completion-03/`.
Do not rerun builds inside a frozen submitted package without rehashing and
resubmitting that changed revision.

## Limits and approval

This is a front-view head with two mouth patches, not production speech art.
Only the declared patch ±2px and moustache ±1px axial micro-offset cases are
tested. No simultaneous offsets, rotation, perspective, body rig or viseme
library is claimed. The neutral patch resembles the source but is no longer
pixel-exact at the rebuilt interface. Manual local colour/contour work is
subject to independent visual review and human preference approval.

No provider, paid call, manuscript, source hash, review metadata, media
blueprint, glossary, registry, skills or implementation contract was changed.
No Godot, audio or video output was created. Claude has not reviewed these
files. `human_approved` remains false. Final production release is held.
