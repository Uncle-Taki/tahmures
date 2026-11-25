# Installation

## Safe installation

1. Back up or commit the current Tahmures repository.
2. Place `Tahmures_Character_Skills_Pack.zip` in the repository root.
3. Extract it at the repository root:

```bash
unzip -n Tahmures_Character_Skills_Pack.zip
```

4. Confirm both paths exist:

```text
skills/tahmures-character-design/SKILL.md
skills/tahmures-blender-production/SKILL.md
```

5. Do not replace the existing `tahmures-blender-production` skill. The new skill is an orchestration and design layer; the existing skill remains the authority for its own Blender production implementation.
6. Open the new `skills/tahmures-character-design/SKILL.md` in Codex and confirm that its relative references resolve.

## Post-install checks

```bash
test -f skills/tahmures-character-design/SKILL.md
test -f skills/tahmures-character-design/scripts/tahmures_character_utility.py
test -f skills/tahmures-character-design/config/utility_weights.json
python3 skills/tahmures-character-design/scripts/tahmures_character_utility.py --help
```

The utility has no third-party Python dependencies.
