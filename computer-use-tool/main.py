from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from dotenv import load_dotenv
load_dotenv()

import asyncio

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp')


async def main():
    agent = Agent(
        task="open google.com and create new  account with these credentials  Email: <uniquetales28271> and password: <since2070> then search for 'how to make a cake' and open the first link",
        llm=llm,

    )
    result = await agent.run()
    print(result)

asyncio.run(main())