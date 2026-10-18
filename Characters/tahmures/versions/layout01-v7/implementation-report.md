# Layout 01 v7 — current neck review package

Codex prepared this package from the immutable v6 result. **Every exported
sprite, alpha mask and provenance mask is byte-identical to v6.** Claude
implemented the v6 neck contour; that fact is retained. This package is not a
claim that Claude independently accepted its own implementation.

## Corrections made by Codex

- Replace the inherited v5 implementation report with accurate v7 attribution,
  input/output paths, reproduction instructions and approval boundary.
- Regenerate current D/E component, mask, provenance and inspection sheets
  from actual v7 exports. V6 had copied some unchanged-looking v5 sheets even
  though hair_back and its ownership masks had changed.
- Keep historical construction scripts under `code/history/`, explicitly
  separate from the current build entry point. The inherited v5 builder must
  not be run as a v7 build: it would revert the neck artwork.
- Regenerate actual A/B/C states and all 18 stress renders, refresh manifest,
  validation and hash index. No face, mouth or neck artwork is changed here.

## Actual input and reproduction

Artwork input: `Characters/tahmures/versions/layout01-v6/`, pinned manifest
`ac574324a3c3f8f5037c70c49188a6608f771fe6a6138061cbedf85ba7c9a8ce`,
index `52ba68c21e9bc13f656cc63e50c99471032a5bc20459356310c065ef1121b430`.
Source master remains the approved v2 master; original source/domain unchanged.

From repository root:

```bash
rtk proxy /usr/bin/python3 Characters/tahmures/versions/layout01-v7/code/rebuild_package.py
rtk proxy /usr/bin/python3 Characters/tahmures/versions/layout01-v7/code/finalize_validation.py
```

The QA builder reads pinned v6; it never modifies it. Its output is a package
of actual assemblies and accurate metadata, not regenerated character art.
Codex verification evidence is under
`workflow/layout01-mouthless-repair/reports/codex/verification-04/`.
`neck-repair-record.json` describes the actual Claude v6 contour construction
from v5; it remains valid as artwork provenance. No original-pixel provenance
is claimed for the reconstructed lower hair locks.

## Limits and release

Same front-view head and two restrained mouth states. Only independent patch
±2px axial and moustache ±1px axial offsets; no combined transforms,
rotation/perspective, body/Godot/speech/video or expression library.
Codex checks this actual implementation. Claude is used only for a fresh,
near-final independent neck closure, not another repair implementation. A
session that made the v6 art cannot self-certify its independent review.
Human visual approval remains separate; all assets remain CANDIDATE/unapproved.
No publishing, provider generation, spending or commits in this package task.
