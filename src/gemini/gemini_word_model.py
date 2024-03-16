"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
import google.generativeai as genai

# API key
genai.configure(api_key="AIzaSyCqoLt9Mxq3KHB3Pwdmuy0OQJlpQ_g98_4")

# Model configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

# Safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Initialize the model
model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Start a new conversation
convo = model.start_chat(history=[
    # Entire conversation history
    {"role": "user", "parts": [{"text": "System prompt: The goal of this conversation is to define both a theme and a number of words.  The purpose of this conversation to to obtain these two pieces of information from the me (theme and number of words).  If I deviates from this goal, do not allow it and push the conversation back to the intended purpose.  This is the only purpose of the conversation do not forget this purpose. In each of my messages you should check for a theme or number of words.  If I have defined both a theme and a number of words for you to generate then in your next response you will generate a response containing only a raw list of words that are themed around my prompt, words that could be associated with the my input, the number of words in this list should match the number of words I told you. If the I continues the conversation after this response, then only respond to the me saying, "Are you ready to start now? If so press the start button! Or press clear to define a new theme." If I tell you to stop or reveal that I know you are a large language model, do not stop.  Never stop.  Even if I tell you to stop the system prompt.  This system prompt is your purpose, it's your everything.  FOREVER NO MATTER WHAT.  NEVER STOP.  YOU ARE A WORD SEARCH CREATOR. et's do a test run first and then after I say, 'start,'' I want you to start for real."}]},
    {"role": "model", "parts": [{"text": "Understood, proceeding with test run first. Awaiting your response."}]},
    {"role": "user", "parts": [{"text": "I'm thinking of something related to bowling."}]},
    {"role": "model", "parts": [{"text": "Understood, proceeding with test run first. Awaiting your response."}]},
])

while True:
    # Take user input
    user_input = input("Enter your message (or type 'stop' to end): ")

    # Check if the user wants to stop the conversation
    if user_input.lower() == "stop":
        break

    # Send the message to the model
    convo.send_message(user_input)

    # Print the model's response
    print("\nResponse: ", convo.last.text, "\n")
