# Codex task: prepare Tahmures Chapter 01 for a controlled Google Flow 2D animation workflow

You are working **inside the existing Tahmures GitHub repository**. Your mission is to **implement a local, inspectable, upload-ready Google Flow production handoff**, using the repository's real narrative, character designs, production assets, approved audio, and media history. Also author an exceptionally practical, step-by-step Google Flow UI runbook that I can follow to make my episodic **2D animated series**. I have **Google AI Pro** and use Google Flow on desktop.

**This is a PREPARATION-ONLY task. Do not access, operate, or upload to Google Flow; do not call image, video, voice, or other paid provider APIs; do not spend AI credits. Do not commit, push, deploy, publish, remove or overwrite approved source files, or alter canonical manuscript material.** Work locally, run available validation, and report what you actually prepared.

Reading public Google support documentation is permitted. Opening an authenticated Flow project, changing account/project settings, creating remote Characters or instructions, and uploading assets are outside this task. All UI steps below are instructions for the owner to perform later. Preserve unrelated working-tree changes and limit edits to the new handoff and its supporting local files.

## A. Read and obey the project first

1. Read the repository's root and any relevant nested `AGENTS.md` files, then `meta-prompt.md`, `book/project-charter.md`, `book/narrative-continuity.md`, and the actual canonical English Chapter 01 narrative. The English manuscript is canonical for story facts; Persian media and translation have separate scopes.
2. Inspect `editorial/media-handoff/chapter-01-animation-status.json`, `editorial/media-handoff/chapter-01-animation-workflow.md`, and the selected active English production revision:
   `Characters/animations/chapter-01-candidate-01/production/english-final-03/`.
   Read its README, `timeline.json`, manifests, review/acceptance records, rebuild instructions, and its relevant `veo-consistency-agent-instructions.md` (locate the exact existing file rather than creating a conflicting replacement). Also search the current repository for newer scoped revisions/approvals; if they supersede these records, document the evidence and follow the legitimate active revision.
3. Inventory relevant assets and records under `Characters/tahmures/`, `Characters/environments/`, `Characters/animations/chapter-01-candidate-01/`, `Characters/godot-character-library-recovery-01/`, and `editorial/media-handoff/`. Include available art, design sheets, backgrounds, props, expression/turnaround references, animation stills, Godot exports, relevant audio/dialogue files, and provenance. Read relevant project-local `.agents/skills/` guidance when useful.
4. Preserve the approved distinction **Div-e Sefid is the messenger in the Chapter 01 animation; Chapar is a separate courier**. Never merge characters, swap their roles, invent canonical facts, or represent a media adaptation as manuscript canon. Respect other canonical identities, costume/color rules, locations, story objects, chronology, English/Persian distinctions, and scoped approvals.
5. The revision `english-final-03` is described in the supplied AGENTS.md as **technically verified, awaiting perceptual review and human lip-sync approval**. Verify its actual status. Filenames such as `final` do NOT prove artistic approval. Distinguish approved, candidate, historical, missing, and conflicting assets at every step.
6. I intend an **11-scene first episode**, but verify the actual repository's scene count and timeline. If they differ, do not change approved timing or force invented scenes; create an explicit discrepancy/decision note and a *proposed, clearly unapproved* 11-scene map only where supportable. Keep individual narrative scenes distinct from multiple short camera shots within each scene.
7. Study only the prompt-engineering book passages relevant to reliable instruction design, constraints, context packaging, consistency, evaluation, and iterative generation. Record the chapter/section sources. Do not copy all 24 chapters into the handoff or introduce competing story/continuity authorities.
8. Treat the current recorded English revision as the starting point, not as an approved finished film: its README describes *Ancient Tablet*, 251.3 seconds, 7539 frames at 30 fps, 1280×720, 34 approved voice recordings, and an independent title scene `T00`. Verify these against `timeline.json` and the source records. Report the title segment separately from the intended eleven narrative scenes; do not count `T00` as an invented twelfth narrative scene. Older 173-second planning and 197.5-second bilingual visual-build records must not replace the selected English timeline.
9. Resolve conflicting status notes with specific evidence: record the path, revision, date when recorded, hash when available, and approval scope. A later filename or modification timestamp alone does not supersede an owner decision. Preserve unresolved conflicts in the decision log rather than silently selecting the most convenient claim.

