"""NOT APPROVED FOR PRODUCTION / NOT AUTHORIZED FOR FLOW GENERATION.

Create candidate writing only; production sources are read-only inputs.
"""
import csv
import hashlib
import io
import json
from pathlib import Path

WORK = Path(__file__).resolve().parents[1]
ROOT = next(p for p in WORK.parents if (p / 'meta-prompt.md').exists())
PROD = ROOT / 'Characters/animations/chapter-01-candidate-01/production/english-final-03'
OFFICIAL = PROD / 'flow-handoff'
FLOW = WORK / 'flow-handoff-candidate'
GATE = 'NOT APPROVED FOR PRODUCTION / NOT AUTHORIZED FOR FLOW GENERATION'


def read(p):
    return json.loads(p.read_text())


def put(base, name, text):
    p = base / name
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        raise FileExistsError(p)
    p.write_text(text)


def md(name, body, base=WORK):
    put(base, name, '**' + GATE + '**\n\n[PROPOSAL] English story-room candidate 01. Source facts and pending decisions are tagged below.\n\n' + body)


def js(name, value, base=WORK):
    put(base, name, json.dumps(dict(status=GATE, approval_status='PROPOSAL', owner_approved=False, **value), ensure_ascii=False, indent=2) + '\n')


def csvwrite(name, fields, rows, base=WORK):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=['candidate_file_status'] + fields)
    writer.writeheader()
    writer.writerows(dict(candidate_file_status=GATE, **r) for r in rows)
    put(base, name, stream.getvalue())


def mmss(t):
    return f'{int(t // 60):02}:{t % 60:06.3f}'


