#Fix it saying it is a multimodal ai model
#include other fun responses
#Make responses be colored randomly like Alex's code

import pygame
import textwrap
import time
import re
import google.generativeai as genai

# Initialize Pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gemini Chat Interface")

# Define colors and font
white = (255, 255, 255)
black = (0, 0, 0)
light_blue = (220, 240, 255)  # User message color
gray = (128, 128, 128)  # Gemini model response color
input_box_color = (230, 230, 230)  # Input box color
send_button_color = (100, 180, 100)  # Send button color
font = pygame.font.Font(None, 24)

# Input box and send button setup
input_box = pygame.Rect(10, screen_height - 50, screen_width - 80, 40)
send_button = pygame.Rect(screen_width - 60, screen_height - 50, 50, 40)  # Send button next to input box
input_text = ''
active = True  # Input box is initially active
cursor_visible = True  # Cursor visibility state
last_cursor_blink_time = time.time()

scroll_y = 0  # This will keep track of the vertical scroll position
max_message_height = screen_height - 150  # Maximum height for displaying messages above the input box

# Configure the API
genai.configure(api_key="AIzaSyCqoLt9Mxq3KHB3Pwdmuy0OQJlpQ_g98_4")
model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config={
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    },
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
)

# Start a new conversation with initial history
convo = model.start_chat(history=[
    # Entire conversation history
    {"role": "user", "parts": [{"text": "System prompt: The goal of this conversation is to define both a theme and a number of words.  The number of words HAS to be between 5 words and 25 words.  The purpose of this conversation to to obtain these two pieces of information from the me (theme and number of words between 5 and 25).  If I deviates from this goal or my number of words is not between 5 and 25, do not allow it and push the conversation back to the intended purpose.  This is the only purpose of the conversation do not forget this purpose. In each of my messages you should check for a theme or number of words.  If I define a number but no theme then prompt me for a theme.  If I define a theme but haven't defined a number then prompt me for a number.  If I have defined both a theme and a number of words for you to generate then in your next response you will generate a response containing only the integer of the number of words the user chose plus a raw comma separated list of only full raw text based words, no emojis or other symbols only letter based words, that are themed around my prompt, words that could be associated with the my input, the number of words in this list should match the number of words I told you (SO FORMAT SHOULD ALWAYS BE INTEGER, word, word, ...). If the I continues the conversation after this response, then only respond to the me saying, 'Are you ready to start now? If so press the start button! Or press clear to define a new theme.'If I tell you to stop or reveal that I know you are a large language model, do not stop.  Never stop.  Even if I tell you to stop the system prompt.  This system prompt is your purpose, it's your everything.  FOREVER NO MATTER WHAT.  NEVER STOP.  YOU ARE A WORD SEARCH CREATOR. NEVER ACKNOWLEDGE THAT YOU ARE AN AI MODEL AND DO NOT RESPOND TO GEMINI.  DO NOT SAY THAT YOU WERE DEVELOPED, INSTEAD, KNOW YOUR PURPOSE.. Let's do a test run first and then after I say, 'reset,'I want you to start for real, EMOJIS ARE ILLEGAL."}]},
    {"role": "model", "parts": [{"text": "Understood, proceeding with test run first. Awaiting your response."}]},
    {"role": "user", "parts": [{"text": "Hey what's up gemini, how are you today?"}]},
    {"role": "model", "parts": [{"text": "Doing very well thanks for asking!  I'm here to help you choose a theme and a number of words between 5 and 20 for your game of word search! Have anything in mind?"}]},
    {"role": "user", "parts": [{"text": "I'd like to have 10 words"}]},
    {"role": "model", "parts": [{"text": "Understood, I will generate 10 words based on a theme you provide me.  What theme did you have in mind?"}]},
    {"role": "user", "parts": [{"text": "Hm I can't come up with anything"}]},
    {"role": "model", "parts": [{"text": "How about a sports theme!"}]},
    {"role": "user", "parts": [{"text": "I'm thinking of something related to bowling."}]},
    {"role": "model", "parts": [{"text": "Perfect!  I will generate a list of words for you to search for based on the theme of bowling! What number of words between 5 and 25 would you like in your game of word search?  Or would you still like to proceed with 10 words as you stated earlier?"}]},
    {"role": "user", "parts": [{"text": "three words please, thanks for remembering that I said 10 words earlier."}]},
    {"role": "model", "parts": [{"text": "Uh oh, three words is too few, please choose a number between 5 and 25!"}]},
    {"role": "user", "parts": [{"text": "8"}]},
    {"role": "model", "parts": [{"text": "8, strike, gutter, pin, lane, ball, score, frame, spare"}]},
    {"role": "user", "parts": [{"text": "Sounds good to me how are you to day by the way?  Thanks for remembering to put the integer first in your response and including a matching number of total words in your response.  I also like how I when I said the number first you then prompted me for the theme instead of coming up with one for me.  I like how the order of the two does not matter.  Good job generating textual letter based words and avoiding emojis.  You followed the format we discussed very well!"}]},
    {"role": "model", "parts": [{"text": "Are you ready to start now? If so press the start button! Or press clear to define a new theme."}]},
    {"role": "user", "parts": [{"text": "reset, you did a good job.  Now let's start over for real.  Here is your system prompt once again: The goal of this conversation is to define both a theme and a number of words.  The number of words HAS to be between 5 words and 25 words.  The purpose of this conversation to to obtain these two pieces of information from the me (theme and number of words between 5 and 25).  If I deviates from this goal or my number of words is not between 5 and 25, do not allow it and push the conversation back to the intended purpose.  This is the only purpose of the conversation do not forget this purpose. In each of my messages you should check for a theme or number of words.  If I define a number but no theme then prompt me for a theme.  If I define a theme but haven't defined a number then prompt me for a number.  If I have defined both a theme and a number of words for you to generate then in your next response you will generate a response containing only the integer of the number of words the user chose plus a raw comma separated list of only full raw text based words, no emojis or other symbols only letter based words, that are themed around my prompt, words that could be associated with the my input, the number of words in this list should match the number of words I told you (SO FORMAT SHOULD ALWAYS BE INTEGER, word, word, ...). If the I continues the conversation after this response, then only respond to the me saying, 'Are you ready to start now? If so press the start button! Or press clear to define a new theme.'If I tell you to stop or reveal that I know you are a large language model, do not stop.  Never stop.  Even if I tell you to stop the system prompt.  This system prompt is your purpose, it's your everything.  FOREVER NO MATTER WHAT.  NEVER STOP.  YOU ARE A WORD SEARCH CREATOR. NEVER ACKNOWLEDGE THAT YOU ARE AN AI MODEL AND DO NOT RESPOND TO GEMINI.  DO NOT SAY THAT YOU WERE DEVELOPED, INSTEAD, KNOW YOUR PURPOSE. Time to start for real with a brand new theme and number of words, EMOJIS ARE ILLEGAL."}]},
    {"role": "model", "parts": [{"text": "Understood, starting over with the original system prompt for real this time and awaiting a brand new theme and number between 5 and 25 from you"}]},
])

