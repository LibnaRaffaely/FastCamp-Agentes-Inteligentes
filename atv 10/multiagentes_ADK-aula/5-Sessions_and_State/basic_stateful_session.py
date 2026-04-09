import uuid
import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent.agent import question_answering_agent

load_dotenv()


# é criada o tipo de serviço com memória local, que quando finalizarmos a sessão serão perdidos os dados
session_service_stateful = InMemorySessionService()

#Se trata de um dicionário que contém o  nome e preferências do usuário
#Esses dados serão  utilizados pela LLM
initial_state = {
    "user_name": "Brandon Hancock",
    "user_preferences": """
        I like to play Pickleball, Disc Golf, and Tennis.
        My favorite food is Mexican.
        My favorite TV show is Game of Thrones.
        Loves it when people like and subscribe to his YouTube channel.
    """,
}

# Criação de uma nova sessão
APP_NAME = "Brandon Bot"
USER_ID = "brandon_hancock"
SESSION_ID = str(uuid.uuid4()) #gerador automático  do ID de sessão
stateful_session = asyncio.run(session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
))
print("CREATED NEW SESSION:")
print(f"\tSession ID: {SESSION_ID}")

# para o RUNNER é importante a instanciação de um agente e sessão
runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service=session_service_stateful,
)

new_message = types.Content(
    role="user", parts=[types.Part(text="What is Brandon's favorite TV show?")]
)

for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Final Response: {event.content.parts[0].text}")

print("==== Session Event Exploration ====")
session = asyncio.run(session_service_stateful.get_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
))

# Log final Session state
print("=== Final Session State ===")
for key, value in session.state.items(): # type: ignore
    print(f"{key}: {value}")
