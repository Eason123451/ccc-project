import json
from flask import current_app
import requests, logging

def fetch_all_documents():
        
        es_url = 'https://elasticsearch-master.elastic.svc.cluster.local:9200'
        index_name = 'twitter'
        
        auth = ('elastic', 'epheli0AJ4eir9xaiM2muqu6eehee4oh')
        
        headers = {'Content-Type': 'application/json'}
        
        results = []
        
        from_ = 0
        size = 1
        
        while True:

            search_url = f'{es_url}/{index_name}/_search?size={size}&from={from_}'
            
            try:
                r = requests.get(search_url, auth=auth, headers=headers, verify=False, timeout=300)

            except Exception as e:
                current_app.logger.info(f'request: {str(e)}')
                return json.dumps({"error": str(e)}, indent=2)
            

            try:
                if r.status_code != 200:
                    current_app.logger.info(f'Error: {r.text}')
                    return json.dumps({"error": r.text}, indent=2)
            
            except Exception as e:

                current_app.logger.info(f'status_code !==200: {str(e)}')
                return json.dumps({"error": str(e)}, indent=2)
            
        
            try:
                response = r.json()
                hits = response['hits']['hits']
            
            except Exception as e:

                current_app.logger.info(f'hit response: {str(e)}')
                return json.dumps({"error": str(e)}, indent=2)

            if not hits:
                break
            
            results.extend([doc['_source'] for doc in hits])
            

            from_ += size
        

        return json.dumps(results, indent=2)
    

def main():

    return fetch_all_documents()

