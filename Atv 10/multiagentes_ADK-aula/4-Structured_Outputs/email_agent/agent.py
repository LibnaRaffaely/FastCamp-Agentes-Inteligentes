import os
import random

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from pydantic import BaseModel, Field

#Especificação do modelo desejado e o token do openrouter criado
model = LiteLlm(
    model="openrouter/openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

#Instanciação de como deve ser  a estrutura enviada no output
#é anotado em cada elemento desse modelo uma description para orientar o modelo como interagir e preencher os dados|
class EmailContent(BaseModel):
    subject: str = Field(
        description="The subject line of the email. Should be concise and descriptive."
    )
    body: str = Field(
        description="The main content of the email. Should be well-formatted with proper greeting, paragraphs, and signature."
    )


root_agent = Agent(
    name="email_agent",
    model=model,
    description="Generates professional emails with structured subject and body",
    instruction="""
        You are an Email Generation Assistant.
        Your task is to generate a professional email based on the user's request.

        GUIDELINES:
        - Create an appropriate subject line (concise and relevant)
        - Write a well-structured email body with:
            * Professional greeting
            * Clear and concise main content
            * Appropriate closing
            * Your name as signature
        - Suggest relevant attachments if applicable (empty list if none needed)
        - Email tone should match the purpose (formal for business, friendly for colleagues)
        - Keep emails concise but complete

        IMPORTANT: Your response MUST be valid JSON matching this structure:
        {
            "subject": "Subject line here",
            "body": "Email body here with proper paragraphs and formatting",
        }

        DO NOT include any explanations or additional text outside the JSON response.
    """,
    output_schema= EmailContent,
    output_key="email",
)

# Guidelines ->  estabelece um padrão mais assertivo de comportamento, 
# mantendo tom, contexto e formato do corpo de resposta sem adicionar dados/textos extras
# O uso de diretrizes "concise and relevant" e "Appropriate closing" estabelecem um padrão de qualidade do output

#output_key -> se trata de como esse dado ficará nomeado na estrutura do agente, ex:
#  email:
#   subject: "Project Deadline Extension Announcement"
#   body: "Dear Team, I hope this message finds you well. I am writing to inform you that the deadline for our current project has been extended by two weeks. This adjustment is due to recent circumstances that have affected our project timeline. The new deadline is now set for [insert new deadline date]. 
#          I encourage everyone to take advantage of this additional time to enhance your contributions and ensure that we meet our project goals with the highest quality. Please feel free to reach out if you have any questions or require further clarification regarding this extension. Thank you for your continued hard work and dedication. Best regards, [Your Name]"