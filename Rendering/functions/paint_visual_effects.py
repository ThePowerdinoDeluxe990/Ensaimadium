from Rendering.Draw.Blend import Blend
from Rendering.Draw.Draw import DrawRRect


def paint_visual_effects(node, cmds, rect):
    opacity = float(node.style.get("opacity", "1.0"))

    blend_mode = node.style.get("mix-blend-mode")
    if node.style.get("overflow", "visible") == "clip":
        if not blend_mode:
            blend_mode = "source-over"
        border_radius = float(node.style.get(
            "border-radius", "0px")[:-2])
        cmds.append(Blend(1.0,"destination-in", [
            DrawRRect(rect, border_radius, "white")
        ]))
    return [Blend(opacity, blend_mode, cmds)]
