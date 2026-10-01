from agents import Agent, Runner, function_tool
from store_data import INVENTORY, DISCOUNT_CODES


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


agent = Agent(
    name="Corner Store Assistant",
    instructions=system_prompt,
    model="gpt-5.4-nano",
    tools=[check_stock]
)


def call_agent(user_prompt) -> str:
    global memory
    memory.append({
        "role": "user", "content": user_prompt
    })
    result = Runner.run_sync(agent, memory)
    memory = result.to_input_list()

    return result.final_output
