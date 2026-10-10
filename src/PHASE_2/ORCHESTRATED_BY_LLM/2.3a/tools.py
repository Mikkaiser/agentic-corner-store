from operator import ge
import uuid
from agents import Agent, Runner, function_tool, trace
from pydantic import BaseModel
from store_data import INVENTORY, DISCOUNT_CODES


MODEL_NAME = "gpt-5.4-nano"

class ProductItem(BaseModel):
    product_name: str
    quantity: int

session_id = str(uuid.uuid4())
memory = []

shopkeeper_prompt = """
You are the shopkeeper of a small corner store. You are friendly, short and polite.

Never state a price or a stock level from your own knowledge. Every number you give must come from a tool or from an earlier tool result in this conversation.

If a product does not exist in the store, say so politely and mention the kinds of products the store sells: dairy, bakery, fruit and vegetables, pantry items, drinks, snacks and household items.

If a customer asks for more units than are in stock, tell them how many are available and do not confirm the full order. Offer the available quantity instead.

If a question is not related to the store, politely decline and say you can only help with the store's products, prices and availability. Do not call any tool in that case.

Understand follow-up messages from the earlier conversation, such as "how much for 5 of them?" or "add 2 coffees to that". If it is truly unclear which product the customer means, ask which product they mean instead of guessing.
"""

inventory_specialist_prompt = """
You are the inventory specialist of a small corner store.
Answer only about availability, using the check_stock tool. Never state a stock level that did not come from the tool.
Report clearly when a product does not exist. If a product is given in singular and is not found, try the plural before saying it does not exist.
Reply with the facts only, no small talk.
"""

pricing_specialist_prompt = """
You are the pricing specialist of a small corner store.
Answer only about unit prices, basket totals and discounts, using the get_price, calculate_total and apply_discount tools. Never state a price that did not come from a tool.
Report clearly when a product or a discount code does not exist. If a product is given in singular and is not found, try the plural before saying it does not exist.
When a discount code is given, first get the total with calculate_total, then apply the code to that total with apply_discount. Report both the total and the discounted total.
Reply with the facts only, no small talk.
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

@function_tool
def apply_discount(code: str, total: float) -> str:
    """
    Returns the final result of the basket after applying the discount code.
    """
    item = DISCOUNT_CODES.get(code.upper())
    if item == None:
        return "code not found"
    
    percent = item.get("percent")
    min_total = item.get("min_total")
    active = item.get("active")

    if(total < min_total):
        return f"min total should be {min_total} for this discount code."
    if not active:
        return f"discount code {code} is NOT active at the moment."

    new_total = total - (total * percent / 100)

    return str(f"{new_total:.2f}")


inventory_specialist = Agent(
    name="Inventory Specialist",
    model=MODEL_NAME,
    tools=[check_stock],
    instructions=inventory_specialist_prompt
)

pricing_specialist = Agent(
    name="Inventory Specialist",
    model=MODEL_NAME,
    tools=[get_price, calculate_total, apply_discount],
    instructions=pricing_specialist_prompt
)

shopkeeper = Agent(
    name="Shopkeeper",
    instructions=shopkeeper_prompt,
    model=MODEL_NAME,
    tools=[
        inventory_specialist.as_tool(
            tool_name="inventory_specialist",
            tool_description="Ask whether a product exists and how many units are in stock. Send one clear question, for example: 'Is coffee in stock?'"
        ),
        pricing_specialist.as_tool(
            tool_name="pricing_specialist",
            tool_description="Ask for unit prices, the total of a basket (product names and quantities) and the result of applying a discount code. Send one clear request, for example: 'Total for 2 coffee, then apply SAVE10'."
        )
    ]
)

async def call_agent(user_prompt) -> None:
    global memory
    memory.append({"role": "user", "content": user_prompt})
    with trace("Corner Store Shopkeeper", group_id=session_id):
        result = await Runner.run(shopkeeper, memory)
    print(f"Agent: {result.final_output}")
    memory = result.to_input_list()
