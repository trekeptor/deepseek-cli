
# AI Chat CLI

A command-line interface for chatting with AI models using the OpenAI-compatible API format. Currently configured to work with DeepSeek and OpenRouter APIs.

## Features

- Interactive command-line chat interface
- Multi-line input support with editing capabilities
- Real-time streaming of AI responses
- Automatic chat logging with timestamped files
- Configurable AI model selection
- Color-coded interface for better readability

## Prerequisites

- Python 3.6+
- pip (Python package installer)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install the required packages:
```bash
pip install openai python-dotenv prompt_toolkit
```

3. Create a `.env` file in the project root and add your API keys:
```
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Usage

1. Run the chat interface:
```bash
python main.py
```

2. Type your messages and press Enter to send. For multi-line messages:
   - Press Enter to start a new line
   - Press Esc + Enter to send the message

3. Press Ctrl+C to exit the chat

## Chat Logs

Each chat session is automatically logged to a unique file in the format:
`chat_log_YYYYMMDD_HHMMSS.txt`

The logs include:
- Timestamp for each message
- Role of the sender (User/Assistant/System)
- Complete message content

## Configuration

You can modify the following in `main.py`:
- AI model selection (currently set to "deepseek-reasoner")
- API endpoints (DeepSeek or OpenRouter)
- System prompt
- Interface styling

## License

[Your chosen license]

## Contributing

Feel free to open issues or submit pull requests for any improvements.
