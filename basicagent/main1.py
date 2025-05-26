import agentops
from agents import Agent , AsyncOpenAI , OpenAIChatCompletionsModel , Runner,trace
from agents.run import RunConfig
import os 
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")


agentops.init("3d684e2b-ffba-42f7-8261-ddbae819076a")

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


async def main():

    
    # Create an agent
    agent = Agent(
        name="Code Reviewer",
        instructions="Review code and suggest improvements."
    )


    result = await Runner.run(
                agent,
                "Review this code: def process_data(data): return data.strip()",
                run_config= config
            )
            
    print(result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())