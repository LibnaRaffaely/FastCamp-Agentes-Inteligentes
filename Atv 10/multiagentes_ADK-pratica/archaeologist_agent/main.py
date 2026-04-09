import asyncio

from google.adk.sessions import DatabaseSessionService
import os
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent

from archaeologist_agent.agent import archaeologist_agent
from google.adk.runners import Runner

from archaeologist_agent.utils import call_agent_async

model = LiteLlm(
    model="openrouter/openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


#Criação do local do BD
db_url = "sqlite+aiosqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

initial_state={
    "user_name": "Líbna Raffaely",
    "artifacts":[]
}

async def main_async():
    APP_NAME = "Archaeologist Agent"
    USER_ID = "LibnaRaffaely"

    #Processo de criação da sessão
    existing_sessions = await session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    if existing_sessions and len(existing_sessions.sessions) > 0: # type: ignore
        #Sessão mais recente será usada
        SESSION_ID = existing_sessions.sessions[0].id # type: ignore
        print(f"Continuing existing session: {SESSION_ID}")
    else:
        new_session =await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID = new_session.id # type: ignore
        print(f"Created new session: {SESSION_ID}")
        
    #Criação do Runner
    runner = Runner(
        agent=archaeologist_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    
    #Inicio do looping interativo
    print("\nWelcome to Achaeologist Agent Chat!")
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
