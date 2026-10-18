# Layout 01 v4 — Implementation Report (GLM revision 1)

Candidate: `Characters/tahmures/versions/layout01-v4/`
Task: `CHARACTER_LAYOUT01_MOUTHLESS_REPAIR` — bounded revision 1 of v3
(Codex verification-01 blockers R1-01..R1-04). Model B local lower-face patch
retained; the two mouth states remain `lower_face_neutral` and one
`lower_face_open_test` small-open technical test.
Status: **CANDIDATE — structural and programmatic gates only.** No Codex
visual acceptance, no Claude independent review, and no human artistic
approval is claimed by this report. Every v3 file/hash is unchanged.

## 1. Inputs and checksums

| Input | Value |
| --- | --- |
| Package | `Characters/tahmures/tahmures_sprites_layout01_v2.zip` |
| Package SHA-256 | `8dbe2832fe4b7728a954ae8c94ac4ca5ec5864584d7dfbbd8efd19be8e72e1f0` (unchanged) |
| Approved master | `Characters/tahmures/versions/layout01-v2/source/approved_master.png` |
| Master SHA-256 | `3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5` (unchanged), 1086×1448 RGBA |
| Baselines | v2 extracted tree and v3 candidate tree — both unchanged (re-hashed in `code/_verify_report.json`) |
| Codex inputs | `workflow/layout01-mouthless-repair/reports/codex/verification-01/` (review.md, structural-check.json, independent-checks.json, moustache-ownership.json, captures) — read-only |

## 2. Architecture (unchanged Model B)

`B_LOCAL_LOWER_FACE_PATCH`: static mouthless beard receiver, swappable
lower-face patch (skin + adjacent beard + mouth), static moustache foreground
above the patch:

```
hair_back < head_base < ear_right < ear_left < beard < [patch] < nose
< eye_right < eye_left < eyebrow_right < eyebrow_left < moustache < diadem_gold
```

Layer order, pivots, parents, canvas, mouth anchor (540,241), footprints
M (2616 px) and P (3217 px) are identical to v3 (asserted against v3's
`_M.npy`/`_P.npy` at build time). No new sprites, states, or groups.

## 3. R1 dispositions — exact repairs and coordinates

### R1-01 — mouthless warm crescent below the moustache centre

- **Defect (v3)**: warm/ink crescent at bbox [530,230,542,237) in state A;
  root cause: the v2 moustache matte is binary (alpha 253/254) and its
  soft-edge RGB blends (warm skin-family colours, e.g. (198,140,96) at
  (540,231)) rendered almost opaque over the dark beard clone.
- **Repair**: matte decontamination in `face/moustache.png` — for every U
  pixel above a faithful reconstructed underlay, (alpha, RGB) is re-solved so
  the pixel composites to the exact master colour over the neutral underlay
  and goes dark over the mouthless clone: 353 px solved (reconstructed
  provenance), 2 pure-underlay px dropped, 29 px kept verbatim (no exact
  solution, all top edge y214–218 over skin), 1436 px kept source. The
  receiver was NOT extended and no rectangle was pasted.
- **Verified**: state A warm px (r≥140, r−b≥55) in the crescent bbox = **0**
  (v3: 8); over the wider clone zone (M ∪ beard U underdraw) = **0**. The
  125 warm px remaining over U elsewhere all sit on the moustache top edge
  over skin fills and match the master's own soft edge there (e.g. master
  (559,209)=(247,183,120)) — natural, not residue.

### R1-02 — baked moustache outlines beneath the movable feature

- **Defect (v3)**: head_base carried 1233 dark px matching the source
  moustache inside [486,209,597,238); beard carried 346 inside
  [498,224,585,239); a doubled edge appeared in ±1px stress samples.
- **Repair**: the full v2 moustache footprint U (1820 px, bbox
  [485,209,597,239)) is underdrawn in every layer beneath the feature:
  `head_base` 1394 px diffused skin, `beard` 345 px cloned texture (outside
  M), both patches 336 px art diffusion from surrounding master mouth art.
  Diffusion boundaries are real art (surrounding master pixels; invisible
  dark non-region px in the seed boxes are included in the region so ink
  does not leak). The decontaminated moustache above guarantees identity at
  rest.
