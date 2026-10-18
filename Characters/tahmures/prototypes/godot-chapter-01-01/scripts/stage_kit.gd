class_name StageKit
extends RefCounted
## Static helpers for building deterministic scene graphics.
## Everything here is plain Godot nodes (sprites, polygons, labels) placed in
## world coordinates. World (0,0)-(1280,720) maps 1:1 to screen with the
## default camera (pos 640,360, zoom 1).

const BG_HALL := Color(0.106, 0.118, 0.157)
const BG_HALL_DUSK := Color(0.122, 0.102, 0.141)
const BG_OUTDOOR := Color(0.129, 0.165, 0.208)
const BG_VILLAGE := Color(0.169, 0.145, 0.157)
const BG_CAMPS := Color(0.114, 0.145, 0.188)
const BG_BRIDGE := Color(0.086, 0.106, 0.141)
const BG_SUNRISE := Color(0.196, 0.173, 0.169)
const BG_LEDGER := Color(0.114, 0.114, 0.137)

const PARCHMENT := Color(0.878, 0.831, 0.710)
const PARCHMENT_DARK := Color(0.769, 0.706, 0.580)
const INK := Color(0.165, 0.137, 0.106)
const LAPIS := Color(0.180, 0.337, 0.639)
const CLAY := Color(0.631, 0.431, 0.310)
const GOLD := Color(0.910, 0.722, 0.294)
const SMOKE := Color(0.627, 0.647, 0.710)
const WOOD := Color(0.404, 0.310, 0.227)
const WOOD_DARK := Color(0.294, 0.224, 0.165)
const FLOOR := Color(0.149, 0.157, 0.192)
const RIVER := Color(0.208, 0.322, 0.431)

static func rtl_font() -> SystemFont:
	var sf := SystemFont.new()
	sf.font_names = PackedStringArray(["Noto Naskh Arabic", "Noto Kufi Arabic", "Noto Sans Arabic", "Vazirmatn", "FreeSerif", "DejaVu Sans"])
	return sf


static func latin_font() -> SystemFont:
	var sf := SystemFont.new()
	sf.font_names = PackedStringArray(["DejaVu Sans", "FreeSans", "Liberation Sans"])
	return sf


static func make_label(text: String, pos: Vector2, font_size: int, color: Color = Color(0.91, 0.92, 0.94), rtl: bool = false, outline: int = 4) -> Label:
	var l := Label.new()
	l.text = text
	l.position = pos
	l.add_theme_font_size_override("font_size", font_size)
	l.add_theme_color_override("font_color", color)
	l.add_theme_color_override("font_outline_color", Color(0, 0, 0, 0.65))
	l.add_theme_constant_override("outline_size", outline)
	if rtl:
		l.text_direction = Control.TEXT_DIRECTION_RTL
		l.layout_direction = Control.LAYOUT_DIRECTION_RTL
		l.add_theme_font_override("font", rtl_font())
	return l


static func make_rect(rect: Rect2, color: Color) -> ColorRect:
	var c := ColorRect.new()
	c.position = rect.position
	c.size = rect.size
	c.color = color
	return c


static func make_polygon(points: PackedVector2Array, color: Color) -> Polygon2D:
	var p := Polygon2D.new()
	p.polygon = points
	p.color = color
	return p


static func make_line(p0: Vector2, p1: Vector2, color: Color, width: float = 2.0) -> Line2D:
	var l := Line2D.new()
	l.add_point(p0)
	l.add_point(p1)
	l.default_color = color
	l.width = width
	return l


static func make_sprite(path: String, pos: Vector2, scale: float = 1.0) -> Sprite2D:
	var s := Sprite2D.new()
	s.texture = load(path)
	s.position = pos
	if not is_equal_approx(scale, 1.0):
		s.scale = Vector2(scale, scale)
	return s


## A rounded-feel panel with centered text (screen-space or world-space).
static func make_panel_label(rect: Rect2, text: String, bg: Color, fg: Color, font_size: int, rtl: bool = false) -> Node2D:
	var n := Node2D.new()
	n.add_child(make_rect(rect, bg))
	var lbl := make_label(text, rect.position + Vector2(6, 0), font_size, fg, rtl)
	lbl.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	lbl.position = rect.position
	lbl.custom_minimum_size = Vector2(rect.size.x, 0)
	lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	n.add_child(lbl)
	return n
