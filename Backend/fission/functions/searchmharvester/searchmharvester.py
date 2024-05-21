from flask import current_app, request
import logging
import json, time
from datetime import datetime
from elasticsearch8 import Elasticsearch

def main():

    try:
        client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        ssl_show_warn = False,
        basic_auth=('elastic', 'epheli0AJ4eir9xaiM2muqu6eehee4oh'),
        timeout = 120)
        current_app.logger.info(f'Log in Elasticsearch client')

    except Exception as e:
        return json.dumps({"elastic client error": str(e)})

    size= request.headers['X-Fission-Params-Size']
    
    query = {
        "size": size,
        "query": {
            "match_all": {}
        },
        "sort": [
            {
                "created_at": {
                    "order": "desc"
                }
            },
            {
                "id": {
                    "order": "desc"
                }
            }
        ]
    }
    
    try:   
        # search data from the elastic search based on size
        response = client.search(index='mastodon', body=query)

        current_app.logger.info('Search data from the Elasticsearch')

        return json.dumps(response['hits']['hits'])

    except Exception as e:
        return json.dumps({"search data error": str(e)})
