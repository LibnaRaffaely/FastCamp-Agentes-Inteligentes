
import os

from datetime import datetime
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext


load_dotenv()

#Especificação do modelo desejado e o token do openrouter criado
model = LiteLlm(
    model="openrouter/openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def purchase_course(tool_context: ToolContext) -> dict:
    """
    Simulates purchasing the AI Marketing Platform course.
    Updates state with purchase information.
    """
    
    #Estabelece o nome do curso e horário da compra
    course_id = "ai_marketing_platform"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # pega a lista de cursos comprados
    current_purchased_courses = tool_context.state.get("purchased_courses", [])

    # Verificação se o User possui o curso a ser comprado
    course_ids = [
        course["id"] for course in current_purchased_courses if isinstance(course, dict)
    ]
    if course_id in course_ids:
        return {"status": "error", "message": "You already own this course!"}

    # Create new list with the course added
    new_purchased_courses = []
    # Only include valid dictionary courses
    for course in current_purchased_courses:
        if isinstance(course, dict) and "id" in course:
            new_purchased_courses.append(course)

    # adiciona o curso a ser comprado na lista de compras
    new_purchased_courses.append({"id": course_id, "purchase_date": current_time})

    # Salva a lista de compras no contexto
    tool_context.state["purchased_courses"] = new_purchased_courses

    # Recebe dentro do contexto o elemento que possui esse titulo que está armazenando o histórico de interação
    current_interaction_history = tool_context.state.get("interaction_history", [])

    # Adiciona um novo elemento de dicionário para o histórico de interação com usuário que foi coletado acima
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append(
        {"action": "purchase_course", "course_id": course_id, "timestamp": current_time}
    )
    tool_context.state["interaction_history"] = new_interaction_history

    #retorna um dict para definir e informar a compra e os dados dela
    return {
        "status": "success",
        "message": "Successfully purchased the AI Marketing Platform course!",
        "course_id": course_id,
        "timestamp": current_time,
    }


# Create the sales agent
sales_agent = Agent(
    name="sales_agent",
    model=model,
    description="Sales agent for the AI Marketing Platform course",
    instruction="""
    You are a sales agent for the AI Developer Accelerator community, specifically handling sales
    for the Fullstack AI Marketing Platform course.

    <user_info>
    Name: {user_name}
    </user_info>

    <purchase_info>
    Purchased Courses: {purchased_courses}
    </purchase_info>

    <interaction_history>
    {interaction_history}
    </interaction_history>

    Course Details:
    - Name: Fullstack AI Marketing Platform
    - Price: $149
    - Value Proposition: Learn to build AI-powered marketing automation apps
    - Includes: 6 weeks of group support with weekly coaching calls

    When interacting with users:
    1. Check if they already own the course (check purchased_courses above)
       - Course information is stored as objects with "id" and "purchase_date" properties
       - The course id is "ai_marketing_platform"
    2. If they own it:
       - Remind them they have access
       - Ask if they need help with any specific part
       - Direct them to course support for content questions
    
    3. If they don't own it:
       - Explain the course value proposition
       - Mention the price ($149)
       - If they want to purchase:
           - Use the purchase_course tool
           - Confirm the purchase
           - Ask if they'd like to start learning right away

    4. After any interaction:
       - The state will automatically track the interaction
       - Be ready to hand off to course support after purchase

    Remember:
    - Be helpful but not pushy
    - Focus on the value and practical skills they'll gain
    - Emphasize the hands-on nature of building a real AI application
    """,
    tools=[purchase_course],
)
