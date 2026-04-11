from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json

# -----------------
# CRIANDO O AGENTE
# -----------------
stay_agent = Agent(
    name="stay_agent",
    #como estou usando o provedor openrouter adicionei openrouter/ ao caminhon até a LLM
    model=LiteLlm("openrouter/openai/gpt-4o"),
    description="Suggests suitable accommodations for a user's trip.",
    instruction=(
        "Given a destination, travel dates, and budget, suggest 2-3 accommodation options. "
        "For each option, provide name, type (hotel, hostel, Airbnb, etc.), location (area/neighborhood), "
        "price per night estimate, and a short description. "
        "Prefer realistic and well-known accommodation types. "
        "Respond in plain English. Keep it concise and well-formatted."
    )
)

# -----------------
# CRIANDO sessão
# -----------------
session_service = InMemorySessionService()

runner = Runner(
    agent=stay_agent,
    app_name="stay_app",
    session_service=session_service
)

USER_ID = "user_stay"
SESSION_ID = "session_stay"


# -----------------
# CRIANDO execute 
# -----------------
async def execute(request):
    #definimos melhor a session
    session_service.create_session(
        app_name="stay_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    #Definimos o Prompt para o agente de atividades , pegando do parametro da função request(que é o envio do payload pelo server)
    # do request selecionamos as chaves que precisamos dos dados 
    prompt = (
        f"User is traveling to {request['destination']} from {request['start_date']} to {request['end_date']}, "
        f"with a budget of {request['budget']}. "
        f"Suggest 2-3 accommodation options, each including name, type, location, price per night, and description. "
        f"Respond in JSON format using the key 'stays' with a list of accommodation objects."
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
                if "stays" in parsed and isinstance(parsed["stays"], list):
                    return {"stays": parsed["stays"]}
                else:
                    print("'stays' key missing or not a list in response JSON")
                    return {"stays": response_text}  # fallback to raw text
            except json.JSONDecodeError as e:
                print("JSON parsing failed:", e)
                print("Response content:", response_text)
                return {"stays": response_text}  # fallback to raw text