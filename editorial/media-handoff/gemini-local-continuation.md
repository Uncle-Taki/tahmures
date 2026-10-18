# Gemini recovery prompt — prepare every supplied character before scenes

> Historical handoff. Current workflow: existing private GitHub repository, branch **main**.
> Start with [AI Studio handoff](README.md) and [starting prompt](ai-studio-start-here.md).
> The Drive/ZIP transfer instructions below are retained for history.

Updated 2026-10-18. This replaces the earlier Tahmures-only/refactor-first
prompt. Paste the text below into Gemini with local repository access.

---

You are the implementation agent recovering my Tahmures Godot work. My previous
GLM run made scenes with incorrect placeholder characters. I have supplied the
actual character artwork in `Characters/`. **First prepare every supplied
character as a reusable layered Godot puppet, following the useful Tahmures
component workflow; only afterward repair and continue the chapter scenes.**

Do real preparation and verification, not only a segmentation plan or file
renaming exercise. Do not recreate the characters as silhouettes, primitive
figures, recoloured duplicates or approximate new drawings. The supplied images
define their working visual identity. Preserve the existing Tahmures rig rather
than starting its accepted head extraction again.

## 1. Read, inspect, and preserve

Repository: `/home/mehdi/Project/leela/tahmures`. Read `AGENTS.md`, its RTK
reference, relevant `.agents/skills/mehdi-context`, `mehdi-media`,
`mehdi-narrative` and `tahmures-narrative` instructions. Prefix shell commands
with `rtk`. Preserve the charter, manuscript, translations, continuity, glossary,
review metadata and approval records.

Read `editorial/media-handoff/2026-10-18-glm-character-review.md` and the
accompanying audit JSON. Inspect the actual artwork visually, then read the
actual new candidate at:

`Characters/tahmures/prototypes/godot-chapter-01-01/`

Inspect `assets/asset-map.json`, `scripts/make_standins.py`,
`scripts/tahmures_rig.gd`, `scripts/stage/scene_ch01_s*.gd`, the timeline/cues,
tests and renders. Do not assume their comments, “CLOSED” findings or output
filenames establish correctness. This candidate is not the character authority.

The previous completion prompt expressly allowed temporary named-character
stand-ins. **That permission is withdrawn for this recovery.** Keep that old
candidate as evidence; do not run its stand-in generator over new artwork.

Inspect the accepted Tahmures sources and controls in:

- `Characters/tahmures/versions/layout01-v2/source/approved_master.png`;
- `Characters/tahmures/versions/layout01-v7/`;
- `Characters/tahmures/prototypes/layout01-facial-states-01/`;
- `Characters/tahmures/prototypes/godot-front-view-character-poc-01/`;
- the separate JSON approvals under `Characters/tahmures/workflow/approvals/`.

Verify approval-bound hashes. Do not mutate frozen package sprites, manifests,
indexes or external approvals. An approval for the old head does not approve
new full-body art or every state in a refactored rig.

## 2. Exact source roster — prepare all of it

| Asset ID | Exact source | Story use |
|---|---|---|
| tahmures | Existing master and approved layered packages above | Reuse accepted head; complete source-faithful body preparation as needed. |
| akvan_div | `Characters/Akvan Div.png` | Keeper of Scripts; present in Chapter 01. |
| black_div | `Characters/Black Div.png` | Literal reading; present in Chapter 01. |
| div_e_sefid | `Characters/Div-e Sefid.png` | Prepare library rig; not inserted into the current eleven-scene Chapter 01 adaptation. |
| shahrasp | `Characters/Shahrasp.png` | Scribe/ledger role in the current adapted chapter. |
| chapar | `Characters/chapar.png` | Incoming courier, distinct from Simurgh. |
| arash | `Characters/arash.png` | Captain and illustrative Gatekeeper. |
| garshasp | `Characters/garshasp.png` | Prepare library rig; remains an offstage handwriting reference in Chapter 01. |
| simurgh_human | `Characters/simurgh - human.png` | Separate prepared variant of Simurgh. |
| simurgh_bird | `Characters/simurgh - bird.png` | Separate prepared variant of the same named character. |

Discover any additional images actually present and add them to the inventory
without guessing their identity. Both Simurgh files exist: prepare both as
separate variants. Do not blend them, silently select one, treat them as two
different story roles, or invent an on-screen transformation. Ask which form to
bind to chapter scenes only when needed; continue all independent preparation
and other characters meanwhile. A test-gallery selector is allowed and is not
a story transformation or final form decision.

