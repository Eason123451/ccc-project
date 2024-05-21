from elasticsearch8 import Elasticsearch
from flask import current_app, request
import json

def main():

    try:
        client = Elasticsearch(
            'https://elasticsearch-master.elastic.svc.cluster.local:9200',
            verify_certs=False,
            ssl_show_warn=False,
            basic_auth=('elastic', 'epheli0AJ4eir9xaiM2muqu6eehee4oh'),
            request_timeout=120,
            max_retries=3,
            retry_on_timeout=True
        )
        current_app.logger.info(f'Log in Elasticsearch client')
    except Exception as e:
            return json.dumps({"elastic client error": str(e)})

    index_name = 'viccrime_twitter'
    scroll_size = 1000
    scroll_time = '2m'

    try:
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
        current_app.logger.info('The first part of data is searched from the Elasticsearch')
        current_app.logger.info('Start searching remaining data from the Elasticsearch')
        while True:
            response = client.scroll(
                scroll_id=scroll_id,
                scroll=scroll_time
            )
            if len(response['hits']['hits']) == 0:
                break
            data.extend(response['hits']['hits'])

            scroll_id = response['_scroll_id']
        current_app.logger.info('Finish the searching')
    except Exception as e:
        return json.dumps({"search data error": str(e)})
    
    all_docs = [doc['_source'] for doc in data]
    return json.dumps(all_docs)
