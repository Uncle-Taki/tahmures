# Gemini recovery prompt — website/app

Updated 2026-10-18. Replaces the earlier Tahmures-only scene-refactor prompt.

## Owner setup: five ZIPs in Google Drive

The local repository is `/home/mehdi/Project/leela/tahmures`. Upload these five
separate files from its `editorial/media-handoff/` directory into one Google
Drive folder (suggested name: `Tahmures-Gemini-Recovery-2026-10-18`):

| Local repository-relative file | Archive layout and purpose |
|---|---|
| `editorial/media-handoff/gemini-web-upload-2026-10-18.zip` | Starts with `gemini-web-upload-2026-10-18/`; ten source character images, facial comparison sheet, prompts, review/audit, instructions and approvals. Start here. Contains no nested ZIPs. |
| `editorial/media-handoff/tahmures-working-reference-pack.zip` | Starts at repository-relative paths such as `Characters/`, `book/`, `.agents/` and `.zcode/`; accepted scoped Tahmures work, source artwork, Godot POC and Chapter 01 planning/context. |
| `editorial/media-handoff/incorrect-glm-candidate-part-01.zip` | Rejected project at `Characters/tahmures/prototypes/godot-chapter-01-01/`, including the Persian movie; first English AVI chunk and restore instructions. |
| `editorial/media-handoff/incorrect-glm-candidate-part-02.zip` | Second English AVI chunk, restore script and manifest. |
| `editorial/media-handoff/incorrect-glm-candidate-part-03.zip` | Third English AVI chunk, restore script and manifest. |

All five ZIPs are separate siblings and each is under 100,000,000 bytes. Upload
them separately, without nesting them in another ZIP. The original oversized
`incorrect-glm-candidate.zip` is preserved locally and is superseded for transfer
by the three parts; do not upload it as a sixth archive. The loose
`gemini-web-upload-2026-10-18/` directory contains the small pack's images and
documents. The rejected candidate's art and completion claims remain unaccepted.
Local filesystem paths are not Drive URLs. Uploading these files does not
itself attach their contents to a Gemini conversation. This document does not
perform the upload or create Drive links.

After uploading, paste the task below into Gemini. Use **Add files → Add from
Drive** to select the five files where supported. Connect Google Workspace
and enable Keep Activity if required by the interface; work/school accounts may
need administrator access. Supply the actual Drive file links in the same
message if useful for identifying the files. Do not invent links or assume that
`@Google Drive` search can unpack ZIPs or inspect their embedded images.

### Check access before relying on the archives

