import datetime

from google.adk.agents import Agent
from google.adk.tools import google_search

#Obtive alguns erros em que na página do localhost não retornou a resposta
#apesar de o modelo conseguir gerar normalmente de acordo com as instruções
def get_current_time() -> dict:
     """
     Get the current time in the format YYYY-MM-DD HH:MM:SS
     """
     return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # type: ignore
     }

root_agent = Agent(
    name="tool_agent",
    model="gemini-2.5-flash",
    description="Tool agent",
    instruction="""
        You are a helpful assistant.

        If the user asks for the current time:
        1. Call the tool get_current_time.
        2. Use the returned value to answer the user.

        Always respond with a natural language sentence.
    """,
    tools=[get_current_time],
)
# O parâmetro *tools* corresponde as ferramentas que aquele agente pode acessar para gerar a resposta
