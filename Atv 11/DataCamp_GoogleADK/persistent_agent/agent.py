# Our Imports
import asyncio
import time
import uuid
from dotenv import load_dotenv

from google.adk.sessions import DatabaseSessionService
from google.adk.agents   import Agent
from google.adk.runners  import Runner
from google.genai        import types # type: ignore
from google.adk.events.event import Event

# We are going to create our own habit agent!

load_dotenv()

DB_URL   = "sqlite:///./habit_data.db"         # persistent storage file
APP_NAME = "Habit Tracker"
USER_ID  = "libna"

# Essas 3 def abaixo são tools que nosso agente terá acesso e irá usar para manipular nosso contexto

# Adding the habit
def add_habit(habit: str, tool_context ) -> dict:
    """Add a new habit to track"""
    habits = tool_context.state.get("habits", [])
    habits.append({"habit": habit})
    tool_context.state["habits"] = habits

    print(f"[State] Added habit: {habit}")
    print_habits(habits)

    return {
        "action": "add_habit",
        "habit": habit,
        "message": f"Added habit: {habit}"
    }

# Viewing the habit
def view_habits(tool_context ) -> dict:
    """View all current habits"""
    habits = tool_context.state.get("habits", [])

    print_habits(habits)

    return {
        "action": "view_habits",
        "message": "Here are your current habits"
    }

# Deleting the habit
def delete_habit(index: int, tool_context ) -> dict:
    """Delete a habit by its index (1-based)"""
    habits = tool_context.state.get("habits", [])

    if 1 <= index <= len(habits):
        removed = habits.pop(index - 1)
        tool_context.state["habits"] = habits

        print(f"[State] Deleted habit {index}: {removed['habit']}")
        print_habits(habits)

        return {
            "action": "delete_habit",
            "index": index,
            "message": f"Deleted habit {index}: {removed['habit']}"
        }

    return {
        "action": "delete_habit",
        "index": index,
        "message": f"Invalid habit index: {index}"
    }

# defining our agent here!
habit_agent = Agent(
    name="habit_agent",
    model="gemini-2.5-flash",
    description="Persistent habit-tracking assistant",
    instruction="""
You help users track daily habits. You have access to the current state and can modify it.

When the user:
  • says "add X"          → call add_habit("X")
  • says "view"           → call view_habits()
  • says "delete N"       → call delete_habit(N)

Always greet the user by name and confirm any action taken.

Current state:
- user_name: {user_name}
- habits: {habits}
""",
    tools=[add_habit, view_habits, delete_habit],
)

# criando nossa session
service = DatabaseSessionService(db_url=DB_URL)
initial_state = {"user_name": "libna", "habits": []}

# seeing if we have a pre-existing session
resp = service.list_sessions(app_name=APP_NAME, user_id=USER_ID)
if resp.sessions:
    SESSION_ID = resp.sessions[0].id
    print("Continuing session:", SESSION_ID)
else:
    SESSION_ID = service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    ).id
    print("Created new session:", SESSION_ID)

# creating our runner
runner = Runner(agent=habit_agent, app_name=APP_NAME, session_service=service)

# Printing habits - FOR DEBUGGING PURPOSES (can delete if needed)
def print_habits(habits):
    if not habits:
        print("[Habits] (none)")
    else:
        print("[Habits]")
        for idx, h in enumerate(habits, 1):
            print(f"  {idx}. {h.get('habit')}")

# function to call the agent
async def ask_agent(text: str): # for improved efficiency
    msg = types.Content(role="user", parts=[types.Part(text=text)])
    
    async for ev in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=msg
    ):
        # Only print the assistant's text part, ignore warnings about non-text parts
        if ev.is_final_response() and ev.content and ev.content.parts:
            # Only print text parts
            for part in ev.content.parts:
                if hasattr(part, 'text') and part.text:
                    print("\nAssistant:", part.text)


# our loop to chat with our agent
async def main():
    print("\nHabit Tracker ready (type 'quit' to exit)\n")
    while True:
        q = input("You: ")
        if q.lower() in ("quit", "exit"):
            print("Session saved. Bye!")
            break
        await ask_agent(q)

if __name__ == "__main__":
    asyncio.run(main())
