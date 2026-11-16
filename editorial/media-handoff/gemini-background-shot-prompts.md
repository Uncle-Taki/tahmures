# Chapter 01 — Gemini / Nano Banana background shot prompts

Prepared 2026-10-20. **25 image requests + 2 programmatic stages.**
Continuation: all 25 candidate image files now exist in the local environment
library; no owner approval is recorded. These cards preserve the requested
designs for reproduction and targeted revisions, not a claim that generation is
still pending. The two code-native stages are blank backgrounds only.
This covers Chapter 01's current plan, not Chapters 02–24. All architecture and camera choices are proposed project-fiction staging (`TIER_C_PROJECT_FICTION`).

Start with [the master prompt](gemini-background-master-prompt.md). These shot cards refine the [environment brief](chapter-01-environment-brief.md); the [JSON queue](gemini-background-queue.json) records IDs, dependencies and honest empty delivery fields.

## How to use

1. Attach the three actual source-art PNGs named in the master. Paste the master and the BG-HALL-00 card. Select a hall master before dependent shots.
2. For each next ID, attach its **actual selected reference image(s)** and paste its card. A filename in text does not provide image access. Reference IDs below are dependencies, not claims that the images already exist.
3. In an existing directed chat, paste only the target card. In a fresh/direct Nano Banana chat, paste the common prefix below **plus the target card**, and attach source-art/set references. Attach the full master too when possible.
4. Download each original full-size result. Suggested `.png` names assume an actual PNG export; preserve the original format if different and convert locally later. Keep originals/revisions distinct. When returning files to Codex, include their IDs, actual model and selected revision; Codex measures dimensions/hashes and checks composites. Flat image candidates do not satisfy the full editable-layer package contract.

## Common prefix for a fresh image chat

```text
Generate the actual single clean background plate described below, with the attached character images used only for style and scale. Warm hand-drawn 2D storybook animation, dark organic outlines, restrained cel shading, tactile plaster/cedar/stone and large readable forms. Match the selected set anchor. Landscape 16:9, full frame, highest useful native resolution offered, no collage or border. Empty set: no people, divs, birds, horses, faces, character shadows, handled story props, readable writing, captions, numbers, logo, UI, guides, live fire, moving smoke or falling rain. No removed decorative door/handle motif; an ordinary functional entrance and the story's western gate are allowed. Keep the lower subtitle zone visually quiet. Wide/medium shots should leave an open acting floor and support foot contact near y=552 in 1280x720 reference space; detail inserts use their own camera scale. Return the image with ID, actual tool/dimensions if known and candidate status, without claiming approval or repository access.
```

## Image queue

