import json
from elasticsearch8 import Elasticsearch

def get_data(port, index_name, scroll_size, scroll_time):
    client = Elasticsearch(
        port,
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'epheli0AJ4eir9xaiM2muqu6eehee4oh'),
        request_timeout=120,
        retry_on_timeout=True,  # Retries on timeout
        max_retries=3  # Sets the maximum number of retries
    )

    response = client.search(
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
        response = client.scroll(
            scroll_id=scroll_id,
            scroll=scroll_time
        )
        if len(response['hits']['hits']) == 0:
            break
        data.extend(response['hits']['hits'])
        scroll_id = response['_scroll_id']
    
    all_docs = [doc['_source'] for doc in data]
    return json.dumps(all_docs)