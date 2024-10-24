from fasthtml.common import *
from openai import OpenAI
import json

# Set up the app, including daisyui and tailwind for the chat component
hdrs = (picolink, Script(src="https://cdn.tailwindcss.com"),
        Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css"))
app = FastHTML(hdrs=hdrs, cls="p-4 max-w-lg mx-auto")

# # Set up OpenAI API key (make sure to set your OpenAI API key here)
# client = OpenAI(
#     api_key="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", # Set your OpenAI API key here
#     organization='org-Tsn20dQmqKgjiD2wUtFtrib7',
#     project='proj_eZDDVOyD7u7vXAKK9hlsAzsC',
# )

# # Function to get ChatGPT response using the OpenAI API
# def get_chatgpt_response(prompt):
#     response = client.chat.completions.create(
#         engine="gpt-4o-mini",  # You can use "gpt-4" if you have access, or stick to "gpt-3.5-turbo"
#         prompt=prompt,
#         max_tokens=150,
#         n=1,
#         stop=None,
#         temperature=0.7
#     )
#     return response.choices[0].text.strip()

# Chat message component (renders a chat bubble)
def ChatMessage(msg, user):
    paragraphs = msg.split("\n")
    bubble_class = "chat-bubble-primary" if user else 'chat-bubble-secondary'
    chat_class = "chat-end" if user else 'chat-start'
    return Div(cls=f"chat {chat_class}")(
               Div('user' if user else 'assistant', cls="chat-header"),
               Div(*[P(p) for p in paragraphs], cls=f"chat-bubble {bubble_class}"),
               Hidden(msg, name="messages")
           )

# The input field for the user message. Also used to clear the
# input field after sending a message via an OOB swap
def ChatInput():
    return Input(name='msg', id='msg-input', placeholder="Type a message",
                 cls="input input-bordered w-full", hx_swap_oob='true')

# The main screen
@app.get
def index():
    page = Form(hx_post=send, hx_target="#chatlist", hx_swap="beforeend")(
           Div(id="chatlist", cls="chat-box h-[73vh] overflow-y-auto"),
               Div(cls="flex space-x-2 mt-2")(
                   Group(ChatInput(), Button("Send", cls="btn btn-primary"))
               )
           )
    return Titled('Chatbot Demo', page)

# Handle the form submission
@app.post
def send(msg: str, messages: list[str] = None):
    if not messages: messages = []
    messages.append({
        "role": "user",
        "content": msg
    })
    
    # Get the response from ChatGPT
    response = {
        "role": "assistant",
        "content": "I'm sorry, I don't understand."
    }

    messages.append(response)
    
    return (ChatMessage(msg, True),    # The user's message
            ChatMessage(response["content"].rstrip() + f"\nConversation: \n{json.dumps(messages, indent=4)}", False), # The chatbot's response
            ChatInput()) # And clear the input field via an OOB swap

serve()