import tkinter
import tkinter.font
WIDTH, HEIGHT = 800,600

HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100
from Rendering.Text_Tag import Text, Tag

class Browser:
    def load(self, url):
        body = url.request()
        text = lex(body)
        self.display_list = layout(text)
        self.draw()

    def __init__(self):
        self.window = tkinter.Tk()
        self.Canvas = tkinter.Canvas(
            self.window,
            width = WIDTH,
            height = HEIGHT,
        )
        self.Canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)

    def draw(self):
        self.Canvas.delete("all")
        for x,y,c in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.Canvas.create_text(x,y-self.scroll,text=c)

    def scrolldown(self,e):
        self.scroll += SCROLL_STEP
        self.draw()

def lex(body):
    out = []
    buffer = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
            if buffer: out.append(Text(buffer))
            buffer = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(buffer))
            buffer = ""
        else:
            buffer +=c
    if not in_tag and buffer:
        out.append(Text(buffer))
    return out
