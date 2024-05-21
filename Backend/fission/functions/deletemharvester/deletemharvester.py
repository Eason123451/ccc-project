from flask import current_app
import logging, requests
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

    query = {
        "query": {
            "match_all": {}
        }
    }

    try:   
        # delete data to the elastic search
        client.delete_by_query(index='mastodon', body=query)
        current_app.logger.info('Indexed data into Elasticsearch')

    except Exception as e:
        return json.dumps({"delete data error": str(e)})

    return 'OK'
