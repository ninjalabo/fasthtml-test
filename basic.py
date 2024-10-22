from fasthtml.common import *
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Set up the app, including daisyui and tailwind for the chat component
hdrs = (picolink, Script(src="https://cdn.tailwindcss.com"),
        Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css"))
app = FastHTML(hdrs=hdrs, cls="p-4 max-w-lg mx-auto")

# Load the GPT-2 model and tokenizer
model_name = "gpt2"  # You can also use "gpt2-medium", "gpt2-large", etc.
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Function to get GPT-2 response
def get_gpt2_response(prompt):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Chat message component (renders a chat bubble)
def ChatMessage(msg, user):
    bubble_class = "chat-bubble-primary" if user else 'chat-bubble-secondary'
    chat_class = "chat-end" if user else 'chat-start'
    return Div(cls=f"chat {chat_class}")(
               Div('user' if user else 'assistant', cls="chat-header"),
               Div(msg, cls=f"chat-bubble {bubble_class}"),
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
def send(msg:str, messages:list[str]=None):
    if not messages: messages = []
    messages.append(msg.rstrip())
    
    # Prepare the prompt for GPT-2
    prompt = " ".join(messages)
    
    # Get the response from GPT-2
    r = get_gpt2_response(prompt)
    
    return (ChatMessage(msg, True),    # The user's message
            ChatMessage(r.rstrip(), False), # The chatbot's response
            ChatInput()) # And clear the input field via an OOB swap

serve()