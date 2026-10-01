from dotenv import load_dotenv
import os
from tools import call_agent
load_dotenv()

print('Agentic Corner Store Exercise: \n')
print('--------------------------------')


while True:
    user_prompt = input('You: ')
    response = call_agent(user_prompt)
    print("Agent: " + response)


