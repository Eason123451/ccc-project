from flask import request, current_app
import requests, logging

def main():
    current_app.logger.info(f'Received request: ${request.headers}')
    r = requests.get('https://elasticsearch-master.elastic.svc.cluster.local:9200/_cluster/health',
        verify=False,
        auth=('elastic', 'epheli0AJ4eir9xaiM2muqu6eehee4oh'))
    current_app.logger.info(f'Status ES request: {r.status_code}')
    return r.json()
