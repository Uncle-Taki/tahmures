"""Candidate S04 blocking. Run with Blender; no network or third-party assets.

The identical source is submitted to Blendstra and executed locally.
Object transform animation, not a production armature or lip-sync rig.
"""

import bpy
import math
from mathutils import Vector

FPS = 12
FRAMES = 120


def material(name, color, metallic=0.0, roughness=0.65):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bs = m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value = (*color, 1)
    bs.inputs["Metallic"].default_value = metallic
    bs.inputs["Roughness"].default_value = roughness
    return m


def finish(obj, name, mat=None, parent=None, smooth=True):
    obj.name = name
    obj["blendstra_id"] = name
    if mat:
        obj.data.materials.append(mat)
    if parent:
        obj.parent = parent
    if smooth and obj.type == "MESH":
        for face in obj.data.polygons:
            face.use_smooth = True
    return obj


def empty(name, location=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(o)
    o.location = location
    o["blendstra_id"] = name
    if parent:
        o.parent = parent
    return o


def box(name, loc, size, mat, parent=None, bevel=0.025):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = finish(bpy.context.object, name, mat, parent, False)
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = o.modifiers.new("Soft crafted edges", "BEVEL")
        mod.width = bevel
        mod.segments = 3
        o.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    return o


def ellipsoid(name, loc, scale, mat, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, location=loc)
    o = finish(bpy.context.object, name, mat, parent)
    o.scale = scale
    return o


def mesh(name, verts, faces, mat, parent=None, smooth=True):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts, [], faces)
    data.update()
    o = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(o)
    return finish(o, name, mat, parent, smooth)


def rings(name, sections, mat, parent=None, count=24, start=0.0, end=2 * math.pi):
    # Deliberately shaped elliptical sections; used for garments and head contours.
    closed = abs(end - start - 2 * math.pi) < 1e-6
    n = count if closed else count + 1
    vs = []
    for z, rx, ry, cx, cy in sections:
        for j in range(n):
            a = start + (end - start) * j / count
            vs.append((cx + rx * math.cos(a), cy + ry * math.sin(a), z))
    fs = []
    for i in range(len(sections) - 1):
        for j in range(count if closed else count):
            k = (j + 1) % n
            fs.append((i * n + j, i * n + k, (i + 1) * n + k, (i + 1) * n + j))
    if closed:
        fs += [
            tuple(reversed(range(n))),
            tuple((len(sections) - 1) * n + j for j in range(n)),
        ]
    o = mesh(name, vs, fs, mat, parent)
    if not closed:
        sol = o.modifiers.new("Cloth thickness", "SOLIDIFY")
        sol.thickness = 0.012
    return o


def tube(name, points, radii, mat, parent=None, sides=10):
    vs = []
    pts = [Vector(p) for p in points]
    for i, p in enumerate(pts):
        direction = (pts[min(i + 1, len(pts) - 1)] - pts[max(0, i - 1)]).normalized()
        axis = Vector((0, 1, 0)) if abs(direction.y) < 0.85 else Vector((1, 0, 0))
        u = direction.cross(axis).normalized()
        v = direction.cross(u).normalized()
        for j in range(sides):
            a = 2 * math.pi * j / sides
            vs.append(tuple(p + radii[i] * (u * math.cos(a) + v * math.sin(a))))
    fs = []
    for i in range(len(pts) - 1):
        for j in range(sides):
            k = (j + 1) % sides
            fs.append(
                (i * sides + j, i * sides + k, (i + 1) * sides + k, (i + 1) * sides + j)
            )
    fs += [
        tuple(reversed(range(sides))),
        tuple((len(pts) - 1) * sides + j for j in range(sides)),
    ]
    return mesh(name, vs, fs, mat, parent)


def cylinder(name, loc, radius, depth, mat, vertices=48):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, radius=radius, depth=depth, location=loc
    )
    o = finish(bpy.context.object, name, mat)
    mod = o.modifiers.new("Edge bevel", "BEVEL")
    mod.width = 0.016
    mod.segments = 2
    o.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return o


