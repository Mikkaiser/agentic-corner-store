import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from dotenv import load_dotenv
from tools import call_agent
import asyncio

load_dotenv()


async def main():
    print('Agentic Corner Store Exercise: \n')
    print('--------------------------------')
    while True:
        user_prompt = input('You: ')
        await call_agent(user_prompt)

asyncio.run(main())
