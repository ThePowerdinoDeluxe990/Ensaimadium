
import sdl2
import skia
import ctypes

from Rendering.Draw.DrawRRect import DrawRRect
from Rendering.Layout.InputLayout import InputLayout
from Rendering.Layout.LineLayout import LineLayout
from Rendering.Layout.TextLayout import TextLayout
from Rendering.functions.paint_visual_effects import paint_visual_effects
from Rendering.functions.get_font import get_font
from userChrome.Rect import Rect

INPUT_WIDTH_PX = 200
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

    def self_rect(self):
        return skia.Rect.MakeLTRB(
            self.x, self.y, self.x + self.width, self.y + self.height
        )

    def paint_effects(self,cmds):
        cmds = paint_visual_effects(
            self.node, cmds, self.self_rect()
        )
        return cmds

    def new_line(self):
        self.cursor_x = 0
        last_line = self.children[-1] if self.children else None
        new_line = LineLayout(self.node, self, last_line)
        self.children.append(new_line)


    def layout_mode(self):
        if isinstance(self.node, Text):
            return "inline"
        elif any([isinstance(child,Element) and \
                  child.tag in BLOCK_ELEMENTS
                  for child in self.node.children]):
            return "block"
        elif self.node.children or self.node.tag == "input":
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

    def word(self, node, word):
        weight = node.style["font-weight"]
        style = node.style["font-style"]
        try:
            size = float(node.style["font-size"][:-2]) * 0.75
        except:
            size= 1
        font = get_font(size, weight, style)
        w = font.measureText(word)
        if self.cursor_x + w > self.width:
            self.new_line()
        line = self.children[-1]
        previous_word = line.children[-1] if line.children else None
        text = TextLayout(node, word, line, previous_word)
        line.children.append(text)
        self.cursor_x += w + font.measureText(" ")

    def layout(self):

        self.width= self.parent.width
        self.x = self.parent.x

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
            self.new_line()
            self.recurse(self.node)

        for child in self.children:
            child.layout()

        self.height = sum([child.height for child in self.children])

    def recurse(self, node):
        if isinstance(node, Text):
            for word in node.text.split():
                self.word(node, word)
        else:
           if node.tag == "br":
               self.new_line()
           elif node.tag == "input" or node.tag == "button":
               self.input(node)
           else:
               for child in node.children:
                   self.recurse(child)

    def input(self, node):
        w = INPUT_WIDTH_PX
        if self.cursor_x + w > self.width:
            self.new_line()
        line = self.children[-1]
        previous_word = line.children[-1] if line.children else None
        input = InputLayout(node, line, previous_word)
        line.children.append(input)
        weight = node.style["font-weight"]
        style = node.style["font-style"]
        size = float(node.style["font-size"][:-2]) * 0.75
        font = get_font(size, weight, style)
        self.cursor_x += w + font.measureText(" ")


    def should_paint(self):
        return isinstance(self.node, Text) or \
            (self.node.tag != "input" and self.node.tag != "button")

    def paint(self):
        cmds = []
        bgcolor = self.node.style.get("background-color",
                                      "transparent")
        if bgcolor != "transparent":
            radius = float(
                self.node.style.get(
                    "border-radius", "0px")[:-2])
            cmds.append(DrawRRect(
                self.self_rect(), radius, bgcolor))

        return cmds