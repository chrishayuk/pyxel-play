import pyxel

def start_background_music():
    # Main melody with a catchy loop
    pyxel.sound(0).set(
        "c4 e4 g4 f4 d4 e4 c4 r",  # A simple and pleasant melody
        "t",
        "5",
        "vff vff vff vff",
        20,
    )
    # Supporting harmony for depth
    pyxel.sound(1).set(
        "g3 b3 d4 g4 b3 d4 g3 r",  # Complementing the main melody
        "t",
        "4",
        "nfn nfn nfn nfn",
        20,
    )
    # Bassline for added rhythm
    pyxel.sound(2).set(
        "c2 g2 c3 g2 c2 g2 c2 r",  # Basic bass pattern
        "n",
        "6",
        "n",
        20,
    )
    # Light percussion for a subtle beat
    pyxel.sound(3).set(
        "c1 r c1 r c1 r c1 r",  # Soft percussion effect
        "p",
        "7",
        "v",
        15,
    )

    # Start playing all channels in a loop for a harmonious effect
    pyxel.play(0, [0], loop=True)
    pyxel.play(1, [1], loop=True)
    pyxel.play(2, [2], loop=True)
    pyxel.play(3, [3], loop=True)
