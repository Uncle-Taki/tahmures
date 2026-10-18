class_name CharacterRig
extends Node2D
## Reusable layered Godot puppet controller for all supplied Tahmures characters.
##
## Candidate source-pose partitions; only whole-rig neutral/idle supported.
## Supports humanoid/div characters (akvan_div, black_div, div_e_sefid, shahrasp,
## chapar, arash, garshasp, simurgh_human) and the bird-specific avian rig
## (simurgh_bird).
##
## HARD RULE: Never falls back to res://assets/standins/*.png. If a required
## character manifest or layer PNG is absent, logs push_error and exits non-zero.

@export var character_id: String = "akvan_div"
@export var library_root: String = "res://characters"

var metadata: Dictionary = {}
var layer_sprites: Dictionary = {}
var sockets: Dictionary = {}
var current_state: String = "neutral"
var time: float = 0.0

const SUPPORTED_STATES := ["neutral", "idle"]
var pose_origin := Vector2.ZERO


func _ready() -> void:
	add_to_group("character_rig")
	pose_origin = position
	load_character(character_id)


func load_character(cid: String) -> bool:
	character_id = cid
	for child in get_children():
		remove_child(child)
		child.queue_free()
	layer_sprites.clear()
	sockets.clear()

	var meta_path := "%s/%s/component-map.json" % [library_root, cid]
	if not FileAccess.file_exists(meta_path):
		push_error("CRITICAL: Missing component-map.json for '%s' at '%s'. Silhouette fallback is forbidden." % [cid, meta_path])
		if get_tree() != null:
			get_tree().quit(1)
		return false

	var f := FileAccess.open(meta_path, FileAccess.READ)
	if f == null:
		push_error("CRITICAL: Cannot read character component map")
		get_tree().quit(1)
		return false
	var parsed: Variant = JSON.parse_string(f.get_as_text())
	f.close()
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("CRITICAL: Invalid component-map.json for '%s'." % cid)
		get_tree().quit(1)
		return false
	if parsed.get("character_id") != cid or typeof(parsed.get("draw_order_bottom_to_top")) != TYPE_ARRAY or parsed["draw_order_bottom_to_top"].is_empty():
		push_error("CRITICAL: Malformed character component map")
		get_tree().quit(1)
		return false
	metadata = parsed

	var draw_order: Array = metadata.get("draw_order_bottom_to_top", [])
	for comp in draw_order:
		if typeof(comp) != TYPE_DICTIONARY or typeof(comp.get("component_id")) != TYPE_STRING or typeof(comp.get("pivot_canvas")) != TYPE_ARRAY or comp["pivot_canvas"].size() != 2:
			push_error("CRITICAL: Malformed character layer record")
			get_tree().quit(1)
			return false
		var comp_id: String = comp.get("component_id", "")
		var tex_path := "%s/%s/layers/%s.png" % [library_root, cid, comp_id]
		if not ResourceLoader.exists(tex_path):
			push_error("CRITICAL: Missing layer texture '%s' for '%s'." % [tex_path, cid])
			if get_tree() != null:
				get_tree().quit(1)
			return false
		var pivot_arr: Array = comp.get("pivot_canvas", [543, 724])
		var pivot := Vector2(float(pivot_arr[0]), float(pivot_arr[1]))

		var holder := Node2D.new()
		holder.name = comp_id + "_pivot"
		holder.position = pivot
		add_child(holder)

		var spr := Sprite2D.new()
		spr.name = comp_id
		spr.texture = load(tex_path)
		spr.centered = false
		spr.position = -pivot
		holder.add_child(spr)
		layer_sprites[comp_id] = holder

	# Register prop & attachment sockets
	for sock in metadata.get("sockets", []):
		var snode := Marker2D.new()
		snode.name = String(sock.get("id", "PropSocket"))
		var pos_arr: Array = sock.get("position", [543, 600])
		snode.position = Vector2(float(pos_arr[0]), float(pos_arr[1]))
		add_child(snode)
		sockets[snode.name] = snode

	reset_pose()
	return true


func reset_pose() -> void:
	current_state = "neutral"
	position = pose_origin
	for comp_id in layer_sprites:
		var holder: Node2D = layer_sprites[comp_id]
		var base_piv: Array = _pivot_of(comp_id)
		holder.position = Vector2(float(base_piv[0]), float(base_piv[1]))
		holder.rotation = 0.0
		holder.scale = Vector2.ONE


func _pivot_of(comp_id: String) -> Array:
	for comp in metadata.get("draw_order_bottom_to_top", []):
		if comp.get("component_id") == comp_id:
			return comp.get("pivot_canvas", [543, 724])
	return [543, 724]


func set_state(state_name: String, t: float = 0.0) -> void:
	reset_pose()
	time = t
	if state_name not in SUPPORTED_STATES:
		current_state = "neutral"
		return
	current_state = state_name

	# Search-window partitions do not establish safe anatomical articulation.
	# Move all layers together; do not fake blinking, gaze or repaired hidden surfaces.
	if state_name == "idle":
		position = pose_origin + Vector2(0, sin(t * TAU / 3.0) * 2.0)
