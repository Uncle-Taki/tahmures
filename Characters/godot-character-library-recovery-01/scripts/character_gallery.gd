extends Node2D
## Local candidate gallery. Rectangular partitions are not approved anatomical cuts.
const IDS := ["tahmures", "akvan_div", "black_div", "div_e_sefid", "shahrasp", "chapar", "arash", "garshasp", "simurgh_human", "simurgh_bird"]
var index := 0
var mode := 0
var idle := false
var elapsed := 0.0
var actor: Node2D
var title: Label
var info: Label
var head_preview := false

func _ready() -> void:
    title = Label.new()
    title.position = Vector2(20, 12)
    title.text = "LOCAL CHARACTER CANDIDATES | anatomical cuts / articulation NOT approved"
    add_child(title)
    info = Label.new()
    info.position = Vector2(20, 48)
    add_child(info)
    var help := Label.new()
    help.position = Vector2(20, 680)
    help.text = "[ / ] character | B background | S neutral/whole-pose idle | H approved head inspector | R reset"
    add_child(help)
    _show()

func _draw() -> void:
    var bg := Color("eee9df") if mode == 1 else Color("171c24")
    draw_rect(Rect2(0, 0, 1280, 720), bg)
    if mode == 2:
        for y in range(0, 720, 24):
            for x in range(0, 1280, 24):
                if (x / 24 + y / 24) % 2 == 0:
                    draw_rect(Rect2(x, y, 24, 24), Color("394353"))

    draw_rect(Rect2(0, 0, 1280, 76), Color("141922"))
    draw_rect(Rect2(0, 668, 1280, 52), Color("141922"))

func _show() -> void:
    if actor != null:
        remove_child(actor)
        actor.queue_free()
    if head_preview:
        actor = load("res://scripts/tahmures_rig.gd").new()
        actor.position = Vector2(-30, 90)
        actor.scale = Vector2(1.2, 1.2)
    else:
        actor = load("res://scenes/characters/%s.tscn" % IDS[index]).instantiate()
        actor.position = Vector2(400, 65)
        actor.scale = Vector2(0.4, 0.4)
    add_child(actor)
    var label := "accepted scoped head / neutral, blink, thinking" if head_preview else str(IDS[index]) + " / candidate partition / neutral + whole-pose idle only"
    info.text = label + " | no character approval recorded here"
    title.modulate = Color.WHITE
    info.modulate = title.modulate
    elapsed = 0.0

func _process(delta: float) -> void:
    elapsed += delta
    if head_preview:
        actor.set_state("thinking" if idle else "neutral")
        actor.set_time(elapsed)
    elif idle:
        actor.set_state("idle", elapsed)

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventKey and event.pressed and not event.echo:
        match event.keycode:
            KEY_BRACKETLEFT:
                index = posmod(index - 1, IDS.size())
                head_preview = false
                _show()
            KEY_BRACKETRIGHT:
                index = posmod(index + 1, IDS.size())
                head_preview = false
                _show()
            KEY_B:
                mode = (mode + 1) % 3
                queue_redraw()
                _show()
            KEY_S:
                idle = not idle
                _show()
            KEY_H:
                head_preview = not head_preview
                _show()
            KEY_R:
                idle = false
                _show()
