"""Generate evidence from actual local output, not the received preview sheet."""

from library_contract import write_json
from PIL import Image, ImageDraw, ImageFont


def font(size):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)


def checker(size):
    out = Image.new("RGBA", size, "#202734")
    draw = ImageDraw.Draw(out)
    for y in range(0, size[1], 16):
        for x in range(0, size[0], 16):
            if (x // 16 + y // 16) % 2:
                draw.rectangle((x, y, x + 15, y + 15), fill="#394352")
    return out


def prepare_review(package, repo, manifest):
    gallery = Image.new("RGB", (1500, 1070), "#141922")
    draw = ImageDraw.Draw(gallery)
    draw.text(
        (16, 12),
        "LOCAL BUILD | Candidates: anatomical cuts and movement need review",
        font=font(20),
        fill="white",
    )
    for i, character in enumerate(manifest["characters"]):
        cid = character["character_id"]
        if "received_measurement_claims" not in character:
            keys = [
                "foreground_bbox",
                "foreground_pixels",
                "interior_pale_pixels_preserved",
                "background_corner_rgb",
            ]
            character["received_measurement_claims"] = {
                k: character.pop(k) for k in keys if k in character
            }
        character["component_definitions_status"] = (
            "received_search_windows_not_verified_anatomy"
        )
        directory = package / "characters" / cid
        scene = package / "scenes/characters" / f"{cid}.tscn"
        scene.parent.mkdir(parents=True, exist_ok=True)
        scene.write_text(
            "[gd_scene load_steps=2 format=3]\n\n"
            '[ext_resource type="Script" '
            'path="res://scripts/character_rig.gd" id="1"]\n\n[node name="'
            + cid
            + '" type="Node2D"]\nscript = ExtResource("1")\ncharacter_id = "'
            + cid
            + '"\n'
        )
        # Compare original and layer-only recomposition after background removal.
        from library_contract import read_json

        cmap = read_json(directory / "component-map.json")
        for component in character["components"]:
            if "received_measurement_claims" not in component:
                component["received_measurement_claims"] = {
                    key: component.pop(key)
                    for key in ("tight_alpha_bbox", "opaque_pixels")
                    if key in component
                }
        composed = Image.new("RGBA", tuple(cmap["canvas"]))
        sheet = Image.new("RGB", (200 * len(character["components"]), 330), "#141922")
        sd = ImageDraw.Draw(sheet)
        for n, record in enumerate(cmap["draw_order_bottom_to_top"]):
            layer = Image.open(
                directory / "layers" / f"{record['component_id']}.png"
            ).convert("RGBA")
            composed = Image.alpha_composite(composed, layer)
            cell = checker((196, 270))
            cell.alpha_composite(layer.resize((196, 262), Image.Resampling.LANCZOS))
            sheet.paste(cell.convert("RGB"), (200 * n, 45))
            sd.text(
                (200 * n + 4, 5),
                record["component_id"][:23],
                font=font(11),
                fill="white",
            )
            sd.text(
                (200 * n + 4, 23),
                f"pixels: {record['opaque_pixels']}",
                font=font(11),
                fill="white",
            )
        sheet.save(directory / "qa/component-sheet.png")
        compare = Image.new("RGB", (620, 470), "#141922")
        cd = ImageDraw.Draw(compare)
        for x, label, image in [
            (
                0,
                "ORIGINAL",
                Image.open(repo / character["source_file"]).convert("RGBA"),
            ),
            (310, "LAYERS ONLY / CANDIDATE", composed),
        ]:
            cell = checker((300, 402))
            cell.alpha_composite(image.resize((300, 400), Image.Resampling.LANCZOS))
            compare.paste(cell.convert("RGB"), (x, 40))
            cd.text((x + 4, 10), label, font=font(14), fill="white")
        compare.save(directory / "qa/source-versus-layers.png")
        cell = checker((280, 440))
        cell.alpha_composite(
            composed.resize((280, 373), Image.Resampling.LANCZOS), (0, 28)
        )
        d = ImageDraw.Draw(cell)
        d.text((6, 5), cid, font=font(16), fill="white")
        d.text((6, 410), "CUTS NEED ANATOMICAL REVIEW", font=font(12), fill="#ffd080")
        gallery.paste(cell.convert("RGB"), (10 + i % 5 * 300, 58 + i // 5 * 500))
        character["technical_readiness_state"] = (
            "candidate_partition_needs_anatomical_review"
        )
    gallery.save(package / "previews/local-character-library-review-gallery.png")
    manifest["status"] = "LOCAL_CANDIDATES_BUILT_ANATOMICAL_REVIEW_REQUIRED"
    manifest["human_approved"] = False
    for defect in manifest.get("glm_candidate_defects_diagnosed", []):
        if "remediation" in defect:
            defect["received_proposed_remediation_unverified"] = defect.pop(
                "remediation"
            )
    write_json(package / "character-library-manifest.json", manifest)
