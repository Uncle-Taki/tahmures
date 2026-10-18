# Claude independent near-final review — Layout 01 facial-state prototype

**Phase:** `LAYOUT01_FACIAL_STATE_PROTOTYPE_01`  
**Mode:** `VERIFY_AND_ACCEPT`  
**Verdict:** **ACCEPTED** — no concrete prototype-gate blocker found.

## Independence and package binding

This was a fresh, read-only review session. I did not implement or repair this prototype; Codex is identified as its executor in `implementation-report.md`. I made no changes to the candidate, source v7, source master, scripts, manifests, approval data, or validation gates. The only project output of this review is this report.

| Bound item | Expected SHA-256 | Observed SHA-256 | Result |
| --- | --- | --- | --- |
| Candidate `manifest.json` | `b081e9190f5ddf1e8eff643863b1bbee5ab7b4a176179a26703b1c4ad32e4ba4` | `b081e9190f5ddf1e8eff643863b1bbee5ab7b4a176179a26703b1c4ad32e4ba4` | Match |
| Candidate `files-sha256.json` | `6135d7b65239919ebb2834913aa20b93d391d16d40f2a35c4a499e337b1cea21` | `6135d7b65239919ebb2834913aa20b93d391d16d40f2a35c4a499e337b1cea21` | Match |
| Source v7 `manifest.json` | `b7539646b960fc9313c907effabb1f5de84ca816678fc0a0d1224c5f46ee1cd4` | `b7539646b960fc9313c907effabb1f5de84ca816678fc0a0d1224c5f46ee1cd4` | Match |
| Source v7 `files-sha256.json` | `3b2ad23048da5ba009069f6c0ca86f78e6694927e151ac3e7b5e84393f4347bc` | `3b2ad23048da5ba009069f6c0ca86f78e6694927e151ac3e7b5e84393f4347bc` | Match |
| Approved master `source/approved_master.png` | `3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5` | `3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5` | Match |

`reviewed-candidate-snapshot.json` records the same candidate manifest/index digests and 128 indexed artifacts. The candidate directory has 129 regular files because that indexed set excludes its index file itself. `reproducibility.json` records a byte-identical rebuild with no changed candidate files and the same candidate-index digest.

The v7 approval binds v7 as a human-approved **input** only. The candidate manifest correctly remains `PROTOTYPE_CANDIDATE` with `human_approved: false`; this review does not change that state.

## Image-access preflight and visual material actually viewed

**Passed.** PNGs were directly viewable; this is a visual review, not an inference from hashes or check counts.

I visually opened:

- Required preflight plates: `previews/state-contact-sheet.png` and `previews/eye-brow-zoom.png`.
- Raw full-canvas assemblies: `states/neutral.png`, `states/blink_closed.png`, `states/thinking.png`, `states/open_test.png`, and `states/mouthless.png`.
- Component/QA plates: `previews/eye-components.png` and `previews/thinking_underlay_qa_only.png` (treated as QA evidence only, not a delivered state).
- Actual new artwork: `assets/eye_left_closed.png`, `assets/eye_right_closed.png`, and `assets/thinking_brow_underlay.png`.
- Their actual alpha masks: `masks/eye_left_closed.png`, `masks/eye_right_closed.png`, and `masks/thinking_brow_underlay.png`.
- Reconstructed provenance masks: `provenance/eye_left_closed__reconstructed.png` and `provenance/thinking_brow_underlay__reconstructed.png`, plus the source-provenance counterpart for the left closed-eye surface.
- Source-v7 comparison layers: `face/eye_left.png`, `face/eye_right.png`, and `face/eyebrow_left.png`.
- Animation containers: `previews/facial-states.gif` and `previews/facial-states.webp`.
- Actual timeline frames: `frames/frame-018.png`, `frame-019.png`, `frame-030.png`, `frame-040.png`, `frame-062.png`, `frame-080.png`, and `frame-095.png`.

The image viewer exposed only the first frame of the GIF and WebP, so I did **not** claim to have watched either animation. I instead inspected the exported PNG frames at the named samples; their persistent labels, fixed composition, state selection, and progress-cursor position substantiate the declared timeline samples.

