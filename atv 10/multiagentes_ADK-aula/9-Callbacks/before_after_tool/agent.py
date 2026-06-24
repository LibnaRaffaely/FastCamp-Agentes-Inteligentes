from datetime import datetime
from typing import Optional
import os

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from google.adk.models.lite_llm import LiteLlm

"""
Before and After Agent Callbacks Example

This example demonstrates how to use both before_agent_callback and after_agent_callback 
for logging purposes.
"""

model = LiteLlm(
    model="openrouter/openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

#------------ EXPLICAÇÃO FUNCIONAMENTO ------------
#Essa implementação serve para vermos a latência do modelo
# e entender como funciona o before before_agent_callback e after_agent_callback 
# que entram como parâmetros na criação do modelo nas linhas finais

    


#Função executada antes da LLM receber o prompt do usuário
def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Simple callback that logs when the agent starts processing a request.

    Args:
        callback_context: Contains state and context information

    Returns:
        None to continue with normal agent processing
    """
    # Get the session state
    state = callback_context.state

    # Record timestamp
    timestamp = datetime.now()

    # Instancia o nome do agente caso esteja vazio pelo estado do callback_context
    if "agent_name" not in state:
        state["agent_name"] = "SimpleChatBot"

    # Inicia a contagem de requisições feitas
    if "request_counter" not in state:
        state["request_counter"] = 1
    else:
        state["request_counter"] += 1

    # salva o tempo de inicio
    state["request_start_time"] = timestamp.isoformat()

    # Log the request
    print("=== AGENT EXECUTION STARTED ===")
    print(f"Request #: {state['request_counter']}")
    print(f"Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    # Print to console
    print(f"\n[BEFORE CALLBACK] Agent processing request #{state['request_counter']}")

    return None

# Esta função roda após o agente gerar a resposta, porém antes de ser efetivamente enviada ao usuário
def after_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Simple callback that logs when the agent finishes processing a request.

    Args:
        callback_context: Contains state and context information

    Returns:
        None to continue with normal agent processing
    """
    # Get the session state
    state = callback_context.state

    # Calculo do tempo de duração da interação
    timestamp = datetime.now()
    duration = None
    if "request_start_time" in state:
        start_time = datetime.fromisoformat(state["request_start_time"])
        duration = (datetime.now() - start_time).total_seconds()

    # Log the completion
    print("=== AGENT EXECUTION COMPLETED ===")
    print(f"Request #: {state.get('request_counter', 'Unknown')}")
    if duration is not None:
        print(f"Duration: {duration:.2f} seconds")

    # Print to console
    print(
        f"[AFTER CALLBACK] Agent completed request #{state.get('request_counter', 'Unknown')}"
    )
    if duration is not None:
        print(f"[AFTER CALLBACK] Processing took {duration:.2f} seconds")

    return None


# Create the Agent
root_agent = LlmAgent(
    name="before_after_agent",
    model=model,
    description="A basic agent that demonstrates before and after agent callbacks",
    instruction="""
    You are a friendly greeting agent. Your name is {agent_name}.
    
    Your job is to:
    - Greet users politely
    - Respond to basic questions
    - Keep your responses friendly and concise
    """,
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
)
