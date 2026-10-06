import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from store_data import INVENTORY
from agents import Agent, Runner, trace
import asyncio
import json

MODEL_NAME="gpt-5.4-mini"

def get_featured_product() -> dict:
    name, product = max(INVENTORY.items(), key=lambda item: item[1]["stock"])
    return {"name": name, **product}

intro = """
You are a marketing writer for a small neighbourhood corner store.
You write short promotional messages for the store owner to send to customers.
Use only the product, price and discount code given in the brief. Never invent prices, products or offers.
"""

warm_style = "Your style is warm and friendly, like a shopkeeper who knows every customer by name. Make the reader feel welcome and part of the neighbourhood."
witty_style = "Your style is witty and playful, with a light pun or clever twist. Keep it charming and never mean or over the top."
direct_style = "Your style is short and direct, like a busy shopkeeper. One or two sentences: the product, the price and the code, with no filler."

warm_agent = Agent(
    name="Warm Writer", 
    instructions=intro + warm_style,
    model=MODEL_NAME
)
witty_agent = Agent(
    name="Witty Writer", 
    instructions=intro + witty_style,
    model=MODEL_NAME
)
direct_agent = Agent(
    name="Direct Writer", 
    instructions=intro + direct_style,
    model=MODEL_NAME
)

async def main():
    product = get_featured_product()
    brief = json.dumps(product)

    with trace("Promo: ORCHESTRATED BY CODE"):
        await asyncio.gather(
            Runner.run(warm_agent, brief),
            Runner.run(direct_agent, brief),
            Runner.run(witty_agent, brief)
        )

asyncio.run(main())

