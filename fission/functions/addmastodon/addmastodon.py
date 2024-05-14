import logging, json
from flask import current_app, request
from elasticsearch8 import Elasticsearch

def main():
    client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        ssl_show_warn= False,
        basic_auth=('elastic', 'epheli0AJ4eir9xaiM2muqu6eehee4oh')
    )

    current_app.logger.info(f'Mastodon Toot to add:  {request.get_json(force=True)}')

    for toot in request.get_json(force=True):
        res = client.index(
            index='mastodon',
            id=f'{toot["id"]}',
            body=toot
        )
        current_app.logger.info(f'Indexed toot {toot["id"]}')

    return 'ok'
