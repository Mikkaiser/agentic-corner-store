# 🛒🤖 Agentic Corner Store Assistant

This is an interactive terminal assistant for a small neighbourhood store, built with the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/). Customers chat with it in plain language ("Do you have milk, and how much would 3 cost?"). The agent answers by calling **tools** for every fact, so it never guesses a price or a stock level.

## Why I built it

I made this project to understand how an agent loop works inside: how tool calls flow between the model and the code, how streaming shows that work as it happens, and how tracing lets you follow each step afterwards.

I used the OpenAI Agents SDK, but the same structure works with any other agent framework. The concepts are the important part, not the library. The project covers these core ideas of agentic apps:

- **Agents and system prompts**: a friendly, short-spoken store assistant that follows strict business rules
- **Function tools** (`@function_tool`): stock lookups, prices, basket totals and discount codes come from code, not from the model's memory
- **Conversation memory**: follow-ups like *"how much for 5 of them?"* or *"add 2 coffees to that"* work across turns
- **Streaming**: replies show up word by word, with live `[tool] …` lines while tools run
- **Tracing**: each chat session can be found in the OpenAI traces dashboard under one workflow name and session id

The full brief is in [`exercise/corner_store_assistant_exercise.pdf`](exercise/corner_store_assistant_exercise.pdf). Phase 1 is the single agent built here; Phase 2 extends it step by step with multi-agent orchestration (parallel agents, agents as tools, handoffs and owner notifications).

## Example

![Demo: the assistant checks stock and prices for milk, adds 2 coffees to the basket, then applies the SAVE10 discount code](docs/demo.gif)

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
- [x] Streaming output with tool-call indicators
- [x] *(Optional)* `apply_discount` tool (checks the code exists, is active and meets the minimum total)
- [x] Phase 2, step 2.1: owner notifications (`notify_owner` tool, Pushover with a log-file fallback)
- [x] Phase 2, step 2.2: weekly promo orchestrated by code (three parallel writers, a picker, and a sender with forced tool use)
- [x] Phase 2, step 2.3a: the chat becomes a Shopkeeper that uses an Inventory Specialist and a Pricing Specialist as tools (agents as tools)

## Project structure

```text
.
├── docs/
│   └── demo.gif                              # Terminal demo shown above
├── exercise/
│   ├── corner_store_assistant_exercise.pdf   # Exercise brief
│   └── store_data_original.py                # Original store data from the brief
├── src/
│   ├── PHASE_1/
│   │   ├── main.py     # Async terminal chat loop
│   │   └── tools.py    # Agent definition, system prompt, tools and memory
│   ├── PHASE_2/
│   │   ├── notifications.py   # Owner notifications (Pushover with fallback)
│   │   ├── ORCHESTRATED_BY_CODE/promo.py   # Weekly promo workflow
│   │   └── ORCHESTRATED_BY_LLM/
│   │       ├── shopkeeper.png   # draw_graph of the Shopkeeper and its specialists
│   │       └── 2.3a/
│   │           ├── main.py      # Async terminal chat loop
│   │           └── tools.py     # Shopkeeper, specialists, tools and memory
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
# optional: set PUSHOVER_USER and PUSHOVER_TOKEN for owner push notifications

# Run the assistant
PYTHONPATH=src uv run src/PHASE_1/main.py
```

The Phase 1 chat needs `PYTHONPATH=src` so it can import the shared `store_data.py`. The Phase 2 scripts add the shared folders to the import path themselves, so they run without it:

```bash
uv run src/PHASE_2/ORCHESTRATED_BY_CODE/promo.py
uv run src/PHASE_2/ORCHESTRATED_BY_LLM/2.3a/main.py
```

The promo script picks the product with the most stock and an active discount code, has three writers draft a message in parallel, picks the best one and sends it to the owner. This sends a real push notification when Pushover is configured. Without `PUSHOVER_USER` and `PUSHOVER_TOKEN`, the notification is printed and appended to `owner_notifications.log` instead.

The 2.3a chat is the Phase 1 assistant split into specialists. The Shopkeeper talks to the customer and owns no function tools. It calls the Inventory Specialist (`check_stock`) for availability and the Pricing Specialist (`get_price`, `calculate_total`, `apply_discount`) for prices, totals and discounts, each one wrapped with `as_tool`. `shopkeeper.png` is the `draw_graph` picture of that structure, which needs the Graphviz `dot` program installed (`sudo apt install graphviz`).

## Tech stack

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) (`openai-agents`)
- [Pushover](https://pushover.net/) for owner push notifications
- [python-dotenv](https://github.com/theskumar/python-dotenv) for loading the API key
- [uv](https://docs.astral.sh/uv/) for dependency management
