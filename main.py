import tkinter

from Browser import Browser
from Web_Connection.URL import URL
from tkinter.simpledialog import askstring

if __name__ == "__main__":
    Browser().new_tab(URL("https://thepowerdinodeluxe990.github.io/Ensaimadium/"))
    tkinter.mainloop()
    #body = URL(sys.argv[1]).request()
    #nodes = HTMLParser(body).parse()
    #print_tree(nodes)

