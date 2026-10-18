extends SceneBase
## CH01-S06 — Consequence montage (17 s). Review finding F1 fixed: the causal
## chain is staged visibly — (a) Simurgh ARRIVES and DELIVERS the wrapped
## packet to Arash (handoff shown); (b) Arash dispatches riders, and the
## overlay notes that delivery is not authentication; (c) three village
## rooftops alarm; (d) eleven charcoal-burner fires, calmly smoking.
## No actor lies; no div is malicious; no invented dialogue.

var _simurgh: Sprite2D
var _arash: Sprite2D
var _packet: Sprite2D
var _riders: Array = []
var _roofs: Array = []
var _campfires: Array = []
var _note_b: Label
var _note_d: Label


func _ready() -> void:
	super._ready()
	scene_id = "CH01-S06"
	duration = 17.0
	# (a) Arash's gate, (b) dispatch road, (c) villages, (d) camps.
	# Arash stands by his gate on the left.
	_arash = StageKit.make_sprite("res://assets/standins/arash.png", Vector2(220, 520 - 148), 0.62)
	add_child(_arash)
	add_child(StageKit.make_rect(Rect2(120, 200, 26, 300), StageKit.WOOD_DARK))
	add_child(StageKit.make_rect(Rect2(90, 200, 190, 26), StageKit.WOOD_DARK))
	# Simurgh enters from the right with the wrapped packet.
	_simurgh = StageKit.make_sprite("res://assets/standins/simurgh.png", Vector2(1400, 520 - 148), 0.62)
	add_child(_simurgh)
	_packet = StageKit.make_sprite("res://assets/standins/oilcloth_packet.png", Vector2(1460, 430), 0.4)
	add_child(_packet)
	# Riders wait at the dispatch gate, leave during beat b.
	for i in 3:
		var r := StageKit.make_sprite("res://assets/standins/courier_rider.png", Vector2(420 + i * 70, 520 - 140), 0.5)
		add_child(r)
		_riders.append([r, 420.0 + i * 70.0])
	# (c) Three village rooftops (beat c).
	for i in 3:
		var x := 380.0 + i * 300.0
		var roof := StageKit.make_polygon(PackedVector2Array([
			Vector2(x, 330), Vector2(x + 130, 280), Vector2(x + 260, 330),
		]), Color(0.427, 0.333, 0.251))
		add_child(roof)
		var house := StageKit.make_rect(Rect2(x, 330, 260, 110), Color(0.561, 0.486, 0.392))
		add_child(house)
		var lamp := StageKit.make_rect(Rect2(x + 118, 350, 12, 16), Color(0.91, 0.722, 0.294, 0.0))
		add_child(lamp)
		_roofs.append([lamp, x + 118.0])
	# (d) Eleven charcoal-burner fires, calmly smoking (beat d).
	for i in 11:
		var x := 90.0 + (i % 6) * 210.0
		var y := 560.0 + (i / 6) * 60.0
		var fire := StageKit.make_polygon(PackedVector2Array([
			Vector2(x, y), Vector2(x + 14, y - 26), Vector2(x + 28, y),
		]), Color(0.851, 0.541, 0.271, 0.9))
		add_child(fire)
		var smoke := StageKit.make_rect(Rect2(x + 10, y - 60, 8, 34), StageKit.SMOKE)
		smoke.modulate.a = 0.0
		add_child(smoke)
		_campfires.append([fire, smoke, x, y, float(i)])
	# Beat annotations (screen-space labels, honest record-truth).
	_note_b = StageKit.make_label("delivery is not authentication — the riders go because a captain sent them", Vector2(60, 84), 15, Color(0.769, 0.800, 0.886))
	_note_b.visible = false
	add_child(_note_b)
	_note_d = StageKit.make_label("eleven fires = charcoal burners outside the frontier; nothing on the tablet was false", Vector2(60, 84), 15, Color(0.769, 0.800, 0.886))
	_note_d.visible = false
	add_child(_note_d)


func update(local_t: float, _ctx: Dictionary) -> void:
	# Beat a: Simurgh arrives (0.4–3.4) and DELIVERS the packet to Arash
	# (handoff at 3.4–5.0): he walks in, stops before Arash, packet transfers.
	var walk_k := clampf((local_t - 0.4) / 3.0, 0.0, 1.0)
	var sim_x := lerpf(1400.0, 420.0, walk_k)
	_simurgh.position.x = sim_x
	if local_t < 4.2:
		_packet.position = Vector2(sim_x + 70, 430)
	else:
		# Handoff: packet moves from Simurgh to Arash's hand, stays there.
		var h := clampf((local_t - 4.2) / 0.8, 0.0, 1.0)
		_packet.position = Vector2(lerpf(sim_x + 70.0, 290.0, h), lerpf(430.0, 452.0, h))
	_note_b.visible = local_t >= 5.2 and local_t < 12.0
	# Beat b: riders dispatched (5.2–8.0), riding out to the right.
	var ride_k := clampf((local_t - 5.2) / 2.8, 0.0, 1.0)
	for entry in _riders:
		var r: Sprite2D = entry[0]
		r.position.x = entry[1] + 1200.0 * ride_k
		r.visible = ride_k < 1.0
	# Beat c: three village lamps flare (8.6–11.4), one per rooftop.
	for i in 3:
		var lamp: ColorRect = _roofs[i][0]
		var on := 8.6 + i * 0.9
		if local_t >= on and local_t < 14.0:
			var k := minf((local_t - on) / 0.7, 1.0)
			lamp.color = Color(0.91, 0.722, 0.294, 0.9 * k)
		else:
			lamp.color = Color(0.91, 0.722, 0.294, 0.0)
	# Beat d: eleven fires with calm smoke rising (11.4–17).
	for entry in _campfires:
		var fire: Polygon2D = entry[0]
		var smoke: ColorRect = entry[1]
		var fi: float = entry[4]
		if local_t >= 11.4:
			var k := minf((local_t - 11.4) / 1.2, 1.0)
			fire.visible = k > 0.0
			smoke.modulate.a = 0.55 * k * (0.7 + 0.3 * sin(local_t * 0.8 + fi))
		else:
			fire.visible = false
			smoke.modulate.a = 0.0
	_note_d.visible = local_t >= 12.2


func cam_target(local_t: float) -> Dictionary:
	# Beat-driven framing: gate (a/b) -> villages (c) -> camps (d).
	var pos := Vector2(640, 360)
	if local_t < 8.6:
		pos = Vector2(480, 340)
	elif local_t < 11.4:
		pos = Vector2(640, 320)
	else:
		pos = Vector2(640, 380)
	return {"pos": pos, "zoom": 1.0}
