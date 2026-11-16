"""Readable character cards and a single operator route for both RW01 branches."""
import csv
import json


# These are performance interpretations of the supplied screenplay, not additions
# to manuscript canon, biographical facts, voice approvals or dialogue rewrites.
PEOPLE = {
 'tahmures': dict(en='Tahmures', fa='طهمورث', role='King; commissions the inquiry and later corrects his own unclear request.', role_fa='شاه؛ سفارش‌دهندهٔ بررسی و مسئولِ روشن نکردنِ خواسته.', want='Obtain an answer and restore control without first choosing exactly what work is wanted.', knows='Knows the tablet was found; does not know its original owner. Learns about the kilns and alarm from the reports.', pressure='Authority lets him avoid a clarifying question; accountability requires a precise correction.', acting='Short, direct questions. Let the held-back outburst in S07 and the seated exchange in S11 show change. No constant shouting or sudden saintly certainty.', acting_fa='پرسش‌ها کوتاه و روشن؛ تغییر را با فروخوردنِ تندی و هم‌سطح نشستن با شهراسب نشان بده.', ties='Shahrasp asks for scope; the three divs expose its absence; Simurgh helps him name the present task.', avoid='No modern engineering terms in his ancient-world dialogue. No verified attribution of the tablet to Hushang.'),
 'shahrasp': dict(en='Shahrasp', fa='شهراسب', role='Minister and recorder; relays the commission and separates documents.', role_fa='وزیر و ثبت‌کننده؛ انتقال‌دهندهٔ خواسته و جداکنندهٔ نوشته‌ها.', want='Make the king’s request precise while carrying out the instruction he actually receives.', knows='Knows Chapar found the object by the northern river; has no verified original sender or recipient.', pressure='Recognises ambiguity but initially carries it onward rather than securing clarification.', acting='Precise, measured delivery and active listening. A pause before taking the tablet matters. Record concrete answers without playing an omniscient tutor.', acting_fa='لحن سنجیده و پرسش‌گر؛ مکثِ پیش از بردنِ لوح و دقت در ثبت پاسخ‌ها مهم است.', ties='Questions Tahmures, delivers to the divs, writes the lesson and correction. He is not the bird mentor.', avoid='Do not merge the ancient tablet, western-gate example, technical closing sheet, correction and reply.'),
 'chapar': dict(en='Chapar', fa='چاپار', role='Finder and initial courier; brings the tablet to court.', role_fa='یابندهٔ لوح و پیکِ نخست؛ رسانندهٔ آن به بارگاه.', want='Deliver a potentially important find while reporting only what he witnessed.', knows='Found it by the northern river; did not see its bearer. The broken seal suggests importance, not verified authority.', pressure='Urgency tempts an embellished story; he chooses the limited truth of discovery.', acting='Breathless arrival, but simple factual speech. Young-looking portrait is an appearance cue, not a specified canonical age. Do not play him as foolish or secretly informed.', acting_fa='رسیدن با نفسِ بریده، اما گزارش کوتاه و دقیق؛ فقط از چیزی بگوید که دیده است.', ties='Hands the bundle to Tahmures. Div-e Sefid is a different, later messenger.', avoid='No horns, crown, armour or bow. The portrait supplies no horse, saddlebag or riding pose; those need separate review.'),
 'arash': dict(en='Arash', fa='آرش', role='Frontier officer at Sepid Fortress; dispatches riders and receives the correction.', role_fa='فرماندهٔ سپیددژ؛ اعزام‌کنندهٔ سواران و گیرندهٔ پیامِ اصلاحی.', want='Protect the frontier quickly when a message appears to come from the royal hall.', knows='Receives an old tablet through White Div; infers a present royal commission before it has been confirmed.', pressure='Protective caution has a public cost when gate closure becomes evidence for a rumour.', acting='Controlled questions and economical gestures. His error is an unchecked inference, not cruelty. In S09 he belongs to an illustrative example, not a second actual dispatch.', acting_fa='پرسش و اشارهٔ کم اما قاطع؛ خطایش شتاب در برداشت است، نه بدخواهی.', ties='Receives from Div-e Sefid; sends riders; later acknowledges the new correction and reports the result.', avoid='Do not invent archery action because the portrait carries a bow. Bow is in anatomical left hand, viewer right; preserve quiver side. For desk work, review a pose that rests the bow in a visible rack or clear continuity position before handling the tablet/message. Never let it vanish or merge with the hand. Exact handling changes need staging review.'),
 'akvan_div': dict(en='Akvan Div', fa='اکوان دیو', role='Examines writing and compares it with records.', role_fa='بررسی‌کنندهٔ خط و سنجندهٔ آن با اسناد.', want='Identify a credible historical association without losing the evidence.', knows='Sees a resemblance to Hushang’s writing; does not know whether Hushang wrote the tablet.', pressure='Recognition feels like an answer, but resemblance cannot establish authorship.', acting='Deliberate, qualified speech; let a pause before “resembles” signal care. Move attention between object and record, not theatrical villain poses.', acting_fa='شمرده و با قیدِ تردید؛ شباهت را گزارش کند، نه انتسابِ قطعی را.', ties='Works beside Black Div and White Div; later reports a possible association to Tahmures.', avoid='No confirmed ancient author, omniscience or malicious deception. Final damp-treaty insert remains optional PROPOSAL.'),
 'black_div': dict(en='Black Div', fa='دیو سیاه', role='Executes the tablet’s apparent instruction and counts the fires.', role_fa='اجراکنندهٔ برداشتِ ظاهری از نوشته و شمارندهٔ آتش‌ها.', want='Complete the count before the written sunrise deadline.', knows='Crossed the river and found eleven charcoal kilns. His count is correct; the role assigned to the tablet is wrong.', pressure='Competent execution of embedded text can still be the wrong task.', acting='Plain, literal report without comic stupidity. Wet sleeve, dripping water and brief answers make the effort tangible.', acting_fa='گزارش ساده و دقیق؛ آستینِ خیس و پاسخ‌های کوتاه، بهای کار را نشان بدهند.', ties='Waits for Akvan to release the tablet before taking it; later contradicts the assumption that these were watchfires.', avoid='Exactly eleven kilns in the report. No enemy army, invented defeat or villainous roar.'),
 'div_e_sefid': dict(en='Div-e Sefid', fa='دیو سفید', role='Onward messenger; carries the found object and later the corrective message.', role_fa='پیام‌رسانِ ادامهٔ مسیر؛ رسانندهٔ لوح و سپس پیامِ اصلاحی.', want='Prevent a potentially urgent message from arriving too late.', knows='Knows where the tablet came from immediately; does not know its original intended recipient or current authority.', pressure='Finding a plausible recipient feels safer than waiting for confirmation.', acting='Urgent but not frantic. Let the unanswered question at the fortress reveal uncertainty; later read the correction’s actual addressee before departing.', acting_fa='شتابِ مهارشده؛ تردید پشت سکوتِ کوتاه پیدا شود، نه با تغییرِ ناگهانی شخصیت.', ties='Distinct from Chapar. Delivers to Arash, returns the tablet, carries an interim restraint message and then the full correction.', avoid='Never turn him into the finder, the bird mentor or the king’s father. Preserve branch-specific face, hair and both horns.'),
 'simurgh_bird': dict(en='Simurgh', fa='سیمرغ', role='Bird mentor summoned by the feather; distinguishes questions and tasks.', role_fa='راهنمای پرنده‌پیکر؛ روشن‌کنندهٔ تفاوتِ پرسش‌ها و کارها.', want='Make Tahmures specify the present request while leaving unknown history unknown.', knows='Hears the king’s account; does not magically recover sender, date, recipient or missing words.', pressure='Has authority to lecture but instead makes the king do the discriminating work.', acting='Calm, concrete questions; restrained head/eyeline changes. Folded wings and a readable perch are preferable to constant flapping. New beak motion needs separate review.', acting_fa='آرام و پرسش‌گر؛ پاسخ را به شاه تلقین نکند و نادانسته‌ها را با داناییِ جادویی پُر نکند.', ties='Advises Tahmures while Shahrasp records; never replaces Div-e Sefid’s courier work.', avoid='Bird only in this owner adaptation. No human body or transformation. Preserve this branch’s exact beak/neck proportions.'),
 'hushang': dict(en='Hushang', fa='هوشنگ', role='Father identity in this media branch; appears as an uncertain remembered association.', role_fa='هویتِ پدر در این اقتباس؛ تصویرِ یادآوری‌شده و نامطمئن.', want='No active present-day objective is written. The image visualises Akvan’s association.', knows='No present-day knowledge or dialogue is supplied.', pressure='The temptation belongs to the observer: treating a familiar image as proof.', acting='A brief subjective still/image insert, fading with the writing. No independent entrance, speech or active exchange in the hall.', acting_fa='تصویری گذرا از تداعیِ اکوان؛ نه ورودِ روح به تالار و نه حضورِ واقعی در صحنه.', ties='Associated with Tahmures as father within this adaptation; authorship of the tablet remains unverified.', avoid='Never recast as Chapar, Arash or the onward messenger. No claim this branch changes book genealogy.'),
}


