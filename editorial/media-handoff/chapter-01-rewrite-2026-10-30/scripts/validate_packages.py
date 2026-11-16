"""Offline checks for the RW01 bilingual writing and two visual handoffs."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parents[1]
ROOT = next(p for p in BASE.parents if (p / 'meta-prompt.md').exists())
SCRIPT = ROOT / 'playscript/chapter-01-final-2026-10-30'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    def local(folder, value):
        p = (folder / value).resolve()
        check(p.is_relative_to(folder.resolve()), f'Unsafe package path: {value}')
        check(p.is_file(), f'Missing package file: {p}')
        return p

    episode = json.loads((SCRIPT / 'episode.json').read_text())
    scenes = episode['scenes']
    blocks = {b['id']: b for s in scenes for b in s['blocks']}
    total = sum(len(s['blocks']) for s in scenes)
    check(len(scenes) == 11, 'Expected eleven editorial scenes')
    check({s['source_scene'] for s in scenes} == set(range(1, 9)), 'Author scene coverage')
    check(len({s['id'] for s in scenes}) == len(scenes), 'Duplicate scene IDs')
    check(len(blocks) == total, 'Duplicate block IDs')
    for s in scenes:
        check(s['duration_seconds'] == 'TBD', f"Invented timing {s['id']}")
        for b in s['blocks']:
            check(all(isinstance(b.get(lang), str) and b[lang].strip() for lang in ['fa', 'en']), f"Missing paired language {b['id']}")
            check(b['type'] in ['action', 'dialogue', 'narration', 'overlay'], f"Bad block type {b['id']}")
            if b['type'] == 'dialogue':
                check(b['speaker'] in s['cast'], f"Speaker missing from cast {b['id']}")

    snapshot = json.loads((SCRIPT / 'source-snapshot.json').read_text())
    for source, recorded in snapshot['files'].items():
        p = ROOT / source
        check(p.is_file() and digest(p) == recorded, f'Protected source changed: {source}')

    plan = json.loads((BASE / 'shot-plan.json').read_text())['shots']
    coverage = Counter(b for s in plan for b in s['block_ids'])
    check(coverage == Counter({b: 1 for b in blocks}), 'Shot coverage differs from exact once per script block')
    check(len({s['id'] for s in plan}) == len(plan), 'Duplicate shot ID')
    cues = json.loads((BASE / 'dialogue-audio-map.json').read_text())['cues']
    spoken = {b['id'] for b in blocks.values() if b['type'] in ['dialogue', 'narration']}
    check({c['id'] for c in cues} == spoken and len(cues) == len(spoken), 'Audio cue coverage')
    for c in cues:
        check(all(c[l] == blocks[c['id']][l] for l in ['fa', 'en']), f"Audio text mismatch {c['id']}")
        check(c['recording_fa'] is None and c['recording_en'] is None, f"Unverified recording {c['id']}")
        check(c['duration_fa'] == c['duration_en'] == 'TBD', f"Invented audio timing {c['id']}")

    image_count = 0
    portrait_pairs = 0
    corrected_bodies = 0
    for branch in ['paper-puppet', 'illustrated-v2']:
        folder = BASE / ('flow-' + branch)
        manifest = json.loads((folder / 'manifests/assets.json').read_text())
        assets = manifest['assets']
        check(len(assets) == (9 if branch=='paper-puppet' else 7), f'{branch}: reference count')
        check(len({a['id'] for a in assets}) == len(assets), f'{branch}: duplicate asset IDs')
        expected_missing=set() if branch=='paper-puppet' else {'chapar','arash'}
        check(set(manifest['missing_characters']) == expected_missing, f'{branch}: missing identity record')
        for a in assets:
            p = local(folder, a['packaged_path'])
            source = ROOT / a['original_path']
            check(source.is_file(), f"Missing source: {source}")
            check(digest(p) == digest(source) == a['sha256'], f"Copied bytes mismatch {p}")
            with Image.open(p) as im:
                im.load()
                check(list(im.size) == a['dimensions'], f'Image dimensions mismatch: {p}')
                check(im.mode == a['mode'] and im.format == a['format'], f'Image format mismatch: {p}')
                alpha = list(im.getchannel('A').getextrema()) if 'A' in im.getbands() else None
                check(alpha == a['alpha_extrema'], f'Alpha mismatch: {p}')
            check(not a['registered'] and not a['uploaded'] and not a['motion_approved'], f"Unverified remote/approval claim {a['id']}")
            check((ROOT / a['source_manifest']).is_file(), f"Missing selection evidence {a['id']}")
            image_count += 1
        infos=json.loads(local(folder,'manifests/character-info.json').read_text())['characters']
        expected_ids={'tahmures','shahrasp','chapar','arash','akvan_div','black_div','div_e_sefid','simurgh_bird','hushang'}
        check(len(infos)==9 and {c['id'] for c in infos}==expected_ids, f'{branch}: character info coverage')
        for c in infos:
            card=local(folder,'context/character-info/'+c['id']+'.md').read_text()
            a=next((a for a in assets if a['character']==c['id']),None)
            check(c['reference_image']==(a['packaged_path'] if a else None),f"Character image mapping {branch}/{c['id']}")
            check(c['reference_sha256']==(a['sha256'] if a else None),f"Character image hash {branch}/{c['id']}")
            expected_cues=[b['id'] for s in scenes for b in s['blocks'] if b.get('speaker')==c['id']]
            check(c['spoken_cue_ids']==expected_cues,f"Character cue mapping {branch}/{c['id']}")
            check(c['flow_character_info'] in card,f"Character info body differs {branch}/{c['id']}")
            check(c['voice_recording'] is None and not c['voice_and_lip_sync_approved'],f"False character voice approval {c['id']}")
        for p in folder.rglob('*.md'):
            for dest in re.findall(r'\]\(([^)]+)\)',p.read_text()):
                if dest.startswith(('https:','http:','#')):continue
                check((p.parent/dest.split('#')[0]).exists(),f'Broken Markdown/image link {p}: {dest}')
        local(folder,'ROADMAP.md');local(folder,'WORKFLOW.md')
        for name in ['episode.json', 'chapter_one_final_fa.md', 'chapter_one_final_en.md']:
            check(digest(local(folder, 'script/' + name)) == digest(SCRIPT / name), f'{branch}: screenplay differs {name}')
        branch_cues = json.loads((folder / 'episode-01/dialogue-audio-map.json').read_text())['cues']
        check(branch_cues == cues, f'{branch}: dialogue/audio text differs')
        branch_shots = json.loads((folder / 'manifests/shot-to-asset-map.json').read_text())['shots']
        check([s['id'] for s in branch_shots] == [s['id'] for s in plan], f'{branch}: shot list differs')
        valid_assets = {a['id'] for a in assets}
        for shot in branch_shots:
            card = local(folder, 'episode-01/shots/' + shot['id'] + '.md').read_text()
            check(set(shot['missing_character_ids']) == (set(shot['cast']) & expected_missing), f"Stale missing identity claim {shot['id']}")
            check(set(shot['asset_ids']) <= valid_assets, f"Bad asset mapping {shot['id']}")
            for id_ in shot['block_ids']:
                check(id_ in card and blocks[id_]['fa'] in card and blocks[id_]['en'] in card, f"Shot text out of sync {shot['id']} / {id_}")
            check(all(shot[k] == 'TBD' for k in ['start', 'end', 'duration', 'generation_duration']), f"Invented shot timing {shot['id']}")
        pairroot=folder/'portrait-body-candidate-01'
        if pairroot.exists():
            paired=json.loads(local(pairroot,'manifest.json').read_text())['pairs']
            check({p['id'] for p in paired}=={a['character'] for a in assets},f'{branch}: portrait/body coverage')
            pairlookup={p['id']:p for p in paired}
            for pair in paired:
                portrait=local(pairroot,pair['portrait']);body=local(pairroot,pair['full_body'])
                original=ROOT/pair['source']
                check(digest(original)==pair['source_sha256']==digest(body)==pair['full_body_sha256'],f"Pair body hash {branch}/{pair['id']}")
                check(digest(portrait)==pair['portrait_sha256'],f"Pair portrait hash {branch}/{pair['id']}")
                with Image.open(body) as im,Image.open(portrait) as crop:
                    im.load();crop.load();box=pair['crop_box']
                    check(0<=box[0]<box[2]<=im.width and 0<=box[1]<box[3]<=im.height,f"Bad portrait rectangle {pair['id']}")
                    expected=im.crop(box)
                    check(expected.mode==crop.mode and expected.size==crop.size and expected.tobytes()==crop.tobytes(),f"Portrait/body pixel mismatch {branch}/{pair['id']}")
                check(not pair['owner_approved'],f"False new-art approval {pair['id']}")
                check(pair['generated_correction']==(branch=='paper-puppet' and pair['id'] in {'chapar','arash','div_e_sefid','simurgh_bird'}),f"Correction provenance {branch}/{pair['id']}")
                portrait_pairs+=1;corrected_bodies+=int(pair['generated_correction'])
            overlay=json.loads(local(pairroot,'shot-to-input-map.json').read_text())['shots']
            check([s['shot_id'] for s in overlay]==[s['id'] for s in branch_shots],f'{branch}: candidate shot mapping')
            for s in overlay:
                original=next(v for v in branch_shots if v['id']==s['shot_id'])
                check(s['script_blocks']==original['block_ids'],f"Candidate changed writing {s['shot_id']}")
                for a in s['candidate_inputs']:
                    p=pairlookup[a['character']]
                    check(a['portrait']==p['portrait'] and a['full_body']==p['full_body'],f"Wrong pair in shot {s['shot_id']}")
            local(pairroot,'PAIR_INDEX.md');local(pairroot,'gallery.html')
        actual = {str(p.relative_to(folder)) for p in (folder / 'assets/characters').glob('*')}
        check(actual == {a['packaged_path'] for a in assets}, f'{branch}: unmanifested reference')

    result = dict(status='PASS' if not errors else 'FAIL', date='2026-10-30',
                  editorial_scenes=len(scenes), original_author_scenes=8,
                  paired_blocks=total, shots_per_branch=len(plan), spoken_cues_per_language=len(cues),
                  physical_character_copies=image_count, character_info_sheets=18,
                  portrait_full_body_pairs=portrait_pairs, generated_body_correction_candidates=corrected_bodies,
                  paper_puppet_principal_images=9, illustrated_v2_principal_images=7,
                  protected_sources_unchanged=len(snapshot['files']), errors=errors,
                  limits='Structure/hash/path/text audits plus separate machine bilingual read-through; not human approval, runtime measurement or moving-image/lip-sync validation.')
    (BASE / 'validation-results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == '__main__':
    main()
