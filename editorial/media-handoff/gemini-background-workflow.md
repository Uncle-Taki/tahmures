# Chapter 01 backgrounds — exact upload and generation workflow

**Current status (2026-10-20):** the owner requested Codex take over after Gemini
quota was exhausted. The 25 candidate image plates now exist in
`Characters/environments/chapter-01-candidate-01/`, with actual Godot previews.
The steps below remain a reusable manual alternative. The queue has been updated
with real files; do not restart generation simply because an older instruction
describes an initially empty queue.

**Start with the master rules and actual references together, not the master
file alone.** After setup, request one shot at a time. The 25-card file is the
catalogue; the JSON queue is a local tracker, not an image request.

The ready-to-use folder is `gemini-background-reference-pack/`. Everything below
refers to that folder. The ZIP contains the same files: extract it locally,
then upload individual files to the chat. Do not depend on Gemini unpacking it.

## 1. Prepare the files

Open [the collected pack](gemini-background-reference-pack/START-HERE.md).
It contains byte-for-byte copies of these three required image references:

| Pack file | Role |
|---|---|
| `references/01-tahmures.png` | Line weight, colour treatment and character scale. |
| `references/02-akvan-div.png` | Matching illustrated world and material treatment. |
| `references/03-shahrasp.png` | Matching costume/material rendering and scale. |

These are style/scale references. The backgrounds themselves remain empty.
No additional character-gallery image or old candidate ZIP is required for
this background pass. The pack's `reference-manifest.json` records source paths,
copied paths, dimensions and SHA-256 hashes.

## 2. Argon chat — prepare the first image prompt

For the requested Argon-to-image workflow, open a chat using Argon where it is
available and attach these **six files together**:

1. `references/01-tahmures.png`
2. `references/02-akvan-div.png`
3. `references/03-shahrasp.png`
4. `gemini-background-master-prompt.md`
5. `chapter-01-environment-brief.md`
6. `gemini-background-shot-prompts.md`

Paste the text inside **`prompts/01-start-argon.txt`** as the message. That
message selects the direction task from the attached master document: Argon
returns one complete image prompt for `BG-HALL-00`. Save that text. Do not ask
Argon to implement an app, finish the whole queue or claim it created images.

If a Markdown attachment is not readable in that interface, paste its contents
as context first, then paste the launcher. Attach the actual PNGs as images.

## 3. Gemini web image chat — generate BG-HALL-00

Open Gemini web's image-generation chat/mode and attach the same **three PNGs**.
Paste the complete BG-HALL-00 image prompt returned by Argon. If Argon asks to
attach an additional selected reference, attach that actual image too.

For this first plate, no generated set anchor exists yet. Request **only
BG-HALL-00**. You do not need to upload the JSON tracker or all 25 cards to this
image chat when the assembled prompt contains the full rules and target card.

Optional direct route: skip step 2, attach the three PNGs and paste
**`prompts/02-start-image-chat.txt`**. It already contains the master image rules
and complete BG-HALL-00 card. Both routes target the same first image; do not run
both unless you deliberately want two candidates.

## 4. Download, review and select the hall anchor

Download the actual full-size image, preserving its original file format.
Save it locally under `background-returns/ch01/BG-HALL-00/` with a revision name,
for example `bg-hall-00-r01.png` **only if it is really PNG**. These return folders
are a suggested location, not pre-existing rendered outputs in this pack.

Bring the downloaded image back to Codex for inspection against the character
art, usable floor, perspective, table access, subtitle space and prohibited
baked text/props. Revise if needed. You select the artistic result; Codex checks
the actual files and later integration. Do not treat the model's approval text
as a review. Keep all revisions distinct.

Once selected, tell the image chat:

```text
Use this attached BG-HALL-00 revision as my selected hall reference for the
next views. It is the architecture/style anchor. Generate only the next target
I request, preserving the relevant geometry and clean-plate rules.
```

Attach the selected image with that message, especially if the chat is new.

## 5. Repeat one card at a time

Use the order in `gemini-background-shot-prompts.md`. The pack also contains
one ready-to-paste text file per image in **`shots/`**. Each combines the common
image rules with that single card.

For each target:

1. Read its `Attach actual selected images` line. Attach those previously
   selected images, not just their filenames. Keep the source character PNGs
   available; reattach them in a new chat.
2. If continuing with Argon direction, attach the same relevant selected
   references in the Argon chat and use `prompts/03-next-argon.txt`, replacing
   `[TARGET-ID]`. Paste the returned standalone prompt into the image chat.
   Otherwise paste the target's complete `shots/<ID>.txt` directly.
3. For a lighting edit, attach the selected original source view and use
   the target card, optionally prefaced by `prompts/04-lighting-edit.txt`.
   Preserve camera/geometry. Use the source listed by the card, rather than an
   arbitrary chain of edited descendants.
4. Download the actual result, record target ID/revision/model and send it for
   review before depending on it as a selected reference for another image.

The night and dawn villages A/B/C remain three distinct locations. The fire
count, characters, gate leaves, interactive props, effects and exact bilingual
text are later separate assets. The engineering slate and end card are two
editable programmatic stages; they are not additional Nano Banana requests.

## 6. Return the batch to Codex

Return the actual image files, selected revision per ID, model/tool used and
known issues. Include the original full-size downloads. The pack's
`gemini-background-queue.json` now records the received/generated candidate files;
its status fields alone are not evidence of acceptance. Codex inspects actual dimensions,
hashes, completeness, style/layout and later Godot composites. Flat downloads
still need local layer/occluder preparation where required.

If interrupted, record the last downloaded ID and exact next ID. In a new chat,
reattach the three source PNGs, the selected set/source images needed by the
next card, and paste that complete single-shot prompt. Chat history does not
transfer reference images automatically.

## Refresh this local pack after prompt changes

From the repository root:

```bash
rtk proxy python3 editorial/media-handoff/prepare_gemini_background_pack.py
```

This offline command recopies the selected references and current prompt
documents, rebuilds the individual card files, verifies copied hashes and
recreates the ZIP. It does not generate images or alter original artwork.
