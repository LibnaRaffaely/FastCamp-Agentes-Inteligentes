import httpx

# função assíncrona que envia uma solicitação POST para uma URL específica com uma determinada carga/payload
#payload: são os dados a serem enviados no corpo da requisição HTTP
async def call_agent(url, payload):
    async with httpx.AsyncClient() as client:
        # envia uma requisição post com a url, os dados e o tempo max de espera, 
        # o await é p/ aguardar a resposta e qnd chegar armazena na response
        response = await client.post(url, json=payload, timeout=60.0)
        
        #aponta uma exceção caso a response tenha um status de falha (4xx ou 5xx)
        response.raise_for_status()
        
        #retorna em formato Json a resposta 
        return response.json()