# Next bounded unit — implement the S01 proof

The static board/preparation unit has produced actual files under
`Characters/animations/chapter-01-candidate-01/planning/`. Read its README,
shot-board.json, missing-asset matrix and s01-proof-specification.md first.
Planning checks pass; artistic approval and performance do not follow from that.

Implement only S01 under `Characters/animations/chapter-01-candidate-01/`:

1. Prepare the minimal crystal, silk, incoming-material and Shahrasp contact
   assets. Reuse actual identity/style references, preserve originals, and
   explicitly record new reconstructed art. Do not mistake the stock held
   book/reed pose for a crystal/silk grip. Any wide-to-insert prop discontinuity
   must be resolved before the proof is accepted. The r02 board commits to
   WIDE-CONTACT-S01 in A/C, matching the close insert's grip rather than switching
   back to stock book/reed. This mandatory P0 artwork is not yet delivered.
2. Create the Godot project/controller and absolute-time 12-second candidate
   timeline. Show the single reading action, then the incoming material reveal.
   Implement EN/FA captions, measured layout and a verified font licence.
3. Implement the proposed render_s01.py runner/interface in the specification,
   with explicit input validation and actual frame capture. The specification's
   commands are future commands until that runner is implemented.
4. Verify normal playback, boundaries, direct seek/reset/replay, missing/malformed
   resources and unsupported languages. Produce real 360-frame captures per
   edition at the current budget and inspect difficult contact/text frames.
5. Save actual commands, exits, dimensions, hashes and visual findings. Use
   source-pose/media validators and required repository checks; report known
   editorial blockers separately. Update chapter-01-animation-status.json.

Include the r02 motion-specific checks (`grip_continuity`, `one_pass_scan`,
`independent_motion`) and their detach/oscillate/whole-picture negative fixtures.
Return per-frame traces and actual frame/ROI evidence; these checks are specified
but not implemented by the board review itself. Read planning/review-reconciliation.md
for the remaining Qwen findings and direct human floor notes.

Simurgh's form and voice approach remain unresolved owner choices. S01 does not
need either to proceed as a silent visual proof. Do not invent speech, new head
motion approval, final performance signoff, commit/push/publish, or full-chapter
implementation. Full integration begins only after this proof is checked.
