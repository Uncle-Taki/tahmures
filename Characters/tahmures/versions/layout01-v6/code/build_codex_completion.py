"""Bounded v5 completion from immutable v4. No provider or source writes.

Hand-defined local contours/overlap replace mottled diffusion at the mouth.
Only the damaged neck material is repainted; source alpha remains immutable.
All new surface and matte pixels are recorded as reconstruction.
"""

import copy
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

DEST = Path(__file__).resolve().parents[1]
ROOT = DEST.parents[3]
BASE = DEST.parent / "layout01-v4"
V2 = DEST.parent / "layout01-v2"
SIZE = (1086, 1448)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def curve(points, step=12):
    """Catmull-Rom interpolation of manually traced contour anchors."""
    pts = [points[0]] + points + [points[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = [np.array(p, dtype=float) for p in pts[i - 1 : i + 3]]
        for t in np.linspace(0, 1, step, endpoint=False):
            v = 0.5 * (
                (2 * p1)
                + (-p0 + p2) * t
                + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                + (-p0 + 3 * p1 - 3 * p2 + p3) * t * t * t
            )
            out.append(tuple(v))
    out.append(points[-1])
    return out


def mask_polygon(points):
    # Supersampling is localized to the head region, not a huge full canvas.
    box = (450, 190, 620, 285)
    scale = 8
    im = Image.new("L", ((box[2] - box[0]) * scale, (box[3] - box[1]) * scale))
    ImageDraw.Draw(im).polygon(
        [((x - box[0]) * scale, (y - box[1]) * scale) for x, y in points], fill=255
    )
    im = im.resize((box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
    full = Image.new("L", SIZE)
    full.paste(im, box[:2])
    return np.array(full)


def compose(sprites, order, move=None, dx=0, dy=0, omit=None):
    result = Image.new("RGBA", SIZE)
    for key in order:
        if key == omit:
            continue
        im = Image.fromarray(sprites[key], "RGBA")
        if key == move:
            layer = Image.new("RGBA", SIZE)
            layer.paste(im, (dx, dy))
            im = layer
        result = Image.alpha_composite(result, im)
    return result


def main():
    manifest = json.loads((BASE / "manifest.json").read_text())
    original = {
        s["id"]: np.array(Image.open(BASE / s["path"]).convert("RGBA"))
        for s in manifest["sprites"]
    }
    sprites = {key: arr.copy() for key, arr in original.items()}
    source = np.array(Image.open(V2 / "source/approved_master.png"))
    domain_image = Image.open(V2 / "masks/visible_head_domain.png").convert("L")
    domain = np.array(domain_image) > 0
    yy, xx = np.indices(source.shape[:2])

    # R2-01/02: an opaque foreground core has a deliberately smooth lower
    # contour. Its upper outline/nose junction retain the original extraction.
    bottom = curve(
        [
            (485, 223),
            (496, 231),
            (511, 234),
            (524, 232),
            (540, 225),
            (555, 231),
            (568, 234),
            (584, 233),
            (596, 225),
        ]
    )
    mo = sprites["moustache"]
    source_mo = np.array(Image.open(V2 / "face/moustache.png"))
    # The source upper contour is preserved; a smooth local lower contour
    # avoids the extraction's jagged notch-ink fringe.
    top = []
    for x in range(485, 597):
        ys = np.nonzero(source_mo[:, x, 3] > 0)[0]
        if len(ys):
            top.append((x, float(ys.min()) - 0.5))
    south = mask_polygon(top + list(reversed(bottom)))
    south_zone = (yy >= 222) & (yy <= 241) & (xx >= 482) & (xx <= 599)
    mo[..., 3][south_zone] = south[south_zone]
    # No skin blend or old black notch ink in the southern foreground.
    # Brown tones sampled from existing moustache/receiver interiors.
    tone = np.stack(
        [
            46 + 1.5 * np.sin((xx - 480) / 18),
            33 + np.sin((xx - 480) / 18),
            28 + 0.8 * np.sin((xx - 480) / 18),
        ],
        axis=2,
    )
    mo[..., :3][south_zone] = np.round(tone[south_zone]).astype(np.uint8)
    # Keep source-edge AA at the top, but make the internal foreground opaque
    # where v4's re-solved matte otherwise admits shifted skin bars.
    core = (mo[..., 3] > 0) & (yy >= 218) & (yy <= 221)
    mo[..., 3][core] = 255
    bad = core & ((mo[..., 0] > 90) | (mo[..., 0] < 20))
    mo[..., :3][bad] = np.round(tone[bad]).astype(np.uint8)

    # A has a continuous cloned receiver beneath the complete mouth overlap.
    union = Image.fromarray((source_mo[..., 3] > 0).astype(np.uint8) * 255, "L").filter(
        ImageFilter.MaxFilter(7)
    )
    receiver = ((np.array(union) > 0) & (yy >= 224)) | (
        (yy >= 228) & (yy <= 245) & (xx >= 502) & (xx <= 578)
    )
    for key in ["beard"]:
        a = sprites[key]
        region = receiver & domain
        a[..., 3][region] = source[..., 3][region]
        a[..., :3][region] = np.round(tone[region]).astype(np.uint8)

    # Shared irregular patch: safe upper overlap behind the moustache. It is
    # still a local lower-face patch, not a full-head source backing.
    patch_top = mask_polygon(
        curve(
            [
                (504, 233),
                (505, 223),
                (514, 219),
                (525, 220),
                (541, 219),
                (557, 220),
                (569, 220),
                (576, 224),
                (577, 234),
            ]
        )
        + [(570, 244), (509, 244)]
    )
    old_patch = original["lower_face_neutral"][..., 3]
    patch_alpha = np.maximum(old_patch, patch_top)
    patch_alpha = np.minimum(patch_alpha, source[..., 3])
    neutral = original["lower_face_neutral"].copy()
    neutral[..., 3] = patch_alpha
    # Extend a smooth skin field from the actual exposed lower-lip surface
    # into its hidden overlap, with no old moustache ink or mixed fill.
    upper = (patch_top > 0) & (yy <= 237)
    old_ink = (source_mo[..., 3] > 0) & (patch_alpha > 0) & ~upper
    neutral[..., :3][old_ink] = np.round(tone[old_ink]).astype(np.uint8)
    for x in range(490, 595):
        # Source y245 is inside genuine exposed skin for centre columns;
        # limit tones at far corners so hidden surfaces have stable colour.
        sx = min(568, max(516, x))
        rgb = source[245, sx, :3].astype(float)
        if rgb[0] < 150:
            rgb = np.array([247, 179, 115], float)
        sel = upper[:, x]
        neutral[sel, x, :3] = np.clip(np.round(rgb), 0, 255).astype(np.uint8)
    sprites["lower_face_neutral"] = neutral
    opent = neutral.copy()
    opening = np.any(
        original["lower_face_open_test"][:, :, :3]
        != original["lower_face_neutral"][:, :, :3],
        axis=2,
    )
    opent[..., :3][opening] = original["lower_face_open_test"][..., :3][opening]
    sprites["lower_face_open_test"] = opent

    # R2-03: continuous vertical hair flow, not colour-class scanline fill.
    # Retain all original alpha/silhouette. Reconstruct only two local wedges.
    cleanup = np.load(BASE / "code/_neck_clean.npy")
    cleanup = (
        np.array(
            Image.fromarray(cleanup.astype(np.uint8) * 255, "L").filter(
                ImageFilter.MaxFilter(3)
            )
        )
        > 0
    )
    # Keep real source neck skin, even if the hidden-coverage wedge overlaps
    # it. Only dark hair or garment-colour samples require this continuation.
    # Trace the genuine neck edge from source skin continuity, rather than
    # treating warm collar/trim colours as skin. The round lower outline is
    # kept with a one-pixel margin.
    neck_left = np.interp(
        yy[:, 0],
        [326, 330, 338, 340, 350, 358, 365, 370, 374],
        [494, 494, 488, 488, 490, 492, 504, 520, 540],
    )[:, None]
    neck_right = np.interp(
        yy[:, 0],
        [326, 330, 338, 340, 350, 358, 365, 370, 374],
        [585, 585, 592, 592, 591, 589, 578, 561, 541],
    )[:, None]
    neck = (
        (yy >= 326)
        & (yy <= 372)
        & (xx >= 463)
        & (xx <= 606)
        & ((xx < neck_left - 1) | (xx > neck_right + 1))
    ) | cleanup
    true_skin = (
        (xx >= neck_left)
        & (xx <= neck_right)
        & (source[..., 0] >= 140)
        & (source[..., 2] >= 74)
    )
    neck &= ~true_skin
    # Smooth along y with vertically curving narrow strands. Palette matches
    # the adjacent original hair; no garment-yellow or blue is sampled.
    offset = xx - 0.14 * (yy - 326)
    wave = 1.5 * np.sin(offset / 2.9)
    hair_tone = np.stack([44 + wave, 32 + 0.7 * wave, 28 + 0.5 * wave], axis=2)
    for key in ["head_base", "hair_back"]:
        a = sprites[key]
        sel = neck & (a[..., 3] > 0)
        a[..., :3][sel] = np.clip(np.round(hair_tone[sel]), 0, 255).astype(np.uint8)

    for folder in [
        "head",
        "face",
        "mouths",
        "masks",
        "provenance",
        "previews",
        "previews/stress",
        "previews/plates",
    ]:
        (DEST / folder).mkdir(parents=True, exist_ok=True)
    domain_image.save(DEST / "masks/visible_head_domain.png")
    manifest = copy.deepcopy(manifest)
    methods = {
        "moustache": (
            "Codex R2 completion: manually traced smooth southern "
            "contour, supersampled matte and opaque interior brown "
            "surface; original upper outline retained. RGB/alpha "
            "modifications are reconstructed, not source pixels."
        ),
        "beard": (
            "Retains v4 receiver/underdraw; local brown continuation "
            "removes detached mouth-like ink in the moustache overlap. "
            "All previous reconstruction ownership retained."
        ),
        "lower_face_neutral": (
            "Retains v4 lower-lip/skin/beard source relationship with "
            "expanded irregular upper overlap and deliberate smooth "
            "hidden skin field; no mottled moustache-ink diffusion."
        ),
        "lower_face_open_test": (
            "Same revised shared patch as neutral with the accepted "
            "59-pixel lip-line opening retained from v4; no new "
            "expression state."
        ),
        "head_base": (
            "Retains v4 feature underdraw; damaged local neck wedge "
            "rebuilt as smooth hair continuation matching adjacent "
            "brown palette. Source alpha and neck silhouette retained."
        ),
        "hair_back": (
            "Retains v4 source hair; only the local neck wedge gets a "
            "continuous hair-tone field, without scanline recolouring. "
            "Source alpha retained."
        ),
    }
    changes = {}
    for rec in manifest["sprites"]:
        key = rec["id"]
        a = sprites[key]
        changed = np.any(a != original[key], axis=2)
        changes[key] = int(changed.sum())
        path = DEST / rec["path"]
        Image.fromarray(a, "RGBA").save(path)
        alpha = Image.fromarray(a[..., 3], "L")
        alpha.save(DEST / rec["mask_path"])
        prior = (
            np.array(Image.open(BASE / rec["provenance"]["reconstructed_pixel_mask"]))
            > 0
        )
        visible = a[..., 3] > 0
        retained = np.all(a[..., :3] == source[..., :3], axis=2) & (
            a[..., 3] <= source[..., 3]
        )
        reconstructed = visible & (prior | changed | ~retained)
        src = visible & ~reconstructed
        for field, mask in [
            ("source_pixel_mask", src),
            ("reconstructed_pixel_mask", reconstructed),
        ]:
            Image.fromarray(np.where(mask, 255, 0).astype(np.uint8), "L").save(
                DEST / rec["provenance"][field]
            )
        rec.update(
            sha256=digest(path),
            mask_sha256=digest(DEST / rec["mask_path"]),
            alpha_bounding_rect=list(alpha.getbbox()),
        )
        if key in methods:
            rec["provenance"]["reconstruction_method"] = methods[key]
            rec["provenance"]["alpha_edge_modifications"] = (
                "See exact exported alpha mask; source alpha retained "
                "except local supersampled mouth interface/overlap. All "
                "increased or changed alpha is reconstructed."
            )
    manifest.update(
        version="layout01-v5",
        revision=(
            "GLM revision 2 diagnosis, completed by Codex at the "
            "owner's request; only R2-01/02/03 repaired."
        ),
    )
    manifest["preview_only_assets"] = []
    manifest["repair_regions"] = {
        "changed_pixels_vs_v4": changes,
        "method": (
            "Hand-defined local contour/overlap and hair continuation; "
            "see code/build_codex_completion.py."
        ),
    }
    manifest["known_limitations"] = [
        "CANDIDATE; no Claude acceptance or human visual approval.",
        (
            "Front-view only. Tested patch ±2px XY and moustache ±1px "
            "XY; no arbitrary rotation or perspective."
        ),
        (
            "The lip opening is a restrained technical test, not a "
            "production speech viseme."
        ),
        (
            "Hidden skin/beard/neck artwork is reconstructed and "
            "subject to independent visual review."
        ),
        "No Godot, body/arms, speech/audio or video asset in this phase.",
    ]
    manifest["supported_motion_envelope"]["description"] = (
        "Actual declared micro-offset tests. Coverage and "
        "compositor equality do not substitute for visual "
        "inspection of seam artwork."
    )
    dump(DEST / "manifest.json", manifest)
    eroded = np.array(domain_image.filter(ImageFilter.MinFilter(3))) > 0

    def metrics(a):
        return {
            "new_fully_transparent_interior": int(
                (eroded & (source[..., 3] > 0) & (a[..., 3] == 0)).sum()
            ),
            "alpha_below_250_where_source_opaque": int(
                (eroded & (source[..., 3] >= 250) & (a[..., 3] < 250)).sum()
            ),
        }

    rendered = {}
    for state, group in [
        ("mouthless", "puppet_core"),
        ("neutral", "puppet_core_neutral"),
        ("open_test", "puppet_core_open_test"),
    ]:
        im = compose(sprites, manifest["render_groups"][group]["layer_order"])
        im.save(DEST / manifest["previews"][state])
        rendered[state] = im
    stress = json.loads((BASE / "stress-tests.json").read_text())
    stress["revision"] = (
        "v5 actual micro-offset evidence; visual QA separate from coverage"
    )
    stress["vacated_strip_rule"] = (
        "Compositing consistency only; not proof of clean underdraw."
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
        im.save(DEST / sample["path"])
        # Old numeric claims must not survive the new render.
        for k in list(sample):
            if k not in ["name", "render_group", "moved_sprite", "offset_px", "path"]:
                del sample[k]
        sample["coverage"] = metrics(np.array(im))
    stress = {k: v for k, v in stress.items() if not k.startswith("all_")}
    stress["all_coverage_pass"] = all(
        not any(s["coverage"].values()) for s in stress["samples"]
    )
    dump(DEST / "stress-tests.json", stress)

    # Unadorned source-scale and enlarged proof plates from actual layers.
    def plate(images, labels, box, zoom, path, background="light"):
        crop_size = ((box[2] - box[0]) * zoom, (box[3] - box[1]) * zoom)
        canvas = Image.new(
            "RGB", (len(images) * crop_size[0], crop_size[1] + 36), (245, 243, 235)
        )
        draw = ImageDraw.Draw(canvas)
        for i, (im, label) in enumerate(zip(images, labels, strict=True)):
            im = im.crop(box).resize(crop_size, Image.Resampling.NEAREST)
            bg = (245, 243, 235, 255) if background == "light" else (25, 25, 29, 255)
            tile = Image.new("RGBA", crop_size, bg)
            if background == "checker":
                td = ImageDraw.Draw(tile)
                for by in range(0, crop_size[1], 16):
                    for bx in range(0, crop_size[0], 16):
                        if (bx // 16 + by // 16) % 2:
                            td.rectangle(
                                (bx, by, bx + 15, by + 15), fill=(180, 180, 180, 255)
                            )
            tile.alpha_composite(im)
            canvas.paste(tile.convert("RGB"), (i * crop_size[0], 36))
            draw.text((i * crop_size[0] + 4, 8), label, fill=(0, 0, 0))
        canvas.save(DEST / "previews/plates" / path)

    master = Image.fromarray(source, "RGBA")
    plate(
        [master] + list(rendered.values()),
        ["source", "A mouthless", "B neutral", "C open test"],
        (350, 0, 730, 432),
        1,
        "D_source_comparison.png",
    )
    plate(
        list(rendered.values()),
        ["A mouthless", "B neutral", "C open test"],
        (480, 195, 610, 285),
        6,
        "D_mouth_zoom.png",
    )
    plate(
        list(rendered.values()),
        ["A mouthless", "B neutral", "C open test"],
        (440, 300, 640, 400),
        4,
        "D_neck_zoom.png",
    )
    for bg in ["light", "dark", "checker"]:
        plate(
            list(rendered.values()),
            ["A", "B", "C"],
            (350, 0, 730, 432),
            1,
            f"D_head_100_{bg}.png",
            bg,
        )
        plate(
            list(rendered.values()),
            ["A", "B", "C"],
            (480, 195, 610, 285),
            4,
            f"D_mouth_{bg}.png",
            bg,
        )
        plate(
            list(rendered.values()),
            ["A", "B", "C"],
            (440, 300, 640, 400),
            4,
            f"D_neck_{bg}.png",
            bg,
        )
    for key in [
        "moustache",
        "beard",
        "head_base",
        "lower_face_neutral",
        "lower_face_open_test",
    ]:
        plate(
            [Image.fromarray(sprites[key], "RGBA")],
            [key],
            (480, 195, 610, 285),
            5,
            f"E_{key}.png",
        )
    for sample in stress["samples"]:
        plate(
            [Image.open(DEST / sample["path"])],
            [sample["name"]],
            (480, 205, 605, 265),
            4,
            sample["name"] + ".png",
        )
    under = compose(
        sprites,
        manifest["render_groups"]["puppet_core_neutral"]["layer_order"],
        omit="moustache",
    )
    plate([under], ["QA underlay only"], (480, 195, 610, 285), 5, "E_underlay.png")
    keys = list(sprites)
    for group in range(0, len(keys), 4):
        row = keys[group : group + 4]
        plate(
            [Image.fromarray(sprites[k], "RGBA") for k in row],
            row,
            (350, 0, 730, 432),
            1,
            f"E_components_{group // 4}.png",
            "checker",
        )
        plate(
            [Image.open(DEST / f"masks/{k}.png").convert("RGBA") for k in row],
            row,
            (350, 0, 730, 432),
            1,
            f"E_masks_{group // 4}.png",
        )
        visual = []
        for key in row:
            ownership = np.zeros(source.shape, dtype=np.uint8)
            src = np.array(Image.open(DEST / f"provenance/{key}__source.png")) > 0
            rec = (
                np.array(Image.open(DEST / f"provenance/{key}__reconstructed.png")) > 0
            )
            ownership[src] = (185, 185, 185, 255)
            ownership[rec] = (220, 40, 40, 255)
            visual.append(Image.fromarray(ownership, "RGBA"))
        plate(visual, row, (350, 0, 730, 432), 1, f"E_provenance_{group // 4}.png")
    (DEST / "previews/plates/README.md").write_text(
        "# Actual layer inspection\n\nA/B/C are raw manifest "
        "assemblies. D compares source/states at source scale and "
        "zoom on three backgrounds. E shows actual exported "
        "components, alpha masks and ownership (grey retained, red "
        "reconstructed). E_underlay is QA only, never a rig "
        "surface. Each named stress plate comes from its actual "
        "PNG. No source-underlay preview is used as puppet "
        "evidence.\n"
    )
    dump(
        DEST / "code/completion-metrics.json",
        {
            "changes": changes,
            "coverage": {s: metrics(np.array(im)) for s, im in rendered.items()},
        },
    )
    print(
        json.dumps(
            {
                "changes": changes,
                "coverage": {s: metrics(np.array(im)) for s, im in rendered.items()},
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
