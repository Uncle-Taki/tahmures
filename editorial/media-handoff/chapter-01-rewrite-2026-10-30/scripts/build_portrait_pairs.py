"""Package exact portrait crops with their source full-body images.

Four built-in image edits are supplied as versioned inputs; this script performs
only deterministic local copying, cropping and labelled review montages.
"""
import csv
import hashlib
import html
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parents[1]
ROOT = next(p for p in BASE.parents if (p / 'meta-prompt.md').exists())
NAMES = {'tahmures':'Tahmures','akvan_div':'Akvan Div','shahrasp':'Shahrasp',
         'hushang':'Hushang','black_div':'Black Div','div_e_sefid':'Div-e Sefid',
         'simurgh_bird':'Simurgh','chapar':'Chapar','arash':'Arash'}
# Source-normalised crop rectangles: full head/headwear, upper shoulders/chest.
# These are image coordinates, not new anatomy or world-scale declarations.
PAPER_CROPS = {
 'tahmures':(.28,.02,.73,.37), 'akvan_div':(.22,0,.79,.40),
 'shahrasp':(.27,.01,.73,.34), 'hushang':(.26,.01,.75,.36),
 'black_div':(.25,.01,.76,.36), 'div_e_sefid':(.25,.01,.75,.35),
 'simurgh_bird':(.31,.015,.91,.39), 'chapar':(.27,.02,.73,.37),
 'arash':(.24,.005,.76,.36)}
V2_CROPS = {c:(.25,0,.75,.36) for c in NAMES}
V2_CROPS['simurgh_bird']=(.28,0,.92,.40)
CORRECTED = {'chapar','arash','div_e_sefid','simurgh_bird'}
# Approximate inspected foot-contact anchors; review lineup before locking scale.
FEET_Y = {'tahmures':.955,'akvan_div':.953,'shahrasp':.963,'hushang':.959,
          'black_div':.963,'div_e_sefid':.945,'simurgh_bird':.921,'chapar':.945,'arash':.937}
RATIOS = {'tahmures':1.0,'shahrasp':1.0,'hushang':1.0,'akvan_div':1.06,
          'black_div':1.04,'div_e_sefid':1.02,'chapar':.96,'arash':1.02,
          'simurgh_bird':1.0}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def fit_white(image, size):
    rgba=image.convert('RGBA')
    tile=Image.new('RGBA',rgba.size,'white');tile.alpha_composite(rgba)
    tile=tile.convert('RGB');tile.thumbnail(size,Image.Resampling.LANCZOS)
    return tile


