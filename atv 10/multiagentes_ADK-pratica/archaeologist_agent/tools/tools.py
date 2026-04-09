from datetime import datetime
import uuid

from google.adk.tools.tool_context import ToolContext

async def record_archaeological(tool_context: ToolContext, name: str, material: str, description: str,estimated_period: str )-> dict:
    """
        Ferramenta para registrar um artefato arqueológico encontrado
        durante a escavação.
    """
    
    #pegamos o dicionário instanciado pelo callback
    local =tool_context.state.get("local", {})
    
    record = {
        "artifact_id": f"ART-{uuid.uuid4()}",
        "name": name,
        "material": material,
        "description": description,
        "estimated_period": estimated_period,
        "local": local,
        "timestamp":datetime.now().isoformat()
    }
    
    artifacts = tool_context.state.get("artifacts", [])
    
    artifacts.append(record)
    tool_context.state["artifacts"]=artifacts
    
    return {
        "action": "Record a artifact",
        "artifact": name
    }
    
def get_list_artifacts(context: ToolContext) -> dict:
    """
    Retorna os artefatos arqueológicos registrados no banco de dados durante a escavação.
    """

    artifacts = context.state.get("artifacts", [])

    if not artifacts:
        return {
            "message": "Nenhum artefato foi registrado ainda."
        }

    return {
        "total": len(artifacts),
        "artifacts": artifacts
    }