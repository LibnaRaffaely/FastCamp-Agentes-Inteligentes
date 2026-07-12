from google.cloud import vectorsearch_v1beta

import pandas as pd
from src.embeeding.config import PROJECT_ID, LOCATION  

df = pd.read_csv("data/mtsamples.csv").rename(columns={"Unnamed: 0": "index"})
df = df.fillna("")   # troca NaN por string vazia
df_demo = df.head(100)   

collection_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/medical-transcriptions-agent-demo"

 
data_client = vectorsearch_v1beta.DataObjectServiceClient() 

# Preparar lote de objetos de dados
batch_request = [] 
for _, row in df_demo.iterrows(): 
    batch_request.append({ 
        "parent": collection_path,  
        "data_object_id" : f"doc-{int(row['index'])}", 
        "data_object" : { 
            "data" : { 
                "index" : float (row[ 'index' ]), 
                "description" : row[ 'description' ], 
                "medical_specialty" : row[ 'medical_specialty' ], 
                "sample_name" : row[ 'sample_name' ], 
                "transcription" : row[ 'transcription' ], 
                "keywords" : row[ 'keywords' ]
            }, 
            # Vetores vazios acionam a geração automática de incorporação 
            "vectors" : {} 
        } 
    }) 
    
# Upload em lote (máximo de 250 por solicitação para gemini-embedding-001)
request = vectorsearch_v1beta.BatchCreateDataObjectsRequest( 
    parent=collection_path, 
    requests=batch_request[: 100 ]   # Processar em lotes
 ) 

response = data_client.batch_create_data_objects(request)
print(f"Ingestão concluída! {len(response.data_objects)} objetos criados.")
