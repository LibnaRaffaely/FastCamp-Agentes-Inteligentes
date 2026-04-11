from common.a2a_server import create_app
from .task_manager import run

#A explicação está no arquivo de mesmo nome na pasta activities_agent, pois o funcionamento é igual
app = create_app(agent=type("Agent", (), {"execute": run}))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)