## B. Google Flow feature model (use as documented baseline, verify when possible)

The owner's reported screenshot labels are: project sidebar **All media, Videos, Characters, Scenes, Uploads, Library, Tools**; a bottom **Agent** toggle; a **Characters → New character** screen offering a prompt, Nano Banana image generation, **Upload**, and **Add from project**; and an **Agent instructions** pane with **Instruction title**, **Reference**, instructions text, **Add instruction**, and **Done**. The owner reports an existing instruction titled `# Tahmures — Veo visual consistency agent instructions`. **Reuse/reconcile existing instructions; do not install a competing style bible.** If the actual screenshots are unavailable, attribute these labels to the owner's description and do not claim to have inspected them. Even inspected screenshots do not establish that any character, voice, clip, or episode is approved or already created.

Google's official desktop documentation (check these as accessible; if offline, use this baseline and flag anything unverified):
- Agent and project instructions: https://support.google.com/flow/answer/17093911
- Create video, Frames, Ingredients, character `@` references, voices: https://support.google.com/flow/answer/16353334
- Create/edit images: https://support.google.com/flow/answer/16729550
- Characters, project assets, uploads, Collections: https://support.google.com/flow/answer/16935308
- Edit video, save frames, Scenebuilder: https://support.google.com/flow/answer/16935718
- Model-feature compatibility: https://support.google.com/flow/answer/16352836
- Create reusable custom Tools (optional; Google AI Pro can make them): https://support.google.com/flow/answer/17104535
- Introduction and subscription: https://support.google.com/flow/answer/16353333

Owner-provided feature baseline to verify against the official documentation before presenting it as current fact:
- Flow **Characters** supports **one or two reference images** per reusable identity, followed by naming and optional voice; use `@CharacterName` after I have actually created and named it in Flow. A file copied into the local folder is NOT automatically a Flow Character.
- **Ingredients** = reusable visual references (character/object/background); **Frames** = an explicit start image and optional end image that constrain a particular shot. Choose the workflow per shot rather than pretending they are identical.
- With the **Agent enabled**, its instructions can include a reference image plus project-wide text. Prefer separate compact instructions for art style, approved identities, environment/props, and shot discipline. Agent queries may have quotas; agent *media generation* consumes credits. Set **Confirm before generating → Always** so expensive actions require my confirmation.
- Model capabilities differ: Omni Flash supports frames, ingredients, and video-to-video editing; Veo 3.1 Lite supports frames/ingredients and certain extensions but not video-to-video editing; Veo 3.1 Fast and Quality have different restrictions (notably Quality cannot use Ingredients). Do not recommend an incompatible combination. Check available models/credit costs in the current UI before recommending a paid generation. Prefer low-cost **Omni 360p drafts** when suitable, then review/upscale selectively as available with Google AI Pro. Do not hard-code changing pricing as guaranteed.
- Flow **Scenes/Scenebuilder** can arrange, trim, preview, and download clips. Keep the master episode edit and audio integration reproducible outside Flow if necessary. **Tools** means optional reusable custom mini-apps, *not* a prerequisite for generating an episode.
- Flow-generated media is NOT automatically synchronized with the local GitHub repository. Specify manual download, import, naming, source-linking, and QA steps. No unsupported claims of Codex-to-Flow automation.

Record each material feature claim, official URL, access date, supported model/mode, plan restrictions, and verification status in `manifests/flow-feature-verification.md`. Distinguish documented capabilities from owner-reported UI labels and account-specific controls to check later. If documentation contradicts this baseline, use the documented capability and explain the difference. If unavailable or inconclusive, mark the claim UNVERIFIED and make the dependent instructions conditional. Do not invent click paths, reference limits, durations, audio-upload support, or model compatibility. Only recommend Omni 360p or another model/resolution after confirming the combination; otherwise name it as an option for the owner to verify. Never imply that an AI Pro subscription establishes a particular remaining balance or entitlement.

## C. Build a self-contained handoff INSIDE the active production area

