from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json

# -----------------
# CRIANDO O AGENTE
# -----------------
activities_agent = Agent(
    name="activities_agent",
    #como estou usando o provedor openrouter adicionei openrouter/ ao caminhon até a LLM
    model=LiteLlm("openrouter/openai/gpt-4o"),
    description="Suggests interesting activities for the user at a destination.",
    instruction=(
        "Given a destination, dates, and budget, suggest 2-3 engaging tourist or cultural activities. "
        "For each activity, provide a name, a short description, price estimate, and duration in hours. "
        "Respond in plain English. Keep it concise and well-formatted."
    )
)

# -----------------
# CRIANDO sessão
# -----------------
session_service = InMemorySessionService()

runner = Runner(
    agent=activities_agent,
    app_name="activities_app",
    session_service=session_service
)

USER_ID = "user_activities"
SESSION_ID = "session_activities"


# -----------------
# CRIANDO execute 
# -----------------
async def execute(request):
    #definimos melhor a session
    session_service.create_session(
        app_name="activities_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    #Definimos o Prompt para o agente de atividades , pegando do parametro da função request(que é o envio do payload pelo server)
    # do request selecionamos as chaves que precisamos dos dados 
    prompt = (
        f"User is flying to {request['destination']} from {request['start_date']} to {request['end_date']}, "
        f"with a budget of {request['budget']}. Suggest 2-3 activities, each with name, description, price estimate, and duration. "
        f"Respond in JSON format using the key 'activities' with a list of activity objects."
    )
    
    
    #Montamos a mensagem e realizamos o envio com o runner
    #nesse looping de run_async, é pego todos os retornos de eventos assincronos de até is_final_response()
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            response_text = event.content.parts[0].text # type: ignore
            
            #Leitura dos dados do Json e envio em formato de dict
            try:
                parsed = json.loads(response_text) # type: ignore
                if "activities" in parsed and isinstance(parsed["activities"], list):
                    return {"activities": parsed["activities"]}
                else:
                    print("'activities' key missing or not a list in response JSON")
                    return {"activities": response_text}  # fallback to raw text
            except json.JSONDecodeError as e:
                print("JSON parsing failed:", e)
                print("Response content:", response_text)
                return {"activities": response_text}  # fallback to raw text