| Order | ID | View / light | Scenes | Selected references needed |
|---|---|---|---|---|
| 1 | BG-HALL-00 | wide / morning | Master only | Character art |
| 2 | BG-HALL-01 | wide / dawn | CH01-S01 | BG-HALL-00 |
| 3 | BG-HALL-02 | intake / wet_morning | CH01-S02 | BG-HALL-00 |
| 4 | BG-HALL-03 | cedar_stand / morning | CH01-S03 | BG-HALL-00 |
| 5 | BG-HALL-04 | catalogue / morning | CH01-S04 | BG-HALL-00 |
| 6 | BG-HALL-05 | intake / morning | CH01-S04 | BG-HALL-00, BG-HALL-02 |
| 7 | BG-HALL-06 | threshold / morning | CH01-S04 | BG-HALL-00, BG-HALL-02 |
| 8 | BG-HALL-07 | worktable / dusk | CH01-S05 | BG-HALL-00 |
| 9 | BG-HALL-08 | worktable / lamplight | CH01-S07, CH01-S11 | BG-HALL-00, BG-HALL-07 |
| 10 | BG-HALL-09 | scribal_bench / morning | CH01-S08 | BG-HALL-00 |
| 11 | BG-HALL-10 | threshold / dawn | CH01-S10 | BG-HALL-00, BG-HALL-06 |
| 12 | BG-POST-01 | delivery / night | CH01-S06 | BG-HALL-00 |
| 13 | BG-POST-02 | rider_departure / night | CH01-S06 | BG-HALL-00, BG-POST-01 |
| 14 | BG-VILLAGE-A-NIGHT | village_wide / night_alarm | CH01-S06 | BG-HALL-00 |
| 15 | BG-VILLAGE-B-NIGHT | village_wide / night_alarm | CH01-S06 | BG-HALL-00, BG-VILLAGE-A-NIGHT |
| 16 | BG-VILLAGE-C-NIGHT | village_wide / night_alarm | CH01-S06 | BG-HALL-00, BG-VILLAGE-A-NIGHT |
| 17 | BG-VILLAGE-A-DAWN | village_wide / dawn_calm | CH01-S10 | BG-VILLAGE-A-NIGHT |
| 18 | BG-VILLAGE-B-DAWN | village_wide / dawn_calm | CH01-S10 | BG-VILLAGE-B-NIGHT |
| 19 | BG-VILLAGE-C-DAWN | village_wide / dawn_calm | CH01-S10 | BG-VILLAGE-C-NIGHT |
| 20 | BG-CAMP-01 | camp_wide / night | CH01-S06 | BG-HALL-00 |
| 21 | BG-CAMP-02 | fire_insert / night | CH01-S06 | BG-CAMP-01 |
| 22 | BG-GATE-01 | gate_and_watch / day | CH01-S08 | BG-HALL-00 |
| 23 | BG-COURT-01 | evidence_table / day | CH01-S08 | BG-HALL-00 |
| 24 | BG-FORD-01 | road / dawn | CH01-S10 | BG-HALL-00, BG-VILLAGE-A-NIGHT |
| 25 | BG-FORD-02 | ford_return / dawn | CH01-S10 | BG-FORD-01 |

## Individual copy/paste cards

### BG-HALL-00 — Hall master — geometry and style anchor

```text
ID: BG-HALL-00
Suggested filename: bg-hall-00.png
Set/view/light: ENV-HALL / wide / morning
Scene use: Reference anchor, not an additional scene
Attach actual selected images: source character art.

Generate one empty Hall of Scripts master plate in neutral morning light, wide eye-level three-quarter view. Show a modest working hall with warm plaster, cedar furniture, stone or packed-earth flooring and restrained bronze fittings. Place one functional entrance and the intake zone screen-left; keep a broad open central acting floor; place the cedar display stand slightly deeper, catalogue shelves along the right/back wall, a worktable nearby and a quiet scribal bench at the side. High daylight enters from screen-left. Use blank stored clay, leather, bark and silk materials sparingly on shelves to establish the hall's work, without readable marks. The furniture has plausible human scale; the stand and worktable do not form a continuous foreground barrier. Keep the bottom caption area quiet. Match the attached character art without painting any characters. This image proposes the room layout; return only this master first so I can select it before related views.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-HALL-01 — Hall wide — dawn opening

```text
ID: BG-HALL-01
Suggested filename: bg-hall-01.png
Set/view/light: ENV-HALL / wide / dawn
Scene use: CH01-S01
Attach actual selected images: source character art; BG-HALL-00.

Edit the selected BG-HALL-00 master into the dawn establishing plate. Preserve its camera, room footprint, architecture, furniture, shelf arrangement and open acting floor. Use soft early golden light from the established high left-side openings with cool residual interior shadows. Keep the room legible and welcoming, rather than a dramatic palace. Leave space for incoming message materials and Shahrasp's reading action as separate assets. Do not add the messages being handled, crystal, ledger or people. Keep the subtitle zone unobtrusive.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-HALL-02 — Intake — wet morning

