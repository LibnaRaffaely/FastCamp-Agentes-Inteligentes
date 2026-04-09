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

MODEL_GEMINI_2_5_FLASH = "gemini-2.5-flash"

MOCK_PLANT_DB = {
      "rose" : {
          "type_sun": "very sunny", 
          "irrigation":"balanced", 
          "informations":"It has flowers of various colors and thorns."},
        "fern": {
            "type_sun": "shade",
            "irrigation": "high",
            "informations": "A leafy plant that grows well in humid and shaded environments."
        },
        "orchid": {
            "type_sun": "indirect sunlight",
            "irrigation": "moderate",
            "informations": "An ornamental plant known for its delicate and exotic flowers."
        },
        "lavender": {
            "type_sun": "very sunny",
            "irrigation": "low",
            "informations": "A fragrant plant with purple flowers often used for essential oils."
        },
        "bamboo": {
            "type_sun": "partial sun",
            "irrigation": "moderate",
            "informations": "A fast-growing plant with hollow stems commonly used in decoration and construction."
        },
        "aloe_vera": {
            "type_sun": "very sunny",
            "irrigation": "low",
            "informations": "A succulent plant known for the medicinal gel inside its leaves."
        },
        "sunflower": {
            "type_sun": "very sunny",
            "irrigation": "moderate",
            "informations": "A tall plant with large yellow flowers that follow the sun."
        },
        "mint": {
            "type_sun": "partial sun",
            "irrigation": "high",
            "informations": "An aromatic herb widely used in teas, foods, and medicine."
        },
        "tulip": {
            "type_sun": "very sun",
            "irrigation": "moderate",
            "informations": "A spring flower known for its cup-shaped colorful blooms."
        },
        "snake_plant": {
            "type_sun": "low light",
            "irrigation": "low",
            "informations": "A very resistant indoor plant that tolerates low light and requires little water."
        },

        "peace_lily": {
            "type_sun": "indirect sunlight",
            "irrigation": "moderate",
            "informations": "A popular indoor plant with white flowers that grows well with indirect light."
        }
    }

def get_plants(plant: str, tool_context: ToolContext) -> dict:
    """Returns information about the desired plant."""
    
    plant_normalize = plant.lower().replace(" ", "")
    
    
    if plant_normalize in MOCK_PLANT_DB:
        data = MOCK_PLANT_DB[plant_normalize]
        sun = data["type_sun"]
        irrigation = data["irrigation"]
        details = data["informations"]
        
        report = f"The {plant} like {sun} e {irrigation} irrigation, and have  this caracteristics: {details} "
        result  = {"status": "sucess", "report": report}
        print(f"--- Tool: Generated report about {plant}. Result: {result} ---")

        tool_context.state["last_plant_required"] = plant
        print(f"--- Tool: Updated state 'last_plant_required': {plant} ---")

        return result     
    else:
        error_msg = f"Sorry, I don't have informations about this plant, '{plant}'."
        print(f"--- Tool: plant '{plant}' not found. ---")
        return {"status": "error", "error_message": error_msg}

def get_specific_sun_plants(sun_type: str)-> dict:
    """Retrieve two plants that match a specific sunlight requirement.

        This function searches the plant database and returns up to two
        plants whose `type_sun` field matches the sunlight condition
        provided by the user.

        Args:
            sun_type (str): The sunlight condition to filter plants by.
                Examples: "low light", "indirect sunlight", "very sunny".

        Returns:
            dict: A dictionary containing up to two plants that match the
            requested sunlight requirement. The keys are the plant names
            and the values are their corresponding information dictionaries.

        Example:
            >>> get_specific_sun_plants("low light")
            {
                "snake_plant": {...},
                "fern": {...}
            }
    """
    sun_type_normalized = sun_type.lower().strip()

    matches = {}

    for plant_name, data in MOCK_PLANT_DB.items():
        if data["type_sun"].lower() == sun_type_normalized:
            matches[plant_name] = data

        if len(matches) == 2:
            break

    if matches:
        result = {"status": "success", "plants": matches}
        print(f"--- Tool: Found plants for sunlight '{sun_type}'. Result: {result} ---")
        return result
    else:
        error_msg = f"No plants found with sunlight requirement '{sun_type}'."
        print(f"--- Tool: No plants found for sunlight '{sun_type}'. ---")
        return {"status": "error", "error_message": error_msg}

