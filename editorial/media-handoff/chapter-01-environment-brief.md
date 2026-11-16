# Chapter 01 environment and scene-asset brief

Prepared 2026-10-20. **Design brief only; no background art approved or delivered.**
The manuscript and narrative continuity control events; all layouts, architecture,
camera placement and lighting here are proposed project-fiction staging
(`TIER_C_PROJECT_FICTION`), not historical reconstruction or a new story bible.
Machine-readable counterpart: `chapter-01-production-plan.json`.

## One consistent visual world

Match the supplied character drawings: readable hand-drawn outlines, restrained
colour/shading, warm tactile materials and clear silhouettes. Use the actual
ten source references when testing the style; do not introduce a competing cast
or photorealistic backgrounds that make the illustrated characters look pasted in.
Choose colours from sampled source art and record them; no new palette is approved
by this brief. Keep quiet wall/floor areas behind the cast and text.

The Hall is a **working place for messages and interpretation**, not a portal
maze. Clay impressions, folded leather/tubes, marked bark, fine silk, catalogue
shelves, the cedar stand, crystal, reed and experiment ledger supply its identity.
Do not design a thirty-door panorama, unlike handles, numbered rooms or a door
metaphor. A modest functional entrance is sufficient as proposed staging.

Propose one hall floor plan: entrance/intake on one side, the cedar stand in the
middle, worktable and catalogue wall deeper inside, a quiet scribal bench off to
one side. Keep their relative positions, window direction and scale stable in
wide, medium and insert views. Do not redesign the room independently per scene.

Use eye-level or mild three-quarter perspective to match the existing source
poses. Top-down inserts show hands and props only; they cannot manufacture a
top-down version of a front-view character. Props that characters must touch
must be separate from the painted set so they can actually change hands.

## Reusable sets and lighting

| Set | Required views | Lighting / state variants |
|---|---|---|
| `ENV-HALL`: Hall of Scripts | Wide, threshold, intake, cedar stand, catalogue, worktable, scribal bench | Dawn, wet morning, morning, dusk, lamplight. Reuse architecture; make light/atmosphere separate layers. |
| `ENV-POST`: northern frontier post | Arrival/delivery, rider departure | Night. Packet handoff readable before dispatch; no visible invaders. |
| `ENV-VILLAGE`: frontier village kit | Village wide; three distinct panels using the kit | Night alarm and dawn calm. Lamps and uncertainty convey the rumour; no attack scene. |
| `ENV-CAMP`: charcoal burners | Camp wide, fire insert | Calm night. Eleven scene-controlled fires; smoke/embers separate. These are occupational fires misread as watchfires. |
| `ENV-GATE`: western gate | Gate and watch | Day. Keep this functional gate for the sentence-role example. |
| `ENV-COURT`: trial evidence | Exhibit/evidence table | Day. The quoted sentence is evidence, not an order being obeyed. |
| `ENV-FORD`: northern road/ford | Road, return crossing | Dawn. Riders return; no newly invented drowning or water crisis. |
| `ENV-OVERLAY`: engineering stage | Neutral slate, end card | Flat code-native design. Not an ancient-world room. |

The apprentice vignette reuses the hall's scribal bench; it does not require a
ninth unrelated room. The village kit must support three readable locations,
not silently collapse the source's three villages to one.

## Coverage of all eleven scenes

| Scene / time | Views and variants | Foreground action and missing support assets |
|---|---|---|
| S01 / 0–12 s | Hall wide, dawn; optional crystal/silk insert | Incoming materials and Shahrasp reading; real source characters, lens and silk/ledger props. The revised opening establishes the work of the hall. |
| S02 / 12–28 s | Hall intake, wet morning | Chapar brings the found tablet; damp garments/rain separate. Close-up of lost seal must not become proof of a sender's identity. |
| S03 / 28–38 s | Hall cedar stand, morning | Tahmures and three recipients; tablet readable as the same object, with lens/cord inserts as feasible. |
| S04 / 38–53 s | Hall catalogue, intake and threshold, morning | Catalogue entry, oilcloth wrapping, Black Div departure. Use the same tablet/custody continuity across the three interpretations. |
| S05 / 53–68 s | Hall worktable, dusk | Wet Black Div reports; dialogue framing and approved head state where supported. No independent sleeve/face motion without valid art. |
| S06 / 68–85 s | Post delivery → rider exit → three village panels → charcoal camp, night | Simurgh delivers before Arash dispatches; riders/horses, villagers/lamps, charcoal burners and exactly eleven fire instances. No malicious-div framing. |
| S07 / 85–116 s | Hall worktable, lamplight; prop inserts | One completed reed-sharpening action, stop, four labels and separate request card. Result = classification/missing information, not counting. Hand contact may require separately reviewed insert art. |
| S08 / 116–131 s | Western gate → court → hall scribal bench | Same sentence as current task, quoted evidence and practice ink. Watch, court participants and apprentice are anonymous extra assets. |
| S09 / 131–151 s | Engineering slate | Eight equal-weight programmatic components. No seal/security icons; prose does not enforce permissions. |
| S10 / 151–166 s | Hall threshold → northern ford → village reprise, dawn | Corrective message, return riders and lowered lamps. Simurgh as carrier is still a staging inference and its form remains undecided. |
| S11 / 166–173 s | Hall ledger insert → neutral end card | Treat lamplit ledger as a recap insert, not a new night after the dawn ending. Series mark and takeaway are separate graphics. |

## Background package contract

For each set/view, deliver a directory with stable IDs matching the JSON plan:

```text
environments/<environment-id>/<view>/
  source/                  editable layers or layered vector source
  background.png           clean plate, no named characters or baked captions
  foreground.png           transparent occluders, when actually needed
  lighting/                reusable actual lighting/state variants
  layout.json              camera, horizon, ground and actor/prop anchor coordinates
  preview/                 actual composite with source art at proposed scale
  provenance.json          source authorship, tools, rights, reconstruction status
```

The first task delivers only one hall wide view and its editable source; other
directories are a contract for later tasks, not a claim they exist. If there is
no occluder, say none instead of inventing unnecessary layers.

Proposed reference frame is **1280×720**, with art at **1920×1080** or editable
vectors. In reference coordinates, reserve `[64,600,1152,104]` for captions and
keep the key action inside `[64,64,1152,512]`; proposed ground contact is `y=552`.
These are initial layout targets to validate on an actual composite, not frozen
approval. Move framing if the action/hand contact is obscured. Do not stretch
source character canvases to make them fit; human Simurgh stays `1087×1447`.

Keep distant architecture, midground furniture, interacting cast/props,
foreground occluders, effects and programmatic text as distinct compositing
layers. Do not paint the tablet twice or trap a movable ledger in the background.
Story labels and Persian/English captions must be rendered as text, with tested
shaping/RTL and font provenance, rather than generated lettering inside art.

Accept a view only after inspecting: source-character scale, perspective,
ground contact, prop reach, caption contrast, near/far occlusion, edge/alpha
quality, cross-shot floor-plan consistency and actual file/provenance completeness.
No background image, JSON flag or model score grants owner approval by itself.