def key(obj, prop, frames_values):
    for frame, value in frames_values:
        setattr(obj, prop, value)
        obj.keyframe_insert(data_path=prop, frame=frame)
    if obj.animation_data and obj.animation_data.action:
        obj.animation_data.action.name = obj.name + " | S04"
        # Compatibility with both Blender 4.3 local and hosted 4.5 actions.
        try:
            for fc in obj.animation_data.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = "BEZIER"
                    kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
        except AttributeError:
            pass


def character(name, location, yaw, skin, coat, hair, variant):
    root = empty(name + ".root", location)
    root.rotation_euler.z = math.radians(yaw)
    root["role"] = {
        "akvan": "examines records",
        "black_div": "literal reading then empty-handed departure",
        "div_e_sefid": "onward messenger; reaches, no custody transfer",
    }[name]
    upper = empty(name + ".torso_pivot", (0, 0, 1.02), root)
    ivory, gold, brown = M["linen"], M["gold"], M["leather"]
    # Boots and separately shaped trouser legs remain grounded in the held stance.
    for sign in (-1, 1):
        x = sign * 0.18
        shoe = ellipsoid(
            name + ".shoe." + str(sign),
            (x, -0.085, 0.075),
            (0.13, 0.235, 0.075),
            M["boots"],
            root,
        )
        shoe["support_z"] = 0.0
        rings(
            name + ".trousers." + str(sign),
            [
                (0.13, 0.075, 0.075, x, 0),
                (0.25, 0.11, 0.105, x, 0),
                (0.55, 0.14, 0.12, x, 0),
                (0.94, 0.145, 0.135, x, 0),
            ],
            brown if variant != "white" else ivory,
            root,
        )
    rings(
        name + ".tunic",
        [
            (-0.38, 0.34, 0.20, 0, 0),
            (-0.08, 0.30, 0.18, 0, 0),
            (0.22, 0.32, 0.195, 0, 0),
            (0.51, 0.43, 0.20, 0, 0),
            (0.58, 0.27, 0.16, 0, 0),
        ],
        ivory if variant != "black" else M["ochre"],
        upper,
    )
    if variant == "black":
        mesh(
            name + ".vest_v_neck",
            [(-0.16, -0.208, 0.54), (0.16, -0.208, 0.54), (0, -0.212, 0.22)],
            [(0, 1, 2)],
            M["dark_cloth"],
            upper,
            False,
        )
        for i in range(3):
            box(
                name + ".vest_clasp." + str(i),
                (0.04, -0.215, 0.20 - i * 0.09),
                (0.12, 0.035, 0.025),
                brown,
                upper,
                0.01,
            )
    # Open front coat: real curved shell, visible lining and paired hems.
    hem = -0.83 if variant != "black" else -0.10
    rings(
        name + ".coat",
        [
            (hem, 0.40, 0.225, 0, 0),
            (-0.05, 0.32, 0.205, 0, 0),
            (0.30, 0.38, 0.215, 0, 0),
            (0.53, 0.445, 0.21, 0, 0),
        ],
        coat,
        upper,
        start=-0.83,
        end=3.97,
    )
    for s in (-1, 1):
        tube(
            name + ".coat_trim." + str(s),
            [
                (s * 0.28, -0.17, hem),
                (s * 0.215, -0.18, -0.04),
                (s * 0.24, -0.18, 0.30),
                (s * 0.28, -0.17, 0.51),
            ],
            [0.012] * 4,
            gold if variant == "black" else ivory,
            upper,
            6,
        )
    rings(
        name + ".sash",
        [(-0.11, 0.325, 0.212, 0, 0), (0.035, 0.325, 0.212, 0, 0)],
        brown if variant != "white" else M["dark_cloth"],
        upper,
    )
    box(
        name + ".sash_end",
        (0.11, -0.23, -0.24),
        (0.09, 0.022, 0.37),
        brown if variant != "white" else M["dark_cloth"],
        upper,
        0.012,
    )
    # Articulated shoulders and elbows; hands have palms, thumbs and fingers.
    arms = []
    for s in (-1, 1):
        shoulder = empty(name + ".shoulder." + str(s), (s * 0.38, 0, 0.46), upper)
        tube(
            name + ".upper_sleeve." + str(s),
            [(0, 0, 0), (s * 0.09, -0.035, -0.20), (s * 0.13, -0.07, -0.36)],
            [0.135, 0.13, 0.10],
            coat
            if variant == "white"
            else ivory
            if variant == "akvan"
            else M["dark_cloth"],
            shoulder,
        )
        elbow = empty(name + ".elbow." + str(s), (s * 0.13, -0.07, -0.36), shoulder)
        tube(
            name + ".fore_sleeve." + str(s),
            [(0, 0, 0), (s * 0.015, -0.09, -0.18), (s * 0.02, -0.15, -0.29)],
            [0.105, 0.10, 0.08],
            ivory if variant != "black" else M["dark_cloth"],
            elbow,
        )
        tube(
            name + ".cuff." + str(s),
            [(s * 0.018, -0.135, -0.26), (s * 0.02, -0.16, -0.30)],
            [0.09, 0.09],
            coat,
            elbow,
        )
        hand = empty(name + ".hand." + str(s), (s * 0.02, -0.17, -0.34), elbow)
        ellipsoid(
            name + ".palm." + str(s),
            (0, -0.02, -0.025),
            (0.067, 0.045, 0.09),
            skin,
            hand,
        )
        for j in range(4):
            fx = -0.043 + j * 0.027
            tube(
                name + ".finger." + str(s) + "." + str(j),
                [(fx, -0.022, -0.07), (fx, -0.042, -0.12), (fx, -0.06, -0.13)],
                [0.014, 0.012, 0.008],
                skin,
                hand,
                6,
            )
        tube(
            name + ".thumb." + str(s),
            [(s * 0.05, -0.02, 0), (s * 0.09, -0.06, -0.04), (s * 0.07, -0.07, -0.075)],
            [0.022, 0.018, 0.011],
            skin,
            hand,
            8,
        )
        arms.append((shoulder, elbow, hand))
    # Neck, shaped jaw/cheeks, projecting nose, separate eyes, brows and ears.
    rings(
        name + ".neck",
        [(0.54, 0.115, 0.105, 0, 0), (0.72, 0.105, 0.10, 0, 0)],
        skin,
        upper,
    )
    head = empty(name + ".head", (0, 0, 0.83), upper)
    rings(
        name + ".face",
        [
            (-0.18, 0.055, 0.07, 0, -0.01),
            (-0.13, 0.14, 0.11, 0, -0.02),
            (-0.02, 0.20, 0.16, 0, 0),
            (0.13, 0.22, 0.18, 0, 0),
            (0.28, 0.20, 0.17, 0, 0.01),
            (0.36, 0.13, 0.12, 0, 0.015),
            (0.38, 0.025, 0.035, 0, 0.01),
        ],
        skin,
        head,
    )
    for s in (-1, 1):
        earverts = [
            (s * 0.18, -0.015, 0.08),
            (s * 0.36, 0.0, 0.22),
            (s * 0.285, -0.04, 0.015),
            (s * 0.20, -0.065, -0.035),
            (s * 0.24, 0.025, 0.08),
        ]
        mesh(
            name + ".ear." + str(s),
            earverts,
            [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4), (3, 2, 1, 0)],
            skin,
            head,
        )
        ellipsoid(
            name + ".eye_white." + str(s),
            (s * 0.087, -0.158, 0.13),
            (0.064, 0.034, 0.077),
            M["eye_white"],
            head,
        )
        ellipsoid(
            name + ".pupil." + str(s),
            (s * 0.078, -0.188, 0.128),
            (0.026, 0.012, 0.034),
            M["ink"],
            head,
        )
        ellipsoid(
            name + ".eye_glint." + str(s),
            (s * 0.078 - 0.008, -0.200, 0.144),
            (0.008, 0.004, 0.010),
            M["eye_white"],
            head,
        )
        tube(
            name + ".brow." + str(s),
            [
                (s * 0.035, -0.171, 0.235),
                (s * 0.087, -0.185, 0.25),
                (s * 0.15, -0.162, 0.23),
            ],
            [0.013, 0.020, 0.012],
            hair,
            head,
            8,
        )
        hornpts = [
            (s * 0.18, 0.015, 0.28),
            (s * 0.255, 0.025, 0.33),
            (s * 0.31, 0.03, 0.40),
            (s * 0.30, 0.045, 0.47),
        ]
        if variant == "white":
            hornpts = [
                (s * 0.19, 0.03, 0.29),
                (s * 0.28, 0.04, 0.36),
                (s * 0.35, 0.02, 0.32),
                (s * 0.365, 0.0, 0.25),
            ]
        tube(
            name + ".horn." + str(s),
            hornpts,
            [0.065, 0.057, 0.035, 0.003],
            M["horn_dark"] if variant == "black" else M["horn"],
            head,
            12,
        )
    ellipsoid(name + ".nose", (0, -0.185, 0.055), (0.043, 0.064, 0.063), skin, head)
    tube(
        name + ".mouth",
        [(-0.065, -0.151, -0.052), (0, -0.173, -0.064), (0.065, -0.151, -0.052)],
        [0.006, 0.008, 0.006],
        M["mouth"],
        head,
        8,
    )
    # Cap of hair on the back, individually swept face-framing locks.
    if variant != "white":
        ellipsoid(name + ".hair_back", (0, 0.09, 0.18), (0.225, 0.15, 0.24), hair, head)
        for s in (-1, 1):
            tube(
                name + ".side_lock." + str(s),
                [
                    (s * 0.12, 0, 0.34),
                    (s * 0.205, -0.035, 0.24),
                    (s * 0.225, 0.015, 0.02),
                    (s * 0.22, 0.04, -0.17 if variant == "akvan" else -0.03),
                ],
                [0.10, 0.075, 0.06, 0.035],
                hair,
                head,
                12,
            )
        tube(
            name + ".forelock",
            [
                (-0.13, -0.03, 0.32),
                (-0.08, -0.12, 0.38),
                (0.04, -0.12, 0.37),
                (0.16, -0.07, 0.29),
            ],
            [0.075, 0.08, 0.075, 0.02],
            hair,
            head,
            12,
        )
    else:
        for s in (-1, 1):
            tube(
                name + ".silver_side_hair." + str(s),
                [
                    (s * 0.19, 0.06, 0.28),
                    (s * 0.23, 0.08, 0.11),
                    (s * 0.22, 0.06, -0.13),
                    (s * 0.17, 0.04, -0.18),
                ],
                [0.075, 0.09, 0.08, 0.02],
                hair,
                head,
                12,
            )
            tube(
                name + ".moustache." + str(s),
                [
                    (0, -0.208, -0.01),
                    (s * 0.065, -0.19, -0.018),
                    (s * 0.11, -0.16, 0.005),
                ],
                [0.018, 0.022, 0.007],
                hair,
                head,
                10,
            )
    if variant in ("black", "white"):
        tube(
            name + ".goatee",
            [(0, -0.13, -0.10), (0, -0.11, -0.21), (0, -0.075, -0.25)],
            [0.065, 0.04, 0.005],
            hair,
            head,
            12,
        )
    return {"root": root, "upper": upper, "head": head, "arms": arms}


