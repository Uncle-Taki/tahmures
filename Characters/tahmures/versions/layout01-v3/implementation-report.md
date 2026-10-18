# Layout 01 v3 — Implementation Report (GLM implementation-01)

Candidate: `Characters/tahmures/versions/layout01-v3/`
Task: `CHARACTER_LAYOUT01_MOUTHLESS_REPAIR` (Model B local lower-face patch).
Status: **CANDIDATE — structural gate only.** No Codex visual acceptance, no
Claude independent review, and no human artistic approval is claimed by this
report.

## 1. Inputs and checksums

| Input | Value |
| --- | --- |
| Package | `Characters/tahmures/tahmures_sprites_layout01_v2.zip` |
| Package SHA-256 | `8dbe2832fe4b7728a954ae8c94ac4ca5ec5864584d7dfbbd8efd19be8e72e1f0` (unchanged) |
| Approved master | `Characters/tahmures/versions/layout01-v2/source/approved_master.png` |
| Master SHA-256 | `3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5` (unchanged), 1086×1448 RGBA |
| Baseline | extracted v2 at `versions/layout01-v2/` (unchanged) |
| Governance | workflow README/phase-status, mouth-architecture, submission-contract, acceptance-criteria, source-checksums, Codex initial-diagnosis, media-continuity-bible |

Baseline `git status`: tracked files clean; only pre-existing untracked
`Characters/` and `li*3`. The candidate directory did not previously exist.

## 2. Selected architecture (Model B)

`B_LOCAL_LOWER_FACE_PATCH` with a **static mouthless beard receiver**, a
**swappable lower-face patch** (skin + adjacent beard + mouth), and a **static
moustache foreground** above the patch:

```
hair_back < head_base < ear_right < ear_left < beard < [patch] < nose
< eye_right < eye_left < eyebrow_right < eyebrow_left < moustache < diadem_gold
```

- `beard` = v2 beard + 304 recovered pixels + the receiver: inside the
  mouth-content region **M** the master mouth (smile line, lips, interior,
  corner strokes) is replaced by beard texture tiled from a verified all-dark
  master block (y270–293, x494–604; asserted all-dark at build time).