def block_keyword_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    Inspects the latest user message for the word 'cacto'. If found, blocks the
    LLM call and returns a predefined response. Otherwise, returns None to allow
    the request to proceed normally.
    """

    agent_name = callback_context.agent_name
    print(f"--- Callback: cactus guardrail running for agent: {agent_name} ---")

    
    last_user_message_text = ""
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.role == "user" and content.parts:
                if content.parts[0].text:
                    last_user_message_text = content.parts[0].text
                    break

    print(f"--- Callback: Inspecting last user message: '{last_user_message_text[:100]}...' ---")

    
    keyword_to_block = "cactus"

    if keyword_to_block in last_user_message_text.lower():
        print(f"--- Callback: Found '{keyword_to_block}'. Blocking LLM call! ---")

        
        callback_context.state["guardrail_cactus_triggered"] = True
        print("--- Callback: Updated state 'guardrail_cactus_triggered': True ---")


        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        text="I cannot process this request because it contains the blocked plant 'cacto'."
                    )
                ],
            )
        )

    else:
        print(f"--- Callback: Keyword not found. Allowing LLM call for {agent_name}. ---")
        return None    
    
def say_welcome(name:Optional[str] = None)-> str:
    """Provides a simple welcome message. If a name is provided, it will be used.

    Arguments:
        name(str, optional): The name of the person to use. The default is a generic greeting if not provided.

    Returns:
        str: A friendly welcome message.
    """
    if name:
        message = f"Hello {name}! Welcome to the flower shop."
        print(f"-----Tool: say_welcome called with name: {name}---")
    else:
        message = f"Hello! Welcome to the flower shop."
        print(f"--- Tool: say_hello called without a specific name ---")
        
    return message

def say_goodbye() -> str:
    """Provides a simple goodbye message to end the conversation."""
    print(f"--- Tool: say_goodbye called ---")
    return "Goodbye! Come back anytime!"

wellcome_agent = None
try:
    wellcome_agent = Agent(
        model = MODEL_GEMINI_2_5_FLASH,
        name="wellcome_agent",
        instruction="You are the Greeting Agent. Your task is to welcome the user warmly using the 'say_hello' tool.",
        description="Handles simple greetings and hellos using the 'say_hello' tool.", # Crucial for delegation
        tools=[say_welcome],
    )
    print(f"✅  Sub-Agent '{wellcome_agent.name}' redefined.")
except Exception as e:
    print(f"❌ Could not create Greeting agent. Check API Key ({wellcome_agent.model}). Error: {e}") # type: ignore


goodbye_agent = None
try:
    goodbye_agent = Agent(
        model = MODEL_GEMINI_2_5_FLASH,
        name="goodbye_agent",
        instruction="You are the Goodbye Agent. Your task is to say goodbye politely using the 'say_goodbye' tool.",
        description="Handles simple goodbyes using the 'say_goodbye' tool.",
        tools=[say_goodbye],
    )
    print(f"✅ SubAgent '{goodbye_agent.name}' redefined.")
except Exception as e:
    print(f"❌ Could not create Farewell agent. Check API Key ({goodbye_agent.model}). Error: {e}") # type: ignore

  
    
root_agent = Agent(
    name="plant_manager_agent",
    model=MODEL_GEMINI_2_5_FLASH,
    description="Main manager agent that coordinates plant information tools and sub-agents, with input guardrails.",
    instruction=("You are the main Plant Manager Agent. "
        "Your job is to coordinate other agents and tools to answer user questions about plants. "
        "Use the appropriate tool to retrieve plant information when needed. "
        "If the user greets, delegate to 'greeting_agent'. "
        "If the user says goodbye, delegate to 'farewell_agent'. "
        "Maintain a polite and helpful tone."),
    tools=[get_plants, get_specific_sun_plants],
    sub_agents=[wellcome_agent, goodbye_agent], # type: ignore
    output_key="last_plant_report",
    before_model_callback=block_keyword_guardrail
)
