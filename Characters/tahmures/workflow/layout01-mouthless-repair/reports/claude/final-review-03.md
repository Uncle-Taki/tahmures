# Claude Layout 01 v7 independent neck-closure review

**Gate:** `CHARACTER_LAYOUT01_MOUTHLESS_REPAIR / CL-NECK-01`  
**Mode:** `VERIFY_FINAL_BLOCKER_CLOSURE`  
**Verdict:** `CL-NECK-01 CLOSED` — independent visual closure gate passes.

This is a fresh, read-only review session and did not implement the v6 neck repair. The v6 implementation attribution is explicitly retained as Claude in `reports/glm/implementation-claude-neck-01.md`; v7 package correction/verification attribution is Codex. This report is therefore an independent review of the actual v7 candidate, not a self-certification of the v6 implementation. It does not grant human visual approval, asset freezing, release approval, or a next phase.

## Package binding

| Item | Required / observed SHA-256 | Result |
| --- | --- | --- |
| Approved master: `Characters/tahmures/versions/layout01-v2/source/approved_master.png` | `3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5` | Match; bound source |
| v7 manifest: `Characters/tahmures/versions/layout01-v7/manifest.json` | `b7539646b960fc9313c907effabb1f5de84ca816678fc0a0d1224c5f46ee1cd4` | Match |
| v7 index: `Characters/tahmures/versions/layout01-v7/files-sha256.json` | `3b2ad23048da5ba009069f6c0ca86f78e6694927e151ac3e7b5e84393f4347bc` | Match |

The observed digests were computed directly from the bound files before adjudication. `reviewed-candidate-snapshot.json` records the same v7 manifest and index digests and the 146 indexed files.

## Image-access preflight and actual visual inventory

**Passed.** Direct image access was available. I visually opened the actual approved master and current v7 `D_source_comparison.png` before evaluating the closure. The master is the front-facing illustrated character with dark hair, gold diadem, facial hair, and blue/gold garment; the comparison plate visibly shows the source plus A mouthless, B neutral, and C open-test head assemblies. This review is based on rendered PNG inspection, not inferred from names, hashes, or counts.

The following actual v7 images were viewed:

- `versions/layout01-v2/source/approved_master.png`
- Raw assemblies: `versions/layout01-v7/previews/mouthless.png`, `neutral.png`, and `open_test.png`
- `previews/plates/D_source_comparison.png`
- `D_head_100_light.png`, `D_head_100_dark.png`, and `D_head_100_checker.png`
- `D_neck_zoom.png`, `D_neck_light.png`, `D_neck_dark.png`, and `D_neck_checker.png`
- `F_neck_v5_v7_neutral.png`, `F_neck_alpha_contour.png`, and `F_neck_hair_component_comparison.png`
- `E_components_0.png`, `E_masks_0.png`, and `E_provenance_0.png`
- Direct component/mask files: `head/hair_back.png` and `masks/visible_head_domain.png`

I also reviewed `neck-repair-record.json`, relevant v7 manifest repair/provenance fields, the prior Claude v5 visual report, the Claude-attributed v6 implementation report, and Codex `verification-04` review, locality/equality, independent-check, structural, candidate-snapshot, and rebuild/reproducibility evidence.

## CL-NECK-01 adjudication

**CLOSED.** The correction in `head/hair_back.png` resolves the prior concrete geometry failure in master region `x=463–606, y=326–375`, including the former left wedge around `x=467–486, y=327–363`.

1. **Exterior edges:** At source scale and in `D_neck_zoom.png`, both lower exterior hair edges now form rounded, continuous, tapered locks. The rejected square/stepped/dangling fragments visible in the v5 side of `F_neck_v5_v7_neutral.png` are absent from the v7 side. Light, dark, and checker backgrounds do not reveal a new conspicuous seam, clipped rectangle, or background-dependent edge artifact.
2. **Neck arc and identity:** In all raw A/B/C assemblies and neck plates, the skin neck arc remains clean and recognisably continuous. The repair sits behind that unchanged skin area; it does not introduce a body, garment/collar backing, rectangular concealment, or broader head redesign.
3. **Components, alpha, and provenance:** `E_components_0.png` and direct `head/hair_back.png` show the rounded locks as part of the actual current hair component. `E_masks_0.png` confirms alpha support for those locks; `E_provenance_0.png` marks their lower portions reconstructed. `neck-repair-record.json` documents the bounded `[458,320,614,384)` contours, 4,497 changed-alpha pixels, no removed-alpha pixels, and reconstructed contour-support RGB/alpha. The unchanged `visible_head_domain` was directly inspected and is also recorded byte-identical to v5 by the preservation evidence. This supports a truthful local reconstruction rather than concealed backing.

The aesthetic choice of a short rounded lower lock is not a remaining geometry defect: it is coherent at delivery scale and at zoom. No concrete blocker requiring a minimum correction was found.

## Focused evidence reconciliation

- Codex's `artwork-preservation.json` records that only `head/hair_back.png`, its alpha mask, and its two provenance masks changed from v5; all **57** exported sprite/alpha/provenance PNGs are byte-identical v6→v7.
- The same record reports each of the three raw assemblies and all 18 declared stress assemblies changed from v5 only within `[458,320,614,384)`, with zero changed pixels outside that box and zero above `y=320`; each v7 assembly is RGBA-identical to v6.
- `independent-checks.json` records exact saved-output assembly matches, zero newly transparent protected-interior pixels, and zero source-opaque alpha deficits for A/B/C and all 18 stress samples.
- `structural-check.json` reports structural-only `pass: true`, explicitly `artistic_approval: false`; it records the hair component as a manually traced reconstructed lower exterior lock and provenance partition/source-claim checks as passing.
- The supplied technical result is **185/185** structural checks passing. It is treated as supporting mechanical evidence only, not as the visual decision in this report.
- `rebuild.log` and `reproducibility.json` report a byte-identical v7 package rebuild with exit code 0 and no changed candidate files.

## Retained prior facial evidence

`final-review-02.md` accepted the face/mouth receiver, neutral/open lower-face patches, identity, and 18 declared movement samples, while blocking only the neck/hair exterior geometry. This closure does not reopen those accepted matters: verification-04 establishes that all face/mouth assets and masks remain byte-identical to v5, and the visual A/B/C comparison shows no contradictory regression. The v7 repair is confined to the stated lower-hair region.

## Criterion dispositions

| Criterion | Disposition | Basis |
| --- | --- | --- |
| L01-07 Cheek/neck connection | **PASS / prior blocker closed** | The current lower hair-to-neck presentation is intentional and coherent; the neck skin arc is preserved without backing or redesign. |
| L01-15 No duplicated features or edge artifacts — neck-edge portion | **PASS / prior blocker closed** | The former square/jagged/dangling exterior remnants are absent on light, dark, and checker evidence; no new conspicuous neck-edge seam is visible. |

## Limits and approval boundary

This decision certifies only the bounded front-view `CL-NECK-01` closure and carries forward the byte-preserved facial evidence. It does **not** certify arbitrary head rotation, perspective, body rigging, garment/body assets, Godot integration, combined transforms, a speech-viseme system, audio/video use, or broader animation capability. The lower-hair reconstruction is truthfully reconstructed artwork, not claimed as pixel-identical recovered master art. Human visual approval remains pending.

CLAUDE_LAYOUT01_ACCEPTED
