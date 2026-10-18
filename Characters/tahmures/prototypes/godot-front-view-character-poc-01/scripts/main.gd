extends Node2D
## GODOT_FRONT_VIEW_CHARACTER_POC_01 — stage A main scene controller.
##
## Drives one deterministic, repeatable 18-second front-view preview
## timeline (AnimationPlayer library "preview", animation
## "preview_master") that exercises the human-approved facial-state
## head components and a clearly-labelled temporary pointing beat.
##
## Determinism: every visible event comes from the AnimationPlayer
## track keyframes in scenes/main.tscn. This script only reads the
## animation position, updates the HUD, and handles replay/language.
## The same visual timeline is used for every language; only the
## narration track (a later stage) will differ.
##
## Language hook: run the project with a user argument, e.g.
##   godot --path <project> -- --language=fa
## or set the project setting tahmures/language (see project.godot).
## Stage A has no narration audio; the hook only selects the future
## audio/caption track and updates the HUD line.

const TIMELINE_LENGTH := 18.0
const ANIMATION_NAME := "preview/preview_master"
const AudioSubtitlePipeline = preload("res://scripts/audio_subtitle_pipeline.gd")
const CAPTION_FIXTURE_PATHS := {
	"en": "res://scripts/tests/fixtures/en-caption.vtt",
	"fa": "res://scripts/tests/fixtures/fa-caption.vtt",
}

## Single source of truth for readable state markers. The animation
## keyframe times below must match the track times in main.tscn.
## "label" is the compact on-screen HUD text (bounded width, left
## control column); "detail" is the long explanation printed to the
## console only (stage-A layout revision: long strings stay off-screen).
const BEATS: Array = [
	{"t": 0.0, "id": "idle", "label": "IDLE", "detail": "neutral idle — approved base state"},
	{"t": 2.5, "id": "blink", "label": "BLINK", "detail": "blink — approved closed-eyelid state"},
	{"t": 2.85, "id": "idle_after_blink", "label": "IDLE", "detail": "blink ended — neutral idle"},
	{"t": 5.0, "id": "thinking", "label": "THINKING", "detail": "thinking — approved brow state (1 px raise + underlay)"},
	{"t": 8.0, "id": "neutral_pause", "label": "IDLE", "detail": "thinking ended — neutral"},
	{"t": 9.0, "id": "point_raise", "label": "POINT", "detail": "point raise — temporary arm (shoulder -6 deg -> -80 deg, 0.8 s)"},
	{"t": 10.5, "id": "point_hold", "label": "POINT", "detail": "point hold — temporary arm raised, mark visible"},
	{"t": 10.8, "id": "point_open_mouth", "label": "POINT + OPEN TEST", "detail": "point + open mouth — approved open-test state (NOT speech / lip-sync)"},
	{"t": 12.2, "id": "point_hold_2", "label": "POINT", "detail": "mouth back to neutral — arm still raised"},
	{"t": 13.0, "id": "return", "label": "RETURN", "detail": "return to neutral — arm lowers (13.0-13.8), mark fades (13.4-14.0)"},
	{"t": 14.0, "id": "idle_end", "label": "IDLE", "detail": "neutral idle to end of loop"},
]

## Progress bar lives in the left control column (x 16..426), below the
## hint line and above the tick labels; it must never enter the character
## zone (x >= 465) or the bottom-centre torso area.
const BAR_X := 16.0
const BAR_Y := 662.0
const BAR_W := 410.0
const BAR_H := 12.0
const TICK_LABEL_Y_OFFSET := 19.0

var language := "en"
var caption_test_mode := false
var _last_beat_id := ""
var _last_printed_beat_id := ""

@onready var anim: AnimationPlayer = $AnimationPlayer
@onready var camera: Camera2D = $World/Camera2D
@onready var state_label: Label = $HUD/StateLabel
@onready var time_label: Label = $HUD/TimeLabel
@onready var bar_fill: ColorRect = $HUD/BarFill
@onready var language_label: Label = $HUD/LanguageLine
@onready var hud: CanvasLayer = $HUD
@onready var narration_player: AudioStreamPlayer = $NarrationPlayer


