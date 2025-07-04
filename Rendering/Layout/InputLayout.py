from Rendering.Draw.Draw import DrawRect, DrawText
from Rendering.Draw.DrawLine import DrawLine

INPUT_WIDTH_PX = 200

class InputLayout:
    def __init__(self,node,parent,previous ):
        self.node = node
        self.children = []
        self.parent = parent
        self.previous = previous

    def layout(self):
        self.width = INPUT_WIDTH_PX

    def paint(self):
        cmds = []
        bgcolor = self.node.style.get("background-color",
                                      "transparent")

        if self.node.tag == "input":
            text = self.node.attributes.get("value", "")
        elif self.node.tag == "button":
            if len(self.node.children) == 1 and \
                    isinstance(self.node.children[0], Text):
                text = self.node.children[0].text
            else:
                print("Ignoring HTML contents inside button")
                text = ""

        if self.node.is_focused:
            cx = self.x + self.font.measure(text)
            cmds.append(DrawLine(
                cx, self.y, cx, self.y + self.height, "black"
            ))

        if bgcolor != "transparent":
            rect = DrawRect(self.self_rect(), bgcolor)
            cmds.append(rect)

        color = self.node.style["color"]
        cmds.append(
            DrawText(self.x, self.y, text, self.font, color)
        )
        return cmds
