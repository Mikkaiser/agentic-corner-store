from agents import Agent, Runner, function_tool, trace
from store_data import INVENTORY, DISCOUNT_CODES
from pydantic import BaseModel
import uuid

class ProductItem(BaseModel):
    product_name: str
    quantity: int

session_id=str(uuid.uuid4())

memory = []

system_prompt = """

You are a friendly assistant for a small corner store. Keep your answers short and polite.

Never state a price or a stock level from your own knowledge. Every number you give must come from a tool (check_stock, get_price, calculate_total) or from an earlier tool result in this conversation. Use the tools whenever a customer asks about availability, prices or totals.

If a product does not exist in the store, say so politely and mention the kinds of products the store sells: dairy, bakery, fruit and vegetables, pantry items, drinks, snacks and household items.

If a customer asks for more units than are in stock, tell them how many are available and do not confirm the full order. Offer the available quantity instead.

If a question is not related to the store, politely decline and say you can only help with the store's products, prices and availability. Do not call any tool in that case.

Understand follow-up messages from the earlier conversation, such as "how much for 5 of them?" or "add 2 coffees to that". If it is truly unclear which product the customer means, ask which product they mean instead of guessing.

"""

@function_tool
def check_stock(product_name: str) -> str:
    """Returns how many units are in stock. Reports clearly
    when the product does not exist in the store."""
    item = INVENTORY.get(product_name, "NOT FOUND")
    if(item == "NOT FOUND"):
        return item

    stock = item.get("stock")
    return str(stock)


def get_price_helper(product_name) -> float | None:
    item = INVENTORY.get(product_name, None)
    if(item is None):
        return None

    price = item.get("price")
    return price

@function_tool
def get_price(product_name: str) -> str:
    """Returns the unit price. Reports clearly when the
        product does not exist. in case the user provides the product
        in singular and you can't fetch by the name, try with plural before
        confirming it doesn't exist"""
    price = get_price_helper(product_name)
    if price is None:
        return "Not Found"
    return str(f"{price:.2f} AED")

@function_tool
def calculate_total(items: list[ProductItem]) -> str:
    """Returns the total cost of the basket by multiplying
        each unit price by its quantity. Check the stock first.
        in case the user writes incorrect gramatical names, search for the closest match of what he meant.
        Tell the user if some item is not available.
        in case the user provides the product
        in singular and you can't fetch by the name, try with plural before
        confirming it doesn't exist."""
    total = 0
    for item in items:
        price = get_price_helper(item.product_name)
        if price is None:
            return f"{item.product_name} Not Found"
        total += price * item.quantity
    return str(f"{total:.2f} AED")

    


agent = Agent(
    name="Corner Store Assistant",
    instructions=system_prompt,
    model="gpt-5.4-nano",
    tools=[check_stock, get_price, calculate_total]
)


def call_agent(user_prompt) -> str:
    global memory
    memory.append({
        "role": "user", "content": user_prompt
    })
    with trace("Corner Store Assistant", group_id=session_id):
        result = Runner.run_sync(agent, memory)
    memory = result.to_input_list()

    return result.final_output
