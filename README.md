# JARVIS_AI

A fully-featured AI voice assistant named Jarvis that combines conversational AI, real-time web search, speech recognition, text-to-speech, and image generation. Built with Python and powered by modern APIs.

## Features

- **Conversational AI Chatbot** - Uses Groq's `llama-3.3-70b-versatile` model for intelligent, context-aware conversations
- **Real-Time Web Search** - Integrates DuckDuckGo search engine to fetch live information from the internet
- **Speech Recognition** - Converts audio input to text with multi-language support (English, Hindi, etc.)
- **Text-to-Speech** - Converts AI responses to natural-sounding audio using Microsoft Edge TTS
- **Image Generation** - Creates AI-generated images based on text descriptions
- **Query Classification** - Automatically routes queries to appropriate handlers (general chat, realtime search, automation, etc.)
- **Multi-Language Support** - Recognizes Hindi and other languages, auto-translates to English
- **Chat History** - Maintains conversation logs for context awareness
- **GUI Interface** - PyQt5-based frontend for interactive use

## Tech Stack

- **Backend**: Python 3.10+
- **AI Models**: Groq API (LLaMA 3.3 70B), Cohere, HuggingFace
- **Speech**: Edge-TTS, Web Speech API (browser-based)
- **Search**: DuckDuckGo Search Library
- **Frontend**: PyQt5, Selenium
- **Data Storage**: JSON-based chat logs

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/JARVIS_AI.git
cd JARVIS_AI
```

2. Install dependencies:
```bash
pip install -r Requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## Setup

Add your API keys to `.env`:
- `GroqAPIKey` - Get from https://console.groq.com
- `CohereAPIKey` - Get from https://cohere.com
- `HuggingFaceAPIKey` - Get from https://huggingface.co
- `GeminiAPIKey` - Get from https://ai.google.dev
- Customize `Username`, `Assistantname`, `InputLanguage`, `AssistantVoice`

## Usage

```bash
# Run main chatbot
python Backend/Chatbot.py

# Use real-time search
python Backend/RealtimeSearchEngine.py "who is Elon Musk"

# Speech-to-text
python Backend/SpeechToText.py

# Text-to-speech
python Backend/TextToSpeech.py

# Image generation
python Backend/ImageGeneration.py
```

## Project Structure

```
JARVIS_AI/
├── Backend/          # Core AI modules
├── Frontend/         # GUI interface
├── Data/            # Chat logs & generated files
├── Main.py          # Entry point
└── Requirements.txt # Dependencies
```

## License

MIT License - Feel free to use and modify!

## Support

For issues or questions, open a GitHub issue.
