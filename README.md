# YouTube Summarizer 🎞️

A powerful Streamlit web application that automatically generates concise Japanese summaries of YouTube video transcripts using Claude AI.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.63+-red)
![LangChain](https://img.shields.io/badge/LangChain-1.4+-green)
![Claude](https://img.shields.io/badge/Claude-API-blueviolet)

## Features

- 🎯 **Automatic Summarization** - Converts long YouTube transcripts into concise Japanese summaries
- 🤖 **Claude AI Powered** - Uses state-of-the-art Claude models (Haiku & Sonnet)
- 🎚️ **Model Selection** - Choose between Haiku (fast & affordable) or Sonnet (more powerful)
- 📺 **Video Metadata** - Displays video title and author automatically
- 🔄 **Map-Reduce Strategy** - Handles long transcripts by summarizing chunks independently then combining
- 🐳 **Docker Support** - Easy deployment with Docker & Docker Compose
- 🌐 **Web Interface** - Clean, user-friendly Streamlit interface

## Prerequisites

- Docker & Docker Compose
- Anthropic API key ([get it here](https://console.anthropic.com))
- Internet connection

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/youtube-summarizer.git
cd youtube-summarizer
```

### 2. Set Up API Key
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Start the Application
```bash
docker compose up -d
```

### 4. Access the App
Open your browser and visit: **http://localhost:8501**

## Usage

1. **Enter YouTube URL** - Paste any YouTube video URL in the input field
2. **Select Model** - Choose Claude Haiku (faster) or Claude Sonnet (more detailed)
3. **Get Summary** - Click and wait for the AI to summarize the transcript
4. **View Results** - See the summary with original transcript below

## Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Rapid Python web app development
- **LLM**: [Claude API](https://www.anthropic.com/api) via Anthropic
- **Framework**: [LangChain](https://www.langchain.com/) - LLM orchestration
- **Containerization**: Docker & Docker Compose
- **Libraries**:
  - `langchain-anthropic` - Claude integration
  - `langchain-community` - YouTube transcript loader
  - `langchain-text-splitters` - Smart text chunking
  - `youtube-transcript-api` - Extract video transcripts
  - `requests` - HTTP client for metadata scraping

## Project Structure

```
youtube-summarizer/
├── src/
│   └── main.py           # Main Streamlit application
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile           # Docker image specification
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (API key)
├── .env.example         # Example environment file
├── .gitignore          # Git ignore rules
├── CLAUDE.md           # Development guide
└── README.md           # This file
```

## How It Works

### Architecture
The app uses a **map-reduce summarization strategy** to handle videos of any length:

1. **Load** - Fetches YouTube transcript using LangChain's YoutubeLoader
2. **Split** - Divides transcript into 4000-character chunks for optimal processing
3. **Map** - Summarizes each chunk independently with Claude
4. **Reduce** - Combines individual summaries into one coherent summary
5. **Display** - Shows video metadata, summary, and original text

### Key Design Decisions
- **No pytube errors**: Uses `add_video_info=False` to avoid internal pytube issues
- **Character-based chunking**: Avoids heavy tiktoken dependency
- **Separate metadata fetching**: Extracts title & author via JSON-LD scraping
- **Fixed chunk size**: 4000 characters proven sufficient for both models

## Configuration

### Environment Variables
Set these in your `.env` file:

```bash
ANTHROPIC_API_KEY=sk-ant-...  # Your Anthropic API key
```

### App Settings
- **Port**: 8501 (default Streamlit port)
- **Chunk Size**: 4000 characters
- **Model Context**: 200K tokens (both Haiku and Sonnet)

## Development

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Basic knowledge of Streamlit and LangChain

### Local Development Setup

```bash
# Start container
docker compose up -d

# Install dependencies
docker compose exec -it app pip install -r requirements.txt

# Run the app
docker compose exec -it app streamlit run src/main.py --server.address=0.0.0.0
```

### Add New Dependencies

```bash
# Install in container
docker compose exec -it app pip install <package-name>

# Update requirements.txt
docker compose exec -it app pip freeze > requirements.txt

# Rebuild container
docker compose build --no-cache
docker compose down && docker compose up -d
```

### Code Quality

This project follows clean code principles:
- Modular function design with clear responsibilities
- Comprehensive error handling
- Type hints where appropriate
- Japanese comments for clarity
- Separation of UI and logic layers

See [CLAUDE.md](./CLAUDE.md) for detailed development guidance.

## Troubleshooting

### "Could not retrieve transcript"
- Ensure the video has captions enabled
- Try a different video
- Check your internet connection

### "Invalid YouTube URL"
- Verify the URL format: `https://www.youtube.com/watch?v=VIDEO_ID`
- Ensure you're using a direct YouTube link

### API Key Errors
- Confirm your API key is correct in `.env`
- Check your API key has proper permissions at https://console.anthropic.com
- Ensure it starts with `sk-ant-`

### Container Won't Start
```bash
# Rebuild the image
docker compose build --no-cache

# Restart containers
docker compose down && docker compose up -d

# Check logs
docker compose logs -f app
```

## Performance

- **Haiku Model**: ~10-30 seconds for typical video (5-15 mins)
- **Sonnet Model**: ~15-45 seconds for typical video (5-15 mins)
- Processing time depends on video length and transcript size

## Limitations

- Only works with videos that have English or Japanese captions
- Long videos (2+ hours) may take several minutes to summarize
- Requires active internet connection for API calls

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For issues, questions, or suggestions:
- Open an [GitHub Issue](https://github.com/yourusername/youtube-summarizer/issues)
- Check existing issues for solutions
- Review the [CLAUDE.md](./CLAUDE.md) development guide

## Acknowledgments

- [Anthropic](https://www.anthropic.com/) for the Claude API
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [LangChain](https://www.langchain.com/) for LLM orchestration tools
- [YouTube Transcript API](https://github.com/jdelatorrealba/youtube-transcript-api) for transcript extraction

## Roadmap

- [ ] Support for multiple languages (not just Japanese)
- [ ] Batch processing for multiple videos
- [ ] Video-based summarization (audio analysis)
- [ ] Custom summary length options
- [ ] Export summaries to PDF/DOCX
- [ ] API endpoint for programmatic access

---

**Made with ❤️ using Claude AI**