# Scene intent is interpretation; source events are separately labelled in output.
SCENES = {
 'S01': dict(title='A hall that can read anything', focal='Shahrasp', want='Make fine writing legible without damaging it',
  obstacle='Messages arrive in many fragile forms; reading a mark does not identify its use',
  entry='The hall appears practised and orderly', tactic='Attend to the silk through the crystal',
  decision='Stay with the small exact work rather than perform mastery for the room',
  turn='Impressive reading skill established → audience is ready to mistake skill for judgement',
  stakes='A system with wide reach can spread a small error', emotion='Confidence with a trace of vulnerability',
  ethical='Does the ability to read oblige the reader to act?', prop='silk; crystal; received messages',
  physical='Preserve the accepted wide illustration; crystal/silk held steady',
  sound='Quiet work; no invented ceremonial music', exit='Legible marks; an unanswered question about who sent them',
  link='The unidentifiable river tablet tests the hall’s apparent competence', source='The Setting',
  costume='Shahrasp green costume', change_ids=[]),
 'S02': dict(title='The honest absence', focal='Chapar', want='Deliver the found tablet without claiming knowledge he lacks',
  obstacle='The tablet arrives without a usable sender or recipient; court attention can make uncertainty feel like failure',
  entry='A courier has an object but no trustworthy route back to its author', tactic='Present the object; decline to fill the missing knowledge with a guess',
  decision='[PROPOSAL SR01] After the tablet rests on the surface, keep the empty hand open briefly when attention seeks an absent seal',
  turn='An object arrives → its origin and destination remain explicitly unknown',
  stakes='An honest limitation can be discarded when the object passes to someone powerful', emotion='Relief at delivery → exposed uncertainty',
  ethical='Who is permitted to say that they do not know?', prop='one found tablet; dissolved seal trace',
  physical='[PROPOSAL] A later released/empty-hand pose needs approval; accepted held art alone cannot perform it',
  sound='Let the existing narration state the unknowns; no new courier speech', exit='One tablet on the intake surface; no invented authentic seal',
  link='Tahmures asks a question without assigning the object a present role', source='The Setting',
  costume='Chapar brown/cream; distinct from white-haired messenger', change_ids=['SR01']),
 'S03': dict(title='A question with three doors', focal='Tahmures', want='Receive a useful description of the object',
  obstacle='He assumes his desired kind of answer is shared', entry='One unidentified object and three capable readers',
  tactic='Ask a short royal question; let each specialist inspect', decision='Retain the original ambiguous request',
  turn='A common object is offered → three incompatible assignments become possible',
  stakes='The ruler’s expectation is not yet a shared constraint', emotion='Ease → unnoticed divergence',
  ethical='Does obedience relieve the questioner of responsibility for the question?', prop='one river tablet; cedar stand',
  physical='Read marks, inspect weight/cord, and read twice in succession; never duplicate the tablet',
  sound='Retain exact D-S03-1; avoid ominous villain scoring', exit='Black Div has read; the hall has not agreed what kind of answer is wanted',
  link='Each reader’s expertise supplies its own answer and action', source='The Request', costume='Three readers keep separate silhouettes',change_ids=[]),
 'S04': dict(title='Competence becomes commitment', focal='Akvan / Div-e Sefid / Black Div', want='Each completes the work they recognise',
  obstacle='The same sentence can be a historical record, an urgent dispatch or a current order',
  entry='No mutually stated role for the tablet', tactic='Catalogue / carry / obey', decision='Messenger takes the supported packet; Black Div leaves without it',
  turn='Three interpretations coexist → they acquire independent physical consequences',
  stakes='A trip cannot be unmade once taken; a message can outrun its uncertainty', emotion='Productive certainty → dread from divergence',
  ethical='Which reasonable precaution becomes unreasonable when its premise is unstated?', prop='catalogue distinct from tablet; oilcloth packet',
  physical='Use the existing supported messenger pose; do not invent a wrapping transformation or new gait',
  sound='Keep exact Akvan/Div-e Sefid recordings. Their certainty should differ, not become evil',
  exit='Packet with messenger; Black Div empty-handed beyond the room',link='A correct numerical answer returns attached to a bodily cost',
  source='The Unexpected Result',costume='Akvan blue-toned/dark-gold; messenger pale/white-haired; Black Div dark',change_ids=[]),
 'S05': dict(title='The right answer costs a journey',focal='Black Div, then Tahmures',want='Report faithfully / recover a shared meaning',
  obstacle='Every existing reply is defensible but fails to undo the crossing', entry='Black Div returns wet, without the tablet',
  tactic='Give a precise count; answer the actual objections without mockery',
  decision='[PROPOSAL SR02] Tahmures looks at the wet clothing before acknowledging the unanticipated cost without yet diagnosing the request defect',
  turn='King seeks an error in the answer → king recognises the unanticipated cost without yet diagnosing its cause',stakes='Wet crossing and elapsed time already spent; the court cannot refund them',
  emotion='Royal disbelief → discomfort → accountable attention',ethical='Can the ruler accept an answer and still admit the harm?',
  prop='wet empty hands/clothing; no river tablet',physical='Hold the body/cloth evidence; do not add wound, collapse or new weather',
  sound='Five original dialogue cues retained; new king cost acknowledgement is a separate unrecorded line; he has not yet diagnosed the request defect',
  exit='[PROPOSAL] The king has no rebuttal ready; the wet reader remains a person, not a lesson prop',
  link='The cost expands from one body/journey to a public false alarm',source='The Unexpected Result',costume='Black Div wet; Tahmures unchanged',change_ids=['SR02']),
 'S06': dict(title='The hall’s error travels',focal='Arash and the affected villages',want='Protect the frontier before an apparent threat arrives',
  obstacle='The courier chain makes urgency visible while hiding uncertainty',entry='Messenger packet reaches Arash before dispatch',
  tactic='Dispatch riders; villages respond; charcoal burners continue ordinary work',decision='Preserve delivery-before-dispatch and show the real camp separately',
  turn='Apparent invasion → eleven ordinary charcoal fires; fear is real though the threat is not',
  stakes='Three villages lose a quiet night; riders and Black Div spend unrecoverable effort',
  emotion='Escalation → recontextualisation, not a comic erasure of cost',ethical='What remains owed after an alarm proves false?',
  prop='one packet with Arash; lamps; exactly eleven charcoal fires',physical='Three distinct village settings; workers/tools clear of fire; no attack or burning home',
  sound='Use existing narration; suggested local ambience changes are PROPOSAL, not existing recorded effects',
  exit='The fires are ordinary; consequences of naming them a threat remain',link='The king initially tries more words, not a different responsibility',
  source='The Unexpected Result',costume='Arash separate from anonymous riders and villagers',change_ids=[]),
 'S07': dict(title='The pen that need not continue',focal='Akvan and Shahrasp against Tahmures’s first remedy',want='Make the next request answerable',
  obstacle='More wording preserves the undefined demand for meaning',entry='King dictates a longer version of the same uncertainty',
  tactic='Akvan interrupts the premise; Shahrasp stops rather than embellishes',decision='[PROPOSAL SR03] Akvan’s economical counterline earns the stop; keep the separate labels/card demonstration',
  turn='Length mistaken for repair → a requested result and missing context become visible',
  stakes='The court must surrender a polished answer and admit three unknowns',emotion='Defensiveness → resistance heard → deliberate restraint',
  ethical='May a subordinate prevent a more eloquent mistake?',prop='reed; ledger; four labels; separate request card',
  physical='No new knife; stop once; exact labels added locally; old tablet packet does not teleport back',
  sound='D-S07-1 kept; D-S07-2 replacement requires approval/new recording; use speech-free source gaps only as measured capacity, not guaranteed silence',
  exit='Four distinct places; first three unknown; request card separated from examined words',
  link='Demonstration tests roles beyond this one embarrassing case',source='The Discovery',costume='Akvan’s gesture/expression requires her own approved pose',change_ids=['SR03']),
 'S08': dict(title='The same words change work',focal='Watch / witnesses / apprentice',want='Show what a sentence does in three settings',
  obstacle='The surface grammar looks unchanged',entry='One sentence is ready to be mistaken for one role',tactic='Compare current order, quoted evidence and handwriting practice',
  decision='Keep the apprentice anonymous and the scenes illustrative',turn='A single grammatical form → several contextual functions',
  stakes='A rule must survive beyond one selected example',emotion='Attention → recognition',ethical='Who gives words their present work?',
  prop='gate order; evidence document; practice sheet all distinct from river tablet',physical='No gate reaction to quoted/practice words',
  sound='Retain original two narration cues; exact phrase is local text',exit='Ink remains ink in the practice vignette',
  link='S09 explicitly translates the dramatic distinction into modern engineering',source='The Discovery',costume='No named hero replaces apprentice',change_ids=[]),
 'S09': dict(title='The engineering bridge',focal='Viewer / narrator',want='Transfer the distinction to the complete model interaction',
  obstacle='A single memorable sentence can eclipse the surrounding system',entry='Ancient example has shown consequences and a repair',
  tactic='Keep eight equal-weight components inspectable',decision='Retain exact bridge content as a separate explanatory register',
  turn='A story about one tablet → a model of a structured request',stakes='Reader must not infer that better prose authenticates or enforces permission',
  emotion='Recognition → usable mental model',ethical='What must deterministic application code still enforce?',
  prop='native editable envelope graphic; no royal seal as security proof',physical='No AI-generated text; keep source formula and eight components',
  sound='All three approved narration cues retained',exit='One testable review question returns the audience to action',
  link='The corrected northbound message demonstrates a concrete next decision',source='From Tale to Engineering / Mental Model',costume='No ancient character delivers modern jargon',change_ids=[]),
 'S10': dict(title='A correction carries a name',focal='Tahmures / Div-e Sefid / returning riders',want='Correct the rumour and receive acknowledgement',
  obstacle='A shorter message can still evade who owns the first alarm',entry='A better-defined request has been prepared',
  tactic='Name recipient, correct the rumour, ask for acknowledgement',decision='[PROPOSAL SR04] Add the local visible correction inscription “The alarm began in this hall.”',
  turn='The king’s authority sent alarm outward → it now carries responsibility outward',
  stakes='Repair does not erase the spent night or guarantee trust restored',emotion='Resolve → limited relief',ethical='Can a correction take responsibility without creating another spectacle?',
  prop='new correction message, not duplicated river tablet',physical='Use reviewed presentation/handoff pose only; overlay exact inscription locally',
  sound='No new speech; retain three narrator cues, natural pacing unchanged unless picture review demands time',
  exit='Riders return; villagers lower the same lamps',link='The ledger retains the lesson; an incomplete treaty tests its limits',
  source='The Discovery',costume='Div-e Sefid receives correction; Chapar not substituted',change_ids=['SR04']),
 'S11': dict(title='A practice, not a victory',focal='Shahrasp, then Akvan / Div-e Sefid in proposed coda',want='Keep a record of what changed without pretending uncertainty has ended',
  obstacle='A neat maxim can close a question that the next case reopens',entry='Correction has returned riders; ledger remains',
  tactic='Keep the existing closing sentence, then contrast a document whose middle is absent',
  decision='[PROPOSAL SR05] Attach a brief canonical-hook coda within S11 before the final series mark; no twelfth narrative scene',
  turn='A named role seems sufficient → missing evidence becomes the next unresolved problem',
  stakes='Div-e Sefid’s confidence must not become proof of promises no one can read',emotion='Earned relief → fresh unease',
  ethical='Who can speak for words that are no longer there?',prop='ledger/reed; candidate damp-damaged treaty, not river tablet',
  physical='New treaty/reference/pose missing; do not fabricate missing promises as readable text',
  sound='Existing NEN-11 retained; proposed hook narration and coda duration TBD',exit='Reed begins before anyone asks for evidence; cut before any missing promise is endorsed',
  link='Chapter 02 uncertainty hook; messenger/Mirror role transition requires owner approval',
  source='The Next Tale',costume='Same named Div-e Sefid; no invented identity merger beyond the scoped proposal',change_ids=['SR05'])
}

