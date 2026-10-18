# Temporary body stand-ins — TEMPORARY PROTOTYPE PLACEHOLDER — NOT APPROVED CHARACTER ART

Everything in this directory is a **temporary stand-in** created for the
stage-A pointing beat because no approved Tahmures body, arm, or hand
artwork exists. None of these files contain or derive extracted source
pixels from any approved artwork.

- `torso.png` — flat robe + hidden neck stub (280 x 340, pivot top-centre)
- `upper_arm.png` — flat sleeve capsule (40 x 95, pivot top-centre)
- `forearm.png` — flat sleeve capsule with cuff band (34 x 85, pivot top-centre)
- `hand_point.png` — flat pointing mitten (36 x 66, pivot at the wrist (18, 8))
- `point_target.png` — flat gold ring mark, a scene prop, not character art
  (48 x 48, pivot centre)
- `placeholders.json` — sizes, pivots, and SHA-256 of the above

All shapes are drawn by deterministic math (capsules, ellipses, one
polygon) in `scripts/generate_temporary_body.py` — no random numbers, no
image inputs, no AI or local image generation. Re-running the generator
reproduces byte-identical files:

    python3 scripts/generate_temporary_body.py

The skin tone used for the hand (248, 179, 116) was sampled from the
approved `head_base.png` cheek region so the placeholder does not clash
with the approved palette; sampling a colour is not extracting character
art. The robe/sleeve colours are new flat design constants.

These stand-ins are visibly labelled in the scene
("TORSO — TEMPORARY PROTOTYPE PLACEHOLDER / NOT APPROVED CHARACTER ART"
and "ARM + HAND — TEMPORARY PROTOTYPE PLACEHOLDER / NOT APPROVED
CHARACTER ART"), and the corresponding scene nodes carry the
`temporary_placeholder` group.

## Replacing the stand-ins with real approved art later

1. Approve real torso/arm/hand art (owner decision, separate gate).
2. Drop the new sprites into a new assets directory.
3. In `scenes/main.tscn`, replace the textures of `TorsoSprite`,
   `UpperArmL/R`, `ForearmL/R`, `HandSpriteL/R` (and `TargetRing` if the
   mark design changes). Keep the node pivots: `Torso` at the neck
   anchor (540, 310), shoulders at (432, 430) and (648, 430), elbows at
   local (0, 95), wrists at local (0, 85). The rotation animations then
   carry over unchanged.
4. Update `manifest.json` hashes and remove this directory (or keep it
   as historical evidence of the stage-A stand-ins).

The `.png.import` files are Godot-generated import metadata.
