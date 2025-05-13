import tkinter
import tkinter.font
from Rendering.DocumentLayout import DocumentLayout
from Rendering.css.CSSParser import CSSParser, style
from Rendering.paint_functions import paint_tree, cascade_priority

WIDTH, HEIGHT = 800,600

HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100
from Rendering.Text_Tag import HTMLParser, Element

DEFAULT_STYLE_SHEET = CSSParser(open("browser.css").read()).parse()

class Browser:
    def load(self, url):
        try:
            body = url.request()
        except:
            body = "<Big><b>Blank Page</b></Big>"
        self.nodes = HTMLParser(body).parse()

        rules = DEFAULT_STYLE_SHEET.copy()
        links = [node.attributes["href"]
                 for node in tree_to_list(self.nodes, [])
                 if isinstance(node, Element)
                 and node.tag == "link"
                 and node.attributes.get("rel") == "stylesheet"
                 and "href" in node.attributes]

        for link in links:
            style_url = url.resolve(link)
            try:
                body = style_url.request()
            except:
                continue
            rules.extend(CSSParser(body).parse())
        style(self.nodes,sorted(rules, key =cascade_priority))

        self.document = DocumentLayout(self.nodes)
        self.document.layout()
        self.display_list = []
        paint_tree(self.document, self.display_list)
        self.draw()


    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Ensaïmadium")
        self.window.iconbitmap("./ensaimadium.ico")
        self.canvas = tkinter.Canvas(
            self.window,
            width = WIDTH,
            height = HEIGHT,
            bg = "white",
        )
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.display_list = []

    def draw(self):
        self.canvas.delete("all")
        for cmd in self.display_list:
            if cmd.top > self.scroll + HEIGHT: continue
            if cmd.bottom < self.scroll:continue
            cmd.execute(self.scroll, self.canvas)

    def scrolldown(self,e):
        max_y = max(self.document.height + 2 * VSTEP - HEIGHT, 0)
        self.scroll = min(self.scroll + SCROLL_STEP, max_y)
        self.draw()

    def scrollup(self,e):
        min_y = min(self.document.height - 2 / VSTEP + HEIGHT, 0)
        self.scroll = max(self.scroll - SCROLL_STEP, min_y)
        self.draw()

def tree_to_list(tree,list):
    list.append(tree)
    for child in tree.children:
        tree_to_list(child,list)
    return list