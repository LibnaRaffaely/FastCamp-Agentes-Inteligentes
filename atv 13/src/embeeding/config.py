from google.cloud import vectorsearch_v1beta 
from dotenv import load_dotenv
from google.api_core import exceptions
import os


load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID") 
LOCATION = os.getenv("LOCATION")         

admin_client = vectorsearch_v1beta.VectorSearchServiceClient() 


collection_config = {
    # Data schema: defines the structure of your data fields
    "data_schema": {
        "type": "object",
        "properties": {
            "index": {"type": "number"},
            "description": {"type": "string"},
            "medical_specialty": {"type": "string"},
            "sample_name": {"type": "string"},
            "transcription": {"type": "string"},
            "keywords": {"type": "string"}
        }
    },
    # Vector schema: configures automatic embedding generation
    "vector_schema": {
        "description_embedding": {
            "dense_vector": {
                "dimensions": 768,
                "vertex_embedding_config": {
                    "model_id": "gemini-embedding-001",
                    # combinação entre 
                    "text_template": "sample: {sample_name}. transcription: {transcription}. keywords: {keywords}",
                    "task_type": "RETRIEVAL_DOCUMENT"
                }
            }
        }
    }
}

request = vectorsearch_v1beta.CreateCollectionRequest( 
        parent= f"projects/{PROJECT_ID}/locations/{LOCATION}" , 
        collection_id= "medical-transcriptions-agent-demo" , 
        collection=collection_config 
    ) 

try:
    operation = admin_client.create_collection(request=request) 
    print("Criando nova coleção...")
    operation.result()
    print("Coleção criada com sucesso!")
except exceptions.AlreadyExists:
    print("A coleção já existe. Prosseguindo para a próxima etapa...")
