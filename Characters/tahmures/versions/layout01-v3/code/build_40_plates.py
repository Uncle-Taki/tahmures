#!/usr/bin/env python3
"""Layout01 v3 repair — stage 40: readable comparison/inspection plates D and E.

Plates are annotated renderings of the actual delivered components; the raw
compositions in previews/ stay unadorned. Backgrounds: checkerboard, light,
dark. Scales: 100% (source pixels) and enlarged nearest-neighbour crops.
"""
import json
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from build_lib import V3, V2, CANVAS, load_master, erode

PLATES = V3 + "/previews/plates"
HEAD_CROP = (356, 0, 724, 432)
MOUTH_CROP = (455, 175, 625, 305)
EYE_CROP = (470, 100, 615, 200)
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
NEAREST = Image.Resampling.NEAREST

SPRITE_PATHS = {
    "head_base": "head/head_base.png",
    "hair_back": "head/hair_back.png",
    "diadem_gold": "head/diadem_gold.png",
    "ear_left": "face/ear_left.png",
    "ear_right": "face/ear_right.png",
    "eye_left": "face/eye_left.png",
    "eye_right": "face/eye_right.png",
    "eyebrow_left": "face/eyebrow_left.png",
    "eyebrow_right": "face/eyebrow_right.png",
    "nose": "face/nose.png",
    "beard": "face/beard.png",
    "moustache": "face/moustache.png",
    "lower_face_neutral": "mouths/lower_face_neutral.png",
    "lower_face_open_test": "mouths/lower_face_open_test.png",
}
SPRITE_ORDER = [
    "hair_back", "head_base", "diadem_gold", "ear_right", "ear_left",
    "beard", "moustache", "nose", "eye_right", "eye_left",
    "eyebrow_right", "eyebrow_left",
    "lower_face_neutral", "lower_face_open_test",
]


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_PATH, size)


