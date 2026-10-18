class_name TahmuresRig
extends Node2D
## Repaired reusable Tahmures puppet rig for godot-character-library-recovery-01.
##
## Preserves the 17 human-approved front-view head layers (layout01-v7 +
## layout01-facial-states-01) byte-for-byte in their exact draw order and
## source canvas coordinates (1086x1448).
##
## FIX FOR GLM DEFECT #3:
## In GLM's godot-chapter-01-01/scripts/tahmures_rig.gd (lines 149-151),
## set_state("thinking") shifted BOTH _brow_l and _brow_r by Vector2(0, -1).
## The accepted POC and human approval contract specify moving ONLY
## eyebrow_left (anatomical left = viewer right) by Vector2(0, -1) over
## thinking_brow_underlay (x=552..613, y=106..138). This script keeps
## _brow_r at Vector2.ZERO at all times.

signal blink_started
signal blink_ended

const HEAD_LAYER_ORDER := [
	"hair_back", "head_base", "thinking_brow_underlay", "ear_right", "ear_left",
	"beard", "lower_face_neutral", "lower_face_open_test", "nose", "eye_right",
	"eye_left", "eye_right_closed", "eye_left_closed", "eyebrow_right",
	"eyebrow_left", "moustache", "diadem_gold",
]
const HIDDEN_BY_DEFAULT := [
	"thinking_brow_underlay", "lower_face_open_test",
	"eye_right_closed", "eye_left_closed",
]

@export var head_asset_dir: String = "res://assets/approved-head"
@export var body_asset_dir: String = "res://characters/tahmures/layers"
@export var use_source_pose_body: bool = false
@export var use_temporary_point_arm: bool = false

var head: Node2D
var body_root: Node2D
var arm_root: Node2D
var mouth_proxy_enabled := false
var time := 0.0
var _state := "neutral"
var _blink_on := false
var _sp: Dictionary = {}
var _brow_l: Sprite2D
var _brow_r: Sprite2D


func _ready() -> void:
	add_to_group("tahmures_rig")
	_build_body()
	_build_head()
	if use_temporary_point_arm:
		_build_temporary_arm()


func _require_texture(path: String) -> Texture2D:
	if not ResourceLoader.exists(path):
		push_error("CRITICAL: Missing required Tahmures texture '%s'. Stand-in fallback is forbidden." % path)
		if get_tree() != null:
			get_tree().quit(1)
		return null
	return load(path)


func _build_body() -> void:
	body_root = Node2D.new()
	body_root.name = "BodyRoot"
	body_root.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	add_child(body_root)
	if not use_source_pose_body:
		return
	var body_layers := [
		"feet_and_boots",
		"outer_robe_and_sash",
		"neck_and_medallion_chest",
		"arm_right_viewer_left",
		"arm_left_viewer_right",
	]
	for layer_name in body_layers:
		var path := "%s/%s.png" % [body_asset_dir, layer_name]
		if ResourceLoader.exists(path):
			var spr := Sprite2D.new()
			spr.name = layer_name
			spr.centered = false
			spr.texture = _require_texture(path)
			spr.add_to_group("candidate_source_body_layer")
			body_root.add_child(spr)


func _build_head() -> void:
	head = Node2D.new()
	head.name = "Head"
	head.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	add_child(head)
	for layer in HEAD_LAYER_ORDER:
		var tex_path := "%s/%s.png" % [head_asset_dir, layer]
		var spr := Sprite2D.new()
		spr.name = layer
		spr.centered = false
		spr.texture = _require_texture(tex_path)
		spr.add_to_group("approved_head_component")
		if layer in HIDDEN_BY_DEFAULT:
			spr.visible = false
		head.add_child(spr)
		_sp[layer] = spr
	_brow_l = _sp["eyebrow_left"]
	_brow_r = _sp["eyebrow_right"]


func _build_temporary_arm() -> void:
	arm_root = Node2D.new()
	arm_root.name = "TemporaryPointArm"
	arm_root.add_to_group("temporary_placeholder")
	add_child(arm_root)


func set_time(t: float) -> void:
	time = t
	if _state == "thinking":
		if _blink_on:
			_set_blink(false)
		return
	var phase := fposmod(t, 3.7)
	var on: bool = t > 1.0 and phase >= 3.0 and phase < 3.35
	if on != _blink_on:
		_set_blink(on)


func _set_blink(on: bool) -> void:
	_blink_on = on
	_sp["eye_left"].visible = not on
	_sp["eye_right"].visible = not on
	_sp["eye_left_closed"].visible = on
	_sp["eye_right_closed"].visible = on
	if on:
		blink_started.emit()
	else:
		blink_ended.emit()


func set_state(s: String) -> void:
	if s != "neutral" and s != "thinking":
		s = "neutral"
	_state = s
	var thinking: bool = (s == "thinking")
	_sp["thinking_brow_underlay"].visible = thinking
	# Approved contract: ONLY anatomical-left brow shifts by (0, -1).
	_brow_l.position = Vector2(0, -1) if thinking else Vector2.ZERO
	_brow_r.position = Vector2.ZERO


func set_mouth(mode: String) -> void:
	var open: bool = (mode == "open_test") and mouth_proxy_enabled
	_sp["lower_face_neutral"].visible = not open
	_sp["lower_face_open_test"].visible = open


func reset_pose() -> void:
	set_state("neutral")
	_set_blink(false)
	set_mouth("neutral")
