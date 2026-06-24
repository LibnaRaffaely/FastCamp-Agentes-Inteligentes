import asyncio

# Import the main customer service agent
from customer_service_agent.agent import customer_service_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import add_user_query_to_history, call_agent_async

load_dotenv()

# Parte 1
# Usaremos a memorial local e momentânea do terminal
session_service = InMemorySessionService()


# Parte 2 
# Formato que virá armazenado nossos dados
initial_state = {
    "user_name": "Líbna Raffaely",
    "purchased_courses": [],
    "interaction_history": [],
}


async def main_async():
    # Setup constants
    APP_NAME = "Customer Support"
    USER_ID = "aiwithlibna"

    # Parte 3
    # Criando a sessão
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    
    
    SESSION_ID = new_session.id
    print(f"Created new session: {SESSION_ID}")

    # Parte 4
    # Criando o RUnner da aplicação
    runner =  Runner(
        agent=customer_service_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Parte 5
    # Looping de interação com o usuário
    print("\nWelcome to Customer Service Chat!")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        # Get user input
        user_input = input("You: ")

        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break

        # Update interaction history with the user's query
        await add_user_query_to_history(
            session_service, APP_NAME, USER_ID, SESSION_ID, user_input
        )

        # Process the user query through the agent
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

    # Parte 6
    # Show final session state
    final_session = session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print("\nFinal Session State:")
    for key, value in final_session.state.items(): # type: ignore
        print(f"{key}: {value}")


def main():
    """Entry point for the application."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
