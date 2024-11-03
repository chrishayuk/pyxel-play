import pyxel

class App:
    def __init__(self):
        # set the window size and title
        pyxel.init(160, 120, title="Hello World!")

        # handle frame updates, and screen draws
        pyxel.run(self.update, self.draw)

    def update(self):
        # look for the q key
        if pyxel.btnp(pyxel.KEY_Q):
            # quit
            pyxel.quit()


    def draw(self):
        # clear the screen
        pyxel.cls(0)

        # draw the moving text
        pyxel.text(60, 60, "Hello, World!", pyxel.frame_count % 16)


# check if startup
if __name__ == "__main__":
    # call the app
    App()