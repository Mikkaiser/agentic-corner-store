import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from dotenv import load_dotenv
from tools import call_agent
from agents.extensions.visualization import draw_graph
import asyncio
from tools import shopkeeper


load_dotenv()


async def main():
    draw_graph(shopkeeper, filename="shopkeeper.png")
    print('Agentic Corner Store Exercise: \n')
    print('--------------------------------')
    while True:
        user_prompt = input('You: ')
        await call_agent(user_prompt)

asyncio.run(main())
