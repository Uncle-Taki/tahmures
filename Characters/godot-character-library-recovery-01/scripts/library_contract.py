"""Local candidate contracts; approval stays in the original external records."""

import hashlib
import json
from pathlib import Path

ROSTER = [
    "tahmures",
    "akvan_div",
    "black_div",
    "div_e_sefid",
    "shahrasp",
    "chapar",
    "arash",
    "garshasp",
    "simurgh_human",
    "simurgh_bird",
]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def verify_inputs(repo, manifest):
    if [c["character_id"] for c in manifest["characters"]] != ROSTER:
        raise ValueError("Expected the exact ten-character roster")
    for c in manifest["characters"]:
        path = repo / c["source_file"]
        if digest(path) != c["sha256"]:
            raise ValueError(f"Source hash mismatch: {path}")
    for name in ("layout01-v7", "layout01-facial-states-01"):
        approval = read_json(
            repo / f"Characters/tahmures/workflow/approvals/{name}-human-approval.json"
        )
        package = repo / approval["candidate"]
        for filename, key in [
            ("manifest.json", "manifest_sha256"),
            ("files-sha256.json", "file_index_sha256"),
        ]:
            if digest(package / filename) != approval[key]:
                raise ValueError(f"Approval binding mismatch: {package / filename}")
        index = read_json(package / "files-sha256.json")
        if len(index) != approval["indexed_artifact_count"]:
            raise ValueError(f"Approval index count mismatch: {name}")
        for rel, expected in index.items():
            if digest(package / rel) != expected:
                raise ValueError(f"Frozen indexed file mismatch: {package / rel}")
    poc = repo / "Characters/tahmures/prototypes/godot-front-view-character-poc-01"
    head = read_json(poc / "manifest.json")["approved_inputs"]["copied_components"]
    if len(head) != 17:
        raise ValueError("Expected 17 approved head components")
    for filename, record in head.items():
        if (
            digest(repo / record["origin_path"]) != record["sha256"]
            or digest(poc / "assets/approved-head" / filename) != record["sha256"]
        ):
            raise ValueError(f"Approved head mismatch: {filename}")
    return head
