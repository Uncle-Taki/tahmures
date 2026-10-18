class_name CaptionLayer
extends CanvasLayer
## Bottom caption panel driven by the cue plan (dialogue + narration).
## One semantic timeline; EN/FA string separation lives in chapter-cues.json.
## Dialogue cues are prefixed with the speaker's name (per language); narrator
## cues are plain. FA captions use RTL direction with an Arabic shaping font.
## This layer shows no text outside a cue's [start, end) bounds.

const PANEL_RECT := Rect2(90, 560, 1100, 140)

var _panel: Panel
var _label: Label
var _rtl_font: SystemFont
var _speaker_names: Dictionary = {}
var _lang := "en"


func _ready() -> void:
	layer = 20
	_panel = Panel.new()
	_panel.position = PANEL_RECT.position
	_panel.size = PANEL_RECT.size
	_panel.self_modulate = Color(0, 0, 0, 0.55)
	add_child(_panel)
	_label = Label.new()
	_label.position = Vector2(PANEL_RECT.position.x + 16, PANEL_RECT.position.y + 18)
	_label.custom_minimum_size = Vector2(PANEL_RECT.size.x - 32, 0)
	_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_label.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_label.add_theme_font_size_override("font_size", 24)
	_label.add_theme_color_override("font_color", Color(0.925, 0.933, 0.949))
	_label.add_theme_color_override("font_outline_color", Color(0, 0, 0, 0.65))
	_label.add_theme_constant_override("outline_size", 5)
	_rtl_font = StageKit.rtl_font()
	add_child(_label)
	_set_language("en")


func set_language(lang: String, speaker_names: Dictionary) -> void:
	_speaker_names = speaker_names
	_set_language(lang)


func _set_language(lang: String) -> void:
	_lang = lang
	if lang == "fa":
		_label.text_direction = Control.TEXT_DIRECTION_RTL
		_label.layout_direction = Control.LAYOUT_DIRECTION_RTL
		_label.add_theme_font_override("font", _rtl_font)
	else:
		_label.text_direction = Control.TEXT_DIRECTION_AUTO
		_label.layout_direction = Control.LAYOUT_DIRECTION_LTR
		_label.add_theme_font_override("font", StageKit.latin_font())


## cues_now: array of cue dicts active at t (at most one by construction).
func show_cues(cues_now: Array) -> void:
	if cues_now.is_empty():
		_label.text = ""
		return
	var c: Dictionary = cues_now[0]
	var text: String = String(c.get("fa" if _lang == "fa" else "en", ""))
	var sp: String = String(c.get("speaker", "narrator"))
	if sp != "narrator" and _speaker_names.has(sp):
		var name: String = String(_speaker_names[sp].get(_lang, ""))
		if not name.is_empty():
			text = name + ": " + text
	_label.text = text


func clear() -> void:
	_label.text = ""
