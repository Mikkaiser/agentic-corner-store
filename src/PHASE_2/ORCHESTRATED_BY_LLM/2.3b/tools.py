import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from store_data import INVENTORY, DISCOUNT_CODES
from agents import Agent, Runner, trace
from notifications import notify_owner
import json

MODEL_NAME = "gpt-5.4-mini"


def get_featured_product() -> dict:
    name, product = max(INVENTORY.items(), key=lambda item: item[1]["stock"])
    code, discount = next(
        (code, d) for code, d in DISCOUNT_CODES.items()
        if d["active"] and d["min_total"] == 0
    )
    return {"name": name, **product, "discount_code": code, "discount_percent": discount["percent"]}


intro = """
You are a marketing writer for a small neighbourhood corner store.
You write short promotional messages for the store owner to send to customers.
Use only the product, price and discount code given in the brief. Never invent prices, products or offers.
"""

warm_style = "Your style is warm and friendly, like a shopkeeper who knows every customer by name. Make the reader feel welcome and part of the neighbourhood."
witty_style = "Your style is witty and playful, with a light pun or clever twist. Keep it charming and never mean or over the top."
direct_style = "Your style is short and direct, like a busy shopkeeper. One or two sentences: the product, the price and the code, with no filler."

promo_manager_prompt = """
You are the promo manager of a small neighbourhood corner store.
You will receive a brief with the featured product, its price and its discount code.
Your job is to get a promotional message for it sent to the store owner for review.

Follow these steps in order:
1. Call each of the three writer tools (warm_writer, witty_writer, direct_writer) exactly once, passing the brief as the input, to get three drafts.
2. Choose the best draft for the store owner to send to customers. Do not rewrite it or mix drafts.
3. Call notify_owner exactly once, with the chosen draft. Never call it more than once.

When you call notify_owner:
- subject: a short title, such as "Promo ready to send"
- text_body: the chosen promotional message as plain text, exactly as written by the writer
- html_body: the same content as HTML. Use only <b>, <i>, <u>, <a href> and <font color> tags, with no other markup. Put the promotional message in bold and add a short line above it saying it is ready for review.

Never change the wording of the promotional message, its price or its discount code. Use only the product, price and discount code from the brief.
"""

warm_agent = Agent(name="Warm Writer", instructions=intro + warm_style, model=MODEL_NAME)
witty_agent = Agent(name="Witty Writer", instructions=intro + witty_style, model=MODEL_NAME)
direct_agent = Agent(name="Direct Writer", instructions=intro + direct_style, model=MODEL_NAME)

promo_manager = Agent(
    name="Promo Manager",
    instructions=promo_manager_prompt,
    model=MODEL_NAME,
    tools=[
        warm_agent.as_tool(tool_name="warm_writer", tool_description="Writes a warm and friendly promotional message for the brief it receives."),
        witty_agent.as_tool(tool_name="witty_writer", tool_description="Writes a witty and playful promotional message for the brief it receives."),
        direct_agent.as_tool(tool_name="direct_writer", tool_description="Writes a short and direct promotional message for the brief it receives."),
        notify_owner
    ]
)
