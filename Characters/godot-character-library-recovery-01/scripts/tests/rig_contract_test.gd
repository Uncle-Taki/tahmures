extends SceneTree

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    if "--malformed-resource" in OS.get_cmdline_user_args():
        var malformed = load("res://scripts/character_rig.gd").new()
        malformed.character_id = "malformed"
        malformed.library_root = "res://scripts/tests/fixtures"
        root.add_child(malformed)
        return
    if "--missing-resource" in OS.get_cmdline_user_args():
        var missing = load("res://scripts/character_rig.gd").new()
        missing.character_id = "missing_character"
        root.add_child(missing)
        return
    var manifest = JSON.parse_string(FileAccess.get_file_as_string("res://character-library-manifest.json"))
    for entry in manifest.characters:
        var actor = load("res://scenes/characters/%s.tscn" % entry.character_id).instantiate()
        actor.position = Vector2(100, 50)
        root.add_child(actor)
        assert(actor.layer_sprites.size() == entry.components.size())
        actor.set_state("idle", 0.75)
        assert(actor.position == Vector2(100, 52))
        actor.reset_pose()
        assert(actor.position == Vector2(100, 50))
        actor.set_state("blink")
        assert(actor.current_state == "neutral")
        for holder in actor.layer_sprites.values():
            assert(holder.rotation == 0.0)
            assert(holder.scale == Vector2.ONE)
            assert(not holder.get_child(0).centered)
        actor.free()
    var head = load("res://scripts/tahmures_rig.gd").new()
    root.add_child(head)
    assert(head._sp.size() == 17)
    head.set_state("thinking")
    assert(head._brow_l.position == Vector2(0, -1))
    assert(head._brow_r.position == Vector2.ZERO)
    head.set_state("neutral")
    head.set_time(3.1)
    assert(head._blink_on)
    head.reset_pose()
    assert(not head._blink_on)
    assert(not head._sp["lower_face_open_test"].visible)
    assert(not head._sp["head_base"].centered)
    head.free()
    print("PASS: ten rigs, whole-pose idle/reset, unsupported states, approved head brow/blink/centering")
    quit(0)
