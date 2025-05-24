import tkinter

from userChrome.Chrome import Chrome
from Rendering.Layout.DocumentLayout import DocumentLayout
from Rendering.css.CSSParser import CSSParser, style
from Rendering.paint_functions import paint_tree, cascade_priority

WIDTH, HEIGHT = 800,600

HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100
from Rendering.Text_Tag import HTMLParser, Element, Text

DEFAULT_STYLE_SHEET = CSSParser(open("browser.css").read()).parse()

class Browser:
    def load(self, url):
        self.url = url
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

    def click(self,x,y):
        x,y = x,y
        y += self.scroll
        objs = [obj for obj in tree_to_list(self.document, [])
                if obj.x <= x < obj.x + obj.width
                and obj.y <= y < obj.y + obj.height]
        if not objs: return
        elt = objs[-1].node

        while elt:
            if isinstance(elt,Text):
                pass
            elif elt.tag == "a" and "href" in elt.attributes:
                url = self.url.resolve(elt.attributes["href"])
                return self.load(url)
            elt = elt.parent

    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT,
            bg="white"
        )
        self.window.title("Ensaimadium")
        self.window.iconbitmap("ensaimadium.ico")
        self.canvas.pack()
        self.tabs = []
        self.active_tab = None
        self.chrome = Chrome(self)

        self.window.bind("<Up>", self.handle_up)
        self.window.bind("<Down>", self.handle_down)
        self.window.bind("<Button-1>", self.handle_click)
        self.window.bind("<Key>", self.handle_key)
        self.window.bind("<Return>", self.handle_enter)

    def handle_enter(self,e):
        self.chrome.enter()
        self.draw()

    def handle_key(self,e):
        if len(e.char) == 0: return
        if not (0x20 <= ord(e.char)< 0x7f): return
        self.chrome.keypress(e.char)
        self.draw()

    def handle_down(self,e):
        self.active_tab.scrolldown()
        self.draw()

    def handle_up(self,e):
        self.active_tab.scrollup()
        self.draw()

    def handle_click(self,e):
        self.active_tab.click(e.x,e.y)
        self.draw()

    def new_tab(self,url):
        from userChrome.Tab import Tab
        new_tab = Tab(HEIGHT - self.chrome.bottom)
        new_tab.load(url)
        self.active_tab = new_tab
        self.tabs.append(new_tab)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.active_tab.draw(self.canvas, self.chrome.bottom)
        for cmd in self.chrome.paint():
            cmd.execute(0, self.canvas)


    def handle_click(self,e):
        if e.y < self.chrome.bottom:
            self.chrome.click(e.x,e.y)
        else:
            tab_y = e.y - self.chrome.bottom
            self.active_tab.click(e.x,tab_y)
        self.draw()

def tree_to_list(tree,list):
    list.append(tree)
    for child in tree.children:
        tree_to_list(child,list)
    return list