These are owner-supplied working references selected by this task. Do not ask
whether to use them again. Preparation does not constitute blanket final-art or
publication approval. Current source artwork controls appearance over old
generic registry descriptions: do not remove Akvan/Black Div's supplied horns,
replace their illustrated faces with featureless clay, strip Arash's depicted
equipment, or change Shahrasp's costume to match an obsolete placeholder card.
Those visual details do not authorize new plot actions or mythic claims.

## 3. Phase A — real component packages and reusable rigs

Work in a new recovery workspace, proposed path:

`Characters/godot-character-library-recovery-01/`

If present, inspect and continue compatible work without overwriting unrelated
files. Keep source PNGs and the rejected GLM candidate unchanged. Use stable
character IDs inside this workspace; filenames containing spaces are valid
source paths and must be quoted safely. Do not create a new competing story
bible or silently promote this local asset index into the canonical registry.

For **every** supplied asset/variant:

1. Record source path, SHA-256, exact dimensions, colour mode and visual identity.
   The nine new references are RGB images with opaque light backgrounds; they
   are not transparent sprites or pre-separated sheets. The human Simurgh is
   1087×1447, while the other eight are 1086×1448. Read dimensions; do not force
   every source to the same size or copy Tahmures's coordinates onto new bodies.
2. Remove background into a derived RGBA working image while preserving the
   character's original face, expression, outlines, horns, hair, palette,
   clothing, equipment and proportions. Do not erase pale clothing/white hair
   together with the background. Check fine hair, feathers, gaps and fingertips.
3. Produce actual layered components suited to the source pose: head/face,
   hair/beard/horns/headwear where separable, eyes/brows/mouth where practical,
   neck/torso, upper/lower arms, hands, garments/legs/feet, and held props. Bird
   Simurgh needs bird-specific head/beak, wing, body, tail, leg/talon and scroll
   treatment, not a humanoid arm skeleton.
4. Record anatomical left/right and screen orientation, per-layer bounding
   boxes, common coordinate system or crop offsets, pivots, joint anchors,
   stacking/occlusion order and motion limits. Reassemble the source pose from
   the actual exported parts at its original resolution before animating.
5. Treat held objects as real occlusion problems. Akvan's tablets, Black Div's
   tablet/cloth, Shahrasp's book/reed, Garshasp's tablet and Simurgh's packet/
   scroll must not be painted into both a hand layer and a second prop. Separate
   only visible pixels honestly; document missing areas hidden behind props.
6. Preserve source-visible pixels where feasible. Any seam allowance, underlap,
   missing eye surface, covered body region or new pose that needs reconstruction
   must be explicitly labelled as reconstructed candidate work with masks and
   review images. Never call inferred pixels recovered source art. Use available
   permitted local tools; do not invoke paid/cloud image services or install
   dependencies without authorization. If quality reconstruction is not possible,
   keep a constrained source-pose rig and report the precise missing surface.
7. Build an editable reusable Godot character scene with named components and
   sensible pivots, attachment sockets and reset/state controls. A single opaque
   whole-image Sprite2D sliding across the screen is not the requested layered
   preparation. Keep a source-pose preview if parts cannot yet move safely, and
   label its capability honestly instead of faking a complete rig.
8. Provide neutral/reset plus supported idle, gaze/blink and small gesture tests
   appropriate to each character. Reuse Tahmures's approved states precisely;
   do not give other characters Tahmures's eyes/mouth as generic substitutes.
   New closed-eye surfaces are reconstructed candidates, not existing approved
   source. Unsupported expressions, turns or phonemes must remain unimplemented
   and identified; no face-stretching to imitate missing poses.

Avoid exact source-pose beauty composites hiding a broken puppet. All approval/
QA previews must be reproducible from the same exported layers used by Godot,
without an intact master image secretly backing holes. Inspect on light, dark
and checker backgrounds, with seams/alpha visible and after motion offsets.

Use the Tahmures workflow as a quality reference, not as a script to clone the
entire V2–V7 history or assume all anatomy/coordinates match. In the new GLM
`tahmures_rig.gd`, both brows move in thinking; the accepted POC raises only the
anatomical-left brow one pixel. Compare actual source behaviour and correct any
such divergence in the recovery candidate without rewriting the accepted input.

## 4. Phase B — mandatory character-readiness gate

Create a runnable gallery/test scene covering Tahmures and **all nine** supplied
images (both Simurgh variants). Show source vs assembled pose, layers/alpha,
neutral and supported motion, sockets and any restricted/reconstructed region.
Provide actual Godot screenshots, component sheets, short local previews,
source hashes, manifest and validation results for every asset.

Use explicit technical states per character: `prepared`, `needs_reconstruction`,
`needs_visual_review`, `ready_for_scene_integration`. Final human approval is a
separate recorded event; do not grant it yourself. Do not stamp every state
“ready” because import succeeded or a file exists. Continue fixing concrete
problems until the characters are prepared, and name genuinely unavailable
inputs accurately rather than masking them with wrong stand-ins.

