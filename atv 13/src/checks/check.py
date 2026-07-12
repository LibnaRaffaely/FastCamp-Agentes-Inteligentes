from google.cloud import vectorsearch_v1beta
from src.embeeding.config import PROJECT_ID, LOCATION

admin_client = vectorsearch_v1beta.VectorSearchServiceClient()
parent = f"projects/{PROJECT_ID}/locations/{LOCATION}"

for col in admin_client.list_collections(parent=parent):
    print("Collection encontrada:", col.name)
