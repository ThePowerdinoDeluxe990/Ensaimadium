import tkinter
from Browser import Browser
from Web_Connection.URL import URL

if __name__ == "__main__":
    # body = URL(sys.argv[1]).request()
    # nodes = HTMLParser(body).parse()
    # print_tree(nodes)
    Browser().load(URL("https://perfectmotherfuckingwebsite.com/"))

    tkinter.mainloop()
