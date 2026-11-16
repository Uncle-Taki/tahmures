"""Package actual background candidates; no provider calls or source-art edits."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HANDOFF = ROOT / "editorial/media-handoff"
DEST = ROOT / "Characters/environments/chapter-01-candidate-01"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def main() -> None:
    queue_path = HANDOFF / "gemini-background-queue.json"
    queue = json.loads(queue_path.read_text())
    log = json.loads((HANDOFF / "background-generation-log.json").read_text())
    selected = {row["id"]: row for row in log}
    received = {
        "BG-HALL-00": "Gemini_Generated_Image_rx0jhzrx0jhzrx0j.jpeg",
        "BG-HALL-01": "Gemini_Generated_Image_ion16kion16kion1.jpeg",
    }
    entries = []
    for shot in queue["shots"]:
        ident = shot["id"]
        folder = DEST / shot["environment"] / shot["view"]
        if ident in received:
            original = ROOT / "scene" / received[ident]
            source = folder / "source" / (ident.lower() + ".jpeg")
            source.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, source)
            assert sha(source) == sha(original)
            tool = "Gemini web, reported by owner; exact model unknown"
        else:
            source = Path(selected[ident]["file"])
            tool = "built-in image_gen; backend model not exposed"
        with Image.open(source) as image:
            image.verify()
        with Image.open(source) as image:
            width, height = image.size
            file_format = image.format
        rel = source.relative_to(DEST).as_posix()
        entry = {
            "id": ident,
            "environment": shot["environment"],
            "view": shot["view"],
            "lighting": shot["lighting"],
            "scenes": shot["scenes"],
            "source": rel,
            "sha256": sha(source),
            "format": file_format,
            "dimensions": [width, height],
            "tool": tool,
            "status": "candidate_visual_reviewed_not_owner_approved",
            "human_approved": False,
            "editable_layers": False,
            "rights": "generated provenance recorded; owner rights review pending",
            "reference_ids": shot["reference_ids"],
            "layout": {
                "reference_viewport": [1280, 720],
                "camera_fit": "uniform_cover_center_no_stretch",
                "caption_safe_rect": [64, 600, 1152, 104],
                "proposed_ground_y": 552,
                "anchors_validated_for_interaction": False,
                "occluders": "not_extracted",
            },
        }
        if ident == "BG-HALL-01":
            entry["lighting_assignment"] = "warm dawn candidate inferred visually"
        entry["limitations"] = [
            "Flat raster; no editable architecture or lighting layers.",
            "Contact/caption/occlusion blocking needs per-shot review.",
        ]
        if ident in {"BG-HALL-03", "BG-HALL-06", "BG-CAMP-02"}:
            entry["limitations"].append(
                "Native framing is wider than requested; crop/block before final use."
            )
        if width * 9 != height * 16:
            entry["limitations"].append(
                "Native aspect is not exact 16:9; uniform cover clips edges slightly."
            )
        write(folder / f"{ident.lower()}-provenance.json", entry)
        shot.update(
            status="candidate_visual_reviewed_not_owner_approved",
            actual_file=str(source.relative_to(ROOT)),
            actual_model=tool,
            actual_dimensions=[width, height],
            sha256=entry["sha256"],
        )
        entries.append(entry)

    for stage in queue["programmatic_stages"]:
        ident = stage["id"]
        folder = DEST / "ENV-OVERLAY" / stage["view"]
        folder.mkdir(parents=True, exist_ok=True)
        svg = folder / (ident.lower() + ".svg")
        svg.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" '
            'viewBox="0 0 1280 720"><g id="neutral-stage">'
            '<rect width="1280" height="720" fill="#20242d"/></g></svg>\n'
        )
        entry = {
            "id": ident,
            "environment": "ENV-OVERLAY",
            "view": stage["view"],
            "lighting": "neutral",
            "scenes": stage["scenes"],
            "source": svg.relative_to(DEST).as_posix(),
            "sha256": sha(svg),
            "dimensions": [1280, 720],
            "tool": "local editable SVG",
            "status": "blank_stage_only_text_and_graphics_pending",
            "human_approved": False,
        }
        entries.append(entry)
        stage["status"] = entry["status"]
        stage["actual_file"] = str(svg.relative_to(ROOT))

    manifest = {
        "schema_version": 1,
        "status": "candidate_background_library_not_chapter_completion",
        "image_count": 25,
        "programmatic_stage_count": 2,
        "owner_approved": False,
        "entries": entries,
    }
    write(DEST / "manifest.json", manifest)
    queue["status"] = "25_candidate_images_received_or_generated_review_pending"
    write(queue_path, queue)
    plan = json.loads((HANDOFF / "chapter-01-production-plan.json").read_text())
    for scene in plan["scene_asset_map"]:
        for bg in scene["backgrounds"]:
            assert any(
                e["environment"] == bg["environment"]
                and e["view"] == bg["view"]
                and e["lighting"] == bg["lighting"]
                and scene["scene"] in e["scenes"]
                for e in entries
            ), (scene["scene"], bg)
    print("PASS: 25 decoded images + 2 SVG stages; all 11 scene mappings covered")


if __name__ == "__main__":
    main()
