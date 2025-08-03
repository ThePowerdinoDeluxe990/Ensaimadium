from Rendering.functions.parse_color import parse_color
import skia

class DrawText:
    def __init__(self,x1,y1,text,font,color):

        self.rect = skia.Rect.MakeLTRB(
            x1,y1,
            x1 + font.measureText(text),
            y1 - font.getMetrics().fAscent \
                + font.getMetrics().fDescent)

        self.font = font
        self.text = text
        self.color = color

    def execute(self, scroll, canvas):
        paint = skia.Paint(
            AntiAlias = True,
            Color = parse_color(self.color),
        )
        baseline = self.rect.top()  \
            - self.font.getMetrics().fAscent
        canvas.drawString(self.text, float(self.rect.left()),
                          baseline, self.font, paint)


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

class DrawRect:
    def __init__(self,rect,color):
        self.rect = rect
        self.color = color

    def execute(self, canvas):
        paint = skia.Paint(
            Color=parse_color(self.color),
        )
        canvas.drawRect(self.rect, paint)