Prefer a new non-destructive folder `Characters/animations/chapter-01-candidate-01/production/english-final-03/flow-handoff/` unless the repository has a clearly superior approved handoff location. If an existing handoff is present, preserve it, extend it carefully, and explain differences; never overwrite historical evidence or approvals. Make the following *logical outputs*, adjusting exact names to fit existing repo conventions:

```
flow-handoff/
  README.md                         # scope, quick start, what's ready vs missing
  context/
    CANONICAL_PRODUCTION_BRIEF.md   # sourced story/world/style/dialogue facts
    CONTINUITY_AND_APPROVALS.md     # canonical vs media adaptation vs candidate
    CHARACTER_BIBLE.md             # sourced identity reference summary, subordinate to canonical records
    ENVIRONMENTS_AND_PROPS.md      # reusable visual sources and scene assignments
  assets/
    upload-ready/
      characters/                  # approved/authorized reference IMAGE copies
      environments/
      props/
      storyboard-frames/           # only existing approved/authorized frames
    needs-review/                  # clearly quarantined nonapproved candidates
    contact-sheets/                # local comparison thumbnails, not new art
  agent-instructions/
    00_BOOTSTRAP_AGENT_PROMPT.md
    01_PROJECT_STYLE.md
    02_CHARACTER_IDENTITY.md
    03_ENVIRONMENT_AND_PROPS.md
    04_SHOT_AND_CONTINUITY_RULES.md
    05_AUDIO_AND_DIALOGUE_RULES.md
    EXISTING_INSTRUCTIONS_RECONCILIATION.md
  episode-01/
    SCENE_MAP.md
    scenes.csv
    scenes.json
    PROMPT_INDEX.md
    shots/S01_SH01.md             # repeat for the ACTUAL grounded shot inventory
    DIALOGUE_AND_AUDIO_MAP.md
    ASSEMBLY_TIMELINE.md
    SHOT_REVIEW_CHECKLIST.md
  guides/
    01_FLOW_PROJECT_SETUP.md
    02_IMPORT_ASSETS_AND_CREATE_CHARACTERS.md
    03_INSTALL_AGENT_INSTRUCTIONS.md
    04_STORYBOARD_AND_KEYFRAMES.md
    05_GENERATE_AND_REFINE_SHOTS.md
    06_VOICES_AUDIO_AND_LIPSYNC.md
    07_BUILD_SCENES_EXPORT_AND_REINTEGRATE.md
    08_REVIEW_FIXES_AND_NEXT_EPISODES.md
    DAILY_OPERATOR_CHECKLIST.md
  manifests/
    asset-manifest.json
    shot-to-asset-map.json
    approval-and-source-map.md
    missing-assets-and-decisions.md
    validation-report.md
    flow-feature-verification.md
    upload-batches.csv
    operator-log.csv               # blank log; actual credits/takes entered by owner
```

### Asset handling: physical folder suitable for manual Flow import

