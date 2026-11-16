#!/usr/bin/env python3
"""Offline validation of locally installed Tahmures story-room skills (stdlib only)."""
from pathlib import Path
import re
import sys

NAMES = [
    'tahmures-episode-purpose', 'tahmures-character-pressure',
    'tahmures-causal-architecture', 'tahmures-original-iranian-dramaturgy',
    'tahmures-eleven-scene-blueprint', 'tahmures-punch-and-timing',
    'tahmures-dialogue-and-subtext', 'tahmures-visual-sound-storytelling',
    'tahmures-series-continuity', 'tahmures-story-red-team',
    'tahmures-story-room-director', 'tahmures-flow-handoff-sync',
]


def check(root):
    errors=[]
    skills=root/'.agents'/'skills'
    for name in NAMES:
        path=skills/name/'SKILL.md'
        if not path.is_file():
            errors.append(f'MISSING {path}')
            continue
        contents=path.read_text(encoding='utf8')
        match=re.match(r'\A---\n(.*?)\n---\n',contents,re.S)
        if not match:
            errors.append(f'BAD FRONT MATTER {path}')
            continue
        fields={a.strip():b.strip() for a,b in re.findall(r'(?m)^([a-z_]+):\s*(.+)$',match.group(1))}
        if fields.get('name') != name:
            errors.append(f'WRONG NAME {path}')
        if len(fields.get('description','')) < 35:
            errors.append(f'MISSING/SHORT DESCRIPTION {path}')
        if len(contents) < 500:
            errors.append(f'UNEXPECTEDLY SHORT {path}')
    for req in ['story-room/CODEX_STORY_ROOM_PROMPT.md', 'story-room/references/CRAFT_AND_RESEARCH.md', 'story-room/templates/11_SCENE_MATRIX.csv','story-room/templates/06_PUNCH_MAP.csv']:
        if not (root/req).is_file():
            errors.append(f'MISSING {req}')
    print(f'Tahmures story-room: checked {len(NAMES)} skills; {len(errors)} errors')
    for e in errors: print('ERROR:',e)
    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(check(Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()))
