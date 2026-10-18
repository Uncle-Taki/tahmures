extends SceneBase
## CH01-S01 — Establishing: the Hall of Scripts (12 s).
## Thirty dissimilar doors, arriving material bundles (clay, leather, bark,
## silk), Shahrasp reading silk through a crystal lens in the far background.

var _doors: Array = []
var _bundles: Array = []
var _shahrasp: Sprite2D
var _lens: Node2D


func _ready() -> void:
	super._ready()
	scene_id = "CH01-S01"
	duration = 12.0
	bg_color = StageKit.BG_HALL
	# Wall of doors: 10 visible along the back wall, each with a dissimilar
	# handle (different colour/position) — "no two handles alike".
	for i in 10:
		var x := 130.0 + i * 115.0
		var door := StageKit.make_rect(Rect2(x, 130, 70, 300), StageKit.WOOD_DARK)
		add_child(door)
		var handle_c: Color = [Color(0.91, 0.722, 0.294), Color(0.631, 0.431, 0.310), Color(0.502, 0.620, 0.749), Color(0.722, 0.800, 0.580)][i % 4]
		var handle := StageKit.make_polygon(
			PackedVector2Array([
				Vector2(x + 46 + (i % 3) * 6, 240 + (i % 5) * 30),
				Vector2(x + 54 + (i % 3) * 6, 240 + (i % 5) * 30),
				Vector2(x + 54 + (i % 3) * 6, 252 + (i % 5) * 30),
				Vector2(x + 46 + (i % 3) * 6, 252 + (i % 5) * 30),
			]), handle_c)
		add_child(handle)
		_doors.append([door, handle])
	# Floor
	add_child(StageKit.make_rect(Rect2(0, 440, 1280, 280), StageKit.FLOOR))
	# Entry bundles (one per material), appear one by one with NEN-01B.
	var cols: Array = [StageKit.CLAY, StageKit.WOOD, StageKit.INK, Color(0.827, 0.843, 0.902)]
	for i in 4:
		var b := StageKit.make_rect(Rect2(90 + i * 78, 560, 60, 34), cols[i])
		b.position.x = -200.0
		add_child(b)
		_bundles.append([b, 90.0 + i * 78.0, 6.5 + i * 1.6])
	# Shahrasp far background, right: small stand-in + crystal lens glow.
	_shahrasp = StageKit.make_sprite("res://assets/standins/shahrasp.png", Vector2(1130, 520 - 144), 0.42)
	add_child(_shahrasp)
	_lens = StageKit.make_polygon(PackedVector2Array(
		[Vector2(1080, 388), Vector2(1096, 396), Vector2(1080, 404), Vector2(1064, 396)]), Color(0.827, 0.922, 1.0, 0.85))
	add_child(_lens)


func update(local_t: float, ctx: Dictionary) -> void:
	for entry in _bundles:
		var b: ColorRect = entry[0]
		var target_x: float = entry[1]
		var appear: float = entry[2]
		if local_t >= appear:
			var k := minf((local_t - appear) / 1.2, 1.0)
			b.position.x = lerpf(-200.0, target_x, k)
		else:
			b.position.x = -200.0
	# Lens glint oscillation (pure).
	var glint := 0.6 + 0.35 * sin(local_t * 1.7)
	_lens.modulate = Color(1, 1, 1, glint)


func cam_target(local_t: float) -> Dictionary:
	return {"pos": Vector2(560.0 + 6.0 * sin(local_t * 0.25), 330.0), "zoom": 1.0}
