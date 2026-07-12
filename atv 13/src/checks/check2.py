from google.cloud import vectorsearch_v1beta
from src.embeeding.config import PROJECT_ID, LOCATION

search_client = vectorsearch_v1beta.DataObjectSearchServiceClient()
collection_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/medical-transcriptions-agent-demo"

request = vectorsearch_v1beta.QueryDataObjectsRequest(parent=collection_path)
count = 0
for obj in search_client.query_data_objects(request=request):
    count += 1
print(f"Total de objetos na collection: {count}")
