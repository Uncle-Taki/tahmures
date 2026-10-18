#!/usr/bin/env python3
"""Phase C planner only. Does not alter or create a chapter project."""

import argparse
import sys
from pathlib import Path

from library_contract import read_json, write_json
from validate_character_library import validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--simurgh-form", choices=["simurgh_human", "simurgh_bird"])
    args = parser.parse_args()
    package = Path(__file__).resolve().parent.parent
    validation = read_json(package / "validation.json")
    if validation.get("pass") is not True:
        raise ValueError("Technical candidate validation must pass first")
    validate(args.repo_root.resolve(), package)
    source = args.repo_root / "Characters/tahmures/prototypes/godot-chapter-01-01"
    if not source.is_dir():
        raise ValueError("Rejected source candidate missing")
    plan = {
        "status": "PLANNING_ONLY_NOT_IMPLEMENTED",
        "human_approved": False,
        "proposed_simurgh_form": args.simurgh_form,
        "source": str(source),
        "writes_to_chapter_project": False,
        "next_steps": [
            "Review anatomical component boundaries and resolve occluded surfaces",
            "Owner selects Simurgh form and reviews the actual motion gallery",
            "Implement reusable CharacterRig instances, not cutout path substitution",
            "Adapt StageKit positioning/scaling to source-canvas coordinates",
            "Repair HUD layout; test reset/seek and EN/FA captions",
            "Render both complete 173-second timelines and probe actual streams",
        ],
    }
    write_json(package / "phase-c-plan.json", plan)
    print("Planning evidence written; no chapter project modified or declared ready.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as exc:
        print("[ERROR]", exc, file=sys.stderr)
        sys.exit(1)
