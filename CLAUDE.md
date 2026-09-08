# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**YouTube Summarizer** is a Streamlit web application that generates concise Japanese summaries of YouTube video transcripts using Claude via LangChain.

### Key Technologies
- **Frontend**: Streamlit (Python web framework)
- **LLM**: Anthropic Claude API (via `langchain-anthropic`)
- **Containerization**: Docker & Docker Compose
- **Dependencies**: LangChain, YouTube Transcript API, requests

### Architecture
Single-file Streamlit app (`src/main.py`) with modular functions:
- `init_page()` - Streamlit page configuration
- `select_model()` - Claude model selection (Haiku/Sonnet) via sidebar, sets `max_token = 4000`
- `get_video_metadata()` - Scrapes YouTube page to extract title and author (avoids pytube errors)
- `get_document()` - Fetches transcript from YouTube, splits into 4000-char chunks using `RecursiveCharacterTextSplitter`
- `summarize()` - Uses LangChain's map_reduce chain to summarize chunks independently, then combines summaries
- `main()` - Orchestrates flow: get URL → fetch transcript → summarize → display with metadata

**Key design decisions:**
- `add_video_info=False` in YoutubeLoader to prevent pytube internal errors
- Character-based chunking (not token-based) to avoid tiktoken dependency
- Fixed `max_token=4000` (sufficient for both models)
- Title/author fetched separately via JSON-LD scraping

## Setup

### Prerequisites
- Docker & Docker Compose
- Anthropic API key (https://console.anthropic.com)

### Quick Start
```bash
# 1. Create .env with API key
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# 2. Start container (dependencies already in requirements.txt)
docker compose up -d

# 3. Run the app
docker compose exec -it app streamlit run src/main.py --server.address=0.0.0.0
# Visit http://localhost:8501
```

### Dependency Management
```bash
# Add a package
docker compose exec -it app pip install <package>

# Save updated dependencies
docker compose exec -it app pip freeze > requirements.txt

# Rebuild with new dependencies
docker compose build --no-cache
docker compose up -d
```

### Debugging
```bash
# View logs
docker compose logs -f app

# Shell access
docker compose exec -it app bash
```

## Code Quality Notes

### Current State
- ✅ OpenAI references removed (pure Claude/Anthropic)
- ✅ No cost tracking (unnecessary for this use case)
- ✅ Error handling for missing transcripts and invalid URLs
- ✅ Streamlit session state for model persistence
- ⚠️ Code structure needs refactoring (see below)

### Known Structural Issues
1. **Leaky UI layer**: `get_document()` calls `st.spinner()` and raises exceptions; main() duplicates error handling
2. **Variable naming inconsistency**: `get_document()` returns `docs` (plural), main() receives as `document` (singular)
3. **Function responsibility blur**: `select_model()` mutates `st.session_state` internally instead of delegating to caller
4. **Comment language mix**: Japanese and English comments scattered; should be consistent (prefer Japanese)

### Refactoring Candidates
- Separate LoGIC (data fetching) from UI (Streamlit calls)
- Rename variables consistently (docs vs document)
- Move state initialization out of `select_model()`
- Consolidate error handling in `main()`

## Configuration

### Environment
- `ANTHROPIC_API_KEY`: Required, set in `.env` (gitignored)

### App Settings
- Port: 8501 (Streamlit default)
- Chunk size: 4000 characters
- Model context: 200K tokens (both Haiku and Sonnet)
