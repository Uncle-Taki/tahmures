extends SceneBase
## CH01-S07 — The four labels (31 s). Six sub-beats:
##   a (0.3–4.8)   Shahrasp sharpens his reed — one completed action
##   b (5.3–11.5)  Tahmures dictates the longer instruction (D-S07-1)
##   c (12.0–15.6) Akvan Div's warning (D-S07-2)
##   d (16.2–19.8) Tahmures stops the reed
##   e (21.0–30.4) four labels appear one by one (OST-S07-1..4 ticks):
##                 speaker/recipient/occasion marked «?», requested result marked
##   f (24.5+)     the actual request on a separate sealed card (prop only;
##                 the seal does not establish authority or provide security)
## The chip row and overlay boundary line are drawn by the OST layer / a
## scene-space note; the four label props are blank clay tiles.

var _tahmures: TahmuresRig
var _shahrasp: Sprite2D
var _akvan: Sprite2D
var _reed: Sprite2D
var _sharpen_glow: Label
var _labels: Array = []
var _sealed_card: Sprite2D
var _card_note: Label


func _ready() -> void:
	super._ready()
	scene_id = "CH01-S07"
	duration = 31.0
	bg_color = StageKit.BG_HALL
	add_child(StageKit.make_rect(Rect2(0, 440, 1280, 280), StageKit.FLOOR))
	# Work table
	add_child(StageKit.make_rect(Rect2(420, 470, 520, 26), StageKit.WOOD))
	add_child(StageKit.make_rect(Rect2(440, 496, 18, 120), StageKit.WOOD_DARK))
	add_child(StageKit.make_rect(Rect2(902, 496, 18, 120), StageKit.WOOD_DARK))
	# Shahrasp at the table (reed in hand region ~ x 560).
	_shahrasp = StageKit.make_sprite("res://assets/standins/shahrasp.png", Vector2(480, 520 - 148), 0.62)
	add_child(_shahrasp)
	_reed = StageKit.make_sprite("res://assets/standins/reed_pen.png", Vector2(580, 470), 0.55)
	add_child(_reed)
	_sharpen_glow = StageKit.make_label("—", Vector2(560, 430), 26, StageKit.GOLD)
	_sharpen_glow.visible = false
	add_child(_sharpen_glow)
	# Tahmures to the right of the table.
	_tahmures = TahmuresRig.new()
	_tahmures.position = Vector2(1050, 724)
	_tahmures.scale = Vector2(0.6, 0.6)
	_tahmures.arm_visible = false
	add_child(_tahmures)
	# Akvan Div at the far left, observing.
	_akvan = StageKit.make_sprite("res://assets/standins/akvan_div.png", Vector2(180, 520 - 148), 0.62)
	add_child(_akvan)
	# Four blank clay label tiles (they appear one by one; the text is the
	# programmatic OST tick row, never pre-baked).
	for i in 4:
		var tile := StageKit.make_rect(Rect2(180.0 + i * 280.0 - 120.0, 430.0, 240.0, 56.0), StageKit.CLAY)
		tile.visible = false
		add_child(tile)
		_labels.append([tile, 21.0 + i * 2.2])
	# Separate sealed card (beat f): arrives beside the labels.
	_sealed_card = StageKit.make_sprite("res://assets/standins/tablet_sealed_card.png", Vector2(700, 396), 0.5)
	_sealed_card.visible = false
	add_child(_sealed_card)
	_card_note = StageKit.make_label("the seal does not establish authority or provide security — it marks a request, nothing more",
		Vector2(240, 84), 15, Color(0.769, 0.800, 0.886))
	_card_note.visible = false
	add_child(_card_note)


func update(local_t: float, _ctx: Dictionary) -> void:
	# Beat a: Shahrasp sharpens the reed — one completed action (0.3–4.8).
	# The reed tilts with a deterministic oscillation that decays to rest.
	var amp := 0.5 * clampf(1.0 - (local_t - 0.3) / 4.5, 0.0, 1.0)
	_reed.rotation = 0.35 * sin(local_t * 6.0) * amp
	_sharpen_glow.visible = local_t >= 0.3 and local_t < 4.8
	# Beat b: Tahmures dictates (5.3–11.5): neutral face, mouth neutral
	# (no owner speech audio), arm points at the tablet region.
	if local_t >= 5.3 and local_t < 11.5:
		_tahmures.set_arm_visible(true)
		_tahmures.set_arm_rotation(-0.7, -0.4, 0.0)
	else:
		_tahmures.set_arm_visible(false)
	# Beat c: Akvan warns (12.0–15.6) — leans in slightly.
	if local_t >= 12.0 and local_t < 15.6:
		_akvan.position.x = 180.0 + 16.0
	else:
		_akvan.position.x = 180.0
	# Beat d: Tahmures stops the reed (16.2–19.8): thinking state, a raised
	# hand gesture (temporary arm) signalling the stop.
	if local_t >= 16.2 and local_t < 19.8:
		_tahmures.set_arm_visible(true)
		_tahmures.set_arm_rotation(-1.15, -0.5, -0.2)
	# Beat e: four labels appear one by one (21.0, 23.2, 25.4, 27.6).
	for entry in _labels:
		var tile: ColorRect = entry[0]
		tile.visible = local_t >= entry[1]
	# Beat f: sealed card arrives at 24.5, note from 25.0 (prop only).
	_sealed_card.visible = local_t >= 24.5
	_card_note.visible = local_t >= 25.0
	# State: neutral except after the stop (realization) — thinking from
	# 16.2 onward.
	if local_t >= 16.2:
		_tahmures.set_state("thinking")
	else:
		_tahmures.set_state("neutral")
	_tahmures.set_mouth("neutral")


func cam_target(local_t: float) -> Dictionary:
	# Table work for a–d; pull back slightly for the label row in e/f.
	var zoom := 1.0
	var pos := Vector2(640, 340)
	if local_t >= 20.5:
		pos = Vector2(640, 360)
		zoom = 1.0
	return {"pos": pos, "zoom": zoom}