func _ready() -> void:
	_detect_language()
	camera.make_current()
	_build_bar_markers()
	language_label.text = "language: %s · narration: none (stage A)" % language.to_upper()
	var audio_inputs: Dictionary = AudioSubtitlePipeline.inspect_language_inputs(language)
	if audio_inputs.get("status", "") == "pending":
		print("narration inputs: pending")
		for missing_path in audio_inputs.get("missing", []):
			print("missing narration input: %s" % missing_path)
	else:
		print("narration input status: %s%s" % [
			audio_inputs.get("status", "invalid"),
			" — " + str(audio_inputs.get("error", "")) if audio_inputs.has("error") else "",
		])
	# The node is an inert integration point only. Stage B0 never loads or plays audio.
	narration_player.stream = null
	narration_player.autoplay = false
	anim.play(ANIMATION_NAME)
	caption_test_mode = OS.get_cmdline_user_args().has("--caption-test")
	if caption_test_mode:
		_show_caption_test()
	print("GODOT_FRONT_VIEW_CHARACTER_POC_01 — stage A visual rig")
	print("godot version: %s" % Engine.get_version_info()["string"])
	print("language: %s (visual timeline identical for en/fa)" % language)
	print("timeline: %s, length %.1f s, %d beats, auto-loop" % [ANIMATION_NAME, TIMELINE_LENGTH, BEATS.size()])
	print("viewport: %s" % get_viewport_rect().size)


func _process(_delta: float) -> void:
	var pos := 0.0
	if anim.is_playing():
		pos = anim.current_animation_position
	var beat: Dictionary = _beat_at(pos)
	if String(beat["id"]) != _last_beat_id:
		_last_beat_id = String(beat["id"])
		state_label.text = String(beat["label"])
		if _last_beat_id != _last_printed_beat_id:
			_last_printed_beat_id = _last_beat_id
			print("BEAT t=%.2f -> %s (%s)" % [pos, beat["label"], beat["detail"]])
	time_label.text = "t = %05.2f / %05.2f s" % [pos, TIMELINE_LENGTH]
	bar_fill.size.x = BAR_W * clamp(pos / TIMELINE_LENGTH, 0.0, 1.0)


func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.physical_keycode == KEY_R:
			replay()


## Replay the timeline from t=0 (also reachable by just waiting for the
## auto-loop, or by re-running the scene in the editor with F6/F5).
func replay() -> void:
	anim.stop()
	anim.play(ANIMATION_NAME)
	_last_beat_id = ""
	_last_printed_beat_id = ""
	print("TIMELINE REPLAYED")


func _beat_at(pos: float) -> Dictionary:
	var current: Dictionary = BEATS[0]
	for beat in BEATS:
		if float(beat["t"]) <= pos + 1e-6:
			current = beat
		else:
			break
	return current


func _detect_language() -> void:
	if ProjectSettings.has_setting("tahmures/language"):
		var setting_value := str(ProjectSettings.get_setting("tahmures/language"))
		if setting_value == "en" or setting_value == "fa":
			language = setting_value
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--language="):
			var value := arg.substr("--language=".length())
			if value == "en" or value == "fa":
				language = value
			else:
				push_warning("unknown language %r, expected en or fa" % value)