## Findings

### Blink — PASS

`blink_closed` reads naturally at source scale and in `eye-brow-zoom.png`: both original eye surfaces have been replaced with coherent local skin fields and a single, clean closed-lid arc. I found no residual white sclera, pupils, circular eye outlines, hard rectangular cover edge, visible seam, or identity-changing alteration. The local reconstructed patches are an appropriate solution for replacement of full eye features; they are not rejected for failing to resemble thin mouth-like lids.

The reviewed component plate and actual assets show the replacement is localized to the two eye footprints. The alpha masks and reconstructed provenance masks align with those same local regions. The eyelid arc is visually clean without an evident mismatch at its skin boundary.

### Thinking brow pose — PASS

The anatomical-left brow rises by the declared one pixel in `states/thinking.png` and the close-up plate. It remains visually coherent and intentionally subtle at delivery scale. The QA-only underlay and the final thinking state show no visible old baked brow, double outline, or exposed vacancy. This passes as the bounded motion test; it is not read as a claim of finished expressive acting.

### Approved-v7 pose preservation — PASS

The neutral, small-open, and mouthless state assemblies retain the approved front-view silhouette, pivots, composition, and layer presentation. The lower-face/mouth work shows no visible regression. This conclusion carries forward the earlier approved v7 closure rather than reopening it: the current validation evidence reports these three as exact approved poses, and direct state inspection provides no contradictory visual evidence.

### Provenance, locality, and source preservation — PASS

The manifest names exactly three new prototype surfaces: two closed-eye reconstructions and one local brow receiver. Their alpha bboxes are bounded to the affected eye/brow interfaces; the declared provenance calls the new pixels reconstructed rather than recovered source pixels. This is consistent with the viewed assets, masks, and provenance views.

`validation.json` records the 146 frozen v7 files and approved master hash as unchanged; it reports exact alpha-mask checks, no residual eye-white pixels, complete original-eye footprint receivers, no dark brow residue in the vacated strip, zero coverage gaps/deficits for every raw state, and changes confined to the eye or brow interfaces. It also records that protected book/code/metadata are unchanged. I treat these results as supporting mechanical evidence, not a substitute for the visual decisions above.

### Preview/timing — PASS within prototype scope

The directly viewed animation files’ first frames identify the result as a front-view, prototype-only, silent preview. PNG timeline inspection confirms:

- `frame-018` and `frame-019`: closed-eyelid blink;
- `frame-030` and `frame-040`: one-pixel brow-raise test;
- `frame-062`: existing small-open-mouth test;
- `frame-080`: mouthless receiver;
- `frame-095`: return to approved v7 neutral.

The visual labels are honest about the states and silence. The frame samples retain a readable fixed composition, and the two-frame closed blink is brief. `validation.json` reports 96 decoded frames and 8,000 ms for both GIF and WebP, shared-palette RGB agreement for GIF, exact lossless RGB agreement for WebP, and no mismatched frames. The independent read-only invocation of `code/validate.py --report /tmp/tahmures-facial-state-independent-validation.json` passed **51/51**, with zero failures.

## Blockers

**None.** No concrete geometry, ghosting, identity, scope, source-preservation, provenance, or transition-sample defect was found. Accordingly, no minimum correction is requested.

## Limits and approval boundary

This acceptance is limited to the submitted front-view prototype: the closed-eye blink, the one-pixel anatomical-left brow test, and reuse of the existing neutral/small-open/mouthless states. It does not approve the new eyelid or brow-receiver artwork for human use, alter `PROTOTYPE_CANDIDATE` status, or authorize canonical promotion.

It does not certify combined expressions, arbitrary head rotation or perspective, body/arm/pointing art, Godot integration, a runtime rig, speech visemes, lip synchronization, TTS/audio, MP4/final video, publication, or any further phase. Human visual approval of the new pose artwork remains separately pending.

CLAUDE_FACIAL_STATE_PROTOTYPE_01_ACCEPTED