def main(selected_branch=None):
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
    total=0
    branches=[selected_branch] if selected_branch else ['paper-puppet','illustrated-v2']
    for branch in branches:
        folder=BASE/('flow-'+branch)
        out=folder/'portrait-body-candidate-01';out.mkdir(exist_ok=True)
        assets=json.loads((folder/'manifests/assets.json').read_text())['assets']
        pairs=[];errors=[]
        overrides_path=out/'body-overrides.json'
        overrides=json.loads(overrides_path.read_text())['overrides'] if overrides_path.exists() else {}
        for a in assets:
            id_=a['character'];corrected=branch=='paper-puppet' and id_ in CORRECTED
            source=out/'generated'/(id_+'_harmonized_full_body_v01.png') if corrected else folder/a['packaged_path']
            override=overrides.get(id_)
            if override:
                source=out/override['source']
            target=out/'characters'/id_;target.mkdir(parents=True,exist_ok=True)
            body=target/'full-body.png';portrait=target/'portrait.png'
            shutil.copyfile(source,body)
            with Image.open(body) as im:
                im.load();w,h=im.size
                r=(PAPER_CROPS if branch=='paper-puppet' else V2_CROPS)[id_]
                if override:
                    r=override.get('crop_normalized',r)
                box=tuple(round(v*(w if i%2==0 else h)) for i,v in enumerate(r))
                im.crop(box).save(portrait)
                mode=im.mode;size=list(im.size)
                alpha=list(im.getchannel('A').getextrema()) if 'A' in im.getbands() else None
            pair=dict(id=id_,name=NAMES[id_],branch=branch,
                portrait=str(portrait.relative_to(out)),full_body=str(body.relative_to(out)),
                source=str(source.relative_to(ROOT)),source_sha256=sha(source),
                original_selected_reference=a['original_path'],original_sha256=a['sha256'],
                full_body_sha256=sha(body),portrait_sha256=sha(portrait),
                full_body_dimensions=size,crop_box=list(box),portrait_dimensions=[box[2]-box[0],box[3]-box[1]],
                mode=mode,alpha_extrema=alpha,method='exact pixel crop; full-body byte copy',
                generated_correction=corrected,owner_approved=False,
                generation_record_override=override.get('generation_record') if override else None,
                source_derivative_review_required=a['review_required'],
                approval_scope='new correction candidate' if corrected else 'unchanged source scope; crop framing still needs owner review',
                flow_name=a['flow_character_name'],flow_registration='not_verified',
                scene_usage=a['scene_usage'])
            pairs.append(pair)
            assert sha(body)==sha(source)
            with Image.open(source) as im,Image.open(portrait) as crop:
                assert im.crop(box).mode==crop.mode
                assert im.crop(box).tobytes()==crop.tobytes(),id_
            total+=1
        dump(out/'manifest.json',dict(date='2026-10-30',status='candidate portrait/full-body inputs; no automatic production promotion',pairs=pairs,missing_characters=[] if branch=='paper-puppet' else ['chapar','arash']))
        infos=json.loads((folder/'manifests/character-info.json').read_text())['characters']
        lookup={p['id']:p for p in pairs}
        updated=[]
        for c in infos:
            a=lookup.get(c['id']);record=dict(c)
            if a:
                record.update(reference_image=a['full_body'],reference_sha256=a['full_body_sha256'],portrait_image=a['portrait'],portrait_sha256=a['portrait_sha256'],planned_flow_name=c['planned_flow_name'].replace('RW01_PP_','RW01_PP_C01_').replace('RW01_V2_','RW01_V2_C01_'),reference_status=a['approval_scope'],owner_approved=False)
            updated.append(record)
        dump(out/'character-info.json',dict(status='candidate reference override only; script and role text unchanged',characters=updated))
        source_shots=json.loads((folder/'manifests/shot-to-asset-map.json').read_text())['shots']
        mapped=[]
        for shot in source_shots:
            mapped.append(dict(shot_id=shot['id'],source_shot_card='../episode-01/shots/'+shot['id']+'.md',script_blocks=shot['block_ids'],source_scene=shot['scene'],candidate_inputs=[dict(character=id_,portrait=lookup[id_]['portrait'],full_body=lookup[id_]['full_body'],portrait_sha256=lookup[id_]['portrait_sha256'],full_body_sha256=lookup[id_]['full_body_sha256']) for id_ in shot['cast'] if id_ in lookup],missing_named_reference=shot['missing_character_ids'],scope='Use these image paths instead of original asset paths ONLY for C01; retain source card dialogue/actions/timing unchanged.',generation_authorized_by_this_file=False))
        dump(out/'shot-to-input-map.json',dict(status='candidate reference mapping for existing proposed shots',shots=mapped))
        with (out/'upload-plan.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=['character','stage','image','planned_name','status'])
            writer.writeheader()
            for p in pairs:
                for stage,key in [('Portrait','portrait'),('Create body','full_body')]:
                    writer.writerow(dict(character=p['name'],stage=stage,image=p[key],planned_name=p['flow_name'],status='candidate; review framing and any corrected identity before use'))
        index=['# Portrait and full-body input pairs',
               '\nEach Portrait is cropped from its exact paired full-body file. No separate face was generated. Stage labels come from the owner’s UI description. New corrections remain candidates; source selection is not motion approval.\n',
               '| Character | Portrait stage | Create body stage | Body source |',
               '|---|---|---|---|']
        for p in pairs:
            index.append(f"| {p['name']} | [portrait.png]({p['portrait']}) | [full-body.png]({p['full_body']}) | {'NEW correction candidate' if p['generated_correction'] else 'Unchanged reference copy'} |")
        index+=['\n[Visual gallery](gallery.html) · [Portrait overview](portrait-overview.png) · [Full-body overview](full-body-overview.png)',
                '\nNo V2 Chapar or Arash source exists; their images have not been invented.' if branch=='illustrated-v2' else '\n[Proposed relative-scale lineup](proposed-scale-lineup.png): presentation ratios are proposals, not manuscript facts.']
        (out/'PAIR_INDEX.md').write_text('\n'.join(index)+'\n')
        rows=[]
        for p in pairs:
            rows.append(f"<section><h2>{html.escape(p['name'])}</h2><p>{'New corrected candidate' if p['generated_correction'] else 'Existing reference — unchanged body'}</p><figure><img src='{p['portrait']}'><figcaption>Portrait — exact crop</figcaption></figure><figure><img src='{p['full_body']}'><figcaption>Create body — paired full body</figcaption></figure></section>")
        (out/'gallery.html').write_text("<!doctype html><meta charset='utf-8'><title>Character reference pairs</title><style>body{font:16px Arial;margin:24px;background:#eee}section{background:white;padding:20px;margin:16px 0}figure{display:inline-block;vertical-align:top;margin:10px}img{max-width:420px;max-height:600px;object-fit:contain}figcaption{padding:10px}</style><h1>Portrait / Create body — candidate references</h1><p>Review framing and corrected identities before generation. Originals are preserved.</p>"+''.join(rows))
        for kind,key in [('portrait','portrait'),('full-body','full_body')]:
            cols=3;cellw=420;cellh=540
            sheet=Image.new('RGB',(cols*cellw,((len(pairs)+cols-1)//cols)*cellh+45),'#f5f3ee')
            draw=ImageDraw.Draw(sheet);draw.text((12,12),'CANDIDATE REFERENCE OVERVIEW - labels belong to review sheet only',fill='black',font=font)
            for i,p in enumerate(pairs):
                with Image.open(out/p[key]) as im:tile=fit_white(im,(cellw-24,cellh-74))
                x=(i%cols)*cellw;y=(i//cols)*cellh+45
                sheet.paste(tile,(x+(cellw-tile.width)//2,y+(cellh-60-tile.height)//2))
                draw.text((x+12,y+cellh-55),p['name'],fill='black',font=font)
                draw.text((x+12,y+cellh-30),'CORRECTION CANDIDATE' if p['generated_correction'] else 'SOURCE BODY / EXACT CROP',fill='#555555',font=font)
            sheet.save(out/(kind+'-overview.png'))
        if branch=='paper-puppet':
            # A proposed staging scale with a common foot baseline. No cm/metres,
            # exact anatomy ratios or canonical heights are inferred from art.
            sheet=Image.new('RGB',(600*len(pairs),1080),'#e7e5df');draw=ImageDraw.Draw(sheet)
            draw.text((20,15),'PROPOSED SCENE SCALE - NOT CANON / NOT AN APPROVED COMPOSITED SCENE',fill='black',font=font)
            draw.text((20,42),'Tahmures = 1.00; ratios are a presentation proposal. Entire figures scaled uniformly, not stretched.',fill='black',font=font)
            baseline=930
            for i,p in enumerate(pairs):
                with Image.open(out/p['full_body']) as im:
                    w,h=im.size
                    # Source border crop removes only outer backdrop, retaining
                    # complete headwear, tail, feet and equipment.
                    upper=0;lower=h
                    body=im.crop((0,upper,w,lower))
                    target_h=round(820*RATIOS[p['id']]);target_w=round(w/h*target_h)
                    tile=fit_white(body,(target_w,target_h))
                x=i*600+(600-tile.width)//2
                sheet.paste(tile,(x,baseline-round(tile.height*FEET_Y[p['id']])))
                draw.text((i*600+20,1030),p['name']+' / '+str(RATIOS[p['id']]),fill='black',font=font)
            draw.line((0,baseline,sheet.width,baseline),fill='#555555',width=2)
            sheet.save(out/'proposed-scale-lineup.png')
            dump(out/'proposed-scale-ratios.json',dict(status='PROPOSAL; frame-to-frame staging reference, not canonical height',basis='Tahmures displayed source image height = 1.0; includes source border; approximate manually reviewed foot-contact anchors. No pixels are cropped from full figures.',foot_anchor_y=FEET_Y,ratios=RATIOS,requires_owner_review=True))
        dump(out/'validation.json',dict(status='PASS',pairs=len(pairs),checks=['all images decode','source/full-body byte hashes match','portrait pixels equal exact source crop','crop rectangles recorded','alpha mode preserved','source selection versus new corrections distinguished'],limits='No human framing/identity approval or motion/lip-sync validation implied.'))
        (out/'README.md').write_text(f"# {branch} — Portrait / Create body candidates\n\n{len(pairs)} complete pairs: one head/upper-body portrait and one full-body PNG per available identity. Open [PAIR_INDEX.md](PAIR_INDEX.md) or [gallery.html](gallery.html).\n\n"+
            ('Four Paper Puppet bodies are new correction candidates: Chapar, Arash, Div-e Sefid and Simurgh. Five use untouched reference bodies. Portraits are exact crops of the paired file, including the corrected bodies. See generation-record.json for every actual built-in image_gen prompt and original output path.\n\n' if branch=='paper-puppet' else 'All seven bodies are unchanged source copies. This task does not redesign V2. Chapar and Arash V2 remain missing.\n\n')+
            'Select `characters/<id>/portrait.png` for your reported Portrait stage and the matching `full-body.png` for Create body. Never mix a portrait from an older source with a corrected candidate body. Review crop/headwear/beak completeness in the gallery. Full-body originals and old handoff assets remain unchanged. No Flow upload, voice or video generation, commit or push.\n')
    print(json.dumps(dict(pairs=total,portrait_files=total,full_body_files=total,generated_corrections=4),indent=2))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--branch',choices=['paper-puppet','illustrated-v2'])
    args=parser.parse_args()
    main(args.branch)
