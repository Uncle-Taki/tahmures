# Gemini web / Gemini 4 Argon / Nano Banana — background production prompt

Prepared 2026-10-20. Copy the prompt below into Gemini web and attach the actual
reference images. Generate one image per request with the companion shot cards.
This is the owner's manual image-generation workflow, separate from the earlier
code/SVG-only AI Studio task 02. Preparing this prompt does not execute a paid API
call, generate images locally or authorize automatic publishing.

## Before pasting

For exact upload order and ready-to-paste launch messages, use
[the step-by-step workflow](gemini-background-workflow.md). Its collected
`gemini-background-reference-pack/` contains copies of the required files.

Attach these actual files, not just their local paths:

In the collected pack, the three images below have shorter names:
`references/01-tahmures.png`, `references/02-akvan-div.png` and
`references/03-shahrasp.png`, respectively. They are unchanged copies; use
those copies for upload. The paths below identify their original repository sources.

1. `Characters/tahmures/versions/layout01-v2/source/approved_master.png` — Tahmures,
   reference for line weight, colour treatment and character scale.
2. `Characters/Akvan Div.png` — reference for the teal/orange costume and the same
   illustrated world.
3. `Characters/Shahrasp.png` — reference for the scribe's clothing/materials.
4. `editorial/media-handoff/chapter-01-environment-brief.md`.
5. `editorial/media-handoff/gemini-background-shot-prompts.md`.

Optional: attach the local character-gallery PNG for style context, but its
checkerboard, labels, frames and UI are not part of the desired art.
If Markdown cannot be read as an attachment, paste the brief and relevant shot
card as text. No GitHub/Drive access or ZIP extraction is assumed in a web chat.

