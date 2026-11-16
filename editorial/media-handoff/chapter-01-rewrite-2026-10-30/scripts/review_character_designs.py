"""Local inspection previews and source evidence for a manual design review.

No generation or source art modification. Crops are comparison derivatives only.
"""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE=Path(__file__).resolve().parents[1]

def main():
    for key in ['paper-puppet','illustrated-v2']:
        folder=BASE/('flow-'+key)
        assets=json.loads((folder/'manifests/assets.json').read_text())['assets']
        output=folder/'design-review';output.mkdir(exist_ok=True)
        cols=5 if key=='paper-puppet' else 4
        rows=(len(assets)+cols-1)//cols
        sheet=Image.new('RGB',(cols*260,rows*320+45),'#f8f6f0')
        draw=ImageDraw.Draw(sheet)
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
        draw.text((10,8),'UPPER-BODY COMPARISON - review only, not identity/Portrait masters',fill='black',font=font)
        draw.text((10,25),'Crops fitted for inspection; displayed scale does not establish relative heights.',fill='black',font=font)
        entries=[]
        for i,a in enumerate(assets):
            path=folder/a['packaged_path']
            actual=hashlib.sha256(path.read_bytes()).hexdigest()
            assert actual==a['sha256'],path
            with Image.open(path) as im:
                im.load();w,h=im.size
                box=(round(w*.08),0,round(w*.96),round(h*.39))
                crop=im.crop(box).convert('RGBA')
                tile=Image.new('RGBA',crop.size,'white');tile.alpha_composite(crop)
                tile=tile.convert('RGB');tile.thumbnail((246,270))
            x=(i%cols)*260;y=(i//cols)*320+45
            sheet.paste(tile,(x+(260-tile.width)//2,y+(275-tile.height)//2))
            draw.text((x+8,y+280),a['id'],fill='black',font=font)
            draw.text((x+8,y+299),'EXISTING IMAGE / REVIEW CROP',fill='#555555',font=font)
            entries.append(dict(character=a['character'],source=a['packaged_path'],sha256=actual,crop_box=list(box),dimensions=a['dimensions'],mode=a['mode'],alpha_extrema=a['alpha_extrema']))
        sheet.save(output/'upper-body-comparison.png')
        (output/'source-evidence.json').write_text(json.dumps(dict(date='2026-10-30',method='Manual visual inspection; comparative crops and exact source hashes; not a numerical style classifier or owner approval',source_images=entries),indent=2)+'\n')
    print('Prepared comparison sheets from 16 existing images. Source art unchanged.')

if __name__=='__main__':main()