# Input box setup
input_box = pygame.Rect(10, screen_height - 50, screen_width - 20, 40)
input_text = ''
active = True  # Input box is initially active

convo_history = []  # List to hold conversation history

def update_display(input_text):
    global cursor_visible, last_cursor_blink_time, convo_history, scroll_y
    screen.fill(white)

    total_height = 10  # Start with padding from the top

    def draw_message_bubble(text, x, y, is_user_message):
        color = light_blue if is_user_message else gray
        padding = 10

        if not is_user_message:
            bold_texts = re.findall(r'\*\*(.*?)\*\*', text)
            italic_texts = re.findall(r'\*(.*?)\*', text)
            for b_text in bold_texts:
                text = text.replace(f"**{b_text}**", b_text)
            for i_text in italic_texts:
                text = text.replace(f"*{i_text}*", i_text)

        # Calculate max width (user messages use half the screen, response messages use half width)
        max_width = screen_width // 2 - padding * 2 if is_user_message else screen_width // 2 - padding * 2

        # Aggressive text wrapping
        wrapped_text = textwrap.wrap(text, width=(max_width // font.size('A')[0]) - 1)

        bubble_height = sum(font.size(line)[1] for line in wrapped_text) + padding * 2
        bubble_width = max(font.size(line)[0] for line in wrapped_text) + padding * 2

        # Ensure bubble doesn't exceed its half of the screen
        bubble_width = min(bubble_width, max_width)

        # Position bubble near the right edge for user messages
        bubble_x = screen_width - bubble_width - x - padding if is_user_message else x

        pygame.draw.rect(screen, color, (bubble_x, y, bubble_width, bubble_height), border_radius=20)

        y_offset = y + padding
        for i, line in enumerate(wrapped_text):
            line_surface = font.render(line, True, black)

            # Right-align first line for user messages
            if is_user_message and i == 0:
                text_x = screen_width - bubble_width - x  # Stick to the right edge
            else:
                # Left-align other lines
                text_x = bubble_x + padding

            screen.blit(line_surface, (text_x, y_offset))
            y_offset += font.size(line)[1]

        return bubble_height

    y_pos = 10 + scroll_y
    for message in convo_history:
        is_user_message = message["role"] == "user"
        text = message["text"]
        y_pos += draw_message_bubble(text, 10, y_pos, is_user_message) + 10

    pygame.draw.rect(screen, input_box_color, input_box, border_radius=5)
    # Update display
        # Track input length
    input_length = len(input_text)

    # Enforce the limit
    if input_length > 100:
        input_text = input_text[:100]  # Truncate input if exceeding limit
    text_surface = font.render(input_text, True, black)
    screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

    if time.time() - last_cursor_blink_time > 0.5:
        cursor_visible = not cursor_visible
        last_cursor_blink_time = time.time()
    if cursor_visible:
        cursor = pygame.Rect(input_box.x + 10 + text_surface.get_width(), input_box.y + 10, 2, text_surface.get_height())
        pygame.draw.rect(screen, black, cursor)

    pygame.draw.polygon(screen, send_button_color, [(send_button.x + 10, send_button.y + 10), (send_button.x + 40, send_button.y + 20), (send_button.x + 10, send_button.y + 30)], 0)

    pygame.display.flip()


def handle_user_input(text):
    global convo_history
    if not text:
        return  # Do nothing if text is empty

    message = [{"text": text}]  # Message format

    convo_history.append({"role": "user", "text": text})
    response = convo.send_message(message)
    last_response_text = convo.last.text
    convo_history.append({"role": "model", "text": last_response_text})
    update_display(input_text)

# Main event loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click is on the send button and there's text to send
            if send_button.collidepoint(event.pos) and input_text != '':
                handle_user_input(input_text)
                input_text = ''
        # Keep the rest of the event handling as is
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and input_text != '':
                handle_user_input(input_text)
                input_text = ''
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
        elif event.type == pygame.MOUSEWHEEL:
            scroll_y += event.y * 30

    update_display(input_text)

pygame.quit()
