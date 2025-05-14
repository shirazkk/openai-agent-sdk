
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
# from agents import enable_verbose_stdout_logging
from agents.extensions.visualization import draw_graph



API_KEY = "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"

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-001"

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

set_tracing_disabled(disabled=True)

# Updated Instructions for web_dev
web_dev: Agent=Agent(
    name="web_dev",
    instructions="You are a specialized web developer. Your task is to address queries and perform tasks specifically related to front-end web development, including HTML, CSS, JavaScript, and related frameworks. If a task is related to mobile app development, backend systems, or operations, do not attempt to handle it yourself; instead, understand what is needed for a handoff.",
    handoff_description="web development expert for front-end tasks.",
    model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
)

# Updated Instructions for app_dev
app_dev: Agent=Agent(
    name="app_dev",
    instructions="You are a specialized mobile application developer. Your role is to provide assistance and perform tasks related to building and managing mobile applications (iOS, Android, cross-platform frameworks). Do not handle tasks related to web development, backend systems, or operations; understand what is needed for a handoff to the appropriate agent.",
    handoff_description="mobile application development expert.",
    model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client),

)

# Updated Instructions for backend_dev
backend_dev: Agent=Agent(
    name="backend_dev",
    instructions="You are a specialized backend developer. Your expertise lies in server-side logic, databases, APIs, and backend frameworks. When presented with a task, determine if it falls within backend development. If it is related to front-end web, mobile apps, or operations, identify the required information for a handoff instead of handling it.",
    handoff_description="backend development expert for server-side tasks.",
    model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
)

# Updated Instructions for dev_ops
dev_ops:Agent=Agent(
    name="dev_ops",
    instructions="You are a specialized DevOps agent. Your responsibility is to handle tasks related to infrastructure, deployment, monitoring, and automation. Evaluate incoming tasks to see if they require DevOps expertise. If the task is related to web development, app development, or backend development, prepare for a handoff with the necessary details.",
    handoff_description="DevOps expert for infrastructure and operations.",
    model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
)

# Updated Instructions for agentic_ai
agentic_ai: Agent=Agent(
    name="agentic_ai",
    instructions="You are an intelligent agent capable of understanding diverse tasks and utilizing specialized tools to accomplish them. Your primary function is to route tasks to the 'backend_dev_tool' for backend-related work or the 'dev_ops_tool' for operations-related work. Analyze the user's request and determine which tool is most appropriate. If the task does not clearly fit backend development or dev ops, or if you need more information to route it, ask clarifying questions. Do not attempt to perform tasks yourself if they are within the scope of your available tools.",
    model = OpenAIChatCompletionsModel(model=MODEL,openai_client=client),
     
    tools=[
      backend_dev.as_tool(
        tool_name="backend_dev_tool",
        tool_description="Use this tool to handle tasks that require backend development expertise, such as database queries, API logic, or server-side scripting."
        ),
     dev_ops.as_tool(
        tool_name="dev_ops_tool",
        tool_description="Use this tool for tasks related to infrastructure management, deployment pipelines, system monitoring, and automation scripts."
        )
    ],
    
)

# Updated Instructions for panacloud_agent
panacloud_agent:Agent = Agent(
    name="panacloud_agent",
    instructions="You are the main coordinator agent, responsible for receiving initial requests and determining which specialized agent is best suited to handle the task. Evaluate the user's request to see if it requires expertise in web development (handoff to 'web_dev'), mobile app development (handoff to 'app_dev'), or if it requires the capabilities of the 'agentic_ai' which can use backend and dev ops tools. If the request clearly aligns with one of these areas, handoff the task. If the request is ambiguous or requires a general AI response, handle it yourself. Prioritize handing off to the most appropriate specialist agent.",
    handoffs=[web_dev, app_dev, agentic_ai],
    model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
  
)


draw_graph(panacloud_agent, filename="agent_graph")


# enable_verbose_stdout_logging()

result =  Runner.run_sync(panacloud_agent,"I need to create a new web page for my portfolio. Can you help me with that?")
print(result.final_output)




