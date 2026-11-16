# Validation — character information update, 2026-10-30

PASS: local package generation and validation completed with exit 0. `make check PYTHON=.venv/bin/python` also completed with observed exit 0 on this update; its captured output is make-check-character-info.log in the shared parent directory. The earlier report/log remains under history/character-update-01 and make-check.log.

## Current counts

- Paper Puppet: nine physical principal references, including unchanged copies of the supplied Chapar nomad and Arash armored archer; no named principal image missing.
- Illustrated V2: seven references; Chapar/Arash still lack matching images. Their information sheets explicitly say MISSING.
- Eighteen principal Character info sheets, two indexes, two supporting-performer sheets, two roadmaps and two workflows.
- Both branches retain eleven editorial units, 44 action-led source-beat cards each, 114 paired script blocks and 66 spoken cues per language. This update does not rewrite dialogue or invent duration.

## Checks actually run

```bash
rtk proxy /usr/bin/python3 editorial/media-handoff/chapter-01-rewrite-2026-10-30/scripts/build_packages.py
rtk proxy /usr/bin/python3 editorial/media-handoff/chapter-01-rewrite-2026-10-30/scripts/validate_packages.py
rtk proxy make check PYTHON=.venv/bin/python
```

The scoped validator checks nine character records per branch; card body/image/hash and cue mappings; image opening/dimensions/alpha; copied-byte equality; source/evidence existence; scene/speaker/shot coverage; exact unchanged language text; no fabricated recordings/times/remote registrations; branch-specific missing-identity sets; and relative Markdown/image links. It also confirms the original 203 protected source hashes. New portrait hashes are recorded in manifests/paper-puppet-cast-additions.json and asserted by the builder. See validation-results.json.

All nine Paper Puppet portraits are opaque RGB. The two supplied files were visually inspected, not edited or background-removed. Existing selected-cast collections, original screenplay, manuscripts, old production/official handoff and source artwork remain unchanged. The new images were appended to the local RW01 handoff through a separate addition manifest.

## Still unverified

The new references do not supply mounted Chapar, Arash desk/bow-rest handling, speaking poses, sets, props or start frames. Five earlier Paper Puppet single-portrait derivatives and two V2 garment derivatives retain their existing review requirements. All new performance, voice and language timing remain unestablished; no final mouth/beak approval is claimed. The independent bilingual read-through from the prior writing pass remains a machine editorial review, not a new human decision.

The repository gate validates book/code workflows, not artistic quality or actual animation/lip-sync. No external generation, Flow access/upload, paid API, commit or push was performed. Per-scene/take logs are preserved across rebuilds and are filled only from actual owner observations.

## Design consistency review — 2026-10-30

All sixteen supplied images were visually inspected in full-body and upper-body comparison sheets. Two branch-specific DESIGN_CONSISTENCY_REVIEW.md reports record observations versus proposed fixes, with source hashes/crop evidence in each design-review/ folder. Sources were not edited; labelled crops are inspection derivatives, not approved Portrait inputs. No style percentages or numerical consistency scores are claimed. `review_character_designs.py` and `validate_packages.py` completed with exit 0; review-evidence hashes match all sixteen input images. `make check PYTHON=.venv/bin/python` completed again with observed exit 0; log: make-check-design-review.log. Artistic consistency remains a subjective review, not something the root gate certifies.

## Latest: portrait/body and Paper Puppet correction task

The latest request authorized actual image edits. Four built-in image_gen corrections were made and saved; 16 portrait/full-body pairs were prepared (9 Paper Puppet, 7 V2). The current pair/shot/pixel/hash checks passed, and `make check PYTHON=.venv/bin/python` completed with observed exit 0. See flow-paper-puppet/portrait-body-candidate-01/VALIDATION_REPORT.md and DESIGN_GAP_RESOLUTION.md; exact prompts are in generation-record.json. `make-check-portrait-body.log` captures the repository gate. No Flow access/upload, video/voice generation, commit or push. Earlier no-generation statements describe earlier preparation-only scopes.

## Paper Puppet Div-e Sefid horn rebuild r02

A new complete Paper Puppet body and exact portrait were generated after the owner clarified that Illustrated V2 is excluded. Current C01 maps/gallery reference the r02 source via body-overrides.json, preserving the r01 pair. Scoped validation and `make check PYTHON=.venv/bin/python` completed with observed exit 0. All 129 Illustrated V2 files match their pre-integration hashes. The earlier interrupted V2 image output was never applied to the repository. Exact prompt, visual review and hashes: flow-paper-puppet/portrait-body-candidate-01/revisions/div-e-sefid-horns-r02/.