def make_bg(size, kind):
    w, h = size
    if kind == "light":
        return Image.new("RGB", size, (245, 242, 235))
    if kind == "dark":
        return Image.new("RGB", size, (28, 26, 24))
    # checkerboard
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    sq = 16
    yy, xx = np.mgrid[0:h, 0:w]
    checks = ((xx // sq) + (yy // sq)) % 2 == 0
    arr[checks] = (200, 200, 200)
    arr[~checks] = (255, 255, 255)
    return Image.fromarray(arr, "RGB")


def labeled_tile(img, title, sub=None, bg_kind="checkerboard", pad=6):
    """Paste an RGBA (or RGB) image on a background with a label bar."""
    w, h = img.size
    bar = 34 if sub is None else 52
    tile = make_bg((w + 2 * pad, h + bar + 2 * pad), bg_kind)
    if img.mode == "RGBA":
        tile.paste(img, (pad, bar + pad), img)
    else:
        tile.paste(img, (pad, bar + pad))
    d = ImageDraw.Draw(tile)
    d.text((pad + 2, 6), title, fill=(20, 18, 16), font=font(19, bold=True))
    if sub:
        d.text((pad + 2, 30), sub, fill=(70, 66, 62), font=font(14))
    return tile


def grid(tiles, cols, title, note=None, pad=12):
    tw = max(t.size[0] for t in tiles)
    th = max(t.size[1] for t in tiles)
    rows = (len(tiles) + cols - 1) // cols
    top = 64 if note is None else 92
    W = cols * tw + (cols + 1) * pad
    H = top + rows * th + (rows + 1) * pad
    sheet = make_bg((W, H), "light")
    d = ImageDraw.Draw(sheet)
    d.text((pad, 14), title, fill=(15, 13, 12), font=font(28, bold=True))
    if note:
        d.text((pad, 50), note, fill=(70, 66, 62), font=font(16))
    for i, t in enumerate(tiles):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = top + r * (th + pad)
        sheet.paste(t, (x, y))
    return sheet


def crop_scale(rgba, box, scale):
    return rgba.crop(box).resize(
        ((box[2] - box[0]) * scale, (box[3] - box[1]) * scale), NEAREST)


def outline_mask(shape_rgb, mask, box, scale, color):
    """Return the crop of shape_rgb with the mask contour painted in color."""
    edge = mask & ~erode(mask, 1)
    out = shape_rgb.crop(box).resize(
        ((box[2] - box[0]) * scale, (box[3] - box[1]) * scale), NEAREST).copy()
    arr = np.asarray(out).copy()
    e = edge[box[1]:box[3], box[0]:box[2]]
    es = np.kron(e, np.ones((scale, scale), dtype=bool))
    arr[es] = color
    return Image.fromarray(arr, "RGBA")


def changed_overlay(state, master, thresh=3):
    """Dimmed state with >thresh RGB changes vs master painted red."""
    ca = np.asarray(state.convert("RGBA"))
    both = (ca[..., 3] >= 250) & (master[..., 3] >= 250)
    diff = np.abs(ca[..., :3].astype(int) - master[..., :3].astype(int)).max(axis=2)
    changed = both & (diff > thresh)
    arr = (ca.astype(np.float64) * 0.45).astype(np.uint8)
    arr[changed] = (255, 48, 32, 255)
    return Image.fromarray(arr, "RGBA"), int(changed.sum())


def main():
    os.makedirs(PLATES, exist_ok=True)
    master = Image.open(V2 + "/source/approved_master.png").convert("RGBA")
    m = np.asarray(master)
    A = Image.open(V3 + "/previews/mouthless.png").convert("RGBA")
    B = Image.open(V3 + "/previews/neutral.png").convert("RGBA")
    C = Image.open(V3 + "/previews/open_test.png").convert("RGBA")
    M = np.load(V3 + "/code/_M.npy")
    P = np.load(V3 + "/code/_P.npy")
    meta = json.load(open(V3 + "/code/_sprite_meta.json"))

    states = [
        (master, "approved master (v2 source — NOT a rig component)", None),
        (A, "A mouthless (puppet_core)", "no patch; receiver beard"),
        (B, "B neutral (puppet_core_neutral)", "+ lower_face_neutral patch"),
        (C, "C open test (puppet_core_open_test)", "+ lower_face_open_test patch"),
    ]

    # ---------------- Plate D: source comparison ----------------
    for bg in ("checkerboard", "light", "dark"):
        tiles = [labeled_tile(img, t, s, bg) for img, t, s in states]
        grid(tiles, 2,
             "Plate D — source comparison at 100% (same scale and alignment)",
             "Left to right, top to bottom: approved master, A mouthless, "
             "B neutral, C open test. Background: %s." % bg
             ).save(PLATES + "/D_source_comparison_%s_100.png" % bg)
        tiles = [labeled_tile(crop_scale(img, HEAD_CROP, 2), t, s, bg)
                 for img, t, s in states]
        grid(tiles, 2,
             "Plate D — source comparison, head crop at 2x",
             "Approved master vs A/B/C. Background: %s." % bg
             ).save(PLATES + "/D_source_comparison_%s_zoom.png" % bg)
        tiles = [labeled_tile(crop_scale(img, MOUTH_CROP, 3), t, s, bg)
                 for img, t, s in states]
        grid(tiles, 2,
             "Plate D — mouth detail at 3x",
             "Master smile vs mouthless receiver (A), neutral patch (B), "
             "small-open test patch (C). Background: %s." % bg
             ).save(PLATES + "/D_mouth_zoom_%s.png" % bg)

    # where reconstruction changed pixels (>3 RGB vs master, both opaque)
    ov_A, nA = changed_overlay(A, m)
    ov_B, nB = changed_overlay(B, m)
    ov_C, nC = changed_overlay(C, m)
    ch = [
        (ov_A, "A vs master — changed pixels", "%d px differ >3 (red): mouth "
         "content region M replaced by cloned beard receiver" % nA),
        (ov_B, "B vs master — changed pixels", "%d px differ >3: neutral state "
             "is pixel-faithful to the master" % nB),
        (ov_C, "C vs master — changed pixels", "%d px differ >3 (red): "
             "synthesized small opening only" % nC),
    ]
    grid([labeled_tile(i, t, s, "dark") for i, t, s in ch], 2,
         "Plate D — reconstruction change map at 100%",
         "Red = RGB difference >3 vs approved master where both are opaque; "
         "base dimmed to 45%. Changes are intentionally confined to the "
         "mouth region.").save(PLATES + "/D_changed_pixels_100.png")
    grid([labeled_tile(crop_scale(i, MOUTH_CROP, 3), t, s, "dark")
          for i, t, s in ch], 2,
         "Plate D — reconstruction change map, mouth crop at 3x",
         "A: whole mouth content region M (receiver). B: none. C: opening only."
         ).save(PLATES + "/D_changed_pixels_zoom.png")

    # ---------------- Plate E: layer inspection ----------------
    sprites = {sid: Image.open(V3 + "/" + rel).convert("RGBA")
               for sid, rel in SPRITE_PATHS.items()}

    def bbox_crop(img, margin=14):
        a = np.asarray(img)[..., 3]
        ys, xs = np.nonzero(a)
        box = (max(0, xs.min() - margin), max(0, ys.min() - margin),
               min(CANVAS[0], xs.max() + 1 + margin),
               min(CANVAS[1], ys.max() + 1 + margin))
        return img.crop(box), box

    tiles = []
    for sid in SPRITE_ORDER:
        crop, _ = bbox_crop(sprites[sid])
        mm = meta[sid]
        tiles.append(labeled_tile(
            crop, sid, "vis %d px — source %d / reconstructed %d"
            % (mm["visible"], mm["source"], mm["reconstructed"]),
            "checkerboard"))
    grid(tiles, 5,
         "Plate E — rig components at 100% (alpha-bbox crops)",
         "Actual delivered sprites. Bottom row: the two swappable lower-face "
         "patches (common footprint).").save(PLATES + "/E_components_100.png")

    mouth_ids = ["beard", "moustache", "lower_face_neutral",
                 "lower_face_open_test", "head_base"]
    tiles = []
    for sid in mouth_ids:
        sub = ("receiver: M filled with cloned beard texture"
               if sid == "beard" else
               "static foreground above the patch" if sid == "moustache" else
               "pure master pixels" if sid == "lower_face_neutral" else
               "master pixels + 80 px synthesized opening"
               if sid == "lower_face_open_test" else
               "skin underdraw; hole = beard receiver area")
        tiles.append(labeled_tile(crop_scale(sprites[sid], MOUTH_CROP, 3),
                                  sid, sub, "checkerboard"))
    grid(tiles, 3,
         "Plate E — lower-face components, mouth crop at 3x",
         "Receiver (beard), static moustache foreground, both patches, and "
         "the head_base underlay showing the receiver hole."
         ).save(PLATES + "/E_components_zoom.png")

    # exact export-alpha masks
    tiles = []
    for sid in SPRITE_ORDER:
        mask = Image.open(V3 + "/masks/%s.png" % sid)
        rgb = Image.new("L", CANVAS, 0)
        alpha_vis = Image.merge(
            "RGBA", [rgb, rgb, rgb, mask.convert("L")])
        crop, _ = bbox_crop(alpha_vis)
        tiles.append(labeled_tile(crop, sid + " alpha", None, "light"))
    grid(tiles, 5,
         "Plate E — exact export-alpha masks at 100% (black = sprite alpha)",
         "masks/ files are L-mode copies of each sprite's exact alpha, "
         "including antialiased edges.").save(PLATES + "/E_alpha_masks_100.png")

    tiles = []
    for sid in ("beard", "moustache", "lower_face_neutral",
                "lower_face_open_test"):
        mask = Image.open(V3 + "/masks/%s.png" % sid)
        rgb = Image.new("L", CANVAS, 0)
        alpha_vis = Image.merge("RGBA", [rgb, rgb, rgb, mask.convert("L")])
        tiles.append(labeled_tile(crop_scale(alpha_vis, MOUTH_CROP, 3),
                                  sid + " alpha", None, "light"))
    grid(tiles, 2,
         "Plate E — exact alpha masks, mouth crop at 3x",
         "Patch footprints are identical; only RGB content differs."
         ).save(PLATES + "/E_alpha_masks_zoom.png")

    # provenance ownership masks
    def prov_overlay(sid):
        src = np.asarray(
            Image.open(V3 + "/provenance/%s__source.png" % sid).convert("L")) > 127
        rec = np.asarray(
            Image.open(V3 + "/provenance/%s__reconstructed.png" % sid).convert("L")) > 127
        arr = np.zeros((CANVAS[1], CANVAS[0], 4), dtype=np.uint8)
        arr[src] = (235, 235, 235, 255)
        arr[rec] = (255, 64, 48, 255)
        return Image.fromarray(arr, "RGBA")

    tiles = []
    for sid in SPRITE_ORDER:
        crop, _ = bbox_crop(prov_overlay(sid))
        mm = meta[sid]
        tiles.append(labeled_tile(
            crop, sid, "white = source pixels, red = reconstructed (%d)"
            % mm["reconstructed"], "dark"))
    grid(tiles, 5,
         "Plate E — pixel ownership provenance at 100%",
         "White: exact master RGB (alpha only possibly reduced). Red: "
         "reconstructed RGB (cloned/inpainted/synthesized)."
         ).save(PLATES + "/E_provenance_100.png")

    tiles = [
        labeled_tile(crop_scale(prov_overlay("beard"), MOUTH_CROP, 3),
                     "beard provenance", "red = cloned beard receiver (M)",
                     "dark"),
        labeled_tile(crop_scale(prov_overlay("lower_face_open_test"),
                                MOUTH_CROP, 3),
                     "open patch provenance", "red = 80 px synthesized opening",
                     "dark"),
        labeled_tile(crop_scale(prov_overlay("lower_face_neutral"),
                                MOUTH_CROP, 3),
                     "neutral patch provenance", "all source pixels", "dark"),
        labeled_tile(crop_scale(prov_overlay("head_base"), EYE_CROP, 3),
                     "head_base provenance (eye crop)",
                     "red = inpainted feature underdraw", "dark"),
    ]
    grid(tiles, 2,
         "Plate E — provenance detail at 3x",
         "Reconstructed surfaces are hidden under other layers in the static "
         "compositions; they exist for future local corrections/joints."
         ).save(PLATES + "/E_provenance_zoom.png")

    # receiver / patch interface
    YELLOW, RED = (255, 210, 40, 255), (255, 48, 32, 255)
    tiles = [
        labeled_tile(outline_mask(sprites["beard"], M, MOUTH_CROP, 3, RED),
                     "beard receiver + M contour (red)",
                     "red contour = mouth-content region M boundary", "checkerboard"),
        labeled_tile(outline_mask(sprites["beard"], P, MOUTH_CROP, 3, YELLOW),
                     "beard receiver + P contour (yellow)",
                     "yellow contour = patch footprint P boundary", "checkerboard"),
        labeled_tile(outline_mask(A, P, MOUTH_CROP, 3, YELLOW),
                     "state A + P contour (yellow)",
                     "patch seam sits inside skin/beard, away from the outer jaw",
                     "checkerboard"),
        labeled_tile(outline_mask(sprites["lower_face_neutral"], P, MOUTH_CROP,
                                  3, YELLOW),
                     "neutral patch + own footprint contour",
                     "common stable footprint for both patch states",
                     "checkerboard"),
    ]
    grid(tiles, 2,
         "Plate E — patch receiver / interface at 3x",
         "Static outer beard keeps the jaw identity; the swappable seam is the "
         "irregular P contour inside skin/beard tones."
         ).save(PLATES + "/E_receiver_interface_zoom.png")

    # layer order diagram
    W, H = 1240, 980
    sheet = make_bg((W, H), "light")
    d = ImageDraw.Draw(sheet)
    d.text((24, 16), "Plate E — render order (index 0 = bottom)",
           fill=(15, 13, 12), font=font(28, bold=True))
    cols = [
        ("puppet_core (A mouthless)", [
            "hair_back", "head_base", "ear_right", "ear_left", "beard",
            "nose", "eye_right", "eye_left", "eyebrow_right", "eyebrow_left",
            "moustache", "diadem_gold"]),
        ("puppet_core_neutral (B)", [
            "hair_back", "head_base", "ear_right", "ear_left", "beard",
            "lower_face_neutral", "nose", "eye_right", "eye_left",
            "eyebrow_right", "eyebrow_left", "moustache", "diadem_gold"]),
        ("puppet_core_open_test (C)", [
            "hair_back", "head_base", "ear_right", "ear_left", "beard",
            "lower_face_open_test", "nose", "eye_right", "eye_left",
            "eyebrow_right", "eyebrow_left", "moustache", "diadem_gold"]),
    ]
    for ci, (title, order) in enumerate(cols):
        x0 = 24 + ci * 400
        d.text((x0, 66), title, fill=(30, 28, 26), font=font(18, bold=True))
        n = len(order)
        bar_h, gap = 34, 6
        y = H - 40 - n * (bar_h + gap)
        for i, sid in enumerate(order):
            y0 = y + i * (bar_h + gap)
            patch = sid.startswith("lower_face_")
            fill = (255, 214, 90) if patch else (
                (150, 205, 160) if sid == "beard" else (225, 222, 215))
            d.rectangle([x0, y0, x0 + 360, y0 + bar_h], fill=fill,
                        outline=(60, 56, 52))
            d.text((x0 + 10, y0 + 7), "%d  %s" % (i, sid), fill=(20, 18, 16),
                   font=font(16))
        d.text((x0, H - 30),
               "beard < patch < moustache", fill=(60, 56, 52), font=font(15))
    d.text((24, 96), "Patch (yellow) sits above beard (green) and below the "
           "static moustache foreground in B and C; A carries no patch.",
           fill=(70, 66, 62), font=font(15))
    d.text((24, 118), "Mouth anchor (540,241). Tested front-view envelope: "
           "patch offsets (0,0),(±2,0),(0,±2); moustache (±1,0),(0,±1).",
           fill=(70, 66, 62), font=font(15))
    sheet.save(PLATES + "/E_layer_order.png")

    # stress contact sheet
    stress = json.load(open(V3 + "/stress-tests.json"))
    tiles = []
    for s in stress["samples"]:
        img = Image.open(V3 + "/" + s["path"]).convert("RGBA")
        o = s["offset_px"]
        tiles.append(labeled_tile(
            crop_scale(img, MOUTH_CROP, 2),
            "%s %+d,%+d" % (s["moved_sprite"], o["x"], o["y"]),
            "holes %d deficits %d confined %s" % (
                s["coverage"]["new_fully_transparent_interior"],
                s["coverage"]["alpha_below_250_where_source_opaque"],
                s["changes_confined_to_moved_footprint"]), "checkerboard"))
    grid(tiles, 6,
         "Plate E — micro-motion stress contact sheet (mouth crop at 2x)",
         "18 samples: each patch at (0,0),(±2,0),(0,±2) and moustache at "
         "(±1,0),(0,±1) over both patch states. Front-view envelope only."
         ).save(PLATES + "/E_stress_contact_sheet.png")

    print("plates written:", len(os.listdir(PLATES)))
    print("stage 40 complete")


if __name__ == "__main__":
    main()
