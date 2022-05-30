from jina import Client
from docarray import Document

client = Client(host='localhost', port=23456)

query = Document(text="Can I catch COVID from my pet armadillo?")

search_filter = {"source": {"$eq": "biomedical"}}

results = client.search(query, parameters={"filter": search_filter})

for result in results:
    print(result.text)
