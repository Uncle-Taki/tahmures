class_name OstLayer
extends CanvasLayer
## Programmatic on-screen text (OST) overlays from the cue plan.
## All text is rendered as Godot labels (shaping-aware, RTL for FA) — no
## pre-baked lettering in any sprite. Kinds and their placement:
##   title        top-centre chapter/scene title card
##   tablet       parchment panel, the tablet's exact sentence (S02, S08)
##   panel_label  one of three equal third-panels (S04, S08)
##   label_tick   one of four equal chips in a row (S07)
##   formula      centre line, the exact eight-term formula (S09)
##   review_line  centre line under the formula (S09)
##   ledger_line  centre line over the ledger (S11)
##   takeaway     upper-centre episode takeaway (S11)

const TABLET_RECT := Rect2(190, 120, 900, 92)
const PANEL_YS := 236.0
const PANEL_W := 300.0
const PANEL_CENTERS := [Vector2(213.0, 0), Vector2(640.0, 0), Vector2(1067.0, 0)]
const CHIP_CENTERS := [Vector2(180.0, 430), Vector2(460.0, 430), Vector2(740.0, 430), Vector2(1020.0, 430)]
const CHIP_W := 240.0

var _holder: Node2D
var _lang := "en"
var _rtl_font: SystemFont


func _ready() -> void:
	layer = 30
	_holder = Node2D.new()
	_holder.name = "OstHolder"
	add_child(_holder)
	_rtl_font = SystemFont.new()
	_rtl_font.font_names = PackedStringArray(["Noto Naskh Arabic", "Noto Kufi Arabic", "Noto Sans Arabic", "Vazirmatn", "FreeSerif", "DejaVu Sans"])


func set_language(lang: String) -> void:
	_lang = lang


func _clear() -> void:
	for child in _holder.get_children():
		_holder.remove_child(child)
		child.queue_free()


func _text_label(text: String, size: int, color: Color) -> Label:
	var l := StageKit.make_label(text, Vector2.ZERO, size, color, _lang == "fa")
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	return l


## Index of an OST within its (scene, kind) sequence, derived from the cue ID
## suffix (OST-S04-2 -> 2). The active set at a given time holds at most one
## same-kind OST, so the position must come from the ID, not the active count.
func _slot_index(o: Dictionary) -> int:
	var id: String = String(o.get("id", ""))
	var parts: PackedStringArray = id.split("-")
	var last: String = parts[parts.size() - 1]
	return int(last) if last.is_valid_int() else 0


## osts_now: active OST dicts at t.
func show_osts(osts_now: Array) -> void:
	_clear()
	for o in osts_now:
		var kind: String = String(o.get("kind", ""))
		var text: String = String(o.get("fa" if _lang == "fa" else "en", ""))
		match kind:
			"title":
				var lbl := _text_label(text, 34, Color(0.965, 0.949, 0.902))
				lbl.position = Vector2(190, 96)
				lbl.custom_minimum_size = Vector2(900, 0)
				_holder.add_child(lbl)
			"tablet":
				_holder.add_child(StageKit.make_rect(TABLET_RECT, StageKit.PARCHMENT))
				var lbl := _text_label(text, 25, StageKit.INK)
				lbl.position = TABLET_RECT.position + Vector2(10, 0)
				lbl.custom_minimum_size = Vector2(TABLET_RECT.size.x - 20, 0)
				lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
				_holder.add_child(lbl)
			"panel_label":
				var cx: float = PANEL_CENTERS[mini(_slot_index(o) - 1, 2)].x
				var rect := Rect2(cx - PANEL_W / 2.0, PANEL_YS, PANEL_W, 64)
				_holder.add_child(StageKit.make_rect(rect, Color(0.0, 0.0, 0.0, 0.55)))
				var lbl := _text_label(text, 22, Color(0.925, 0.933, 0.949))
				lbl.position = rect.position + Vector2(8, 0)
				lbl.custom_minimum_size = Vector2(PANEL_W - 16, 0)
				lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
				_holder.add_child(lbl)
			"label_tick":
				var c: Vector2 = CHIP_CENTERS[mini(_slot_index(o) - 1, 3)]
				var rect := Rect2(c.x - CHIP_W / 2.0, c.y, CHIP_W, 56)
				var is_known: bool = not text.strip_edges().ends_with("?") and not text.strip_edges().ends_with("؟")
				_holder.add_child(StageKit.make_rect(rect, Color(0.0, 0.0, 0.0, 0.55) if not is_known else Color(0.180, 0.337, 0.639, 0.85)))
				var lbl := _text_label(text, 21, Color(0.925, 0.933, 0.949))
				lbl.position = rect.position + Vector2(8, 0)
				lbl.custom_minimum_size = Vector2(CHIP_W - 16, 0)
				lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
				_holder.add_child(lbl)
			"formula":
				var lbl := _text_label(text, 20, Color(0.878, 0.831, 0.710))
				lbl.position = Vector2(40, 452)
				lbl.custom_minimum_size = Vector2(1200, 0)
				_holder.add_child(lbl)
			"review_line":
				var lbl := _text_label(text, 20, Color(0.769, 0.800, 0.886))
				lbl.position = Vector2(40, 516)
				lbl.custom_minimum_size = Vector2(1200, 0)
				_holder.add_child(lbl)
			"ledger_line":
				var lbl := _text_label(text, 21, Color(0.925, 0.933, 0.949))
				lbl.position = Vector2(140, 428)
				lbl.custom_minimum_size = Vector2(1000, 0)
				_holder.add_child(lbl)
			"takeaway":
				var lbl := _text_label(text, 30, Color(0.965, 0.949, 0.902))
				lbl.position = Vector2(140, 150)
				lbl.custom_minimum_size = Vector2(1000, 0)
				_holder.add_child(lbl)
			_:
				pass


func clear() -> void:
	_clear()
