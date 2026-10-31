# ReAct Agent

**Live Demo:** [https://reserach-agent.onrender.com](https://reserach-agent.onrender.com)

A Streamlit web app powered by a **ReAct (Reasoning + Acting)** agent built with LangGraph, Gemini, Tavily Search, and Weatherstack.

---

## Features

- **Web Search** — Searches the web in real-time using Tavily
- **Weather Lookup** — Fetches live weather data for any city via Weatherstack
- **ReAct Agent** — Uses Gemini 2.5 Flash Lite with chain-of-thought reasoning
- **Simple UI** — Enter a query, click Run, get an answer
- **Step Viewer** — Expandable panel showing all agent reasoning steps

---

## Project Structure

```
research/
├── app.py               # Streamlit app
├── agent_demo.ipynb     # Jupyter notebook (prototyping)
├── requirements.txt     # Python dependencies
├── .env                 # API keys (not committed)
└── README.md
```

---

## Setup

### 1. Clone / navigate to the project

```bash
cd "d:\Agentic AI\langchain-agent\research"
```

### 2. Activate conda environment

```bash
conda activate aii_agents
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up API keys

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
WEATHERSTACK_API_KEY=your_weatherstack_api_key
```

| Key | Get it from |
|-----|-------------|
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `TAVILY_API_KEY` | [Tavily](https://app.tavily.com) |
| `WEATHERSTACK_API_KEY` | [Weatherstack](https://weatherstack.com) |

---

## Run the App

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## How It Works

```
User Query
    │
    ▼
ReAct Agent (Gemini 2.5 Flash Lite)
    │
    ├── Tavily Search Tool  →  Web search results
    └── Weather Tool        →  Live weather data
    │
    ▼
Final Answer → Streamlit UI
```

The agent follows a **Thought → Action → Observation** loop until it arrives at a final answer.

---

## Tech Stack

| Component | Library |
|-----------|---------|
| UI | Streamlit |
| LLM | Gemini 2.5 Flash Lite (`langchain-google-genai`) |
| Agent Framework | LangGraph (`create_react_agent`) |
| Web Search | Tavily (`langchain-community`) |
| Weather | Weatherstack API |
| Prompt | `hwchase17/react` from LangChain Hub |

---

## Example Queries

- `What is the weather in Kathmandu?`
- `Find the capital of Nepal and its current weather`
- `Latest news about artificial intelligence`
- `What is the population of Tokyo?`
