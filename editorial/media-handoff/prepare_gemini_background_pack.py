"""Build the offline, owner-operated Chapter 01 background reference pack."""

from __future__ import annotations

import hashlib
import json
import re
import struct
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
DEST = BASE / "gemini-background-reference-pack"
ARCHIVE = BASE / "gemini-background-reference-pack.zip"
REFERENCES = {
    "references/01-tahmures.png": (
        "Characters/tahmures/versions/layout01-v2/source/approved_master.png"
    ),
    "references/02-akvan-div.png": "Characters/Akvan Div.png",
    "references/03-shahrasp.png": "Characters/Shahrasp.png",
}
DOCUMENTS = (
    "gemini-background-master-prompt.md",
    "chapter-01-environment-brief.md",
    "gemini-background-shot-prompts.md",
    "gemini-background-queue.json",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build() -> None:
    payload: dict[str, bytes] = {}
    records = []
    for target, source in REFERENCES.items():
        data = (ROOT / source).read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"Expected actual PNG reference: {source}")
        width, height = struct.unpack(">II", data[16:24])
        payload[target] = data
        records.append(
            {
                "source_path": source,
                "pack_path": target,
                "sha256": digest(data),
                "bytes": len(data),
                "dimensions": [width, height],
                "operation": "byte_for_byte_copy_no_image_edit",
            }
        )

    for name in DOCUMENTS:
        payload[name] = (BASE / name).read_bytes()
    master = payload[DOCUMENTS[0]].decode()
    cards = payload[DOCUMENTS[2]].decode()
    queue = json.loads(payload[DOCUMENTS[3]])
    common = re.search(r"## Common prefix.*?```text\n(.*?)\n```", cards, re.S)
    director = re.search(r"## Optional first step.*?```text\n(.*?)\n```", master, re.S)
    if common is None or director is None:
        raise ValueError("Missing common prefix or Argon launcher in source documents")

    for shot in queue["shots"]:
        shot_id = shot["id"]
        pattern = rf"^### {re.escape(shot_id)} —[^\n]*\n\n```text\n(.*?)\n```"
        match = re.search(pattern, cards, re.M | re.S)
        if match is None or shot["prompt"] not in match[1]:
            raise ValueError(f"Missing or inconsistent card: {shot_id}")
        text = common[1] + "\n\n" + match[1] + "\n"
        payload[f"shots/{shot_id}.txt"] = text.encode()

    image_rules = master.split("## Paste this master prompt\n\n", 1)[1]
    image_rules = image_rules.split("### Prompts to use after the master", 1)[0]
    payload["prompts/01-start-argon.txt"] = (director[1] + "\n").encode()
    payload["prompts/02-start-image-chat.txt"] = (
        image_rules
        + "\nTarget card follows. Generate this single plate only.\n\n"
        + payload["shots/BG-HALL-00.txt"].decode().split("\n\n", 1)[1]
    ).encode()
    payload["prompts/03-next-argon.txt"] = (
        b"Prepare one complete Nano Banana image prompt for [TARGET-ID] from the "
        b"attached shot catalogue. Use the master rules and actual selected reference "
        b"images attached here. Preserve the card's scene role, camera/light "
        b"dependencies and exclusions. List the actual images to attach in the image "
        b"chat, then return the standalone prompt. If a required visual reference is "
        b"missing, identify it; do not pretend a filename provides image access. "
        b"Do not claim to render images or write files.\n"
    )
    payload["prompts/04-lighting-edit.txt"] = (
        b"Edit the attached selected [SOURCE-ID] into [TARGET-ID], following the "
        b"target card pasted below. Change only its specified lighting/exterior "
        b"weather cues. Keep camera, architecture, furniture and framing stable. "
        b"Add no actors, moving effects, text or interactive story props. Return "
        b"one actual image marked candidate_needs_review.\n"
    )

    workflow = (BASE / "gemini-background-workflow.md").read_text()
    workflow = workflow.replace(
        "[the collected pack](gemini-background-reference-pack/START-HERE.md)",
        "the `references/` directory beside this START-HERE file",
    )
    workflow = workflow.replace(
        "The ready-to-use folder is `gemini-background-reference-pack/`. "
        "Everything below\n"
        "refers to that folder.",
        "You are reading the ready-to-use pack. "
        "Everything below refers to this folder.",
    )
    payload["START-HERE.md"] = workflow.encode()
    payload["gemini-background-workflow.md"] = workflow.encode()
    manifest = {
        "schema_version": 1,
        "scope": "Chapter 01 background references and manual generation prompts",
        "status": "reference_copies_only_no_backgrounds_generated",
        "references": records,
        "support_files": [
            {"path": name, "sha256": digest(data), "bytes": len(data)}
            for name, data in sorted(payload.items())
            if name not in REFERENCES
        ],
        "image_request_count": len(queue["shots"]),
    }
    payload["reference-manifest.json"] = (
        json.dumps(manifest, indent=2) + "\n"
    ).encode()

    # Touch only generated pack files; never delete owner-added downloads/revisions.
    for name, data in payload.items():
        destination = DEST / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        if digest(destination.read_bytes()) != digest(data):
            raise ValueError(f"Copy verification failed: {name}")
    for record in records:
        if digest((ROOT / record["source_path"]).read_bytes()) != record["sha256"]:
            raise ValueError("Original reference changed during collection")

    # Include only the explicit payload, not arbitrary owner-added files.
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(payload):
            archive.writestr(f"{DEST.name}/{name}", payload[name])
    with zipfile.ZipFile(ARCHIVE) as archive:
        if archive.testzip() is not None:
            raise ValueError("Archive integrity check failed")
    print(f"Created {DEST.relative_to(ROOT)}")
    print(
        f"Verified {len(records)} unchanged image copies; {len(queue['shots'])} cards"
    )
    print(f"ZIP: {ARCHIVE.relative_to(ROOT)} ({ARCHIVE.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
