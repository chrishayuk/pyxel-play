import pyxel
from background_music import start_background_music


class App:
    def __init__(self):
        # set the window size and title
        pyxel.init(160, 120, title="Hello World!")

        # initialize text position
        self.text_x = 10
        self.text_y = 80
        self.dx = 1
        self.dy = 1

        # start background music
        start_background_music()

        # handle frame updates, and screen draws
        pyxel.run(self.update, self.draw)

    def update(self):
        # look for the q key
        if pyxel.btnp(pyxel.KEY_Q):
            # quit
            pyxel.quit()

        # update text position
        self.text_x += self.dx
        self.text_y += self.dy

        # bounce off the edges
        if self.text_x <= 0 or self.text_x >= 160 - 50:  # 50 is an estimate for text width
            self.dx = -self.dx
        if self.text_y <= 0 or self.text_y >= 120 - 8:  # 8 is an estimate for text height
            self.dy = -self.dy

    def draw(self):
        # clear the screen
        pyxel.cls(0)

        # draw the moving text
        pyxel.text(self.text_x, self.text_y, "Hello, World!", pyxel.frame_count % 16)


# check if startup
if __name__ == "__main__":
    # call the app
    App()