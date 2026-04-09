import uuid                      
from dotenv import load_dotenv   
from pydantic import BaseModel, Field # We are going to use structured outputs again!
from google.adk.sessions import InMemorySessionService
from google.adk.agents   import Agent
from google.adk.runners  import Runner
from google.genai        import types

load_dotenv()  

#definindo nosso output estruturado
class StateOutput(BaseModel):
    fav_color: str    = Field(description="Favourite colour of user.")
    name:      str    = Field(description="Name of the user.")
    fav_subject: str  = Field(description="Favourite subject of the user.")

# Recriando o mesmo agente de agent.py porém estruturando o output
chef = Agent(
    name="InformationAgent",
    model="gemini-2.5-flash",
    instruction="""
You are a helpful assistant that knows the user's name, favorite colour, and favorite subject.

Current state:
- name: {name}
- fav_color: {fav_color}
- fav_subject: {fav_subject}

If the user asks to update anything, reply *only* with JSON matching this schema: 

{
  "fav_color": "<new colour>",
  "name": "<new name>",
  "fav_subject": "<new subject>"
}

When updating, preserve existing values for fields that should remain the same. Only change the specific fields mentioned by the user.

Otherwise, answer their question in plain text.
""",
    output_schema=StateOutput,    # forçamos que a saída tenha o formado da classe definida no inicio
    output_key="state"            # nome do output que queremos dentro do state da session
)

#recriando dados essenciais e a mesma sessão anterior
service    = InMemorySessionService()
session_id = str(uuid.uuid4())

service.create_session(
    app_name="InformationApp",
    user_id="LibRaf",
    session_id=session_id,
    # same state as before
    state={"fav_color": "Roxo",                   
           "name": "Libna Raffaely", 
           "fav_subject":"Biologia",
    },
)

# criação do mesmo runner
waiter = Runner(
    agent=chef,
    session_service=service,
    app_name="InformationApp"
)

# enviando uma mensagem do usuário para o agente realizar essas alterações no estado
msg = types.Content(
    role="user",
    parts=[types.Part(text=(
        "Please change my favorite color to red and my favourite subject to Computer Science."
    ))]
)

# Executando o agente e capturando a saída bruta.
for ev in waiter.run(user_id="LibRaf", session_id=session_id, new_message=msg):
    if ev.is_final_response() and ev.content and ev.content.parts:
        raw = ev.content.parts[0].text
        print(raw, "\n")
        print("------------------------")

# reccebendo os dados e estados da sessão informada
session = service.get_session(
    app_name="InformationApp",
    user_id="LibRaf",
    session_id=session_id
)

# verificamos se temos o output estruturado como definimos na L41 e L40
if "state" in session.state:
    structured_data = session.state["state"]
    print("✅ Updating session state:")
    
    # por meio de um for ele percorre os dados estruturados que coletamos na L91 
    # e associa os nomes das variáveis á chaves e anexa seus conteudos a ela dentro do estado da sessão principal,
    # armazenando elas sobre o que definimos anteriormente
    
    for key, value in structured_data.items():
        session.state[key] = value
        print(f"  - {key} updated to: {value}")
    
    # remove o estado state que criamos na L41
    del session.state["state"]
else:
    print("No structured output found in session state.")

# Printing the new session state to confirm
print("\n📘 Final session state:")
for key, value in session.state.items():
    print(f"{key}: {value}")