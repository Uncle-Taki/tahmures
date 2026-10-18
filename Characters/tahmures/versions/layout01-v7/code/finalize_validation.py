"""Hash the completed candidate and record the unchanged structural checker."""

import hashlib
import json
import subprocess
from pathlib import Path

C = Path(__file__).resolve().parents[1]
ROOT = C.parents[3]


def index():
    hashes = {
        str(p.relative_to(C)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(C.rglob("*"))
        if p.is_file() and p.name != "files-sha256.json"
    }
    (C / "files-sha256.json").write_text(json.dumps(hashes, indent=2) + "\n")


def run():
    return subprocess.run(
        [
            "rtk",
            "proxy",
            "/usr/bin/python3",
            "Characters/tahmures/workflow/tools/validate_submission.py",
            "--candidate",
            str(C.relative_to(ROOT)),
            "--baseline",
            "Characters/tahmures/versions/layout01-v2",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def main():
    index()
    result = run()
    output = json.loads(result.stdout)
    doc = {
        "gate": "structural_only",
        "exit_code": result.returncode,
        "checker": output,
        "artistic_approval": False,
        "human_approved": False,
    }
    (C / "validation-results.json").write_text(json.dumps(doc, indent=2) + "\n")
    index()
    final = run()
    assert final.returncode == 0, final.stdout + final.stderr
    assert json.loads(final.stdout) == output
    print("Checker pass:", len(output["checks"]), "checks; final index current.")


if __name__ == "__main__":
    main()
