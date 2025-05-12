import tkinter
from Browser import Browser
from Rendering.css.CSSParser import CSSParser
from Web_Connection.URL import URL
from tkinter.simpledialog import askstring

if __name__ == "__main__":
    url = askstring("Ensaïmadium","Pon la url de la pagina que quieras visitar WIP")
    Browser().load(URL(url))
    tkinter.mainloop()
    #body = URL(sys.argv[1]).request()
    #nodes = HTMLParser(body).parse()
    #print_tree(nodes)

