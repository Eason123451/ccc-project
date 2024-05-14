from elasticsearch8 import Elasticsearch
import json
from flask import current_app

def main():
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'epheli0AJ4eir9xaiM2muqu6eehee4oh')
    )

    try:
        info = client.info()
        current_app.logger.info("Connected to Elasticsearch")
        current_app.logger.info(info)
        return info
    except Exception as e:
        error_message = f"Error: {str(e)}"
        current_app.logger.error(error_message)
        return json.dumps({"error": error_message}, indent=2)
    



def main():
    try:
        client = Elasticsearch(
            'https://elasticsearch-master.elastic.svc.cluster.local:9200',
            verify_certs=False,
            ssl_show_warn=False,
            basic_auth=('elastic', 'epheli0AJ4eir9xaiM2muqu6eehee4oh')
        )

        query = {
            "_source": ["twitter.Sentiment", "twitter.Created_At"],
            "query": {
                "match_all": {}
            }
        }

        response = client.search(index="twitter", body=query)

        results = []
        for doc in response['hits']['hits']:
            twitter_list = doc['_source'].get('twitter', [])

            for item in twitter_list:
                created_at = item['Created_At']
                results.append(created_at)
                current_app.logger.info(f'Found Created_At: {created_at}')
                current_app.logger.info(f'Found document')

        return json.dumps(results)
    except Exception as e:
        error_message = f"Error: {str(e)}"
        current_app.logger.error(error_message)
        return json.dumps({"error": error_message}, indent=2)