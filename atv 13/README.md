

# 1. Criar e ativar o ambiente virtual
    python -m venv .venv
    .venv\Scripts\Activate.ps1

# 2. Entrar na pasta
cd "atv 13" 

# 3. Instalar libs
pip install -r requirements.txt

# 4. ativar cloud cli 
gcloud auth application-default login
gcloud services enable vectorsearch.googleapis.com --project="fastcamp13-502212"

# 5. Criar a Collection e ingerir os dados
python -m src.embeeding.config      # cria a collection
python -m src.embeeding.ingestion   # ingere ~100 documentos

# 6. (Opcional) Verificar a ingestão
python -m src.checks.check           # lista collections
python -m src.checks.check2          # conta objetos
 

# 7. Rodar o agente (ADK)
adk web
------------------------
# Desligar o serviço para evitar custos
gcloud services disable aiplatform.googleapis.com --project="SEU_PROJECT_ID"

# Verificar índices/recursos
gcloud ai indexes list --region=us-central1 --project="SEU_PROJECT_ID"
