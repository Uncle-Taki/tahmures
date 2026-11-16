# Qwen prompt — independent Chapter 01 board / S01 preparation review

Use this with Qwen in the repository, or upload the actual files/images listed
below in a web chat. Local filenames alone do not provide a web model access.
No particular Qwen model/version capability is assumed.

## Files to provide

Repository agent: open the files from the checkout and inspect the images.
Web chat: attach these files; paste Markdown as text if attachments are unreadable.
The first three files are under
`Characters/animations/chapter-01-candidate-01/planning/`:

1. `shot-board.json` — primary review target; includes cue text, shots, actual
   reference paths/hashes, custody, camera rectangles and known risks.
2. `missing-asset-action-matrix.json` — requirements and S01 priorities.
3. `s01-proof-specification.md` — proposed implementation contract.
4. `book/part-1/01-what-is-a-prompt.md` — canonical English story/bridge.
5. `book/fa/part-1/01-what-is-a-prompt.md` — corresponding Persian text.
6. `book/narrative-continuity.md` — canonical roles/continuity.
7. `planning/storyboard-contact-sheet.jpg` — use the full path under the planning
   directory above; static board overview, not rendered performance.
8. `planning/panels/ch01-s01-a.png`, `ch01-s01-b.png` and `ch01-s01-c.png` from
   the same directory — full-resolution S01 panels. Add other individual panels
   as needed; unreadable thumbnails do not support detailed visual claims.
9. `planning/s01-caption-layout-en-nen-01a.png` and
   `planning/s01-caption-layout-fa-nen-01a.png` from that directory — static
   caption-layout specimens. The second cue's corresponding files are available
   too, with suffix `nen-01b.png`.
10. `Characters/Shahrasp.png` — actual source-art reference showing the current
    book/reed hold. This image is essential to judge the S01 prop conflict.

Additional repository references, or attachments if needed:

- Planning `README.md`, `board-validation.json`, `s01-caption-layout-check.json`,
  `shot-seeds.json`, `build_board.py`, `shot-board.md` and `index.html`.
- `editorial/media-handoff/chapter-01-production-plan.json`.
- `editorial/media-handoff/chapter-01-animation-workflow.md` and
  `chapter-01-animation-status.json`.
- `editorial/media-handoff/2026-10-20-tahmures-beard-repair.md`.
- `Characters/environments/chapter-01-candidate-01/README.md`, `manifest.json`
  and the original background/character files actually referenced by a finding.

Do not use the raw `tahmures_complete_studio_bundle.json` as acceptance evidence.
It is a received proposal with unsupported implementation/certification claims.
If supplied for comparison, keep it subordinate to the canonical story and the
current local evidence.

---

## Copy/paste review prompt

You are the independent **Qwen reviewer** for Tahmures Chapter 01, “The Three
Readings”. Review the **static Chapter 01 board and S01 production preparation**.
Your job is to find concrete defects and assess whether the proposed next unit
is well specified. Do not implement the animation, redesign characters or
approve work on the owner's behalf. Codex will verify and address your findings.

### Authority, access and scope

Follow repository `AGENTS.md` and applicable local instructions when available.
English Chapter 01 and `book/narrative-continuity.md` control story and technical
meaning. Persian human-reviewed wording must not be changed by this review.
The production plan is a candidate adaptation; the board may legitimately flag
problems in it rather than reproduce them silently. Existing scoped artwork
approvals cover only their stated assets/states, not a complete animation.

First state which files and images you actually accessed. Distinguish:

- content inspected directly;
- assertions found in validation/status documents;
- checks you independently reproduced;
- unavailable material or tools.

In a web chat, do not claim local filesystem, Git, Godot or hash access merely
because the prompt lists a path. Inspect attached pixels, not filenames. If a
visual reference is missing or unreadable, identify exactly which judgments are
limited and continue the independent checks that remain possible.

This is a review task. Do not edit source/planning files, regenerate assets,
update status/approval records, rewrite Persian hashes, call providers, install
dependencies, commit, push or publish. Do not run `build_board.py` just to inspect
it: it overwrites planning outputs. In a repository session, use read-only code,
JSON, path/hash and image inspection as needed; prefix shell commands with `rtk`.
Report actual commands/results, never invented runs.

Return the review as Markdown. If a repository session supports saving a report,
the only new file allowed is
`editorial/media-handoff/qwen-chapter-01-board-review.md`. Otherwise return the
report in chat. Its creation is not approval and must not mutate phase state.

