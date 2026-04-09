# parallel agent
from dotenv import load_dotenv
load_dotenv()
from google.adk.agents import Agent, ParallelAgent
from google.adk.tools import google_search

import os
#os.environ["OTEL_PYTHON_DISABLED"] = "true" # OpenTelemetry issues -> regarding internal asyncio package


# Hotel Search Agent - Seleciona as acomodações 
hotel_search_agent = Agent(
    name="HotelSearchAgent",
    model="gemini-2.0-flash",
    tools=[google_search],
    description="An agent that searches for hotels and accommodation options in a given destination",
    instruction="""
    You are a hotel booking specialist. You will be given a destination and travel dates, and you will search for:
    - Popular hotels in the area
    - Different price ranges (budget, mid-range, luxury)
    - Hotel amenities and ratings
    - Location advantages
    Provide a summary of the best accommodation options with brief descriptions.
    ONLY research for hotels and nothing else.
    """,
    output_key="hotel_options",
)

# Restaurant Search Agent - Encontra recomendações de restaurantes
restaurant_search_agent = Agent(
    name="RestaurantSearchAgent",
    model="gemini-2.0-flash",
    tools=[google_search],
    description="An agent that searches for restaurants and dining experiences in a given destination",
    instruction="""
    You are a food and dining expert. You will be given a destination and you will search for:
    - Top-rated restaurants and cafes
    - Local cuisine specialties
    - Different dining price ranges
    - Unique dining experiences
    Provide a summary of the best dining options with cuisine types and highlights.
    Only research for restaurants and nothing else.
    """,
    output_key="restaurant_options",
)

# Activities Search Agent - Encontra coisas a se fazer
activities_search_agent = Agent(
    name="ActivitiesSearchAgent",
    model="gemini-2.0-flash",
    tools=[google_search],
    description="An agent that searches for activities and attractions in a given destination",
    instruction="""
    You are a local activities expert. You will be given a destination and you will search for:
    - Popular tourist attractions
    - Outdoor activities and adventures
    - Cultural experiences and museums
    - Entertainment and nightlife options
    Provide a summary of the best activities with brief descriptions and recommendations.
    Only research for activities and nothing else.
    """,
    output_key="activity_options",
)

# O root é instanciado como ParallelAgent para que os subagentes sejam  geridos de forma paralela
root_agent = ParallelAgent(
    name="TravelPlanningSystem",
    description="A comprehensive system that simultaneously searches for hotels, restaurants, and activities for trip planning",
    sub_agents=[hotel_search_agent, restaurant_search_agent, activities_search_agent],
)
