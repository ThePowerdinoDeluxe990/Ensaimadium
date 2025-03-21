import tkinter.font
import tkinter
HSTEP, VSTEP = 13, 18

class Layout:
    def __init__(self, tokens):
        self.display_list = []
        self.cursor_x = HSTEP,
        self.cursor_y = VSTEP,
        self.weight = "normal"
        self.style = "roman"
        for tok in tokens:
            self.token(tok)

    def token(self, tok):
        if isinstance(tok, tkinter.Text):
            for word in tok.text.split():
                word(self, word)
        elif tok.tag == "i":
           self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            self.weight = "bold"
        elif tok.tab == "/b":
            self.weight == "normal"

    def word(self, word):
        font = tkinter.font.Font(
            size = 16,
            weight=self.weight,
            slant=self.style,
        )
        w = font.measure(word)
        self.display_list.append((self.cursor_x, self.cursor_y, word, font))