## Test-only bilingual caption presentation. Fixture lines are a shaping and
## layout test, not owner-approved narration. No audio or mouth motion is used.
func _show_caption_test() -> void:
	hud.visible = false
	var fixture_path := String(CAPTION_FIXTURE_PATHS[language])
	var source := FileAccess.get_file_as_string(fixture_path)
	var parsed: Dictionary = AudioSubtitlePipeline.parse_webvtt(source)
	if not parsed.ok:
		push_error("caption test fixture is invalid: %s" % parsed.error)
		return
	var layer := CanvasLayer.new()
	layer.name = "CaptionTestLayer"
	layer.layer = 110
	add_child(layer)
	var panel := Panel.new()
	panel.name = "CaptionTestPanel"
	panel.anchor_left = 0.05
	panel.anchor_right = 0.95
	panel.anchor_top = 0.72
	panel.anchor_bottom = 0.96
	var panel_style := StyleBoxFlat.new()
	panel_style.bg_color = Color(0.035, 0.045, 0.07, 0.96)
	panel_style.border_color = Color(0.9098, 0.7216, 0.2941, 1.0)
	panel_style.set_border_width_all(2)
	panel_style.set_corner_radius_all(10)
	panel.add_theme_stylebox_override("panel", panel_style)
	layer.add_child(panel)
	var caption := Label.new()
	caption.name = "CaptionFixture"
	caption.anchor_left = 0.035
	caption.anchor_right = 0.965
	caption.anchor_top = 0.08
	caption.anchor_bottom = 0.68
	caption.text = String(parsed.cues[0].text)
	caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	caption.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	caption.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	caption.add_theme_font_size_override("font_size", 30)
	caption.add_theme_color_override("font_color", Color(0.96, 0.96, 0.98, 1))
	if language == "fa":
		caption.text_direction = Control.TEXT_DIRECTION_RTL
		caption.layout_direction = Control.LAYOUT_DIRECTION_RTL
		var persian_font := SystemFont.new()
		persian_font.font_names = PackedStringArray(["Noto Naskh Arabic", "Noto Kufi Arabic", "Vazirmatn", "FreeSerif", "DejaVu Sans"])
		caption.add_theme_font_override("font", persian_font)
	panel.add_child(caption)
	var notice := Label.new()
	notice.name = "NotApprovedNotice"
	notice.anchor_left = 0.035
	notice.anchor_right = 0.965
	notice.anchor_top = 0.70
	notice.anchor_bottom = 0.94
	notice.text = "RTL / SUBTITLE LAYOUT TEST — NOT OWNER-APPROVED NARRATION"
	notice.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	notice.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	notice.add_theme_font_size_override("font_size", 15)
	notice.add_theme_color_override("font_color", Color(0.9098, 0.7216, 0.2941, 1))
	panel.add_child(notice)
	print("CAPTION_TEST_ONLY: %s fixture; no narration audio or speech motion" % language)


## Progress-bar tick marks and labels for the main beats so the current
## position and the upcoming events are readable while watching. Ticks
## straddle the bar; the small text labels sit below the bar, inside the
## left control column (stage-A layout revision).
func _build_bar_markers() -> void:
	for beat in BEATS:
		var x := BAR_X + BAR_W * float(beat["t"]) / TIMELINE_LENGTH
		var tick := ColorRect.new()
		tick.color = Color(0.533, 0.573, 0.671, 0.9)
		tick.position = Vector2(x - 1.0, BAR_Y - 5.0)
		tick.size = Vector2(2.0, BAR_H + 10.0)
		tick.mouse_filter = Control.MOUSE_FILTER_IGNORE
		hud.add_child(tick)
	var labelled := {
		"blink": "blink",
		"thinking": "think",
		"point_raise": "point",
		"point_open_mouth": "open",
		"return": "back",
	}
	var settings := LabelSettings.new()
	settings.font_size = 10
	settings.font_color = Color(0.533, 0.573, 0.673, 1)
	settings.outline_size = 3
	settings.outline_color = Color(0, 0, 0, 0.65)
	for beat in BEATS:
		var beat_id := String(beat["id"])
		if labelled.has(beat_id):
			var x := BAR_X + BAR_W * float(beat["t"]) / TIMELINE_LENGTH
			var label := Label.new()
			label.text = String(labelled[beat_id])
			label.label_settings = settings
			label.position = Vector2(x - 20.0, BAR_Y + TICK_LABEL_Y_OFFSET)
			label.size = Vector2(40.0, 16.0)
			label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			label.mouse_filter = Control.MOUSE_FILTER_IGNORE
			hud.add_child(label)
