# GLM output inspection and character-first recovery

Date: 2026-10-18. This is an inspection snapshot and handoff correction, not
approval of the chapter candidate or prepared character artwork.

## Result

The new chapter candidate uses generated abstract named-character stand-ins,
not the nine supplied illustrated character references in `Characters/`.
Source inspection of the stage scripts confirms this; the viewed Akvan stand-in
is a circle/trapezoid figure, unlike the supplied illustrated Akvan. The existing
rendered `frame-t3.png` similarly shows a geometric Shahrasp at the hall edge.

The earlier GLM completion prompt explicitly permitted temporary silhouettes
for unavailable named-character art. That allowance made this outcome possible
and is withdrawn by the owner's current instruction. The recovery starts with
the supplied character references, prepares them as layered reusable rigs and
visually checks the set before continuing chapter assembly.

## What was appended since the earlier inventory

Compared with `editorial/git-hygiene/2026-10-18-file-decisions.csv`, there are
**149 additional non-cache files under `Characters/`**:

- **Nine owner-supplied reference PNGs** at `Characters/` root.
- **140 files** in `Characters/tahmures/prototypes/godot-chapter-01-01/`.

The [audit JSON](2026-10-18-glm-character-audit.json) lists every additional file
with path, size and SHA-256, reference dimensions/modes, scene-to-stand-in uses
and actual movie metadata. The comparison excludes `.godot/` and bytecode. It
identifies additions against the earlier inventory, not exact creation times.
Git does not establish authorship for untracked files; attribution of the
candidate to GLM follows the owner's report and its task/implementation files.
The nine new source PNGs are not classified as GLM-generated scene assets.

| New candidate group | Contents |
|---|---|
| `project.godot`, `scenes/main.tscn` | Chapter project and script-driven entry scene. |
| `scripts/stage/scene_ch01_s01.gd` through `scene_ch01_s11.gd` | Eleven staged scene scripts; named cast use `res://assets/standins/` textures. |
| `scripts/timeline.gd`, `main.gd`, caption/OST/stage scripts | Potentially reusable sequencing, controls and overlay scaffolding; not independently accepted. |
| `scripts/tahmures_rig.gd` | Copied-head assembly and temporary arm component; behaviour must be compared with the accepted POC. |
| `scripts/make_standins.py`, `assets/standins/` | Source of the rejected named-character silhouettes and temporary props. Do not regenerate these over supplied character artwork. |
| `assets/approved-head/`, `assets/temporary-body/` | Copies of old Tahmures prototype input/placeholder assets; not preparation of the new cast. |
| `assets/asset-map.json` | Describes the silhouettes using old generic card anchors; does not map the named cast to the supplied illustrated PNGs. |
| `data/chapter-cues.json`, `captions-en.vtt`, `captions-fa.vtt` | Candidate chapter/caption data; needs source, timing and parity review before salvage. |
| `planning/review-findings.md`, `baseline-protected.sha256` | Local self-reported closure and preservation data, not independent review. |
| `scripts/tests/` | Timeline and placeholder tests. These do not establish correct character identity. |
| `renders/ch01-en.avi`, `ch01-fa.avi`, `frames/frame-t3.png` | Actual outputs exist, but the movies do not cover the same declared chapter duration. |

No candidate-root `README.md`, `implementation-report.md`, or `validation.json`
was present on inspection. An empty malformed directory beginning `{assets`
also exists; it is noted, not removed. These are observations of the received
snapshot, not a claim about whether another agent may still be working.

## Supplied visual sources inspected

All nine files were opened and visually inspected. They share an illustrated
character family and have opaque light backgrounds. They are RGB originals,
not ready-to-use transparent components. Preserve them as source inputs.

