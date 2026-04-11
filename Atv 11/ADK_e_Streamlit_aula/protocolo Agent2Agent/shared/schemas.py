from pydantic import BaseModel

#Estabelece um padrão de dados para ser usados pelos agentes
class TravelRequest(BaseModel):
    origin: str
    destination: str
    start_date: str
    end_date: str
    budget: float