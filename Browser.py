import tkinter

WIDTH, HEIGHT = 800,600

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.Canvas = tkinter.Canvas(
            self.window,
            width = WIDTH,
            height = HEIGHT
        )
        self.Canvas.pack()


    def load(self,url):
        body = url.request()
        show(body)
        self.Canvas.create_rectangle(10,20,400,300)
        self.Canvas.create_oval(100,100,150,150)
        self.Canvas.create_text(200,150, text="Hola")



def show(body):
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")
