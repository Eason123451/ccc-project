from elasticsearch import Elasticsearch
import json
import logging
from flask import Flask

app = Flask(__name__)

def search_twitter():
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'epheli0AJ4eir9xaiM2muqu6eehee4oh')
    )

    query = {
        "_source": ["sentiment", "time"],
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
            app.logger.info(f'Found Created_At: {created_at}')

    return json.dumps(results)

@app.route('/search')
def search():
    return search_twitter()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