```text
ID: BG-HALL-02
Suggested filename: bg-hall-02.png
Set/view/light: ENV-HALL / intake / wet_morning
Scene use: CH01-S02
Attach actual selected images: source character art; BG-HALL-00.

Make a medium-wide view of the same hall's entrance/intake zone. Keep the entrance on the established side, with a modest static intake table off-centre and a clear standing/handoff area beside it. The tabletop must be visible enough for a found tablet to be added later. Light is overcast cool grey from outside, with a small damp patch near the threshold; suggest wet weather through surfaces and light, with no falling rain. Preserve the master's architecture, materials and furniture designs. Show no courier, receiver, tablet, packet, cord or seal trace. Avoid foreground furniture hiding the handoff.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-HALL-03 — Cedar stand — three recipients

```text
ID: BG-HALL-03
Suggested filename: bg-hall-03.png
Set/view/light: ENV-HALL / cedar_stand / morning
Scene use: CH01-S03
Attach actual selected images: source character art; BG-HALL-00.

Frame the established cedar stand and the open floor around it in a medium-wide eye-level three-quarter view of the same hall. The empty stand is low and modest, offset enough to leave natural positions for Tahmures and three recipients, with their body silhouettes and access to the stand unobscured. Keep the stand's top visible for a separate tablet. Morning light comes from the same high left-side source. Retain recognisable catalogue/worktable landmarks in the appropriate background direction. No throne, grand dais, people, tablet, lens, crystal or cord.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-HALL-04 — Catalogue — record interpretation

```text
ID: BG-HALL-04
Suggested filename: bg-hall-04.png
Set/view/light: ENV-HALL / catalogue / morning
Scene use: CH01-S04
Attach actual selected images: source character art; BG-HALL-00.

Show the hall's established catalogue wall in a medium shot, retaining the same shelf design, neighbouring worktable relationship and morning light direction. Use a small number of large readable shelf shapes, with stored blank clay records and folded materials; no script, invented language or category labels. Leave a clear working position beside the shelving and a visible empty placement surface for later catalogue action. The acting area should suit the supplied front/three-quarter character poses. Do not paint Akvan, the found tablet, an open catalogue book or written labels.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-HALL-05 — Intake — wrapping interpretation

```text
ID: BG-HALL-05
Suggested filename: bg-hall-05.png
Set/view/light: ENV-HALL / intake / morning
Scene use: CH01-S04
Attach actual selected images: source character art; BG-HALL-00, BG-HALL-02.

Edit the selected BG-HALL-02 intake plate into ordinary morning light. Preserve exactly the same camera, table, doorway, architecture and handoff floor. Replace overcast exterior illumination with the hall's established soft morning daylight; reduce the wet-weather cue without redesigning the floor. Keep the tabletop empty for the oilcloth-wrapping action to be composited. No Simurgh, tablet, cloth, packet, readable writing or added furnishings.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-HALL-06 — Threshold — departure

```text
ID: BG-HALL-06
Suggested filename: bg-hall-06.png
Set/view/light: ENV-HALL / threshold / morning
Scene use: CH01-S04
Attach actual selected images: source character art; BG-HALL-00, BG-HALL-02.

Show the hall's one functional entrance from just inside, with enough hall landmarks to recognise the same intake side and enough exterior path visible to read a departure later. Use an eye-level medium-wide camera and morning light consistent with the hall master. Keep a clear continuous floor/path near the proposed sprite ground line. This is an ordinary entrance, without ornate handles, repeated doorways or portal symbolism. No Black Div, footprints implying an unseen actor, tablet or packet. Keep all later movement space empty.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-HALL-07 — Worktable — dusk report

```text
ID: BG-HALL-07
Suggested filename: bg-hall-07.png
Set/view/light: ENV-HALL / worktable / dusk
Scene use: CH01-S05
Attach actual selected images: source character art; BG-HALL-00.

Show the established hall worktable from a medium-wide eye-level three-quarter camera, with an empty work surface and clear floor positions for two or more speakers beside it. Keep the same catalogue wall and entrance relationship as the master. Dusk light from the established windows is cool blue, softened by restrained warm reflected interior tones. Maintain facial readability for characters to be added later; this is a misunderstanding, not a villain's lair. Keep the table off-centre and prevent it hiding all full-body sprites. No people, wet garments, tablet, ledger, cards or active flames.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-HALL-08 — Worktable — lamplight and recap

