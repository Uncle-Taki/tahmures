#!/usr/bin/env python3
"""Optional offline fallback; the primary AI Studio handoff uses private GitHub."""

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "editorial/media-handoff"
OUT = BASE / "ai-studio-exchange"
LIB = ROOT / "Characters/godot-character-library-recovery-01"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    if OUT.exists():
        raise SystemExit(
            f"Preserving existing snapshot; choose a new destination: {OUT}"
        )
    sources = {
        p
        for p in LIB.rglob("*")
        if p.is_file()
        and not any(part in (".godot", "__pycache__") for part in p.parts)
        and p.suffix not in (".pyc", ".pyo", ".avi", ".zip")
    }
    manifest = json.loads((LIB / "character-library-manifest.json").read_text())
    sources.update(ROOT / c["source_file"] for c in manifest["characters"])
    for name in ("layout01-v7", "layout01-facial-states-01"):
        approval_path = (
            ROOT / f"Characters/tahmures/workflow/approvals/{name}-human-approval.json"
        )
        approval = json.loads(approval_path.read_text())
        directory = ROOT / approval["candidate"]
        index = json.loads((directory / "files-sha256.json").read_text())
        sources.update(directory / rel for rel in index)
        sources.update(
            [
                approval_path,
                directory / "manifest.json",
                directory / "files-sha256.json",
            ]
        )
    poc = ROOT / "Characters/tahmures/prototypes/godot-front-view-character-poc-01"
    sources.add(poc / "manifest.json")
    sources.update((poc / "assets/approved-head").glob("*.png"))
    selected = [
        "AGENTS.md",
        "meta-prompt.md",
        "book/project-charter.md",
        "book/narrative-continuity.md",
        "book/part-1/01-what-is-a-prompt.md",
        "book/fa/part-1/01-what-is-a-prompt.md",
        "book/fa/translation-glossary.md",
        "writing_persian_eng_books.md",
        ".agents/skills/mehdi-media/SKILL.md",
        ".agents/skills/tahmures-narrative/SKILL.md",
        ".agents/skills/tahmures-narrative/references/story-world.md",
        "editorial/media-handoff/README.md",
        "editorial/media-handoff/ai-studio-start-here.md",
        "editorial/media-handoff/ai-studio-baseline.json",
        "editorial/media-handoff/ai-studio-roadmap.md",
        "editorial/media-handoff/ai-studio-task-01.md",
        "editorial/media-handoff/ai-studio-return-template.md",
        "editorial/media-handoff/2026-10-18-gemini-local-recovery-audit.md",
        "editorial/media-handoff/prepare_ai_studio_exchange.py",
    ]
    sources.update(ROOT / path for path in selected)
    for path in sources:
        if not path.is_file():
            raise SystemExit(f"Missing selected source: {path}")
    OUT.mkdir()
    records = []
    for source in sorted(sources):
        relative = source.relative_to(ROOT)
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        checksum = digest(source)
        if digest(target) != checksum:
            raise ValueError(f"Copy mismatch: {source}")
        records.append(
            {"path": str(relative), "bytes": source.stat().st_size, "sha256": checksum}
        )
    rtk = Path("/home/mehdi/.codex-gpt-1/RTK.md")
    shutil.copy2(rtk, OUT / "RTK.md")
    records.append(
        {"path": "RTK.md", "bytes": rtk.stat().st_size, "sha256": digest(rtk)}
    )
    readme = """# Optional AI Studio offline fallback

The primary workflow uses the owner's private GitHub repository, branch main.
Start with editorial/media-handoff/README.md and ai-studio-start-here.md.
This archive is optional transfer backup, not the repository authority.
AGENTS.md references the workstation RTK.md path; its exact companion is RTK.md
at this snapshot root. No project_context.md exists in the source checkout;
use the canonical charter/continuity instead of inventing a context document.

This is a selected source snapshot, not a full Git checkout or a full book build.
Run media checks documented in Characters/godot-character-library-recovery-01/.
The full repository gate and its eight editorial baseline failures are checked
only on the original workstation. Do not run make check here and claim parity.
Approved packages are input bytes; historical full rebuild inputs are not all
included. Do not rebuild or alter them for this Akvan-only task.

The owner reports the project is already pushed to a private GitHub repository.
Import the intended repository/branch; record its actual revision. Use this
fallback only when repository import is unavailable and record that choice.
No giant upload archives, rejected movie exports, raw chat logs or editor caches
are included. Keep the original PNGs, approval records and indexed bytes intact.
"""
    (OUT / "EXCHANGE-README.md").write_text(readme)
    records.append(
        {
            "path": "EXCHANGE-README.md",
            "bytes": (OUT / "EXCHANGE-README.md").stat().st_size,
            "sha256": digest(OUT / "EXCHANGE-README.md"),
        }
    )
    (OUT / "EXCHANGE-MANIFEST.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "date": "2026-10-18",
                "task": "Akvan anatomical extraction only",
                "human_approved": False,
                "files": records,
            },
            indent=2,
        )
        + "\n"
    )
    archive = BASE / "ai-studio-exchange.zip"
    if archive.exists():
        raise SystemExit(f"Preserving existing archive: {archive}")
    with zipfile.ZipFile(
        archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6
    ) as z:
        for path in sorted(OUT.rglob("*")):
            if path.is_file():
                z.write(path, str(path.relative_to(OUT)))
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise ValueError("ZIP CRC failure")
        for record in records:
            if hashlib.sha256(z.read(record["path"])).hexdigest() != record["sha256"]:
                raise ValueError(f"ZIP entry mismatch: {record['path']}")
    print(
        f"Prepared {len(records)} source files plus manifest; "
        f"{archive.stat().st_size / 1_000_000:.2f} MB"
    )
    print(f"Baseline manifest SHA-256: {digest(OUT / 'EXCHANGE-MANIFEST.json')}")


if __name__ == "__main__":
    main()
