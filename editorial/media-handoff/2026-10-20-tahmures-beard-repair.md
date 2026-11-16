# Tahmures beard — source-alpha repair

The owner identified the full-body Tahmures in the environment library's
`preview/hall-source-character-scale.png`, rather than the separate accepted
head inspector. The builder was applying RGB border-colour flood-fill to the
already transparent RGBA master. Transparent black edge pixels allowed removal
to spread into similar dark beard/outline pixels. In source rectangle
`[460,210,620,330]`, 658 visible source pixels had been erased.

`remove_bg_border_flood` now treats an existing alpha channel as authoritative:
it preserves all visible RGBA pixels and normalises RGB only where alpha is
zero. RGB character sources retain the existing background-removal algorithm.
No repainting, new face design, approval promotion or change to source artwork
was necessary. The separate approved head package remains byte-for-byte intact.

Rebuilt Tahmures cutout, six partitions, masks, provenance and QA; regenerated
the actual environment Godot scale preview. The old preview is retained under
`Characters/environments/chapter-01-candidate-01/preview/beard-repair/before.png`.
The adjacent `comparison.png` magnifies the two actual Godot frames.

Verification:

- Ten targeted Python tests pass, including transparent black connected to
  near-black visible artwork, opaque RGBA boundaries, partial alpha and the
  actual Tahmures source-pixel preservation case.
- Full local library validator and Godot rig contract checks pass.
- Every visible source RGBA value matches the rebuilt cutout exactly.
- 672 other-character/approved-head files match pre-rebuild hashes.
- Re-rendered the environment scene on the display; no head/limb motion or
  anatomical approval is inferred from a repaired source-pose cutout.
- Full repository `make check` retains the known stale Persian source-hash
  failures; manuscript review metadata was not modified for this repair.

Reproduce from repository root:

```bash
rtk proxy python3 Characters/godot-character-library-recovery-01/scripts/tests/test_library_contract.py
rtk proxy python3 Characters/godot-character-library-recovery-01/scripts/build_character_library.py
rtk proxy python3 Characters/godot-character-library-recovery-01/scripts/validate_character_library.py
rtk proxy godot --headless --path Characters/godot-character-library-recovery-01 --editor --import --quit
rtk proxy godot --headless --path Characters/godot-character-library-recovery-01 --script scripts/tests/rig_contract_test.gd --quit-after 20
rtk proxy godot --path Characters/environments/chapter-01-candidate-01 -- --capture
rtk proxy godot --path Characters/environments/chapter-01-candidate-01 --script beard_comparison.gd
```
