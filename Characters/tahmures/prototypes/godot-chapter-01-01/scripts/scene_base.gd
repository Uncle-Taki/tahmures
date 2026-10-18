class_name SceneBase
extends Node2D
## Base class for the eleven chapter scenes.
##
## Determinism contract: update() is a pure function of local_t (seconds into
## the scene). No accumulated state — restart and seek simply re-enter and
## re-evaluate, which makes both fully reset (no residue from previous runs).

var scene_id := ""
var duration := 0.0
var bg_color: Color = StageKit.BG_HALL
## World position of the "ground line" where standing figures put their feet.
var ground_y := 640.0

func _ready() -> void:
	visible = false


## Called once when this scene becomes active (and again after restart/seek).
func enter(_local_t: float, _ctx: Dictionary) -> void:
	pass


## Called every frame with local time. Must be a pure function of local_t.
func update(_local_t: float, _ctx: Dictionary) -> void:
	pass


## Camera pose for this scene at local_t: {pos: Vector2, zoom: float}.
func cam_target(_local_t: float) -> Dictionary:
	return {"pos": Vector2(640, 360), "zoom": 1.0}