### Current claims to verify independently

The preparation package reports 34 shots covering 11 scenes, 34 candidate
narration/dialogue cues and 18 candidate on-screen text entries. Proposed timing
is 0–173 seconds, 30 fps, 5190 frames, in 1280×720 reference space. The asset
matrix currently has 47 rows. Check these against actual data; do not repeat
them as verified facts without checking.

All panels are **static blocking proposals** using background and unchanged
source-pose references. Amber role/contact markers explicitly represent missing
art or unresolved casting. They are not performed contact actions or final
actors. The S01 Godot project/runner, recordings and actual reading performance
are not claimed as implemented by this preparation task. Future commands in the
specification are proposed interfaces, not commands already executed.

### Review A — story, roles and causality

Check every scene and shot against an exact canonical section/quotation:

1. S01 introduces incoming clay, leather/bronze tube, bark and silk, with
   **Shahrasp** reading fine silk writing through a polished crystal. No substitute
   reader, modern magnifying-glass assumption or invented plot beat.
2. Chapar is the initial courier, distinct from Simurgh. Three recipients
   interpret one found tablet differently. Garshasp stays offstage; Div-e Sefid
   is not inserted because an asset happens to exist.
3. Track the tablet, wrapping and packet through every relevant shot. Check
   whether stock held objects accidentally imply extra copies. Black Div must
   not leave carrying the same tablet that Simurgh wraps/transports. Discussion
   of the object in S07 must not silently teleport its packet back from Arash.
4. Simurgh's delivery precedes Arash's dispatch. Three villages remain distinct;
   eleven fires belong to charcoal burners, not invaders. No malicious-div or
   seal-as-authentication explanation is invented.
5. S07 contains one complete reed-sharpening action, a stop, four labels and a
   separate request card. Requested result is **classify the object and state
   what information is missing**, not count the fires. Is the card visibly and
   semantically separate from the examined sentence?
6. S08 preserves the *same sentence* as current task, quoted court evidence and
   apprentice practice. The ordinary western gate remains; the decorative
   multiple-door/unlike-handle motif is removed. Arash's stock bow/quiver must
   not invent an archery event or mythical claim.
7. S09 is the engineering bridge: eight equal-weight components; deterministic
   application enforcement is outside the metaphor. No seal/security hierarchy.
8. S10 corrects the rumour and returns riders; messenger form and dawn village
   choreography remain labelled staging choices. S11's lamplit ledger is a
   recap, not an unexplained new night after dawn.

Flag inference presented as canon, changed agency, missing causality and unclear
prop identity. Separate actual story defects from optional visual preferences.

### Review B — shot data, cameras and visual blocking

Inspect source JSON and the actual available panels:

- Unique IDs, complete scene membership, positive intervals, half-open frame
  boundaries, arithmetic and contiguous scene coverage. Do not equate arithmetic
  coverage with natural speech or successful action timing.
- Every camera references actual existing imagery; crop rectangles stay in
  bounds and preserve aspect ratio. Cropping a flat plate must not imply newly
  drawn geometry, usable tabletop perspective or unseen character surfaces.
- Cast/pose scale, foot contact, perspective, furniture overlap, caption safety,
  readability of the proposed action and contact-insert placement. Are positions
  and offsets consistent between JSON, panels and S01 specification?
- Does the board clearly identify missing extras/props/actions rather than
  depict the source pose as evidence that the performance exists? Does a
  supposedly illustrative pose contradict the stated custody strongly enough
  that it needs replacement even in the production plan?
- Simurgh stays explicitly unresolved. A marker is acceptable for planning; it
  cannot qualify a final handoff. Do not select the human/bird form yourself.

Inspect full-resolution panels for specific findings; the contact sheet alone
cannot establish fine alpha/contact or small-text quality. Do not treat every
deliberate planning marker as a newly discovered production defect.

### Review C — cues, bilingual readability and timing

Check cue/OST references, intervals, exact strings and relation to visible shots.
Inspect English and Persian specimens where supplied. Check Persian shaping,
ZWNJ, word order and direction without rewriting approved wording to mimic
English. Distinguish Pillow/RAQM specimens from an actual Godot font/render test.

Independently evaluate these **known open risks**; confirm, refine or dismiss
with evidence rather than merely echoing the risk list:

- S03 leaves 2.5 seconds for the three inspection actions/two readings.
- S06's first candidate cue describes charcoal burners while the board opens
  with delivery/dispatch. Preserve the causal order when proposing a repair.
