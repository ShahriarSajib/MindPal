# ⚡ MindPal AI Chatbot

> A high-performance, full-stack conversational AI platform built with Python, Streamlit, and LangChain — powered by the **Gemini Flash-Lite Engine**.

🌐 **Live Demo:** [mindpal-ai-chatbot.streamlit.app](https://mindpal-ai-chatbot.streamlit.app/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Cloud Deployment](#cloud-deployment)

---

## Overview

MindPal is a multimodal AI chatbot that leverages LangChain and Google's Gemini model to deliver low-latency, context-aware conversations. It supports file uploads, persistent memory across sessions, and a clean, modern interface built entirely on Streamlit.

---

## Key Features

| Feature                      | Description                                                                             |
| ---------------------------- | --------------------------------------------------------------------------------------- |
| 🏎️ **Live Token Streaming**  | Word-by-word output via Python async generators and LangChain token-level streaming     |
| 📂 **Multimodal File Input** | Upload images (`.png`, `.jpg`, `.jpeg`) and text (`.txt`) directly into the LLM context |
| 🗄️ **Persistent Memory**     | SQLite-backed conversation history that survives tab closures and browser refreshes     |
| 🗑️ **Session Management**    | Switch conversations, delete individual threads, or wipe the full database              |
| 📱 **Unified Input Hub**     | File attachment and prompt bar merged into a single bottom navigation row               |

---

## Tech Stack

| Layer                        | Technology                                |
| ---------------------------- | ----------------------------------------- |
| **Frontend & Orchestration** | Streamlit                                 |
| **AI Framework**             | LangChain Core / `langchain-google-genai` |
| **Foundation Model**         | Google Gemini Flash-Lite                  |
| **Persistent Storage**       | SQLite3                                   |
| **Image Processing**         | Pillow (PIL)                              |

---

## Project Structure

```
mindpal-ai/
│
├── main.py               # Application entry point
├── chat_engine.py        # Streaming generators & base64 vision handlers
├── database.py           # SQLite transactions and data loading
├── ui_components.py      # Modular UI elements and layout rendering
├── config.py             # CSS injection and credential management
├── requirements.txt      # Dependency manifest
└── .gitignore            # Excludes local DB, caches, and env variables
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- A [Google AI Studio](https://aistudio.google.com/) API key

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/ShahriarSajib/MindPal.git
cd mindpal-ai
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY="your_google_api_key_here"
```

**5. Run the app**

```bash
streamlit run main.py
```

The app will be available at `http://localhost:8501`.

---

## Cloud Deployment

To deploy on **Streamlit Community Cloud**:

1. Push your repository to GitHub (ensure `.env` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set **Main file path** to `main.py`
4. Under **Advanced Settings → Secrets**, add your credentials in TOML format:

```toml
GOOGLE_API_KEY = "your_google_api_key_here"
```

---

## License

This project is open-source. See [LICENSE](LICENSE) for details.
