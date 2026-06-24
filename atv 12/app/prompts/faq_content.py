"""Base de textos prontos para o agente de FAQ.

Preencha os blocos abaixo com os textos oficiais aprovados.
"""

FAQ_CONTENT = {
    "horario_atendimento": """
    [TOPICO] Horario de atendimento
    [RESPOSTA_OFICIAL]
    - Os atendimentos ocorrem de Segunda a Sexta das 12h às 18h, e aos sábados pela manhã.
        \nVocê tem preferência por um horário ou dia específico?
        \nAssim consigo olhar o melhor horário para você
    """.strip(),
    "endereco": """
    [TOPICO] Endereco
    [RESPOSTA_OFICIAL]
    - Rua - 4   Nr- 485  Qd- F3  Lt-34 Ed. Maria Coelho St.  Oeste - Goiânia -Go   Cep: 74.110-140
        \nSala 202.
    """.strip(),
    "funcionamento_sessao": """
    [TOPICO] Como funciona sessao
    [RESPOSTA_OFICIAL]
    - O Wemerson oferece uma variedade de tratamentos, como ventosaterapia, liberação miofascial, realinhamento postural e massoterapia. No momento do atendimento, ele realiza uma avaliação completa das suas necessidades e, por meio de uma conversa, define os procedimentos personalizados para o seu caso. A grande vantagem é que, ao agendar seu horário, você já inicia o tratamento durante a sessão, com um valor único, independentemente dos procedimentos realizados. O foco é sempre na sua saúde muscular, seja para definição ou tratamento de dores localizadas e crônicas.
    """.strip(),
    "valores_pagamento": """
    [TOPICO] Valores e formas de pagamento
    [RESPOSTA_OFICIAL]
    - A sessão está 190 reais, esão aceitos pagamentos em dinheiro, pix e cartão (com adicional de taxa da maquininha).
    """.strip(),
    "vestimentas": """
    [TOPICO] Vestimentas
    [RESPOSTA_OFICIAL]
    - Recomendamos que tanto homens quanto mulheres utilizem shorts de academia flexíveis, e para mulheres top. Mas pode ir da forma que se sinta mais confortável
    """.strip()
}


def render_faq_catalog() -> str:
    """Concatena os blocos de FAQ em um texto unico para instruction."""
    return "\n\n".join(FAQ_CONTENT.values())