def build_character_info(base, root, episode):
    def put(folder, name, text):
        p=folder/name; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text.strip()+'\n')

    for branch,display,prefix in [('paper-puppet','Paper Puppet','PP'),('illustrated-v2','Illustrated V2','V2')]:
        folder=base/('flow-'+branch)
        assets=json.loads((folder/'manifests/assets.json').read_text())['assets']
        lookup={a['character']:a for a in assets}
        missing=[c for c in PEOPLE if c not in lookup]
        records=[]; index=[]
        for id_,p in PEOPLE.items():
            a=lookup.get(id_)
            scenes=[s['id'] for s in episode['scenes'] if id_ in s['cast']]
            cues=[b['id'] for s in episode['scenes'] for b in s['blocks'] if b.get('speaker')==id_]
            evidence=[b['id'] for s in episode['scenes'] if id_ in s['cast'] for b in s['blocks'] if b.get('speaker')==id_ or b['type']=='action']
            reference=a['packaged_path'] if a else None
            status=('Supplied/selected reference; derivative review needed' if a and a['review_required'] else 'Owner-supplied/selected reference available') if a else 'MISSING visual reference in this branch'
            visual=a['description'] if a else 'No matching image supplied. Story information below is usable for planning; visual generation of this identity remains blocked. Never borrow the other branch’s image.'
            name=a['flow_character_name'] if a else f'RW01_{prefix}_{id_}'
            flow=f"{p['en']} / {p['fa']}. Role in RW01: {p['role']} Visual identity: {visual} Performance direction (proposal): {p['acting']} Knowledge boundary: {p['knows']} Do not change or invent dialogue. {p['avoid']} Keep this identity distinct from the other cast and match only the selected {display} references."
            rec=dict(id=id_,name_en=p['en'],name_fa=p['fa'],branch=branch,role=p['role'],role_fa=p['role_fa'],reference_image=reference,reference_sha256=a['sha256'] if a else None,reference_status=status,planned_flow_name=name,flow_registration='not_verified',source_scene_ids=scenes,spoken_cue_ids=cues,source_block_ids=evidence,performance_status='PROPOSAL derived from editorial screenplay',motivation=p['want'],knowledge=p['knows'],pressure=p['pressure'],performance=p['acting'],flow_character_info=flow,voice_recording=None,voice_and_lip_sync_approved=False)
            records.append(rec)
            photo=f"![{p['en']} reference](../../{reference})" if a else '**MISSING: no image supplied for this branch.**'
            put(folder,f'context/character-info/{id_}.md',f"""# Character info — {p['en']} / {p['fa']}

{display} · RW01 · `{id_}`

{photo}

**Story source:** this branch's `script/episode.json`; scenes {', '.join(scenes)}. This is the new media adaptation, not a manuscript-canon biography. Source-backed action/knowledge is distinguished from **PROPOSAL** performance interpretation. Age, height, birthplace and new history are UNKNOWN unless actually sourced; they are not invented here.

## Identity and reference

- Role: {p['role']}
- نقش: {p['role_fa']}
- Reference status: {status}.
- Exact local file: `{reference or 'MISSING'}`.
- Original source: `{a['original_path'] if a else 'not supplied'}`.
- SHA256: `{a['sha256'] if a else 'not available'}`.
- Planned Flow name: `{name}`; registration not verified. Use @ only after selecting the real project entry.
- Visual lock: {visual}

## Motivation and performance

- Immediate objective (**PROPOSAL reading**): {p['want']}
- Knowledge boundary (**script evidence**): {p['knows']}
- Dramatic pressure (**PROPOSAL reading**): {p['pressure']}
- Relationships: {p['ties']}
- Playable direction (**PROPOSAL**): {p['acting']}
- راهنمای اجرا: {p['acting_fa']}
- Prohibited changes: {p['avoid']}

Exact spoken cues: {', '.join(cues) or 'none; no spoken line is written for this identity'}. Full action anchors and cue IDs are in `manifests/character-info.json`. Quoted wording always comes from the paired script, not from this descriptive card.

## Copy/paste Character info

Use this body if your Flow UI offers a character description/info field; otherwise use it as selected-character context for the Agent. “Character info” is our local document title, not a claim about a verified UI control. Do not paste the whole bible into a short field. Attach the exact identity image separately. A missing-image card is for planning only.

```text
{flow}
```

## Portrait / Create body pair

[Open the candidate pair index](../../portrait-body-candidate-01/PAIR_INDEX.md). Use the exact portrait and its matching full-body file for this identity; original selected references above remain preserved. New corrected art and crop framing retain separate review status.

## Production needs

No new voice, speaking shapes, turnaround, mounted pose, hidden anatomy or moving performance is approved by this card. New RW01 recording, timed performance and mouth/beak alignment remain unestablished. Check branch roadmap and exact shot card before creating a scene frame. Reference selection does not approve every future motion.
""")
            index.append(f"| [{p['en']} / {p['fa']}](character-info/{id_}.md) | {', '.join(scenes)} | {status} | `{name}` |")
        put(folder,'context/CHARACTER_INFO.md',f"""# Character info — {display}

Start here to choose a character, review the reference and copy a compact description. Nine principal identity sheets are provided. {'All nine have supplied visual references.' if not missing else 'Missing matching images: '+', '.join(missing)+'.'} Story source: `script/episode.json`; visual evidence: `manifests/assets.json`. Performance notes are proposals, not additional canon or voice approval.

| Character | Scene coverage | Image status | Planned Flow name |
|---|---|---|---|
"""+'\n'.join(index)+"\n\n[Supporting performers and narrator](SUPPORTING_PERFORMERS.md) · [Roadmap](../ROADMAP.md) · [Step-by-step workflow](../WORKFLOW.md)\n\nThe scene list is an allowed cast inventory: Hushang appears only as a subjective memory, Arash in S09 only as an illustrative context, and Shahrasp in S10 only at the hall return. It does not demand everyone occupy every shot. Body/voice/performance descriptions never replace the exact paired dialogue cues.")
        put(folder,'context/SUPPORTING_PERFORMERS.md',"""# Supporting performer info

These are screenplay roles, not additional selected named portraits. No new identities are invented.

| Role | Source | Character / performance info | Production state |
|---|---|---|---|
| Narrator / راوی | S10 bridge; S11 outcome | Modern explanatory voice outside the ancient story. Distinguish facts, authority and uncertainty; use measured phrasing and readable graphic holds. No on-screen body required. | New exact FA/EN recordings and timings missing; no voice assigned |
| Market voices / بازاریان | S06; market recovery S11 | Different unnamed speakers convey question → inference → personal cost. Shared `extras_market` ID identifies the group, not one person speaking every line. Decide actor assignments before recording. | No selected portraits or actor assignments |
| Riders / سواران | S05–S06 and S11 | Dispatch under Arash, later return at a slower pace. Do not portray an actual battle or confirmed enemy. | Horse/rider references and contact poses missing |
| Charcoal workers | S06 visual reveal | Ordinary kiln work gives the viewer knowledge before the court. No military weapons/costume or new dialogue. | References missing; count and spatial staging need review |
| Guard, judge, apprentice | S09 illustrative inserts | These explain different uses of the same sentence. They are not new events in the main timeline. Hands-only/offscreen staging can be proposed and reviewed. | References/staging missing; no named biographies |

No child/female/elder/vendor identity should be inferred from the group labels. Choose visible extras and voices explicitly where needed. Extra performers must match the selected branch; they must not be duplicated principal portraits.
""")
        put(folder,'manifests/character-info.json',json.dumps(dict(episode_id='RW01',branch=branch,status='local reference and performance planning; no remote registration verified',characters=records),ensure_ascii=False,indent=2))
        ready=f'{len(assets)} supplied principal portraits; '+('all nine principal identities have images.' if not missing else 'matching images still missing for '+', '.join(missing)+'.')
        put(folder,'README.md',f"""# Chapter One — {display}

**Start with [ROADMAP.md](ROADMAP.md), then [WORKFLOW.md](WORKFLOW.md).** This is the RW01 screenplay adaptation. Original references remain preserved; new portrait/full-body candidates are provided separately. No Flow upload has been performed.

| What you need | Open this |
|---|---|
| What should I do next? | [Roadmap and current status](ROADMAP.md) |
| What do I do during one work session? | [Step-by-step workflow](WORKFLOW.md) |
| Do the designs match? | [Design consistency review](DESIGN_CONSISTENCY_REVIEW.md) |
| Portrait and Create body files | [Paired image index](portrait-body-candidate-01/PAIR_INDEX.md) · [visual gallery](portrait-body-candidate-01/gallery.html) |
| Who is each character? | [Character info index](context/CHARACTER_INFO.md) |
| Persian script | [Persian editorial final](script/chapter_one_final_fa.md) |
| English script | [English editorial final](script/chapter_one_final_en.md) |
| Which shot do I work on? | [44 proposed shot briefs](episode-01/PROMPT_INDEX.md) |
| Which exact image do I select? | [Character file/name table](context/CHARACTERS.md) |
| What do I paste into Agent? | [Bootstrap](agent-instructions/00_BOOTSTRAP.md) and [identity rules](agent-instructions/02_IDENTITIES.md) |
| How do I record progress? | [Scene checklist](manifests/scene-progress.csv) and [take/credit log](manifests/operator-log.csv) |

## Current state

{ready} There are eleven editorial scene units, 44 proposed visual beats, 114 aligned FA/EN script blocks and 66 spoken cues per language. Exact times remain TBD. A visual beat may need more than one generated clip; S10 is principally a local graphics/narration edit.

Five Paper Puppet portrait derivatives still need likeness review; two V2 garment derivatives need review in the V2 branch only. Check each character's actual status. Scene backgrounds, props, exact frames, action poses, recordings and final lip-sync remain separate work.

## Today’s next step

{'Review the new Chapar and Arash reference cards, then choose the two-character S11 pilot composition.' if not missing else 'Choose matching V2 Chapar/Arash references if you want full-episode coverage; you can prepare the supplied two-character S11 pilot first.'} Prepare the pilot's table, tablet/cloth and exact start frame before video generation. Use the workflow one shot at a time. Keep styles in separate projects.

For an owner-friendly entry in Persian: ابتدا «Character info» را مرور کن، سپس فقط یک نمای آزمایشی را با پس‌زمینه و وسایلِ مشخص آماده کن. بعد از بررسیِ نتیجه، صحنه‌ها را یکی‌یکی پیش ببر. زمانِ اجرای فارسی و انگلیسی جداگانه اندازه‌گیری می‌شود.

## Boundaries

The original screenplay, manuscripts, source artwork, old film and official handoff are unchanged. Final editorial wording does not establish approved motion/voice/timing. All planned @ names require real project registration. Existing general Veo consistency rules are reconciled in agent-instructions/05_SCOPE_AND_RECONCILIATION.md; do not import old costumes, timing or human-form mentor into this branch.
""")
        put(folder,'ROADMAP.md',f"""# Roadmap — {display}

**Current position: character references and screenplay prepared; scene assets and timed performance not finished.** {ready} This roadmap has no invented dates or credit budget.

| Stage | Your action | Done when | Current state |
|---|---|---|---|
| 1. Lock the writing | Read FA/EN editions; accept/revise by block ID; keep/omit optional final treaty hook | One reviewed text edition per language | Editorial finals prepared; owner read-through pending |
| 2. Lock identities | Review [Character info](context/CHARACTER_INFO.md), exact images and marked derivatives | Each needed identity has an agreed reference hash | {len(assets)}/9 portraits supplied; {'no named identity image missing' if not missing else 'Chapar/Arash missing'} |
| 3. Prepare pilot artwork | Choose RW01-S11-SH01 held seated phase; prepare matched table, tablet/cloth, writing sheet, background and composition | Exact pilot start frame and intended end state reviewed | Scene frame/props not supplied |
| 4. Read and measure | Perform separate FA/EN reads; map approved takes and meaningful pauses to cue IDs | Recorded lengths and reviewed cue placement | No RW01 recordings/timing yet |
| 5. Run one picture pilot | Follow WORKFLOW; use one short supported setting with cost confirmation | Full take and join pass identity/style/contact checks | Not generated; picture test is initially silent |
| 6. Prove speaking performance | Review actual approved voice with mouth/beak plan, using local edit if needed | Actual language/performance test accepted | Not tested; character voice is not exact-audio import |
| 7. Build scene by scene | Finish approved frames/actions for S01 onward; reuse only reviewed references | Each scene has selected takes and passed joins | 44 source-beat briefs prepared; clip splits TBD |
| 8. Assemble both editions | Use measured FA/EN timelines, exact local overlays and audio | Full playback and language QA pass | Not assembled; do not inherit old 251.3s timing |
| 9. Export and archive | Preserve takes, metadata, cue map, actual costs and owner decisions | New named versions and explicit acceptance records | Not exported or promoted |

**Order matters:** review a still composition before spending on motion; prove one restrained pilot before a batch; establish measured speech before final clip lengths. A short silent identity test may precede recording, but it cannot approve dialogue timing.

Start the pilot with Tahmures and Shahrasp seated, fixed mouths, the tablet on the left and a new sheet on the right. Do not attempt the entire long correction in one preset. Once that works, test a transfer or a speaking phase separately. Mounted discovery, crowds and feather-to-bird entrance should follow simpler successful tests.

Read [DESIGN_CONSISTENCY_REVIEW.md](DESIGN_CONSISTENCY_REVIEW.md) before locking references; its rendering/scale suggestions are proposals, not approved identity changes. Read [WORKFLOW.md](WORKFLOW.md) for the repeatable shot procedure. Record progress in manifests/scene-progress.csv; keep actual takes and credit spend in manifests/operator-log.csv. See guides/FLOW_FEATURES.md for dated documentation, not guaranteed account controls.
""")
        put(folder,'WORKFLOW.md',f"""# Workflow — one shot at a time

Use [ROADMAP.md](ROADMAP.md) for the overall order. Use this page for a single session. Select only the **{display}** assets. UI steps are owner actions; no remote operation is performed by these files.

## A. Prepare locally

1. Pick one card from episode-01/PROMPT_INDEX.md. Read its source blocks and exact FA/EN cues. Choose one bounded phase if the card contains several actions.
2. Open context/CHARACTER_INFO.md; confirm each visible identity's reference and status. Scene cast is an allowed set, not a requirement to show everyone.
3. Confirm the location, exact start composition, final pose, hand/prop custody and intended next cut. A portrait is not a finished scene frame. Stop that shot if a required reference is missing; prepare another supported task meanwhile.
4. For spoken work, obtain/review exact recordings and measure language-specific lengths. Keep timing TBD until measured. For the initial silent pilot, keep mouths still and identify it as a picture test only.

## B. Set up the project once

5. Follow [project/character setup](guides/01_PROJECT_AND_CHARACTERS.md). Create or use a dedicated `Tahmures_RW01_{prefix}` project. Recheck actual available controls, settings and costs. Keep generation confirmation Always.
6. Use manifests/upload-plan.csv and the exact assets/characters image path. Compare each imported tile with its local original. The local review montage is not a character master. Do not upload the whole context folder or manuscript sources.
7. Name registered identities using the exact planned names in character cards. If a Character info/description field is offered, paste the compact card body; otherwise use it as selected-character Agent context. Do not invent a UI field or assume copying registered anything. Test actual @ entry resolution.
8. Follow [Agent reconciliation and pilot](guides/02_AGENT_FRAMES_AND_PILOT.md). Use the branch style/identity entries without contradictory older costume/mentor rules. Paste bootstrap plus the one chosen shot, not all 44 cards.

## C. Review a plan, then generate only the intended take

9. Ask the Agent for a plan first: exact references, visible cast, one action, frame continuity, missing inputs and proposed settings. Compare its plan with the card; correct drift before approving any paid operation.
10. Choose Frames for an approved composition or Ingredients for approved reusable references only if the actual model supports it. Use guides/FLOW_FEATURES.md as dated evidence, verify current UI compatibility/cost, and choose one output and a finite retry budget. Never force an entire narrative scene or long speech into one preset.
11. When you approve a specific generation, inspect the complete moving take: face, silhouette, clothes, horns, hand/foot contact, prop count/custody, background and join. Record a failure reason. Change one bounded cause at a time; do not adopt a drifted face as the new master.

## D. Finish locally and record the result

12. Download the actual chosen take. Preserve the raw download; name a working copy using the shot/style/language/revision/take scheme in the card. Enter actual model/settings/reference hashes/prompt/source link/credits and file hash in manifests/operator-log.csv.
13. Use [audio/export/return](guides/03_AUDIO_EXPORT_AND_RETURN.md). Integrate exact separately approved recordings and locally shaped captions/inscriptions. Do not infer an exact-WAV lip-sync workflow from optional Character voice. S10 graphics and long narration are assembled locally with readable holds.
14. Preview the whole shot and adjacent cuts in the measured language edit. Mark the scene row done only after required references, picture/performance, audio and continuity reviews are recorded. Archive failures and selected takes without overwriting older outputs.

## If something goes wrong

| Problem | Next action |
|---|---|
| Character face, costume or style changes | Return to original branch identity; simplify camera/action; retry only after a bounded revised plan |
| Chapar and White Div are merged | Stop; reattach their separate named portraits and source roles |
| Bow/hand flips on Arash | Compare anatomical left/right with the card; review handling/frame before another motion take |
| Exact lettering or Persian shaping fails | Replace with a locally rendered overlay; do not spend repeated takes on generated typography |
| Speech does not fit | Use measured audio to propose more retained phases/cuts; do not speed or rewrite approved speech |
| Mouth/beak does not align | Keep the take provisional; use a reviewed local speaking/compositing plan or regenerate a bounded phase; no final sync claim |
| Required frame/pose/prop is absent | Log the missing item and prepare/review that input before generation |

No paid action, remote registration or acceptance is implied by completion of the local documents.
""")
        rows=[]
        for s in episode['scenes']:
            rows.append(dict(scene_id='RW01-'+s['id'],title=s['title']['en'],missing_named_references=';'.join(c for c in s['cast'] if c in missing),frames='not_prepared',script_review='pending',voice_fa='not_recorded',voice_en='not_recorded',timing='TBD',picture='not_generated',assembly='not_started',owner_decision='',next_action='review script and prepare branch-matched scene frame'))
        path=folder/'manifests/scene-progress.csv'
        if not path.exists():
            with path.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        upload=[dict(local_file=a['packaged_path'],intended_location='Uploads then Characters or Ingredients',planned_name=a['flow_character_name'],scene_usage=';'.join(a['scene_usage']),status='REVIEW DERIVATIVE FIRST' if a['review_required'] else 'SUPPLIED SELECTED REFERENCE; owner checks actual import',uploaded='false') for a in assets]
        with (folder/'manifests/upload-plan.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(upload[0]));w.writeheader();w.writerows(upload)


if __name__ == '__main__':
    raise SystemExit('Use build_packages.py to regenerate the complete synchronized handoff.')
