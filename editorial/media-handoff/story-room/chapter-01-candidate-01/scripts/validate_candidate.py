"""NOT APPROVED FOR PRODUCTION / NOT AUTHORIZED FOR FLOW GENERATION.

Read-only source validation; reports are written only in this candidate root.
"""
import csv
import hashlib
import json
import wave
from pathlib import Path

W = Path(__file__).resolve().parents[1]
R = next(p for p in W.parents if (p / 'meta-prompt.md').exists())
F = W / 'flow-handoff-candidate'
G = 'NOT APPROVED FOR PRODUCTION / NOT AUTHORIZED FOR FLOW GENERATION'


def read(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def path(base, value):
    p = Path(value)
    require(not p.is_absolute() and '..' not in p.parts, 'Unsafe path: ' + value)
    target = base / p
    require(target.resolve().is_relative_to(base.resolve()) and not target.is_symlink(), 'Path escape')
    require(target.is_file(), 'Missing path: ' + str(target))
    return target


def validate():
    snapshot = read(W / 'source-snapshot.json')['files']
    for name, digest in snapshot.items():
        require(sha(path(R, name)) == digest, 'Protected source changed: ' + name)
    inherited = read(F / 'manifests/existing-handoff-snapshot.json')
    for name, digest in inherited['files'].items():
        require(sha(path(R / inherited['root'], name)) == digest, 'Existing handoff changed: ' + name)
    story = read(W / 'candidate-story.json')
    dialogue = read(W / 'dialogue-candidate.json')['lines']
    flow_dialogue = read(F / 'episode-01/dialogue-audio-map.json')['lines']
    require(dialogue == flow_dialogue, 'Candidate dialogue maps disagree')
    require(len(dialogue) == 36, 'Candidate spoken entry count differs')
    require(len({x['cue_id'] for x in dialogue}) == 36, 'Duplicate cue IDs')
    require([x['cue_id'] for x in dialogue if x['new_recording_required']] == ['D-S07-2','SR02-KING-ACK','SR05-HOOK'], 'Untracked voice change')
    for l in dialogue:
        if l['source_audio_path']:
            p = path(R, l['source_audio_path'])
            require(sha(p) == l['source_sha256'], 'Source WAV differs')
            with wave.open(str(p)) as stream:
                require(abs(stream.getnframes() / stream.getframerate() - l['source_duration']) < 1e-6, 'Source audio duration differs')
        require(l['candidate_start'] == l['candidate_end'] == 'TBD', 'Invented candidate cue time')
        if l['new_recording_required']:
            require(l['candidate_recording_path'] is None, 'Unrecorded speech assigned old audio')
        else:
            require(l['candidate_text'] == l['text'], 'Untracked retained-text change')
        require(not l['human_lip_sync_approved'], 'Unearned mouth approval')
        require(l['candidate_text'] in (W / '07_CANDIDATE_SCRIPT.md').read_text(), 'Selected line absent from candidate script')
    scenes = read(F / 'episode-01/scene-index.json')
    production = read(path(R, story['source_timeline']))
    require(scenes['source_duration_seconds'] == production['duration'] == 251.3, 'Source runtime mismatch')
    require(story['candidate_duration_seconds'] == scenes['candidate_duration_seconds'] == 'TBD', 'Candidate runtime fabricated')
    require(len(scenes['source_scenes']) == 12 and scenes['source_scenes'][0]['source_id'] == 'T00', 'Scene/title mismatch')
    for candidate, source in zip(scenes['source_scenes'], production['scenes'], strict=True):
        require(candidate['source_id'] == source['scene'] and candidate['source_start'] == source['start'] and candidate['source_end'] == source['end'] and candidate['source_frames'] == source['frames'], 'Source scene locator mismatch')
        require(candidate['candidate_start'] == candidate['candidate_end'] == 'TBD', 'Candidate scene time invented')
    assets = read(F / 'manifests/asset-manifest.json')['assets']
    byasset = {a['id']: a for a in assets}
    require(len(byasset) == len(assets) == 51, 'Missing/duplicate asset map')
    copies = []
    for a in assets:
        require(sha(path(R, a['original_path'])) == a['sha256'], 'Image source differs')
        require(sha(path(R, a['official_handoff_path'])) == a['sha256'], 'Prior packaged reference differs')
        if a['candidate_image_path']:
            p = path(F, a['candidate_image_path'])
            require(sha(p) == a['sha256'], 'Candidate image differs')
            require(a['source_asset_approval_status'] == 'approved_scoped_reference', 'Unapproved art copied as candidate master')
            require(G in path(F, a['candidate_image_path']+'.status.md').read_text(), 'Missing image status sidecar')
            copies.append(p.resolve())
        require(not a['candidate_owner_approved'] and a['candidate_package_status'] == G, 'Candidate asset promoted')
    require(len(copies) == 2, 'Unexpected image copies')
    actual_images = {p.resolve() for p in (F/'assets').rglob('*.png')}
    require(actual_images == set(copies), 'Untracked image copy')
    shots = read(F / 'manifests/shot-to-asset-map.json')['shots']
    require(len(shots) == len({s['id'] for s in shots}) == 48, 'Shot count/uniqueness differs')
    require({s['scene'] for s in shots} == {f'S{i:02}' for i in range(1,12)}, 'Incomplete scene shot coverage')
    actual_cards = {p.stem for p in (F/'episode-01/shots').glob('*.md')}
    require(actual_cards == {s['id'] for s in shots}, 'Missing or stale shot card')
    cueids = {l['cue_id'] for l in dialogue}
    changes = {c['id']: c for c in story['changes']}
    with (F/'episode-01/punch-map.csv').open() as stream:
        punches = {r['beat_id']: r for r in csv.DictReader(stream)}
    for s in shots:
        require(not s['production_authorized'] and not s['owner_approved'], 'Shot promoted')
        require(s['candidate_cut_start'] == s['candidate_cut_end'] == s['candidate_generation_duration'] == 'TBD', 'Unsourced candidate shot time')
        require(set(s['asset_ids']) <= byasset.keys(), 'Invalid shot asset')
        require(set(s['cue_ids']) <= cueids, 'Invalid shot cue')
        require(set(s['change_ids']) <= changes.keys(), 'Unknown story change')
        require(set(s['punch_ids']) <= punches.keys(), 'Unknown punch reference')
        require('simurgh' not in s['cast'], 'Historical messenger reused as active cast')
        text = path(F, 'episode-01/shots/'+s['id']+'.md').read_text()
        require(s['primary_action'] in text and s['character_decision'] in text, 'Shot intent stale')
        for l in dialogue:
            if l['cue_id'] in s['cue_ids']:
                require(l['candidate_text'] in text, 'Shot dialogue stale')
        if s['scene'] == 'S06':
            require('Arash receives/attends' in s['primary_action'] and 'then riders depart' in s['primary_action'], 'Dispatch causal dependency missing')
    with (F/'CHANGE_IMPACT_MATRIX.csv').open() as stream:
        matrix = list(csv.DictReader(stream))
    require(len(matrix) == 53, 'Impact row missing')
    require({r['story_change_id'] for r in matrix} == set(changes) | {'SHOT-'+s['id'] for s in shots}, 'Change/shot impact coverage missing')
    for row in matrix:
        require(row['candidate_file_status'] == G, 'CSV candidate gate missing')
        for field in ['context_files','agent_instructions','flow_prompt_files','dialogue_audio_files']:
            for name in row[field].split(';'):
                path(F, name)
    # Source punch values checked to cue starts; proposed landings always TBD.
    source_cues = {l['cue_id']: l for s in production['scenes'] for l in s['lines']}
    for id_, row in punches.items():
        if id_.startswith('SRC-'):
            l=source_cues[id_[4:]]
            minute, sec=row['start_mmss'].split(':')
            require(abs(60*int(minute)+float(sec)-l['global_start'])<0.0006,'Source punch timestamp differs')
            require(abs(float(row['episode_percent'])-100*l['global_start']/251.3)<0.0001,'Source percentage differs')
        else:
            require(row['start_mmss'] == row['episode_percent'] == 'TBD','Proposed punch time invented')
    # Every authored text artifact is gated, binaries via status filenames/sidecars.
    for p in W.rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts:
            continue
        if p.suffix in ['.md','.json','.csv','.py']:
            require(G in p.read_text(), 'Candidate file ungated: '+str(p))
    alltexts='\n'.join(p.read_text() for p in (F/'agent-instructions').glob('*.md'))
    require('Div-e Sefid' in alltexts and 'Chapar' in alltexts and 'not a second style bible' in alltexts, 'Agent authority/identity reconciliation missing')
    require('You crossed because I left the question open.' not in (W/'07_CANDIDATE_SCRIPT.md').read_text(), 'Rejected premature diagnosis remains selected')
    return dict(status=G,validation_result='PASS',source_snapshot_files=len(snapshot),source_hashes='UNCHANGED',existing_handoff='UNCHANGED',narrative_scenes=11,title_segments=1,candidate_shot_briefs=48,impact_rows=53,source_audio_cues=34,candidate_spoken_entries=36,new_or_replacement_recordings_missing=3,copied_reference_images=2,unapproved_source_reference_pointers=49,candidate_runtime='TBD',owner_approved=False,production_authorized=False,artistic_quality='NOT VERIFIED',actual_flow_account_state='NOT ACCESSED')


if __name__=='__main__':
    result=validate()
    for bad in ['../AGENTS.md','/etc/passwd','missing-image.png']:
        try:
            path(F,bad)
        except ValueError:
            continue
        raise ValueError('Unsafe/missing path accepted')
    result['negative_path_checks']='PASS'
    report=F/'manifests/candidate-validation.json'
    report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
