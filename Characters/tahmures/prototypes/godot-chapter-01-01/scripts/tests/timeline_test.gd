extends SceneTree
## Headless validation of the chapter cue plan + timeline behaviour.
## Run:  godot --headless --path <candidate> --script res://scripts/tests/timeline_test.gd
## Exits 0 on success, 1 on failure.

var _failures: Array = []


func _init() -> void:
	var tl: Timeline = Timeline.new()
	var ok := tl.load_plan()
	if not ok:
		for e in tl.errors:
			_failures.append("plan: " + e)
	else:
		_run_checks(tl)
	_finish()


func _run_checks(tl: Timeline) -> void:
	_check(tl.scenes.size() == 11, "11 scenes present")
	_check(tl.total_seconds == 173.0, "timeline is 173 s")
	_check(tl.fps == 30, "30 fps declared")
	var expected := [12.0, 16.0, 10.0, 15.0, 15.0, 17.0, 31.0, 15.0, 20.0, 15.0, 7.0]
	for i in 11:
		_check(is_equal_approx(float(tl.scenes[i].get("duration")), expected[i]),
			"scene %s duration = %s s" % [tl.scenes[i].get("id"), expected[i]])
	# Deterministic scene/cue lookup at representative frames.
	_check(tl.scene_at(0.0).get("id") == "CH01-S01", "t=0 -> S01")
	_check(tl.scene_at(172.9).get("id") == "CH01-S11", "t=172.9 -> S11")
	_check(tl.scene_at(173.0).get("id") == "CH01-S11", "t=173 clamps -> S11")
	var c3 := tl.cues_at(33.5)
	_check(c3.size() == 1 and c3[0].get("id") == "D-S03-1", "t=33.5 -> D-S03-1 only")
	var c5 := tl.cues_at(57.0)
	_check(c5.size() == 1 and c5[0].get("id") == "D-S05-1", "t=57.0 -> D-S05-1 only")
	var o7 := tl.osts_at(107.0)
	_check(o7.size() == 1 and o7[0].get("id") == "OST-S07-1", "t=107.0 -> OST-S07-1 only")
	_check(tl.osts_at(140.0).size() == 1, "t=140.0 -> exactly one OST (formula)")
	_check(tl.osts_at(171.0).size() == 2, "t=171.0 -> S11 ledger + takeaway overlap (by design)")
	# Bilingual completeness.
	var missing := 0
	for c in tl.cues:
		if String(c.get("en", "")).strip_edges().is_empty() or String(c.get("fa", "")).strip_edges().is_empty():
			missing += 1
	_check(missing == 0, "all cues have EN and FA text")
	# Dialogue census (per the live cue plan): 10 dialogue cues.
	var dialogue := 0
	var speakers: Dictionary = {}
	for c in tl.cues:
		if c.get("speaker") != "narrator":
			dialogue += 1
			speakers[c.get("speaker")] = int(speakers.get(c.get("speaker"), 0)) + 1
	_check(dialogue == 10, "10 dialogue cues")
	_check(speakers.get("tahmures", 0) == 4, "tahmures 4 dialogue cues")
	_check(speakers.get("akvan_div", 0) == 2, "akvan_div 2 dialogue cues")
	_check(speakers.get("black_div", 0) == 3, "black_div 3 dialogue cues")
	_check(speakers.get("simurgh", 0) == 1, "simurgh 1 dialogue cue")
	# Verbatim source dialogue spot-checks (live English chapter controls).
	_check(_text(tl, "D-S03-1", "en") == "Tell me what this is.", "D-S03-1 EN verbatim")
	_check(_text(tl, "D-S05-1", "en") == "There are eleven watchfires.", "D-S05-1 EN verbatim")
	_check(_text(tl, "D-S07-1", "fa").begins_with("بنویس: "), "D-S07-1 FA verbatim (dictation)")
	_check(_text(tl, "OST-S09-1", "en").count(" + ") == 7, "OST-S09-1 formula has eight terms")
	_check(_text(tl, "OST-S02-1", "en") == "Count the watchfires beyond the water before moonrise.", "OST-S02-1 tablet sentence verbatim")
	# Caption files parse and match the plan.
	# Plain relative paths resolve against the working directory; the test
	# is documented to run from the candidate directory via --path .
	var vtt_root: String = "data/"
	_check(_vtt_count(vtt_root + "captions-en.vtt") == tl.cues.size(), "EN VTT cue count matches plan")
	_check(_vtt_count(vtt_root + "captions-fa.vtt") == tl.cues.size(), "FA VTT cue count matches plan")


func _text(tl: Timeline, id: String, lang: String) -> String:
	for c in tl.cues:
		if c.get("id") == id:
			return String(c.get(lang, ""))
	for o in tl.osts:
		if o.get("id") == id:
			return String(o.get(lang, ""))
	return ""


func _vtt_count(path: String) -> int:
	if not FileAccess.file_exists(path):
		return -1
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return -1
	var n := 0
	# get_line() returns "" for the empty WebVTT separator lines, so loop on
	# eof_reached(), not on the returned text.
	while not f.eof_reached():
		var line: String = f.get_line()
		if line.is_valid_int():
			n += 1
	f.close()
	return n


func _check(ok: bool, what: String) -> void:
	if ok:
		print("PASS: " + what)
	else:
		_failures.append(what)
		printerr("FAIL: " + what)


func _finish() -> void:
	if _failures.is_empty():
		print("TIMELINE TESTS: ALL PASS")
		quit(0)
	else:
		for f in _failures:
			printerr("FAIL: " + f)
		printerr("TIMELINE TESTS: %d FAILURE(S)" % _failures.size())
		quit(1)
