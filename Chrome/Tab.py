from Browser import tree_to_list, VSTEP, SCROLL_STEP
from Rendering.Layout.DocumentLayout import DocumentLayout
from Rendering.Text_Tag import Element, HTMLParser, Text
from Rendering.css.CSSParser import style, CSSParser
from Rendering.paint_functions import paint_tree, cascade_priority


DEFAULT_STYLE_SHEET = CSSParser(open("browser.css").read()).parse()
class Tab:
    def __init__(self, tab_height):
        self.url = None
        self.history = []
        self.tab_height = tab_height

    def draw(self, canvas, offset):
        for cmd in self.display_list:
            if cmd.rect.top > self.scroll + self.tab_height:
                continue
            if cmd.rect.bottom < self.scroll: continue
            cmd.execute(self.scroll - offset, canvas)

    def load(self,url):
        body = url.request()
        self.scroll = 0
        self.url = url
        self.history.append(url)
        self.nodes = HTMLParser(body).parse()

        rules = DEFAULT_STYLE_SHEET.copy()
        links = [node.attributes["href"]
                 for node in tree_to_list(self.nodes, [])
                 if isinstance(node, Element)
                 and node.tag == "link"
                 and node.attributes.get("rel") == "stylesheet"
                 and "href" in node.attributes]
        for link in links:
            try:
                body = url.resolve(link).request()
            except:
                continue
        style(self.nodes, sorted(rules, key=cascade_priority))

        self.document = DocumentLayout(self.nodes)
        self.document.layout()
        self.display_list = []
        paint_tree(self.document, self.display_list)


    def go_back(self):
        if len(self.history) > 1:
            self.history.pop()
            back = self.history.pop()
            self.load(back)

    def scrollup(self):
        min_y = min(self.document.height - 2 / VSTEP + self.tab_height, 0)
        self.scroll = max(self.scroll - SCROLL_STEP, min_y)


    def scrolldown(self):
        max_y = max(
            self.document.height + 2 * VSTEP - self.tab_height, 0)
        self.scroll = min(self.scroll + SCROLL_STEP, max_y)

    def click(self, x, y):
        y += self.scroll
        objs = [obj for obj in tree_to_list(self.document, [])
                if obj.x <= x < obj.x + obj.width
                and obj.y <= y < obj.y + obj.height]
        if not objs: return
        elt = objs[-1].node
        while elt:
            if isinstance(elt, Text):
                pass
            elif elt.tag == "a" and "href" in elt.attributes:
                url = self.url.resolve(elt.attributes["href"])
                return self.load(url)
            elt = elt.parent