CHANGES = [
 dict(id='SR01',scene='S02',type='visual',source='The Setting / NEN-02C',prior='Unknown carrier/recipient conveyed by narration; accepted held Chapar art has no released pose',
      proposed='Witness Chapar declining to invent an absent sender, with an open empty hand after release; no new dialogue',
      timing='TBD exact action/hold; preserve source narration; released/empty-hand frame not approved',
      audio='No new recording proposed',asset='Released Chapar/contact/empty-hand pose and composition need approval'),
 dict(id='SR02',scene='S05',type='new_dialogue',source='The Unexpected Result / D-S05-1..5',prior='Five exchanges end on “The tablet asked for a count.”',
      proposed='Retain all five; after seeing the wet clothing Tahmures adds: “I had not reckoned on the crossing.”',
      timing='TBD new line/response; existing scene tail cannot be assumed to fit it',audio='New Tahmures line SR02-KING-ACK; no recording exists',asset='Listening/reaction pose and extension require review'),
 dict(id='SR03',scene='S07',type='replace_dialogue',source='The Discovery / D-S07-2',prior='That still leaves means to carry a large burden.',
      proposed='Akvan: “More words. The same question.”',timing='TBD measured duration; source D-S07-2 window remains reference only',
      audio='Replacement D-S07-2 must be newly recorded only after approval; original WAV preserved',asset='Akvan pose/expression and new alignment need review'),
 dict(id='SR04',scene='S10',type='overlay',source='The Discovery / NEN-10B',prior='Correction names recipient, corrects rumour, asks acknowledgement',
      proposed='Local correction-message inscription: “The alarm began in this hall.”',timing='TBD readable hold; existing narration not lengthened automatically',
      audio='No new speech',asset='Exact correction overlay/composition/readability require approval; never generated lettering'),
 dict(id='SR05',scene='S11',type='coda',source='The Next Tale',prior='Current media ending stops with the maxim; book hook absent',
      proposed='After ledger maxim and before final series mark, Akvan opens damp-damaged treaty; Div-e Sefid begins writing missing promises before a request for evidence',
      timing='TBD coda; complete candidate duration TBD; stays within S11 as proposed coda',
      audio='New narrator line SR05-HOOK; no recording exists',asset='Treaty, coda composition, Akvan/Div-e Sefid pose and role transition require approval')
]

NEW_LINES = {
 'SR02-KING-ACK': dict(scene='S05',speaker='tahmures',text='I had not reckoned on the crossing.',change_id='SR02'),
 'SR05-HOOK': dict(scene='S11',speaker='narrator',text='Akvan opened a treaty, its middle eaten by damp. Div-e Sefid called the missing promises obvious, and began to write before anyone asked how it knew.',change_id='SR05')
}


