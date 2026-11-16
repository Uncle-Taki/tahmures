# AI Studio complete bundle — acceptance review, 2026-10-20

**Decision: retain as a specification draft; do not accept its extraction,
motion or certification claims.** The useful content is a ten-character roster,
an eleven-scene outline and bilingual cue candidates. It is not the missing
Akvan task implementation or a runnable chapter package.

Received input: `tahmures_complete_studio_bundle.json` at the repository root.
It is preserved byte-for-byte. Local comparison details and its SHA-256 are in
[`studio-bundle-review.json`](studio-bundle-review.json). Reproduce with:

```bash
rtk proxy /usr/bin/python3 editorial/media-handoff/review_studio_bundle.py
```

The script successfully producing a report does not mean the reviewed bundle
passes acceptance. It never imports the export into the working rigs.

## Findings

| Severity | Evidence | Required response |
|---|---|---|
| Blocker | `health_and_compliance_audit` calls all ten characters “100% Extraction Complete & Certified”, with all motion/contour/prop flags true. The delivery contains no new contour masks, asset bytes, code changes, before/after plates or execution logs. | Request the actual Akvan-only task artifacts. Keep qualification pending; do not copy these booleans into approval state. |
| Blocker | 288 unique texture paths are referenced. Four are missing, all for Tahmures `eyes_and_brows` (layer, mask and two provenance files). | Do not manufacture that combined asset from a name. Reuse the accepted 17-component head controller with its actual state/visibility/draw-order contract. |
| High | Across 71 existing layer PNGs, 56 claimed alpha bounds and 67 claimed opaque-pixel counts differ from local files. Example: head-package box claims `[389,15,687,687]`, while the local partition is `[389,15,687,310]`; the local neck partition is empty. | Recompute metadata from actual returned PNGs. A local path pointing at an unchanged candidate is not evidence of a new extraction. |
| High | The supplied Garshasp, human Simurgh and bird Simurgh source hashes do not match the actual source files. | Use actual protected-input hashes from the repository baseline; do not overwrite sources to match an invented digest. |
| High | Human Simurgh is exported as `1086×1448`, but its actual source is `1087×1447`. The export's root canvas/origin also uses the generic dimensions. | Preserve its native canvas and derive its transform, bounds and pivots from those actual pixels. |
| High | Every rig is assigned neutral/idle/thinking/blink/alert/talking and broad rotations (including ±45°), without joint-gap or reconstructed-surface evidence. | The working candidates remain neutral/whole-pose only. The accepted head's scoped blink/thinking tests do not certify new bodies or other characters. |
| Blocker | `OST-S07-4` says **“Requested Result: Count (Sealed)”**, with `seal_icon: true`. Tahmures actually wants the object classified and missing information identified. | Correct the result label; the counting was Black Div's mistaken action. A separate physical request card is useful, but its seal is not authentication or authority. |
| High | The head registry reverses the viewer-side descriptions of left/right ears and changes the accepted receiver-underlay order (after the nose rather than immediately after the head base) if its `zIndex` is used directly. It describes `open_test` as phoneme articulation. | Follow the accepted Godot head order/anatomical naming. Open-test remains an optional simple mouth test, not a viseme or lip-sync approval. |
| High | `godot_4_3_contracts` declares scene/director files absent from the maintained recovery project. The local tested toolchain is Godot 4.7.2; this JSON does not establish compatibility with 4.3, Unity, Spine or PixiJS. | Return actual Godot scene/scripts and run the required import/runtime/render checks. Do not migrate toolchains based on an export label. |
| High | The file labels the project “Proprietary / Educational”, contrary to its repository licences. | Keep content CC BY 4.0 and code Apache-2.0 under the existing licence files; record actual new-art provenance separately. |
| Medium | Scene outline, cue counts and time ranges are internally consistent: 11 scenes, 34 cues, 18 OSTs, 173 seconds. No waveform or read-through proves those durations. | Retain as a proposed budget. Several dialogue cues are dense; test actual EN/FA readings and caption dwell before fixing the performance length. |
| High | No scene-background artwork, set layout manifest, independent props/extras, final font/audio delivery or full render evidence is present in this input. | Supply the missing production bundles below; do not equate an animatic data table with a completed film. |

All ten original source PNGs match the prior repository baseline, but only
seven of the ten source hashes **claimed in this export** match those files.
The 620 protected non-target character outputs also match the prior baseline.
That supports preservation of the local sources; it does not support the
export's new all-ten certification claims.

## Door removal and corrected planning source

The opening's thirty-door/unlike-handle detail was atmosphere: it did not cause
the failure, explain a decision or resolve the story. Its intended visual
variety was already conveyed by the message materials. Removing it makes the
opening more focused without losing the engineering lesson.

