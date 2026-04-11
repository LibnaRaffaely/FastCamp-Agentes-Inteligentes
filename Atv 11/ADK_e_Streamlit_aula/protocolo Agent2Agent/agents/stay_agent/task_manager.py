from .agent import execute

#essa função é assincrona e roda o execute do agente 
async def run(payload):
    #o await pausa run até que execute finalize
    return await execute(payload)
