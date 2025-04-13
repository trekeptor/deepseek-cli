# Please install OpenAI SDK first: `pip3 install openai`

import os
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    # base_url="https://openrouter.ai/api/v1",
    # api_key=os.getenv("OPENROUTER_API_KEY"),
)

def get_available_models():
    try:
        models = client.models.list()
        return [model.id for model in models]
    except Exception as e:
        print(f"Error fetching models: {e}")
        return ["deepseek-reasoner"]  # Fallback to default model

def select_model():
    models = get_available_models()
    print("\nAvailable models:")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    while True:
        try:
            choice = int(input("\nSelect a model (enter the number): "))
            if 1 <= choice <= len(models):
                return models[choice - 1]
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

# Get user's model selection
selected_model = select_model()
print(f"\nSelected model: {selected_model}\n")

# Initialize conversation history
messages = [
    {"role": "system", "content": "You are a helpful assistant"}
]

# Initialize prompt sessions with style
user_session = PromptSession()  # Renamed from 'session' to 'user_session'
assistant_session = PromptSession()  # New session for assistant output
style = Style.from_dict({
    'prompt': 'green bold',
    'assistant': 'blue',
})

# Create a unique log file name when the program starts
log_file_name = f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

# Add logging function
def log_message(role, content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_name, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {role}: {content}\n")

# Log the start of the session
log_message("System", "Chat session started")

# Interactive chat loop
try:
    while True:
        # Get user input with better editing experience
        user_input = user_session.prompt(
            "You: ",
            style=style,
            multiline=True,
        )
        
        # Skip empty inputs
        if not user_input.strip():
            continue
            
        messages.append({"role": "user", "content": user_input})
        log_message("User", user_input)  # Log user message

        # Get streaming response from API
        response = client.chat.completions.create(
            model=selected_model,  # Use the selected model instead of hardcoded one
            messages=messages,
            stream=True  # Enable streaming
        )

        # Print assistant's response as it streams using prompt_toolkit
        print("\n", end="")  # Add a newline before assistant response
        assistant_response = ""
        assistant_session.app.output.write_raw("Assistant: ")  # Add prefix
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                assistant_session.app.output.write_raw(content)
                assistant_session.app.output.flush()
                assistant_response += content
        print("\n")  # Add a newline after response
        
        # Add assistant's response to conversation history
        messages.append({"role": "assistant", "content": assistant_response})
        log_message("Assistant", assistant_response)  # Log assistant message

except KeyboardInterrupt:
    print("\nGoodbye!")
    log_message("System", "Chat session ended")  # Log session end
