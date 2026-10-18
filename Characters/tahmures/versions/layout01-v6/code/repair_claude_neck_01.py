#!/usr/bin/env python3
"""CL-NECK-01 bounded v6 repair; run only in the copied v6 candidate."""
import hashlib, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

C=Path(__file__).resolve().parents[1]; V5=C.parent/'layout01-v5'; V2=C.parent/'layout01-v2'; SIZE=(1086,1448)
# Exterior hair locks trace from v5's side masses and wrap their protected tips
# into one continuously tapering silhouette. No existing v5 alpha is removed.
P={
 # Broad continuations sit behind head_base: their inner edge is deliberately
 # occluded by the unchanged neck layer, while the exposed edge rounds each
 # formerly stepped side mass into one short, tapered lock.
 'left':[(458,320),(458,340),(460,353),(464,365),(470,374),(477,380),(484,382),(491,380),(497,374),(500,366),(499,354),(496,342),(491,330),(487,320)],
 'right':[(612,320),(612,340),(610,353),(606,365),(600,374),(593,380),(586,382),(579,380),(573,374),(570,366),(571,354),(574,342),(579,330),(583,320)]}
def dig(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x): p.write_text(json.dumps(x,indent=2)+"\n")
def contour():
 box=(458,320,614,384); s=8; hi=Image.new('L',((box[2]-box[0])*s,(box[3]-box[1])*s)); d=ImageDraw.Draw(hi)
 for q in P.values(): d.polygon([((x-box[0])*s,(y-box[1])*s) for x,y in q],fill=255)
 o=np.zeros((1448,1086),np.uint8); o[box[1]:box[3],box[0]:box[2]]=np.array(hi.resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)); return o
def compose(S,order,move=None,dx=0,dy=0):
 out=Image.new('RGBA',SIZE)
 for k in order:
  im=Image.fromarray(S[k],'RGBA')
  if k==move:
   q=Image.new('RGBA',SIZE);q.paste(im,(dx,dy));im=q
  out=Image.alpha_composite(out,im)
 return out
