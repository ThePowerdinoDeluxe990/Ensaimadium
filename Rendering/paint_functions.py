
def paint_tree(layout_object, display_list):
    display_list.extend(layout_object.paint())

    for child in layout_object.children:
        paint_tree(child, display_list)

def cascade_priority(rule):
    selector, body = rule
    return selector.priority