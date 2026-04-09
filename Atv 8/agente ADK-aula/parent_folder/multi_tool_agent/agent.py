
import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm 
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.tools.tool_context import ToolContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.agents.callback_context import CallbackContext


# Para iniciar rode:
#1) .\.venv\Scripts\activate      
#2) adk run multi_tool_agent    

MODEL_GEMINI_2_5_FLASH = "gemini-2.5-flash"

# Todo e qualquer texto escrito dentro de comentários nesse formato: """ **** ""
# Serão interpretados pelo modelo de linguagem como uma DOCSTRING
# Que  é a definição de como deve ser o uso dessa ferramenta
# Em sitexe, a DocString define sobre a ferramenta: O que faz; quando usar;  argumentos necessários; infos retornadas
#
#OBS: as DocString devem ser claras, descritivas e precisas em cada ferramenta

def get_weather_stateful(city: str, tool_context: ToolContext) -> dict:
    """Retrieves weather, converts temp unit based on session state."""
    print(f"--- Tool: get_weather_stateful called for {city} ---")

    # --- Read preference from state ---
    preferred_unit = tool_context.state.get("user_preference_temperature_unit", "Celsius") # Default to Celsius
    print(f"--- Tool: Reading state 'user_preference_temperature_unit': {preferred_unit} ---")

    
    city_normalized = city.lower().replace(" ", "")
    
    # Dados base que nossa ferramenta tem acesso
    # Caso o prompt do User venha com um local fora desse escopo do DB
    # Haverá o erro apresentado no else da line[72]
    mock_weather_db = {
        "newyork": {"temp_c": 25, "condition": "sunny"},
        "london": {"temp_c": 15, "condition": "cloudy"},
        "tokyo": {"temp_c": 18, "condition": "light rain"},
    }
    
    # É realizado a coleta dos dados conforme estão no DB,convertendo de dict (dicionário) para variáveis únicas
    # São organizadas a resposta  dentro de *report*, com as variáveis coletadas 
    # e são sistematizadas dentro do *result* com status e mensagem
    if city_normalized in mock_weather_db:
        data = mock_weather_db[city_normalized]
        temp_c = data["temp_c"]
        condition = data["condition"]

        # Definição da unidade de Temperatura desejada e conversão (se necessário)
        if preferred_unit == "Fahrenheit":
            temp_value = (temp_c * 9/5) + 32
            temp_unit = "°F"
        else: 
            temp_value = temp_c
            temp_unit = "°C"

        report = f"The weather in {city.capitalize()} is {condition} with a temperature of {temp_value:.0f}{temp_unit}."
        result = {"status": "success", "report": report}
        print(f"--- Tool: Generated report in {preferred_unit}. Result: {result} ---")

        tool_context.state["last_city_checked_stateful"] = city
        print(f"--- Tool: Updated state 'last_city_checked_stateful': {city} ---")

        return result
    else:
        error_msg = f"Sorry, I don't have weather information for '{city}'."
        print(f"--- Tool: City '{city}' not found. ---")
        return {"status": "error", "error_message": error_msg}


# Essa ferramenta, apesar de não ser chamada, ela serve para retornar o tempo(horas)
#  específico da cidade enviada no prompt. 
def get_current_time(city: str) -> dict:
    
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

 
#Ferramenta que irá ser utilizada pelo agente greeting_agent
# Onde inicialmente há a DocString de definição de ferramenta
# E é estabelecido como ocorrerá a saudação com o sem o nome do user
#
def say_hello(name: Optional[str] = None) -> str: 
    """Provides a simple greeting. If a name is provided, it will be used.

    Args:
        name (str, optional): The name of the person to greet. Defaults to a generic greeting if not provided.

    Returns:
        str: A friendly greeting message.
    """
    if name:
        greeting = f"Hello, {name}!"
        print(f"--- Tool: say_hello called with name: {name} ---")
    else:
        greeting = "Hello there!" 
        print(f"--- Tool: say_hello called without a specific name (name_arg_value: {name}) ---")
    return greeting

#Ferramenta que irá ser utilizada pelo agente farewell_agent
# Onde inicialmente há a DocString de definição de ferramenta
# E é estabelecido como ocorrerá a despedida simples
# eficiente para dividir funções e padronizar respostas do agente
def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    print(f"--- Tool: say_goodbye called ---")
    return "Goodbye! Have a great day."

