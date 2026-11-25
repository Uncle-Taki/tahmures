# Akvan Div blockout — candidate v02

Created directly in the live Blender 5.3 GUI session, with native MCP execution and dedicated local HTTP reference/viewport/save routes. Native project: `akvan_div_base_v02.blend`; v01 and pre-build session snapshot retained. Dedicated save produces a copy, so the GUI may still label its working session unsaved; independent reopening of both saved copies succeeded.

## Authority and preservation

APPROVED MEDIA ADAPTATION: Paper Puppet static master; owner explicitly selected its identity for this task. Repository source, supplied (2) copy and packed image independently match SHA256 47362a764bc38cce4e09ab022741a093a296fb69918344eb33bf6fa1829e6813. Original image unchanged. Archive extracted safely to /tmp/akvan-staging-msxcy4ib (293 entries); active work stayed in the real repository. Git root /home/mehdi/Project/leela/tahmures, main, commit 090e5acbab0bef37d89079a6400ffa0a29fab62d. Existing uncommitted integration edits and work-pack directories preserved.

CANON: Akvan Div, she/her, Keeper of Scripts. PROPOSAL: all 3D anatomy/depth, rear surfaces, topology and matte palette interpretation. No manuscript, continuity facts, episode timing, Persian edition, performance or existing media changed. See shot-contract-v01.md and 09_CONTINUITY_AUDIT.md.

## Scene and geometry

`CHAR_AkvanDiv` contains 01_Reference, 02_BaseMesh, 03_Armature, 04_StudioRig. Exactly six custom modular mesh objects in 02_BaseMesh:

- Akvan_Head_Headwear: 248 vertices / 190 faces
- Akvan_Eyes_Brows: 88 / 62
- Akvan_Torso_GarmentCore: 128 / 90
- Akvan_Arm_L: 160 / 107
- Akvan_Arm_R: 160 / 107
- Akvan_LowerGarment_Legs: 344 / 244

Total 1128 vertices, 800 faces. Custom extruded polygon garments/face/hair, ring-built horns and arms, shaped hands and shoes, inset ornaments; editable disconnected subassemblies within the six modules. Character faces -Y; shared world origin and identity object transforms; both mirrored feet touch Z=0, feet separated. No Akvan_Prop_Proxy, no duplicate character meshes in inspection scene. Original default scene and its cube/camera/light retained separately. Empty armature collection intentionally has zero bones/objects.

Six Principled matte materials, roughness 0.88: ochre, forest, rust, cream, charcoal, pale gold. Layered shoulders, sleeves, cuffs, skirt panels, edging, diamond ornaments, round shoulder fasteners. Packed front-orthographic locked image reference in 01_Reference, hidden in final inspection viewport to avoid obscuring the mesh; unhide it for comparison. Two orthographic cameras and three area lights; neutral world. Static frame 1, 24 FPS, Eevee, 800 x 1100 PNGs; no video/audio, so codec and animation duration are not applicable.

## Visual review

Inspected actual rendered front and three-quarter images. Corrected all-ochre material assignment, square-looking shoulder fasteners, and cluttered initial viewport. Front and three-quarter previews show full silhouette without clipping, symmetric lowered arms/hands, readable face/horns/hair, distinct garment layers and separated grounded footwear. Deliberately faceted blockout, without paper texture reproduction, sculpt detail or deformation-ready topology. Artistic likeness and unseen-depth interpretation still require owner review; no production/anatomy/rig approval claimed.

## Saved-file verification and tests

Independent Blender 5.3 background reopen of v02 passed all assertions in inspect_saved.py. Checked six meshes and exact collections, identity transforms, six shader slots per mesh, packed reference bytes/hash, two cameras, three lights, frame settings, empty rig collection, no prop, and no missing image dependencies. Evidence: saved-file-audit-v02.log and validation-v02.json. Front preview front_v01.png, three-quarter three_quarter_v01.png; bridge captures viewport_front_v01.png (historical cluttered capture) and viewport_front_clean_v01.png (corrected).

Full `make check PYTHON=.venv/bin/python` passed: 797 Python tests, Go tests, 82 bridge/integration tests, manuscript/continuity/translation/editorial checks, offline experiments, parity, and both strict documentation builds. Six existing Persian Agentها morphology warnings in chapter summaries were inspected and left unchanged because Persian editing is outside this task; editorial checks report zero errors. No commit or push.
