#!/usr/bin/env python3
"""Layout01 v4 repair — stage 60: files-sha256.json + supervisor validation.

Runs the read-only structural checker from the repository root exactly as
specified (via rtk proxy) and records both commands and their outcomes in
validation-results.json, then proves a fixed point: the recorded run is the
run that passes against the final on-disk hash index.
"""
import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path("/home/mehdi/Project/leela/tahmures")
ROOT = REPO / "Characters/tahmures/versions/layout01-v4"
BASE = REPO / "Characters/tahmures/versions/layout01-v2"
CHECKER = "Characters/tahmures/workflow/tools/validate_submission.py"
CAND_REL = "Characters/tahmures/versions/layout01-v4"
BASE_REL = "Characters/tahmures/versions/layout01-v2"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_index():
    idx = {}
    for p in sorted(ROOT.rglob("*")):
        if p.is_file() and p.name != "files-sha256.json":
            idx[str(p.relative_to(ROOT))] = digest(p)
    (ROOT / "files-sha256.json").write_text(
        json.dumps(idx, indent=2, sort_keys=True) + "\n")
    return len(idx)


def run(cmd):
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def main():
    args = [CHECKER, "--candidate", CAND_REL, "--baseline", BASE_REL]

    # 1. the literal task command (rtk proxy resolves to the book .venv
    #    interpreter, which has no Pillow) — recorded honestly
    lit_rc, lit_out, lit_err = run(["rtk", "proxy", "python3"] + args)
    print("literal command exit=%d" % lit_rc)
    if lit_rc != 0:
        print("literal command stderr tail:",
              lit_err.strip().splitlines()[-1] if lit_err.strip() else "(empty)")

    # 2. executable run with the system interpreter (Pillow 10.2.0 available)
    build_index()
    rc, out, err = run(["rtk", "proxy", "/usr/bin/python3"] + args)
    parsed = json.loads(out)
    print("checker exit=%d pass=%s checks=%d" % (
        rc, parsed.get("pass"), len(parsed.get("checks", []))))
    assert rc == 0 and parsed.get("pass") is True, "supervisor checker failed"

    doc = {
        "gate": "supervisor_structural_checker",
        "artistic_approval": False,
        "pass": True,
        "commands": [
            {
                "command": "rtk proxy python3 %s" % " ".join(args),
                "role": "literal task command (resolves to the book .venv "
                        "interpreter)",
                "exit_code": lit_rc,
                "stdout": lit_out,
                "stderr_tail": "\n".join(lit_err.strip().splitlines()[-3:]),
                "outcome": "FAILED: the book .venv has no Pillow "
                           "(ModuleNotFoundError: No module named 'PIL'). "
                           "Reported to Codex as a tooling contract "
                           "discrepancy; no environment or checker change "
                           "was made.",
            },
            {
                "command": "rtk proxy /usr/bin/python3 %s" % " ".join(args),
                "role": "executed run — system interpreter with Pillow "
                        "10.2.0 and numpy 1.26.4",
                "exit_code": rc,
                "stdout": out,
                "parsed": parsed,
                "outcome": "PASS (%d structural checks)" % len(parsed.get("checks", [])),
            },
        ],
        "working_directory": str(REPO),
        "note": "The supervisor checker is read-only and unmodified. The "
                "candidate hash index covers every file under the candidate "
                "root except files-sha256.json itself, including this file.",
        "fixed_point_verified": False,
    }

    # 3. fixed-point iteration: rewrite validation-results.json, rebuild the
    #    index, rerun, and require the recorded stdout to be reproduced
    (ROOT / "validation-results.json").write_text(
        json.dumps(doc, indent=2) + "\n")
    for attempt in range(4):
        n = build_index()
        rc2, out2, err2 = run(["rtk", "proxy", "/usr/bin/python3"] + args)
        assert rc2 == 0, "checker failed during fixed-point iteration"
        if out2 == doc["commands"][1]["stdout"]:
            if doc["fixed_point_verified"]:
                print("fixed point reached: index covers %d files; recorded "
                      "stdout reproduced exactly" % n)
                break
            doc["fixed_point_verified"] = True
            (ROOT / "validation-results.json").write_text(
                json.dumps(doc, indent=2) + "\n")
            print("fixed-point pass recorded; verifying once more")
        else:
            doc["commands"][1]["stdout"] = out2
            doc["commands"][1]["parsed"] = json.loads(out2)
            doc["fixed_point_verified"] = False
            (ROOT / "validation-results.json").write_text(
                json.dumps(doc, indent=2) + "\n")
            print("checker output changed at attempt %d; re-recorded" % attempt)
    else:
        raise AssertionError("validation results did not reach a fixed point")

    # final state on disk
    final_index = json.loads((ROOT / "files-sha256.json").read_text())
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*")
              if p.is_file() and p.name != "files-sha256.json"}
    assert set(final_index) == actual, "index and files diverged"
    for rel, expected in final_index.items():
        assert digest(ROOT / rel) == expected, "stale hash: " + rel
    print("index final: %d files, all hashes current" % len(final_index))
    print("stage 60 complete")


if __name__ == "__main__":
    main()
