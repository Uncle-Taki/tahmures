"""Deterministic front-view facial-state prototype from frozen approved v7.

No provider calls. New eyelid/hidden-brow art is prototype-only reconstruction.
Run using system Python with Pillow and NumPy from the repository root.
"""

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

P = Path(__file__).resolve().parents[1]
ROOT = P.parents[3]
SOURCE = ROOT / "Characters/tahmures/versions/layout01-v7"
APPROVAL = (
    ROOT / "Characters/tahmures/workflow/approvals/layout01-v7-human-approval.json"
)
MASTER = ROOT / "Characters/tahmures/versions/layout01-v2/source/approved_master.png"
CANVAS = (1086, 1448)
FRAME_SIZE = (720, 720)
HEAD_CROP = (350, 0, 730, 432)
FPS = 12
SECONDS = 8


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def assert_source():
    approval = json.loads(APPROVAL.read_text())
    assert digest(SOURCE / "manifest.json") == approval["manifest_sha256"]
    assert digest(SOURCE / "files-sha256.json") == approval["file_index_sha256"]
    assert approval["authority"] == "HUMAN_OWNER"
    index = json.loads((SOURCE / "files-sha256.json").read_text())
    assert all(digest(SOURCE / rel) == value for rel, value in index.items())
    actual = {
        str(p.relative_to(SOURCE))
        for p in SOURCE.rglob("*")
        if p.is_file() and p.name != "files-sha256.json"
    }
    assert actual == set(index), "Frozen source inventory changed."
    source_manifest = json.loads((SOURCE / "manifest.json").read_text())
    assert digest(MASTER) == source_manifest["source_image_sha256"]
    return approval


def bezier(points):
    p0, p1, p2, p3 = [np.array(point, dtype=float) for point in points]
    return [
        tuple(
            (1 - t) ** 3 * p0
            + 3 * (1 - t) ** 2 * t * p1
            + 3 * (1 - t) * t * t * p2
            + t**3 * p3
        )
        for t in np.linspace(0, 1, 80)
    ]


def skin_patch(alpha, source, obstacles):
    """Fit a local skin colour plane using actual skin outside the feature."""
    support = alpha > 0
    area = Image.fromarray(support.astype(np.uint8) * 255, "L")
    grown = np.array(area.filter(ImageFilter.MaxFilter(5))) > 0
    ring = (np.array(area.filter(ImageFilter.MaxFilter(15))) > 0) & ~grown
    rgb = source[..., :3].astype(float)
    skin = (rgb[..., 0] > 170) & ((rgb[..., 0] - rgb[..., 1]) > 25)
    skin &= (rgb[..., 1] - rgb[..., 2]) > 25
    samples = ring & skin & ~obstacles
    ys, xs = np.nonzero(samples)
    assert len(xs) > 30, "Insufficient genuine skin samples; do not guess a fill."
    cy, cx = np.mean(ys), np.mean(xs)
    design = np.stack([np.ones(len(xs)), (xs - cx) / 25, (ys - cy) / 25], axis=1)
    coef = np.linalg.lstsq(design, rgb[ys, xs], rcond=None)[0]
    yy, xx = np.nonzero(grown)
    field = np.stack([np.ones(len(xx)), (xx - cx) / 25, (yy - cy) / 25], axis=1) @ coef
    centre = np.median(rgb[ys, xs], axis=0)
    field = np.clip(field, centre - 14, centre + 14)
    patch = np.zeros((*source.shape[:2], 4), dtype=np.uint8)
    patch[yy, xx, :3] = np.clip(np.round(field), 0, 255).astype(np.uint8)
    # All original feature pixels are fully covered. New edges blend into skin.
    matte = area.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(0.45))
    matte_array = np.array(matte)
    matte_array[support] = 255
    matte_array[obstacles & ~support] = 0
    patch[..., 3] = matte_array
    visible = matte_array > 0
    # Fill faint antialias-support pixels with the same analytic skin field.
    ey, ex = np.nonzero(visible & ~grown)
    edge = np.stack([np.ones(len(ex)), (ex - cx) / 25, (ey - cy) / 25], axis=1) @ coef
    patch[ey, ex, :3] = np.clip(
        np.round(np.clip(edge, centre - 14, centre + 14)), 0, 255
    )
    return patch, {
        "skin_sample_count": len(xs),
        "skin_plane_coefficients": coef.tolist(),
    }