| Source, relative to repository | Identity/appearance observed | Preparation and story scope |
|---|---|---|
| `Characters/Akvan Div.png` | Teal skin, dark braided hair, horns with gold bands, decorated dark/orange robe, held tablets. | Prepare full reusable actor; Keeper in Chapter 01. Do not replace with a generic human catalogue-keeper silhouette. |
| `Characters/Black Div.png` | Broad friendly face, dark skin/hair/beard, horns, layered brown clothes, tablet held in cloth. | Prepare full reusable actor; preserve identity, hands/cloth/tablet occlusions and non-malicious performance. |
| `Characters/Div-e Sefid.png` | Pale long-haired horned figure in white/grey robes, mirror and document. | Prepare library rig; outside the eleven-scene Chapter 01 adaptation. |
| `Characters/Shahrasp.png` | Dark hair/beard, olive headband/robe, reed and book. | Prepare scribe/ledger actor; keep source identity over generic old card costume. |
| `Characters/chapar.png` | Brown hood/cape, travel equipment, document tube and satchel. | Prepare incoming courier, distinct from Simurgh. |
| `Characters/arash.png` | Grey headband/scarf, brown armour/bracers, keys, bow/quiver. | Prepare captain/Gatekeeper actor. Equipment in the image does not authorize new archery actions in the story. |
| `Characters/garshasp.png` | Older grey-streaked hair/beard, blue robe, dark cloak and held tablet. | Prepare library rig; stays offstage as a handwriting reference in Chapter 01. |
| `Characters/simurgh - human.png` | Teal-clothed human messenger with packet and satchel. | Prepare separately; chapter-form choice remains to be resolved. |
| `Characters/simurgh - bird.png` | Teal/gold bird with beak, wings, tail, talons and carried scroll. | Prepare separate bird-specific rig; no invented transformation or second story role. |

Human Simurgh measures 1087×1447; the other eight references measure 1086×1448.
Do not copy Tahmures's pivots/crop coordinates to every character or erase pale
costumes, hair or feather edges during background removal. Their new use is
authorized by the owner's current direction; final reconstructed rig outputs
still need review. No chapter manuscript or mythic claims should be changed
merely because art has horns or equipment absent from an old generic card.

## Concrete recovery findings

1. **Wrong visual-source selection.** S02 loads `standins/chapar.png`; S03/S04
   load stand-in Akvan, Simurgh and Black Div; S01/S07/S11 load stand-in
   Shahrasp; S06/S08 load stand-in Arash; S10 loads stand-in Simurgh. Those
   references must eventually become explicit prepared-character scene bindings.
   A missing asset must not trigger an automatic silhouette fallback.
2. **No full cast preparation.** The supplied nine images are not layered
   packages in this candidate. Replacing texture paths with the opaque original
   posters would still not supply transparent, articulated puppets.
3. **Tahmures state divergence, from code.** In `scripts/tahmures_rig.gd`,
   `set_state()` moves both left and right brows by the thinking offset. The
   accepted POC specifies only the anatomical-left brow moving one source
   pixel. Recheck actual source-pose/motion equivalence before reusing this rig.
4. **Outputs are not matching full-chapter evidence.** FFprobe reports about
   **156.466667 seconds** for EN and **18 seconds** for FA, both MJPEG 1280×720
   at 30 fps with PCM audio streams. The chapter plan declares 173 seconds.
   Neither output duration matches that complete plan; diagnose whether these
   are partial runs, export errors or other configuration before claiming
   completion. An audio stream alone is not proof of recorded narration.
5. **Self-reports are not visual acceptance.** The finding record says closures
   are implemented, but naming eleven scripts and testing timeline data cannot
   prove correct characters, full duration, actual readability or art quality.

The inspection did not execute or repair the new chapter code, fully review
both movies, run a new full repository gate or grant any art/voice approval.
Movie metadata, source files, supplied artwork and one existing candidate frame
were inspected. Frozen/source/candidate files were not changed.

## Revised order of work

1. Inventory and preserve all supplied visual sources, old accepted Tahmures
   packages and the rejected GLM candidate.
2. Prepare Tahmures plus every supplied source/variant: alpha extraction,
   source-faithful layers, occlusion/reconstruction accounting, pivots, reusable
   Godot scenes and actual motion/edge/source-pose checks.
3. Present one complete character review gallery and readiness ledger. Resolve
   Simurgh's chapter form without blocking preparation of either variant.
4. After the character prerequisite, salvage verified chapter scaffolding into
   a recovery candidate, replace every named-character stand-in, preserve the
   chapter's correct roles and causal beats, and verify bilingual scene timing.
5. Integrate actual owner voice inputs when available, complete visual/audio/
   language and independent review as applicable, then select one final package
   for Git. Intermediate packages and `.godot/` remain local; no commit is
   authorized by this handoff.

Both [local Gemini](gemini-local-continuation.md) and
[web/app Gemini](gemini-web-continuation.md) prompts now implement this order.
The web prompt explicitly requires the actual artwork as attachments and
distinguishes a proposed cut map from an executed component package.
