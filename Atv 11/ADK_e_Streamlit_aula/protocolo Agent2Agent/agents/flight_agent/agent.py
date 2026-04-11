from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json

# -----------------
# CRIANDO O AGENTE
# -----------------
flight_agent = Agent(
    name="flight_agent",
    model=LiteLlm("openrouter/openai/gpt-4o"),
    description="Finds suitable flight options for a given trip.",
    instruction=(
        "Given an origin, destination, travel dates, and budget, suggest 2-3 flight options. "
        "For each option, include airline, departure and arrival times, total duration, and estimated price. "
        "Prefer practical routes with reasonable travel time and minimal layovers. "
        "Respond in plain English. Keep it concise and well-formatted."
    )
)

# -----------------
# CRIANDO sessão
# -----------------
session_service = InMemorySessionService()

runner = Runner(
    agent=flight_agent,
    app_name="flight_app",
    session_service=session_service
)

USER_ID = "user_flight"
SESSION_ID = "session_flight"


# -----------------
# CRIANDO execute 
# -----------------
async def execute(request):
    #definimos melhor a session
    session_service.create_session(
        app_name="flight_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    #Definimos o Prompt para o agente de atividades , pegando do parametro da função request(que é o envio do payload pelo server)
    # do request selecionamos as chaves que precisamos dos dados 
    prompt = (
        f"User is traveling from {request['origin']} to {request['destination']} "
        f"between {request['start_date']} and {request['end_date']}, "
        f"with a budget of {request['budget']}. "
        f"Suggest 2-3 flight options, each including airline, departure time, arrival time, duration, and price estimate. "
        f"Respond in JSON format using the key 'flights' with a list of flight objects."
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
                if "flight" in parsed and isinstance(parsed["flight"], list):
                    return {"flight": parsed["flight"]}
                else:
                    print("'flight' key missing or not a list in response JSON")
                    return {"flight": response_text}  # fallback to raw text
            except json.JSONDecodeError as e:
                print("JSON parsing failed:", e)
                print("Response content:", response_text)
                return {"flight": response_text}  # fallback to raw text