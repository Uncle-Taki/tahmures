extends Node2D
## Chapter 01 visual sequence — chapter director (candidate 01).
##
## One deterministic master clock (0..173 s) drives:
##   * 11 scene nodes (pure functions of local time — restart/seek reset all
##     state because nothing accumulates),
##   * the bilingual caption track (data/chapter-cues.json),
##   * the programmatic OST overlay track,
##   * the camera (lerped toward each scene's target pose),
##   * the HUD and optional debug HUD.
##
## Controls:
##   Space  pause / resume          R  restart (full state reset)
##   [ ]    previous / next scene   L  toggle en / fa
##   Q E    step -0.5 s / +0.5 s    D  toggle debug HUD          Esc  quit
##
## User args:  --language=en|fa  --seek=<t>  --mouth-proxy=off|open_test
##             (movie maker: --write-movie <out> --fixed-fps 30 --quit-after 5190)
##
## Silent-animatic is the default. If owner audio is later placed at
## audio/<lang>/narration.wav it is attached and played in sync with t.
## Mouth: neutral for all spoken cues unless --mouth-proxy=open_test
## (two-state PROXY only — explicitly not lip-sync).

const SCENE_SCRIPTS := {
	"CH01-S01": "res://scripts/stage/scene_ch01_s01.gd",
	"CH01-S02": "res://scripts/stage/scene_ch01_s02.gd",
	"CH01-S03": "res://scripts/stage/scene_ch01_s03.gd",
	"CH01-S04": "res://scripts/stage/scene_ch01_s04.gd",
	"CH01-S05": "res://scripts/stage/scene_ch01_s05.gd",
	"CH01-S06": "res://scripts/stage/scene_ch01_s06.gd",
	"CH01-S07": "res://scripts/stage/scene_ch01_s07.gd",
	"CH01-S08": "res://scripts/stage/scene_ch01_s08.gd",
	"CH01-S09": "res://scripts/stage/scene_ch01_s09.gd",
	"CH01-S10": "res://scripts/stage/scene_ch01_s10.gd",
	"CH01-S11": "res://scripts/stage/scene_ch01_s11.gd",
}
const SCENE_IDS := ["CH01-S01", "CH01-S02", "CH01-S03", "CH01-S04", "CH01-S05",
	"CH01-S06", "CH01-S07", "CH01-S08", "CH01-S09", "CH01-S10", "CH01-S11"]

var timeline: Timeline
var t := 0.0
var paused := false
var at_end := false
var language := "en"
var mouth_proxy := false
var _current_scene := -1
var _scene_nodes: Dictionary = {}
var _world: Node2D
var _camera: Camera2D
var _bg: ColorRect
var _captions: CaptionLayer
var _ost: OstLayer
var _hud_title: Label
var _hud_sub: Label
var _hud_scene: Label
var _hud_time: Label
var _hud_lang: Label
var _hud_hint: Label
var _bar_fill: ColorRect
var _hud_animatic: Label
var _debug_layer: CanvasLayer
var _debug_labels: Array = []
var _audio: AudioStreamPlayer
var _seek_requested := -1.0


func _ready() -> void:
	timeline = Timeline.new()
	if not timeline.load_plan():
		push_error("Chapter cue plan failed to load:")
		for e in timeline.errors:
			push_error("  - " + e)
		get_tree().quit(1)
		return
	_apply_user_args()
	_build_tree()
	if _seek_requested >= 0.0:
		jump_to(timeline.clamp_time(_seek_requested), true)
	set_language(language)
	# Fail clearly on an unsupported language configuration.
	if language != "en" and language != "fa":
		push_error("Unsupported language '%s' — only en and fa are provided." % language)
		get_tree().quit(1)
		return
	_try_attach_audio()


func _apply_user_args() -> void:
	for a in OS.get_cmdline_user_args():
		var kv := a.split("=")
		if kv.size() != 2:
			continue
		match kv[0].trim_prefix("--"):
			"language":
				language = kv[1]
			"seek":
				_seek_requested = float(kv[1])
			"mouth-proxy":
				mouth_proxy = kv[1] == "open_test"


