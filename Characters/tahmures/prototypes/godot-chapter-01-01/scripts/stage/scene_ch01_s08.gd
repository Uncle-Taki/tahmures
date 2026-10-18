extends SceneBase
## CH01-S08 — Roles become testable (15 s).
## The SAME sentence «دروازهٔ غربی را ببند» / "Close the western gate" shown
## three ways (panel labels from the OST layer): current task when Arash the
## Gatekeeper sends it to the watch; evidence when quoted in a trial; mere ink
## under a practising apprentice's hand. The tablet text itself is
## OST-S08-0, rendered programmatically — never baked into sprites.

var _panels: Array = []
var _arash: Sprite2D
var _beam: Line2D
var _pan_l: Line2D
var _pan_r: Line2D
var _cup_l: Polygon2D
var _cup_r: Polygon2D
var _apprentice: Sprite2D
var _ink_swell: ColorRect
var _gate_tablet: Sprite2D


func _ready() -> void:
	super._ready()
	scene_id = "CH01-S08"
	duration = 15.0
	bg_color = StageKit.BG_HALL
	add_child(StageKit.make_rect(Rect2(0, 440, 1280, 280), StageKit.FLOOR))
	var centers := [213.0, 640.0, 1067.0]
	for i in 3:
		var p := StageKit.make_rect(Rect2(centers[i] - 190.0, 90.0, 380.0, 470.0), Color(0.055, 0.067, 0.094, 0.55))
		add_child(p)
		_panels.append(p)
	# a) Gatekeeper: Arash at the gate with a watch tablet.
	_arash = StageKit.make_sprite("res://assets/standins/arash.png", Vector2(170.0, 560 - 148), 0.6)
	add_child(_arash)
	_gate_tablet = StageKit.make_sprite("res://assets/standins/tablet.png", Vector2(268, 470), 0.3)
	add_child(_gate_tablet)
	# b) Court: a balance/scales glyph (neutral geometry, no iconography). All
	# parts rotate together around the post pivot when evidence is weighed.
	_beam = StageKit.make_line(Vector2(580, 430), Vector2(700, 430), StageKit.GOLD, 3.0)
	add_child(_beam)
	var post := StageKit.make_line(Vector2(640, 430), Vector2(640, 520), StageKit.GOLD, 3.0)
	add_child(post)
	_pan_l = StageKit.make_line(Vector2(580, 430), Vector2(580, 468), StageKit.GOLD, 2.0)
	add_child(_pan_l)
	_pan_r = StageKit.make_line(Vector2(700, 430), Vector2(700, 468), StageKit.GOLD, 2.0)
	add_child(_pan_r)
	_cup_l = StageKit.make_polygon(PackedVector2Array([Vector2(562, 468), Vector2(598, 468), Vector2(580, 492)]), Color(0.878, 0.831, 0.710, 0.9))
	add_child(_cup_l)
	_cup_r = StageKit.make_polygon(PackedVector2Array([Vector2(682, 468), Vector2(718, 468), Vector2(700, 492)]), Color(0.878, 0.831, 0.710, 0.9))
	add_child(_cup_r)
	# c) Apprentice's practice slab with a swelling ink blot.
	_apprentice = StageKit.make_sprite("res://assets/standins/apprentice.png", Vector2(1030.0, 560 - 148), 0.6)
	add_child(_apprentice)
	add_child(StageKit.make_rect(Rect2(1080, 500, 120, 20), StageKit.WOOD))
	_ink_swell = StageKit.make_rect(Rect2(1110, 512, 24, 6), StageKit.INK)
	add_child(_ink_swell)


func update(local_t: float, _ctx: Dictionary) -> void:
	# Panel a active 0.4–5.6 (NEN-08A), b active 6.8–11.6 (NEN-08B first
	# clause), c active 12.0–14.6 (NEN-08B last clause).
	var a_on := local_t >= 0.4 and local_t < 5.6
	var b_on := local_t >= 5.8 and local_t < 11.6
	var c_on := local_t >= 11.8
	# a) Arash hands the tablet to the (off-panel) watch: a short forward lean.
	var lean := 10.0 * (1.0 if a_on else 0.0)
	_arash.position.x = 170.0 + lean * clampf(local_t / 4.0, 0.0, 1.0)
	_gate_tablet.visible = a_on
	# b) Scales settle: the beam tilts from level and settles level again
	# (evidence is weighed, not decided — no outcome implied).
	var pivot := Vector2(640, 430)
	var tilt := 0.0
	if b_on:
		var settle := clampf((local_t - 5.8) / 3.0, 0.0, 1.0)
		tilt = 0.16 * sin(settle * 5.0) * (1.0 - settle)
	var p_l := pivot + Vector2(-60, 0).rotated(tilt)
	var p_r := pivot + Vector2(60, 0).rotated(tilt)
	_beam.points = PackedVector2Array([p_l, p_r])
	_pan_l.points = PackedVector2Array([p_l, p_l + Vector2(0, 38).rotated(tilt)])
	_pan_r.points = PackedVector2Array([p_r, p_r + Vector2(0, 38).rotated(tilt)])
	var drop_l := p_l + Vector2(0, 38).rotated(tilt)
	var drop_r := p_r + Vector2(0, 38).rotated(tilt)
	_cup_l.polygon = PackedVector2Array([drop_l + Vector2(-18, 0), drop_l + Vector2(18, 0), drop_l + Vector2(0, 24)])
	_cup_r.polygon = PackedVector2Array([drop_r + Vector2(-18, 0), drop_r + Vector2(18, 0), drop_r + Vector2(0, 24)])
	# c) Ink blot swells under the apprentice's hand (pure pulse).
	if c_on:
		var k := 1.0 + 0.35 * sin(local_t * 1.6)
		_ink_swell.size = Vector2(24.0 * k, 6.0 * k)
		_ink_swell.position = Vector2(1110.0 - 12.0 * (k - 1.0), 512.0 - 3.0 * (k - 1.0))
	else:
		_ink_swell.size = Vector2(24, 6)
		_ink_swell.position = Vector2(1110, 512)


func cam_target(_local_t: float) -> Dictionary:
	return {"pos": Vector2(640, 360), "zoom": 1.0}
