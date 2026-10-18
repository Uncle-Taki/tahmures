"""Reproduce v7 packaging/QA from immutable v6 artwork, never edit sources."""

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

C = Path(__file__).resolve().parents[1]
BASE = C.parent / "layout01-v6"
V5 = C.parent / "layout01-v5"
V2 = C.parent / "layout01-v2"
SIZE = (1086, 1448)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compose(sprites, order, move=None, dx=0, dy=0, omit=None):
    out = Image.new("RGBA", SIZE)
    for key in order:
        if key == omit:
            continue
        im = sprites[key]
        if key == move:
            layer = Image.new("RGBA", SIZE)
            layer.paste(im, (dx, dy))
            im = layer
        out = Image.alpha_composite(out, im)
    return out


def plate(images, labels, box, zoom, path, background="light"):
    width = (box[2] - box[0]) * zoom
    height = (box[3] - box[1]) * zoom
    result = Image.new("RGB", (width * len(images), height + 34), (245, 243, 235))
    draw = ImageDraw.Draw(result)
    for i, (im, label) in enumerate(zip(images, labels, strict=True)):
        tile = Image.new(
            "RGBA",
            (width, height),
            (25, 25, 29, 255) if background == "dark" else (245, 243, 235, 255),
        )
        if background == "checker":
            td = ImageDraw.Draw(tile)
            for y in range(0, height, 16):
                for x in range(0, width, 16):
                    if (x // 16 + y // 16) % 2:
                        td.rectangle((x, y, x + 15, y + 15), fill=(180, 180, 180, 255))
        tile.alpha_composite(
            im.crop(box).resize((width, height), Image.Resampling.NEAREST)
        )
        result.paste(tile.convert("RGB"), (i * width, 34))
        draw.text((i * width + 4, 7), label, fill=(0, 0, 0))
    result.save(path)


def main():
    assert digest(BASE / "manifest.json") == (
        "ac574324a3c3f8f5037c70c49188a6608f771fe6a6138061cbedf85ba7c9a8ce"
    )
    assert digest(BASE / "files-sha256.json") == (
        "52ba68c21e9bc13f656cc63e50c99471032a5bc20459356310c065ef1121b430"
    )
    index = json.loads((BASE / "files-sha256.json").read_text())
    assert all(digest(BASE / rel) == value for rel, value in index.items())
    manifest = json.loads((BASE / "manifest.json").read_text())
    manifest.update(
        version="layout01-v7",
        revision=(
            "Codex review-package correction from immutable Claude-produced v6: "
            "all artwork/masks unchanged; current QA sheets and documentation."
        ),
        implementation_provenance={
            "v6_neck_artist": "CLAUDE per actual implementation report",
            "v7_package_and_verification": "CODEX",
            "artwork_changed_vs_v6": False,
            "source_candidate": "layout01-v6",
        },
    )
    (C / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    )
    sprites = {
        rec["id"]: Image.open(C / rec["path"]).convert("RGBA")
        for rec in manifest["sprites"]
    }
    for rec in manifest["sprites"]:
        for rel in [
            rec["path"],
            rec["mask_path"],
            rec["provenance"]["source_pixel_mask"],
            rec["provenance"]["reconstructed_pixel_mask"],
        ]:
            assert digest(C / rel) == digest(BASE / rel), rel
    states = {}
    for name, group in [
        ("mouthless", "puppet_core"),
        ("neutral", "puppet_core_neutral"),
        ("open_test", "puppet_core_open_test"),
    ]:
        im = compose(sprites, manifest["render_groups"][group]["layer_order"])
        im.save(C / manifest["previews"][name])
        states[name] = im
    stress = json.loads((BASE / "stress-tests.json").read_text())
    stress["revision"] = (
        "v7: unchanged v6 artwork; actual manifest assemblies regenerated"
    )
    for sample in stress["samples"]:
        order = manifest["render_groups"][sample["render_group"]]["layer_order"]
        im = compose(
            sprites,
            order,
            sample["moved_sprite"],
            sample["offset_px"]["x"],
            sample["offset_px"]["y"],
        )
        im.save(C / sample["path"])
    (C / "stress-tests.json").write_text(json.dumps(stress, indent=2) + "\n")
    p = C / "previews/plates"
    master = Image.open(V2 / "source/approved_master.png").convert("RGBA")
    labels = ["A mouthless", "B neutral", "C open test"]
    plate(
        [master] + list(states.values()),
        ["source"] + labels,
        (350, 0, 730, 432),
        1,
        p / "D_source_comparison.png",
    )
    for bg in ["light", "dark", "checker"]:
        for kind, box, zoom in [
            ("head_100", (350, 0, 730, 432), 1),
            ("mouth", (480, 195, 610, 285), 4),
            ("neck", (440, 300, 640, 400), 4),
        ]:
            plate(
                list(states.values()), labels, box, zoom, p / f"D_{kind}_{bg}.png", bg
            )
    plate(list(states.values()), labels, (440, 300, 640, 400), 5, p / "D_neck_zoom.png")
    plate(
        list(states.values()), labels, (480, 195, 610, 285), 6, p / "D_mouth_zoom.png"
    )
    keys = list(sprites)
    for offset in range(0, len(keys), 4):
        row = keys[offset : offset + 4]
        plate(
            [sprites[key] for key in row],
            row,
            (350, 0, 730, 432),
            1,
            p / f"E_components_{offset // 4}.png",
            "checker",
        )
        plate(
            [Image.open(C / f"masks/{key}.png").convert("RGBA") for key in row],
            row,
            (350, 0, 730, 432),
            1,
            p / f"E_masks_{offset // 4}.png",
        )
        provenance = []
        for key in row:
            src = Image.open(C / f"provenance/{key}__source.png").convert("L")
            rec = Image.open(C / f"provenance/{key}__reconstructed.png").convert("L")
            im = Image.new("RGBA", SIZE)
            im.paste((185, 185, 185, 255), (0, 0), src)
            im.paste((220, 40, 40, 255), (0, 0), rec)
            provenance.append(im)
        plate(
            provenance,
            row,
            (350, 0, 730, 432),
            1,
            p / f"E_provenance_{offset // 4}.png",
        )
    for key in [
        "moustache",
        "beard",
        "head_base",
        "lower_face_neutral",
        "lower_face_open_test",
    ]:
        plate([sprites[key]], [key], (480, 195, 610, 285), 5, p / f"E_{key}.png")
    under = compose(
        sprites,
        manifest["render_groups"]["puppet_core_neutral"]["layer_order"],
        omit="moustache",
    )
    plate([under], ["QA underlay only"], (480, 195, 610, 285), 5, p / "E_underlay.png")
    for sample in stress["samples"]:
        plate(
            [Image.open(C / sample["path"]).convert("RGBA")],
            [sample["name"]],
            (480, 205, 605, 265),
            4,
            p / (sample["name"] + ".png"),
        )
    plate(
        [Image.open(V5 / "previews/neutral.png").convert("RGBA"), states["neutral"]],
        ["v5 rejected neck", "v7 current neck (same v6 artwork)"],
        (440, 300, 640, 400),
        5,
        p / "F_neck_v5_v7_neutral.png",
        "checker",
    )
    (p / "README.md").write_text(
        "# Current v7 inspection evidence\n\n"
        "D/E sheets and named stress plates are regenerated from the actual v7 "
        "exports, including the changed hair alpha/provenance. Grey means retained "
        "source pixels; red means reconstructed artwork. Raw A/B/C and all 18 stress "
        "renders use actual manifest layers. No master-image backing.\n\n"
        "F files naming v6 retain historical construction comparisons; v7 artwork "
        "equals v6 byte-for-byte. F_neck_v5_v7_neutral.png is the current comparison. "
        "E_underlay is QA only, never a rig state.\n"
    )
    print("v7 metadata/QA rebuilt; all exported artwork and masks identical to v6.")


if __name__ == "__main__":
    main()
