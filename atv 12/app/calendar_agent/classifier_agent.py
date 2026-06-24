import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
from app.tools.faq_tools import save_classification
from app.prompts.prompt_classifier import description, CLASSIFIER_INSTRUCTION

load_dotenv()

model = LiteLlm(
    model="openrouter/openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


classifier_agent = Agent(
    name="classifier_agent",
    model = model,
    description =description,
    instruction =CLASSIFIER_INSTRUCTION,
    tools =[save_classification],
)