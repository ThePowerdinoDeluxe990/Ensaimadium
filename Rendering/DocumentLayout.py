from Rendering.BlockLayout import BlockLayout
WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18

class DocumentLayout:
    def __init__(self,node):
        self.node = node
        self.previous = None
        self.parent = None
        self.children = []

    def paint(self):
        return []

    def layout(self):
        child = BlockLayout(self.node, self, None)
        self.children.append(child)

        self.width = WIDTH - 2*HSTEP
        self.x = HSTEP
        self.y = VSTEP
        child.layout()
        self.height = child.height