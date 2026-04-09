from google.adk.agents import Agent

def get_contact(person:str) -> dict:

    # Docstring - Determina para o agente que irá acessá-la como será o funcionamento dessa tool
    """ 
    Gets the contact details of the chosen person

    Args:
        person (str): The name of the person whose contact you want

    Returns:
        dict: The contact details

    """

    # Good practice to output as dictionary rather than just result - also gives more context
    return {
        "contact": f"{person}'s number is 12345"
    }

    # Google ADK converts the output as a dictionary automatically: {result: ---}

root_agent = Agent(
    name = "tool_custom_agent",
    model = "gemini-2.0-flash",
    description = "Tool Agent",
    instruction = "You are a helpful assistant that can use the following tools: "
    "- get_contact. Always use this tool to get people's contacts.",
    tools = [get_contact] 
    
)


#------------------------------------------------------------------------------------------#
from google.adk.tools import google_search # New import for Google Search

# A bit buggy - be warned!

# root_agent = Agent(
#     name="basic_search_agent",
#     model="gemini-2.0-flash",
#     description="Agent to answer questions using Google Search.",
#     instruction="I can answer your questions by searching the internet. Just ask me anything!",
#     # google_search is a pre-built tool which allows the agent to perform Google searches.
#     tools=[google_search]
# )





