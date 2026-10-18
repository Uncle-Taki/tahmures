extends SceneBase
## CH01-S04 — Three readings (15 s).
## Three equal third-panels (panel labels from the OST layer):
##   a: Akvan Div catalogues under "Military Records: Northern Frontier"
##   b: Simurgh wraps the tablet in oilcloth as an urgent message
##   c: Black Div reads and leaves to act
## Each panel shows a distinct actor and a distinct action; the three are
## staged as parallel columns (equal width), not a hierarchy.

var _panels: Array = []
var _akvan: Sprite2D
var _simurgh: Sprite2D
var _black_div: Sprite2D
var _wrap: ColorRect
var _wrap_k_label: Label


func _ready() -> void:
	super._ready()
	scene_id = "CH01-S04"
	duration = 15.0
	bg_color = StageKit.BG_HALL
	add_child(StageKit.make_rect(Rect2(0, 440, 1280, 280), StageKit.FLOOR))
	var centers := [213.0, 640.0, 1067.0]
	for i in 3:
		var p := StageKit.make_rect(Rect2(centers[i] - 190.0, 90.0, 380.0, 470.0), Color(0.055, 0.067, 0.094, 0.55))
		add_child(p)
		_panels.append(p)
	# a) Akvan Div catalogues: stand-in + a small catalogue slip.
	_akvan = StageKit.make_sprite("res://assets/standins/akvan_div.png", Vector2(170.0, 560 - 148), 0.62)
	add_child(_akvan)
	# b) Simurgh wraps: stand-in + oilcloth wrap closing over a tablet.
	_simurgh = StageKit.make_sprite("res://assets/standins/simurgh.png", Vector2(600.0, 560 - 148), 0.62)
	add_child(_simurgh)
	var tablet_b := StageKit.make_sprite("res://assets/standins/tablet.png", Vector2(660, 520), 0.34)
	add_child(tablet_b)
	_wrap = StageKit.make_rect(Rect2(632, 500, 60, 42), Color(0.541, 0.620, 0.502, 0.9))
	_wrap.scale = Vector2(0.0, 1.0)
	add_child(_wrap)
	# c) Black Div reads then leaves to act.
	_black_div = StageKit.make_sprite("res://assets/standins/black_div.png", Vector2(1030.0, 560 - 148), 0.62)
	add_child(_black_div)


func update(local_t: float, _ctx: Dictionary) -> void:
	# Panel a (record): Akvan leans over the slip, a pen scratch.
	_akvan.position.x = 170.0 + 14.0 * clampf(local_t / 4.0, 0.0, 1.0)
	# Panel b (urgent message): wrap closes over the tablet during
	# D-S04-2 (48.2–50.9 global -> local 10.2–12.9).
	var wk := clampf((local_t - 10.2) / 2.7, 0.0, 1.0)
	_wrap.scale = Vector2(maxf(wk, 0.001), 1.0)
	# Panel c (command): Black Div reads for a while, then walks off right.
	var leave_k := clampf((local_t - 13.2) / 1.8, 0.0, 1.0)
	_black_div.position.x = 1030.0 + 260.0 * leave_k
	_black_div.visible = leave_k < 1.0


func cam_target(_local_t: float) -> Dictionary:
	return {"pos": Vector2(640, 360), "zoom": 1.0}
