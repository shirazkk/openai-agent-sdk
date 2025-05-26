"""
How to configure LLM Providers (Other than OpenAI) at different levels (Global, Run and Agent)?

"""

# 1. AGENT LEVEL

# import asyncio
# from openai import AsyncOpenAI
# from agents import Agent , OpenAIChatCompletionsModel , Runner , set_tracing_disabled
# import os 
# from dotenv import load_dotenv

# load_dotenv()
# gemini_api_key = os.getenv("GOOGLE_API_KEY")

# client = AsyncOpenAI(
#     api_key= gemini_api_key,
#     base_url= "https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# set_tracing_disabled(disabled=True)

# async def main():
#     agent = Agent(
#         name="Assistant",
#         instructions="You only respond in python language",
#         model= OpenAIChatCompletionsModel(
#             model= "gemini-2.0-flash",
#             openai_client= client
#         )
#     )

#     result = await Runner.run(
#         agent,
#         "who is founder of pakistan",
#     )

#     print(result.final_output)


# if __name__ == "__main__":
#     asyncio.run(main())



# 2. RUN LEVEL

from agents import Agent , AsyncOpenAI , OpenAIChatCompletionsModel , Runner
from agents.run import RunConfig
import os 
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")


external_client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    "gemini-2.0-flash",
     openai_client= external_client
)

config = RunConfig(
    model= model,
    model_provider = external_client,
    tracing_disabled= True
)

agent = Agent(
    name= "Ai Agent",
    instructions= "You are Ai assistance agent"
)

run = Runner.run_sync(
    agent,
    "Tell me the latest news of Ai Agent",
    run_config= config
)

print(run.final_output)


# 3. GLOBAL


# from agents import Agent , AsyncOpenAI , OpenAIChatCompletionsModel , Runner, set_default_openai_client
# import os 
# from dotenv import load_dotenv

# load_dotenv()
# gemini_api_key = os.getenv("GOOGLE_API_KEY")


# external_client = AsyncOpenAI(
#     api_key= gemini_api_key,
#     base_url= "https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# set_default_openai_client(external_client)

# model = OpenAIChatCompletionsModel(
#     "gemini/gemini-1.5-flash",
#      openai_client= external_client
# )


# agent = Agent(
#     name= "Ai Agent",
#     instructions= "You are Ai assistance agent",
#     model= model
# )

# run = Runner.run_sync(
#     agent,
#     "Tell me the latest news of Ai Agent",
# )

# print(run.final_output)