func _build_tree() -> void:
	# Background (screen-space, behind everything).
	var bg_layer := CanvasLayer.new()
	bg_layer.layer = -100
	add_child(bg_layer)
	_bg = ColorRect.new()
	_bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg_layer.add_child(_bg)
	# World: scenes + camera.
	_world = Node2D.new()
	_world.name = "World"
	add_child(_world)
	_camera = Camera2D.new()
	_camera.position = Vector2(640, 360)
	_world.add_child(_camera)
	# One scene node per planned shot; only the active one is visible/updated.
	for id in SCENE_IDS:
		var script: GDScript = load(SCENE_SCRIPTS[id])
		var node: Node2D = script.new()
		node.name = id
		_world.add_child(node)
		_scene_nodes[id] = node
	# Text and overlay layers.
	_captions = CaptionLayer.new()
	add_child(_captions)
	_ost = OstLayer.new()
	add_child(_ost)
	# HUD.
	var hud := CanvasLayer.new()
	hud.layer = 50
	add_child(hud)
	_hud_title = _hud_label(hud, Vector2(16, 6), 18, Color(0.91, 0.92, 0.94))
	_hud_title.text = "TAHMURES — CHAPTER 01 · THE THREE READINGS · سه خوانش"
	_hud_sub = _hud_label(hud, Vector2(16, 28), 13, Color(0.769, 0.800, 0.886))
	_hud_sub.text = "PROVISIONAL ANIMATIC — temporary art, NOT approved character art · silent animatic — no narration"
	_hud_scene = _hud_label(hud, Vector2(16, 52), 15, Color(0.91, 0.92, 0.94))
	_hud_time = _hud_label(hud, Vector2(430, 52), 15, Color(0.91, 0.92, 0.94))
	_hud_lang = _hud_label(hud, Vector2(620, 52), 15, Color(0.769, 0.800, 0.886))
	_hud_hint = _hud_label(hud, Vector2(16, 70), 12, Color(0.60, 0.64, 0.72))
	_hud_hint.text = "Space pause · [ ] scene · L language · Q/E step · R restart · D debug"
	_bar_fill = ColorRect.new()
	_bar_fill.position = Vector2(16, 88)
	_bar_fill.size = Vector2(0, 4)
	_bar_fill.color = Color(0.91, 0.722, 0.294)
	hud.add_child(_bar_fill)
	var bar_track := ColorRect.new()
	bar_track.position = Vector2(16, 88)
	bar_track.size = Vector2(400, 4)
	bar_track.color = Color(0.165, 0.188, 0.251)
	hud.add_child(bar_track)
	_hud_animatic = _hud_label(hud, Vector2(760, 690), 12, Color(0.769, 0.800, 0.886))
	_hud_animatic.text = "ANIMATIC CANDIDATE 01 — visual sequence only; pending owner art/voice decisions"
	# Debug HUD (toggled with D; never part of the production frame).
	_debug_layer = CanvasLayer.new()
	_debug_layer.layer = 60
	_debug_layer.visible = false
	add_child(_debug_layer)
	for i in 6:
		var l := _hud_label(_debug_layer, Vector2(860, 12 + i * 18), 12, Color(0.769, 0.800, 0.886))
		_debug_labels.append(l)
	# Audio route (inert until owner narration exists).
	_audio = AudioStreamPlayer.new()
	add_child(_audio)


func _hud_label(parent: Node, pos: Vector2, size: int, color: Color) -> Label:
	var l := StageKit.make_label("", pos, size, color)
	parent.add_child(l)
	return l


func set_language(lang: String) -> void:
	language = lang
	_captions.set_language(lang, timeline.speaker_names)
	_ost.set_language(lang)
	if _scene_nodes.has("CH01-S09"):
		_scene_nodes["CH01-S09"].set_language(lang)
	_hud_lang.text = "lang=%s" % lang
	_try_attach_audio()


func _try_attach_audio() -> void:
	# Silent-animatic is the default; owner audio is attached ONLY when a
	# real recording exists at the contract path (see audio/<lang>/README.md).
	var path := "res://audio/%s/narration.wav" % language
	if FileAccess.file_exists(path):
		var stream: AudioStream = load(path)
		_audio.stream = stream
		if t > 0.0 and t < stream.get_length():
			_audio.play(t)
		else:
			_audio.stop()
	else:
		_audio.stop()
		_audio.stream = null


func _process(delta: float) -> void:
	if not paused and not at_end:
		t += delta
		if t >= timeline.total_seconds:
			t = timeline.total_seconds
			at_end = true
		if _audio.playing and _audio.stream != null:
			# Keep audio glued to the master clock (drift-safe).
			if absf(_audio.get_playback_position() - t) > 0.25:
				_audio.play(t)
	var scene_idx := timeline.scene_index_at(t)
	var scene_id: String = timeline.scenes[scene_idx].get("id")
	if scene_idx != _current_scene:
		_current_scene = scene_idx
		_activate_scene(scene_id)
	var node: Node2D = _scene_nodes[scene_id]
	var local_t := t - _scene_start_of(scene_id)
	# Keep the master clock on every Tahmures rig (deterministic blinks).
	for rig in get_tree().get_nodes_in_group("tahmures_rig"):
		rig.set_time(t)
	node.update(local_t, {})
	# OST and captions.
	_ost.show_osts(timeline.osts_at(t))
	_captions.show_cues(timeline.cues_at(t))
	# Mouth proxy: two-state only (open_test while a non-narrator cue is
	# active AND the proxy was explicitly enabled). NEVER lip-sync.
	var speaking := false
	for c in timeline.cues_at(t):
		if c.get("speaker") != "narrator":
			speaking = true
	_set_rig_mouth(speaking)
	# Camera: lerp toward the active scene's target pose (seek snaps).
	var target: Dictionary = node.cam_target(local_t)
	var kp := 1.0 - pow(0.001, delta / 1.0)
	if _seek_requested >= 0.0:
		_camera.position = Vector2(target.get("pos"))
		_zoom_to(target)
		_seek_requested = -1.0
	else:
		_camera.position = _camera.position.lerp(Vector2(target.get("pos")), kp)
		_zoom_to(target, kp)
	# HUD.
	_hud_scene.text = "%s · beat %s" % [scene_id, String(timeline.scenes[scene_idx].get("beat", ""))]
	_hud_time.text = "%06.2f / %06.2f" % [t, timeline.total_seconds]
	_bar_fill.size.x = 400.0 * (t / timeline.total_seconds)
	if at_end:
		_hud_hint.text = "END — press R to restart"
	_update_debug(scene_id, local_t)