```text
ID: BG-HALL-08
Suggested filename: bg-hall-08.png
Set/view/light: ENV-HALL / worktable / lamplight
Scene use: CH01-S07, CH01-S11
Attach actual selected images: source character art; BG-HALL-00, BG-HALL-07.

Edit selected BG-HALL-07 into its lamplit version. Lock camera, geometry, table, catalogue shelves and empty actor positions. Use warm illumination from a modest fixed oil-lamp fixture, with cool dim surroundings; the lamp housing may be visible but its animated flame is omitted. Keep the tabletop clear and evenly readable for later reed, ledger, four labels and separate request card. These objects and their text must not appear in this plate. The same image supports S07 and a later editorial recap insert in S11; do not introduce evidence of another later night.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-HALL-09 — Scribal bench — practice context

```text
ID: BG-HALL-09
Suggested filename: bg-hall-09.png
Set/view/light: ENV-HALL / scribal_bench / morning
Scene use: CH01-S08
Attach actual selected images: source character art; BG-HALL-00.

Create a medium view of the quiet scribal bench already established at the side of the hall. Preserve the master room, furniture materials, daylight direction and scale. A plain empty bench/work surface and an unobtrusive wall or shelf establish a working apprenticeship space. Leave a clear seated/standing action position and accessible tabletop for separate apprentice and practice-sheet assets. Do not add another room, pupil, hand, reed, inked words, loose practice sheet or modern school equipment. Morning lighting, calm and visually restrained.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-HALL-10 — Threshold — corrective-message dawn

```text
ID: BG-HALL-10
Suggested filename: bg-hall-10.png
Set/view/light: ENV-HALL / threshold / dawn
Scene use: CH01-S10
Attach actual selected images: source character art; BG-HALL-00, BG-HALL-06.

Edit selected BG-HALL-06 threshold plate to dawn. Retain the exact entrance, camera, interior/exterior geometry and clear transfer floor. Use a fresh warm sunrise outside with cool quiet interior shadows; the scene should support a corrective message leaving the hall. Do not add a messenger in any form, bird, packet, seal, message text or people. Do not decide whether Simurgh is human or bird; the clean set is independent of that later casting decision.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-POST-01 — Frontier post — arrival and delivery

```text
ID: BG-POST-01
Suggested filename: bg-post-01.png
Set/view/light: ENV-POST / delivery / night
Scene use: CH01-S06
Attach actual selected images: source character art; BG-HALL-00.

Create an empty modest northern frontier relay/watch post courtyard at night, matching the selected hall's illustrated materials and line treatment, without copying its floor plan. Low plaster/stone walls, a simple shelter and a fixed lamp fixture define an occupational outpost, not a castle or army camp. Leave an unobstructed foreground handoff area between a readable arrival path on screen-left and an open departure track toward screen-right/back. A low static counter may sit to one side without hiding the handoff. Cool night light plus restrained warm fixture illumination. No messenger, captain, horse, soldiers, packet, live flames, smoke, invading army or threat silhouettes.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-POST-02 — Frontier post — dispatch exit

```text
ID: BG-POST-02
Suggested filename: bg-post-02.png
Set/view/light: ENV-POST / rider_departure / night
Scene use: CH01-S06
Attach actual selected images: source character art; BG-HALL-00, BG-POST-01.

Reframe the selected BG-POST-01 post toward its departure track, maintaining the same buildings, gate opening, track direction, materials and night lighting. The empty track must provide plausible scale and unobstructed room for riders/horses to be composited moving away. Keep a recognisable part of the delivery courtyard as the reverse landmark, so delivery and dispatch read as one place. No riders, animals, hoof dust, motion streaks, army, alarm banners or written orders. This is the dispatch location following delivery, not a depiction of an attack.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-VILLAGE-A-NIGHT — Village A — night alarm clean set

```text
ID: BG-VILLAGE-A-NIGHT
Suggested filename: bg-village-a-night.png
Set/view/light: ENV-VILLAGE / village_wide / night_alarm
Scene use: CH01-S06
Attach actual selected images: source character art; BG-HALL-00.

