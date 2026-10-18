extends SceneBase
## CH01-S05 — There are eleven watchfires (15 s).
## Dusk. The wet Black Div returns and reports eleven fires; the five-line
## source exchange is captioned verbatim; Tahmures's realization shows as the
## approved thinking state. No new dialogue beyond the source.

var _tahmures: TahmuresRig
var _black_div: Sprite2D


func _ready() -> void:
	super._ready()
	scene_id = "CH01-S05"
	duration = 15.0
	bg_color = StageKit.BG_HALL_DUSK
	add_child(StageKit.make_rect(Rect2(0, 440, 1280, 280), StageKit.FLOOR))
	# River hint on the left: Black Div has crossed it.
	add_child(StageKit.make_rect(Rect2(0, 470, 260, 250), StageKit.RIVER))
	_tahmures = TahmuresRig.new()
	_tahmures.position = Vector2(360, 724)
	_tahmures.scale = Vector2(0.6, 0.6)
	_tahmures.arm_visible = false
	add_child(_tahmures)
	_black_div = StageKit.make_sprite("res://assets/standins/black_div.png", Vector2(-120, 520 - 148), 0.66)
	add_child(_black_div)

func update(local_t: float, _ctx: Dictionary) -> void:
	# Return during NEN-05 (53.2–55.8 global -> local 0.2–2.8), stops at 340.
	var walk_k := clampf((local_t - 0.2) / 2.6, 0.0, 1.0)
	_black_div.position.x = lerpf(-120.0, 340.0, walk_k)
	# Five-line exchange: 56.2–67.7 global -> local 3.2–14.7.
	# Tahmures listens, then realizes (thinking) after D-S05-4 ends (65.4 -> local 12.4).
	if local_t < 3.2:
		_tahmures.set_state("neutral")
	elif local_t < 12.4:
		_tahmures.set_state("neutral")
	else:
		_tahmures.set_state("thinking")
	_tahmures.set_mouth("neutral")


func cam_target(_local_t: float) -> Dictionary:
	return {"pos": Vector2(540, 320), "zoom": 1.0}