func _zoom_to(target: Dictionary, kp: float = 1.0) -> void:
	var z: float = float(target.get("zoom", 1.0))
	_camera.zoom = _camera.zoom.lerp(Vector2(z, z), kp)


func _scene_start_of(scene_id: String) -> float:
	for s in timeline.scenes:
		if s.get("id") == scene_id:
			return float(s.get("start"))
	return 0.0


func _activate_scene(scene_id: String) -> void:
	for id in SCENE_IDS:
		_scene_nodes[id].visible = (id == scene_id)
	var node: Node2D = _scene_nodes[scene_id]
	var local_t := t - _scene_start_of(scene_id)
	node.enter(local_t, {})
	_bg.color = node.bg_color

func _set_rig_mouth(speaking: bool) -> void:
	for rig in get_tree().get_nodes_in_group("tahmures_rig"):
		rig.mouth_proxy_enabled = mouth_proxy
		rig.set_mouth("open_test" if (speaking and mouth_proxy) else "neutral")


func _update_debug(scene_id: String, local_t: float) -> void:
	if not _debug_layer.visible:
		return
	var cues := timeline.cues_at(t)
	var osts := timeline.osts_at(t)
	var rig_state := ""
	for rig in get_tree().get_nodes_in_group("tahmures_rig"):
		if rig.get_parent() != null and rig.get_parent().visible:
			var mouth_now := "open_test" if (mouth_proxy and speaking_now()) else "neutral"
			rig_state = "state=%s mouth=%s" % [rig._state, mouth_now]
	_debug_labels[0].text = "scene=%s local_t=%.2f" % [scene_id, local_t]
	_debug_labels[1].text = "cues=[%s] ost=[%s]" % [_ids(cues, "id"), _ids(osts, "id")]
	_debug_labels[2].text = rig_state if rig_state != "" else "rig=hidden"
	_debug_labels[3].text = "head=approved front-view prototype (scope-limited) | bodies/actors=TEMPORARY placeholders"
	_debug_labels[4].text = "audio=%s" % ("pending owner narration (silent animatic)" if _audio.stream == null else "owner narration attached")
	_debug_labels[5].text = "lang=%s mouth_proxy=%s paused=%s" % [language, str(mouth_proxy), str(paused)]


func speaking_now() -> bool:
	for c in timeline.cues_at(t):
		if c.get("speaker") != "narrator":
			return true
	return false


func _ids(items: Array, key: String) -> String:
	var out: Array = []
	for i in items:
		out.append(String(i.get(key, "?")))
	return ", ".join(out)


func jump_to(new_t: float, _snap: bool = true) -> void:
	t = timeline.clamp_time(new_t)
	at_end = t >= timeline.total_seconds
	_current_scene = -1  # force re-entry → full scene state reset
	var idx := timeline.scene_index_at(t)
	_camera.position = Vector2(_scene_nodes[String(timeline.scenes[idx].get("id"))].cam_target(0.0).get("pos", Vector2(640, 360)))
	_camera.zoom = Vector2.ONE
	_captions.clear()
	_ost.clear()
	if _audio.stream != null:
		if t < _audio.stream.get_length():
			_audio.play(t)
		else:
			_audio.stop()


func restart() -> void:
	paused = false
	jump_to(0.0, true)


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_SPACE:
				if not at_end:
					paused = not paused
			KEY_R:
				restart()
			KEY_L:
				set_language("fa" if language == "en" else "en")
			KEY_D:
				_debug_layer.visible = not _debug_layer.visible
			KEY_ESCAPE:
				get_tree().quit()
			KEY_Q:
				jump_to(t - 0.5, false)
			KEY_E:
				jump_to(t + 0.5, false)
			KEY_BRACKETLEFT:
				jump_to(_scene_start_of(SCENE_IDS[maxi(0, _current_scene - 1)]), true)
			KEY_BRACKETRIGHT:
				jump_to(_scene_start_of(SCENE_IDS[mini(SCENE_IDS.size() - 1, _current_scene + 1)]), true)
