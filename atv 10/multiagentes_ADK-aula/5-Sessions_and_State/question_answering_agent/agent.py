
import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


model = LiteLlm(
    model="openrouter/openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

question_answering_agent = Agent(
    name="question_answering_agent",
    model=model,
    description="Question answering agent",
    instruction="""
        You are a helpful assistant that answers questions about the user's preferences.

        Here is some information about the user:
        Name: 
        {user_name}
        Preferences: 
        {user_preferences}
    """,
)
