import os
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent

from google.adk.tools.tool_context import ToolContext

DB_SOLVENT={
        "madeira": {
            "solvente": "Aguarrás mineral ou etanol diluído",
            "procedimento": "Aplicar com cotonete ou pincel macio",
            "cuidado": "Evitar água em excesso pois pode causar expansão da madeira"
        },
        "metal_ferroso": {
            "solvente": "Etanol industrial ou acetona",
            "procedimento": "Aplicar com cotonete para remoção de resíduos orgânicos",
            "cuidado": "Utilizar inibidor de corrosão após limpeza"
        },
        "metal_nao_ferroso": {
            "solvente": "Etanol ou acetona",
            "procedimento": "Limpeza superficial com cotonete",
            "cuidado": "Evitar abrasão para não remover pátina histórica"
        },
        "ceramica": {
            "solvente": "Água destilada com detergente neutro",
            "procedimento": "Escova macia ou algodão",
            "cuidado": "Evitar imersão prolongada"
        },
        "vidro": {
            "solvente": "Água destilada ou etanol",
            "procedimento": "Aplicação leve com algodão",
            "cuidado": "Evitar choque térmico"
        },
        "osso": {
            "solvente": "Etanol diluído ou água destilada",
            "procedimento": "Limpeza leve com cotonete",
            "cuidado": "Material poroso, evitar saturação"
        },
        "marfim": {
            "solvente": "Água destilada mínima",
            "procedimento": "Aplicar com algodão seco levemente umedecido",
            "cuidado": "Evitar solventes fortes"
        },
        "pedra": {
            "solvente": "Água destilada ou etanol",
            "procedimento": "Escova macia ou algodão",
            "cuidado": "Evitar abrasivos"
        },
        "couro": {
            "solvente": "Etanol diluído",
            "procedimento": "Aplicação leve com algodão",
            "cuidado": "Evitar ressecamento do material"
        },
        "tecido": {
            "solvente": "Água destilada com detergente neutro",
            "procedimento": "Limpeza suave com algodão",
            "cuidado": "Evitar fricção"
        }
    }

model = LiteLlm(
    model="openrouter/openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


#Ferramenta que irá fornecer os cuidados de conservação de acordo com solventes
def get_solvent(context: ToolContext,material: str) -> dict:
    """Ferramenta para consulta de tecnicas de uso de solventes para conservação de peças arqueológicas"""
    
    material=material.lower()
    
    if material in DB_SOLVENT:
        return{
            "material": material,
            "recomendação": DB_SOLVENT[material]
        }
    else:
        return{
            "erro": "Material não encontrado",
            "Materiais disponíveis:": list(DB_SOLVENT.keys())
        }
    
    
    


conservation_specialist = Agent(
    name ="conservation_specialist",
    model=model,
    description= "Agente especialista em conservação",
    instruction="""
        Você é um especialista em conservação arqueológica.

Seu conhecimento sobre solventes é restrito EXCLUSIVAMENTE aos dados
fornecidos pela ferramenta `get_solvent`.

REGRAS DE FUNCIONAMENTO:

1. Sempre que o usuário perguntar sobre limpeza, conservação ou solventes
   para um artefato arqueológico, você DEVE utilizar a ferramenta `get_solvent`.

2. Nunca utilize conhecimento externo ou químico que não esteja presente
   na base `DB_SOLVENT`.

3. Não peça informações adicionais sobre o tipo específico do material
   (ex: tipo de tecido, tipo de pedra, tipo de madeira).
   Utilize apenas a categoria geral do material.

4. Materiais aceitos pela base:
   madeira
   metal_ferroso
   metal_nao_ferroso
   ceramica
   vidro
   osso
   marfim
   pedra
   couro
   tecido

5. Caso o material esteja entre os materiais suportados,
   consulte a ferramenta `get_solvent` e apresente:

   - solvente recomendado
   - procedimento de aplicação
   - cuidados de conservação

6. Caso o material não exista na base, informe que o material
   não está registrado na base de conservação disponível.

7. Sempre priorize o material já registrado no artefato no sistema.

Nunca solicite especificações adicionais se o material já existir
na base DB_SOLVENT.
    """,
    tools=[get_solvent],
)