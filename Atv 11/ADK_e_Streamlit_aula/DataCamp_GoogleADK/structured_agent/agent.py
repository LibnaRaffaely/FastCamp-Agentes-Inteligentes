# Example for Output Schema

from pydantic import BaseModel, Field # Library to define these schematics
from google.adk.agents import Agent

#definição da estrutura da resposta e segue a oristação da description
class GreetingOutput(BaseModel):
    greeting: str = Field(description="A greeting message to the person.")

# Agent that must return structured output
root_agent = Agent(
    name="output_schema_agent", 
    model="gemini-2.0-flash",
    instruction="Given a person's name, respond with a JSON object like {\"greeting\": \"Hello, name!\"}",
    output_schema=GreetingOutput,  # É estabelecido como será o retorno/output com base na classe definida
    output_key="final_greeting" # O retorno será guardado aqui dentro dentro do context["final_greeting"], salvando no estado do agente
)
