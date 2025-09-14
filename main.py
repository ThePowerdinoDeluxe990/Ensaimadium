import sdl2dll
import sdl2

from Browser import Browser
from Rendering.functions.mainloop import mainloop
from Web_Connection.URL import URL



if __name__ == "__main__":
    sdl2.SDL_Init(sdl2.SDL_INIT_EVENTS)
    browser = Browser()
    browser.new_tab(URL("https://thepowerdinodeluxe990.github.io/Ensaimadium/"))
    browser.draw()
    mainloop(browser)


