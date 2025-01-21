# Feishu AI Assistant Bot

A Feishu (飞书) bot implementation that provides AI-powered chat capabilities and meeting scheduling functionality. The bot uses a graph-based architecture to handle different types of interactions and supports multiple AI models.

## Features

- 🤖 AI-powered chat interactions
- 📅 Intelligent meeting scheduling
- 🔄 Message deduplication system
- 🌐 WebSocket-based real-time communication
- 🎯 Multi-skill system (chat, meeting management)
- 🗃️ Interactive card interfaces for meeting creation

## Prerequisites

- Python 3.8+
- Feishu App credentials (APP_ID and APP_SECRET)
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd feishu-ai-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your Feishu credentials in `bot.py`:
```python
lark.APP_ID = "your_app_id"
lark.APP_SECRET = "your_app_secret"
lark.USER_ACCESS_TOKEN = "your_user_access_token"
```

## Usage

Run the bot:
```bash
python bot.py
```

## Features in Detail

### Message Handling
- Automatic message deduplication
- Support for text messages and interactive cards
- Real-time message processing through WebSocket connection

### Meeting Management
- Create meetings with title, date, time, and attendees
- Interactive meeting cards for confirmation
- Calendar integration for scheduling
- Support for meeting updates and queries

### AI Conversation
- Multi-skill routing system
- Context-aware responses
- Support for both chitchat and task-oriented conversations

## Dependencies

- anthropic: AI model integration
- python-dotenv: Environment variable management
- openai: OpenAI API integration
- tiktoken: Token handling
- lark-oapi: Feishu API SDK

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
