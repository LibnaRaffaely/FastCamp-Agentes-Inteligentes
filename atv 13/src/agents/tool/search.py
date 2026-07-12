from google.cloud import vectorsearch_v1beta
from typing import Any
from dotenv import load_dotenv
import os
import json


load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID") 
LOCATION = os.getenv("LOCATION")  

search_client = vectorsearch_v1beta.DataObjectSearchServiceClient()
collection_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/medical-transcriptions-agent-demo"


def search_cases(symptoms: str, keywords: str, filter: str = "") -> list[dict[str, Any]]:
    print("\n>>> TOOL CALL: find_rentals (Hybrid Search)")
    print(f"    Query: {symptoms}")
    print(f"    keywords: {keywords if keywords else 'None'}")
    
    # # Parse Filter JSON (if provided)
    # filter_dict = None
    # if filter.strip():
    #     try:
    #         filter_dict = json.loads(filter)
    #     except json.JSONDecodeError:
    #         print("    Warning: Invalid JSON filter, ignoring.")
            
    try:
        
        # Busca semantica
        semantic_search = vectorsearch_v1beta.SemanticSearch(
            search_text=symptoms,
            search_field="description_embedding",  # The vector field to search
            # filter=filter_dict,  
            task_type= vectorsearch_v1beta.EmbeddingTaskType.QUESTION_ANSWERING,
            top_k=10,
            output_fields=vectorsearch_v1beta.OutputFields(
                data_fields=["sample_name", "description", "medical_specialty", "keywords", "transcription"] # Dados que serão retornados
            )
        )
        
        # Busca sintática
        text_search = vectorsearch_v1beta.TextSearch(
            search_text=keywords,
            data_field_names=["sample_name","medical_specialty", "keywords", "transcription", "description"],
            # filter=filter_dict,  # Metadata filtering supported
            top_k=10,
            output_fields=vectorsearch_v1beta.OutputFields(
                data_fields=["sample_name", "description", "medical_specialty", "keywords", "transcription"]# Dados que serão retornados
            ),
        )
        
        # Criação da request unindo os 2 tipos de busca
        request = vectorsearch_v1beta.BatchSearchDataObjectsRequest(
            parent=collection_path,
            searches=[
                vectorsearch_v1beta.Search(semantic_search=semantic_search),
                vectorsearch_v1beta.Search(text_search=text_search),
            ],
            combine=vectorsearch_v1beta.BatchSearchDataObjectsRequest.CombineResultsOptions(
                ranker=vectorsearch_v1beta.Ranker(
                    rrf=vectorsearch_v1beta.ReciprocalRankFusion(
                        weights=[0.6, 0.4] # aqui eu atribuo um peso maior à busca semântica
                    )
                )
            ),
        )
        
        response = search_client.batch_search_data_objects(request=request)
        
        results = []
        if response.results and response.results[0].results:
            for res in response.results[0].results:
                data = dict(res.data_object.data)
                results.append(
                    {
                        "sample_name": data.get("sample_name"),
                        "description": data.get("description"),
                        "medical_specialty": data.get("medical_specialty"),
                        "keywords": data.get("keywords"),
                    }
                )

        print(f"    Found: {len(results)} listings")
        return results
        
    except Exception as e:
        print(f"    Error: {e}")
        return []
    
    
if __name__ == "__main__":
    for r in search_cases("dor no peito e falta de ar", ""):
         print(r["medical_specialty"], "->", r["sample_name"])