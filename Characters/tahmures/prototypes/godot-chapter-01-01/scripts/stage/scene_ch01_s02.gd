extends SceneBase
## CH01-S02 — The tablet arrives (16 s).
## Chapar (distinct from Simurgh: single satchel stand-in) brings the found
## tablet; the dissolved seal scar is highlighted; the exact imperative is
## rendered as programmatic text by the OST layer (OST-S02-1).

var _chapar: Sprite2D
var _tablet: Sprite2D
var _pedestal: ColorRect
var _seal_ring: Line2D


func _ready() -> void:
	super._ready()
	scene_id = "CH01-S02"
	duration = 16.0
	bg_color = StageKit.BG_HALL
	add_child(StageKit.make_rect(Rect2(0, 440, 1280, 280), StageKit.FLOOR))
	# Cedar pedestal
	_pedestal = StageKit.make_rect(Rect2(660, 470, 130, 60), StageKit.WOOD)
	add_child(_pedestal)
	# Tablet starts off-screen with Chapar, lands on the pedestal.
	_tablet = StageKit.make_sprite("res://assets/standins/tablet.png", Vector2(-150, 430), 0.42)
	add_child(_tablet)
	# Chapar: single satchel, clearly distinct from Simurgh's double satchel.
	_chapar = StageKit.make_sprite("res://assets/standins/chapar.png", Vector2(-120, 520 - 148), 0.62)
	add_child(_chapar)
	# Seal-scar magnifier ring (appears during NEN-02B).
	_seal_ring = Line2D.new()
	_seal_ring.width = 3.0
	_seal_ring.default_color = Color(0.965, 0.949, 0.902, 0.9)
	add_child(_seal_ring)


func update(local_t: float, ctx: Dictionary) -> void:
	# Chapar walks in during NEN-02A (12.5–18.3 -> local 0.5–6.3), stops at 300.
	var walk_k := clampf((local_t - 0.5) / 5.0, 0.0, 1.0)
	var walk_x := lerpf(-120.0, 300.0, walk_k)
	_chapar.position.x = walk_x
	# Tablet rides with Chapar until local 6.5, then moves to the pedestal.
	if local_t < 6.5:
		_tablet.position = Vector2(walk_x + 70, 420)
	else:
		var put_k := minf((local_t - 6.5) / 1.2, 1.0)
		_tablet.position = Vector2(lerpf(walk_x + 70.0, 725.0, put_k), lerpf(420.0, 432.0, put_k))
	# Dissolved seal highlight: ring pulses over the tablet's cracked corner
	# during NEN-02B (local 6.5–9.3).
	var ring_on: float = 0.0
	if local_t >= 6.5 and local_t < 9.3:
		ring_on = 0.55 + 0.45 * sin(local_t * 4.0)
	_seal_ring.visible = ring_on > 0.0
	if ring_on > 0.0:
		var c := Vector2(725, 432)
		_seal_ring.points = PackedVector2Array([
			c + Vector2(30, -26), c + Vector2(44, -8), c + Vector2(30, 10), c + Vector2(14, -8),
		])
		_seal_ring.closed = true
		_seal_ring.default_color = Color(0.965, 0.949, 0.902, ring_on)


func cam_target(_local_t: float) -> Dictionary:
	return {"pos": Vector2(560, 330), "zoom": 1.0}
