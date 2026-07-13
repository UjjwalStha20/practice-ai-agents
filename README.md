# AI Travel Agent

An intelligent travel planning assistant powered by a local LLM (Ollama) with function-calling capabilities. The agent helps users plan trips to destinations across Nepal by providing weather info, hotel recommendations, local food suggestions, and attraction details.

## Features

- **Weather Lookup** – Fetches real-time weather data via the Weatherstack API
- **Hotel Search** – Recommends hotels in a given city with optional budget filtering
- **Food Search** – Suggests local cuisine options within a price range
- **Attraction Search** – Lists popular attractions, optionally filtered by type
- **Multi-tool orchestration** – The LLM automatically decides which tools to call based on the user's request

## Tech Stack

- **Python 3.10+**
- **Ollama** (local LLM) – tested with `qwen2.5:3b`
- **OpenAI Python SDK** (compatible with Ollama's API)
- **Weatherstack API** (for live weather data)
- Mock data for hotels, food, and attractions across **12 Nepalese cities**

## Supported Destinations

Kathmandu, Pokhara, Chitwan, Lumbini, Nagarkot, Bandipur, Dhulikhel, Janakpur, Ilam, Jomsom, Gorkha, Rara, Daman, Bhaktapur, Lalitpur

## Setup

1. **Clone the repo and create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate
```

2. **Install dependencies:**

```bash
pip install openai python-dotenv requests
```

3. **Configure environment variables:**

Copy `.env.example` to `.env` and add your API keys:

```
WEATHER_API_KEY=your_weatherstack_key
```

> Note: The `OPENAI_API_KEY` in `.env` is not required—the client is hardcoded to use Ollama's API key (`ollama`).

4. **Run Ollama locally** (ensure the `qwen2.5:3b` model is pulled):

```bash
ollama pull qwen2.5:3b
ollama serve
```

5. **Run the agent:**

```bash
python main.py
```

## Usage

Once running, enter natural-language travel queries at the prompt:

```
Enter your question (or type 'exit' to quit): What's the weather like in Pokhara and find me a hotel under 6000 NPR?
```

The agent will call the appropriate tools and return a friendly summary.

## Project Structure

```
├── agent.py       – TravelAgent class (message loop + tool execution)
├── config.py      – Tool definitions (OpenAI-compatible function schemas)
├── main.py        – CLI entry point
├── mock_data.py   – Static travel data for 12 Nepalese cities
├── models.py      – (reserved for Pydantic models)
├── prompts.py     – System prompt instructing the agent's behavior
├── tools.py       – Tool implementations (weather, hotels, food, attractions)
├── utils.py       – (reserved for utility functions)
├── .env.example   – Environment variable template
└── .gitignore
```

## How It Works

1. User enters a query
2. The system prompt instructs the LLM to act as a travel planner
3. The LLM decides which functions to call (weather, hotels, etc.) and returns tool call requests
4. The agent executes each tool with the arguments provided by the LLM
5. Tool results are fed back to the LLM as new messages
6. The LLM produces a natural-language summary for the user
7. Steps 3–6 repeat until no more tool calls are needed
