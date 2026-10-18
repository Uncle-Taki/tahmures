extends SceneBase
## CH01-S10 — The second message (15 s).
## The short corrective sealed message (recipient named, rumour corrected,
## acknowledgement requested) is handed to Simurgh — a STAGING INFERENCE
## (the prose does not name that carrier; labelled as such in debug/notes,
## never presented as source fact). The seal prop marks the message; it does
## not grant authority. Sunrise tableau: riders return across the ford and
## villagers lower their lamps. No invented dialogue.

var _tahmures: TahmuresRig
var _simurgh: Sprite2D
var _sealed_msg: Sprite2D
var _seal: Sprite2D
var _note: Label
var _riders: Array = []
var _lamps: Array = []
var _sun: Polygon2D


func _ready() -> void:
	super._ready()
	scene_id = "CH01-S10"
	duration = 15.0
	bg_color = StageKit.BG_SUNRISE
	# Ford + far bank.
	add_child(StageKit.make_rect(Rect2(0, 430, 1280, 120), StageKit.RIVER))
	add_child(StageKit.make_rect(Rect2(0, 550, 1280, 170), StageKit.FLOOR))
	# Tahmures on the near bank, left.
	_tahmures = TahmuresRig.new()
	_tahmures.position = Vector2(300, 724)
	_tahmures.scale = Vector2(0.62, 0.62)
	_tahmures.arm_visible = false
	add_child(_tahmures)
	# Sealed message prop in Tahmures's hand region.
	_sealed_msg = StageKit.make_sprite("res://assets/standins/tablet_sealed_card.png", Vector2(380, 470), 0.42)
	add_child(_sealed_msg)
	_seal = StageKit.make_sprite("res://assets/standins/seal_lapis.png", Vector2(380, 470), 0.42)
	add_child(_seal)
	# Simurgh (staging inference) crosses the ford from right to left.
	_simurgh = StageKit.make_sprite("res://assets/standins/simurgh.png", Vector2(1380, 560 - 148), 0.62)
	add_child(_simurgh)
	# Riders returning: they ride in from the right across the far bank.
	for i in 3:
		var r := StageKit.make_sprite("res://assets/standins/courier_rider.png", Vector2(1400 + i * 80, 400 - 140), 0.46)
		add_child(r)
		_riders.append([r, 1400.0 + i * 80.0])
	# Villagers with lamps on the near bank (right side), lamps lowered 8.0+.
	for i in 2:
		var v := StageKit.make_sprite("res://assets/standins/villager.png", Vector2(880 + i * 120, 560 - 148), 0.58)
		add_child(v)
		var lamp := StageKit.make_rect(Rect2(880 + i * 120 + 40, 470, 12, 18), Color(0.91, 0.722, 0.294, 0.9))
		add_child(lamp)
		_lamps.append([lamp, 880.0 + i * 120.0 + 40.0])
	# Sun glow rising (deterministic).
	_sun = StageKit.make_polygon(PackedVector2Array([
		Vector2(1060, 380), Vector2(1140, 380), Vector2(1100, 320),
	]), Color(0.965, 0.855, 0.620, 0.5))
	add_child(_sun)
	# Staging-inference note (record-truth; shown throughout the handoff beat).
	_note = StageKit.make_label("carrier staged as Simurgh — STAGING INFERENCE: the tale does not name the carrier; the seal marks the message, it grants no authority",
		Vector2(60, 84), 14, Color(0.769, 0.800, 0.886))
	add_child(_note)


func update(local_t: float, _ctx: Dictionary) -> void:
	# Beat 1 (0.4–4.0): Tahmures composes/seals; arm offers the message.
	if local_t >= 1.0 and local_t < 5.0:
		_tahmures.set_arm_visible(true)
		_tahmures.set_arm_rotation(-0.9, -0.35, 0.0)
	else:
		_tahmures.set_arm_visible(false)
	# Beat 2 (4.0–8.0): Simurgh crosses the ford to Tahmures; handoff at 5.0.
	var cross_k := clampf((local_t - 2.0) / 3.0, 0.0, 1.0)
	var sim_x := lerpf(1380.0, 460.0, cross_k)
	_simurgh.position.x = sim_x
	if local_t < 5.0:
		_sealed_msg.position = Vector2(380, 470)
		_seal.position = Vector2(380, 470)
	else:
		var h := clampf((local_t - 5.0) / 1.0, 0.0, 1.0)
		_sealed_msg.position = Vector2(lerpf(380.0, sim_x + 70.0, h), 470.0)
		_seal.position = Vector2(lerpf(380.0, sim_x + 70.0, h), 470.0)
	# Simurgh then carries it off (8.0–10.5) — the message exits with him.
	var leave_k := clampf((local_t - 8.0) / 2.5, 0.0, 1.0)
	if local_t >= 8.0:
		_simurgh.position.x = 460.0 + 1100.0 * leave_k
		_sealed_msg.position = Vector2(_simurgh.position.x + 70, 470)
		_seal.position = Vector2(_simurgh.position.x + 70, 470)
	_note.visible = local_t < 10.5
	# Beat 3 (10.5–14.5): sunrise tableau — riders return across the ford.
	var ret_k := clampf((local_t - 10.5) / 4.0, 0.0, 1.0)
	for entry in _riders:
		var r: Sprite2D = entry[0]
		r.position.x = entry[1] - 1150.0 * ret_k
	# Villagers lower their lamps (8.0–11.0).
	for entry in _lamps:
		var lamp: ColorRect = entry[0]
		var low := clampf((local_t - 8.0) / 3.0, 0.0, 1.0)
		lamp.position.y = 470.0 + 40.0 * low
		lamp.modulate.a = 1.0 - 0.5 * low
	# Sun rises slowly (pure).
	_sun.position.y = -14.0 * clampf(local_t / 15.0, 0.0, 1.0)
	_tahmures.set_state("neutral")
	_tahmures.set_mouth("neutral")


func cam_target(local_t: float) -> Dictionary:
	if local_t < 10.5:
		return {"pos": Vector2(560, 330), "zoom": 1.0}
	return {"pos": Vector2(700, 330), "zoom": 1.0}
