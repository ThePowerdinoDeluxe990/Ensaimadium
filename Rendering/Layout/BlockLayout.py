import tkinter.font
import tkinter

from Rendering.Layout.LineLayout import LineLayout
from Rendering.Layout.TextLayout import TextLayout

FONTS = {}
WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
from Rendering.Text_Tag import Element, Text

BLOCK_ELEMENTS = [
    "html", "body", "article", "section", "nav", "aside",
    "h1", "h2", "h3", "h4", "h5", "h6", "hgroup", "header",
    "footer", "address", "p", "hr", "pre", "blockquote",
    "ol", "ul", "menu", "li", "dl", "dt", "dd", "figure",
    "figcaption", "main", "div", "table", "form", "fieldset",
    "legend", "details", "summary"
]

def get_font(size,weight,style):
    key = (size, weight, style)
    if key not in FONTS:
        font = tkinter.font.Font(size=size, weight=weight,slant= style)
        label = tkinter.Label(font=font)
        FONTS[key] = (font,label)
    return FONTS[key][0]

class BlockLayout:
    def __init__(self,node,parent,previous):
        self.node = node
        self.display_list = []
        self.parent = parent
        self.previous = previous
        self.children = []
        self.x = None
        self.y = None
        self.width = None
        self.height= None

    def new_line(self):
        self.cursor_x = 0
        last_line = self.children[-1] if self.children else None
        new_line = LineLayout(self.node, self, last_line)
        self.children.append(new_line)


    def layout_mode(self):
        if isinstance(self.node, tkinter.Text):
            return "inline"
        elif any([isinstance(child,Element) and \
                  child.tag in BLOCK_ELEMENTS
                  for child in self.node.children]):
            return "block"
        elif self.node.children:
            return "inline"
        else:
            return "block"

    def layout_intermediate(self):
        previous = None
        for child in self.node.children:
            next = BlockLayout(child,self,previous)
            self.children.append(next)
            previous = next
        
    def open_tag(self,tag):
        if tag == "i":
            self.style = "italic"
        elif tag == "b":
            self.weight = "bold"
        elif tag == "small":
            self.size -= 2
        elif tag == "big":
            self.size += 4
        elif tag == "br":
            self.flush()

    def close_tag(self,tag):
        if tag == "i":
            self.style = "roman"
        elif tag == "b":
            self.weight = "normal"
        elif tag == "small":
            self.size +=2
        elif tag == "big":
            self.size -=4
        elif tag == "/p":
            self.flush()
            self.cursor_y += VSTEP


    def flush(self):
        if not self.line: return
        metrics = [font.metrics() for x, word, font, color in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        for rel_x, word, font,color in self.line:
            x = self.x + rel_x
            y = self.y + baseline - font.metrics("ascent")
            self.display_list.append((x,y,word,font,color))
        self.cursor_x = 0
        self.line = []
        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline+1.25*max_descent

    def word(self, node, word):
        weight = node.style["font-weight"]
        style = node.style["font-style"]
        if style=="normal": style="roman"
        size = int(float(node.style["font-size"][:-2])*.75)
        font = get_font(size,weight,style)

        w = font.measure(word)
        if self.cursor_x + w > self.width:
            self.flush()
        color = node.style["color"]
        self.line.append((self.cursor_x,word, font, color))
        self.cursor_x += w + font.measure(" ")

        line = self.children[-1]
        previous_word = line.children[-1] if line.children else None
        text = TextLayout(node,word,line,previous_word)
        line.children.append(text)
        if self.cursor_x + w > self.width:
            self.new_line()

    def layout(self):
        self.x = self.parent.x
        self.width= self.parent.width

        if self.previous:
            self.y= self.previous.y+self.previous.height
        else:
            self.y = self.parent.y

        mode = self.layout_mode()
        if mode == "block":
            previous = None
            for child in self.node.children:
                next = BlockLayout(child, self, previous)
                self.children.append(next)
                previous = next
        else:
            self.cursor_x = 0
            self.cursor_y = 0
            self.weight = "normal"
            self.style = "roman"
            self.size = 12

            self.line = []
            self.recurse(self.node)
            self.flush()

        for child in self.children:
            child.layout()

        if mode == "block":
            self.height = sum([
                child.height for child in self.children])
        else:
            self.new_line()
            self.recurse(self.node)

    def recurse(self, node):
        if isinstance(node, Text):
            for word in node.text.split():
                self.word(node, word)
        else:
           if node.tag == "br":
               self.flush()
           for child in node.children:
                self.recurse(child)