def light(name, loc, color, power, size, target):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = power
    data.color = color
    data.shape = "DISK"
    data.size = size
    o = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (Vector(target) - o.location).to_track_quat("-Z", "Y").to_euler()


def build():
    global M
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    M = {
        "sand": material("warm limestone", (0.36, 0.25, 0.16)),
        "floor": material("sandstone floor", (0.28, 0.18, 0.115)),
        "dark_wall": material("night passage", (0.018, 0.037, 0.063)),
        "cedar": material("cedar", (0.18, 0.075, 0.028)),
        "gold": material("muted brass", (0.62, 0.36, 0.095), 0.6, 0.36),
        "linen": material("warm linen", (0.80, 0.68, 0.47)),
        "leather": material("brown sash", (0.24, 0.12, 0.052)),
        "boots": material("dark leather boots", (0.043, 0.027, 0.017)),
        "dark_cloth": material("charcoal cloth", (0.065, 0.052, 0.045)),
        "akvan_skin": material("Akvan turquoise", (0.18, 0.53, 0.48)),
        "akvan_coat": material("Akvan forest green", (0.035, 0.145, 0.105)),
        "black_skin": material("Black Div warm charcoal", (0.20, 0.175, 0.15)),
        "ochre": material("Black Div ochre vest", (0.61, 0.31, 0.07)),
        "white_skin": material("White Div warm ivory", (0.73, 0.59, 0.39)),
        "white_coat": material("White Div blue grey", (0.18, 0.29, 0.36)),
        "hair": material("dark brown hair", (0.034, 0.021, 0.013)),
        "silver": material("silver hair", (0.57, 0.60, 0.59)),
        "horn": material("ivory horns", (0.68, 0.54, 0.32)),
        "horn_dark": material("brown horns", (0.24, 0.12, 0.055)),
        "ink": material("dark eyes and ink", (0.007, 0.008, 0.009)),
        "eye_white": material("warm eye whites", (0.92, 0.90, 0.83)),
        "mouth": material("mouth detail", (0.075, 0.045, 0.028)),
        "clay": material("river clay tablet", (0.50, 0.25, 0.12)),
        "cloth": material("tablet travelling cloth", (0.28, 0.34, 0.31)),
        "rug": material("muted woven rug", (0.22, 0.065, 0.035)),
    }
    # A declared open-front film set; no final room/runtime completeness claim.
    box("set.floor", (0, 0, -0.13), (9, 7, 0.26), M["floor"], bevel=0.03)
    back = box("set.back_wall", (0, 3.0, 1.8), (9, 0.35, 3.6), M["sand"], bevel=0)
    # An actual arch-shaped Boolean aperture with visible passage depth.
    outline = [(-0.65, 0), (0.65, 0), (0.65, 1.9)]
    outline += [
        (0.65 * math.cos(math.pi * i / 16), 1.9 + 0.65 * math.sin(math.pi * i / 16))
        for i in range(1, 17)
    ]
    vs = [(2.6 + x, y, z) for y in (2.6, 3.4) for x, z in outline]
    n = len(outline)
    fs = [tuple(reversed(range(n))), tuple(range(n, 2 * n))] + [
        (i, (i + 1) % n, (i + 1) % n + n, i + n) for i in range(n)
    ]
    cutter = mesh("set.door_cutter", vs, fs, None, smooth=False)
    bpy.context.view_layer.objects.active = back
    bo = back.modifiers.new("OPENING-D01 real passage", "BOOLEAN")
    bo.operation = "DIFFERENCE"
    bo.solver = "EXACT"
    bo.object = cutter
    bpy.ops.object.modifier_apply(modifier=bo.name)
    bpy.data.objects.remove(cutter, do_unlink=True)
    box("set.passage_floor", (2.6, 4, -0.04), (1.4, 2.0, 0.08), M["floor"])
    box("set.passage_backing", (2.6, 5.0, 1.5), (1.5, 0.12, 3.0), M["dark_wall"])
    for x in (-3.6, -2.2, 0.2, 1.3, 3.8):
        box("set.pilaster." + str(x), (x, 2.74, 1.58), (0.20, 0.22, 3.16), M["sand"])
        box("set.capital." + str(x), (x, 2.68, 3.10), (0.36, 0.34, 0.16), M["gold"])
    box("set.frieze", (0, 2.72, 3.32), (8.8, 0.18, 0.18), M["gold"])
    rug = box("set.rug", (0, 0, 0.009), (5.5, 4.2, 0.018), M["rug"], bevel=0)
    for x in (-2.55, 2.55):
        box(
            "set.rug_border." + str(x),
            (x, 0, 0.022),
            (0.035, 3.9, 0.009),
            M["gold"],
            bevel=0,
        )
    table = cylinder(
        "props.round_cedar_table", (0, -0.12, 0.995), 1.08, 0.13, M["cedar"]
    )
    for x, y in [(-0.65, -0.65), (0.65, -0.65), (-0.65, 0.45), (0.65, 0.45)]:
        box(
            "props.table_leg." + str(x) + "." + str(y),
            (x, y, 0.465),
            (0.11, 0.11, 0.93),
            M["cedar"],
        )
    cylinder("props.table_inlay", (0, -0.12, 1.063), 1.01, 0.006, M["gold"])
    cylinder("props.table_inner", (0, -0.12, 1.068), 0.99, 0.006, M["cedar"])
    box(
        "props.travel_cloth",
        (0, -0.10, 1.079),
        (0.61, 0.44, 0.016),
        M["cloth"],
        bevel=0.012,
    )
    tablet = box(
        "props.found_tablet",
        (0, -0.10, 1.122),
        (0.43, 0.30, 0.07),
        M["clay"],
        bevel=0.025,
    )
    tablet["custody"] = "On supported travelling cloth; no hand custody in this excerpt"
    tablet["inscription"] = "Before sunrise, count the watchfires beyond the water."
    tablet["rendered_marks"] = (
        "Decorative invented strokes; not an authentic script or readable quotation"
    )
    # Surface strokes deliberately remain decorative; the text is in external captions.
    for row in range(4):
        for col in range(5):
            x = -0.155 + col * 0.069
            y = -0.205 + row * 0.065
            mesh(
                "props.tablet_mark." + str(row) + "." + str(col),
                [
                    (x, y, 1.158),
                    (x + 0.031, y + 0.008, 1.158),
                    (x + 0.006, y + 0.019, 1.158),
                ],
                [(0, 1, 2)],
                M["mouth"],
                smooth=False,
            )
    box(
        "props.archive_record",
        (-0.61, -0.08, 1.08),
        (0.35, 0.42, 0.013),
        M["linen"],
        bevel=0.01,
    )
    for i in range(6):
        box(
            "props.record_line." + str(i),
            (-0.61, -0.21 + i * 0.053, 1.089),
            (0.24, 0.005, 0.002),
            M["leather"],
            bevel=0,
        )
    # Akvan has the source's green coat/turquoise skin; Black ochre; White blue-grey.
    a = character(
        "akvan",
        (-1.51, 0.48, 0),
        38,
        M["akvan_skin"],
        M["akvan_coat"],
        M["hair"],
        "akvan",
    )
    b = character(
        "black_div", (0, 1.59, 0), 0, M["black_skin"], M["ochre"], M["hair"], "black"
    )
    w = character(
        "div_e_sefid",
        (1.53, 0.50, 0),
        -38,
        M["white_skin"],
        M["white_coat"],
        M["silver"],
        "white",
    )
    r = math.radians
    key(
        a["head"],
        "rotation_euler",
        [
            (1, (r(7), 0, r(-6))),
            (26, (r(16), 0, r(7))),
            (52, (r(8), 0, r(-8))),
            (82, (r(13), 0, r(5))),
            (120, (r(8), 0, r(-2))),
        ],
    )
    key(
        a["arms"][1][0],
        "rotation_euler",
        [
            (1, (r(-18), 0, r(-8))),
            (24, (r(-40), r(-8), r(-8))),
            (55, (r(-31), 0, r(-6))),
            (120, (r(-27), 0, r(-6))),
        ],
    )
    key(
        b["upper"],
        "rotation_euler",
        [
            (1, (0, 0, 0)),
            (25, (r(14), 0, 0)),
            (46, (r(14), 0, 0)),
            (63, (0, 0, 0)),
            (82, (0, 0, r(-42))),
            (120, (0, 0, r(-42))),
        ],
    )
    key(
        b["head"],
        "rotation_euler",
        [
            (1, (r(2), 0, 0)),
            (25, (r(10), 0, 0)),
            (47, (r(8), 0, 0)),
            (72, (0, 0, r(-20))),
            (120, (0, 0, r(-20))),
        ],
    )
    # Turn-in-place anticipates a departure; no sliding walk cycle or off-screen travel.
    key(
        b["arms"][0][1],
        "rotation_euler",
        [(1, (0, 0, 0)), (44, (r(-10), 0, 0)), (68, (0, 0, 0)), (120, (0, 0, 0))],
    )
    key(
        w["head"],
        "rotation_euler",
        [
            (1, (r(5), 0, r(4))),
            (48, (r(4), 0, r(-8))),
            (74, (r(12), 0, r(2))),
            (120, (r(10), 0, 0)),
        ],
    )
    key(
        w["arms"][0][0],
        "rotation_euler",
        [
            (1, (r(-7), 0, r(5))),
            (65, (r(-7), 0, r(5))),
            (100, (r(-48), r(8), r(12))),
            (120, (r(-48), r(8), r(12))),
        ],
    )
    key(
        w["arms"][0][1],
        "rotation_euler",
        [(1, (0, 0, 0)), (65, (0, 0, 0)), (100, (r(-12), 0, 0)), (120, (r(-12), 0, 0))],
    )
    # No mouth animation or performance-synced sound is implied.
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = FRAMES
    scene.render.fps = FPS
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene["candidate_status"] = (
        "try2 S04 previsualisation; owner likeness/motion approval pending"
    )
    scene["set_exception"] = (
        "Open-front animation stage; no final enclosed-room Form/Runtime approval"
    )
    scene["source_scene"] = (
        "S04, playscript/chapter-01-final-2026-10-30/chapter_one_final_en.md"
    )
    for f, name in [
        (1, "Akvan examines record"),
        (25, "Black Div reads"),
        (63, "Black Div turns empty-handed"),
        (100, "White Div reaches; tablet stays"),
    ]:
        scene.timeline_markers.new(name, frame=f)
    bpy.ops.object.camera_add(location=(4.3, -7.4, 4.15))
    cam = bpy.context.object
    cam.name = "camera.production"
    cam.rotation_euler = (
        (Vector((0, 0.55, 1.2)) - cam.location).to_track_quat("-Z", "Y").to_euler()
    )
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 6.65
    scene.camera = cam
    light("light.warm_key", (-3, -4, 6), (1.0, 0.77, 0.49), 950, 4.0, (0, 0, 1))
    light("light.cool_fill", (4, -1, 4), (0.56, 0.72, 1.0), 650, 3.0, (0, 0.5, 1))
    light("light.rim", (-1, 3.0, 4), (1.0, 0.58, 0.25), 1000, 3.0, (0, 0.5, 1.5))
    if scene.world is None:
        scene.world = bpy.data.worlds.new("Tahmures night world")
    scene.world.color = (0.045, 0.045, 0.045)
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 12
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 768
    scene.render.resolution_y = 432
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "AgX"
    scene.frame_set(1)
    # Store the brief inside the recoverable native Blender scene.
    t = bpy.data.texts.new("TRY2_CONTEXT.md")
    t.write(
        "Tahmures / Ancient Tablet / S04 Three Readings. 10s at 12fps. Candidate procedural Illustrated V2 interpretations. Akvan examines records; Black Div reads then turns empty-handed; Div-e Sefid reaches. One tablet stays on cloth on table. No dialogue/lipsync/custody transfer. No final likeness, motion or room approval. Source commit e8afb28d077e7daa5623d2fec9ab041236395724. Exact sources and hashes: chapter-context.json on try2."
    )
    return scene


build()
