import os 
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import chainlit as cl


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@cl.on_chat_start
async def start():

    await cl.Message(content="Welcome to the Shiraz Ali AI Assistant! How can I help you today?").send()


@cl.on_message
async def main(message:cl.Message):

    external_client = AsyncOpenAI(
        api_key= gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model= "gemini-2.0-flash",
        openai_client= external_client,
    )


    config = RunConfig(
        model= model,
        model_provider=external_client,
        tracing_disabled=True,
    )

    agent:Agent = Agent(
        name="Assistant", 
        instructions="You are a helpful assistant",
        model=model
    )
    
    msg = cl.Message(content="Thinking...")
    await msg.send()

    try:
        result = Runner.run_sync(
            agent,
            input = message.content,
            run_config=config
        )
        
        response_content = result.final_output

        msg.content = response_content
        await msg.update()

        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")