def save_asset(name, arr, pivot, method):
    path = P / "assets" / (name + ".png")
    Image.fromarray(arr, "RGBA").save(path)
    alpha = Image.fromarray(arr[..., 3], "L")
    alpha.save(P / "masks" / (name + ".png"))
    visible = arr[..., 3] > 0
    Image.new("L", CANVAS).save(P / "provenance" / (name + "__source.png"))
    Image.fromarray(visible.astype(np.uint8) * 255, "L").save(
        P / "provenance" / (name + "__reconstructed.png")
    )
    return {
        "id": name,
        "path": str(path.relative_to(P)),
        "sha256": digest(path),
        "mask_path": f"masks/{name}.png",
        "alpha_bbox": list(alpha.getbbox()),
        "pivot": pivot,
        "status": "PROTOTYPE_RECONSTRUCTION_NOT_HUMAN_APPROVED",
        "method": method,
        "provenance": {
            "source_pixel_mask": f"provenance/{name}__source.png",
            "reconstructed_pixel_mask": f"provenance/{name}__reconstructed.png",
        },
    }


def make_closed_eye(key, sprite, source, obstacles, pivot):
    arr = np.array(sprite)
    patch, recipe = skin_patch(arr[..., 3], source, obstacles)
    cx, cy = pivot["x"], pivot["y"]
    points = [(cx - 17, cy), (cx - 8, cy + 6), (cx + 8, cy + 6), (cx + 17, cy)]
    box = (cx - 23, cy - 5, cx + 24, cy + 13)
    scale = 8
    line = Image.new("RGBA", ((box[2] - box[0]) * scale, (box[3] - box[1]) * scale))
    draw = ImageDraw.Draw(line)
    curve = [((x - box[0]) * scale, (y - box[1]) * scale) for x, y in bezier(points)]
    draw.line(curve, fill=(8, 5, 5, 255), width=18, joint="curve")
    line = line.resize((box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
    out = Image.fromarray(patch, "RGBA")
    out.alpha_composite(line, box[:2])
    name = key + "_closed"
    record = save_asset(
        name,
        np.array(out),
        pivot,
        "Local skin underdraw plus supersampled closed eyelid arc; "
        "all new artwork reconstructed",
    )
    record["recipe"] = {
        **recipe,
        "eyelid_bezier_control_points": points,
        "stroke_width_px": 2.25,
    }
    controls = " ".join(f"{x},{y}" for x, y in points[1:])
    (P / "assets" / (name + "_lid.svg")).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1086" height="1448" '
        f'viewBox="0 0 1086 1448"><path d="M {points[0][0]},{points[0][1]} '
        f'C {controls}" fill="none" stroke="#080505" stroke-width="2.25" '
        'stroke-linecap="round"/></svg>\n'
    )
    return out, record


def assemble(sprites, order, overrides=None, move=None, auxiliary=None):
    result = Image.new("RGBA", CANVAS)
    for key in order:
        sprite = (overrides or {}).get(key, sprites[key])
        if move and key == move["sprite"]:
            shifted = Image.new("RGBA", CANVAS)
            shifted.paste(sprite, (move["dx"], move["dy"]))
            sprite = shifted
        result = Image.alpha_composite(result, sprite)
        if key == "head_base" and auxiliary is not None:
            result = Image.alpha_composite(result, auxiliary)
    return result


def sheet(images, labels, path, box=HEAD_CROP, zoom=1):
    width, height = (box[2] - box[0]) * zoom, (box[3] - box[1]) * zoom
    result = Image.new("RGB", (width * len(images), height + 34), (243, 241, 232))
    draw = ImageDraw.Draw(result)
    for i, (im, label) in enumerate(zip(images, labels, strict=True)):
        crop = im.crop(box).resize((width, height), Image.Resampling.NEAREST)
        bg = Image.new("RGBA", crop.size, (243, 241, 232, 255))
        bg.alpha_composite(crop)
        result.paste(bg.convert("RGB"), (i * width, 34))
        draw.text((i * width + 4, 8), label, fill=(0, 0, 0))
    result.save(path)


def state_at(t):
    if 1.5 <= t < 1.67 or 4.5 <= t < 4.67:
        return "blink_closed"
    if 2.25 <= t < 4.25:
        return "thinking"
    if 5.0 <= t < 6.0:
        return "open_test"
    if 6.25 <= t < 7.25:
        return "mouthless"
    return "neutral"


def main():
    approval = assert_source()
    for folder in ["assets", "masks", "provenance", "states", "previews", "frames"]:
        (P / folder).mkdir(exist_ok=True)
    manifest = json.loads((SOURCE / "manifest.json").read_text())
    records = {s["id"]: s for s in manifest["sprites"]}
    sprites = {
        key: Image.open(SOURCE / rec["path"]).convert("RGBA")
        for key, rec in records.items()
    }
    source = np.array(Image.open(MASTER).convert("RGBA"))
    obstacles = np.zeros(source.shape[:2], bool)
    for key in [
        "diadem_gold",
        "nose",
        "ear_left",
        "ear_right",
        "eyebrow_left",
        "eyebrow_right",
    ]:
        obstacles |= np.array(sprites[key])[..., 3] > 0
    new = []
    closed = {}
    for key in ["eye_left", "eye_right"]:
        closed[key], record = make_closed_eye(
            key, sprites[key], source, obstacles, records[key]["pivot"]
        )
        new.append(record)
    brow_obstacles = np.zeros_like(obstacles)
    for key in ["diadem_gold", "nose", "eye_left", "eye_right", "eyebrow_right"]:
        brow_obstacles |= np.array(sprites[key])[..., 3] > 0
    old_brow = np.array(sprites["eyebrow_left"])
    receiver, recipe = skin_patch(old_brow[..., 3], source, brow_obstacles)
    brow_record = save_asset(
        "thinking_brow_underlay",
        receiver,
        records["eyebrow_left"]["pivot"],
        "Local reconstructed skin beneath original eyebrow footprint "
        "for one-pixel upward shift",
    )
    brow_record["recipe"] = recipe
    new.append(brow_record)
    neutral_order = manifest["render_groups"]["puppet_core_neutral"]["layer_order"]
    rendered = {
        "neutral": assemble(sprites, neutral_order),
        "blink_closed": assemble(sprites, neutral_order, overrides=closed),
        "thinking": assemble(
            sprites,
            neutral_order,
            move={"sprite": "eyebrow_left", "dx": 0, "dy": -1},
            auxiliary=Image.fromarray(receiver, "RGBA"),
        ),
        "open_test": assemble(
            sprites, manifest["render_groups"]["puppet_core_open_test"]["layer_order"]
        ),
        "mouthless": assemble(
            sprites, manifest["render_groups"]["puppet_core"]["layer_order"]
        ),
    }
    for state, im in rendered.items():
        im.save(P / "states" / (state + ".png"))
    thinking_underlay = assemble(
        sprites,
        [k for k in neutral_order if k != "eyebrow_left"],
        auxiliary=Image.fromarray(receiver, "RGBA"),
    )
    thinking_underlay.save(P / "previews/thinking_underlay_qa_only.png")
    sheet(
        list(rendered.values()), list(rendered), P / "previews/state-contact-sheet.png"
    )
    sheet(
        [rendered["neutral"], rendered["blink_closed"], rendered["thinking"]],
        ["source eyes", "closed eyelids", "thinking (brow -1px)"],
        P / "previews/eye-brow-zoom.png",
        (465, 100, 615, 200),
        4,
    )
    sheet(
        [
            sprites["eye_left"],
            closed["eye_left"],
            sprites["eye_right"],
            closed["eye_right"],
        ],
        ["left original", "left closed", "right original", "right closed"],
        P / "previews/eye-components.png",
        (465, 100, 615, 200),
        3,
    )
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font = ImageFont.truetype(font_path, 20)
    small = ImageFont.truetype(font_path, 15)
    labels = {
        "neutral": "Neutral — approved v7",
        "blink_closed": "Blink — reconstructed closed eyelids",
        "thinking": "Thinking test — one-pixel brow raise",
        "open_test": "Small-open mouth test",
        "mouthless": "Mouthless receiver",
    }
    frames = []
    timeline = []
    durations = []
    for frame in range(FPS * SECONDS):
        t = frame / FPS
        state = state_at(t)
        image = Image.new("RGBA", FRAME_SIZE, (243, 241, 232, 255))
        head = (
            rendered[state].crop(HEAD_CROP).resize((494, 562), Image.Resampling.LANCZOS)
        )
        image.alpha_composite(head, (113, 55))
        draw = ImageDraw.Draw(image)
        draw.text(
            (28, 18),
            "Tahmures / Layout 01 facial-state prototype",
            font=font,
            fill=(35, 29, 25),
        )
        draw.text((28, 627), labels[state], font=font, fill=(35, 29, 25))
        draw.text(
            (28, 665),
            "Front view · prototype only · silent",
            font=small,
            fill=(80, 76, 70),
        )
        draw.line([(28, 699), (692, 699)], fill=(170, 165, 154), width=3)
        cursor = 28 + round(664 * frame / (FPS * SECONDS - 1))
        draw.ellipse((cursor - 4, 695, cursor + 4, 703), fill=(100, 72, 35))
        rgb = image.convert("RGB")
        rgb.save(P / "frames" / f"frame-{frame:03d}.png")
        frames.append(rgb)
        # GIF timing uses 10 ms units; split 8 seconds evenly over 96 frames.
        duration = (round((frame + 1) * 100 / FPS) - round(frame * 100 / FPS)) * 10
        durations.append(duration)
        timeline.append(
            {
                "frame": frame,
                "start_ms": sum(durations[:-1]),
                "duration_ms": duration,
                "state": state,
            }
        )
    # One shared palette prevents per-frame quantisation from flickering on
    # an otherwise stationary face. WebP remains exact lossless RGB.
    atlas = Image.new("RGB", (FRAME_SIZE[0] * len(rendered), FRAME_SIZE[1]))
    for i, key in enumerate(rendered):
        sample = next(
            frame
            for frame, cue in zip(frames, timeline, strict=True)
            if cue["state"] == key
        )
        atlas.paste(sample, (i * FRAME_SIZE[0], 0))
    palette = atlas.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    palette_record = Image.new("P", (16, 16))
    palette_record.putpalette(palette.getpalette())
    palette_record.putdata(list(range(256)))
    palette_record.save(P / "previews/gif-palette.png")
    indexed = [
        frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames
    ]
    indexed[0].save(
        P / "previews/facial-states.gif",
        save_all=True,
        append_images=indexed[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=1,
    )
    frames[0].save(
        P / "previews/facial-states.webp",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        lossless=True,
        quality=100,
        method=4,
    )
    prototype = {
        "schema_version": 1,
        "phase": "LAYOUT01_FACIAL_STATE_PROTOTYPE_01",
        "status": "PROTOTYPE_CANDIDATE",
        "human_approved": False,
        "character_id": manifest["character_id"],
        "display_name_fa": manifest["display_name_fa"],
        "canvas": list(CANVAS),
        "source": {
            "manifest_path": str(SOURCE.relative_to(ROOT) / "manifest.json"),
            "manifest_sha256": approval["manifest_sha256"],
            "index_sha256": approval["file_index_sha256"],
            "approval": str(APPROVAL.relative_to(ROOT)),
        },
        "new_assets": new,
        "render_order": neutral_order,
        "states": {
            "neutral": {"group": "puppet_core_neutral"},
            "blink_closed": {
                "group": "puppet_core_neutral",
                "replace": {
                    "eye_left": "eye_left_closed",
                    "eye_right": "eye_right_closed",
                },
            },
            "thinking": {
                "group": "puppet_core_neutral",
                "auxiliary_after_head_base": "thinking_brow_underlay",
                "move": {"sprite": "eyebrow_left", "dx": 0, "dy": -1},
            },
            "open_test": {"group": "puppet_core_open_test"},
            "mouthless": {"group": "puppet_core"},
        },
        "timeline": timeline,
        "duration_ms": sum(durations),
        "fps_target": FPS,
        "limits": [
            "front view only",
            "closed eyelids are reconstructed prototype art",
            "one-pixel brow shift only",
            "existing small-open patch is not a speech viseme",
            "no combined expression transforms, body, Godot, TTS or lip sync",
        ],
    }
    dump(P / "manifest.json", prototype)
    print(
        "Rendered five states, 96 PNG frames, 8-second GIF and lossless animated WebP."
    )
    assert_source()


if __name__ == "__main__":
    main()