- **Verified**: for all four moustache offsets (±1,0),(0,±1) over both patch
  states, the vacated strip renders **byte-exactly** as the moustache-free
  underlay (0 mismatched px) — no doubled edge, halo, or lip residue.
  head_base dark px in Codex's bbox dropped 1234 → 87 (86 diffused skin
  fills near dark beard/strand boundaries + 1 master stray at (556,209)
  kept as source art); none form the old outline (see R1_02 plate and
  stress contact sheet).

### R1-03 — coherent small mouth opening

- **Defect (v3)**: the opening was a dark addition at the central beard/chin
  notch (x531–553, y253–258) while the actual lip curve below the moustache
  stayed closed — two disconnected marks.
- **Repair**: one restrained lens-shaped opening at the actual lip parting
  line: per column x531–553 the darkest master row in y237..243 (the
  master's y240 line) is parted — 59 px, bbox [531,239,554,242); centre row
  = 55% master line colour + 45% mouth-interior dark; adjacent rows = 65%
  gap + 35% underlying master pixel; 3 rows for x536–548, 2 rows for the
  wings; pixels inside U or outside P are skipped. The chin-notch mark is
  gone (that area is plain receiver/patch content).
- **Verified**: B vs C differ at exactly 59 px, all inside the opening, 0
  outside footprint P; exactly one coherent mouth feature exists in C; jaw
  silhouette, moustache identity, palette and anchor unchanged.

### R1-04 — lower-neck garment contamination

- **Defect (v3)**: head_base carried 419 garment-colour px near
  x467–606, y326–374 (routed there by v3's uncovered-pixel rule);
  `hair_back` carried 8.
- **Repair**: strict garment classifier with the mandatory b≤70 guard
  (garment gold r≥150 & r−b≥140; blend fringe r≥120 & r−b≥90; pale collar
  trim r≥200 & 30≤r−b≤110 & g≥185; all y≥300): 277 px in head_base replaced
  by strand-continuation diffusion seeded from the head's own kept colours
  plus hair_back where the head is transparent; 6 px cleaned in hair_back.
  Neck-shading skin (r−b up to 147 but b≥73) is preserved. No torso was
  extracted, the hair mass was not redrawn, and the immutable domain was
  not shrunk.
- **Verified**: head_base garment px 419 → **0**; hair_back 8 → **0**;
  B vs master differs at 283 px, all inside the neck repair zone (intended);
  coverage A/B/C remains 0 holes / 0 deficits in the eroded domain.

## 4. Retained vs reconstructed artwork

| Sprite | visible px | source px | reconstructed px | Reconstruction |
| --- | --- | --- | --- | --- |
| head_base | 29106 | 21513 | 7593 | feature underdraw 5922 (v3 recipe) + U skin underdraw 1394 (R1-02) + neck cleanup 277 (R1-04) |
| hair_back | 31514 | 31508 | 6 | garment-gold strand continuation (R1-04) |
| diadem_gold | 7241 | 7241 | 0 | verbatim (+410 recovered, source) |
| ear_left / ear_right | 1170 / 1344 | all | 0 | verbatim v2 |
| eye_left / eye_right | 2067 / 2098 | all | 0 | verbatim v2 |
| eyebrow_left / eyebrow_right | 710 / 727 | all | 0 | verbatim v2 |
| nose | 320 | 320 | 0 | verbatim v2 |
| beard | 10830 | 7869 | 2961 | receiver clone inside M 2616 + U clone underdraw 345 (R1-02) |
| moustache | 1818 | 1465 | 353 | (alpha,RGB) re-solve decontamination (R1-01/R1-02); 2 px dropped |
| lower_face_neutral | 3217 | 2881 | 336 | U underdraw art diffusion (R1-02) |
| lower_face_open_test | 3217 | 2822 | 395 | U underdraw 336 + opening 59 (R1-03) |

Source claims are exact master RGB with alpha ≤ master alpha. Reconstructed
pixels are labelled reconstructed in `provenance/` even where colours are
sampled from the master palette — no fake original-pixel attribution.

## 5. Groups and overlap strategy

Three groups as in v3 (`puppet_core`, `puppet_core_neutral`,
`puppet_core_open_test`); patch at layer index 5, moustache static above.
Deliberate hidden overlap: patch over beard receiver; moustache over patch
top and skin; U underdraw duplicated across head_base/beard/patch so any of
them can be revealed by ±1px moustache offsets; features over the inpainted
head_base underdraw. Outer silhouette boundary remains single-owner with
exact master alpha. Eye pivots (579,160)/(505,160) and brow pivots
(579,116)/(501,116) are byte-equal to the v2 baseline manifest values.

## 6. Machine test outcomes (actual runs)

- **Coverage (one-pixel eroded immutable domain)**: A/B/C each 0 holes /
  0 deficits; all 18 stress samples 0/0.
- **Fidelity vs master (both opaque, diff >3)**: B 283 px (all intended neck
  repair), A 2371 px (mouthless design + U underdraw, 0 escaping), C 342 px
  (neck repair + opening, 0 escaping).
- **B vs C**: 59 px, all inside the opening; 0 outside P.
- **R1-01**: state A warm px in crescent bbox 0; over clone zone 0.
- **R1-02**: vacated-strip identity 0 mismatches for all 4 offsets over both
  states; (0,0) samples byte-identical to previews; changes confined to
  moved footprint in all 18 samples; revealed receiver always dark clone.
- **Supervisor checker**: see `validation-results.json` (fixed-point
  verified; both the literal and the system-interpreter runs recorded).
- **Independent checks**: `code/_verify_report.json` (recomposition
  byte-equality, mask==alpha, provenance partition, source claims,
  v2/v3/ZIP/master hashes unchanged, Codex-metric before/after recounts).

## 7. Visual inspection — method and coverage

This agent cannot view rendered images. All visual properties were verified
programmatically (classifiers, masks, byte-equality, diff maps, contour
renderings). Readable plates for Codex/human viewing: `previews/plates/`
— D source comparison (3 backgrounds × 100%/2x, mouth 3x), D change maps,
E components/alpha masks/provenance/receiver interface (incl. U contour)/
layer order/stress contact sheet, and R1_01..R1_04 before/after evidence
plates (8x crescent, 8x moustache-shift ghost with QA underlay render,
8x lip-line opening, 6x neck on three backgrounds). These checks are not
artistic approval.

## 8. Remaining defects and limits

1. Structural/programmatic gates only; visual naturalness requires Codex
   review and human approval.
2. Front-view micro-offset envelope only; no perspective/turn/viseme claims.
3. 29 moustache px kept verbatim (top edge y214–218, no exact ink-blend
   solution); 2 fringe px at (528–529,236) left as underlay art; 1 master
   stray at (556,209) kept — all documented, all invisible or harmless at
   rest.
4. 87 dark px remain in head_base inside Codex's R1-02 bbox — diffused skin
   fills adjacent to dark beard boundaries, not an outline.
5. Garment-family gold hidden under the diadem (62 px hair_back y89–124,
   34 px head_base y95–99) predates this revision, is invisible in every
   composition, and is out of scope.
6. 1828 recovered gap pixels remain palette/zone heuristics (v3 recipe,
   unchanged).
7. Checker interpreter discrepancy (literal `rtk proxy python3` fails: book
   .venv has no Pillow) — recorded honestly, no environment change made.

## 9. Files produced (candidate root)

- `manifest.json`, `files-sha256.json`, `validation-results.json`,
  `stress-tests.json`, `implementation-report.md` (this file).
- `head/` (3), `face/` (9), `mouths/` (2) — full-canvas 1086×1448 RGBA.
- `masks/` (15 = 14 exact-alpha L-mode + immutable `visible_head_domain.png`).
- `provenance/` (28 binary ownership masks).
- `previews/` (3 unadorned A/B/C), `previews/stress/` (18 samples),
  `previews/plates/` (27 labelled plates incl. R1 evidence).
- `code/` (editable build/analysis/verification sources, region masks
  `_M/_P/_U/_opening/_ink_head/_ink_beard/_patch_ink/_neck_clean/...` npy,
  `_u_neutral.npy` QA underlay render, build metadata).

## 10. Recommended Codex review targets

1. `R1_01_mouthless_crescent.png` — crescent gone in A; moustache form kept.
2. `R1_02_moustache_ghost.png` + `E_stress_contact_sheet.png` — no doubled
   edge under ±1px moustache shifts; QA underlay surface.
3. `R1_03_opening.png` + `D_mouth_zoom_*.png` — single coherent opening at
   the lip line; restraint in C.
4. `R1_04_neck*.png` — no gold shards, smooth neck/hair attachment on all
   three backgrounds.
5. `E_receiver_interface_zoom.png` — U contour vs P/M geometry.
6. §8 residual-pixel notes (fallback 29, fringe 2, stray 1, dark 87).
