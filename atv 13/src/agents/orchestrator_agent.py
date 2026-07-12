import warnings

from google.adk.agents import SequentialAgent

from src.agents.subagents import recuperador, auditor_risco, sumarizador

# SequentialAgent está marcado como deprecated no ADK 2.4.0, mas continua
# 100% funcional. É apenas um aviso — silenciei para não poluir o console.
warnings.filterwarnings("ignore", category=DeprecationWarning)


root_agent = SequentialAgent(
    name="orchestrator_agent",
    sub_agents=[recuperador, auditor_risco, sumarizador],
)
