from elasticsearch import Elasticsearch
import json
import os

es = Elasticsearch(
    ['https://localhost:9200'],
    verify_certs=False,
    ssl_show_warn=False,
    basic_auth=('elastic', 'epheli0AJ4eir9xaiM2muqu6eehee4oh'),
    request_timeout=180,
    max_retries=20,
    retry_on_timeout=True
)

index_name = 'viccrime_twitter'
scroll_size = 1000
scroll_time = '2m'
response = es.search(
    index=index_name,
    body={
        "query": {"match_all": {}},
        "size": scroll_size
    },
    scroll=scroll_time
)
scroll_id = response['_scroll_id']
data = response['hits']['hits']
while True:
    response = es.scroll(
        scroll_id=scroll_id,
        scroll=scroll_time
    )
    if len(response['hits']['hits']) == 0:
        break
    data.extend(response['hits']['hits'])
    scroll_id = response['_scroll_id']
all_docs = [doc['_source'] for doc in data]
save_path = "/mnt/c/Users/Windows/Documents/GitHub/ccc-project/es vic crime/viccrime_twitter.json"
os.makedirs(os.path.dirname(save_path), exist_ok=True)
with open(save_path, 'w') as json_file:
    json.dump(all_docs, json_file, indent=2)

