import tkinter
import tkinter.font

from Rendering.Layout import Layout

WIDTH, HEIGHT = 800,600

HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100
from Rendering.Text_Tag import HTMLParser

class Browser:
    def load(self, url):
        body = url.request()
        self.nodes = HTMLParser(body).parse()
        self.display_list = Layout(self.nodes).display_list
        self.draw()

    def __init__(self):
        self.display_list = []
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

        for x,y,word,font in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.Canvas.create_text(x,y-self.scroll,text=word, font = font, anchor="nw")

    def scrolldown(self,e):
        self.scroll += SCROLL_STEP
        self.draw()

