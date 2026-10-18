class_name Timeline
extends RefCounted
## Loads data/chapter-cues.json and exposes the chapter's deterministic
## scene/cue/OST plan. This is the single source of truth for the visual
## timeline (173 s, 30 fps, 1280x720). Scenes are the 11 planned shots
## CH01-S01..CH01-S11 with the review-brief durations.

const CUES_PATH := "res://data/chapter-cues.json"

var total_seconds: float = 0.0
var fps: int = 30
var scenes: Array = []          # dicts: id, start, duration, title_en, title_fa, beat, location
var cues: Array = []            # dialogue/narration cue dicts
var osts: Array = []            # on-screen-text overlay dicts
var speaker_names: Dictionary = {}
var errors: Array = []          # validation errors (empty when plan is sound)


func load_plan() -> bool:
	var file := FileAccess.open(CUES_PATH, FileAccess.READ)
	if file == null:
		errors.append("cannot open " + CUES_PATH)
		return false
	var data: Variant = JSON.parse_string(file.get_as_text())
	file.close()
	if typeof(data) != TYPE_DICTIONARY:
		errors.append("chapter-cues.json is not a JSON object")
		return false
	var ep: Dictionary = data.get("episode", {})
	total_seconds = float(ep.get("timeline_seconds", 0.0))
	fps = int(ep.get("fps", 30))
	speaker_names = data.get("speaker_names", {})
	var slist: Array = data.get("scenes", [])
	for s in slist:
		scenes.append(s)
	for c in data.get("cues", []):
		cues.append(c)
	for o in data.get("osts", []):
		osts.append(o)
	_validate()
	return errors.is_empty()


func _validate() -> void:
	if scenes.size() != 11:
		errors.append("expected 11 scenes, got %d" % scenes.size())
	var sum := 0.0
	var prev_end := 0.0
	for s in scenes:
		var d := float(s.get("duration", 0.0))
		var st := float(s.get("start", 0.0))
		if not is_equal_approx(st, prev_end):
			errors.append("%s start %f does not follow previous scene end %f" % [s.get("id", "?"), st, prev_end])
		sum += d
		prev_end = st + d
	if not is_equal_approx(sum, total_seconds):
		errors.append("scene durations sum to %f, not %f" % [sum, total_seconds])
	var bounds: Dictionary = {}
	for s in scenes:
		bounds[s.get("id")] = [float(s.get("start")), float(s.get("start")) + float(s.get("duration"))]
	for c in cues:
		var b: Variant = bounds.get(c.get("scene"))
		if b == null:
			errors.append("cue %s references unknown scene" % c.get("id", "?"))
			continue
		if float(c.get("start")) < b[0] - 0.01 or float(c.get("end")) > b[1] + 0.01:
			errors.append("cue %s %f-%f outside scene %s" % [c.get("id"), float(c.get("start")), float(c.get("end")), c.get("scene")])
	for o in osts:
		var b2: Variant = bounds.get(o.get("scene"))
		if b2 == null:
			errors.append("OST %s references unknown scene" % o.get("id", "?"))
			continue
		if float(o.get("start")) < b2[0] - 0.01 or float(o.get("end")) > b2[1] + 0.01:
			errors.append("OST %s %f-%f outside scene %s" % [o.get("id"), float(o.get("start")), float(o.get("end")), o.get("scene")])
	_check_overlap(cues, "cue")
	_check_overlap(osts, "OST")
	for c in cues:
		if String(c.get("en", "")).is_empty() or String(c.get("fa", "")).is_empty():
			errors.append("cue %s missing bilingual text" % c.get("id", "?"))


func _check_overlap(items: Array, what: String) -> void:
	# Overlaps are only a defect within the same band: dialogue/narration cues
	# share one caption track; OST overlays of DIFFERENT kinds are designed to
	# coexist (e.g. the S08 tablet line + its panel label, S11 ledger +
	# takeaway). Same-kind pairs must still be disjoint.
	for a in range(items.size()):
		for b2 in range(a + 1, items.size()):
			var ia: Dictionary = items[a]
			var ib: Dictionary = items[b2]
			if ia.get("scene") != ib.get("scene"):
				continue
			var has_kind: bool = items[0].has("kind")
			if has_kind and ia.get("kind") != ib.get("kind"):
				continue
			var s1: float = max(float(ia.get("start")), float(ib.get("start")))
			var e1: float = min(float(ia.get("end")), float(ib.get("end")))
			if e1 - s1 > 0.01:
				errors.append("%s overlap: %s vs %s" % [what, ia.get("id"), ib.get("id")])


func scene_at(t: float) -> Dictionary:
	for s in scenes:
		if t >= float(s.get("start", 0.0)) and t < float(s.get("start", 0.0)) + float(s.get("duration", 0.0)):
			return s
	if scenes.is_empty():
		return {}
	return scenes[scenes.size() - 1]


func scene_index_at(t: float) -> int:
	for i in scenes.size():
		if t >= float(scenes[i].get("start", 0.0)) and t < float(scenes[i].get("start", 0.0)) + float(scenes[i].get("duration", 0.0)):
			return i
	return scenes.size() - 1 if not scenes.is_empty() else 0


func cues_at(t: float) -> Array:
	var out: Array = []
	for c in cues:
		if t >= float(c.get("start")) and t < float(c.get("end")):
			out.append(c)
	return out


func osts_at(t: float) -> Array:
	var out: Array = []
	for o in osts:
		if t >= float(o.get("start")) and t < float(o.get("end")):
			out.append(o)
	return out


func cues_for_scene(scene_id: String) -> Array:
	var out: Array = []
	for c in cues:
		if c.get("scene") == scene_id:
			out.append(c)
	return out


func osts_for_scene(scene_id: String) -> Array:
	var out: Array = []
	for o in osts:
		if o.get("scene") == scene_id:
			out.append(o)
	return out


func clamp_time(t: float) -> float:
	return clampf(t, 0.0, total_seconds)
