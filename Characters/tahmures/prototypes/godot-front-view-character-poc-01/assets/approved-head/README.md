# Approved head components (copied inputs)

The PNGs in this directory are byte-exact copies of the human-approved
front-view facial-state prototype components. They are **inputs**, not
new art: do not edit, retouch, rescale, or re-export them.

## Origin and approval

- Pinned package: `Characters/tahmures/prototypes/layout01-facial-states-01`
  - `manifest.json` SHA-256
    `b081e9190f5ddf1e8eff643863b1bbee5ab7b4a176179a26703b1c4ad32e4ba4`
  - `files-sha256.json` SHA-256
    `6135d7b65239919ebb2834913aa20b93d391d16d40f2a35c4a499e337b1cea21`
  - Human approval:
    `Characters/tahmures/workflow/approvals/layout01-facial-states-01-human-approval.json`
- 14 layer sprites originate from the frozen, human-approved
  `layout01-v7` package (`Characters/tahmures/versions/layout01-v7`),
  referenced by the facial-state prototype's own manifest.
- 3 reconstructed components (`eye_left_closed.png`,
  `eye_right_closed.png`, `thinking_brow_underlay.png`) originate from
  the reviewed facial-state prototype itself.

Every file's origin path and SHA-256 is recorded in the project
`manifest.json`. `scripts/check_integrity.py` re-verifies all of them
against the pinned source packages.

## Approval boundary

The approval covers the reviewed front-view facial-state prototype for
continued prototype use. It does **not** approve:

- a permanent body, torso, arm, hand, or pointing pose;
- new expressions, combined transforms, or head rotation;
- a speech-viseme set or any lip-sync claim;
- promotion of this art as the permanent canonical character design.

The temporarily scheduled open-mouth sprite (`lower_face_open_test.png`)
is the approved small-open test state. Showing it in the timeline is a
state exercise, **not** speech and not lip-sync.

## Rendering rules used by the scene

- All sprites are full-canvas 1086 x 1448 images; the scene places them
  unrotated and unscaled at one shared position, so canvas coordinates
  equal world coordinates (pixel-exact alignment, `texture_filter =
  nearest` on the `Head` node).
- Neutral draw order (bottom to top): `hair_back`, `head_base`,
  `ear_right`, `ear_left`, `beard`, `lower_face_neutral`, `nose`,
  `eye_right`, `eye_left`, `eyebrow_right`, `eyebrow_left`, `moustache`,
  `diadem_gold`.
- Blink replaces `eye_right`/`eye_left` with the closed variants at the
  same z slots. Thinking inserts `thinking_brow_underlay` directly above
  `head_base` and shifts `eyebrow_left` up by exactly 1 source pixel.
  The open state swaps `lower_face_neutral` for `lower_face_open_test`.

The `.png.import` files beside the sprites are Godot-generated import
metadata (stable once committed) and contain no artwork.
