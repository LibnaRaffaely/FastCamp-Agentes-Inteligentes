import uuid # Used to generate a unique session ID
from google.adk.sessions import InMemorySessionService # in-memory service that stores user data
from google.adk.agents   import Agent
from google.adk.runners  import Runner # connects the session and the agent together
from google.genai import types # tools to define user messages
from dotenv import load_dotenv

load_dotenv() # Loading our API keys

chef = Agent(
    name="InformationAgent",
    model="gemini-2.5-flash",
    instruction="User's favourite colour is {fav_color}, name {name}, and favourite subject: {fav_subject}. Answer questions about it."
)
# A instrução possui variáveis, que irtão coletar o estado da sessão antes de cada invocação/chamada do agente


service = InMemorySessionService() # é definida o formado da sessão, que armazena o estado de memória na conversa

session_id  = str(uuid.uuid4()) #  Gerador de I unico para a sessão

# Após definirmos acima (L18) o tipo de session e sua memoria, iremos instanciar e criar a memória com os dados de estado e contextos necessários
service.create_session(   
    app_name="InformationApp", # nome do sistema
    user_id="LibRaf", # é instanciado o Usuário da sessão, definindo ele
    session_id=session_id, # id único que geramos na L20
    state={"fav_color": "Roxo",  #Instanciamos estados dessa memória, criando um dict com dados importantes a serem armazenados                  
           "name": "Libna Raffaely", 
           "fav_subject":"Biologia"},
)

# Instanciamos e criamos nosso Runner, que irá unir a session e o agente
waiter = Runner(agent=chef, session_service=service, app_name="InformationApp")

#vamos simular um envio de mensagem pelo usuário, apenas definindo a role
msg = types.Content(role="user", parts=[types.Part(text="What is my name and what color do I like? ")])


for ev in waiter.run(user_id="LibRaf", session_id=session_id, new_message=msg):
    print(ev)
    if ev.is_final_response() and ev.content and ev.content.parts:
        print(ev.content.parts[0].text) # only prints the final response that has content 
        print("-----------")   

"""
#------
1. Runner retrieves session by user_id, session_id
2. Fills placeholders in the prompt with state (roxo, Libna Raffaeçy  , Biologia)
3. Calls Gemini - our base LLM
4. Outputs a response
#------
"""

# pegamos a sessão dentro da memória para printarmos ela 
session = service.get_session(app_name="InformationApp", user_id="LibRaf", session_id=session_id)

# 6️⃣ Print updated state
print("\n📘 Final session state:")
for key, value in session.state.items():
    print(f"{key}: {value}")


# Learning: the model can’t modify the state by itself! So we need a way to be able to parse it!