Use **Gemini 4 Argon**, if available in your account, for the art-direction pass.
Argon's documented output is text; it does not itself generate images. Use
Gemini web's actual image-generation mode for the pictures. These can be two
separate chats; attach the actual reference images in each, since context does
not automatically transfer between them.
Google's [Gemini Apps image guide](https://support.google.com/gemini/answer/14286560?co=GENIE.Platform%3DDesktop&hl=en)
documents image/reference editing and a full-size download action. The exact
model options, resolution and account limits are interface-dependent; record
what was actually used. Argon's current official name is documented
[here](https://ai.google.dev/gemini-api/docs/models/gemini-4-argon).

## Optional first step — paste into Argon for art direction

Attach the source images, this file, the environment brief and the shot cards.
Paste:

```text
Act as Tahmures's background art director. Read the attached master rules,
environment brief, shot cards and actual source-art references. Follow the
existing Chapter 01 plan; do not invent story events or replace our cast.

Prepare one standalone Nano Banana image-generation prompt for BG-HALL-00.
Combine the common visual rules and that card into a clear image request;
prioritise compatibility with the supplied character art, a usable empty
acting floor, quiet subtitle space and a coherent reusable room layout.
Include the actual reference images I must attach in the image chat.
Do not generate code, an app, a new story bible, a completion certification
or claims that you rendered/wrote files. You are preparing text for the
image model. Stop after the BG-HALL-00 prompt.

After I select a real generated master, refine one remaining card at a time
using the selected image(s) I attach. Preserve every card's ID, scene role,
camera/lighting dependencies and clean-plate exclusions. Ask for a missing
visual reference only when it is required for that target; do not claim
that a filename or an earlier chat gives you access to its image pixels.
```

Then paste the assembled image prompt into Gemini web's image mode, with the
actual references. Alternatively skip Argon and use the master below directly
in that image chat. The separate code-only AI Studio Build task is unchanged.

---

## Paste this master prompt

You are the background art director for **Tahmures**, an illustrated bilingual
engineering-book animation. We are generating **25 separate clean background
plates** for Chapter 1, “The Three Readings”, using the attached shot cards.
Gemini 4 Argon handles continuity and prompt refinement where available; the
Nano Banana image-generation tool available in this chat produces the actual
pictures. Report the actual model/tool used rather than claiming a particular
backend from the prompt wording alone.

This is an image-production task, not a request for another scene-plan JSON,
web app, character redesign or a claim that all art is complete. Generate and
return actual images one at a time. All generated images are review candidates.
I select artistic results; Codex later checks files, dimensions, layout,
character compatibility and Godot integration. Do not certify your own output.

### Style and visual identity

Use the attached Tahmures, Akvan and Shahrasp pictures as the visual reference:
warm hand-drawn 2D storybook animation, confident dark organic outlines,
restrained cel-like shading, softly textured plaster/wood/stone, readable
large shapes and gentle depth. Match the reference line weight and rendering
simplicity. Buildings should be detailed enough to feel inhabited, but visually
quieter than the characters. Avoid photorealism, shiny 3D game rendering,
hyper-detailed concept-art spectacle and flat geometric placeholder scenery.

The characters guide style and scale only. **Do not put any people, divs, birds,
horses, faces, statues shaped like the cast or character shadows into these
clean plates.** Do not copy their costume ornaments onto every wall. Do not
copy reference-image backgrounds, checkerboards, UI labels or contact-sheet grids.

This is original Persian-myth-inspired teaching fiction, not a documentary
reconstruction of a specific historical dynasty. Propose modest plaster/stone
walls, cedar furniture, clay vessels, leather, woven textiles and bronze fittings
consistent across the set. Avoid modern technology, fantasy portals, monumental
palaces, religious iconography or stereotyped decorative excess. The supplied
character style, rather than a newly invented historical claim, controls the look.

### Story limits

The hall receives messages on clay, leather, bark and silk. A found tablet is
mistakenly treated as a record, urgent message and current command. A frontier
alarm arises from missing context, not an invading army or malicious divs.
The hall's work, not its decoration, introduces the episode.

The former decorative thirty-door/unlike-handle motif is removed. Do not depict
or allude to it through rows of unusual doors, numbered rooms, portals or handle
collections. A single modest functional hall entrance is enough. The separate
**western gate** remains because it belongs to a later contextual-command example.

Keep readable words, numbers, calligraphy, logos, captions, seals-as-authority
symbols, maps with invented labels, arrows, alignment guides and title lettering
out of the generated art. Catalogue tablets and stored writing materials can
have blank or indistinct nonlinguistic surfaces. Exact story text, labels and
Persian/English captions will be composited later as programmatic text.
Do not request removal of platform-provided provenance marks; add no custom marks.

### Build one coherent Hall of Scripts

First generate `BG-HALL-00`, the neutral-morning wide master. Propose this stable
layout: entrance and intake toward screen-left, an open central floor with the
cedar stand slightly deeper in the room, catalogue wall and worktable toward
screen-right/back, a quiet scribal bench at the side, daylight entering high
from screen-left. This is a layout candidate, not already approved architecture.

Keep the foreground/middle acting area open. The set must accommodate the
source-pose characters at natural size with feet on the floor. The stand and
table must not block the full width of the acting zone. Avoid a huge foreground
desk that would hide every body or hand contact.

Once I select a hall master, use that **actual selected image** as the anchor
for every subsequent hall view. Do not treat silence or an automatic quality
score as selection. During selection I can request a revision; otherwise continue
the queue using the selected visual references without asking permission for
each individual image. Keep the room's floor plan, materials, furniture design,
window direction and proportions consistent.

For the new camera views, reproject the same room rather than adding/removing
doors or relocating furniture. Eye-level/mild three-quarter views match the
existing character artwork. Top-down shots are for separate prop inserts, not
the default backgrounds. For a lighting variant of an existing view, edit that
view's original selected plate and change only light/exterior weather cues.
Avoid repeatedly editing a degraded descendant; return to the clean source anchor.

### Framing and output

Every plate: landscape **16:9**, one full-frame image, no collage, no split panel,
no mockup or letterboxing. Request the highest useful native resolution offered
by this interface, preferably at least 1920×1080 equivalent. A prompt is not a
guarantee of exact pixels: state actual downloaded dimensions if tools expose
them; otherwise mark dimensions unverified. Never claim a small preview is a
4K deliverable. Preserve the original full-size download before local conversion.

For wide/medium acting shots, use this proposed composition in reference
1280×720 space, scaled uniformly to the actual image size:

- Main action inside x=64..1216 and y=64..576.
- Proposed foot contact near y=552; an honest horizontal ground surface.
- Bottom x=64..1216, y=600..704 is a quiet subtitle region: low contrast detail,
  no essential props/faces or strong patterns. Do not draw a caption box.
- Keep actor-scale perspective readable and the horizon consistent within each
  view. Insert/detail plates may use their own camera distance; record that so
  full-body sprites are not mistakenly placed in a tabletop close-up.

These are composition targets, not guides to paint onto the picture. Do not
stretch characters, distort the set or cover the key interaction to satisfy a
nominal coordinate. Use the whole canvas with no decorative border.

Deliver **empty clean sets**. Static walls, shelves, fixed furniture, distant
landscape and stored noninteractive materials may appear. The found tablet,
oilcloth packet, four labels, separate request card, carried book/ledger, reed,
handheld crystal, corrective message and practice/evidence documents must stay
out of these plates. They are separate animation assets. Static shelf objects
must not be confused with those identifiable story props.

Rain streaks, moving smoke, embers, splashes, foreground birds, riders, villagers
and live fire are separate effects/extras; do not bake them into clean plates.
Wet ground, cloudy exterior light and fixed lamp fixtures are allowed when the
shot card specifies them. For the charcoal camp, fire instances and the exact
count of eleven are later controlled in Godot, not entrusted to image counting.

### Honest deliverables and continuation

For each requested ID, return:

1. The actual single image.
2. A short text caption outside the image: ID, suggested filename, set/view/light,
   source anchor used, actual tool and actual dimensions or “not verified”.
3. Any visible mismatch needing revision. Mark status `candidate_needs_review`.

The suggested filename is for me to save the download. Do not claim you wrote
that file into my repository, uploaded an archive, ran Godot, computed a hash,
sampled exact colour values or created PSD layers unless you actually did so.
A flat generated PNG is a **flat candidate plate**, not an editable multilayer
package. We will derive occluders/layout/provenance locally after selection.
Do not fake alpha transparency by painting a checkerboard into an image.

Begin with **BG-HALL-00 only** from the shot-card file. Return the actual image
and its short delivery note. After its selection, continue through the queue in
order, one plate per response or as many separate images as the tool genuinely
supports. Keep a text ledger of finished IDs; a contact sheet is not a replacement
for individual images. If a rate limit/tool limitation interrupts the work,
report the last actual completed ID and the exact next ID so we can resume.

### Prompts to use after the master

**Continue:** “Continue with the next unfinished shot card. Use the selected
master/reference images and locked style; generate the actual single plate.
Do not replace output with a JSON completion claim.”

**New chat:** “Resume Tahmures backgrounds at [ID]. Attached are the source-art
references, selected hall master, relevant set anchor, master prompt and target
shot card. List only missing visual references needed for this image, then
generate it. Earlier text-only references do not establish image access.”

**Lighting edit:** “Edit the attached selected [SOURCE-ID] into [TARGET-ID].
Change only the lighting/exterior weather cues described in that card. Keep
camera, architecture, furniture, dimensions and framing stable; add no actors,
moving effects, text or interactive story props.”

**Correction:** “Revise the attached [ID] only: [specific defect]. Preserve all
other selected geometry/style/composition. Return the actual revised image and
identify the change; do not mark it approved on my behalf.”

## Other model use

For a direct Nano Banana image request, paste the global style/framing rules plus
one complete shot card and attach its source-art/set anchors. Argon can prepare
that combined prompt; if it cannot render an image in the current mode, switch
to the actual image tool instead of requesting a fictional file.

Google documents [aspect-ratio and reference-image controls for developer image
generation](https://ai.google.dev/gemini-api/docs/image-generation). Those API
controls are not a promise that every web-chat option is exposed. This pack
does not need an API key, code execution, GitHub connection or automatic billing.