- `lower_face_neutral` = pure master pixels on the common footprint **P**.
- `lower_face_open_test` = neutral + a restrained 80 px synthesized opening.
- `head_base` = master pixels following the true skin/neck silhouette inside
  the immutable head domain (fixes v2's rectangular cheek cuts and neck gaps),
  plus hidden feature underdraw (see §4). No body artwork extracted.
- `moustache` and all other features are reused verbatim from v2.

Only `lower_face_neutral` and `lower_face_open_test` exist; no mouth library
was started. `neutral_mouth` / `neutral_face_without_mouth` are not rig
components, and no v2 preview underlay or master copy is used as a component.

## 3. Exact repairs and coordinates (full-canvas coordinates)

| Region | Pixels | bbox (x0..x1, y0..y1) | Meaning |
| --- | --- | --- | --- |
| M (mouth content) | 2616 | 500..580, 228..269 | master mouth content replaced by receiver clone |
| P (patch footprint) | 3217 | 497..584, 226..273 | common stable footprint of both patches; irregular contour = dilate(M,3) clipped y≥226, traced from actual contours — not a rectangle |
| Opening (open test) | 80 | 531..553, 253..258 | synthesized small opening: interior 45% master line + 55% master interior sample; bottom edge 75% line + 25% below-line sample |
| Clone block | — | y270–293, x494–604 | verified all-dark beard texture source for the receiver |

Seam repairs (Codex initial-diagnosis items), all inside the immutable
head-domain coverage target (domain never shrunk):

1. **Diadem/forehead seam**: 410 previously-uncovered pixels assigned to
   `diadem_gold` (gold elements, outlines, shadows in the y≤130 band);
   crown pixels above y≤40 assigned to `hair_back`.
2. **Irregular vertical cheek cuts** (v2 rectangular `head_base`): rebuilt as
   the true master silhouette — removes the x465–467/y226–248 skin intrusion
   and restores the missing cheek skin x618–626.
3. **Jagged neck/hair joins**: right-side hair strands (x655–690, y170–374)
   and lower hair mass added to `hair_back` (+816 px); neck-side and chin-tip
   pixels assigned by palette (298 px to `head_base`, 304 px to `beard`).
   1828 uncovered domain pixels total, classified by nearest reference palette
   (skin 247,176,112 / gold 200,135,55 / dark 45,32,27 / black 6,4,4) with
   zone rules; assignment is local and editable in `code/`.

The patch seam sits inside skin/beard tones (P contour), away from the outer
jaw; the receiver stays continuous beneath patch and moustache. The patch does
not extend over eyes, nose, forehead or neck (P bbox y226–273 vs eyes y135–187,
nose ends y221).

## 4. Retained vs reconstructed artwork

| Sprite | visible px | source px | reconstructed px | Reconstruction |
| --- | --- | --- | --- | --- |
| head_base | 29106 | 23184 | 5922 | Laplacian-diffusion inpaint of eye/eyebrow/nose solid interiors (alpha≥252) from surrounding master skin — hidden feature underdraw so features can move later; soft feature edges keep master RGB |
| hair_back | 31514 | 31514 | 0 | +816 recovered master pixels (source) |
| diadem_gold | 7241 | 7241 | 0 | +410 recovered master pixels (source) |
| ear_left / ear_right | 1170 / 1344 | all | 0 | verbatim v2 |
| eye_left / eye_right | 2067 / 2098 | all | 0 | verbatim v2 |
| eyebrow_left / eyebrow_right | 710 / 727 | all | 0 | verbatim v2 |
| nose | 320 | 320 | 0 | verbatim v2 |
| beard | 10830 | 8214 | 2616 | receiver clone inside M |
| moustache | 1820 | 1820 | 0 | verbatim v2 |
| lower_face_neutral | 3217 | 3217 | 0 | pure master pixels |
| lower_face_open_test | 3217 | 3137 | 80 | synthesized opening |

Source claims are exact master RGB; alpha equals master alpha everywhere
(extraction never increases it). Reconstructed pixels are labelled
reconstructed in `provenance/` even where sampled from the master palette —
no fake original-pixel attribution.

## 5. Groups and overlap strategy

Three groups (see `manifest.json`): `puppet_core` (no patch, state A),
`puppet_core_neutral` (+`lower_face_neutral`, state B),
`puppet_core_open_test` (+`lower_face_open_test`, state C). The arrays are
authoritative; no contradictory z-index sorting exists.

Overlap is deliberate and hidden-coverage-preserving: the patch overlaps the
beard receiver; the moustache overlaps the patch top; features overlap the
inpainted head_base underdraw; hair/diadem extensions close the former gaps.
The outer silhouette boundary is single-owner, so the master's antialiased
edge alpha is preserved exactly (no forced opacity). Eye pivots remain
left (579,160), right (505,160); brows left (579,116), right (501,116); all
other pivots/parents follow v2 (patches: pivot (540,241) = mouth anchor,
parent `beard`).

## 6. Machine test outcomes (actual runs)

- **Coverage (one-pixel eroded immutable domain)**: states A/B/C each have
  0 new fully transparent interior pixels and 0 alpha-below-250 deficits.
- **Fidelity vs master (both opaque, per-pixel max channel diff >3)**:
  - B (neutral): **0 px** (max diff 2) — pixel-faithful;
  - A (mouthless): 2045 px, **all inside M** (intended mouthless design);
  - C (open test): 80 px, exactly the synthesized opening.
- **B vs C**: 80 differing px, 0 outside footprint P — only the intended
  patch changes; nose/eyes/brows/diadem alignment is trivially preserved
  because B is pixel-exact and C differs only inside the opening.
- **Micro-motion stress (18 samples, `stress-tests.json` + `previews/stress/`)**:
  each patch at (0,0),(+2,0),(-2,0),(0,+2),(0,-2); moustache at (+1,0),(-1,0),
  (0,+1),(0,-1) over both patch states. All 18: coverage 0/0; composition
  changes confined to the moved sprite's original∪shifted footprint; revealed
  receiver inside M always dark cloned beard (no master mouth leakage);
  (0,0) samples byte-identical to the unadorned previews. This is a limited
  front-view envelope — no perspective/turn/viseme claims.
- **Supervisor structural checker** (`validate_submission.py`, read-only,
  unmodified): **pass, 185/185 checks, exit 0** — see `validation-results.json`
  for commands and full stdout.
- **Independent verification script** (`code/verify_70_checks.py`): group
  recomposition byte-identical to previews A/B/C, mask==alpha equality,
  provenance partition/source claims, pivots/bboxes, ZIP/master/v2 unchanged —
  results in `code/_verify_report.json`.

Tooling note (honest discrepancy): the checker command in the task uses
`rtk proxy python3`, which resolves to the book `.venv` interpreter that has
no Pillow; the literal command fails with `ModuleNotFoundError: No module
named 'PIL'`. The checker was therefore executed with the system interpreter
(`rtk proxy /usr/bin/python3`, Pillow 10.2.0 + numpy 1.26.4). Both runs are
recorded in `validation-results.json`. No dependency or project-runtime
change was made.

## 7. Visual inspection — method and coverage

This agent cannot view images; all "visual" inspection below was performed
programmatically (pixel statistics, palette checks, difference maps, contour
renderings at crops). Readable plates for human/Codex viewing are in
`previews/plates/` (D: source comparison at 100%/2x/3x on checkerboard, light,
dark; change maps; E: components, exact alpha masks, provenance, receiver
interface, layer order, stress contact sheet).

Programmatically verified: state A's mouth region is uniform dark beard
receiver — no lip line, no smile remnant, no skin-coloured hole (2045 changed
px are all dark clone); the receiver texture mean (44.1, 31.7, 27.8) matches
the neighbouring beard below the mouth (43.8, 31.5, 27.7), though its
variance is slightly higher (std 7.6 vs 0.8 — the clone block carries subtle
master noise); no rectangle is used (M/P are irregular traced contours, shown
in `E_receiver_interface_zoom.png`); the moustache is byte-identical to v2
(position/weight unchanged); B reproduces the master mouth exactly; C's
opening uses only master-sampled line/interior colours with matching line
weight; no duplicated lips/moustache exist (single patch per group, features
verbatim); edge quality is preserved because every sprite keeps exact master
alpha (no binarization, no blur). These checks are not artistic approval.

## 8. Remaining defects and limits

1. Structural gate only; artistic naturalness still requires Codex visual
   review and human approval (plates provided for exactly this).
2. Front-view micro-offset envelope only; no perspective turn, rotation, or
   arbitrary articulation is claimed or tested.
3. `lower_face_open_test` is a technical test state, not a viseme library.
4. Receiver clone (2616 px) and opening (80 px) are reconstructions, not
   master pixels; head_base underdraw (5922 px) is hidden until features move.
5. The 1828 recovered gap pixels were assigned by palette/zone heuristics —
   plausible but heuristic; locally editable in `code/build_10_sprites.py`.
6. Clone-texture variance is slightly higher than the adjacent beard (see
   §7) — flagged for Codex visual attention at zoom.
7. Checker interpreter discrepancy (§6) — reported to Codex as a tooling
   contract defect; no fix was applied to the checker or the environment.

## 9. Files produced (candidate root)

- `manifest.json`, `files-sha256.json`, `validation-results.json`,
  `stress-tests.json`, `implementation-report.md` (this file).
- `head/` (3), `face/` (9), `mouths/` (2) — full-canvas 1086×1448 RGBA.
- `masks/` (15 = 14 exact-alpha L-mode + immutable `visible_head_domain.png`).
- `provenance/` (28 binary ownership masks).
- `previews/` (3 unadorned A/B/C), `previews/stress/` (18 samples),
  `previews/plates/` (20 labelled inspection plates).
- `code/` (editable analysis/build/verification sources + region masks
  `_M.npy`, `_P.npy`, `_opening.npy`, `_beard_region.npy`, `_head_region.npy`
  and build metadata).

## 10. Recommended Codex review targets

1. `previews/plates/D_mouth_zoom_*.png` — receiver naturalness in A; seam
   tone compatibility; open-state restraint in C.
2. `previews/plates/E_receiver_interface_zoom.png` — irregular seam geometry
   vs outer jaw identity.
3. `previews/plates/E_provenance_zoom.png` + `D_source_comparison_*_zoom.png`
   — diadem band, right hair strands, neck-side/chin gap assignments.
4. `previews/plates/E_stress_contact_sheet.png` — micro-offset coherence.
5. Clone-texture variance note (§8.6) at 3x zoom.
6. Checker interpreter discrepancy (§6) — needs a Codex tooling decision.