Create village A as a distinct location within the shared northern-frontier architectural kit. A small plaster-and-stone cluster beside low terraced fields, with a plain square well toward one side and a wide open foreground path. Match the hall's warm hand-drawn outlines, tactile restrained materials and simple shaded forms. Wide eye-level composition, quiet cool night and small warm window glows; keep homes and path legible rather than horror-dark. Provide open ground for villagers and handheld lamps to be added, with a quiet caption strip. The alarm will be shown by animation, not damage in the scenery. No people, animals, fire, moving smoke, attackers, burning roofs, weapons, flags, signs or readable text. 

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-VILLAGE-B-NIGHT — Village B — night alarm clean set

```text
ID: BG-VILLAGE-B-NIGHT
Suggested filename: bg-village-b-night.png
Set/view/light: ENV-VILLAGE / village_wide / night_alarm
Scene use: CH01-S06
Attach actual selected images: source character art; BG-HALL-00, BG-VILLAGE-A-NIGHT.

Create village B as a distinct location within the shared northern-frontier architectural kit. A distinct village on a shallow hillside, with a short low retaining wall, stepped roof silhouettes and a clear gently sloping approach; no dangerous cliff. Match the hall's warm hand-drawn outlines, tactile restrained materials and simple shaded forms. Wide eye-level composition, quiet cool night and small warm window glows; keep homes and path legible rather than horror-dark. Provide open ground for villagers and handheld lamps to be added, with a quiet caption strip. The alarm will be shown by animation, not damage in the scenery. No people, animals, fire, moving smoke, attackers, burning roofs, weapons, flags, signs or readable text. Share materials and scale with village A, but do not duplicate its layout or landmarks.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-VILLAGE-C-NIGHT — Village C — night alarm clean set

```text
ID: BG-VILLAGE-C-NIGHT
Suggested filename: bg-village-c-night.png
Set/view/light: ENV-VILLAGE / village_wide / night_alarm
Scene use: CH01-S06
Attach actual selected images: source character art; BG-HALL-00, BG-VILLAGE-A-NIGHT.

Create village C as a distinct location within the shared northern-frontier architectural kit. A distinct village beside an orchard edge, with a low woven fence, a few simple homes and a broad open lane; no river crossing in this set. Match the hall's warm hand-drawn outlines, tactile restrained materials and simple shaded forms. Wide eye-level composition, quiet cool night and small warm window glows; keep homes and path legible rather than horror-dark. Provide open ground for villagers and handheld lamps to be added, with a quiet caption strip. The alarm will be shown by animation, not damage in the scenery. No people, animals, fire, moving smoke, attackers, burning roofs, weapons, flags, signs or readable text. Share materials and scale with village A, but do not duplicate its layout or landmarks.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-VILLAGE-A-DAWN — Village A — dawn calm reprise

```text
ID: BG-VILLAGE-A-DAWN
Suggested filename: bg-village-a-dawn.png
Set/view/light: ENV-VILLAGE / village_wide / dawn_calm
Scene use: CH01-S10
Attach actual selected images: source character art; BG-VILLAGE-A-NIGHT.

Edit the selected BG-VILLAGE-A-NIGHT into the dawn-calm reprise of that exact village. Keep its camera, horizon, homes, all landmarks, path width and foreground geometry unchanged. Replace cool night with gentle dawn light, warm near the horizon and soft cool shadows; reduce window glow naturally. Calm comes from light and later performance, not newly added objects. Leave all actor positions empty for villagers lowering separate lamps. No people, lamps held by invisible hands, animals, new buildings, smoke, damage, text or changed season.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-VILLAGE-B-DAWN — Village B — dawn calm reprise

```text
ID: BG-VILLAGE-B-DAWN
Suggested filename: bg-village-b-dawn.png
Set/view/light: ENV-VILLAGE / village_wide / dawn_calm
Scene use: CH01-S10
Attach actual selected images: source character art; BG-VILLAGE-B-NIGHT.

