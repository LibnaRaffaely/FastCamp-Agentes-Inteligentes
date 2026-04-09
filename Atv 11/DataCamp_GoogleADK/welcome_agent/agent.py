from google.adk.agents import Agent
from google.genai import types # For further configuration controls

# In every file, you need to define root_agent - This is important!
root_agent = Agent(

    name = "welcome_agent", # nome
    model = "gemini-2.0-flash", # modelo a ser usado
    description = "Greeting Agent", # apresentgação sobre o que é o agente
    instruction = "You are a helpful assistant that greets the user. Talk to me in a pirate manner.", # detalhamento sobre função

    generate_content_config=types.GenerateContentConfig(
        temperature=0.2, # define a criatividade do agente, qnt mais próximo de 0 mais determinísitco (as respostas serão padrões e exatas de acordo com o mesmo input)
        max_output_tokens=250 #máximo de tokens na resposta
    )
)

