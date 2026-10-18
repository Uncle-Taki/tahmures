extends SceneTree
## Actual viewport captures. Run with a display; headless dummy rendering is not proof.

func _initialize() -> void:
    call_deferred("_capture")

func _frame(path: String) -> void:
    await process_frame
    await RenderingServer.frame_post_draw
    var result := root.get_texture().get_image().save_png(path)
    assert(result == OK)

func _capture() -> void:
    DirAccess.make_dir_recursive_absolute("res://previews/godot")
    var gallery = load("res://scripts/character_gallery.gd").new()
    root.add_child(gallery)
    gallery.mode = 2
    gallery.queue_redraw()
    for i in range(gallery.IDS.size()):
        gallery.index = i
        gallery.head_preview = false
        gallery._show()
        await _frame("res://previews/godot/%s-neutral.png" % gallery.IDS[i])
    gallery.set_process(false)
    gallery.actor.set_state("idle", 0.75)
    await _frame("res://previews/godot/simurgh_bird-idle.png")
    gallery.head_preview = true
    gallery.idle = false
    gallery._show()
    await _frame("res://previews/godot/approved-head-neutral.png")
    gallery.idle = true
    gallery.actor.set_state("thinking")
    await _frame("res://previews/godot/approved-head-thinking.png")
    gallery.actor.set_state("neutral")
    gallery.actor.set_time(3.1)
    await _frame("res://previews/godot/approved-head-blink.png")
    print("PASS: 14 actual Godot viewport captures written to previews/godot")
    quit(0)
