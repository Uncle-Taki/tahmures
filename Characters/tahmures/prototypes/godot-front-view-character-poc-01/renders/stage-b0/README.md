# Stage B0 caption-render status

The dedicated caption-test scene mode is available with `--caption-test` and
`--language=fa|en`. It uses WebVTT test fixtures explicitly marked as not
owner-approved narration. The initial Codex workspace had no usable X11 or
Wayland, and Godot `--headless --write-movie` failed on its dummy renderer.
Claude later rendered and visually inspected a real Godot sample using its
available display backend. The one-second AVI and extracted PNG are retained
outside this project at:

    Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/claude/evidence/

The Stage-A AVI and its six frames remain unchanged. These fixture visuals do
not approve subtitle wording, final caption layout, or narration.

On a desktop with Godot 4.7.2 and an available display, run from the repository
root:

    godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --write-movie Characters/tahmures/prototypes/godot-front-view-character-poc-01/renders/stage-b0/fa-caption-test.avi --fixed-fps 30 --quit-after 30 -- --language=fa --caption-test

Inspect the produced frame visually before treating Persian shaping, direction,
punctuation, or subtitle fit as verified. The existing Stage-A AVI and frames
must remain unchanged.
