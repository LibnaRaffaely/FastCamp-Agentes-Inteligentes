import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
from app.prompts.prompt_faq import description, build_instruction
from app.prompts.faq_content import render_faq_catalog

LiteLLM = LiteLlm


load_dotenv()

model = LiteLLM(
    model="openrouter/openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


faq_agent = Agent(
    name = "faq_agent",
    model = model,
    description = description,
    instruction = build_instruction(render_faq_catalog()),
    tools = []
)