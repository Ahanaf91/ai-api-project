# AI API 2.0 Project

This project demonstrates an AI chat system using the A4F API.

## Features:
- Chat with various AI models.
- Memory system to retain conversation context.
- Cleaning utility to filter out "unuseful" chat messages based on semantic similarity.

## Files:
- `ai api 2.0.py`: The main chat application.
- `clean.py`: Script to clean the chat memory.
- `memory.json`: Stores raw chat history.
- `memory_clean.json`: Stores cleaned chat history.

## Setup:
1. Install dependencies (e.g., `openai`, `sentence-transformers`).
2. Run `ai api 2.0.py` to start chatting.
3. Run `clean.py` to clean your chat memory.
