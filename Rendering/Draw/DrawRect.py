import skia

from Rendering.functions.parse_color import parse_color


class DrawRect:
    def __init__(self,rect,color):
        self.rect = rect
        self.color = color

    def execute(self, canvas):
        paint = skia.Paint(
            Color=parse_color(self.color),
        )
        canvas.drawRect(self.rect, paint)
