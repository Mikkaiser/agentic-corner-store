import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from store_data import INVENTORY, DISCOUNT_CODES
from agents import Agent, Runner, trace, ModelSettings
import asyncio
import json
from dotenv import load_dotenv
from notifications import notify_owner

load_dotenv()

MODEL_NAME="gpt-5.4-mini"

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
promo_picker_prompt = """
You are the editor for a small neighbourhood corner store.
You will receive a brief with the featured product, its price and its discount code, followed by several promotional messages written for it.
Pick the one message the store owner should send to customers.

Reply one with the chosen message, nothing else.
"""
sender_prompt = """
You are the assistant of a small neighbourhood corner store owner.
You will receive the promotional message that was chosen to be sent to customers.
Use the notify_owner tool exactly once to tell the owner the message is ready for review.

When you call the tool:
- subject: a short title, such as "Promo ready to send"
- text_body: the promotional message as plain text, exactly as you received it
- html_body: the same content as HTML. Use only <b>, <i>, <u>, <a href> and <font color> tags, with no other markup. Put the promotional message in bold and add a short line above it saying it is ready for review.

Never change the wording of the promotional message, its price or its discount code.
"""

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
        writters_output = await asyncio.gather(
            Runner.run(warm_agent, brief),
            Runner.run(direct_agent, brief),
            Runner.run(witty_agent, brief)
        )
        outputs = [result.final_output for result in writters_output]

        picker = Agent(
            name="Promo Picker",
            instructions = promo_picker_prompt + "\nOptions: \n" + "\n\n".join(outputs),
            model=MODEL_NAME
        )

        picker_choice = await Runner.run(picker, brief)
        
        sender = Agent(
            name="Promo Sender",
            instructions = sender_prompt,
            model=MODEL_NAME,
            tools=[notify_owner],
            model_settings=ModelSettings(tool_choice="required")
        )

        await Runner.run(sender, picker_choice.final_output)

asyncio.run(main())

