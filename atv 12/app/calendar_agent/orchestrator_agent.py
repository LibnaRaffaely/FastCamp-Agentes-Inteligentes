import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents.callback_context import CallbackContext
from app.calendar_agent.faq_agent import faq_agent
from app.calendar_agent.classifier_agent import classifier_agent
from app.prompts.prompt_orchestrator import description, ORCHESTRATOR_INSTRUCTION

load_dotenv()

model = LiteLlm(
    model="openrouter/openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# classifier é chamado como ferramenta: orquestrador chama, recebe resultado e mantém controle
classifier_tool = AgentTool(agent=classifier_agent)


def initialize_session_state(callback_context: CallbackContext) -> None:
    """Reseta intent no início de cada turno para garantir nova classificação."""
    callback_context.state["intent"] = "não classificado"


root_agent = Agent(
    name="orchestrator_agent",
    model=model,
    description=description,
    instruction=ORCHESTRATOR_INSTRUCTION,
    sub_agents=[faq_agent],
    tools=[classifier_tool],
    before_agent_callback=initialize_session_state,
)
