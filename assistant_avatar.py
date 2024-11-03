import pyxel
import time

class AssistantAvatar:
    def __init__(self):
        # Initialize
        self.is_talking = False
        self.streaming_index = 0
        self.response_text = ""
        self.full_response = ""
        
        # Set up sound for talking
        pyxel.sound(1).set(
            "g1 r g1 r r g1 r g1 r r", 
            "n", 
            "6", 
            "n", 
            20
        )

        # Corrected font dimensions (Pyxel's default font)
        self.FONT_WIDTH = 4  # Each character is 4 pixels wide
        self.FONT_HEIGHT = 6  # Each character is 6 pixels tall
        self.LINE_HEIGHT = self.FONT_HEIGHT + 2  # Additional spacing between lines

        # Fixed size for the speech bubble
        self.bubble_width = 150  # Fixed width
        self.bubble_height = 60  # Fixed height

    def start_talking(self, response_text):
        # Start talking
        self.is_talking = True
        self.streaming_index = 0
        self.response_text = ""
        self.full_response = response_text

    def stop_talking(self):
        # Stop talking
        self.is_talking = False

    def update_talking(self):
        if self.is_talking and self.streaming_index < len(self.full_response):
            self.response_text += self.full_response[self.streaming_index]
            self.streaming_index += 1
            
            if self.streaming_index % 2 == 0:  # Play talking sound
                pyxel.play(1, 1)
            
            time.sleep(0.05)  # Control streaming speed
            
            if self.streaming_index == len(self.full_response):
                self.stop_talking()
                return False  # Indicate end of response
        
        return self.is_talking  # Return whether speaking or not

    def draw_avatar(self):
        # Draw the avatar
        pyxel.circ(128, 40, 40, 11)  # Head
        pyxel.rect(108, 20, 8, 8, 0)  # Left eye
        pyxel.rect(148, 20, 8, 8, 0)  # Right eye

        # Animate the mouth if talking
        if self.is_talking and self.streaming_index % 4 < 2:
            pyxel.rect(122, 48, 14, 4, 0)  # Open mouth
        else:
            pyxel.rect(122, 50, 14, 2, 0)  # Closed mouth

        # Draw the speech bubble
        if self.response_text:
            self.draw_speech_bubble()

    def draw_speech_bubble(self):
        # Fixed position for the bubble
        bubble_x = 50
        bubble_y = 80  # Adjusted base Y position

        padding = 6  # Total horizontal padding (left + right)
        padding_top = 4  # Padding at the top of the bubble
        padding_bottom = 4  # Padding at the bottom of the bubble

        # Recalculate maximum characters per line with correct font width
        max_chars_per_line = (self.bubble_width - padding) // self.FONT_WIDTH
        max_lines = 6#(self.bubble_height - padding_top - padding_bottom) // self.LINE_HEIGHT

        # Wrap text into lines
        text_lines = self.wrap_text(self.response_text, max_chars_per_line)

        # Limit the number of visible lines to max_lines
        visible_lines = text_lines[-max_lines:]  # Only show the last max_lines

        # Draw the bubble background
        pyxel.rect(bubble_x, bubble_y, self.bubble_width, self.bubble_height, 7)

        # Draw the text
        for i, line in enumerate(visible_lines):
            y = bubble_y + padding_top + i * self.LINE_HEIGHT
            # Draw each line within the bubble without offset issues
            pyxel.text(bubble_x + padding // 2, y, line, 0)


    def wrap_text(self, text, max_chars_per_line):
        words = text.split(' ')
        lines = []
        current_line = ''

        for word in words:
            # Handle very long words that exceed max_chars_per_line
            while len(word) > max_chars_per_line:
                if current_line:
                    lines.append(current_line)
                    current_line = ''
                lines.append(word[:max_chars_per_line])
                word = word[max_chars_per_line:]

            # Check if adding the word exceeds the line length
            if len(current_line) + len(word) + (1 if current_line else 0) <= max_chars_per_line:
                if current_line:
                    current_line += ' ' + word
                else:
                    current_line = word
            else:
                # Add the current line to lines and start a new line
                lines.append(current_line)
                current_line = word

        # Add any remaining text
        if current_line:
            lines.append(current_line)

        return lines
