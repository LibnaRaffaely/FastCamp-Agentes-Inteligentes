import asyncio
import os

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from memory_agent.agent import memory_agent
from utils import call_agent_async

from google.adk.models.lite_llm import LiteLlm

load_dotenv()

model = LiteLlm(
    model="openrouter/openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Parte 1
# Iniciamos como queremos nosso banco de dados
# utilizamos o DatabaseSessionService para criá-lo
db_url = "sqlite+aiosqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)


# Parte 2
# Estruturamos o estado inicial e como serão guardados os dados a serem "lembrados"
initial_state = {
    "user_name": "Brandon Hancock",
    "reminders": [],
}



async def main_async():
    # Setup constants
    APP_NAME = "Memory Agent"
    USER_ID = "aiwithbrandon"

    # Parte 3
    # é iniciado uma sessão igual feito no modulo anterior
    #Na linha abaixo recebemos todas as sessões dentro do DB criado
    existing_sessions = await session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    # é verificado se existe alguma sessão retirado da consulta anterior, 
    # em caso positivo, coletamos o id dessa sessão para utilizá-lo
    if existing_sessions and len(existing_sessions.sessions) > 0: # type: ignore
        # Use the most recent session
        SESSION_ID = existing_sessions.sessions[0].id # type: ignore
        print(f"Continuing existing session: {SESSION_ID}")
    else:
        # Caso o DB esteja vazio é instanciado uma nova sessão dentro dele
        new_session =await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID = new_session.id # type: ignore
        print(f"Created new session: {SESSION_ID}")

    # Parte 4
    # Criação de um RUNNER com a sessão já instanciada
    runner =  Runner(
        agent=memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Parte 5
    # é Iniciado o ciclo de interação em looping
    print("\nWelcome to Memory Agent Chat!")
    print("Your reminders will be remembered across conversations.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        #pegando o input do usuário
        user_input = input("You: ")

        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Your data has been saved to the database.")
            break

        # Process the user query through the agent
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)


if __name__ == "__main__":
    asyncio.run(main_async())
