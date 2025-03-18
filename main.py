import tkinter

from Browser import Browser
from URL import URL


#Continuar con conexions encriptades
if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()
