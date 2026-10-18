extends SceneBase
## CH01-S09 — Engineering overlay: the request envelope (20 s). Review
## finding F5 compliant: ALL EIGHT components appear as equal-weight chips
## (identical size and colour; two rows are a neutral layout, not a
## hierarchy). The exact formula and the review line come from the OST
## layer as programmatic text. Review questions are neutral numbered dots —
## no seal icons, no laptop/screen icons, no security-boundary claim:
## enforcement belongs to the application.

const CHIP_SIZE := Vector2(250, 54)
const ROW1_Y := 180.0
const ROW2_Y := 262.0
const COL_X := [170.0, 450.0, 730.0, 1010.0]
const TERMS_EN := ["instructions", "current task", "context", "data", "examples", "constraints", "output contract", "interaction state"]
const TERMS_FA := ["دستورها", "وظیفهٔ جاری", "کانتکست", "داده", "مثال‌ها", "محدودیت‌ها", "قرارداد خروجی", "وضعیت تعامل"]
const ENV_RECT := Rect2(60.0, 140.0, 1160.0, 210.0)

var _lang := "en"
var _chips: Array = []          # [chip, label, appear_t]
var _dots: Array = []           # [polygon, number_label, appear_t]
var _envelope: Line2D
var _boundary_note: Label
var _note_fa := "اجرا به عهدهٔ سامانه است، نه واژه‌ها"
var _note_en := "enforcement belongs to the application — not to the words"


func _ready() -> void:
	super._ready()
	scene_id = "CH01-S09"
	duration = 20.0
	bg_color = StageKit.BG_BRIDGE
	# Envelope outline, line-drawn: points grow over time (pure function).
	_envelope = Line2D.new()
	_envelope.width = 2.0
	_envelope.default_color = Color(0.878, 0.831, 0.710, 0.8)
	add_child(_envelope)
	# Eight equal chips — identical size and colour in both rows.
	for i in 8:
		var row: int = i / 4
		var col: int = i % 4
		var y := ROW1_Y if row == 0 else ROW2_Y
		var rect := Rect2(COL_X[col] - CHIP_SIZE.x / 2.0, y, CHIP_SIZE.x, CHIP_SIZE.y)
		var chip := StageKit.make_rect(rect, Color(0.165, 0.208, 0.318))
		chip.visible = false
		add_child(chip)
		var lbl := StageKit.make_label(TERMS_EN[i], rect.position + Vector2(6, 0), 19, Color(0.925, 0.933, 0.949))
		lbl.custom_minimum_size = Vector2(CHIP_SIZE.x - 12, 0)
		lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		lbl.visible = false
		add_child(lbl)
		_chips.append([chip, lbl, 5.0 + i * 1.0])
	# Four neutral numbered dots for the review questions (no seal icons).
	for i in 4:
		var c := Vector2(490 + i * 90, 396)
		var pts := PackedVector2Array()
		for k in 16:
			var a := TAU * float(k) / 16.0
			pts.append(c + Vector2(cos(a), sin(a)) * 14.0)
		var poly := Polygon2D.new()
		poly.polygon = pts
		poly.color = Color(0.318, 0.380, 0.522)
		poly.visible = false
		add_child(poly)
		var num := StageKit.make_label(str(i + 1), c + Vector2(-6, -8), 16, Color(0.925, 0.933, 0.949))
		num.visible = false
		add_child(num)
		_dots.append([poly, num, 13.4 + i * 0.6])
	# Boundary note (application owns enforcement; no security claim).
	_boundary_note = StageKit.make_label(_note_en, Vector2(170, 356), 15, Color(0.769, 0.800, 0.886))
	_boundary_note.visible = false
	add_child(_boundary_note)


func set_language(lang: String) -> void:
	_lang = lang
	for i in 8:
		var lbl: Label = _chips[i][1]
		lbl.text = TERMS_EN[i] if lang == "en" else TERMS_FA[i]
		if lang == "fa":
			lbl.text_direction = Control.TEXT_DIRECTION_RTL
			lbl.layout_direction = Control.LAYOUT_DIRECTION_RTL
			var sf = StageKit.rtl_font()
			lbl.add_theme_font_override("font", sf)
		else:
			lbl.text_direction = Control.TEXT_DIRECTION_AUTO
			lbl.layout_direction = Control.LAYOUT_DIRECTION_LTR
			lbl.add_theme_font_override("font", StageKit.latin_font())
	_boundary_note.text = _note_fa if lang == "fa" else _note_en
	if lang == "fa":
		_boundary_note.text_direction = Control.TEXT_DIRECTION_RTL
		_boundary_note.layout_direction = Control.LAYOUT_DIRECTION_RTL
		var sf2 = StageKit.rtl_font()
		_boundary_note.add_theme_font_override("font", sf2)
	else:
		_boundary_note.text_direction = Control.TEXT_DIRECTION_AUTO
		_boundary_note.layout_direction = Control.LAYOUT_DIRECTION_LTR
		_boundary_note.add_theme_font_override("font", StageKit.latin_font())


func _set_envelope_progress(k: float) -> void:
	# Perimeter walk around ENV_RECT; k in [0,1] reveals that fraction.
	var r := ENV_RECT
	var per: float = 2.0 * (r.size.x + r.size.y)
	var target: float = per * k
	var pts := PackedVector2Array([r.position])
	var corners: Array = [r.position, Vector2(r.end.x, r.position.y), Vector2(r.end.x, r.end.y), Vector2(r.position.x, r.end.y)]
	var side_lengths: Array = [r.size.x, r.size.y, r.size.x, r.size.y]
	var walk: float = 0.0
	for i in 4:
		if walk >= target:
			break
		var from: Vector2 = corners[i]
		var to: Vector2 = corners[(i + 1) % 4]
		var side: float = side_lengths[i]
		var remaining: float = target - walk
		if remaining >= side:
			pts.append(to)
			walk += side
		else:
			pts.append(from.lerp(to, remaining / side))
			walk = target
	_envelope.points = pts


func update(local_t: float, _ctx: Dictionary) -> void:
	# Envelope line-draw during NEN-09A (131.4–135.8 global -> local 0.4–4.8).
	_set_envelope_progress(clampf((local_t - 0.4) / 4.4, 0.0, 1.0))
	# Eight chips, one per listed term (local 5.0–13.0, during NEN-09B).
	for i in 8:
		var appear: float = _chips[i][2]
		_chips[i][0].visible = local_t >= appear
		_chips[i][1].visible = local_t >= appear
	# Review dots during NEN-09C (local 13.4–19.5).
	for entry in _dots:
		var on: bool = local_t >= entry[2]
		entry[0].visible = on
		entry[1].visible = on
	_boundary_note.visible = local_t >= 14.6


func cam_target(_local_t: float) -> Dictionary:
	return {"pos": Vector2(640, 360), "zoom": 1.0}