- S07's label/card density and long bilingual requested-result text.
- S08's sentence OST currently ends with the gate vignette although the same
  wording should be visible in the court and apprentice contexts.
- S10's three calm village reprises are only about 1.3 seconds each.
- S11's ledger OST continues into the proposed end-card interval.

Propose the smallest coherent remedy: retime a cue, extend a shot, adjust layout
or clarify a transition. Do not insist on 173 seconds when it harms readability.
Do not claim recorded pacing has passed without actual recordings.

### Review D — S01 implementation readiness

Review `s01-proof-specification.md` as an executable work specification:

1. Is the minimum crystal/silk/material/contact asset list complete and properly
   prioritised? Does the matrix cover the spec's work, including any wide contact
   pose required to make the transition coherent?
2. Shahrasp's source drawing holds a book and reed. Is the wide-to-close-to-wide
   plan consistent, or does it leave an unresolved prop/action discontinuity?
   A dedicated insert must not animate through stock hands or hide a missing
   grip behind a whole-image translation.
3. Are the proposed screen anchor, uniform scale, native alpha bounding box,
   coordinate conventions and camera crop consistent? Can the scribe stand clear
   of the painted bench and still perform the intended action with plausible
   reach? Clearly separate an untested contact assumption from measured fact.
4. Can the crystal move with its holding hand while the silk stays supported?
   Is approach -> one scan -> settle an actual finite action specification?
   Are newly reconstructed pixels and allowed transform limits documented?
5. Are caption/title regions, font/rights/shaping checks and both languages
   specified adequately? Does the requirement avoid generated pseudo-writing?
6. Are absolute-time state, direct seek, reset/replay, resource failures,
   malformed inputs, boundaries and output frame counts sufficiently specified?
   Identify missing tests that would catch a real likely failure.
7. Are the proposed future render commands clearly labelled unimplemented?
   Are actual expected outputs and validation evidence defined without pretending
   that file presence proves rendered performance?

Missing contact artwork is expected next-unit work. It blocks accepting an S01
performance today, but does not by itself invalidate a sound preparation package.
An incoherent or underspecified plan that the implementer cannot resolve safely
is an actionable planning/readiness finding. Judge these separately.

### Review E — evidence and boundaries

Verify that claims remain scoped: static board vs animation; source-pose
recomposition vs anatomical rigging; beard-alpha repair vs approved new art;
machine checks vs owner signoff; media checks vs full repository release.

Reported full repository baseline is 789 tests passing and eight stale Persian
source-hash failures. Confirm only if you actually run/inspect current evidence.
Do not change review metadata or recommend bypassing validators to make it green.
The beard repair preserves existing RGBA rather than repainting the face; do
not propose editing frozen head/source files as a routine staging fix.

### Required report

Use this structure:

1. **Review basis and access limits:** actual files/images/commands inspected;
   note snapshot/hash identity where measurable.
2. **Two distinct verdicts:**
   - Planning-package quality: `PASS`, `PASS_WITH_REWORK`, `BLOCKED` or
     `INSUFFICIENT_EVIDENCE`.
   - Ready to start bounded S01 implementation: `READY`,
     `READY_WITH_EXPLICIT_CONSTRAINTS`, `REWORK_FIRST` or
     `INSUFFICIENT_EVIDENCE`.
   State separately that completed S01 performance/final animation/owner art
   approval are **not assessed or granted** by this planning review.
3. **Prioritised actionable findings**, sorted by severity. For each provide:
   stable finding ID; severity (`blocker`, `high`, `medium`, `low`); affected
   file and shot/JSON key or verified line; observed evidence; consequence;
   smallest concrete repair; and a test or visual check demonstrating closure.
4. **Known-risk disposition:** each supplied risk confirmed/refined/dismissed,
   with evidence; distinguish already disclosed limitations from newly found
   contradictions or missing requirements. Do not double-count the same cause.
5. **Coverage summary:** all 11 scenes, custody chain, cue/OST mapping,
   camera/reference checks, S01 minimum assets, bilingual specimens and future
   proof tests. Mark unavailable checks `not verified`.
6. **Next repair order for Codex:** a short ordered list of changes necessary
   before S01 implementation, changes implementable within S01, and later-chapter
   dependencies that do not block S01. Keep owner casting/voice/art decisions
   distinct from routine engineering work.

No invented percentage scores, certification flags, human approvals or execution
claims. If no actionable defect is found, say so with the exact inspection limits;
do not manufacture findings to fill a quota. Review independently and concretely.
