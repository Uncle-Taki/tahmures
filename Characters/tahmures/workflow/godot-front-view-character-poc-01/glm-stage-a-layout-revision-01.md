# GLM bounded correction — GODOT_FRONT_VIEW_CHARACTER_POC_01 stage-A layout

MODE = IMPLEMENT_AND_VERIFY

CURRENT GATE = STAGE_A_HUD_AND_SAFE_LAYOUT_CORRECTION

GLM remains the primary implementer. GPT-Codex validates the resubmission.
Correct only the visual UI/layout blocker identified below. Preserve the
already passing Godot project, approved art, animation and render behavior.
Do not start audio integration.

## Inputs

Read:

- Characters/tahmures/workflow/godot-front-view-character-poc-01/ROADMAP.md
- Characters/tahmures/workflow/godot-front-view-character-poc-01/phase-brief.md
- Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/codex/verification-01.md
- Characters/tahmures/prototypes/godot-front-view-character-poc-01/README.md
- Characters/tahmures/prototypes/godot-front-view-character-poc-01/implementation-report.md
- Characters/tahmures/prototypes/godot-front-view-character-poc-01/validation.json
- Current project scene, controller, manifest, checker and render frames.

The approved source package remains hash-bound by the existing manifest and
approval record. Run the existing checker before editing and record its
baseline. Do not overwrite or alter the approved head inputs.

## Exact defect

The current 1280×720 preview has overlapping interface layers:

- Language/debug text at roughly y=92 crosses the head/diadem.
- Temporary torso and arm labels occupy roughly y=540–616.
- The dynamic state label spans about x=16–1000 at y=606–646, drawing across
  the body and colliding with those placeholder labels. The long THINKING and
  OPEN TEST strings are especially intrusive.
- Time, hint and progress controls then compete for the remaining lower strip.

See the six existing frames, especially
renders/frames/t6.5s-thinking.png and
renders/frames/t11.0s-point-open-mouth.png. The current overlap obscures both
the character and the prototype status labels.

## Minimum correction

Re-layout the screen so the following occupy clearly distinct, readable areas
at every inspected key state:

1. Approved character and temporary body/arm motion.
2. Persian name and short project header.
3. Temporary placeholder identification.
4. Current state indicator.
5. Time/progress controls.

Keep all necessary prototype/approval information visible, but shorten the
on-screen state text to compact labels such as IDLE, BLINK, THINKING, POINT,
OPEN TEST, and RETURN. Move long explanations to the README or console.
Keep the temporary torso/arm status unmistakable, but move compact callouts
outside the character silhouette and away from the dynamic HUD. The language
line must not cross the head or diadem. You may reposition the assembled rig
or camera to create a dedicated UI safe region, but do not rescale, rotate,
repaint, or otherwise change any approved facial sprite.

Choose the layout and record a small screen-region map in the report. Add a
machine-checkable assertion for any fixed UI rectangles that must not
intersect. Manually inspect the actual rendered keyframes; geometry checks
alone do not prove readability.

## Preserve passed work

Do not change:

- the 17 approved input images or their source hashes;
- the approved facial-state prototype, approval record, or v7 package;
- facial layer order, state art, or the 1 px thinking-brow shift;
- timeline duration (18 seconds), event ordering or beat times;
- the temporary-only status of torso, arms, hands, and target marker;
- language selection behavior;
- eSpeak decision (both voices remain rejected);
- manuscript, blueprint, registry, glossary, review metadata or shared tools;
- audio, subtitles, mouth-sync, or final bilingual exports.

Do not create narration, synthetic tones, silent files pretending to be speech,
new character art, or permanent registry assets. Keep the existing AVI’s
silence accurately described. Because the UI is baked into the silent render,
regenerate the AVI and keyframe evidence after the correction.

## Required outputs

Edit only inside:

Characters/tahmures/prototypes/godot-front-view-character-poc-01/

Update as needed:

- scenes/main.tscn and scripts/main.gd;
- the existing project-local integrity checker or a focused layout check;
- renders/stage-a-preview.avi and six keyframe PNGs;
- renders/verification.json;
- manifest.json, validation.json and implementation-report.md;
- README.md only if its owner-facing UI description changed.

Preserve the output tree and update hashes for every changed/generated file.
Do not add empty reports or claim visual inspection you did not perform.

## Validation

Run and record:

    godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --import

    godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --quit-after 2

    python3 Characters/tahmures/prototypes/godot-front-view-character-poc-01/scripts/check_integrity.py

Regenerate the same 18-second, 1280×720, 30 fps silent preview and the keyframes
at:

    t=1.0
    t=2.65
    t=6.5
    t=10.6
    t=11.0
    t=15.0

Use Movie Maker or the existing deterministic path. Verify the output with
ffprobe and verify the audio track remains documented as silence, not narration.
Inspect the actual frames at full view and the HUD/body intersections. Ensure
all required labels are legible, nothing crosses the head/diadem, state text
does not cover the torso, and temporary callouts do not collide with the HUD.
Re-run the integrity checker and `git diff --check`. Report tracked/untracked
scope accurately; do not attribute pre-existing untracked files to this pass.

## Return report

Update implementation-report.md with only the bounded layout revision summary,
screen-region map, files changed, frame inspection evidence, commands and
results. In validation.json report the original Stage-A gates as preserved and
add explicit HUD/layout checks with PASS/FAIL and frame evidence. State that
audio stage, narration quality, lip-sync and permanent body art remain pending.

Finish with exactly one token:

GODOT_FRONT_VIEW_CHARACTER_POC_01_LAYOUT_REVISION_READY_FOR_GPT
GODOT_FRONT_VIEW_CHARACTER_POC_01_LAYOUT_REVISION_REQUIRED
GODOT_FRONT_VIEW_CHARACTER_POC_01_OWNER_INPUT_REQUIRED
GODOT_FRONT_VIEW_CHARACTER_POC_01_TOOLING_BLOCKED

Do not commit, publish, modify approvals, or start Stage B.