def main():
    source = read(PROD / 'timeline.json')
    js('candidate-story.json', {'version':'story-room-01-recommended-restrained',
        'source_timeline':str((PROD/'timeline.json').relative_to(ROOT)),
        'source_duration_seconds':source['duration'],'source_frames':source['frames'],
        'candidate_duration_seconds':'TBD','source_scene_count':11,'source_title_segments':1,
        'scenes':[dict(id=sid, **data) for sid,data in SCENES.items()],
        'changes':CHANGES,'new_lines':NEW_LINES})
    fields = next(csv.reader((ROOT/'story-room/templates/11_SCENE_MATRIX.csv').open()))
    rows=[]; blueprint='# Eleven scene blueprint\n\n[APPROVED MEDIA ADAPTATION] Source has T00 plus eleven narrative units. T00 is title only, not one of these rows. [PROPOSAL] Candidate preserves their IDs and order; all changed line/action/cut timings are TBD. Source scene boundaries below are locators, not candidate booking slots.\n\n'
    for src in source['scenes']:
        sid=src['scene']
        if sid=='T00':continue
        d=SCENES[sid]
        rows.append(dict(scene_id=sid,source_ref=f"{(PROD/'timeline.json').relative_to(ROOT)}#/scenes/{sid}; book/part-1/01-what-is-a-prompt.md#{d['source']}",authority='CANON events / APPROVED MEDIA ADAPTATION source timing / PROPOSAL staging',status='PROPOSAL',start_time_s=src['start'],end_time_s=src['end'],entrance_state=d['entry'],focal_character=d['focal'],active_want=d['want'],obstacle=d['obstacle'],tactic=d['tactic'],turn_before_to_after=d['turn'],punch_type='BRIDGE' if sid=='S09' else 'NEXT_EPISODE_HOOK' if sid=='S11' else 'TURN',exit_image=d['exit'],next_scene_link=d['link'],runtime_conflict='TBD candidate timing; '+('; '.join(c['timing'] for c in CHANGES if c['scene']==sid) or 'source voice retained; no new cut approval'),owner_decision=';'.join(d['change_ids']) or 'Retain source; review candidate shot staging'))
        blueprint+=f"""## {sid} — {d['title']}

[APPROVED MEDIA ADAPTATION] Source interval {mmss(src['start'])}–{mmss(src['end'])}, {src['frames']} frames; source revision {src['source_revision']}. Source cues: {', '.join(l['cue_id'] for l in src['lines'])}. [CANON] Event source: Chapter 01 → {d['source']}; Div-e Sefid messenger substitution is separately approved media scope.

[PROPOSAL] Entry: {d['entry']}. Focal character: {d['focal']}. Active want: {d['want']}. Obstacle: {d['obstacle']}. Tactic: {d['tactic']}.

[PROPOSAL] Choice: {d['decision']}. Turn: {d['turn']}. Visible stakes: {d['stakes']}. Emotional shift: {d['emotion']}. Ethical pressure: {d['ethical']}

[PROPOSAL] Physical beat / prop: {d['physical']} / {d['prop']}. Sound/dialogue burden: {d['sound']}. Exit: {d['exit']}. Transition: {d['link']}.

[PROPOSAL] Causal test: because {d['entry'].lower()}, {d['focal']} tries to {d['want'].lower()}, but {d['obstacle'].lower()}; the change is {d['turn'].lower()}.

[UNKNOWN] Candidate scene/cut/word-landing timing TBD. Change IDs: {', '.join(d['change_ids']) or 'none; retention with unapproved coverage'}. All new composition/action and final picture need approval; identity source art is not new motion approval.

"""
    blueprint+='[PROPOSAL] Tension contour: quiet skill → uncertainty exposed → confident divergence → body-cost reversal → public consequence → resisted self-repair → comparative breathing space → explicit bridge → accountable correction → incomplete-evidence hook. This is a qualitative contour, not a quota or a prescribed percentage chart. S01/S08/S09 are intentionally not manufactured confrontations; their changes are perceptual/epistemic.\n'
    md('05_SCENE_BLUEPRINT.md',blueprint)
    csvwrite('11_SCENE_MATRIX.csv',fields,rows)
    # Source punch windows are exact audio windows. Word/gesture landings remain TBD.
    targets={'NEN-02C':('HOOK',2,'An object arrives as if it were a normal dispatch','Its sender/recipient are unknown','Object → missing context'),
             'D-S03-1':('DECISION',2,'Three specialists face one object','The king asks an underspecified question','Royal expectation → independent assignments'),
             'D-S04-2':('DECISION',2,'Catalogue and inspection appear harmless','Messenger commits to carrying urgency','Interpretation → external action'),
             'D-S05-1':('REVEAL',3,'The king expects a description','A wet reader returns an accurate count','A right answer reveals a wrong task'),
             'D-S05-5':('REVERSAL',3,'King objects to a literal answer','Tablet and king have competed as sources of purpose','Rebuttal fails to recover the spent journey'),
             'NEN-06A':('COST',3,'Villages fear invasion','Ordinary charcoal burners are the counted fires','True words / false alarm; fear is not harmless'),
             'D-S07-2':('REVERSAL',2,'A longer request seems safer','Akvan challenges what remains unspecified','Length → target of resistance'),
             'NEN-07D':('DECISION',3,'Three labels still invite guessed answers','Unknowns stay unknown; requested result is separated','Ruler must choose what he actually wants'),
             'NEN-09A':('BRIDGE',2,'Ancient drama has shown a boundary','Complete interaction replaces single-sentence model','Story → engineering register'),
             'NEN-10C':('MOTIF_PAYOFF',2,'Riders carried alarm outward','They return after correction','Repair visible; lost night not refunded'),
             'NEN-11':('MOTIF_PAYOFF',1,'Words seemed to prescribe their own role','The ledger retains a qualified rule','Practice continues rather than sovereign perfection')}
    fields=next(csv.reader((ROOT/'story-room/templates/06_PUNCH_MAP.csv').open()))+['source_cue_end_mmss','exact_word_or_visual_landing','speech_free_gap_after_s']
    punches=[]; gaps=[]; cue_lines=[]
    for s in source['scenes']:
        for i,l in enumerate(s['lines']):
            start=l['global_start'];end=start+l['duration']
            following=s['start']+s['lines'][i+1]['scene_start'] if i+1<len(s['lines']) else s['end']
            gap=following-end
            gaps.append(dict(scene=s['scene'],cue_id=l['cue_id'],source_speech_end=end,source_next_speech_or_scene_end=following,available_speech_free_seconds=gap,artistic_silence='UNKNOWN',candidate_silence='TBD'))
            cue_lines.append(dict(cue_id=l['cue_id'],scene=s['scene'],speaker=l['speaker_id'],text=l['canonical_text'],source_start=start,source_end=end,source_duration=l['duration'],source_audio_path=str((PROD/'projects'/s['scene'].lower()/'lip-sync/en'/l['audio_file']).relative_to(ROOT)),source_sha256=l['working_audio_sha256'],source_approved_performance=l['performance_approved'],human_lip_sync_approved=False,candidate_text='More words. The same question.' if l['cue_id']=='D-S07-2' else l['canonical_text'],candidate_text_status='PROPOSAL' if l['cue_id']=='D-S07-2' else 'APPROVED MEDIA ADAPTATION retained text',candidate_recording_path=None if l['cue_id']=='D-S07-2' else str((PROD/'projects'/s['scene'].lower()/'lip-sync/en'/l['audio_file']).relative_to(ROOT)),candidate_start='TBD',candidate_end='TBD',new_recording_required=l['cue_id']=='D-S07-2',change_ids=['SR03'] if l['cue_id']=='D-S07-2' else []))
            if l['cue_id'] not in targets:continue
            typ,impact,setup,landing,change=targets[l['cue_id']]
            punches.append(dict(scene_id=s['scene'],beat_id='SRC-'+l['cue_id'],source_ref=str((PROD/'timeline.json').relative_to(ROOT))+'#'+l['cue_id'],authority='APPROVED MEDIA ADAPTATION source audio; PROPOSAL dramatic reading',start_mmss=mmss(start),episode_percent=f'{100*start/source["duration"]:.4f}',beat_type=typ,setup=setup,expectation=setup,landing_action_or_line=landing,change_in_knowledge_power_or_goal=change,impact_0_to_3=impact,aftershock_or_silence='UNKNOWN sound; source speech-free capacity '+str(gap),existing_or_proposed='source cue window / PROPOSAL interpretation',owner_decision='Review actual playback; no word-level landing inferred',source_cue_end_mmss=mmss(end),exact_word_or_visual_landing='TBD',speech_free_gap_after_s=gap))
    for c in CHANGES:
        punches.append(dict(scene_id=c['scene'],beat_id=c['id'],source_ref=c['source'],authority='PROPOSAL',start_mmss='TBD',episode_percent='TBD',beat_type={'SR01':'SUBTEXT','SR02':'COST','SR03':'REVERSAL','SR04':'DECISION','SR05':'NEXT_EPISODE_HOOK'}[c['id']],setup='See source scene and linked existing cue',expectation='Existing source expectation retained',landing_action_or_line=c['proposed'],change_in_knowledge_power_or_goal=c['proposed'],impact_0_to_3=3 if c['id'] in ['SR02','SR05'] else 2,aftershock_or_silence='TBD; do not borrow an unmeasured pause',existing_or_proposed='PROPOSAL',owner_decision=c['id']+' exact scope/timing/art/voice review',source_cue_end_mmss='TBD',exact_word_or_visual_landing='TBD',speech_free_gap_after_s='TBD'))
    csvwrite('06_PUNCH_MAP.csv',fields,punches)
    js('speech-gap-audit.json',{'gaps':gaps,'method':'Timeline speech onset plus actual recorded duration; this is not a full soundtrack or phoneme analysis.'})
    for id_,l in NEW_LINES.items():
        cue_lines.append(dict(cue_id=id_,scene=l['scene'],speaker=l['speaker'],text=None,source_start=None,source_end=None,source_duration=None,source_audio_path=None,source_sha256=None,source_approved_performance=False,human_lip_sync_approved=False,candidate_text=l['text'],candidate_text_status='PROPOSAL',candidate_recording_path=None,candidate_start='TBD',candidate_end='TBD',new_recording_required=True,change_ids=[l['change_id']]))
    js('dialogue-candidate.json',{'source_cues':34,'candidate_spoken_entries':36,'lines':cue_lines,'source_recordings_untouched':True,'candidate_runtime':'TBD'})
    final5=next(g for g in gaps if g['cue_id']=='D-S05-5')
    md('06_PACING_NOTES.md',f"""# Pacing notes and temporal audit

[APPROVED MEDIA ADAPTATION] Baseline runtime 251.3 seconds, 7539 frames at 30fps. 06_PUNCH_MAP uses actual cue-window starts/ends and percentages of that baseline only. [UNKNOWN] It does not locate a particular word, blink, breath or hand action inside a WAV. Those exact landings are TBD; no listening/table-read performance has been claimed.

[PROPOSAL] The central contrast is slow professional competence against fast unsupported commitment, then correct speech against an irreversible journey. Do not make every scene a peak. Keep S01 patient, S05 uncomfortable, S06 widening, S07 interrupted, S08 comparative and S10 restrained. S09 is a necessary change of register, not an ancient character's lecture.

## Read-only scheduling simulation

[APPROVED MEDIA ADAPTATION] All 34 source windows are extracted to speech-gap-audit.json. End of D-S05-5 is {mmss(final5['source_speech_end'])}; S05 ends {mmss(final5['source_next_speech_or_scene_end'])}. Only {final5['available_speech_free_seconds']:.6f}s remains. [CONFLICT] That is not capacity for an seven-word cost acknowledgement plus listening. SR02 must be separately read and timed; do not squeeze it into the tail or speed approved voices.

[APPROVED MEDIA ADAPTATION] D-S07-2 is 4.24s as recorded. [PROPOSAL] Its five-word economical alternate may release space, but word count is not performed duration. Keep candidate duration TBD until a real read. Do not claim the difference pays for SR02 or the coda.

[CONFLICT] Existing Flow coverage proportionally reallocates historical beats. S04's wrapping coverage comes after D-S04-2 has finished. Source scene intervals are reliable locators; those proposed camera cuts are not. Candidate shot-cut times are therefore TBD and must be rebuilt around actual speech, custody and observed native actions after approval.

[PROPOSAL] SR05 adds a hook after the source ledger maxim, before the final series mark. Its exact start/end/runtime is TBD. It is not silently fitted under NEN-11, and not called a twelfth source scene. Its treaty image and narrator take are missing.

## Three high-value contrast decisions

1. [PROPOSAL SR01] Let the viewer see uncertainty before confident specialist action. No additional factual answer or new courier speech.
2. [PROPOSAL SR02/SR04] Let the wet reader and the visible correction carry the king's accountability. Separate the admission from the emotional relief of returning riders.
3. [PROPOSAL SR03/SR05] Cut rhetorical weight at the failed repair, then reopen uncertainty with the damaged treaty. Keep the final unanswered question free of a lecture.

[UNKNOWN] A spoken table read and muted 30-second animatic viewing were not performed. Proposed tests: listen to S05's unchanged chain, then read SR02 after it without hurrying; compare the two Akvan variants blind; view baseline 01:30–02:00 muted (source interval only) to see whether wet cost, village alarm and ordinary fire reveal remain legible. Record observations, not assumed results.
""")
    # Original text retained alongside exactly two alternatives per pivotal exchange.
    annotations={
      'D-S03-1':('Obtain a usable description','Make three servants answer without naming the required classification','Power assumes shared purpose; preserve its ambiguity','Keep original in recommended script; clearer request here destroys the error'),
      'D-S04-1':('Identify an old military command by resemblance','Have the court accept her catalogue placement','Her competence seeks stable provenance; resemblance is not authorship proof','Keep original; do not turn her into the villain'),
      'D-S04-2':('Treat the object as urgent and carry it to Arash','Obtain room to dispatch it before a possible threat grows','Protective urgency competes with archival care','Keep original; locked supported pose avoids invented wrap'),
      'D-S05-1':('Report an exact count','Have the ruler accept work completed','Pride in precision meets an unshared task','Keep factual count and wet body together'),
      'D-S05-2':('Ask whether the river was crossed','Get him to confront unexpected consequence','Surprise may become blame; listen before answering','Keep; direct question exposes human cost'),
      'D-S05-3':('Attribute action to the tablet imperative','Defend a reasonable literal reading','He can explain the action without settling who owned the task','Keep; no smirk or accusation invented'),
      'D-S05-4':('Distinguish the king’s question from tablet wording','Restore his intended hierarchy of purpose','The intention arrives late; authority alone cannot refund effort','Keep, then let later admission answer it'),
      'D-S05-5':('State why a count seemed required','Make the king face the competing request','Plain grammar punctures royal certainty','Keep exact strongest existing line'),
      'D-S07-1':('Ask a longer version of the same unresolved question','Make Shahrasp write a seemingly complete remedy','More command may defend power rather than solve a problem','Keep; actors should play a sincere attempted repair'),
      'D-S07-2':('Expose the continuing burden on means','Make the king stop and define success','Akvan spends social permission to resist an eloquent mistake','Replace only as PROPOSAL SR03; original retained in source map')}
    score='# Dialogue score\n\n[APPROVED MEDIA ADAPTATION] Exact originals and WAV/time links are in dialogue-candidate.json. [UNKNOWN] Source voice performance approval does not establish human mouth alignment. All proposed lines are English originals, not translations or imitation.\n\n## Line-by-line spoken exchange audit\n\n'
    for l in cue_lines:
        if l['cue_id'] not in annotations:continue
        literal,want,subtext,decision=annotations[l['cue_id']]
        score+=f"### {l['cue_id']} — {l['speaker']} / {l['scene']}\n\n[APPROVED MEDIA ADAPTATION] Exact original: “{l['text']}” Source window {mmss(l['source_start'])}–{mmss(l['source_end'])}; `{l['source_audio_path']}`.\n\n[PROPOSAL analysis] Literal: {literal}. Wants listener to: {want}. Tactic/subtext: {subtext}. Listener change sought: pause or alter the next decision. Withheld information: none established; do not play a secret motive as fact. Power: king can close the exchange; specialist/courier can supply evidence or resistance. Decision: {decision}.\n\n"
    score+='''## Pivotal exchange A — S03: keep the damaging ambiguity

[APPROVED MEDIA ADAPTATION] Tahmures: “Tell me what this is.”

[PROPOSAL economical alternate] Tahmures: “What have they brought me?”

[PROPOSAL ceremonial alternate] Tahmures: “Let each of you tell me what has come into my hall.”

[PROPOSAL recommendation] Retain the exact original in the coherent script. The economical version shifts attention toward the courier; the ceremonial version consumes time and makes the king perform sovereignty before its cost is earned. Both alternatives are retained for comparison, not selected. All alternate spoken durations TBD; no new recording authorized.

## Pivotal exchange B — S05: an answer is not a refund

[APPROVED MEDIA ADAPTATION] Original sequence: Black Div “There are eleven watchfires.” / Tahmures “You crossed the river?” / Black Div “The tablet said to count them.” / Tahmures “I asked what the tablet was.” / Black Div “The tablet asked for a count.”

[PROPOSAL economical / RECOMMENDED SR02] Retain that five-line sequence verbatim. The king looks at wet clothing instead of preparing another rebuttal. Add Tahmures: “I had not reckoned on the crossing.” Do not bow, touch the other character or turn the admission into a royal award. The existing body-cost gets a response. New admission timing and speaking pose TBD.

[PROPOSAL ceremonial alternate] Black Div: “Eleven watchfires.” Tahmures: “You went beyond the water?” Black Div: “The words sent me.” Tahmures: “I asked you to name the thing.” Black Div: “I found a command, and obeyed it.” Tahmures: “Then let the fault be spoken here, where the words were handed to you.”

[PROPOSAL comparison] The ceremonial version makes admission public but replaces five already good recordings, inflates the ruler’s last word and risks absolving the court in one proclamation. Reject for the coherent package. The economical version preserves each defence and adds only the ruler’s decision to stop contesting the evidence. Neither line means Black Div never bears responsibility; it identifies the defect in the request rather than manufacturing a villain.

## Pivotal exchange C — S07: resistance changes the action

[APPROVED MEDIA ADAPTATION] Tahmures: “Write: Examine this tablet carefully, consider every word, and tell me exactly what it means.” Akvan: “That still leaves means to carry a large burden.”

[PROPOSAL economical / RECOMMENDED SR03] Retain Tahmures exactly. Akvan: “More words. The same question.” She asks no permission to decorate the objection; a listening king stops the reed. Say it to change the writing, not to win a clever exchange.

[PROPOSAL ceremonial alternate] Akvan: “Your words have grown, my king. Your question has not.” One figurative contrast, then plain action. Respectful address buys the room to oppose him, but adds rhetorical polish and may sound too much like the sovereign’s own voice.

[PROPOSAL comparison] Original ten words: 4.24s recorded. Economical five words; ceremonial eleven words. Word counts do not establish durations or matching mouth events. New take, listening pause and exact alignment TBD; preserve original audio rather than splicing a new textual claim onto its WAV.

## Voice fingerprints and table-read test

[PROPOSAL] Tahmures starts with short demands, tries a long command, then earns one plain acknowledgement. Akvan uses diagnostic contrasts and points to the object; no sermon. Black Div speaks in literal completed actions, without villainous relish. Div-e Sefid favours destination/urgency and avoids scholarly proof language. Chapar’s silence refuses a guess; it must not erase his witness function. Shahrasp listens through a reed that can stop; he is not a comic echo. Arash’s visible dispatch carries the claim; do not invent offscreen belligerent speech.

[UNKNOWN] No actor table read has occurred. Compare economical/ceremonial versions without speaker labels, then ask a listener which person is trying to get what. If they only hear a shared aphoristic voice, use the economical version and fewer metaphors. New voices/recordings and phoneme claims remain blocked pending owner authorization.
'''
    md('07_DIALOGUE_SCORE.md',score)
    script='# Ancient Tablet — complete recommended candidate continuity script\n\n[PROPOSAL] Restrained package SR01–SR05; alternatives in 07_DIALOGUE_SCORE. All existing dialogue/narration not explicitly replaced is retained below, in source order. Source windows are locators ONLY. Candidate scene/line times and total runtime TBD. No source WAV is changed. T00 remains the existing title.\n\n'
    for s in source['scenes']:
        sid=s['scene']
        if sid=='T00':
            script+='## T00 — retained title\n\n[APPROVED MEDIA ADAPTATION] Ancient Tablet; source 00:00–00:03. [PROPOSAL] Candidate title timing not reassigned.\n\n';continue
        d=SCENES[sid]
        script+=f"## {sid} — {d['title']}\n\n[APPROVED MEDIA ADAPTATION] Source {mmss(s['start'])}–{mmss(s['end'])}. [PROPOSAL] {d['physical']}. Entry: {d['entry']}.\n\n"
        for l in s['lines']:
            if l['cue_id']=='D-S07-2':
                script+='[PROPOSAL SR03; new recording required; time TBD] **AKVAN DIV:** More words. The same question.\n\n'
            else:
                script+=f"[APPROVED MEDIA ADAPTATION retained text; {l['cue_id']}] **{l['speaker_id'].upper()}:** {l['canonical_text']}\n\n"
        if sid=='S05':script+='[PROPOSAL SR02; after original D-S05-5, NOT in its source tail; time TBD] The king lets the wet clothing answer him first. **TAHMURES:** I had not reckoned on the crossing. He does not reach for a reward, issue an excuse or demand assent. Black Div is not required to forgive him.\n\n'
        if sid=='S10':script+='[PROPOSAL SR04, exact local graphic, no new speech; time TBD] On the correction message, distinguish the king’s words from the found tablet. Visible inscription: **The alarm began in this hall.** Keep recipient/correction/acknowledgement intact. Do not frame a seal as proof that its content is true.\n\n'
        if sid=='S11':script+='[PROPOSAL SR05, canon-grounded coda within S11; new composition/narrator; time TBD] After the ledger maxim, before the final series mark: Akvan opens a treaty whose middle is eaten by damp. Div-e Sefid begins to write where words are missing. **NARRATOR:** '+NEW_LINES['SR05-HOOK']['text']+' The cut leaves those promises unendorsed. No invented complete treaty text is shown. The identity/function transition from media messenger to book-hook Mirror role is an owner decision, not an accomplished continuity repair.\n\n'
        script+=f"[PROPOSAL] Exit: {d['exit']}. Transition: {d['link']}.\n\n"
    md('07_CANDIDATE_SCRIPT.md',script)
    visual='# Visual and sound pass\n\n[PROPOSAL] Meaning is carried by one tablet changing hands, one wet body returning, one reed stopping and a different document losing its middle. No new injury, threat, evil intent or historical ritual is asserted. Sound below is a design proposal unless tied to an exact approved cue; no effects were created.\n\n'
    for sid,d in SCENES.items():
        visual+=f"### {sid}\n\n[CANON / APPROVED MEDIA ADAPTATION source] See Chapter01 → {d['source']} and source scene {sid}. [PROPOSAL] Entry: {d['entry']}. Picture-first: {d['physical']}. Exit: {d['exit']}. Sound/silence: {d['sound']}. Object: {d['prop']}. Cost risk: do not add contact, crowds, facial turns or exact writing without approved frame/action support.\n\n"
    visual+='''## Exposition-to-action substitution

[PROPOSAL SR01/SR04] Do not add a speech explaining honest ignorance or royal accountability. Let the empty courier hand expose missing origin; let the correction carry the local inscription while the existing narrator states recipient/correction/acknowledgement. These change audience attention, not the factual contents of the found tablet. Released Chapar action and correction readability are unresolved art/timing decisions.

[PROPOSAL] Reed contact, custody transfer and readable text are better retained in native/local animation than entrusted to generative video. Flow may supply a reviewed held-composition background/light pass; that is not a performance replacement. New SR02 speech requires a speaking asset/recording or a clearly non-speaking reaction insert under a legitimate voiceover edit, approved separately. No automatic new lip-sync is claimed.

[UNKNOWN] Proposed muted baseline observation window: 01:30–02:00, 30 source seconds. No movie was modified or newly rendered, and no viewing result is asserted. Test whether a viewer can identify Black Div's cost, the spread of alarm, and the ordinary camp without hearing narration. If not, select a closer existing image or propose a new reviewed composition; do not declare imaginary frames available.

[PROPOSAL] Sound motif: work rhythm interrupted, a report heard without protective music, village activity allowed to subside. Any pen/drip/hoof/ambient recording is missing until inventory and rights approval; no score is assumed to be silent merely because speech has paused. Avoid using ominous music to mark divs as evil or triumphant music to erase the spent night.
'''
    md('08_VISUAL_SOUND_PASS.md',visual)
    md('09_CONTINUITY_AUDIT.md','''# Continuity and scope audit

| Priority / finding | Source and evidence | Candidate treatment | Gate |
|---|---|---|---|
| [CANON] Requirements/interface design owns the failure | Chapter01 Failure Analysis | Preserve accurate count, unknown origin, ambiguous request; no malicious-div explanation | PASS for written proposal; not art approval |
| [APPROVED MEDIA ADAPTATION] Div-e Sefid messenger / Chapar separate | continuity 2026-10-24; source D-S04-2 | Every candidate cast map retains both distinct functions | PASS |
| [CONFLICT] Film hook missing / book hook uses Mirror role | Chapter01 The Next Tale versus source S11/NEN-11 | SR05 coda labelled new media proposal; same-name role transition requires decision | BLOCKED for production |
| [CANON] Garshasp only referenced; count eleven; three villages | The Unexpected Result; source S04/S06 | No onstage Garshasp, invasion, deaths, wounds, burned houses or new genealogy | PASS |
| [CONFLICT] Source depicts read/repair, not external hearing or formal tribunal | Source narrative/scene manifests | Ceremonial hearing is an unselected alternate only; recommended version stays restrained | PASS if not silently mixed |
| [UNKNOWN] Private guilt/fear/trauma | No source states hidden psychology | Character pressure marked inference; visible choices proposed | No invented backstory |
| [CONFLICT] New line/replace line cannot reuse prior approved WAV as new performance | D-S05-5 tail and D-S07-2 source audio | Two new cues plus one replacement need scoped recording/time decisions; source hashes retained | BLOCKED |
| [CONFLICT] Old Flow cuts do not prove camera alignment | Existing handoff shot-map / validation report | Candidate cut times TBD; preserve original scene locators only | BLOCKED until edit review |
| [APPROVED MEDIA ADAPTATION] No knife, steady tablet/cloth, native writing | Veo consistency rules; REVISION-REPORT | No speculative wrapping/gait/hand contact; exact text locally composed | PASS for instruction scope |
| [UNKNOWN] New released Chapar/treaty/reaction composition | Existing art acceptance limits | Missing references explicitly blocked; do not create new images | BLOCKED |
| [CANON] Modern bridge belongs outside ancient drama | Chapter01 From Tale to Engineering / Mental Model | S09 alone retains engineering terms; no AI/model jargon added to character lines | PASS |
| [UNKNOWN] Final visual/phoneme approval | README and independent-recheck owner flag false | No owner signoff implied from tests | BLOCKED for production |
| [CANON] English/Persian separate | AGENTS.md and review-status | No Persian proposal, translation/source hash/metadata edits; English voice approval never covers Persian | PASS |

[PROPOSAL] Candidate continuity delta is confined to SR01–SR05; no recurring cast, genealogy, world rule or previous source fact is retconned. The coda cites the existing next-chapter promise but its new pictures/voice placement are not approved adaptation. The wet crossing and villagers' alarm already happened in canon; “lost trust” remains interpretive, not a newly established permanent series state.

[UNKNOWN] Final candidate runtime and source/candidate word landings. All are TBD where not sourced. Do not write proposed durations into original timeline.json or call a source recording approved lip sync.

[PROPOSAL] Zero silent canon mutations: the source-snapshot validator must match before handoff. Existing official handoff is an input, not an output path. Promotion later requires accepted change IDs, exact revision hashes, timing/audio/art scope and new destination. No unreported high-severity contradiction is production-ready.
''')
    print('Created phases 5–9 and machine-readable story/dialogue/gap ledgers')


if __name__=='__main__':main()
