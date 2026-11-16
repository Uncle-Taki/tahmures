"""Build two local context packages from RW01 bilingual editorial data.

No provider calls, uploads, image generation, or original-source edits.
"""
import csv
import hashlib
import html
import io
import json
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = next(p for p in BASE.parents if (p / 'meta-prompt.md').exists())
SCRIPT = ROOT / 'playscript/chapter-01-final-2026-10-30'
DATE = '2026-10-30'
STATUS = 'EDITORIAL FINAL FOR OWNER REVIEW; NOT A FINAL PICTURE, AUDIO OR TIMING APPROVAL'
NAMES = {
 'tahmures': ('طهمورث', 'Tahmures'), 'shahrasp': ('شهراسب', 'Shahrasp'),
 'hushang': ('هوشنگ', 'Hushang'), 'akvan_div': ('اکوان دیو', 'Akvan Div'),
 'black_div': ('دیو سیاه', 'Black Div'), 'div_e_sefid': ('دیو سفید', 'Div-e Sefid'),
 'simurgh_bird': ('سیمرغ', 'Simurgh'), 'chapar': ('چاپار', 'Chapar'),
 'arash': ('آرش', 'Arash'), 'extras_riders': ('سواران', 'Riders'),
 'extras_market': ('بازاریان', 'Market voices'), 'narrator': ('راوی', 'Narrator')}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(folder, name, content):
    p = folder / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


def js(folder, name, obj):
    write(folder, name, json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def csvfile(folder, name, rows, fields):
    if name=='manifests/operator-log.csv' and (folder/name).exists():
        return  # Preserve owner-entered takes and spending across rebuilds.
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields)
    writer.writeheader(); writer.writerows(rows)
    write(folder, name, stream.getvalue())


def md(folder, name, body):
    write(folder, name, body + '\n')


BRANCHES = {
 'paper-puppet': {
  'source':'Characters/selected-paper-cut-cast-01', 'display':'Paper Puppet', 'prefix':'PP',
  'style':'Handcrafted flat paper-puppet illustration with angular cut-paper silhouettes, visible paper grain, restrained layered colour shapes and shallow planar overlap. Preserve the supplied portrait proportions and edge character. Treat the references as flat raster designs, not separated rigs. No glossy 3D, photorealism, volumetric characters or rounded cartoon redraw.',
  'descriptors':{
   'tahmures':'Long oxblood-red royal robe, cream/gold edging and gold crown; dark beard. Do not import the blue V2 coat or its trouser edit.',
   'akvan_div':'Slender angular horned figure in long green/cream/rust/gold costume; preserve face, horns and long silhouette from the selected master, not V2 turquoise cartoon skin or new trousers.',
   'shahrasp':'Dark green formal cap, angular green/cream/rust ministerial layers; preserve the selected right-board identity.',
   'hushang':'Elder royal in oxblood robe, crown and long silver-streaked beard. Used only as an explicitly subjective memory/image of a handwriting association; not a courier or literal ghost.',
   'black_div':'Broad upward horns, dark warm complexion and beard, ochre patterned vest and dark trousers. Literal and competent, not an evil silhouette.',
   'div_e_sefid':'Pale/silver-haired slender figure, blue-grey and cream robes; exactly two continuous ivory horns with intact tips and distinct roots.',
   'simurgh_bird':'Long-necked, long-legged blue/teal/gold bird with a long straight beak and right-facing three-quarter view. Never the short-beaked V2 bird or a humanoid.'}},
 'illustrated-v2': {
  'source':'Characters/selected-illustrated-cast-v2-01', 'display':'Illustrated V2', 'prefix':'V2',
  'style':'Outlined, softly shaded 2D storybook cartoon illustration. Match the supplied rounded facial proportions, clean dark outlines, painted colour and material detail. Preserve each exact supplied identity. No paper-cut angular redraw, realistic humans, 3D plastic figures or borrowing Paper Puppet designs.',
  'descriptors':{
   'tahmures':'Blue/gold long outer coat, cream tunic ending near knees, loose warm-brown trousers with gathered/tapered ankles, unchanged shoes. Current trouser derivative needs owner review. Real alpha background, not a black backdrop.',
   'akvan_div':'Turquoise/blue-green skin, dark long hair and horns, green outer garment, knee-length cream tunic, loose brown trousers. Current trouser derivative needs owner review.',
   'shahrasp':'Rounded outlined ministerial face, moustache, green/cream/rust layers and gold trim. Do not substitute Paper Puppet cap/silhouette.',
   'hushang':'Supplied older royal identity with oxblood/gold garment, crown, long dark/silver-streaked beard. No courier or actual supernatural apparition is implied.',
   'black_div':'Dark charcoal skin, horns, black hair/beard, ochre fastened vest and dark trousers. Preserve rounded face and exact horn shapes; no exaggerated villain motion.',
   'div_e_sefid':'Supplied pale, white-haired, pointed-ear horned identity in blue-grey/cream robes. Preserve its exact older facial proportions and modest horn geometry; do not import the Paper Puppet younger face or enlarged horns.',
   'simurgh_bird':'Rounded large-headed blue/teal/gold bird with short curved beak, crest and feathered silhouette. Never lengthen it into the Paper Puppet crane-like shape or turn it human.'}}
}