**Do not rewrite chapter scenes, substitute cast graphics or start full chapter
exports until the complete supplied-character preparation pass and its visual
evidence are ready.** Obtain the owner's review of the actual character gallery
before treating new reconstructed art as selected. Preparation is already
authorized; this review concerns the actual results, not permission to start.
If an existing revision-specific approval covers a result, use it rather than
asking for the same approval again. Preserve work while waiting for a real
remaining decision; no automatic promotion when the owner has not replied.

At that boundary present one compact review set for all prepared characters,
including the Simurgh form choice if still unresolved. Continue independent
diagnostics/planning, but do not skip this prerequisite to produce another
chapter render with incorrect people.

## 5. Phase C — then recover Chapter 01 and continue remaining work

After the character-readiness gate and required visual choices:

- Audit and salvage useful timeline/caption/scene logic from the GLM candidate
  into a separate recovery project. Do not discard all code or trust its claims
  wholesale. Replace **every named-character** stand-in with the correct prepared
  reusable character scene by explicit ID/source hash. Never fall back silently
  to `assets/standins/` when a character resource is missing. Fail clearly.
- Keep the rejected candidate for comparison. Background anonymous collectives
  and prop/background placeholders are a separate declared scope; they cannot
  stand in for named characters. No new character art generated from scratch.
- Use the live Chapter 01 tales, current continuity, eleven-scene screenplay,
  supervisory findings and bounded correction brief. Keep Chapar and Simurgh
  distinct, Garshasp offstage, Div-e Sefid outside the eleven-scene adaptation,
  Simurgh delivery before Arash's dispatch, and S10's carrier an explicit media
  inference. Do not invent transformations, archery actions or malicious divs.
- Preserve the engineering lesson: one tablet receives record/message/current
  command readings; missing context owns the failure. Four labels help
  interpretation, not enforcement. Eight prompt components are conceptual peers.
  Keep modern explanation in the engineering overlay, not ancient dialogue.
- Audit the seven screenplay review findings; GLM's `CLOSED` labels are
  self-reports, not independent or human acceptance. Keep candidate-local
  corrections traceable and original manuscript/blueprints unchanged.
- Recheck the declared 173-second chapter plan, scene/cue reset/seek and exact
  EN/FA text. Existing probed renders were about 156.47 s EN and 18 s FA, so
  filenames do not prove full chapter delivery. Regenerate only after correct
  characters are integrated, and verify actual durations against the final
  timeline, actual frame coverage and both language captions.
- Implement missing narration only with owner-provided real recordings,
  confirmed transcripts/subtitles and the mouth-motion decision. Do not use
  rejected eSpeak or fabricate audio. Silent animatics must be called silent.
  A full chapter must use chapter-specific timing; the old 18-second POC audio
  limit cannot be copied unchanged. No phoneme lip-sync claim for a two-state
  mouth proxy.
- Complete technical/visual/language checks, prepare independent-review evidence
  when requested, obtain final owner art/voice decisions, and package one final
  deliverable without hidden dependencies on excluded intermediate versions.
  Only final versions will later be selected for Git.

## 6. Checks and deliverables

First deliver the full character library, gallery, source/component manifests,
reconstruction/occlusion ledger, source-to-rig comparison evidence, actual tests
and a concise per-character readiness table. Then deliver scene-replacement
mapping, repaired runnable chapter and actual bilingual render evidence after
the required gate. Do not return only a character-cutting plan.

Run appropriate local import/runtime/state/source-preservation checks. Inspect
real rendered character images: headless parsing and a count of scene scripts
cannot prove identity or visual quality. Test missing source/rig resources and
ensure they cannot trigger a stand-in fallback. Check alpha edges, overlaps,
joint seams, body proportions, props, feet/ground and camera framing.

Before implementation handoff, run `rtk proxy git diff --check` and the required
`rtk proxy make check PYTHON=.venv/bin/python`. The earlier baseline was 789
passing tests and eight stale Chapters 01–04 Persian-source-hash failures;
rerun and report actual results without repairing manuscript hashes to hide
unrelated failures. Preserve source art and frozen package hashes throughout.

Keep `.godot/` locally ignored; preserve `.import` and `.uid` metadata with
resources. No commits, pushes, publication, destructive cleanup, paid/provider
calls, dependency changes, manuscript edits or fabricated approvals. Keep local
recovery status in this workspace rather than changing old phase records to
declare success.

Begin by inspecting the supplied images and new GLM files, then execute the
character-preparation milestone. Do not jump directly to rendering scenes.
