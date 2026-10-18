class_name TahmuresRig
extends Node2D
## Reusable Tahmures staging component (candidate-local).
##
## The Head node is a byte-for-byte reproduction of the approved front-view
## prototype head: same 17 full-canvas (1086x1448) sprite children in the same
## order, same texture filter (nearest), group "approved_head_component".
## In the POC the Head sits at world (543, 724) under a Camera2D at
## (560, 330) zoom 1, landing the face centre at screen (543, 174). The
## candidate keeps that exact placement by default (set by the chapter
## director) and scales the whole rig down for wide shots.
##
## States available (all from the approved facial-state set — no new faces):
##   neutral / blink / thinking   (eyes + brow underlay + 1px brow lift)
##   mouth: neutral / open_test   (open_test is a two-state PROXY only,
##                                 never lip-sync; off unless explicitly enabled)
##
## The optional temporary arm chain (POC temporary-body assets) is a
## temporary_placeholder group, clearly not approved art.

signal blink_started
signal blink_ended

const HEAD_LAYER_ORDER := [
	"hair_back", "head_base", "thinking_brow_underlay", "ear_right", "ear_left",
	"beard", "lower_face_neutral", "lower_face_open_test", "nose", "eye_right",
	"eye_left", "eye_right_closed", "eye_left_closed", "eyebrow_right",
	"eyebrow_left", "moustache", "diadem_gold",
]
const HIDDEN_BY_DEFAULT := ["thinking_brow_underlay", "lower_face_open_test", "eye_right_closed", "eye_left_closed"]

var head: Node2D
var arm_root: Node2D          # optional temporary arm (may be null)
var arm_visible := true
var mouth_proxy_enabled := false
var time := 0.0               # set by the director; blink is a pure fn of it
var _state := "neutral"
var _blink_on := false

# Sprite references
var _sp: Dictionary = {}
var _brow_l: Sprite2D
var _brow_r: Sprite2D


func _ready() -> void:
	add_to_group("tahmures_rig")
	_build_head()
	_build_temporary_arm()


func _build_head() -> void:
	head = Node2D.new()
	head.name = "Head"
	head.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	add_child(head)
	for layer in HEAD_LAYER_ORDER:
		var spr := Sprite2D.new()
		spr.name = layer
		spr.texture = load("res://assets/approved-head/%s.png" % layer)
		spr.add_to_group("approved_head_component")
		if layer in HIDDEN_BY_DEFAULT:
			spr.visible = false
		head.add_child(spr)
		_sp[layer] = spr
	_brow_l = _sp["eyebrow_left"]
	_brow_r = _sp["eyebrow_right"]


func _build_temporary_arm() -> void:
	# POC temporary-body chain (torso implied off-screen; arm only) at the
	# POC's relative positions, used to point at tablets/labels.
	arm_root = Node2D.new()
	arm_root.name = "ArmRoot"
	arm_root.add_to_group("temporary_placeholder")
	add_child(arm_root)
	var shoulder := Node2D.new()
	shoulder.name = "ShoulderL"
	shoulder.position = Vector2(0, 0)
	shoulder.rotation = -0.10472
	shoulder.add_to_group("temporary_placeholder")
	arm_root.add_child(shoulder)
	var upper := Sprite2D.new()
	upper.name = "UpperArmL"
	upper.texture = load("res://assets/temporary-body/upper_arm.png")
	upper.offset = Vector2(0, -47.5)
	upper.add_to_group("temporary_placeholder")
	shoulder.add_child(upper)
	var elbow := Node2D.new()
	elbow.name = "ElbowL"
	elbow.position = Vector2(0, 95)
	elbow.rotation = 0.174533
	elbow.add_to_group("temporary_placeholder")
	shoulder.add_child(elbow)
	var forearm := Sprite2D.new()
	forearm.name = "ForearmL"
	forearm.texture = load("res://assets/temporary-body/forearm.png")
	forearm.offset = Vector2(0, -42.5)
	forearm.add_to_group("temporary_placeholder")
	elbow.add_child(forearm)
	var handn := Node2D.new()
	handn.name = "HandL"
	handn.position = Vector2(0, 85)
	handn.add_to_group("temporary_placeholder")
	elbow.add_child(handn)
	var hand := Sprite2D.new()
	hand.name = "HandSpriteL"
	hand.texture = load("res://assets/temporary-body/hand_point.png")
	hand.offset = Vector2(0, -25)
	hand.add_to_group("temporary_placeholder")
	handn.add_child(hand)


## Deterministic blink: a pure function of `time` (no accumulated RNG state),
## so seek and restart land on identical frames. One 0.35 s blink every
## 3.7 s, suppressed while thinking.
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
	# Only approved facial states. Unknown values fall back to neutral.
	if s != "neutral" and s != "thinking":
		s = "neutral"
	_state = s
	var thinking: bool = s == "thinking"
	_sp["thinking_brow_underlay"].visible = thinking
	# POC uses a 1px brow lift for thinking; keep that, no other geometry.
	var lift := Vector2(0, -1) if thinking else Vector2(0, 0)
	_brow_l.position = lift
	_brow_r.position = lift


func set_mouth(mode: String) -> void:
	# "neutral" (default) or "open_test" (two-state proxy, only when enabled
	# explicitly via --mouth-proxy=open_test; it is NOT lip-sync).
	var open: bool = (mode == "open_test") and mouth_proxy_enabled
	_sp["lower_face_neutral"].visible = not open
	_sp["lower_face_open_test"].visible = open


func set_arm_visible(v: bool) -> void:
	if arm_root != null:
		arm_root.visible = v


func set_arm_rotation(shoulder_rot: float, elbow_rot: float, hand_rot: float) -> void:
	if arm_root == null:
		return
	var shoulder: Node2D = arm_root.get_node("ShoulderL")
	shoulder.rotation = shoulder_rot
	var elbow: Node2D = shoulder.get_node("ElbowL")
	elbow.rotation = elbow_rot
	var hand: Node2D = elbow.get_node("HandL")
	hand.rotation = hand_rot