def screenplay(episode, language, markdown=True):
    name_index = 0 if language == 'fa' else 1
    title = episode['title'][language]
    out = [('# ' if markdown else '') + title,
           'نسخهٔ نهایی ویراستاری برای بازبینی نویسنده؛ زمان‌بندی و اجرای نهایی هنوز تأیید نشده است.' if language == 'fa' else STATUS,
           'روایت آموزشیِ تألیفی؛ بازسازی تاریخی یا ترجمهٔ شاهنامه نیست.' if language == 'fa' else 'Original teaching fiction, not history or reconstructed Shahnameh.', '']
    for scene in episode['scenes']:
        out += [f"{'## ' if markdown else ''}{scene['id']} — {scene['title'][language]}",
                f"{scene['location'][language]} | {scene['time'][language]}", '']
        for b in scene['blocks']:
            if b['type'] in ['dialogue','narration']:
                speaker=NAMES.get(b.get('speaker'), (b.get('speaker',''),)*2)[name_index]
                out += [(f'**{speaker}:** ' if markdown else speaker+': ') + b[language], '']
            elif b['type']=='overlay':
                out += [('نوشتهٔ روی تصویر: ' if language=='fa' else 'On-screen text: ') + b[language], '']
            else: out += ['['+b[language]+']','']
    return '\n'.join(out)+'\n'


def groups(scene):
    """An action-led visual beat with its following exact utterances/overlays.

    No duration is inferred from word count and no old scene/cue ID is reused.
    """
    result=[]; current=[]
    for b in scene['blocks']:
        if b['type']=='action' and current:
            result.append(current);current=[]
        current.append(b)
    if current:result.append(current)
    return result


