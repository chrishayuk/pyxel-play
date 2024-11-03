from time import sleep
import pyxel
from llm_handler import stream_llm_response
from assistant_avatar import AssistantAvatar

class ChatApp:
    def __init__(self):
        pyxel.init(256, 160, title="AIs Chat Experience")

        # Stores chat messages as (text, is_user)
        self.messages = []  
        self.input_text = ""
        self.typing_mode = True

        # Instantiate the avatar
        self.avatar = AssistantAvatar() 

        # game loop
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.typing_mode:
            self.handle_input()

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.process_user_input()

        # Update talking status of the avatar
        if not self.typing_mode:
            if not self.avatar.update_talking():
                self.typing_mode = True

    def handle_input(self):
        # allow a-z
        for key in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
            # add the key
            if pyxel.btnp(key):
                self.input_text += chr(key).lower()

        # check for backspace
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.input_text) > 0:
            # remove previous letter
            self.input_text = self.input_text[:-1]

        # check for space
        if pyxel.btnp(pyxel.KEY_SPACE):
            # add a space
            self.input_text += " "

    def process_user_input(self):
        if self.input_text.strip():
            # Add the message
            self.add_message(self.input_text, is_user=True)

            # Clean up
            self.input_text = ""
            self.typing_mode = False
            pyxel.play(3, 0)

            # Add the LLM response
            self.add_llm_response()

    def add_message(self, text, is_user):
        # Adds a message to the chat
        self.messages.append((text, is_user))

    def add_llm_response(self):
        # Collect the full response from the stream
        full_response = ""

        # Pass the last user message as input
        response_stream = stream_llm_response(self.messages[-1][0])

        # Accumulate all chunks  
        for chunk in response_stream:
            full_response += chunk
            sleep(0.1)  # Ensure gradual update to match visual experience

        # Start avatar talking with the full response
        self.avatar.start_talking(full_response)
        self.add_message(full_response, is_user=False)

    def draw(self):
        # Clear screen
        pyxel.cls(0)

        # Draw input box at the bottom
        pyxel.rect(0, 150, 256, 10, 1)
        pyxel.text(5, 152, "> " + self.input_text, 7)

        # Draw the avatar
        self.avatar.draw_avatar()

# Check if startup
if __name__ == "__main__":
    # Call the app
    ChatApp()