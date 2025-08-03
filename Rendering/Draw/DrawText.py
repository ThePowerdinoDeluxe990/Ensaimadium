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

    def execute(self, canvas):
        paint = skia.Paint(
            AntiAlias = True,
            Color = parse_color(self.color),
        )
        baseline = self.rect.top()  \
            - self.font.getMetrics().fAscent
        canvas.drawString(self.text, float(self.rect.left()),
                          baseline, self.font, paint)


