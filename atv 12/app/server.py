import logging
import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from app.calendar_agent.orchestrator_agent import root_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name="calendar_agent", session_service=session_service)

class Message(BaseModel):
    session_id: str
    message: str

def _get_or_create_session(session_id: str):
    session = session_service.get_session(
        app_name="calendar_agent", user_id=session_id, session_id=session_id
    )
    if session is None:
        session = session_service.create_session(
            app_name="calendar_agent", user_id=session_id, session_id=session_id
        )
    return session

def _reset_session(session_id: str):
    try:
        session_service.delete_session(
            app_name="calendar_agent", user_id=session_id, session_id=session_id
        ) # type: ignore
    except Exception:
        pass
    session_service.create_session(
        app_name="calendar_agent", user_id=session_id, session_id=session_id
         )# type: ignore

@app.post("/chat")
async def chat(body: Message):
    from google.genai import types

    _get_or_create_session(body.session_id)

    content = types.Content(role="user", parts=[types.Part(text=body.message)])
    response_text = ""
    try:
        async for event in runner.run_async(
            user_id=body.session_id, session_id=body.session_id, new_message=content
        ):
            if event.is_final_response() and event.content:
                response_text = event.content.parts[0].text  # type: ignore
    except Exception as e:
        logger.error("Erro no agente: %s\n%s", e, traceback.format_exc())
        _reset_session(body.session_id)
        raise HTTPException(status_code=500, detail=str(e))

    return {"response": response_text}
