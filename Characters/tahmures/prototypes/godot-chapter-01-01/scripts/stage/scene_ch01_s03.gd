extends SceneBase
## CH01-S03 — Tell me what this is (10 s).
## Tahmures asks his underspecified question (D-S03-1, mouth neutral — the
## candidate has no owner-approved speech audio); three distinct recipients
## examine the tablet in their own methods: the Keeper traces marks with a
## lens, Simurgh hefts and checks the cord, the Black Div reads twice and holds.

var _tahmures: TahmuresRig
var _akvan: Sprite2D
var _simurgh: Sprite2D
var _black_div: Sprite2D
var _tablet: Sprite2D
var _lens: Node2D


func _ready() -> void:
	super._ready()
	scene_id = "CH01-S03"
	duration = 10.0
	bg_color = StageKit.BG_HALL
	add_child(StageKit.make_rect(Rect2(0, 440, 1280, 280), StageKit.FLOOR))
	_tablet = StageKit.make_sprite("res://assets/standins/tablet.png", Vector2(760, 470), 0.5)
	add_child(_tablet)
	add_child(StageKit.make_rect(Rect2(730, 500, 60, 40), StageKit.WOOD))
	_tahmures = TahmuresRig.new()
	_tahmures.position = Vector2(300, 724)
	_tahmures.scale = Vector2(0.55, 0.55)
	_tahmures.arm_visible = false
	add_child(_tahmures)
	_akvan = StageKit.make_sprite("res://assets/standins/akvan_div.png", Vector2(640, 520 - 148), 0.62)
	add_child(_akvan)
	_simurgh = StageKit.make_sprite("res://assets/standins/simurgh.png", Vector2(900, 520 - 148), 0.62)
	add_child(_simurgh)
	_black_div = StageKit.make_sprite("res://assets/standins/black_div.png", Vector2(1100, 520 - 148), 0.62)
	add_child(_black_div)
	_lens = StageKit.make_polygon(PackedVector2Array(
		[Vector2(742, 440), Vector2(752, 448), Vector2(742, 456), Vector2(732, 448)]), Color(0.827, 0.922, 1.0, 0.9))
	add_child(_lens)


func update(local_t: float, _ctx: Dictionary) -> void:
	# D-S03-1 (32.8–35.3 global -> local 4.8–7.3): Tahmures asks. Mouth stays
	# neutral (no owner speech audio); a brief thinking state follows the
	# question as he waits for answers.
	if local_t < 4.8:
		_tahmures.set_state("neutral")
	elif local_t < 7.3:
		_tahmures.set_state("neutral")
	else:
		_tahmures.set_state("thinking")
	_tahmures.set_mouth("neutral")
	# Local time into the examination (starts ~5.0).
	var ex := local_t - 5.0
	# Akvan traces marks with the lens: lens moves along the tablet face.
	if ex >= 0.0:
		_lens.position = Vector2(740.0 + 25.0 * sin(ex * 1.1), 444.0 + 6.0 * sin(ex * 2.3))
		_lens.visible = true
	else:
		_lens.visible = false
	# Simurgh hefts the tablet: small bob.
	if ex >= 0.8:
		_simurgh.position.y = 372.0 - 6.0 * maxf(0.0, sin(ex * 2.0))
	# Black Div reads twice and holds: two quick nods, then still.
	if ex >= 1.6:
		var bob := 4.0 * sin(ex * 3.0) if ex < 4.0 else 0.0
		_black_div.position.y = 372.0 + bob


func cam_target(_local_t: float) -> Dictionary:
	return {"pos": Vector2(560, 330), "zoom": 1.0}
