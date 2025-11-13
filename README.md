# AI Chat Project (with A4F API)

This project is a simple yet powerful AI chat application that leverages the free AI APIs provided by [A4F](https://a4f.com). It's a great starting point for developers looking to experiment with different AI models without worrying about API costs.

##  Features

*   **Chat with Multiple AI Models:** Easily switch between different AI models available through the A4F API.
*   **Conversation Memory:** The chat system remembers previous parts of your conversation for better context.
*   **Smart Memory Cleaning:** A utility script is included to automatically filter and remove less relevant messages from the chat history, keeping your memory focused and efficient.

##  Project Files

*   `ai api 2.0.py`: The main application to run the chat interface.
*   `clean.py`: A script to process and clean the chat history.
*   `memory.json`: Stores the complete, raw chat history.
*   `memory_clean.json`: Stores the cleaned and more concise chat history.
*   `config.example.json`: Example configuration file.

##  Getting Started

### 1. Prerequisites

Make sure you have Python installed. You will also need to install the required libraries:

```bash
pip install openai sentence-transformers
```

### 2. Configuration

Rename `config.example.json` to `config.json` and add your A4F API key. You can get a free API key from the [A4F website](https://a4f.com).

### 3. Run the Chat

To start the chat application, run the following command in your terminal:

```bash
python "ai api 2.0.py"
```

### 4. Clean Chat Memory

After you've had a few conversations, you can run the cleaning script to optimize the chat memory:

```bash
python clean.py
```

---

> **Note on A4F API:** This project uses the A4F API because it provides free access to a variety of AI models. This is a great resource for developers and hobbyists who want to build AI-powered applications without the financial burden of paid APIs. We are not affiliated with A4F, just happy users!