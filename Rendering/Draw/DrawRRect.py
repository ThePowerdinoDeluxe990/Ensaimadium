import skia

from Rendering.functions.parse_color import parse_color


class DrawRRect:
    def __init__(self,rect,radius, color):
        self.rect = rect
        self.rrect = skia.RRect.MakeRectXY(rect, radius, radius)
        self.color = color

    def execute(self,canvas):
        paint = skia.Paint(
            Color = parse_color(self.color),
        )
        canvas.drawRRect(self.rrect, paint)