#Ferramenta que irá ser chamada sempre antes de acionar um agente
#útil para limitar que tipo de mensagem não irá passar pela LLM
# Evitando gastos de crédito em requisições
def block_keyword_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    Inspects the latest user message for 'BLOCK'. If found, blocks the LLM call
    and returns a predefined LlmResponse. Otherwise, returns None to proceed.
    """
    agent_name = callback_context.agent_name # Get the name of the agent whose model call is being intercepted
    print(f"--- Callback: block_keyword_guardrail running for agent: {agent_name} ---")

    # Extract the text from the latest user message in the request history
    last_user_message_text = ""
    if llm_request.contents:
        # Find the most recent message with role 'user'
        for content in reversed(llm_request.contents):
            if content.role == 'user' and content.parts:
                # Assuming text is in the first part for simplicity
                if content.parts[0].text:
                    last_user_message_text = content.parts[0].text
                    break # Found the last user message text

    print(f"--- Callback: Inspecting last user message: '{last_user_message_text[:100]}...' ---") # Log first 100 chars

    # --- Guardrail Logic ---
    keyword_to_block = "BLOCK"
    if keyword_to_block in last_user_message_text.upper(): # Case-insensitive check
        print(f"--- Callback: Found '{keyword_to_block}'. Blocking LLM call! ---")
        # Optionally, set a flag in state to record the block event
        callback_context.state["guardrail_block_keyword_triggered"] = True
        print(f"--- Callback: Set state 'guardrail_block_keyword_triggered': True ---")

        # Construct and return an LlmResponse to stop the flow and send this back instead
        return LlmResponse(
            content=types.Content(
                role="model", # Mimic a response from the agent's perspective
                parts=[types.Part(text=f"I cannot process this request because it contains the blocked keyword '{keyword_to_block}'.")],
            )
            # Note: You could also set an error_message field here if needed
        )
    else:
        # Keyword not found, allow the request to proceed to the LLM
        print(f"--- Callback: Keyword not found. Allowing LLM call for {agent_name}. ---")
        return None # Returning None signals ADK to continue normally



greeting_agent = None
try:
    greeting_agent = Agent(
        model = MODEL_GEMINI_2_5_FLASH,
        name="greeting_agent",
        instruction="You are the Greeting Agent. Your task is to welcome the user warmly using the 'say_hello' tool.",
        description="Handles simple greetings and hellos using the 'say_hello' tool.", # Crucial for delegation
        tools=[say_hello],
    )
    print(f"✅  Sub-Agent '{greeting_agent.name}' redefined.")
except Exception as e:
    print(f"❌ Could not create Greeting agent. Check API Key ({greeting_agent.model}). Error: {e}") # type: ignore


farewell_agent = None
try:
    farewell_agent = Agent(
        model = MODEL_GEMINI_2_5_FLASH,
        name="farewell_agent",
        instruction="You are the Farewell Agent. Your task is to say goodbye politely using the 'say_goodbye' tool.",
        description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.", # Crucial for delegation
        tools=[say_goodbye],
    )
    print(f"✅ SubAgent '{farewell_agent.name}' redefined.")
except Exception as e:
    print(f"❌ Could not create Farewell agent. Check API Key ({farewell_agent.model}). Error: {e}") # type: ignore
    
# Esse é o agente principal da nossa aplicação
# onde definimos na description e instruction que ele será o gerenciador 
# além de delegar quais tools serão solicitadas
root_agent = Agent(
    name="weather_time_agent_v3_model_guardrail",
    model=MODEL_GEMINI_2_5_FLASH,
    description="Main agent: Handles weather, delegates greetings/farewells, includes input keyword guardrail.",
    instruction=("You are the main Weather Agent. "
        "IMPORTANT: Always start by greeting the user using 'greeting_agent' if they said hello. " # Força o cumprimento
        "Then, provide weather using 'get_weather_stateful'. "
        "Delegate farewells to 'farewell_agent'. "
        "Maintain a polite and helpful tone."),
    tools=[get_weather_stateful, get_current_time],
    sub_agents=[greeting_agent, farewell_agent], # type: ignore
    output_key="last_weather_report",
    before_model_callback=block_keyword_guardrail
)