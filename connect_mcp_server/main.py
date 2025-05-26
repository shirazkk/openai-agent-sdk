from agents import Agent , Runner , OpenAIChatCompletionsModel , Runner,set_tracing_disabled
from agents.mcp import  MCPServerStdio
from openai import AsyncOpenAI
import asyncio
from agents.run import RunConfig
import os 
from dotenv import load_dotenv


load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")

set_tracing_disabled(True)

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
)

async def run (time_mcp_server):
    agent = Agent(
        name = "Assistant",
        instructions="Use the tools to help users finding the answers.",
        mcp_servers= [time_mcp_server],
        model= model,
    )

    # # Ask a question that reads then reasons.
    # message = "Look at my files and tell me which games are my favourite."
    # print(f"\n\nRunning: {message}")
    # result = await Runner.run(starting_agent=agent, input=message)
    # print(result.final_output)

      # Ask a question that reads then reasons.
    message = "When time is it in karachi right now?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)


async def main():

    async with MCPServerStdio(
        name = "Time server", 
        params = {
            "command": "python",
            "args": ["-m", "mcp_server_time", "--local-timezone=America/New_York"]
        },
        cache_tools_list=True,
    ) as time_mcp_server:
        
        print("Starting MCP server...")
        await run(time_mcp_server)

if __name__ == "__main__":
    print("Started Running..")
    asyncio.run(main())