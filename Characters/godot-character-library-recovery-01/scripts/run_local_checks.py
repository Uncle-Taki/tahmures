#!/usr/bin/env python3
"""Run real local checks and save commands, outputs and expected failure evidence."""

import argparse
import subprocess
import sys
from pathlib import Path

from library_contract import write_json

PKG = Path(__file__).resolve().parent.parent
REPO = PKG.parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--repository-check", action="store_true")
    args = parser.parse_args()
    evidence = PKG / "evidence"
    evidence.mkdir(exist_ok=True)
    python = [sys.executable]
    godot = ["rtk", "proxy", "godot", "--headless", "--path", str(PKG)]
    jobs = []
    if args.build:
        jobs.append(
            ("build", python + [str(PKG / "scripts/build_character_library.py")], 0)
        )
    jobs.extend(
        [
            (
                "python-regressions",
                python + [str(PKG / "scripts/tests/test_library_contract.py")],
                0,
            ),
            (
                "reject-missing-repo",
                python
                + [
                    str(PKG / "scripts/validate_character_library.py"),
                    "--repo-root",
                    "/definitely-missing-tahmures",
                ],
                1,
            ),
            (
                "validate",
                python + [str(PKG / "scripts/validate_character_library.py")],
                0,
            ),
            ("godot-import", godot + ["--import"], 0),
            (
                "rig-regressions",
                godot
                + [
                    "--script",
                    "scripts/tests/rig_contract_test.gd",
                    "--quit-after",
                    "20",
                ],
                0,
            ),
            (
                "reject-missing-character",
                godot
                + [
                    "--script",
                    "scripts/tests/rig_contract_test.gd",
                    "--quit-after",
                    "20",
                    "--",
                    "--missing-resource",
                ],
                1,
            ),
            ("gallery-smoke", godot + ["--quit-after", "10"], 0),
        ]
    )
    jobs.append(
        (
            "reject-malformed-character",
            godot
            + [
                "--script",
                "scripts/tests/rig_contract_test.gd",
                "--quit-after",
                "20",
                "--",
                "--malformed-resource",
            ],
            1,
        )
    )
    if args.render:
        jobs.append(
            (
                "viewport-captures",
                [
                    "rtk",
                    "proxy",
                    "godot",
                    "--path",
                    str(PKG),
                    "--script",
                    "scripts/tests/render_review.gd",
                ],
                0,
            )
        )
    if args.repository_check:
        jobs.append(
            (
                "repository-check",
                ["rtk", "proxy", "make", "check", "PYTHON=.venv/bin/python"],
                0,
            )
        )
    results = []
    for name, command, expected in jobs:
        try:
            result = subprocess.run(
                command, cwd=REPO, text=True, capture_output=True, timeout=300
            )
            output = result.stdout + result.stderr
            exit_code = result.returncode
        except subprocess.TimeoutExpired as exc:
            output, exit_code = str(exc), -1
        (evidence / f"{name}.log").write_text(output)
        passed = exit_code == expected
        if expected == 0 and any(
            token in output for token in ("SCRIPT ERROR:", "ERROR:", "Assertion failed")
        ):
            passed = False
        if name == "reject-missing-character":
            passed = passed and "Missing component-map.json" in output
        if name == "reject-malformed-character":
            passed = passed and "Malformed character component map" in output
        if name == "reject-missing-repo":
            passed = passed and "[FAIL]" in output
        results.append(
            {
                "name": name,
                "command": command,
                "exit_code": exit_code,
                "expected_exit_code": expected,
                "pass": passed,
                "log": f"evidence/{name}.log",
            }
        )
        print(
            f"{'PASS' if passed else 'FAIL'} {name} "
            f"(exit {exit_code}, expected {expected})",
            flush=True,
        )
    media = all(r["pass"] for r in results if r["name"] != "repository-check")
    repository = next(
        (r["pass"] for r in results if r["name"] == "repository-check"), None
    )
    write_json(
        evidence / "local-checks.json",
        {
            "media_candidate_checks_passed": media,
            "repository_gate_passed": repository,
            "anatomical_art_approved": False,
            "human_approved": False,
            "godot_viewport_capture_executed": args.render,
            "checks": results,
        },
    )
    return 0 if media and repository is not False else 1


if __name__ == "__main__":
    sys.exit(main())
