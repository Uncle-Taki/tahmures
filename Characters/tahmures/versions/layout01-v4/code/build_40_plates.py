#!/usr/bin/env python3
"""Layout01 v4 repair — stage 40: readable comparison/inspection plates D and E.

Plates are annotated renderings of the actual delivered components; the raw
compositions in previews/ stay unadorned. Backgrounds: checkerboard, light,
dark. Scales: 100% (source pixels) and enlarged nearest-neighbour crops.

v4 revision 1 additionally writes R1_01..R1_04 evidence plates that contrast
the defective v3 candidate (read-only) with the repaired v4 output for each
of Codex's four blockers.
"""
import json
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from build_lib import V4, V3, V2, CANVAS, load_master, erode

PLATES = V4 + "/previews/plates"
HEAD_CROP = (356, 0, 724, 432)
MOUTH_CROP = (455, 175, 625, 305)
EYE_CROP = (470, 100, 615, 200)
CRESCENT_CROP = (505, 205, 575, 255)     # R1-01 moustache-centre crescent zone
LIP_CROP = (505, 228, 575, 262)          # R1-03 lip parting line
NECK_CROP = (440, 300, 640, 400)         # R1-04 lower-neck join
GHOST_CROP = (495, 205, 585, 245)        # R1-02 moustache shift zone
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


def warm_mask(state_arr):
    """R1-01 warm-residue classifier (same as the stage-10 check)."""
    return ((state_arr[..., 0] >= 140) & (state_arr[..., 0] - state_arr[..., 2] >= 55)
            & (state_arr[..., 3] > 0))


def box_overlay(rgba, box_in, color=(255, 48, 32, 255), width=3):
    """Return an RGBA copy with a rectangle drawn at box_in (x0,y0,x1,y1)."""
    out = rgba.copy()
    d = ImageDraw.Draw(out)
    d.rectangle(list(box_in), outline=color, width=width)
    return out


def mask_highlight(rgba, mask, box, scale, color=(255, 48, 32, 255)):
    """Crop of rgba with mask pixels painted solid colour, nearest-scaled."""
    out = rgba.crop(box).resize(
        ((box[2] - box[0]) * scale, (box[3] - box[1]) * scale), NEAREST).copy()
    arr = np.asarray(out).copy()
    m = np.kron(mask[box[1]:box[3], box[0]:box[2]],
                np.ones((scale, scale), dtype=bool))
    arr[m] = color
    return Image.fromarray(arr, "RGBA")