Google's [Gemini file-upload documentation](https://support.google.com/gemini/answer/14903178?hl=en-GB)
currently lists a 100 MB ZIP limit, up to ten contained files (subject to
availability), and no audio/video inside ZIPs. Splitting fixes the candidate's
archive size only. The small upload pack has 22 files, the working pack has 399,
and candidate part 01 contains movie content and more than ten files. Parts 02
and 03 contain binary movie fragments, not independently playable clips.
Do not promise these transfer archives meet Gemini's other ZIP constraints.
Storing them in Drive does
not establish that Gemini can ingest them. Google also documents limitations
on pictures/videos through the [Workspace connected app](https://support.google.com/gemini/answer/14959807?hl=en).
Verify actual access with the current interface instead of promising retrieval.

If an archive is rejected or Gemini cannot inspect its contents, keep the five
ZIPs in Drive as transfer copies, extract them locally and attach supported
individual files in batches of up to ten. Start with the ten source PNGs below,
paste this prompt as chat text, then send the comparison sheet, review,
instructions and approvals in a second batch. Supply specific source/code files
from the working and rejected packs as needed; attach any movie separately.
For large code trees, use the interface's supported code-folder import where
available and within its limits. Never treat an inaccessible archive as read.

## Paths after extraction

Let `UPLOAD_ROOT` mean the extracted `gemini-web-upload-2026-10-18/` folder.
Let `WORK_ROOT` mean the directory into which the working-reference ZIP is
extracted; its child directories are `Characters/`, `book/`, `.agents/`, etc.
Let `REJECTED_ROOT` mean the SAME empty directory into which all three
incorrect-candidate part ZIPs are extracted. These are ordinary independent
ZIPs, not a `.z01` multipart archive. Project files from part 01 are directly
inspectable. The English AVI is divided losslessly into
`_reassembly/ch01-en.avi.part-001`, `-002` and `-003`; these are binary chunks,
not separate scenes. After extracting all parts locally, run
`python3 restore-incorrect-candidate.py` from `REJECTED_ROOT` (Python 3.11+).
The helper restores the exact original AVI and verifies all 140 original files.
See `RESTORE-CANDIDATE.md` and `candidate-split-manifest.json` in each part.
Do not concatenate the ZIP files themselves. Scene/code diagnosis can proceed
without restoring that movie. These labels describe archive roots, not paths
on Gemini's host.

| Character | File inside the small upload pack | Corresponding path under `WORK_ROOT` |
|---|---|---|
| Tahmures | `UPLOAD_ROOT/approved_master.png` | `Characters/tahmures/versions/layout01-v2/source/approved_master.png` |
| Akvan Div | `UPLOAD_ROOT/Akvan Div.png` | `Characters/Akvan Div.png` |
| Black Div | `UPLOAD_ROOT/Black Div.png` | `Characters/Black Div.png` |
| Div-e Sefid | `UPLOAD_ROOT/Div-e Sefid.png` | `Characters/Div-e Sefid.png` |
| Shahrasp | `UPLOAD_ROOT/Shahrasp.png` | `Characters/Shahrasp.png` |
| Chapar | `UPLOAD_ROOT/chapar.png` | `Characters/chapar.png` |
| Arash | `UPLOAD_ROOT/arash.png` | `Characters/arash.png` |
| Garshasp | `UPLOAD_ROOT/garshasp.png` | `Characters/garshasp.png` |
| Simurgh, human | `UPLOAD_ROOT/simurgh - human.png` | `Characters/simurgh - human.png` |
| Simurgh, bird | `UPLOAD_ROOT/simurgh - bird.png` | `Characters/simurgh - bird.png` |

Read `UPLOAD_ROOT/START-HERE.md`, `AGENTS.md`, `RTK.md`,
`2026-10-18-glm-character-review.md`, `2026-10-18-glm-character-audit.json`,
`2026-10-18-process-state.md`, `gemini-local-continuation.md`,
`state-contact-sheet.png`, `layout01-v7-human-approval.json` and
`layout01-facial-states-01-human-approval.json` from that same folder.
`UPLOAD-MANIFEST.json` maps copies to original paths and records archive hashes;
the archives it describes are separate Drive files, not nested attachments.
The retained original-candidate record is historical provenance; its
`candidate_parts` records identify the three replacement transfer ZIPs.

Required working directories under `WORK_ROOT`:

- `Characters/tahmures/versions/layout01-v7/`
- `Characters/tahmures/prototypes/layout01-facial-states-01/`
- `Characters/tahmures/prototypes/godot-front-view-character-poc-01/`
- `Characters/tahmures/workflow/` (selected status/approval records only)
- `.zcode/ch01-only-finalization/animation-script/` and its supplied review/brief
- `book/` and `.agents/` (selected canonical/context files only)

The working ZIP is a selected handoff, not the entire repository. If a rebuild
requires historical V2/V5/V6 inputs not present in it, identify the exact missing
paths before attempting that rebuild; do not regenerate or modify frozen
approved packages merely to make the handoff self-contained.

Diagnose the rejected project at
`REJECTED_ROOT/Characters/tahmures/prototypes/godot-chapter-01-01/`:
`assets/asset-map.json`, `scripts/make_standins.py`, `scripts/tahmures_rig.gd`,
`scripts/stage/` and `renders/`. Do not look for these directly at the ZIP root.
Preserve `.import` and `.uid` metadata; caches are excluded from the handoff.

---

## Paste into Gemini (with the setup/path map above)

---

Help recover my Tahmures Godot project. GLM made chapter scenes using abstract
stand-ins instead of the illustrated characters I supplied. **First prepare
every supplied character like the existing layered Tahmures puppet; only after
the character set is prepared and visually reviewed, continue the scenes and
remaining workflows.** Do not begin with another scene rewrite or chapter movie.

This is a bilingual engineering book with original myth-inspired teaching
fiction. Existing manuscript and continuity control roles/plot. My supplied
images control working visual identity over obsolete generic descriptions.
The earlier allowance to use silhouettes for named characters is withdrawn.

## Be clear about access

You are in a web chat. I am supplying the five named ZIPs through Google
Drive. First identify each archive actually attached/retrieved, its accessible
contents and any extraction limitation. Use the archive-root mapping above.
If access fails, request the smallest extracted-file batch needed for the next
step and continue any work supported by accessible inputs. Never claim local
filesystem access, segmentation, file export, Godot
execution, hash verification, image inspection or rendered proof unless you
actually perform it with available tools and inputs. If you cannot produce
layered bitmap assets or runnable project files here, say so and deliver the
precise per-character component maps and local execution handoff; do not call
an annotated full image or a plan a completed puppet. Ask for only the missing
material needed for the current step and continue independent work.

## Character roster

Prepare Tahmures by reusing its accepted head package, then all nine supplied
images: Akvan Div, Black Div, Div-e Sefid, Shahrasp, Chapar, Arash, Garshasp,
human Simurgh and bird Simurgh. Preserve exact source identity: faces,
expressions, skin, outlines, horns, hair, colours, costumes, proportions and
equipment. Do not erase supplied horns or turn the characters into featureless
registry-card silhouettes. Existing source equipment is appearance reference,
not authorization to invent new plot actions.

Both Simurgh images must be prepared separately. They are variants of the same
named character, not two newly invented roles. Do not blend them, silently
choose one or create a transformation. Ask for the chapter's form selection at
the appropriate visual-review point; meanwhile prepare both and continue all
other characters. Chapar remains a distinct incoming courier.

Garshasp and Div-e Sefid must also be prepared for the library even though
Garshasp stays offstage in Chapter 01 and Div-e Sefid is outside its current
eleven-scene adaptation. Available art does not authorize inserting them.

## First milestone: complete character preparation

For every source/variant:

1. Inventory actual name/file/dimensions/mode and image identity. The nine new
   references are RGB with opaque light backgrounds, not transparent sheets;
   human Simurgh is 1087×1447 and the others 1086×1448. Do not invent alpha data,
   a rig or hidden body surfaces from file presence alone.
2. Produce a derived transparent cutout and layered component package if your
   tools support it. Preserve white robes/hair, fine feathers, hand gaps and
   original outlines when removing the background. Leave originals untouched.
3. Separate pose-appropriate head/face, hair/beard/horns/headwear, feasible
   eyes/brows/mouth, torso/neck, arms/hands, garments/legs/feet and held props.
   Use a bird-specific wing/tail/beak/leg structure for bird Simurgh. Copying
   Tahmures's coordinates or humanoid skeleton to every asset is not preparation.
4. Specify each component's box, crop offset/common canvas, anatomical side,
   pivot, overlap order, joint/socket and movement limit. Reassemble from the
   actual separated parts and compare to the original at source scale.
5. Resolve held-prop occlusion honestly. Do not duplicate Akvan's tablets, Black
   Div's cloth/tablet, Shahrasp's book/reed or other items inside both body and
   prop layers. Mark obscured or missing surfaces separately from extracted
   pixels. Any new seam/underlap/closed-eye patch is reconstructed candidate
   art, not recovered or already approved artwork.
6. Build reusable editable Godot character scenes when supported. A whole-image
   sprite with a movement tween or a character-name label is not a layered
   puppet. Show supported neutral/reset, idle, blink/gaze and small gesture
   tests; mark capabilities requiring missing surfaces accurately. Do not
   generate new faces or false phoneme states to make a checklist look complete.
7. Supply actual component sheets, alpha/edge checks on checker/light/dark,
   source-versus-rig reconstruction and motion samples. An intact original
   image hidden beneath the exported layers cannot be used to mask holes.

My instruction selects these images as working references; do not ask whether
to use them again. Permanent-art, reconstructed-surface and final performance
approval still concern actual reviewed results. Do not manufacture those
approvals or mutate Tahmures's frozen indexes/status fields.

Read-only retrieval of the supplied Google Drive materials in this Gemini chat
is authorized. No additional paid/cloud service calls, external image-generation
actions or dependency installation are authorized. Preserve evidence and originals. Where
tool support is insufficient, give a concrete local task per missing output
instead of quietly substituting a stick figure or claiming asset completion.

## Character-readiness gate

Present one review gallery covering Tahmures and all nine supplied images,
including both Simurgh variants. Give each package its source mapping,
extraction/reconstruction status, supported motion, real evidence and remaining
limitations. Request review of the actual completed set and resolve the scene
form choice for Simurgh before claiming selected scene characters. Do not ask
again for any approval already recorded for the exact result.

Do not proceed to chapter assembly merely because files import. Complete the
preparation and meaningful visual checks first. Final approval is not granted
by the model, an output filename or the old GLM claim that review findings are
closed. Do independent planning/diagnostics while awaiting a genuine decision.

## Then continue the remaining workflows

After the character gate, help recover the existing eleven-scene Chapter 01
project. Salvage verified timeline/caption logic, replace all named-character
stand-ins with the prepared reusable characters, and make missing resources
fail explicitly instead of falling back to wrong art. Keep the rejected
candidate intact for comparison. Anonymous background groups/props are a
separate declared scope, never substitutes for named characters.

Preserve correct cast/causality: Chapar brings the tablet; Akvan catalogues;
Simurgh carries it to Arash; Black Div counts the fires; Simurgh's arrival/
delivery precedes dispatch; Shahrasp supports the ledger. The false alarm
comes from ambiguous context, not malicious divs. Preserve the four contextual
labels and eight peer prompt components. Keep Garshasp offstage, Div-e Sefid
outside the eleven scenes, and modern explanation in engineering overlay space.

Inspect the actual screenplay review corrections, not only GLM's self-report.
Check timing, reset/seek, framing and Persian/English captions with the correct
art. Existing renders were measured at approximately 156.47 seconds EN and
18 seconds FA against a declared 173-second plan; this is not complete paired
chapter evidence. Do not assert new rendering/timing tests were performed
unless actual tools ran them.

Later narrated exports require owner recordings and confirmed transcript/cues.
No rejected eSpeak or fabricated speech; no automatic mouth-flap activation.
A simple authorized two-state mouth proxy is not phoneme lip-sync. Adapt audio
duration checks to the full chapter, not the old 18-second character POC.

Conclude with runnable candidate files/patches when tools and source inputs
support them, exact local checks, actual evidence, remaining art/voice choices
and a final-package plan. Only final versions go to Git later. Do not commit,
publish, delete history, rewrite the book/translation hashes or claim a
completed independent review on anyone's behalf.

## What to return now

Start with the attachment inventory and complete the character-preparation
work first. Deliver all character component/rig packages and the review gallery
if tools permit, or clearly labelled exact local instructions where execution
is unavailable. Preserve useful existing Tahmures work. Do not skip to another
chapter render, stop at a vague plan, or declare a scene complete with the
wrong characters.