The owner's request is applied to the current English and Persian Chapter 1
opening and recorded in `book/narrative-continuity.md`. The hall is introduced
through incoming clay/leather/bark/silk messages and Shahrasp's crystal reading.
The ordinary western gate in Scene 8 stays: that gate has an explicit role in
the contextual-command example and is a different object.

[`chapter-01-production-plan.json`](chapter-01-production-plan.json) is the
**corrected planning candidate** for future media work. It replaces the opening
cue and OST, removes the decorative motif from Scene 1, fixes the requested
result label, and marks all scenes as unrendered candidates. Scene 11's lamplit
ledger is explicitly a recap insert, not a new night after the dawn return.
Its timing remains provisional. The rest of its adapted dialogue still needs
source, Persian and performance review; this is not a blanket script approval.

The raw received export, rejected GLM scripts/captions/renders and old transfer
snapshots remain historical evidence and can still contain the removed motif.
They must not be reused as current story instructions. Do not patch frozen or
rejected history to hide the difference, and do not load the raw Studio JSON as
the current runtime manifest.

The existing Persian `source_sha256` and review records are not refreshed by
this narrow deletion: Chapters 01–04 already require current-revision editorial
signoff/reconciliation. This edit does not certify the remainder of those drafts.

## Missing bundles and next order

The corrected plan enumerates **nine production bundles**, with explicit
deliverables and separate exit gates:

1. **Character qualification:** the actual Akvan masks/code/assets and review,
   followed by the other source characters. Keep coupled hands/props honest.
2. **Environments:** eight reusable sets with named views and lighting variants,
   beginning with one coherent Hall of Scripts. No background art is claimed
   complete by this review.
3. **Props:** the shared found tablet, damaged seal trace, oilcloth, separate
   request card, four labels, catalogue, reed/ledger, corrective message and
   vignette exhibits. Character-held equipment alone does not cover story props.
4. **Extras/effects:** riders/horses, watch, villagers, apprentice/court workers,
   charcoal burners, rain, wet clothing, fire/smoke and river effects.
5. **Storyboard/camera:** shot blocking, ground lines, insert views and transitions
   for all eleven scenes and their subshots; continuity of the tablet's custody.
6. **Text/graphics:** reviewed bilingual cues, safe caption layout, a licensed
   Persian-capable font, eight equal-weight components and series mark.
7. **Audio:** owner recordings, exact transcripts/VTT, ambience/effects provenance,
   bus/language routing and an explicit mouth-performance decision.
8. **Godot implementation:** real chapter scenes/director, loaders, deterministic
   seek/reset, failures on missing named assets and actual runtime tests.
9. **Release evidence:** hashes, licences, owner art/audio review, complete EN/FA
   renders/probes and separate whole-book release gates.

**Next two bounded tasks:** return the missing Akvan implementation under task 01;
in parallel, use [`ai-studio-task-02-environments.md`](ai-studio-task-02-environments.md)
for one Hall of Scripts design candidate. Neither needs the other's final art
to begin planning. Then review both before attempting a 12-second Scene 1
integration test. Do not build the entire film around these unqualified rigs.

See [`chapter-01-environment-brief.md`](chapter-01-environment-brief.md) for the
scene-to-set table, visual direction and background delivery contract. The JSON
plan contains the exact machine-readable scene/prop/extra dependencies.

## Validation of this change

- Bundle audit executed against local source/texture bytes; raw input unchanged.
- All 306 distinct protected inputs and 620 non-target outputs match the prior
  baseline. The new report does not change that baseline or the working rigs.
- Corrected plan checked for unique scene/cue IDs, contiguous 173-second scene
  budget, cue/OST ranges, all eleven scene-to-environment mappings and valid
  view/lighting references. This validates planning consistency, not playback.
- English/Persian executable fences and front matter are byte-preserved; the
  scoped prose change and continuity update pass `make validate`.
- Both strict MkDocs builds pass. Review-script lint/format and diff checks pass.
- `make check`: 789 tests pass, eight fail from the existing stale Persian
  source-hash conditions. It stops at Python tests; subsequent full-gate stages
  are not claimed as run. Translation validation also stops on the stale hash.
- Editorial status, citation parity, protected-content parity and Persian
  regression checks pass. Six existing morphology warnings concern `Agentها`
  in Chapters 13–18 descriptions, outside this change. The aggregate editorial
  command fails its translation subcommand on the stale Chapter 1 hash.

No source hash, historical approval or human-review status was silently refreshed.
No new art or Godot scene was generated by this review, and no commit/push was made.
