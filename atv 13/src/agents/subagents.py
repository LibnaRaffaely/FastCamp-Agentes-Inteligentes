import os
from google.adk.agents import Agent

from google.adk.models.lite_llm import LiteLlm
from src.agents.tool.search import search_cases
from src.agents.prompt.prompt_recuperator import INSTRUCTION_RECUPERADOR
from src.agents.prompt.prompt_auditor import INSTRUCTION_AUDITOR
from src.agents.prompt.prompt_sumarizador import INSTRUCTION_SUMARIZADOR


model = LiteLlm(
    model="openrouter/google/gemini-2.5-flash-lite",
    api_key=os.getenv("OPENROUTER_API_KEY")
)



recuperador = Agent(name="recuperador", model=model,
                    instruction=INSTRUCTION_RECUPERADOR,
                    tools=[search_cases], output_key="recuperacao")

auditor_risco = Agent(name="auditor_risco", model=model,
                      instruction=INSTRUCTION_AUDITOR, output_key="auditoria")

sumarizador = Agent(name="sumarizador", model=model,
                    instruction=INSTRUCTION_SUMARIZADOR)


