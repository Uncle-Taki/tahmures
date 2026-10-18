from pathlib import Path
import hashlib
import json
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
manifest = json.loads((root / 'candidate-split-manifest.json').read_text())
def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()
target = root / manifest['movie']
if target.exists():
    if digest(target) != manifest['movie_sha256']:
        raise SystemExit('Existing movie differs; refusing to overwrite: ' + str(target))
else:
    for record in manifest['chunks']:
        chunk = root / record['path']
        if not chunk.is_file() or digest(chunk) != record['sha256']:
            raise SystemExit('Missing or altered chunk: ' + str(chunk))
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix('.avi.restoring')
    with temporary.open('xb') as output:
        for record in manifest['chunks']:
            with (root / record['path']).open('rb') as stream:
                for block in iter(lambda: stream.read(1048576), b''):
                    output.write(block)
    if digest(temporary) != manifest['movie_sha256']:
        raise SystemExit('Restoration hash mismatch: ' + str(temporary))
    temporary.replace(target)
for record in manifest['original_files']:
    path = root / record['path']
    if not path.is_file() or digest(path) != record['sha256']:
        raise SystemExit('Missing or altered original file: ' + str(path))
print('Verified all', len(manifest['original_files']), 'original files, including the restored English AVI.')
