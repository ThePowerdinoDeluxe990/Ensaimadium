import skia

NAMED_COLORS = {
    "black": "#000000",
    "white": "#ffffff",
    "red":   "#ff0000",
    "blue": "#0000ff",
    "green": "#00ff00",
    "yellow": "#ffff00",
    "cyan": "#00ffff",
    "magenta": "#ff00ff",
}


def parse_color(color):
    if color.startswith("#") and len(color) == 7:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        return skia.Color(r, g, b)
    elif color in NAMED_COLORS:
        return parse_color(NAMED_COLORS[color])
    elif color.startswith("#") and len(color) == 9:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        a = int(color[7:9], 16)
        return skia.Color(r, g, b, a)
    else:
        return skia.ColorBLACK