def main():
    episode=json.loads((SCRIPT/'episode.json').read_text())
    for lang in ['fa','en']:
        write(SCRIPT, f'chapter_one_final_{lang}.md', screenplay(episode,lang,True))
        write(SCRIPT, f'chapter_one_final_{lang}.txt', screenplay(episode,lang,False))
    # Readable bilingual semantic review; stable IDs remain out of spoken text.
    rows=[]
    for s in episode['scenes']:
        for b in s['blocks']:
            rows.append(f"<tr><td><bdi>{html.escape(b['id'])}</bdi><br>{html.escape(b['type'])}<br>{html.escape(str(b.get('speaker') or ''))}</td><td lang='fa' dir='rtl'>{html.escape(b['fa'])}</td><td lang='en' dir='ltr'>{html.escape(b['en'])}</td></tr>")
    write(SCRIPT,'bilingual_review.html',"<!doctype html><meta charset='utf-8'><title>RW01 bilingual review</title><style>body{font-family:Tahoma,Arial,sans-serif;margin:24px}table{width:100%;border-collapse:collapse}td{border:1px solid #ccc;padding:12px;vertical-align:top;line-height:1.8}td:first-child{width:14%;font-size:12px}td:nth-child(2),td:nth-child(3){width:43%}</style><h1>RW01 — bilingual editorial review</h1><p>Editorial final for owner review. No picture, voice or timing approval inferred.</p><table>"+''.join(rows)+"</table>")
    js(SCRIPT,'bilingual-parity-map.json', {'episode_id':'RW01','language_source':'author Persian rewrite; editorial paired FA/EN','status':STATUS,'blocks':[{'id':b['id'],'scene':s['id'],'speaker':b.get('speaker'),'type':b['type'],'fa':b['fa'],'en':b['en']} for s in episode['scenes'] for b in s['blocks']]})
    spoken=[dict(id=b['id'],scene=s['id'],speaker=b['speaker'],fa=b['fa'],en=b['en'],recording_fa=None,recording_en=None,duration_fa='TBD',duration_en='TBD',performance_approved=False,lip_sync_approved=False) for s in episode['scenes'] for b in s['blocks'] if b['type'] in ['dialogue','narration']]
    js(BASE,'text-overlays.json',{'episode_id':'RW01','status':'exact language text for LOCAL overlays; not generated lettering','overlays':[dict(b,scene=s['id']) for s in episode['scenes'] for b in s['blocks'] if b['type']=='overlay']})
    shotlist=[]
    for s in episode['scenes']:
        for i,blocks in enumerate(groups(s),1):
            id_=f"RW01-{s['id']}-SH{i:02}"
            actions=[b for b in blocks if b['type']=='action']
            action=actions[0]['en'] if actions else ('Present the exact local engineering graphic for this beat.' if s['id']=='S10' else 'Hold the approved scene composition for the attached cue.')
            shotlist.append(dict(id=id_,scene=s['id'],source_scene=s['source_scene'],block_ids=[b['id'] for b in blocks],action=action,cast=s['cast'],location=s['location'],time=s['time'],cue_ids=[b['id'] for b in blocks if b['type'] in ['dialogue','narration']],overlay_ids=[b['id'] for b in blocks if b['type']=='overlay'],source='playscript/chapter_one_persian.txt',start='TBD',end='TBD',duration='TBD',generation_duration='TBD',production_approved=False))
    js(BASE,'shot-plan.json',{'episode_id':'RW01','status':'proposed visual coverage of the editorial-final screenplay','shots':shotlist})
    js(BASE,'dialogue-audio-map.json',{'episode_id':'RW01','status':STATUS,'old_recordings_reused':False,'cues':spoken})
    csvfile(BASE,'scene-map.csv',[dict(scene=s['id'],original_author_scene=s['source_scene'],title_fa=s['title']['fa'],title_en=s['title']['en'],cast=';'.join(s['cast']),start='TBD',duration_fa='TBD',duration_en='TBD') for s in episode['scenes']],['scene','original_author_scene','title_fa','title_en','cast','start','duration_fa','duration_en'])
    for key,branch in BRANCHES.items():
        folder=BASE/('flow-'+key)
        source=ROOT/branch['source'];source_manifest=json.loads((source/'manifest.json').read_text())
        assets=[]
        for c in source_manifest['characters']:
            character=c['id'].replace('-','_')
            original=source/c['file'];output='assets/characters/'+original.name
            (folder/'assets/characters').mkdir(parents=True,exist_ok=True)
            shutil.copyfile(original,folder/output)
            from PIL import Image
            with Image.open(original) as im:
                im.load();alpha=im.getchannel('A').getextrema() if 'A' in im.getbands() else None
                dims=list(im.size);fmt=im.format;mode=im.mode
            assets.append(dict(id=branch['prefix']+'-'+character,character=character,packaged_path=output,original_path=str(original.relative_to(ROOT)),source_manifest=branch['source']+'/manifest.json',sha256=sha(original),dimensions=dims,format=fmt,mode=mode,alpha_extrema=alpha,source_selection_scope=c.get('selection_status',c.get('selection_scope')),source_image_status=c['image_status'],review_required=c.get('requires_new_likeness_review',False) or c.get('requires_garment_review',False),flow_character_name='RW01_'+branch['prefix']+'_'+character,registered=False,uploaded=False,motion_approved=False,description=branch['descriptors'][character],scene_usage=[s['id'] for s in episode['scenes'] if character in s['cast']],local_preparation_authorized=True,external_upload_performed=False,external_upload_authorization='not exercised; owner reviews eligible references before manual upload',rights_provenance='owner-supplied project reference; source manifest retained; independent rights documentation not found'))
        for asset in assets:
            assert asset['sha256']==next(c['sha256'] for c in source_manifest['characters'] if c['id'].replace('-','_')==asset['character'])
        if key=='paper-puppet':
            additions_path=BASE/'manifests/paper-puppet-cast-additions.json'
            additions=json.loads(additions_path.read_text())['characters']
            for c in additions:
                original=ROOT/c['original_path'];output='assets/characters/'+c['packaged_name']
                assert sha(original)==c['sha256'], 'Changed supplied portrait: '+c['id']
                shutil.copyfile(original,folder/output)
                with Image.open(original) as im:
                    im.load();alpha=list(im.getchannel('A').getextrema()) if 'A' in im.getbands() else None
                    dims=list(im.size);fmt=im.format;mode=im.mode
                assets.append(dict(id='PP-'+c['id'],character=c['id'],packaged_path=output,original_path=c['original_path'],source_manifest=str(additions_path.relative_to(ROOT)),sha256=c['sha256'],dimensions=dims,format=fmt,mode=mode,alpha_extrema=alpha,source_selection_scope=c['selection_status'],source_image_status=c['image_status'],review_required=c['review_required'],flow_character_name='RW01_PP_'+c['id'],registered=False,uploaded=False,motion_approved=False,description=c['description'],scene_usage=[s['id'] for s in episode['scenes'] if c['id'] in s['cast']],local_preparation_authorized=True,external_upload_performed=False,external_upload_authorization='not exercised; owner manual action',rights_provenance='owner-supplied portrait; independent rights documentation not found'))
        available={a['character'] for a in assets}
        missing_principals=[c for c in ['chapar','arash'] if c not in available]
        missing_note=('Chapar and Arash are MISSING in this selected branch.' if missing_principals else 'Chapar and Arash now have owner-supplied Paper Puppet references. Their new action/mounted/speaking states still need review.')
        js(folder,'manifests/assets.json',{'branch':key,'status':'physically copied local references; selection and derivative review kept distinct','assets':assets,'missing_characters':missing_principals,'missing_other_assets':['matching environments','river tablet/cloth/seal','courier and messenger horse poses','riders/market extras; charcoal workers; illustrative guard/judge/apprentice','feather/brazier/summoning transition','speaking and expression states','start/end scene frames']})
        (folder/'script').mkdir(parents=True,exist_ok=True)
        for lang in ['fa','en']:
            shutil.copyfile(SCRIPT/f'chapter_one_final_{lang}.md',folder/f'script/chapter_one_final_{lang}.md')
        shutil.copyfile(SCRIPT/'episode.json',folder/'script/episode.json')
        js(folder,'episode-01/dialogue-audio-map.json',{'episode_id':'RW01','status':STATUS,'cues':spoken,'old_recordings_reused':False})
        js(folder,'episode-01/scene-index.json',{'episode_id':'RW01','source_author_scene_count':8,'editorial_scene_count':len(episode['scenes']),'timing':'TBD for each language; no previous production timing inherited','scenes':episode['scenes']})
        js(folder,'manifests/shot-to-asset-map.json',{'branch':key,'shots':[dict(s,asset_ids=[a['id'] for a in assets if a['character'] in s['cast']],missing_character_ids=[c for c in s['cast'] if c in missing_principals],style=branch['style']) for s in shotlist]})
        # Technical review montage of existing images; no new artwork is generated.
        from PIL import ImageDraw, ImageFont
        sheet=Image.new('RGB',(210*len(assets),440),'white'); draw=ImageDraw.Draw(sheet)
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',11)
        for i,a in enumerate(assets):
            with Image.open(folder/a['packaged_path']) as original:
                tile=Image.new('RGBA',original.size,'white');tile.alpha_composite(original.convert('RGBA'))
                tile=tile.convert('RGB');tile.thumbnail((198,340))
                sheet.paste(tile,(i*210+(210-tile.width)//2,30+(340-tile.height)//2))
            label=a['id']+'\n'+('REVIEW DERIVATIVE' if a['review_required'] else 'SUPPLIED / SELECTED')
            draw.multiline_text((i*210+5,375),label,fill='black',font=font)
        draw.text((5,5),'LOCAL REVIEW CONTACT SHEET - not a Flow identity master. Exact sources and hashes: manifests/assets.json',fill='black',font=font)
        sheet.save(folder/'assets/local-review-contact-sheet.png')
        assettable='\n'.join(f"| {NAMES[a['character']][1]} | `{a['packaged_path']}` | `{a['flow_character_name']}` | {'Derivative details pending review' if a['review_required'] else 'Selected/supplied reference; no new motion approval'} |" for a in assets)
        md(folder,'context/CHARACTERS.md',f"# {branch['display']} — character identities\n\nOne active image per identity, second image not supplied. Do not invent a turnaround. All planned @ names require actual registration; none exists remotely by this preparation.\n\n| Identity | Exact local file | Planned Flow name | Scope |\n|---|---|---|---|\n{assettable}\n\n"+'\n\n'.join('### '+NAMES[a['character']][1]+'\n\n'+a['description'] for a in assets)+f"\n\n{missing_note} Hushang is a remembered royal father identity, not a courier. Anonymous riders, horses, merchants, charcoal workers and illustrative guard/judge/apprentice roles need separate matching references or reviewed offscreen/hands-only staging. No borrowing a missing character from the other visual branch. No supplied portrait grants a mounted, wet, turning or speaking pose.\n")
        md(folder,'context/STYLE.md',f"# {branch['display']} — sole style contract for RW01\n\n{branch['style']}\n\nUse only this branch’s reference files. The {len(assets)} source images were visually compared on a contact sheet; portraits are raster images, not editable joints/layers. Match background and prop art to this same treatment before shot generation. No background has yet been selected. Grey portrait backdrops are not story sets. Transparency does not imply separated limbs. Preserve both full horns, facial silhouette, clothing edges and anatomical sides.\n\n"+('All current portraits are opaque RGB; paper texture does not constitute real paper layers.' if key=='paper-puppet' else 'Tahmures has true alpha; remaining images retain opaque grey. Tahmures/Akvan current trouser derivatives await owner garment/likeness review. Do not revert the knee-length inner tunics or transplant these trousers into Paper Puppet.')+"\n")
        md(folder,'context/PRODUCTION_BRIEF.md',f"""# RW01 — {branch['display']} production brief

Source: owner’s `playscript/chapter_one_persian.txt`, polished into eleven editorial units in script/episode.json. Final editorial text is available in Persian and English. This is a new scoped screenplay adaptation, not a replacement of book canon or english-final-03. Original eight scene numbers map to eleven units by splitting the large closing lesson/correction; S01 IDs here mean RW01, not old production S01.

Keep sunset/rain discovery, sunrise inscription deadline, royal city/palace, Shahrasp as minister, Divan House’s three interpretations, White Div delivering to Arash, riders causing a market war rumour, wet accurate Black Div report, Hushang handwriting resemblance as hypothesis, and feather-summoned bird-only Simurgh as mentor. Palace architecture is stylised project fiction; no historical period/date/ritual authenticity is asserted.

Do not replace missing evidence with confidence: damaged seal is not a verified royal order; old handwriting resemblance does not authenticate Hushang’s authorship. Count eleven ordinary charcoal fires, not an actual army. Trace one tablet through every hand and table. Correction is a new authored message, distinct from the found object. Unknown source facts stay unknown.

All modern engineering explanation belongs to the explicit narrator-led bridge, not the ancient characters’ mouths. Preserve both exact language tracks and eight-component formula. Requested result is classification plus identifying missing context, not magically recovering unavailable information. Analogy limits: divs are teaching fiction, not literal software contracts; labels/royal seals are not application permissions or security controls.

No old audio, duration, picture approval or Flow @ registration carries over. All FA/EN performance durations and final timeline remain TBD until separately recorded/reviewed. Scripts are editorial deliverables; picture, action, derivative-likeness and final lip-sync review remain distinct.
""")
        md(folder,'context/CONTINUITY_AND_BLOCKERS.md',f"""# Continuity, version boundaries and blockers

User-authorised rewrite scope: Simurgh bird mentor is now included separately from Div-e Sefid onward messenger; Shahrasp is a minister who records; Hushang is a father/uncertain handwriting association; sunrise replaces the book’s moonrise. These are scoped screenplay choices, not silently migrated book facts. Canon manuscripts, continuity, earlier films, accepted recordings, prior handoffs and cast originals are preserved.

Chapar’s discovery → delivery to Tahmures → Shahrasp → Divan table → Div-e Sefid → Arash is a single-object chain. Any return for the lesson must be shown explicitly or the lesson must use a copied sentence, not teleport the tablet. No second river tablet. Riders dispatch only after Arash receives the message. Closing gates is a precaution that contributes to rumour, not proof of war. Correction must identify recipient, retract the alarm and request acknowledgement; a seal does not guarantee truth.

{missing_note} Remaining gaps: no approved environments/props/horse/crowd/contact poses; no completed RW01 FA/EN voice takes; no lip-sync/time approval; derivative image review as marked in assets manifest. Hushang memory must not become a confirmed ghost, an authenticated ancient author, or a recast courier. No new named cast is created to fill a gap.

Keep any editorial hook addition clearly distinguished from author input; see shared EDITORIAL_NOTES and script blocks. It is a proposed editorial addition until reviewed, not a recorded scene. No exact runtime is inherited from the previous 251.3s film or 48-shot story-room proposal.
""")
        md(folder,'agent-instructions/00_BOOTSTRAP.md',f"""# Bootstrap — planning only

```text
We are planning RW01 Chapter One, {branch['display']} version only. Read the selected branch style and identity images, the single chosen shot card and its exact Persian/English cues. Do not generate, upload, create voices, alter/delete project assets or spend credits. Keep Confirm before generating set to Always. First list the actual attached files, allowed cast, one primary action, object custody, missing references and unresolved timing/performance approvals. Return a shot plan and any blockers. Do not assume local filenames are registered Flow Characters. Wait for my separate approval of an actual generation and its displayed settings/cost.
```
""")
        entries={
          '01_STYLE':branch['style']+' Use only the exact current branch images. Never combine Paper Puppet and Illustrated V2 features. Missing background/action frames must be reported, not invented as approved art.',
          '02_IDENTITIES':'Preserve exact attached faces, costume colours, body proportions, both horns, hair and anatomical sides. Div-e Sefid is the onward messenger; Chapar is a separate courier. Simurgh is a bird mentor, never a messenger substitute or human. Hushang is the father/subjective memory identity, not a courier. '+missing_note+' Never treat a portrait as an approved action frame. Do not duplicate cast or invent turnarounds.',
          '03_STORY_AND_ACTION':'One found river tablet; damaged seal and unknown sender do not grant authority. Three divs are capable and mistaken in different ways. Keep eleven ordinary charcoal fires and the causal chain of delivery, dispatch and market alarm. Preserve the exact RW01 script and source block IDs. One bounded action per clip, stable camera/identity/contact; split a complex source action into reviewed phases instead of promising a whole scene in one generation. No invented war or malevolent-div performance.',
          '04_DIALOGUE_AND_TIMING':'Exact Persian and English script cues are separate language editions, not alternate paraphrases. No previous approved audio is assigned to these rewritten words. All recording paths and timing remain missing/TBD. Prepare silent picture by default, discard generated audio locally, and use separately approved local recordings/native speaking layers. Do not rewrite dialogue, create voices, accelerate speech, claim automatic lip-sync approval or invent Persian text. Exact inscriptions/subtitles/diagrams are local overlays.',
          '05_SCOPE_AND_RECONCILIATION':'Existing Tahmures Veo consistency instructions apply to an older cast/film. Retain general evidence, identity, contact, budget and review discipline, but do not paste old fixed costume colours, ban this new bird mentor, reuse old moonrise/dialogue or treat old timing as RW01. This branch style and new owner rewrite govern this scoped preparation only. Canon/previous media are untouched. Newly generated art, action, voice or final picture is not owner-approved merely because the writing is final.'}
        for file,body in entries.items():
            md(folder,'agent-instructions/'+file+'.md',f"# RW01 {branch['display']} — {file}\n\nTitle: `RW01 {branch['prefix']} {file}`\n\nReference: `{assets[0]['packaged_path']}` for the style entry; `{next(a['packaged_path'] for a in assets if a['character']=='div_e_sefid')}` for identities. Other entries: text-only, no reference image needed; if the actual UI requires one, stop rather than attach an unrelated image.\n\n```text\n{body}\n```\n")
        for shot in shotlist:
            scene=next(s for s in episode['scenes'] if s['id']==shot['scene'])
            selected=[b for b in scene['blocks'] if b['id'] in shot['block_ids']]
            matching=[a for a in assets if a['character'] in shot['cast']]
            reftext='\n'.join(f"- `{a['id']}` → `{a['packaged_path']}`; review required: {a['review_required']}; intended name `{a['flow_character_name']}` (not registered)." for a in matching) or '- No supplied character needed; environment/prop/composition reference still missing.'
            missing=[c for c in shot['cast'] if c in missing_principals]
            text='\n\n'.join(f"**{b['id']} / {b['type']} / {b.get('speaker') or 'stage'}**\n\nFA: {b['fa']}\n\nEN: {b['en']}" for b in selected)
            prompt=f"""RW01 {shot['id']}, {branch['display']} branch. {branch['style']}
Use the attached, owner-selected branch identities and approved exact start composition. Setting: {scene['location']['en']}. Time: {scene['time']['en']}. Cast permitted in this scene: {', '.join(shot['cast'])}. The specific source visual beat is: {shot['action']}
Plan ONE bounded continuous action phase from this beat; if it contains several changes of pose, contact, place or camera, return the necessary phase split for review before generation. Lock the camera to the chosen approved frame. Preserve exact face/clothes/body/horns, background layout, floor contact and prop custody. Never add a second river tablet, a restored seal, confirmed enemy troops, an actual Hushang ghost or a human Simurgh. No cross-branch style features.
Do not produce readable text, subtitles or diagrams; exact FA/EN overlays are added locally. No generated speech, music or lip movement for the initial picture test. Use separate reviewed language recordings later. Missing character/environment/prop/phase/start-frame approval is a blocker, not permission to guess. Do not generate or spend credits until I explicitly approve the final shot plan, actual model/mode/duration/resolution/output count and displayed cost.
"""
            md(folder,'episode-01/shots/'+shot['id']+'.md',f"""# {shot['id']} — {branch['display']}

Source: RW01 editorial script / {scene['id']}, original author scene {scene['source_scene']}, blocks {', '.join(shot['block_ids'])}. This is new proposed coverage, not a shot from the older film. Runtime/cut/recording/start/end: **TBD**. Final script wording does not mean its moving performance is approved.

## Purpose and staged action

Scene: {scene['title']['en']} / {scene['title']['fa']}. Play the source beat below with specific attention to who is trying to change whose action. Preserve visible consequences and distinguish ignorance from deliberate deception. Do not make all divs villains or turn the correction into proof every cost was undone.

Action: {shot['action']}

Start frame: MISSING reviewed exact scene composition; character portraits are identity ingredients, not start frames. End frame: TBD, reviewed pose/custody matching the next shot. New contact/wet/mounted/speaking/wing/fire states need approved support. Locked camera preferred. Large actions require phase splits and handles after measured FA/EN read-through; no word-count fit claim.

## Branch references

{reftext}

Missing selected identities in scene: {', '.join(missing) or 'none among the named supplied principal cast'}. Extras/horses/props/backgrounds are still missing. Only this branch’s physical copies may be selected; no accidental mixing with its sibling. Model suggestion after references are approved: Omni Flash 1.1 Frames for an exact start/end frame or Ingredients for reusable approved references; supported length chosen later. Veo Quality cannot use Ingredients. Capability evidence: guides/FLOW_FEATURES.md. S10-SH01 is a local narration-and-graphics edit, not a single generated clip; split its eight formula components and five review questions into readable local holds after recording. No paid generation is currently performed or authorised by this file.

## Exact paired script block(s)

{text}

Each dialogue/narration block maps to a separate future recording in dialogue-audio-map.json, with no existing WAV. Keep original cue text; use a planned @ name only after actual registration. The scene cast list is an allowed set, not a demand to put every character in every composition. Memory/overlay/vignette material is not an extra person standing in the court.

## Copy/paste planning prompt

```text
{prompt}```

## Review / return

Reject identity/style drift, costume/horn changes, duplicate/teleported tablet, wrong fire count, hand/prop merges, sliding feet, unrequested mouth movement or inaccurate sound/text. Inspect entire moving take normally/slowly and its join. Record PASS/FAIL/NOT VERIFIED plus owner picture/performance decision separately. Missing frame/asset approval keeps this shot blocked. Failed generations are not new identity masters.

Future filename: `RW01_{branch['prefix']}_{shot['scene']}_{shot['id'].split('-')[-1]}_LANG_r01_take01.mp4`; replace LANG with FA or EN only for a real reviewed edition. Save original download, exact prompt/model/settings/reference hashes/source link/actual credits; append operator log. Nothing is automatically synchronized with GitHub.
""")
        md(folder,'episode-01/PROMPT_INDEX.md','# Proposed shot index\n\nEvery action-led script beat is mapped once, with its following exact dialogue/overlays. These cards are not claims of completed clips or final timecoded cuts. Further splitting of difficult multi-phase action remains a reviewed production choice.\n\n'+'\n'.join('- ['+s['id']+'](shots/'+s['id']+'.md)' for s in shotlist))
        md(folder,'episode-01/ASSEMBLY_AND_AUDIO.md',"""# Language, audio and assembly contract

RW01 is a rewrite. Do not bind its cue IDs to old english-final-03 WAVs or the 251.3s edit. Record/review Persian and English independently using the exact paired cue map; no audio generation was performed. Each spoken block has null recording fields and TBD duration. Final source lengths may differ by language; no speeding Persian to match English.

Build a new edit at the chosen agreed frame rate/aspect after read-through. Place picture in the measured language timeline, preserve actor pause/breath/action time, and retain source takes. Captions and exact writing/formula are locally editable overlays; render Persian with correct shaping/RTL. Keep the modern bridge clearly separate from the ancient world. In the first picture pilot lips stay still; silent picture does not constitute completed dialogue. A bird mentor needs separate reviewed beak/performance support if speaking motion is attempted.

Trace the one tablet and message custody at each cut. Hushang mental association is a subjective insert, not co-presence or proof. Prepare explicit masks before any layered compositing; flat raster portraits have no automatic separable limbs or transparent scene video. Render a NEW candidate export, inspect actual codecs/frame rate/frame count/duration/audio streams, then watch/listen fully in each language. Never overwrite existing movies/voice approvals. Preserve downloads and exact source/version/hash/settings/credit records.
""")
        md(folder,'guides/FLOW_FEATURES.md',"""# Public Flow feature check — 2026-10-30

Public support pages read; no authenticated project/account inspected. Capabilities may vary by account/region; always inspect actual controls/costs.

- [Agent](https://support.google.com/flow/answer/17093911?hl=en): project instructions accept reference/guidelines; Always confirmation is available; media generation spends credits.
- [Video](https://support.google.com/flow/answer/16353334?hl=en): Frames uses start/optional end composition; Ingredients uses references; registered names can be @ referenced. These are different controls.
- [Projects](https://support.google.com/flow/answer/16935308?hl=en): Characters accepts one/two images; voice/name step follows; project/asset organisation and downloads are supported. Optional omission of a forced voice is not established; stop and use visual ingredients if registration insists on an unapproved voice.
- [Models](https://support.google.com/flow/answer/16352836?hl=en): Omni Flash 1.1 supports Frames/Ingredients at 4/6/8/10s and edits up to 10s; draft 360p available. Veo Lite/Fast Frames 4/6/8s, Ingredients 8s; Quality Frames 4/6/8s, no Ingredients. Lite extends eligible 8s Veo clips; do not assume all models extend.
- [Editing/scenes](https://support.google.com/flow/answer/16935718?hl=en): Save frame, sequence/trim/preview/download supported; video-to-video uses Omni. A saved frame is a candidate until reviewed, not automatic identity approval.

No exact-WAV-driven lip-sync guarantee is established by these pages. All new speech remains a local recording/edit plan; no prices, balances, automatic synchronization or model-identity guarantees are asserted.\n""")
        md(folder,'guides/01_PROJECT_AND_CHARACTERS.md',f"""# 01 — Create a separate {branch['display']} project (owner steps)

1. Read README, context/CHARACTERS and manifests/assets first. Review marked derivative details before registering identities. Check missing_characters in manifests/assets.json; resolve only the identities still listed. No placeholders.
2. In desktop Flow choose **+ New project**. Name it `Tahmures_RW01_{branch['prefix']}` using the project rename control. Use 16:9 landscape for chosen video settings. Keep the sibling style in another project.
3. Turn **Agent** on; **Settings → Confirm before generating → Always**. Reopen to verify. Record actual credit balance and a finite pilot budget. No generation is authorised by preparing this folder.
4. In **Uploads**, use the offered Upload/Add control or the documented device-file prompt Add route. Select only one exact `assets/characters/` file at a time, reopen the tile, compare identity/crop. Do not upload local review contact sheet, manifests or whole repository.
5. Choose **Characters → New Character**. Upload the one chosen image; use **Add from project** if your UI offers it. That label is account-reported, not guaranteed. One image is supplied per identity; no invented second turnaround. Name from the exact planned name in assets.json.
6. Inspect whether the documented Generate/voice step incurs cost or requires a voice choice. Stop rather than generate a replacement design/voice unintentionally. Only finish **Done** with permitted settings. If optional voice omission is unavailable, use image ingredients for picture-only work.
7. Test @ resolution by selecting the actual entry, not by assuming a copied filename became a Character. Mark registration locally only after observing it. Missing identities stay blocked.

Expected result: clearly separated branch project and reviewed references. If alpha/crop changes in UI, compare with original and defer conversion; do not infer a new identity from a broken preview. Never import sibling references to fix a missing costume/pose. See FLOW_FEATURES for dated official documentation; UI variations must be recorded rather than guessed.
""")
        md(folder,'guides/02_AGENT_FRAMES_AND_PILOT.md',"""# 02 — Instructions, approved frames and one pilot

1. Reconcile the older Tahmures Veo rule using agent-instructions/05_SCOPE_AND_RECONCILIATION. Keep general consistency/review discipline, replace only branch-specific style/role/timing assumptions for this NEW project. Do not keep contradictory old costume colours or “no Simurgh” rules beside the new mentor assignment.
2. With Agent enabled open **Agent instructions → Add instruction**, use each entry title/body, attach a single relevant branch reference where appropriate, and click **Done**. Text-only entries are conditional if your UI requires an image; do not attach an unrelated picture just to fill a field.
3. Paste 00_BOOTSTRAP. Expect a plan and blocker list, not generated media. Provide only one chosen shot’s block IDs, exact references and constraints, never an entire book dump.
4. Select a reviewed exact start composition BEFORE video generation. A full-body portrait is an identity ingredient, not a ready scene frame. Where missing, prepare a keyframe brief from the shot card and review it; this local task has generated none. Do not infer scene approval from a character portrait.
5. In model selector choose **Video → Frames** for a fixed composition or **Video → Ingredients** for reusable references. Choose compatible model, one output, supported length, 16:9, and draft resolution where available; check actual cost. Omni 360p is a reasonable trial when offered. No guarantee of identity or exact runtime.
6. Pilot RW01-S11-SH01’s seated Tahmures/Shahrasp composition, with approved props/frames first. Test a held listening phase, not the complete long spoken message. Lock hands, faces and tablet; animate a small environment/light phase. Inspect full output normally/slowly before requesting acting/contact/speaking. Do not begin with mounted action, crowds or a fire-to-bird transformation.
7. Save the selected first/last frame only after review, then use it as a candidate reference for the next phase. Reject style drift, extra horns, face changes, wrong clothing or duplicated tablet; return to original identity rather than promoting drift.

No actual image/video generation or Flow upload was performed. Exact duration/timing and performance are still TBD. For multi-phase source action, approve a phase split rather than cram all changes into one preset.\n""")
        md(folder,'guides/03_AUDIO_EXPORT_AND_RETURN.md',"""# 03 — Voices, assembly, export and return

1. Use episode-01/dialogue-audio-map.json for exact FA/EN cue text/speaker. No RW01 recording exists. Obtain separately approved performances; do not reuse an old WAV for changed words or create a new voice automatically.
2. Begin with silent picture; discard generated audio locally. Optional Flow Character voice is not import of an exact original WAV and not proof of synchronization. Keep native/local speaking and exact captions as the reliable fallback.
3. After reviewing each take, use clip **More → Add to Scene** where offered; arrange, trim and preview. Keep actual language lengths distinct and preserve the original download/takes. A Scene is a narrative group; many clips may belong to it.
4. For editing an eligible candidate use Omni video-to-video with one bounded correction; Veo extension is a separate model-limited path. Recheck compatibility instead of assuming each model supports both.
5. Download using the asset/scene download controls; verify the real file/container. Save under its RW01/style/scene/shot/language/revision/take name, not an old film output. Record actual source link, prompt/model/settings/date/reference hashes/credits and chosen in/out points in manifests/operator-log.csv.
6. Assemble in a NEW local edit with the measured FA or EN cue map, exact locally rendered text and reviewed timing. Do not overwrite original film/scripts/recordings. Inspect ffprobe metadata and complete playback/listening, including Persian joins and beak/lip alignment.
7. Record PASS/FAIL/NOT VERIFIED for plot, cast, style, anatomy/contact, tablet custody, eleven fires, translation parity, caption/audio timing and ending. Owner reviews actual final art/performance separately from deterministic results.

Use collections for per-scene takes and reviewed references if available; Library/Tools can be optional organisation aids, never required media generators. No automatic Flow-to-repository synchronization exists. Keep a finite retry/credit budget; if a shot cannot preserve identity/contact, simplify staging or retain a reviewed local composition instead of endlessly regenerating.\n""")
        csvfile(folder,'manifests/operator-log.csv',[],['date','shot_id','language','take_id','model','mode','reference_ids','prompt_path','displayed_cost','actual_credits','download_path','sha256','review','owner_decision'])
        md(folder,'README.md',f"""# RW01 — {branch['display']} Flow context

Prepared {DATE} from the new owner Persian rewrite and its polished paired editions. **Local preparation only.** No Flow upload, image/video/voice generation, credit spend, commit or push. Existing book/film/voice/art sources are unchanged.

## Ready locally

- Final editorial Persian/English scripts in `script/`, with exact paired source blocks in `script/episode.json`.
- {len(assets)} byte-identical branch character copies and a visual comparison sheet; `manifests/assets.json` retains selection versus derivative-review status.
- Eleven new editorial scene units and {len(shotlist)} action-led shot cards with exact FA/EN cues, identity links, camera/action plan and missing-frame gates.
- Six Agent instruction files, three numbered operator guides, current official feature links, dialogue/audio and scene/shot manifests, assembly/QA instructions and blank operator log.

## Quick start

1. Review script/chapter_one_final_fa.md and chapter_one_final_en.md.
2. Read context/STYLE, CHARACTERS and CONTINUITY_AND_BLOCKERS; compare the local review sheet.
3. Review derivative likeness/garments as indicated; resolve matching Chapar/Arash and scene frame/prop gaps.
4. Follow guides 01–03 as OWNER steps only after each relevant art/action/timing/voice/spending decision.
5. Open episode-01/PROMPT_INDEX and choose one bounded pilot. Keep Generate confirmation Always.
6. Record/export measured language editions separately; do not import old 251.3s clocks or old voice tracks.

## Limits

Final editorial wording is ready for owner read-through; all moving art, scene references, exact FA/EN runtime, recordings and lip sync still need evidence. Selected source models do not approve every regenerated detail or new pose. {len(assets)} portraits are reference art, not a complete scene library. {missing_note} Remaining gaps: extras/horses/sets/props/turnarounds/speaking states have no branch approval. No Hushang courier substitution. This branch is self-contained for supplied portrait files and script/context planning, not a claim of a finished movie or a complete upload-ready scene library.

The sibling style is a separate production experiment. Do not mix the two character identities, facial proportions, costume palettes, horn shapes or bird anatomy. Read the shared CAST_AND_SCRIPT_ANALYSIS.md for comparison.\n""")
    from build_character_info import build_character_info
    build_character_info(BASE,ROOT,episode)
    print(json.dumps({'editorial_scenes':len(episode['scenes']),'action_led_shots_per_branch':len(shotlist),'spoken_cues_per_language':len(spoken),'branches':list(BRANCHES),'physical_character_copies':sum(len(json.loads((BASE/('flow-'+k)/'manifests/assets.json').read_text())['assets']) for k in BRANCHES)},indent=2))


if __name__=='__main__':main()
