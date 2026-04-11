from fastapi import FastAPI
import uvicorn
# Isso visa criar uma API simples com um único endpoint POST que processa os dados recebidos usando um método agent`send` execute

#recebe um agente como parametro
def create_app(agent):
    #instancia uma API com o nome app, que será o objeto registrados das rotas criadas
    app = FastAPI()
    
    #Aqui definimos a requisição post com rota /run
    #que irá receber o payload como Dict e enviará para o agente executar, aguardando o retorno para o envio da response desse /run
    # fluxo: Cliente → POST /run → FastAPI → agent.execute(payload) → resposta
    @app.post("/run")
    async def run(payload: dict):
        return await agent.execute(payload)
    
    #retorna a API pronta com seus métodos de requisições e implementações
    #estando pronta para ser executada pelo uvicorn
    return app