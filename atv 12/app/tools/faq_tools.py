from google.adk.tools.tool_context import ToolContext

INTENT_TO_TOPICS = {
    "faq": {"horario_atendimento", "endereco", "funcionamento_sessao", "valores_pagamento", "vestimentas"},
    "outros_sistemas": {"agendamento", "cancelamento", "confirmacao", "fora_de_contexto"},
}

VALID_TOPICS = {t for topics in INTENT_TO_TOPICS.values() for t in topics}


def save_classification(topic: str = "", tool_context: ToolContext = None) -> dict:
    """
    Persiste a classificação de intenção no estado da sessão.

    Determina automaticamente o `intent` de roteamento ("faq" ou "outros_sistemas")
    a partir do `topic` granular classificado.

    Args:
        topic: Sub-categoria classificada. Valores aceitos:
               FAQ       → horario_atendimento | endereco | funcionamento_sessao |
                           valores_pagamento | vestimentas
               Outros    → agendamento | cancelamento | confirmacao | fora_de_contexto

    Returns:
        Dicionário com intent de roteamento e topic salvo no estado.
    """
    if not topic or topic not in VALID_TOPICS:
        return {
            "status": "error",
            "message": f"Tópico inválido '{topic}'. Use: {sorted(VALID_TOPICS)}",
        }

    intent = next(k for k, topics in INTENT_TO_TOPICS.items() if topic in topics)

    tool_context.state["intent"] = intent
    return {"status": "ok", "intent": intent}
