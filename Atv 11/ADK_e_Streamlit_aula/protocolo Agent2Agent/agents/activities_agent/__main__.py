from common.a2a_server import create_app
from .task_manager import run

#chama a função do a2aServer que criamos antes 
# e passa a função run de task_manager -> para que tenha o acesso ao agente e toda as regras
app = create_app(agent=type("Agent", (), {"execute": run}))

#toda vez que rodamos um arquivo existe um parametro __name__, e se corresponder com main ele irá rodar esse arquivo 
# (ex: python main.py = __name__ == "__main__" → True)
#Isso é importante pois caso n usassemos isso, ao importar iria subir e iniciar a aplicação na porta 8003
#uvicorn = servidor ASGI para executar aplicações web em Python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8003)