def main():
    os.makedirs(PLATES, exist_ok=True)
    master = Image.open(V2 + "/source/approved_master.png").convert("RGBA")
    m = np.asarray(master)
    A = Image.open(V4 + "/previews/mouthless.png").convert("RGBA")
    B = Image.open(V4 + "/previews/neutral.png").convert("RGBA")
    C = Image.open(V4 + "/previews/open_test.png").convert("RGBA")
    A3 = Image.open(V3 + "/previews/mouthless.png").convert("RGBA")
    B3 = Image.open(V3 + "/previews/neutral.png").convert("RGBA")
    M = np.load(V4 + "/code/_M.npy")
    P = np.load(V4 + "/code/_P.npy")
    U = np.load(V4 + "/code/_U.npy")
    neck_clean = np.load(V4 + "/code/_neck_clean.npy")
    opening = np.load(V4 + "/code/_opening.npy")
    meta = json.load(open(V4 + "/code/_sprite_meta.json"))

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
         "content region M replaced by cloned beard receiver; moustache "
         "footprint underdraw; lower-neck garment cleanup" % nA),
        (ov_B, "B vs master — changed pixels", "%d px differ >3: neutral state "
             "is pixel-faithful except the repaired lower-neck join" % nB),
        (ov_C, "C vs master — changed pixels", "%d px differ >3 (red): "
             "neck repair + synthesized small opening" % nC),
    ]
    grid([labeled_tile(i, t, s, "dark") for i, t, s in ch], 2,
         "Plate D — reconstruction change map at 100%",
         "Red = RGB difference >3 vs approved master where both are opaque; "
         "base dimmed to 45%. Changes are intentionally confined to the "
         "mouth region and the lower-neck repair zone.").save(
        PLATES + "/D_changed_pixels_100.png")
    grid([labeled_tile(crop_scale(i, MOUTH_CROP, 3), t, s, "dark")
          for i, t, s in ch], 2,
         "Plate D — reconstruction change map, mouth crop at 3x",
         "A: mouth content region M (receiver). B: none. C: opening only."
         ).save(PLATES + "/D_changed_pixels_zoom.png")

    # ---------------- Plate E: layer inspection ----------------
    sprites = {sid: Image.open(V4 + "/" + rel).convert("RGBA")
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
        sub = ("receiver: M filled with cloned beard texture; "
               "moustache footprint U underdrawn (clone)" if sid == "beard" else
               "static foreground; decontaminated matte (353 px solved)" if sid == "moustache" else
               "master pixels + U underdraw fills" if sid == "lower_face_neutral" else
               "master pixels + U fills + 59 px synthesized opening"
               if sid == "lower_face_open_test" else
               "skin underdraw (M hole + U footprint + neck repair)")
        tiles.append(labeled_tile(crop_scale(sprites[sid], MOUTH_CROP, 3),
                                  sid, sub, "checkerboard"))
    grid(tiles, 3,
         "Plate E — lower-face components, mouth crop at 3x",
         "Receiver (beard), static moustache foreground, both patches, and "
         "the head_base underlay showing the receiver hole and U underdraw."
         ).save(PLATES + "/E_components_zoom.png")

    # exact export-alpha masks
    tiles = []
    for sid in SPRITE_ORDER:
        mask = Image.open(V4 + "/masks/%s.png" % sid)
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
        mask = Image.open(V4 + "/masks/%s.png" % sid)
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
            Image.open(V4 + "/provenance/%s__source.png" % sid).convert("L")) > 127
        rec = np.asarray(
            Image.open(V4 + "/provenance/%s__reconstructed.png" % sid).convert("L")) > 127
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
                     "beard provenance", "red = cloned beard receiver (M) + "
                     "moustache-footprint underdraw (U)",
                     "dark"),
        labeled_tile(crop_scale(prov_overlay("lower_face_open_test"),
                                MOUTH_CROP, 3),
                     "open patch provenance", "red = U fills + 59 px "
                     "synthesized opening",
                     "dark"),
        labeled_tile(crop_scale(prov_overlay("lower_face_neutral"),
                                MOUTH_CROP, 3),
                     "neutral patch provenance", "336 px reconstructed "
                     "(U underdraw fills)", "dark"),
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
        labeled_tile(outline_mask(A, U, MOUTH_CROP, 3, (90, 200, 255, 255)),
                     "state A + U contour (blue)",
                     "blue contour = moustache movement footprint underdraw "
                     "boundary (R1-02)", "checkerboard"),
        labeled_tile(outline_mask(sprites["lower_face_neutral"], P, MOUTH_CROP,
                                  3, YELLOW),
                     "neutral patch + own footprint contour",
                     "common stable footprint for both patch states",
                     "checkerboard"),
    ]
    grid(tiles, 2,
         "Plate E — patch receiver / interface at 3x",
         "Static outer beard keeps the jaw identity; the swappable seam is the "
         "irregular P contour inside skin/beard tones; U marks the moustache "
         "underdraw that guarantees clean ±1 px shifts."
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
    stress = json.load(open(V4 + "/stress-tests.json"))
    tiles = []
    for s in stress["samples"]:
        img = Image.open(V4 + "/" + s["path"]).convert("RGBA")
        o = s["offset_px"]
        extra = ""
        if "vacated_strip_mismatched_px" in s:
            extra = ", vacated exact %s" % s[
                "vacated_strip_matches_underlay_exactly"]
        tiles.append(labeled_tile(
            crop_scale(img, MOUTH_CROP, 2),
            "%s %+d,%+d" % (s["moved_sprite"], o["x"], o["y"]),
            "holes %d deficits %d confined %s%s" % (
                s["coverage"]["new_fully_transparent_interior"],
                s["coverage"]["alpha_below_250_where_source_opaque"],
                s["changes_confined_to_moved_footprint"], extra),
            "checkerboard"))
    grid(tiles, 6,
         "Plate E — micro-motion stress contact sheet (mouth crop at 2x)",
         "18 samples: each patch at (0,0),(±2,0),(0,±2) and moustache at "
         "(±1,0),(0,±1) over both patch states. Front-view envelope only."
         ).save(PLATES + "/E_stress_contact_sheet.png")

    # ================= R1 evidence plates =================
    # ---- R1-01: mouthless warm crescent below moustache centre ----
    warm3 = warm_mask(np.asarray(A3))
    warm4 = warm_mask(np.asarray(A))
    cres = np.zeros((CANVAS[1], CANVAS[0]), dtype=bool)
    cres[230:237, 530:542] = True
    tiles = [
        labeled_tile(crop_scale(box_overlay(A3, (530, 230, 542, 237)),
                                CRESCENT_CROP, 8),
                     "v3 state A (defective)", "red box = crescent bbox "
                     "[530,230,542,237)", "checkerboard"),
        labeled_tile(crop_scale(box_overlay(A, (530, 230, 542, 237)),
                                CRESCENT_CROP, 8),
                     "v4 state A (repaired)", "same box; crescent removed",
                     "checkerboard"),
        labeled_tile(mask_highlight(A3, warm3 & cres, CRESCENT_CROP, 8),
                     "v3 warm residue (red)", "warm px = r>=140, r-b>=55; "
                     "box [530,230,542,237)", "checkerboard"),
        labeled_tile(mask_highlight(A, warm4 & cres, CRESCENT_CROP, 8),
                     "v4 warm residue (red)", "0 warm px in the crescent bbox",
                     "checkerboard"),
        labeled_tile(crop_scale(sprites_v3("face/moustache.png"),
                                CRESCENT_CROP, 8),
                     "v3 moustache component", "binary matte carried warm "
                     "blend RGB over dark clone", "checkerboard"),
        labeled_tile(crop_scale(sprites["moustache"], CRESCENT_CROP, 8),
                     "v4 moustache component", "matte decontaminated by the "
                     "underlay solve", "checkerboard"),
    ]
    grid(tiles, 3,
         "R1-01 — mouthless remnant below the moustache centre (8x)",
         "Before (v3, read-only) vs after (v4): the warm/ink crescent is "
         "gone from state A; the moustache keeps its recognizable outer form."
         ).save(PLATES + "/R1_01_mouthless_crescent.png")

    # ---- R1-02: baked moustache outlines beneath the movable feature ----
    st3 = Image.open(V3 + "/previews/stress/moustache-over-neutral-dx0-dy1.png"
                     ).convert("RGBA")
    st4 = Image.open(V4 + "/previews/stress/moustache-over-neutral-dx0-dy1.png"
                     ).convert("RGBA")
    u_img = Image.fromarray(
        np.load(V4 + "/code/_u_neutral.npy").astype(np.uint8), "RGBA")
    head4 = sprites["head_base"]
    head3 = Image.open(V3 + "/head/head_base.png").convert("RGBA")
    tiles = [
        labeled_tile(crop_scale(st3, GHOST_CROP, 8),
                     "v3 moustache dy+1 (defective)",
                     "doubled dark edge under the shifted moustache",
                     "checkerboard"),
        labeled_tile(crop_scale(st4, GHOST_CROP, 8),
                     "v4 moustache dy+1 (repaired)",
                     "vacated strip equals the underlay byte-exactly",
                     "checkerboard"),
        labeled_tile(crop_scale(head3, GHOST_CROP, 8),
                     "v3 head_base under moustache",
                     "baked outline of the old feature (1233 dark px)",
                     "checkerboard"),
        labeled_tile(crop_scale(head4, GHOST_CROP, 8),
                     "v4 head_base under moustache",
                     "baked outline removed; skin underdraw in U",
                     "checkerboard"),
        labeled_tile(crop_scale(u_img, GHOST_CROP, 8),
                     "QA underlay (no moustache)",
                     "inspection render only — NOT a facial state",
                     "checkerboard"),
        labeled_tile(outline_mask(A, U, GHOST_CROP, 8, (90, 200, 255, 255)),
                     "state A + U contour (blue)",
                     "U = moustache footprint underdraw region", "checkerboard"),
    ]
    grid(tiles, 3,
         "R1-02 — baked moustache outline beneath the movable feature (8x)",
         "Before (v3) vs after (v4): head_base and beard no longer carry the "
         "old moustache outline; shifted-moustache samples show no doubled "
         "edge, halo, or exposed lip residue."
         ).save(PLATES + "/R1_02_moustache_ghost.png")

    # ---- R1-03: coherent small mouth opening ----
    bc = np.asarray(B) != np.asarray(C)
    bc_mask = bc.any(axis=2) & (np.asarray(C)[..., 3] > 0)
    tiles = [
        labeled_tile(crop_scale(master, LIP_CROP, 8),
                     "approved master", "lip parting line at y240 (reference)",
                     "checkerboard"),
        labeled_tile(crop_scale(B, LIP_CROP, 8),
                     "B neutral", "original mouth/skin/beard relationship",
                     "checkerboard"),
        labeled_tile(crop_scale(C, LIP_CROP, 8),
                     "C open test", "one restrained opening on the actual lip "
                     "line; second mark removed", "checkerboard"),
        labeled_tile(mask_highlight(B, bc_mask, LIP_CROP, 8,
                                    (255, 210, 40, 255)),
                     "B vs C differing px (yellow)",
                     "exactly %d px differ, all inside the patch footprint"
                     % int(bc_mask.sum()), "checkerboard"),
        labeled_tile(mask_highlight(C, opening, LIP_CROP, 8),
                     "opening mask (red)", "59 px lens on the lip parting "
                     "line y239-241", "checkerboard"),
        labeled_tile(crop_scale(A, LIP_CROP, 8),
                     "A mouthless (context)", "receiver beard; no mouth marks",
                     "checkerboard"),
    ]
    grid(tiles, 3,
         "R1-03 — neutral vs small-open test at the lip line (8x)",
         "C parts the actual lips with one coherent opening; B and C differ "
         "only inside the patch; no duplicated mouth mark in the beard notch."
         ).save(PLATES + "/R1_03_opening.png")

    # ---- R1-04: lower-neck garment contamination ----
    head_only_v3 = Image.open(V3 + "/head/head_base.png").convert("RGBA")
    head_only = sprites["head_base"]
    garment_v3 = np.zeros((CANVAS[1], CANVAS[0]), dtype=bool)
    g = np.asarray(head_only_v3).astype(int)
    garment_v3 = (((g[..., 0] >= 150) & (g[..., 0] - g[..., 2] >= 140))
                  | ((g[..., 0] >= 120) & (g[..., 0] - g[..., 2] >= 90))) \
        & (g[..., 2] <= 70) & (g[..., 3] > 0)
    garment_v3 &= neck_zone(garment_v3)
    tiles = [
        labeled_tile(crop_scale(B3, NECK_CROP, 6),
                     "v3 state B neck (defective)",
                     "gold garment shards and jagged join", "checkerboard"),
        labeled_tile(crop_scale(B, NECK_CROP, 6),
                     "v4 state B neck (repaired)",
                     "garment contamination removed; smooth local neck/hair "
                     "attachment", "checkerboard"),
        labeled_tile(mask_highlight(head_only_v3, garment_v3, NECK_CROP, 6),
                     "v3 head_base garment px (red)",
                     "classifier: warm gold over neck zone", "checkerboard"),
        labeled_tile(crop_scale(head_only, NECK_CROP, 6),
                     "v4 head_base (isolated)",
                     "0 garment px; strand-continuation underdraw", "checkerboard"),
        labeled_tile(outline_mask(head_only, neck_clean, NECK_CROP, 6,
                                  (90, 200, 255, 255)),
                     "v4 neck cleanup zone (blue contour)",
                     "277 px cleaned + reconstructed as neck/hair", "checkerboard"),
        labeled_tile(crop_scale(prov_overlay("head_base"), NECK_CROP, 6),
                     "v4 head_base provenance",
                     "red = reconstructed (underdraw + neck repair)",
                     "checkerboard"),
    ]
    grid(tiles, 3,
         "R1-04 — lower-neck garment cleanup (6x)",
         "Before (v3) vs after (v4): clothing-colour fragments removed from "
         "the head layer; hidden neck/hair underdraw completed without a "
         "torso extraction."
         ).save(PLATES + "/R1_04_neck.png")

    # isolated head neck on three backgrounds (R1-04 requirement)
    for bg in ("checkerboard", "light", "dark"):
        tiles = [
            labeled_tile(crop_scale(head_only, NECK_CROP, 1),
                         "v4 head_base neck at 100%%", None, bg),
            labeled_tile(crop_scale(head_only, NECK_CROP, 4),
                         "v4 head_base neck at 4x", None, bg),
            labeled_tile(crop_scale(B, NECK_CROP, 1),
                         "v4 state B neck at 100%%", None, bg),
            labeled_tile(crop_scale(B, NECK_CROP, 4),
                         "v4 state B neck at 4x", None, bg),
        ]
        grid(tiles, 4,
             "R1-04 — isolated head / lower-neck components (%s background)"
             % bg,
             "No gold/garment shards, jagged neck join, or new transparent "
             "gap; identical head used by A/B/C."
             ).save(PLATES + "/R1_04_neck_bg_%s.png" % bg)

    print("plates written:", len(os.listdir(PLATES)))
    print("stage 40 complete")


def sprites_v3(rel):
    return Image.open(V3 + "/" + rel).convert("RGBA")


def neck_zone(mask):
    """Restrict a mask to the lower-neck band used by the R1-04 classifier."""
    z = np.zeros_like(mask)
    z[300:400, 440:660] = True
    return z


if __name__ == "__main__":
    main()
