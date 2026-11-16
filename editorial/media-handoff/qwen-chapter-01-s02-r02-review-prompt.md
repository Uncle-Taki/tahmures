# Optional review — S02 r02 held-pose art gate

Codex has implemented and checked this unit locally. Qwen tokens are not a gate.
If an external reviewer is available, review read-only under AGENTS.md/RTK.
No manuscript, original art, approval, prior evidence, provider call, commit,
upload, push, or automatic repair is authorized. Do not mark owner approval.

Candidate root:
`Characters/animations/chapter-01-candidate-01/revisions/s02-r02/`.

Read README, manifest, exact generation prompt, shot-override.json,
approval-request.json, index.html, review.gd/tscn/project.godot and
check_and_capture.py. Inspect actual assets/chapar-held-tablet.png and
actual evidence/local-02/{en-hall,fa-hall,en-contact}/study.png with their
render-state.json, Godot logs and verification.json. Compare actual original
Chapar and r01 tablet images named by the manifest; check canonical Chapter 01,
continuity and board S02-A/B/C. Do not infer file access from a filename.

Priority questions:

1. Does the new whole generated derivative preserve recognizable Chapar identity,
   costume and strap grip well enough? The face, folds and stance changed beyond
   the requested free arm. No exact original pixel identity is claimed. Judge
   the source/candidate side by side; identify concrete visual defects.
2. Inspect sleeve/wrist, visible palm and foreground fingers in the actual QA
   crop. Is one tablet plausibly supported without duplicate old hand, floating
   edges, fused fingers or misleading seal identity? It is a static hold only;
   no hidden thumb/back surface, independent mask, grip dynamics or release is
   proved. Does the redrawn tablet still read as the same r01 design? Compare
   texture/style, residue and cord ends; neither asset is owner-approved.
3. Do both actual hall captures show sensible scale, feet on visible floor,
   unclipped prop and readable exact EN/FA NEN-02A/OST-S02-1 text? Full actual
   BG-HALL-02 art is used without invented extent. Tablet is held above the
   counter, not placed. Message is review overlay, not baked clay glyphs.
4. Verify the scope: no Akvan receiver in this proposal (original board called
   her role a staging inference), no substituted stock three-tablet hold,
   no change to canonical carrier/recipient uncertainty. S03 cedar-stand action
   remains Tahmures's later action. The QA crop is not a production close-up.
5. Check actual source/dependency/asset hashes, fresh-output guard, 15 negative
   cases, current code-to-report binding and actual viewport capture commands.
   In local-01 a blank white contact crop was missed by initial numeric checks;
   it is superseded. Holding the Texture2D resource fixed it. The current
   blank-image fixture must fail, and local-02 must contain actual art. Source
   conservation/technical success cannot approve visible contact quality.
6. Approval-request.json requests art selection only, not acceptance. S01 r04
   motion and Simurgh/voice remain pending. No full S02 performance or chapter
   assembly exists. make-check.log records 789 pass / 8 stale Persian source-hash
   failures, later targets not reached. No metadata repair was made.

Commands from repository root:

```bash
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/revisions/s02-r02/check_and_capture.py --validate-only
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/revisions/s02-r02/check_and_capture.py --output evidence/external-01
```

Use another fresh suffix if it exists. Capture needs local display access;
headless import alone is not capture. Offline QA uses installed system Pillow;
existing S01 production validators remain stdlib-only.

State exactly which files, images and commands you accessed. Return separate
technical and visible-art verdicts, concrete coordinate/file evidence and bounded
repairs. Do not approve unproduced release animation. Save any report separately
as editorial/media-handoff/qwen-chapter-01-s02-r02-review.md.