def plate(images,labels,box,z,path,bg='light'):
 w,h=(box[2]-box[0])*z,(box[3]-box[1])*z; can=Image.new('RGB',(w*len(images),h+34),(245,243,235)); dr=ImageDraw.Draw(can)
 for i,(im,lab) in enumerate(zip(images,labels)):
  crop=im.crop(box).resize((w,h),Image.Resampling.NEAREST); tile=Image.new('RGBA',(w,h),(245,243,235,255) if bg=='light' else (25,25,29,255))
  if bg=='checker':
   td=ImageDraw.Draw(tile)
   for y in range(0,h,16):
    for x in range(0,w,16):
     if (x//16+y//16)%2: td.rectangle((x,y,x+15,y+15),fill=(180,180,180,255))
  tile.alpha_composite(crop);can.paste(tile.convert('RGB'),(i*w,34));dr.text((i*w+4,7),lab,fill=(0,0,0))
 path.parent.mkdir(parents=True,exist_ok=True);can.save(path)
def main():
 m=json.loads((C/'manifest.json').read_text()); source=np.array(Image.open(V2/'source/approved_master.png').convert('RGBA'))
 S={r['id']:np.array(Image.open(C/r['path']).convert('RGBA')).copy() for r in m['sprites']}; old=np.array(Image.open(V5/'head/hair_back.png').convert('RGBA')).copy(); S['hair_back']=old.copy(); q=contour(); hair=S['hair_back']; yy,xx=np.indices(q.shape); supp=q>0; tone=np.stack([43+1.2*np.sin((xx-465)/3.7),31+.8*np.sin((xx-465)/3.7),27+.6*np.sin((xx-465)/3.7)],2)
 # The whole supersampled local continuation is reconstructed. max preserves all v5 coverage.
 hair[:,:,:3][supp]=np.round(tone[supp]).astype(np.uint8); hair[:,:,3]=np.maximum(hair[:,:,3],q); S['hair_back']=hair
 Image.fromarray(hair,'RGBA').save(C/'head/hair_back.png');Image.fromarray(hair[:,:,3],'L').save(C/'masks/hair_back.png')
 prior=np.array(Image.open(V5/'provenance/hair_back__reconstructed.png').convert('L'))>0;vis=hair[:,:,3]>0;ret=np.all(hair[:,:,:3]==source[:,:,:3],2)&(hair[:,:,3]<=source[:,:,3]);rec=vis&(prior|supp|~ret);src=vis&~rec
 Image.fromarray(np.where(src,255,0).astype(np.uint8),'L').save(C/'provenance/hair_back__source.png');Image.fromarray(np.where(rec,255,0).astype(np.uint8),'L').save(C/'provenance/hair_back__reconstructed.png')
 chalpha=(hair[:,:,3]>old[:,:,3]); record={'repair':'CL-NECK-01','base':'layout01-v5','component':'head/hair_back.png','bbox':[458,320,614,384],'contours_master_coordinates':P,'method':'8x supersampled manually traced continuous tapered exterior hair locks; alpha=max(v5 alpha, contour alpha)','changed_alpha_pixels':int(chalpha.sum()),'changed_or_recoloured_pixels':int(np.any(hair!=old,2).sum()),'added_alpha_sum':int(np.maximum(hair[:,:,3].astype(int)-old[:,:,3].astype(int),0).sum()),'removed_alpha_pixels':0,'provenance':'All contour-support RGB and alpha are reconstructed; pre-existing source/reconstructed partition remains retained elsewhere.'};dump(C/'neck-repair-record.json',record)
 for r in m['sprites']:
  if r['id']=='hair_back':
   r['sha256']=dig(C/r['path']);r['mask_sha256']=dig(C/r['mask_path']);r['alpha_bounding_rect']=list(Image.fromarray(hair[:,:,3],'L').getbbox());r['provenance']['reconstruction_method']='CL-NECK-01: manually traced 8x-supersampled tapered lower exterior hair locks; all added or recoloured RGB/alpha is reconstructed, not extracted source pixels.';r['provenance']['alpha_edge_modifications']='Only x=458–613,y=320–383 lower exterior hair: alpha=max(v5 alpha, traced antialiased contour); no alpha removed. See neck-repair-record.json.'
 m['version']='layout01-v6';m['revision']='Bounded CL-NECK-01 exterior neck/hair contour repair from immutable layout01-v5; mouth and facial work retained byte-identically.';m['repair_regions']={'CL-NECK-01':record,'unchanged_from_v5':'All exported sprites except hair_back; head_base and visible_head_domain retained byte-identically.'};m['known_limitations']=['CANDIDATE; no Claude acceptance or human visual approval.','CL-NECK-01 repairs only the bounded lower exterior hair contour; no body or garment is supplied.','Front-view only. Tested patch ±2px XY and moustache ±1px XY; no arbitrary rotation or perspective.','The lip opening is a restrained technical test, not a production speech viseme.','No Godot, body/arms, speech/audio or video asset in this phase.'];dump(C/'manifest.json',m)
 rendered={}
 for st,g in [('mouthless','puppet_core'),('neutral','puppet_core_neutral'),('open_test','puppet_core_open_test')]:
  im=compose(S,m['render_groups'][g]['layer_order']);im.save(C/m['previews'][st]);rendered[st]=im
 stress=json.loads((C/'stress-tests.json').read_text())
 for sam in stress['samples']: compose(S,m['render_groups'][sam['render_group']]['layer_order'],sam['moved_sprite'],sam['offset_px']['x'],sam['offset_px']['y']).save(C/sam['path'])
 domain=np.array(Image.open(C/'masks/visible_head_domain.png').convert('L')); eroded=np.array(Image.fromarray(domain).filter(ImageFilter.MinFilter(3)))>0
 def metrics(a): return {'new_fully_transparent_interior':int((eroded&(source[...,3]>0)&(a[...,3]==0)).sum()),'alpha_below_250_where_source_opaque':int((eroded&(source[...,3]>=250)&(a[...,3]<250)).sum())}
 for sam in stress['samples']: sam['coverage']=metrics(np.array(Image.open(C/sam['path']).convert('RGBA')))
 stress['all_coverage_pass']=all(not any(sam['coverage'].values()) for sam in stress['samples']);stress['revision']='v6 CL-NECK-01: v5 offsets retained; all stress renders regenerated and coverage recomputed after bounded hair-contour repair.';dump(C/'stress-tests.json',stress)
 p=C/'previews/plates';master=Image.fromarray(source,'RGBA');plate([master]+list(rendered.values()),['source','A mouthless','B neutral','C open test'],(350,0,730,432),1,p/'D_source_comparison.png')
 for bg in ['light','dark','checker']:
  plate(list(rendered.values()),['A','B','C'],(350,0,730,432),1,p/f'D_head_100_{bg}.png',bg);plate(list(rendered.values()),['A','B','C'],(440,300,640,400),4,p/f'D_neck_{bg}.png',bg)
 plate(list(rendered.values()),['A mouthless','B neutral','C open test'],(440,300,640,400),5,p/'D_neck_zoom.png');plate([Image.fromarray(old,'RGBA'),Image.fromarray(hair,'RGBA')],['v5 hair_back','v6 hair_back'],(455,315,620,380),5,p/'F_neck_hair_component_comparison.png','checker');plate([Image.fromarray(old[:,:,3],'L').convert('RGBA'),Image.fromarray(hair[:,:,3],'L').convert('RGBA'),Image.fromarray(q,'L').convert('RGBA')],['v5 alpha','v6 alpha','contour alpha'],(455,315,620,380),5,p/'F_neck_alpha_contour.png');plate([Image.open(V5/'previews/neutral.png').convert('RGBA'),rendered['neutral']],['v5 neutral','v6 neutral'],(440,300,640,400),5,p/'F_neck_v5_v6_neutral.png','checker')
 print(json.dumps(record,indent=2))
if __name__=='__main__': main()