Edit the selected BG-VILLAGE-B-NIGHT into the dawn-calm reprise of that exact village. Keep its camera, horizon, homes, all landmarks, path width and foreground geometry unchanged. Replace cool night with gentle dawn light, warm near the horizon and soft cool shadows; reduce window glow naturally. Calm comes from light and later performance, not newly added objects. Leave all actor positions empty for villagers lowering separate lamps. No people, lamps held by invisible hands, animals, new buildings, smoke, damage, text or changed season.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-VILLAGE-C-DAWN — Village C — dawn calm reprise

```text
ID: BG-VILLAGE-C-DAWN
Suggested filename: bg-village-c-dawn.png
Set/view/light: ENV-VILLAGE / village_wide / dawn_calm
Scene use: CH01-S10
Attach actual selected images: source character art; BG-VILLAGE-C-NIGHT.

Edit the selected BG-VILLAGE-C-NIGHT into the dawn-calm reprise of that exact village. Keep its camera, horizon, homes, all landmarks, path width and foreground geometry unchanged. Replace cool night with gentle dawn light, warm near the horizon and soft cool shadows; reduce window glow naturally. Calm comes from light and later performance, not newly added objects. Leave all actor positions empty for villagers lowering separate lamps. No people, lamps held by invisible hands, animals, new buildings, smoke, damage, text or changed season.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-CAMP-01 — Charcoal camp — calm wide

```text
ID: BG-CAMP-01
Suggested filename: bg-camp-01.png
Set/view/light: ENV-CAMP / camp_wide / night
Scene use: CH01-S06
Attach actual selected images: source character art; BG-HALL-00.

Create a wide empty charcoal-burners' work clearing at night beyond the frontier, matching the same illustrated world. Show a restrained woodland edge, earth ground, a few stable timber/log stacks and simple occupational shelters or charcoal-making structures around the sides. Leave a broad central/midground clearing with enough separated space for eleven small scene-controlled fire effects and charcoal burners to be added later; do not attempt to paint or count the fire instances. The empty clearing should remain readable in soft cool ambient night light. No military formations, watchtowers implying a new threat, live flames, glow pools from missing fires, smoke, embers, people or animals.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-CAMP-02 — Charcoal camp — fire-site insert

```text
ID: BG-CAMP-02
Suggested filename: bg-camp-02.png
Set/view/light: ENV-CAMP / fire_insert / night
Scene use: CH01-S06
Attach actual selected images: source character art; BG-CAMP-01.

Make a closer ground-level insert within the selected BG-CAMP-01 clearing: a bare earth/stone work patch with static fuel wood or a charcoal mound at the edge and a quiet camp context beyond. Preserve the same materials, night exposure and location identity. Leave a central clear place for a separate small occupational fire/smoke effect. No visible flame, smoke, embers, person, hand or new threat. This is a detail camera for a possible camp insert; do not force the full-body character ground-line convention onto this close view.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-GATE-01 — Western gate — current-task context

```text
ID: BG-GATE-01
Suggested filename: bg-gate-01.png
Set/view/light: ENV-GATE / gate_and_watch / day
Scene use: CH01-S08
Attach actual selected images: source character art; BG-HALL-00.

Create an empty functional western settlement gate setting in daylight, in the same modest plaster/stone and cedar architectural language as the hall. Show one sturdy ordinary opening with permanent gateposts, hinge recesses, an adjacent watch position and clear swing space. Omit the movable timber gate leaves: a separate matching animated gate asset will be added later. Use eye-level three-quarter framing with an open actor area beside the opening for a watch member. Keep the opening and wall geometry simple enough for that separate gate asset to align. No guards, weapons display, command tablets, banners, written words, decorative door collections or fantasy portal effects.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-COURT-01 — Court — evidence context

