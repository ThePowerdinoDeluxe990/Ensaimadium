import tkinter


FONTS = {}

def get_font(size,weight,style):
    key = (size, weight, style)
    if key not in FONTS:
        font = tkinter.font.Font(size=size, weight=weight,slant= style)
        label = tkinter.Label(font=font)
        FONTS[key] = (font,label)
    return FONTS[key][0]


def paint_tree(layout_object, display_list):
    if layout_object.should_paint():
        display_list.extend(layout_object.paint())

    for child in layout_object.children:
        paint_tree(child, display_list)

def cascade_priority(rule):
    selector, body = rule
    return selector.priority