- Perform a broad inventory first; then select ONLY story-relevant reference assets. **Physically copy** eligible images into `assets/upload-ready/` (do not rely on symlinks that won't survive packaging). Keep original sources untouched. This folder should be immediately usable with Flow's **Upload** and **Add from project** functions.
- Create a machine-readable asset manifest for each collected image: stable ID, packaged relative path, original path, role, character/location/prop, shot usage, approval evidence/reference, approval scope, sha256, dimensions, format, alpha status, any derivatives, owner/rights/provenance if recorded, conflicts, and any missing information. Prefer original approved artwork; only make non-destructive technical conversions when necessary and note them. Do not infer approval from a clean file name or technical validity.
- Place potentially useful but unapproved images separately in `needs-review`, clearly named so I cannot mistake them for upload-ready masters. If approvals are ambiguous, *do not promote assets into upload-ready*. Record the blocker. Never invent replacement imagery or silently generate pictures.
- Produce annotated contact sheets/previews from existing files so I can select the right image. Preserve proportions, line art, transparency, identity details, and captions; clearly distinguish a contact sheet from an uploadable reference.
- Provide practical upload batches by character, environment, prop, and scene, plus a mapping of **exact local file → intended Google Flow location → when it is referenced**. Record which 1–2 images should initialize each Flow Character; keep full turnaround and expression sheets as supplementary references.
- Keep protected assets, private source materials, and unlicensed third-party media out of any upload-ready set unless authorized. Don't copy unnecessary manuscript/code files into an external-upload bundle.
- Track artistic approval, permission to prepare a reference, provenance/rights, and external-upload authorization as separate fields. This request authorizes local preparation of eligible production references, not an actual upload. A scoped head/pose approval does not approve a full-body derivative or newly extracted movie frame. Unknown eligibility belongs in `needs-review`; an empty upload-ready category is acceptable when supported by the evidence. Give the exact evidence needed to unblock each withheld asset.
- Contact sheets are local review derivatives, never identity masters or proof of approval. Use existing local image tooling only; retain source hashes and label every thumbnail's ID, source, and status. Do not extract new animation frames unless authorized by existing records; inventory existing captures first and record missing frames as blockers.

### Prompt engineering deliverables

- Create a **single derived 2D style contract for this handoff**, subordinate to the repository's canonical records and existing Veo consistency instructions, with line weight, color palette, shading, proportions, clothing, animation feel, environment style, camera, lighting, and negative constraints only if supported by approved art/records. Preserve the recorded softly shaded storybook style; do not impose cel shading if unsupported. No photorealism or 3D drift. Never claim a prompt guarantees identity preservation.
- Write **copy/paste-ready** Google Flow Agent instruction entries with title, body text, and **exact one best reference image path when appropriate**. Reconcile with the existing `veo-consistency-agent-instructions.md` and any on-screen `# Tahmures — Veo visual consistency agent instructions` entry; state what to keep, update, or avoid duplicating.
- Write a short **Flow Agent bootstrap message** that makes it assist with *one planned scene* and explicitly **not generate/spend credits until I approve**. Avoid feeding entire books or enormous unstructured prompts into Flow.
- Generate a shot card for every grounded shot (not merely one vague prompt for each narrative scene), including: immutable scene/shot ID; canonical source citation/path; dramatic objective and allowed cast; approved assets and Flow `@` identities; exact composition/start/end frames when available; camera position/motion; one primary character action; duration compatible with chosen Flow model; dialogue and speaker attribution; sound plan; plain-English copy/paste generation prompt; prohibited visual changes; expected last-frame continuity; recommended model and mode with feature justification; retries/fixes; acceptance gates; and final filename.
- Build explicit multi-shot coverage for a scene only when justified by narrative and production records. Use scene timeline durations and propose shot lengths without altering the canonical timing. If a required image or approval is missing, mark the prompt BLOCKED or PROVISIONAL, never disguise a guess as a finished instruction.
- For each shot, distinguish its source timeline interval, proposed generated clip duration, and proposed retained edit interval. Explain handles, splits, and joins where a scene exceeds a model's verified duration limit. Preserve source scene boundaries and approved recording bytes; do not speed speech, rewrite dialogue, or stretch approved timing to fit a generation preset. Mark newly proposed coverage as unapproved rather than implying that it exists in the production timeline.
- For episodic scale, provide conventions for reusable character IDs, reference versioning, recurring locations, season-to-season continuity, clip IDs, prompts, review status, and change logs. Keep story facts and media adaptation approvals separate.

## D. Make the runbook truly executable by a human in my Flow UI

Each guide must give **numbered click-by-click steps**, expected on-screen result, which local file(s) to select, which prompt to paste, what to verify, and how to recover from common problems. Use my screenshot's desktop labels wherever grounded; mark differences across UI versions rather than inventing controls. Cover all of these:

1. Open/create/rename a Flow project for the selected English Chapter 01 revision, whose final picture approval remains pending; set output orientation where the verified UI supports it, confirm-before-generation, media organization, and naming conventions. Explain Google AI Pro credit awareness.
2. Import images from `assets/upload-ready` through **Uploads**; verify upload success; create Flow **Characters** from the approved 1–2 images; name each character precisely; add or omit voice per approval; use `@CharacterName` only after it exists. Explain **Add from project**.
3. Open **Agent** and **Agent instructions → Add instruction**; paste separated instruction entries, attach each reference, click **Done**, avoid contradictory instructions, and verify the existing Tahmures rule remains intact. Explain the difference between Agent instructions and per-shot text prompts.
4. Generate or place storyboard/keyframes: use existing approved images first; for gaps, provide *proposed* Nano Banana image prompts that I can review and optionally run in Flow. Codex must not generate any new artwork itself. Indicate which frames need owner approval before animation.
5. Choose **Video → Frames** for shots with a locked start/end composition, and **Video → Ingredients** for reusable visual references; use compatible Omni/Veo models; specify conservative output count, length, resolution, and how to verify credit cost. Pilot ONE representative dialogue/character/action shot before mass production.
6. Generate, inspect, and iterate shots for 2D consistency, anatomy, facial identity, clothing, props, floor contact, lip sync, timing, shot boundaries, occlusion, and audio. Use saved still frames as later start/end references where useful. For editing, explain Omni's video-to-video workflow and Veo-specific extension limitations; do not promise unsupported features.
7. Prefer existing approved recordings for characters/dialogue. Document exact input audio filenames and timeline mapping; show a safe fallback for separately editing/mixing audio and subtitles. Do not create new voices/recordings or claim automatic mouth alignment is approved; identify owner signoff requirements for voice and lip sync.
8. Add clips to **Scenes/Scenebuilder**, arrange and trim, preview, export; preserve original versions. Map local downloaded files back to shot IDs and production manifests, and give editor handoff instructions if full-episode audio assembly needs another editor.
9. Provide explicit quality gates after character registration, pilot scene, each shot, each scene, episode assembly, and English final review. Include what to do if Flow drifts toward 3D, changes costume/face, swaps Chapar and Div-e Sefid, changes character count, invents dialogue, or fails to sync lips.
10. Explain **Library/Collections** for organizing assets and **Tools** as optional Google AI Pro custom helpers. If a reusable tool is useful, provide an *optional tool-design prompt only* (e.g., a reference/shot consistency checklist); do not build one remotely or make it mandatory.
11. Provide a **one-page daily operator checklist** to follow as I work scene by scene, recording clip status, actual credit spend, chosen take, and outstanding approvals.

Keep approved audio local unless an explicitly supported and authorized upload workflow is established. Do not treat Flow's optional character voice as an import of an existing recording, a matching voice identity, or a lip-sync guarantee. When exact approved speech cannot be preserved in Flow, plan picture-only generation and external editing against the original recordings; generated speech remains an unapproved candidate and must not replace the approved tracks.

## E. Verification and handoff

- Create or reuse local scripts only if helpful for safe offline asset inventory, hash/dimension validation, missing-path detection, manifest/schema checking, contact sheets, and shot mapping. Do not add runtime dependencies without good reason; use existing project tooling where possible.
- Inspect scoped media commands before running them. Run only checks that preserve existing production sources, captures, movies, packages, and approval records; direct any new handoff-validation output into the handoff. Do not run build, render, assemble, packaging, or review-generation commands merely because the README lists them. Where a check would rebuild or overwrite production outputs, record it as deferred with its reason. Run the repository gate `make check PYTHON=.venv/bin/python` if feasible, but explain that it does **not** validate artistic quality, Godot output, or final lip sync. Do not claim commands passed unless run to completion with an observed exit status; capture results and any environment blockers. Do not rerender or modify the existing animation.
- Audit every `upload-ready` file exists, can be opened, is documented in the manifest, has an identified original source, and has appropriate approval/rights. Audit every shot's references to valid files and characters; flag unsupported or unresolved material and any scene-count discrepancy.
- Record expected Flow Character names as `not_registered` until the owner creates them; local validation can verify the naming plan, not remote registration. Validate relative package paths, unique asset/shot IDs, copied-byte hashes, source existence, approval evidence links, scene coverage, shot interval arithmetic, and audio cue coverage. Distinguish existing artifacts from proposed instructions in every machine-readable report. Add a dated source snapshot so later operators can detect stale references without treating the handoff as a new source of truth.
- In your final Codex reply, show: exact created/changed file paths; a 10-line quick start; number of canonical scenes/derived shots; counts of upload-ready versus needs-review assets; missing approvals and decisions; validation commands/results; an explicit **NO external generation/upload/commit/push performed** statement; and the recommended first pilot scene/shot with rationale.

**Do the audit and create the actual handoff files now. Do not stop after proposing a plan, and do not ask me for information already present in the repository. When information is genuinely missing, deliver the supported partial artifacts and record specific blockers instead of inventing facts.**
