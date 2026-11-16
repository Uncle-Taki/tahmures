"""NOT APPROVED FOR PRODUCTION / NOT AUTHORIZED FOR FLOW GENERATION.

Derive a separate candidate handoff after the story/red-team stages. No source
or existing handoff mutation, no remote execution, no media generation.
"""
import copy
import csv
import hashlib
import json
import shutil

from build_story import WORK, ROOT, PROD, OFFICIAL, FLOW, GATE, read, md, js, csvwrite


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    if not (WORK/'10_STORY_RED_TEAM.md').is_file():
        raise RuntimeError('Independent story review must precede synchronization')
    story=read(WORK/'candidate-story.json'); changes=story['changes']
    intent={s['id']:s for s in story['scenes']}
    dialogue=read(WORK/'dialogue-candidate.json')
    timeline=read(PROD/'timeline.json')
    original_shots=read(OFFICIAL/'manifests/shot-to-asset-map.json')['shots']
    original_assets=read(OFFICIAL/'manifests/asset-manifest.json')['assets']
    with (WORK/'06_PUNCH_MAP.csv').open() as stream:
        punch_ids={row['beat_id'] for row in csv.DictReader(stream)}
    # Only the two scoped-accepted reference bytes are copied. The enclosing
    # candidate package cannot itself authorize their upload or performance.
    assets=[]
    for original in original_assets:
        a=copy.deepcopy(original)
        a['source_asset_approval_status']=a.pop('approval_status')
        a['candidate_package_status']=GATE
        a['candidate_owner_approved']=False
        a['official_handoff_path']=str(OFFICIAL.relative_to(ROOT))+'/'+a.pop('packaged_path')
        a['candidate_image_path']=None
        a['role_in_candidate']='Source reference only; no new pose, performance or upload approval'
        a['derivatives']=[]
        if a['source_asset_approval_status']=='approved_scoped_reference':
            source=ROOT/a['official_handoff_path']
            path='assets/reference-images/NOT_APPROVED_FOR_PRODUCTION__'+source.name
            dest=FLOW/path;dest.parent.mkdir(parents=True,exist_ok=True)
            if dest.exists():raise FileExistsError(dest)
            shutil.copyfile(source,dest)
            a['candidate_image_path']=path
            md(path+'.status.md',f"# Reference copy status\n\n[APPROVED MEDIA ADAPTATION] Exact source art: `{a['original_path']}`; sha256 `{a['sha256']}`. Scope: {a['approval_scope']}\n\n[PROPOSAL] This copy is a local comparison reference only. It is not a new image/pose/motion approval and does not authorize uploading or generation. Image bytes are unchanged; this sidecar and filename carry the candidate gate.\n",FLOW)
        assets.append(a)
    js('manifests/asset-manifest.json',{'assets':assets,'copied_images':2,'uncopied_needs_review_references':49},FLOW)
    md('assets/README.md','''# Candidate references

[APPROVED MEDIA ADAPTATION] Two exact accepted reference images are physically copied, with unchanged bytes and status sidecars. Other 49 source records remain repository pointers in the manifest, not uploads or copies. Neither acceptance of original artwork nor physical copying approves the new story/shot. [UNKNOWN] Released Chapar pose, king listening/speaking insert, correction inscription layout and damp-treaty coda frames are missing or unapproved. No replacement art has been generated. Never upload this directory as a batch.
''',FLOW)
    candidate_shots=[]
    for old in original_shots:
        sid=old['scene']; d=intent[sid]
        lineids=[l['cue_id'] for l in dialogue['lines'] if l['scene']==sid and l['source_audio_path']]
        reference_ids=list(old['asset_ids'])
        action=old.get('bounded_performance_action',old['primary_beat'])
        siblings=[s for s in original_shots if s['historical_board_beat']==old['historical_board_beat']]
        continuation=siblings.index(old)>0
        if continuation:
            action='Hold the reviewed ending state of the preceding part of this same beat; do not repeat the transfer, gesture or writing action.'
        # Source restrictions take precedence over old speculative choreography.
        if sid=='S04' and old['historical_board_beat'].endswith('-B'):
            action='Hold Div-e Sefid’s supported tablet/cloth pose steadily. No wrapping, folding, closing or lip motion.'
        if sid=='S02' and old==[s for s in original_shots if s['scene']==sid][-1]:
            action='PROPOSAL SR01: after the tablet rests on the surface, anchor Chapar’s attention between the absent seal position and the receiver. An open empty hand never reaches toward the king like a payment request; if no released pose is approved, retain held art and narration. Do not invent a seal fragment or sender.'
        if sid=='S10' and old['historical_board_beat'].endswith('-A'):
            action='Hold the correction message distinct from the original tablet; exact SR04 inscription is added locally after approval, never generated lettering.'
        if sid=='S07' and old['historical_board_beat'].endswith('-C'):
            action='Let Akvan hold the king’s attention through a restrained listening/objection pose; no new brow/hand/mouth action without its exact approval.'
        if sid=='S06':
            action += ' Scene prerequisite: messenger presents one packet, Arash receives/attends, Arash decides, then riders depart; never invert delivery and dispatch or claim old cuts already prove contact.'
        candidate_shots.append(dict(id=old['id'],scene=sid,origin='existing handoff proposal reinterpreted',
             source_handoff_shot=str((OFFICIAL/'episode-01/shots'/f"{old['id']}.md").relative_to(ROOT)),
             source_board_beat=old['historical_board_beat'],source_scene_interval=old['source_scene_interval'],
             prior_unapproved_cut_interval=old['proposed_edit_seconds'],
             candidate_cut_start='TBD',candidate_cut_end='TBD',candidate_generation_duration='TBD',
             candidate_timing_status='PROPOSAL; no source timing or audio changed',
             cast=old['cast'],flow_names=old['flow_names'],registration='UNKNOWN; not inspected',
             asset_ids=reference_ids,cue_ids=lineids,change_ids=d['change_ids'],
             episode_goal='Recall the consequences of an unshared purpose without scapegoating those who acted',
             character_decision=d['decision'],scene_turn=d['turn'],dramatic_intent=d['want'],
             emotion=d['emotion'],primary_action=action,custody=old['custody'],
             transition=d['link'],punch_ids=['SRC-'+l for l in lineids if 'SRC-'+l in punch_ids]+d['change_ids'],
             source_citation=old['canonical_source'],
             start_frame='Existing exact approved composition only if recorded; otherwise TBD / missing approval',
             end_frame='TBD; ending state must match next chosen composition',
             recommended_model='Omni Flash 1.1 / Frames for approved composition; Ingredients only with separately approved references',
             model_duration_limits='See inherited dated feature verification; choose supported 4/6/8/10s only after timing/approval',
             candidate_state='PROPOSAL',production_authorized=False,owner_approved=False,
             final_filename=f"TAH_E01_{old['id']}_EN_STORY01_r01_take01.mp4"))
    # New inserts remain part of their parent scenes; their times are unassigned.
    for id_,sid,cid,cast,action in [
      ('S05_SR02_INSERT','S05','SR02',['tahmures','black_div'],'Show Tahmures listening to the wet return rather than preparing another rebuttal; stable held body/prop pose, no generated mouth sync.'),
      ('S11_SR05_CODA','S11','SR05',['akvan_div','div_e_sefid'],'Show the damp-damaged treaty already open, with the reed poised at its missing middle; exact writing remains native, missing promises never generated as readable text.')]:
        d=intent[sid];src=next(s for s in timeline['scenes'] if s['scene']==sid)
        candidate_shots.append(dict(id=id_,scene=sid,origin='PROPOSAL new insertion within existing scene',source_handoff_shot=None,
             source_board_beat=None,source_scene_interval=[src['start'],src['end']],prior_unapproved_cut_interval=None,
             candidate_cut_start='TBD',candidate_cut_end='TBD',candidate_generation_duration='TBD',candidate_timing_status='PROPOSAL extension; full candidate runtime TBD',
             cast=cast,flow_names=[],registration='UNKNOWN; not inspected',asset_ids=[],
             cue_ids=['SR02-KING-ACK'] if cid=='SR02' else ['SR05-HOOK'],change_ids=[cid],
             episode_goal='Expose responsibility for the question, then the next limit of evidence',
             character_decision=d['decision'],scene_turn=d['turn'],dramatic_intent=d['want'],emotion=d['emotion'],
             primary_action=action,custody='Wet Black Div empty-handed; no tablet' if cid=='SR02' else 'Treaty with Akvan; reed with Div-e Sefid; no river tablet copy; “obvious” is its unsupported claim, not recovered evidence',
             transition=d['link'],punch_ids=[cid],source_citation={'file':'book/part-1/01-what-is-a-prompt.md','heading':d['source']},
             start_frame='MISSING owner-approved exact composition',end_frame='TBD missing approved ending/transition',
             recommended_model='TBD until frame/action approval; keep native speaking/writing pipeline',model_duration_limits='Do not assign a preset before actual action and voice timing',
             candidate_state='PROPOSAL',production_authorized=False,owner_approved=False,final_filename=f'TAH_E01_{id_}_EN_STORY01_r01_take01.mp4'))
    # Order inserts after the parent scene’s last inherited card.
    candidate_shots.sort(key=lambda s:(s['scene'],s['id']))
    js('manifests/shot-to-asset-map.json',{'shots':candidate_shots,'source_scene_count':11,'candidate_shot_briefs':48,'source_coverage_shots':46,'new_insert_shots':2},FLOW)
    js('episode-01/dialogue-audio-map.json',{'lines':dialogue['lines'],'source_cue_count':34,'candidate_spoken_entries':36,'new_recording_entries':['SR02-KING-ACK','D-S07-2','SR05-HOOK'],'candidate_duration':'TBD'},FLOW)
    js('episode-01/scene-index.json',{'source_timeline':str((PROD/'timeline.json').relative_to(ROOT)),
          'source_duration_seconds':251.3,'candidate_duration_seconds':'TBD','source_title_count':1,
          'source_scenes':[dict(source_id=s['scene'],source_start=s['start'],source_end=s['end'],source_frames=s['frames'],kind='title' if s['scene']=='T00' else 'narrative',candidate_start='TBD',candidate_end='TBD') for s in timeline['scenes']]},FLOW)
    asset_byid={a['id']:a for a in assets}
    for shot in candidate_shots:
        sid=shot['scene']; d=intent[sid]
        references='\n'.join(f"- `{id_}`: `{asset_byid[id_]['candidate_image_path'] or asset_byid[id_]['original_path']}` — {asset_byid[id_]['source_asset_approval_status']}; only original scoped art, not proposed performance." for id_ in shot['asset_ids']) or 'MISSING approved exact start/end identity/contact reference; do not fabricate an upload master.'
        line_rows=[l for l in dialogue['lines'] if l['cue_id'] in shot['cue_ids']]
        cues='\n'.join(f"- `{l['cue_id']}` / {l['speaker']}: {l['candidate_text_status']} → “{l['candidate_text']}”; source WAV `{l['source_audio_path'] or 'NONE'}`; candidate recording `{l['candidate_recording_path'] or 'MISSING — approval/new take required'}`; candidate cue time TBD." for l in line_rows)
        prompt=f"""CANDIDATE TEXT ONLY; DO NOT GENERATE OR SPEND CREDITS.
Shot {shot['id']}, Ancient Tablet. After exact owner approvals, use the attached approved composition and identities in the existing hand-drawn, softly shaded 2D storybook style. Visible cast only: {', '.join(shot['cast']) or 'the sourced extras/graphic only'}. Character intent: {shot['dramatic_intent']}. One primary visual action: {shot['primary_action']} Preserve custody: {shot['custody']} Camera locked at the approved source angle. Let {shot['emotion'].lower()} come from attention and staging, not unapproved exaggerated expressions. Preserve identity, costume, light direction, floor contact and background geometry. End in the reviewed state needed by the next shot. No extra bodies, tablet copies, added gestures, wrapping transformations, invented gait, generated lettering or 3D surfaces. No new speech, mouth motion, voice imitation, music or sound is requested. Exact approved/local future authorised voice, native speaking/writing layers, captions and inscriptions are assembled outside this prompt. Missing frame, action, recording, timing or owner approval means BLOCKED; return a missing-input report instead of generation.
"""
        md('episode-01/shots/'+shot['id']+'.md',f"""# {shot['id']} — recommended restrained PROPOSAL

[CANON] Source anchor `{shot['source_citation']['file']}` → {shot['source_citation']['heading']}. [APPROVED MEDIA ADAPTATION] Source scene {sid}: {shot['source_scene_interval']} seconds. These are source locators, NOT the candidate cut. [PROPOSAL] Prior handoff cut {shot['prior_unapproved_cut_interval']} is historical unapproved coverage, not accepted timing. Candidate in/out/generation duration: **TBD**. Source entry: `{shot['source_handoff_shot'] or 'new candidate insert'}`.

## Full dramatic chain

[PROPOSAL] Episode goal: {shot['episode_goal']}. Character choice: {shot['character_decision']}. Scene turn: {shot['scene_turn']}. Punch source IDs: {', '.join(shot['punch_ids'])}. Exact candidate punch/word/gesture time: TBD. Source cue windows remain in the punch map; percentages do not apply to unknown candidate runtime.

[PROPOSAL] Entry state: {d['entry']}. One primary action: {shot['primary_action']} Ending/transition: {shot['transition']}. Listener/exit image: {d['exit']}. Character/prop continuity: {shot['custody']}. Keep Div-e Sefid messenger and Chapar courier distinct. No numbered continuation repeats a completed action.

## Frames, identities, assets and timing gate

{references}

[UNKNOWN] Start: {shot['start_frame']}. End: {shot['end_frame']}. No new frame was extracted or generated. All planned @ names refer only to a future actual registration, never to a local filename. Final camera staging and foreground masks remain owner-reviewed decisions.

[PROPOSAL] Model/mode: {shot['recommended_model']}. {shot['model_duration_limits']}. One output only if separately authorised later; actual resolution, duration, credits and cost are UNKNOWN. No approximate cut is declared compatible merely because it is shorter than a preset. Add edit handles only after exact speech/action timing; no approved WAV stretching.

## Dialogue and sound implications

{cues or '[PROPOSAL] No spoken cue directly assigned; match approved scene sound plan after edit decisions.'}

[UNKNOWN] Human lip sync remains unapproved. Source WAV paths prove provenance, not permission to reuse an old performance for changed words. New/replaced speech remains unrecorded. Reaction holds require real timing; speech-free intervals are not proof the soundtrack is silent.

## Candidate prompt — planning text, not authorization

```text
{prompt}```

[PROPOSAL] QA: compare against exact references, full normal/slow playback, silhouette/anatomy, feet/hand contact, prop count/custody, emotion and neighboring join. No royal blame shifted to malicious divs. Verify source speakers and local overlays. Record PASS/FAIL/NOT VERIFIED and reviewer evidence. Candidate must pass story, art, action, voice, timing and owner scope gates before any generation. If references/action conflict, retain baseline and record a blocker.

[PROPOSAL] Return filename after any future separately authorised generation: `{shot['final_filename']}`. Preserve original download, exact prompt/model/settings/reference hashes/source link/actual credits. Change IDs: {', '.join(shot['change_ids']) or 'none; retained source beat recontextualised as candidate coverage'}. No actual take exists.
""",FLOW)
    # Contexts are actual synchronized texts, not a promise to update later.
    md('context/EPISODE_PURPOSE.md',(WORK/'01_EPISODE_PURPOSE.md').read_text(),FLOW)
    md('context/CHARACTER_MOTIVATIONS.md',(WORK/'02_CHARACTER_PRESSURE.md').read_text(),FLOW)
    md('context/STORY_AND_SCENE_STATES.md',(WORK/'05_SCENE_BLUEPRINT.md').read_text(),FLOW)
    md('context/CONTINUITY_AND_APPROVALS.md',(WORK/'09_CONTINUITY_AUDIT.md').read_text(),FLOW)
    md('context/VISUAL_STYLE_LOCATIONS_AND_PROPS.md','''# Existing visual authority and candidate dramatic use

[APPROVED MEDIA ADAPTATION] Keep the selected revision's existing `veo-consistency-agent-instructions.md`: hand-drawn storybook, clean dark outlines, softly shaded painted colour, warm parchment/cedar/stone, restrained teal accents, exact existing costumes/faces. No numeric palette or new art style is invented. This is the sole retained visual style authority; new story intent does not authorize redesign.

[CANON] Hall/intake/cedar stand, frontier, three villages, eleven charcoal fires, worktable labels/request card, illustrative gate/court/practice, ledger and damp treaty hook are sourced in Chapter01. [PROPOSAL] Scene states and object ownership are in STORY_AND_SCENE_STATES and shot map. SR01 requires a released courier hand, SR02 a listening king, SR04 an exact local correction inscription, SR05 an approved treaty composition. None has new artwork approval. The river tablet is never duplicated; correction card, catalogue, practice sheet, ledger and treaty are separate objects.

[UNKNOWN] Most shot start/end images and reference-use rights remain unresolved as in the existing handoff. Asset manifest stores exact pointers, not invented references. Copying two accepted art files has not promoted the candidate performances.
''',FLOW)
    md('context/SOURCE_AUTHORITY.md',(WORK/'00_SOURCE_LEDGER.md').read_text(),FLOW)
    instructions={
      '00_BOOTSTRAP.md':('Candidate planning only','Plan one supplied shot. Do not generate, upload, spend credits, create voices, edit/delete project assets or treat these writing proposals as owner approval. Keep Confirm before generating Always. First state source facts, proposed deltas, actual references, timing/voice/art blockers and unresolved cast/role questions. Return a plan only.'),
      '01_STORY_INTENT.md':('Ancient Tablet — candidate dramatic intent','Recommended proposal: a capable court causes harm when it leaves a request’s purpose unshared. Preserve Chapar’s honest unknowns, Black Div’s accurate count, Akvan’s effective resistance and Tahmures’s responsibility. No malicious-div explanation or invented invasion. SR01–SR05 are separate unapproved deltas, not canon. Do not mix ceremonial alternatives into the selected restrained version.'),
      '02_VISUAL_IDENTITY_AND_STYLE.md':('Ancient Tablet — retain existing visual authority','Retain the existing Tahmures — Veo visual consistency agent instructions. This entry is a pointer, not a second style bible. Div-e Sefid is the pale white-haired/horned messenger; Chapar is a separate courier. Preserve exact approved image identities/costumes, 2D linework, soft shading, lighting, one river tablet, eleven charcoal fires and three villages. Missing identity or mismatched props means block the shot, not invent a design.'),
      '03_PERFORMANCE_AND_SUBTEXT.md':('Ancient Tablet — candidate listening and resistance','Play an intention toward another person, not a moral speech. Black Div reports without smirking; king listens before contesting; Akvan challenges the remedy to stop the reed, not to win an aphorism. Chapar is not forced to invent a sender. Preserve the messenger’s defensible urgency. No bowed forgiveness, reward, wound or surprise backstory. New facial/contact/speaking poses require exact owner review.'),
      '04_PACING_AND_SILENCE.md':('Ancient Tablet — timing evidence and contrast','Source scene and audio windows are locators. All candidate cut/insert/word landings and total runtime are TBD. Do not fit new speech into small gaps, speed approved recordings, or treat speech-free time as silence. Allow contrast: skill, divergence, bodily cost, public alarm, interrupted repair, qualified relief, unanswered evidence hook. Do not invent percentage-based twists or copy old proportional cuts as approved timing.'),
      '05_DIALOGUE_AUDIO_AND_OVERLAYS.md':('Ancient Tablet — source versus proposed speech','Keep the 34 original approved recordings separately. Candidate SR02-KING-ACK and SR05-HOOK have no recording; candidate D-S07-2 replaces text only and needs a new approved take. Never relabel an original WAV as the new line. Human lip sync is pending. Initial picture prompts request no new speech or mouth motion; native/local audio, writing, captions and correction inscription remain separate. No generated readable text or new voices.'),
      '06_AUTHORITY_AND_NEGATIVE_CONSTRAINTS.md':('Ancient Tablet — candidate approval boundary','Every file here is NOT APPROVED FOR PRODUCTION / NOT AUTHORIZED FOR FLOW GENERATION. A validation pass is not story, art, voice, timing or lip-sync approval. Canonical manuscript, approved media adaptation, source recordings, historical handoff and new proposals retain distinct scopes. Missing frame/asset evidence or a custody/cast conflict blocks generation. Never update canon, original timeline, acceptance records or official handoff from this candidate automatically.')}
    for file,(title,body) in instructions.items():
        md('agent-instructions/'+file,f'# Candidate Agent entry\n\n[PROPOSAL] Title: `{title}`\n\nReference: none newly assigned. Retain existing approved reference attachment; do not attach unapproved new expressions/compositions.\n\n```text\n{body}\n```\n\n[UNKNOWN] Actual installed entry/account state was not inspected. Owner may install only the accepted subset after the promotion and spending gates.\n',FLOW)
    md('agent-instructions/EXISTING_INSTRUCTIONS_RECONCILIATION.md','''# Existing instruction reconciliation

[APPROVED MEDIA ADAPTATION] Local baseline: `Characters/animations/chapter-01-candidate-01/production/english-final-03/veo-consistency-agent-instructions.md`. Owner reported a Flow entry with the corresponding title; no account was accessed. Keep its visual/identity/prop/audio restrictions. The source supported-tablet instruction forbids newly invented wrapping; candidate shots follow that limit even when an older board called the beat wrapping.

[PROPOSAL] Candidate 02 points to existing style authority instead of duplicating it. 01/03/04 add only story, subtext and unassigned temporal intent. 05 separates new spoken text from old approved WAVs; it does not override the ban on new voice generation. 00/06 prohibit production/generation until explicit scope approval. If an installed rule says keep all existing speech/timing, that remains in force: promote a specifically approved replacement later, do not install contradictory candidate text now.

[PROPOSAL] After approval, manually compare exact installed text with retained original, save a copy, and add/update only accepted nonoverlapping entries. Resolve any new action versus stable-pose conflict using the most restrictive valid scope. Do not keep competing full bibles active or infer approval because an Agent answered. Candidate review now involves local text only.
''',FLOW)
    # Preserve source public-doc guidance as evidence; operator guides get a
    # candidate gate and tailored story/recording constraints, not live UI claims.
    for p in sorted((OFFICIAL/'guides').glob('*.md')):
        text=p.read_text()
        for a in assets:
            old=next(o['packaged_path'] for o in original_assets if o['id']==a['id'])
            if a['candidate_image_path']: text=text.replace(old,a['candidate_image_path'])
        md('guides/'+p.name,'# Candidate operator procedure\n\n[PROPOSAL] INACTIVE UNTIL SCOPE APPROVAL. The numbered procedure below is retained from the previous local handoff for use only AFTER story/art/voice/timing approval and separately authorised generation. It is not permission to perform any remote operation now. Exact old paths that reference baseline assets require the manifest mapping in this candidate; never upload a needs-review source.\n\n[UNKNOWN] UI controls and subscription/model availability were documented earlier in this session, not inspected in an authenticated account. See manifests/flow-feature-verification.md for dated sources. Actual registration/balance/cost remain unknown.\n\n[PROPOSAL] Story-room changes SR01–SR05 do not receive generation authority from these steps. Review candidate lines before any old prompt; source WAVs for retained lines remain separate. Candidate shot cuts/runtime are TBD. New references and recordings require the decisions in manifests/missing-assets-and-decisions.md.\n\n[PROPOSAL — conditional future steps]\n\n'+text,FLOW)
    md('manifests/flow-feature-verification.md',(OFFICIAL/'manifests/flow-feature-verification.md').read_text()+'\n\n[UNKNOWN] Retained dated public-doc verification; no new account check. This candidate run calls no Flow service. Exact new shot duration choices remain TBD until voice/action timing is approved.\n',FLOW)
    md('manifests/missing-assets-and-decisions.md','''# Candidate blockers

[UNKNOWN] Source visual references: retain original acceptance limits; six cast identities, standalone backgrounds/props, new contacts and most exact frames remain unapproved in the prior manifest. Only two exact art copies have scoped reference acceptance. No current Flow @ registration is verified.

[PROPOSAL] SR01: release/empty-hand Chapar composition; SR02: new king acknowledgement take, listening/speaking pose and inserted timing; SR03: new Akvan take, expression/alignment and measured duration; SR04: correction overlay readable within a reviewed shot; SR05: treaty composition, Akvan/Div-e Sefid continuity transition, narrator take and coda timing. Full candidate runtime TBD. No placeholder filename is an existing WAV/frame.

[CONFLICT] Old proportional coverage is retained only as an audit locator, not a candidate edit. S04 speech-to-wrapping mismatch must be resolved before a pilot. Reject any adoption that preserves the wrong cut merely to keep a nominal runtime.

[PROPOSAL] Owner must separately choose story change IDs, visual/action references, dialogue wording/performance, timing, final picture/lip sync, exact newly versioned handoff destination and (later) actual generation/upload budget. No decision is accepted by silence or tests. Canon/English/Persian approvals never expand automatically.
''',FLOW)
    md('episode-01/SCENE_AND_SHOT_INDEX.md','# Scene and shot index\n\n[APPROVED MEDIA ADAPTATION] Source: T00 + S01–S11, 251.3s/7539 frames. [PROPOSAL] Forty-six retained coverage IDs plus two new within-scene inserts. Candidate cuts/runtime TBD; T00 not a generated narrative shot.\n\n| Scene | Candidate briefs | Proposed change IDs |\n|---|---|---|\n'+'\n'.join(f"| {sid} | {', '.join(s['id'] for s in candidate_shots if s['scene']==sid)} | {', '.join(intent[sid]['change_ids']) or 'none; source retained'} |" for sid in intent)+'\n',FLOW)
    md('episode-01/ASSEMBLY_PLAN.md','''# Candidate assembly and sound plan

[APPROVED MEDIA ADAPTATION] Retain original 251.3s / 7539-frame / 30fps production and its 34 WAVs as immutable baseline. [PROPOSAL] Work only in a new review edit. Candidate scene IDs/order remain S01–S11 after title T00; candidate global times and total duration TBD. New inserts belong to S05/S11, not a silent twelfth narrative scene.

[PROPOSAL] SR02 follows original D-S05-5 with a separately measured reaction and new king take. SR03 replaces D-S07-2 text only after a new approved recording; never play old words beneath the new subtitle. SR04 inscription remains a local editable graphic and never replaces recipient/correction/acknowledgement. SR05 follows the ledger maxim and precedes the final series mark. Its exact timing, role transition and source art are blocked. Do not treat the book hook as already shot or recorded.

[PROPOSAL] Rebuild all candidate cut and cue offsets after read-through. Keep exact audio speeds; shortening another scene is an explicit owner edit choice, never an automatic “fit”. Check custody through scene transitions: one tablet reaches Arash; correction and treaty are separate. Exact written content, subtitles, native speaking/writing and masks remain local; generated video is not a transparent layered rig.

[UNKNOWN] No new edit, render, voice, soundtrack or full playback has been performed. After later approval, record actual takes/hashes/settings/costs, export a new candidate file, inspect actual frame/stream/duration data and watch/listen completely. Never overwrite source assembly or infer owner approval from a technical probe.
''',FLOW)
    md('episode-01/PUNCH_AND_SILENCE_MAP.md',(WORK/'06_PACING_NOTES.md').read_text(),FLOW)
    # CSV retains the original column names plus the candidate file gate.
    put_csv=WORK/'06_PUNCH_MAP.csv'
    (FLOW/'episode-01/punch-map.csv').write_bytes(put_csv.read_bytes())
    md('episode-01/SHOT_QA.md','''# Candidate review gates

[PROPOSAL] Review story before performance: can the viewer track what the king asked, what each reader did, what it cost, what Akvan changed and what correction cannot undo? Compare voices without character labels. Keep S09 explicit bridge separate. Exact cue/gesture landing is TBD until playback.

[PROPOSAL] Per shot: verify approved identities/reference hashes, messenger/courier distinction, one tablet, costume/alpha/anatomy/floor/contact/occlusion, no added villain cues or invented text. Review entire clip normally/slowly and compare first/last joins. New poses and correct mouth movement require human evidence; source performance approval cannot authorize replacement speech.

[PROPOSAL] Per scene and episode: review causal continuity, three villages/eleven fires, delivery before dispatch, king accountability without coerced forgiveness, correct labels/card role, no new knife, native text/audio and unresolved treaty evidence. No cut may be called approved because its numbers sum correctly. Record PASS/FAIL/NOT VERIFIED separately from owner acceptance.

[UNKNOWN] No candidate moving clip exists. All production and generation gates remain blocked. The independent writing review is not perceptual or artistic signoff.
''',FLOW)
    # Full propagation: each atomic story change and each candidate shot has a row.
    rows=[]
    context_files='context/EPISODE_PURPOSE.md;context/CHARACTER_MOTIVATIONS.md;context/STORY_AND_SCENE_STATES.md;context/CONTINUITY_AND_APPROVALS.md;context/VISUAL_STYLE_LOCATIONS_AND_PROPS.md'
    instruction_files='agent-instructions/01_STORY_INTENT.md;agent-instructions/03_PERFORMANCE_AND_SUBTEXT.md;agent-instructions/04_PACING_AND_SILENCE.md;agent-instructions/05_DIALOGUE_AUDIO_AND_OVERLAYS.md;agent-instructions/06_AUTHORITY_AND_NEGATIVE_CONSTRAINTS.md'
    for c in changes:
        matching=[s for s in candidate_shots if c['id'] in s['change_ids']]
        rows.append(dict(story_change_id=c['id'],scene_id=c['scene'],shot_id=';'.join(s['id'] for s in matching),original_source=c['source'],prior_state=c['prior'],proposed_state=c['proposed'],context_files=context_files,agent_instructions=instruction_files,flow_prompt_files=';'.join('episode-01/shots/'+s['id']+'.md' for s in matching),dialogue_audio_files='episode-01/dialogue-audio-map.json;episode-01/punch-map.csv',timeline_impact=c['timing']+'; episode-01/scene-index.json;episode-01/ASSEMBLY_PLAN.md',asset_reference_impact=c['asset']+'; manifests/asset-manifest.json;manifests/shot-to-asset-map.json',approval_status='PROPOSAL / '+GATE,owner_decision='PENDING; no scope approval recorded',validation_status='PENDING candidate validator'))
    for s in candidate_shots:
        rows.append(dict(story_change_id='SHOT-'+s['id'],scene_id=s['scene'],shot_id=s['id'],original_source=s['source_handoff_shot'] or s['source_citation']['file']+'#'+s['source_citation']['heading'],prior_state='Historical unapproved coverage '+str(s['prior_unapproved_cut_interval']),proposed_state=s['primary_action']+'; candidate cut TBD; parent changes '+','.join(s['change_ids']),context_files=context_files,agent_instructions=instruction_files,flow_prompt_files='episode-01/shots/'+s['id']+'.md',dialogue_audio_files='episode-01/dialogue-audio-map.json;episode-01/punch-map.csv',timeline_impact='TBD candidate; source scene untouched; episode-01/scene-index.json;episode-01/ASSEMBLY_PLAN.md',asset_reference_impact=';'.join(s['asset_ids'])+'; manifests/asset-manifest.json;manifests/shot-to-asset-map.json',approval_status='PROPOSAL / '+GATE,owner_decision='PENDING scope and exact frame/action/timing approval',validation_status='PENDING candidate validator'))
    fields=next(csv.reader((ROOT/'story-room/templates/FLOW_HANDOFF_IMPACT_MATRIX.csv').open()))
    csvwrite('CHANGE_IMPACT_MATRIX.csv',fields,rows,FLOW)
    # Every file compared by hash/path; new candidate files never replace input.
    source_files={str(p.relative_to(OFFICIAL)):sha(p) for p in OFFICIAL.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    js('manifests/existing-handoff-snapshot.json',{'root':str(OFFICIAL.relative_to(ROOT)),'files':source_files},FLOW)
    md('README.md','''# Story-room synchronized Flow candidate 01

[PROPOSAL] This package derives from the existing production handoff at `Characters/animations/chapter-01-candidate-01/production/english-final-03/flow-handoff/`. That source is unchanged and is itself a preparation handoff with scoped art approvals, not blanket final-film approval. This package is versioned candidate writing only.

[APPROVED MEDIA ADAPTATION] Baseline: eleven narrative scenes plus T00 title, 251.3 seconds, 7539 frames, 34 approved source cues. [PROPOSAL] Candidate: 48 shot briefs (46 inherited IDs plus S05_SR02_INSERT and S11_SR05_CODA), 36 candidate spoken entries, five atomic story changes, candidate runtime TBD. Two exact image copies retain only prior art acceptance; 49 other references are pointers needing review.

## Local owner review quick start

1. Read ../00_SOURCE_LEDGER.md and ../01_EPISODE_PURPOSE.md.
2. Read ../07_CANDIDATE_SCRIPT.md and compare originals/alternatives in the dialogue score.
3. Read ../10_STORY_RED_TEAM.md, including the second pass and unresolved blockers.
4. Decide SR01–SR05 separately using ../11_OWNER_DECISIONS.md.
5. Inspect scene-index, dialogue-audio-map, punch map and the 48 individual briefs.
6. Inspect reference hashes/scopes and missing composition, voice, timing and identity approvals.
7. Review CHANGE_IMPACT_MATRIX.csv and file-by-file changes in HANDOFF_DIFF_AND_PROMOTION.md.
8. Resolve measured read-through/runtime, exact art and new recording decisions; no performance is generated now.
9. Record explicit accepted IDs/scopes/hashes; leave rejected alternatives unpromoted.
10. Only then request a new versioned official handoff using the conditional promotion instruction. Generation/upload/spending requires separate authorization.

[PROPOSAL] Agent entries and guides are local planning drafts, not instructions to install or run now. All files are gated; image names and sidecars retain the same gate without changing approved pixels. Canonical/approved-media status in a source field does not approve this candidate. Actual Flow project state remains UNKNOWN. No paid/provider or Flow actions, commits, pushes or media generation were performed.
''',FLOW)
    md('11_OWNER_DECISIONS.md','''# Individual decisions — no approval assumed

[PROPOSAL] Reply to each ID accept/reject/revise. Acceptance of writing intent alone does not approve art, voice, timing, final picture or Flow generation. No decision is required to inspect this local package.

| ID | Concrete choice | Downstream gates |
|---|---|---|
| SR01 | Show Chapar’s honest lack of sender knowledge through a released empty-hand hold, with source narration retained? | Exact released pose/contact/frame/readability approval; no new factual knowledge |
| SR02 | Keep all five S05 lines and add Tahmures “I had not reckoned on the crossing.” after the wet return? | New recording, reaction/speaking pose, measured pause and scene/episode timing; original tail cannot fit by assumption |
| SR03 | Select Akvan’s economical “More words. The same question.” instead of the original, or retain original? Ceremonial alternative is separate. | Wording/performance choice, new take, exact alignment and timing; original WAV unchanged |
| SR04 | Add local correction inscription “The alarm began in this hall.” while retaining recipient/correction/acknowledgement? | Exact text/layout/readable hold/composition; no image-model lettering |
| SR05 | Add canon-grounded damp-treaty coda in S11 before series mark, with the proposed narrator line? | Div-e Sefid messenger→Mirror role interpretation, treaty art/coda frames/new narration/runtime/hook approval |

[PROPOSAL] Recommended: restrained package, not ceremonial hearing. Highest-priority decisions are SR02 accountability, SR03 effective resistance and whether SR05's new coda/role transition belongs in this episode. SR01/SR04 avoid extra exposition but still need visible staging.

[UNKNOWN] None of these five changes has owner acceptance. Candidate total duration TBD. Separate approval for permitted local reference use, source art rights, voices/new recordings, exact edit timings and final moving picture remains necessary. No explicit generation/spending request exists. The precise conditional promotion instruction is in flow-handoff-candidate/HANDOFF_DIFF_AND_PROMOTION.md.
''')
    md('12_FLOW_WRITING_HANDOFF.md','# Shot-writing intent handoff\n\n[PROPOSAL] This summary is input to the complete synchronized package in flow-handoff-candidate/, not a substitute for it. Source scene windows and original WAVs are exact; candidate cuts/word landings are TBD.\n\n| Scene/shot | Source anchor | Dramatic intent | Physical/action cue | Changes |\n|---|---|---|---|---|\n'+'\n'.join(f"| {s['scene']} / {s['id']} | {s['source_citation']['file']} → {s['source_citation']['heading']} | {s['dramatic_intent']} | {s['primary_action']} | {','.join(s['change_ids']) or 'retained source'} |" for s in candidate_shots)+'\n\n[UNKNOWN] References, source audio, proposed replacement/new speech, punch anchors and assembly impacts are linked in each full brief and the machine maps. All new action/frame/voice/timing approvals remain blocked.\n')
    print('Synchronized candidate: 48 shot briefs, 8 Agent documents, 36 dialogue entries, 53 impact rows')


if __name__=='__main__':main()
