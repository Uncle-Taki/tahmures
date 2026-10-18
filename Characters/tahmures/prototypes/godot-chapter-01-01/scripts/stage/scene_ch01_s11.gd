extends SceneBase
## CH01-S11 — Takeaway + series card (7 s).
## Shahrasp's hands over a ledger; the ledger line is the tale-verbatim
## overlay (OST-S11-1); the episode takeaway card (OST-S11-2); the series
## mark (clay tablet crossed by reed pen — the committed series_mark.png
## prop, deterministic). The two OST lines overlap by design (169.8–172.6):
## the takeaway sits upper, the ledger line centre — distinct bands.

var _shahrasp: Sprite2D
var _ledger: Sprite2D
var _hand_l: Sprite2D
var _hand_r: Sprite2D
var _mark: Sprite2D
var _mark_ring: Line2D


func _ready() -> void:
	super._ready()
	scene_id = "CH01-S11"
	duration = 7.0
	bg_color = StageKit.BG_LEDGER
	add_child(StageKit.make_rect(Rect2(0, 470, 1280, 250), StageKit.FLOOR))
	# Ledger on a lectern.
	add_child(StageKit.make_rect(Rect2(560, 470, 160, 24), StageKit.WOOD))
	add_child(StageKit.make_rect(Rect2(626, 494, 28, 130), StageKit.WOOD_DARK))
	_ledger = StageKit.make_sprite("res://assets/standins/ledger.png", Vector2(640, 452), 0.6)
	add_child(_ledger)
	# Shahrasp's hands (temporary placeholders) resting on the ledger edge.
	_hand_l = StageKit.make_sprite("res://assets/temporary-body/hand_point.png", Vector2(560, 470), 0.5)
	_hand_l.add_to_group("temporary_placeholder")
	add_child(_hand_l)
	_hand_r = StageKit.make_sprite("res://assets/temporary-body/hand_point.png", Vector2(720, 470), 0.5)
	_hand_r.add_to_group("temporary_placeholder")
	add_child(_hand_r)
	# Shahrasp stands behind the lectern, smaller/farther.
	_shahrasp = StageKit.make_sprite("res://assets/standins/shahrasp.png", Vector2(640, 430 - 148), 0.5)
	add_child(_shahrasp)
	# Series mark (clay tablet crossed by reed pen) with a slow ring pulse.
	_mark = StageKit.make_sprite("res://assets/standins/series_mark.png", Vector2(640, 250), 0.5)
	_mark.visible = false
	add_child(_mark)
	_mark_ring = Line2D.new()
	_mark_ring.width = 2.0
	_mark_ring.default_color = Color(0.91, 0.722, 0.294, 0.7)
	_mark_ring.closed = true
	_mark_ring.visible = false
	add_child(_mark_ring)


func update(local_t: float, _ctx: Dictionary) -> void:
	# Hands settle onto the ledger (0.3–1.5).
	var settle := clampf((local_t - 0.3) / 1.2, 0.0, 1.0)
	_hand_l.position = Vector2(lerpf(520.0, 560.0, settle), lerpf(430.0, 470.0, settle))
	_hand_r.position = Vector2(lerpf(760.0, 720.0, settle), lerpf(430.0, 470.0, settle))
	# Series mark fades in under the takeaway (4.2+).
	var mk := clampf((local_t - 4.2) / 1.0, 0.0, 1.0)
	_mark.visible = mk > 0.0
	_mark.modulate = Color(1, 1, 1, mk)
	_mark_ring.visible = mk > 0.0
	if mk > 0.0:
		var rr := 46.0 + 6.0 * sin(local_t * 2.0)
		var pts := PackedVector2Array()
		for k in 24:
			var a := TAU * float(k) / 24.0
			pts.append(Vector2(640, 250) + Vector2(cos(a), sin(a)) * rr)
		_mark_ring.points = pts
		_mark_ring.default_color = Color(0.91, 0.722, 0.294, 0.7 * mk)
	# Gentle breathing bob (deterministic, approved head is elsewhere; the
	# stand-in is a silhouette, bob is staging only).
	_shahrasp.position.y = 282.0 + 2.0 * sin(local_t * 1.2)


func cam_target(_local_t: float) -> Dictionary:
	return {"pos": Vector2(640, 360), "zoom": 1.0}
