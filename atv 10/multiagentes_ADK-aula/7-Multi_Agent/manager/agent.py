
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext

from .sub_agents.funny_nerd.agent import funny_nerd
from .sub_agents.news_analyst.agent import news_analyst
from .sub_agents.stock_analyst.agent import stock_analyst
from .tools.tools import get_current_time

load_dotenv()

#Especificação do modelo desejado e o token do openrouter criado
model = LiteLlm(
    model="openrouter/openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

#Criação do agente raiz que irá gerenciar os demais agentes 
root_agent = Agent(
    name="manager",
    model=model,
    description="Manager agent",
    instruction="""
    You are a manager agent that is responsible for overseeing the work of the other agents.

    Always delegate the task to the appropriate agent. Use your best judgement 
    to determine which agent to delegate to.

    You are responsible for delegating tasks to the following agent:
    - stock_analyst
    - funny_nerd

    You also have access to the following tools:
    - news_analyst
    - get_current_time
    """,
    sub_agents=[stock_analyst, funny_nerd],
    tools=[
        AgentTool(news_analyst),
        get_current_time,
    ],
)
#Ao enviar um prompt o manager irá analisar a descrição de casa subAgente para ver qual é o mais apropriado
# AgentTool(news_analyst) -> Este não é um agente simples, ele é um agente ferramenta
# pois ele é não possui ferramentas instanciadas, apenas a pesquisa via google declarada na sua ação 