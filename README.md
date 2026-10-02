# 🛒 Agentic Corner Store Assistant

> 🚧 **Work in progress**: this exercise isn't finished yet. Some features listed below are still being built. See [Progress](#progress).

This is an interactive terminal assistant for a small neighbourhood store, built with the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/). Customers chat with it in plain language ("Do you have milk, and how much would 3 cost?"). The agent answers by calling **tools** for every fact, so it never guesses a price or a stock level.

I built it as a hands-on practice exercise for the core ideas of agentic apps:

- **Agents and system prompts**: a friendly, short-spoken store assistant that follows strict business rules
- **Function tools** (`@function_tool`): stock lookups, prices and basket totals come from code, not from the model's memory
- **Conversation memory**: follow-ups like *"how much for 5 of them?"* or *"add 2 coffees to that"* work across turns
- **Streaming**: replies show up word by word, with live `[tool] …` lines while tools run
- **Tracing**: each chat session can be found in the OpenAI traces dashboard under one workflow name and session id

The full brief is in [`exercise/corner_store_assistant_exercise.pdf`](exercise/corner_store_assistant_exercise.pdf).

## Example

```text
you> Do you have milk, and how much would 3 cost?
[tool] check_stock(product="milk") ... done
[tool] get_price(product="milk") ... done
[tool] calculate_total(items=[{"product": "milk", "quantity": 3}]) ... done
agent> Yes, we have milk in stock! It costs 7.00 AED each, so 3 bottles come to 21.00 AED.
```

## Business rules

The agent:

1. Is friendly, short and polite.
2. Never states a price or stock level from its own knowledge. Every number comes from a tool.
3. Politely says when a product doesn't exist and mentions what the store does sell.
4. Never confirms more units than are in stock, and offers the available quantity instead.
5. Declines off-topic questions without calling any tool.
6. Understands follow-ups from earlier turns, and asks for clarification when a reference is truly unclear.

## Progress

- [x] Project setup (uv, OpenAI Agents SDK, `.env` for the API key)
- [x] Store data: an expanded inventory (≈45 products across 7 categories, prices in AED) plus discount codes
- [x] System prompt covering all six business rules
- [x] `check_stock` tool
- [x] Basic chat loop with in-memory conversation history
- [x] `get_price` tool
- [x] `calculate_total` tool
- [x] Tracing with a custom workflow name and shared session id
- [ ] `exit` command to end the chat loop
- [ ] Streaming output with tool-call indicators
- [ ] Error handling, so a failing tool or a network error doesn't crash the loop
- [ ] *(Optional)* SQLite memory so sessions can be resumed after a restart
- [ ] *(Optional)* Experiments, such as an `apply_discount` tool

## Project structure

```text
.
├── exercise/
│   ├── corner_store_assistant_exercise.pdf   # Exercise brief
│   └── store_data_original.py                # Original store data from the brief
├── src/
│   ├── main.py         # Terminal chat loop
│   ├── tools.py        # Agent definition, system prompt, tools and memory
│   └── store_data.py   # Expanded inventory and discount codes
├── .env.example
└── pyproject.toml
```

## Getting started

You need Python 3.12+, [uv](https://docs.astral.sh/uv/) and an OpenAI API key.

```bash
# Install dependencies
uv sync

# Configure your API key
cp .env.example .env
# then edit .env and set OPENAI_API_KEY

# Run the assistant
uv run src/main.py
```

## Tech stack

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) (`openai-agents`)
- [python-dotenv](https://github.com/theskumar/python-dotenv) for loading the API key
- [uv](https://docs.astral.sh/uv/) for dependency management