```text
ID: BG-COURT-01
Suggested filename: bg-court-01.png
Set/view/light: ENV-COURT / evidence_table / day
Scene use: CH01-S08
Attach actual selected images: source character art; BG-HALL-00.

Create a modest empty ancient-world hearing courtyard or chamber, consistent with the hall's materials but identifiable as a different place. A low plain exhibit table offset from centre, a few restrained fixed benches and a quiet plaster backdrop establish a place for examining evidence. Daylight, eye-level medium-wide perspective, space for separate participants without the table hiding every body. The exhibit surface is empty for a quoted-sentence document to be added. No people, judge statue, scales-of-justice icon, gavel, throne, readable words, evidence tablet, modern legal equipment or magical seal.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-FORD-01 — Northern road — dawn geography anchor

```text
ID: BG-FORD-01
Suggested filename: bg-ford-01.png
Set/view/light: ENV-FORD / road / dawn
Scene use: CH01-S10
Attach actual selected images: source character art; BG-HALL-00, BG-VILLAGE-A-NIGHT.

Create a wide empty northern road at dawn approaching a shallow, broad ford through low hills. Use the same modest rural landscape and material rendering as the village kit. Establish a readable road direction, near bank and distant crossing that can support a closer return view next. Soft fresh sunrise, quiet terrain, plausible horse travel and a caption-safe foreground. No people, riders, animals, cart, written waymarkers, dramatic storm, deep gorge, broken bridge or drowning incident. The water surface is still, with no animated splashes.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

### BG-FORD-02 — Ford — riders return

```text
ID: BG-FORD-02
Suggested filename: bg-ford-02.png
Set/view/light: ENV-FORD / ford_return / dawn
Scene use: CH01-S10
Attach actual selected images: source character art; BG-FORD-01.

Reframe the selected BG-FORD-01 landscape closer to its shallow crossing, preserving the same hills, banks, road direction and dawn light. Show a legible gentle ford, with a clear route from the far bank toward the near return road and enough lateral space for riders/horses to be composited. Keep shallow water and firm banks readable; no sudden waterfall, dangerous depth, new bridge or water crisis. Use quiet static water, no riders, horses, villagers, splashes, wake trails or motion blur. The return action is a later foreground layer.

Apply the master/common clean-plate rules. Return one actual image, not a contact sheet or completion JSON. Status: candidate_needs_review.
```

## Two code-native stages — do not spend image requests on these

### BG-OVERLAY-01 — slate

Use: CH01-S09. Method: Godot Control nodes or editable SVG; not image generation.

Create a clean flat dark-slate stage from code, palette chosen after actual plate/character review. Add the eight request-envelope components as equal-weight editable text/chips in a later graphics layer. Keep bilingual text exact and Persian shaping tested. No seal/security icon, computer-screen picture or implied authority hierarchy.

### BG-OVERLAY-02 — end_card

Use: CH01-S11. Method: Godot Control nodes or editable SVG; not image generation.

Reuse the neutral programmatic stage for the takeaway and series end card. Add the reviewed exact text and separate clay-tablet/reed series mark as editable graphics. No generated lettering, painted UI, new story room or implied later-night establishing scene.

## Review and resuming

After downloading, check the image rather than its delivery note: source-art compatibility, empty actor space, table reach, caption contrast, stable room geometry and lighting, no baked movable props/text/effects, correct village identity and night/dawn pairing. Review count-critical fire instances later in Godot. A lamplit S11 reuse is a recap, not a chronological new night.

If interrupted, tell Gemini: “Resume at [next ID]. These attached images are my selected references: [IDs]. Use that card, generate one actual plate, then report its ID.” Keep downloaded outputs as the evidence; do not accept a model's list of allegedly completed images.
