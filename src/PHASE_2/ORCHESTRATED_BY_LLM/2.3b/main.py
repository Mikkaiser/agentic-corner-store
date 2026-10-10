from dotenv import load_dotenv
from tools import Runner, trace, json, get_featured_product, promo_manager
import asyncio

load_dotenv()


async def main():
    brief = json.dumps(get_featured_product())

    with trace("Promo: ORCHESTRATED BY LLM"):
        await Runner.run(promo_manager, brief)

asyncio.run(main())
