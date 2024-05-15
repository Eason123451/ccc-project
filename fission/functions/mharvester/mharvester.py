from flask import current_app
import logging, requests
from mastodon import Mastodon
import json, time
from datetime import datetime
from elasticsearch8 import Elasticsearch
from bs4 import BeautifulSoup
import pytz

def main():
    m = Mastodon(
        api_base_url=f'https://mastodon.au'
    )

    # Get the ID of the lastid status main the public timeline
    lastid= m.timeline(timeline='public', since_id=None, limit=1, remote=True)[0]['id']

    # Sleep for 30 seconds to allow for some status to be posted before we fetch them
    time.sleep(30)
    data_set = m.timeline(timeline='public', since_id=lastid, remote=True)
    current_app.logger.info(f'Harvested mastodon toots for specifc period')

    # set local zone
    local_zone = pytz.timezone('Australia/Sydney')

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

    
    for data in data_set:
        try:
            # change the UTC time to Local time
            converted_time = data['created_at'].astimezone(local_zone).isoformat()
            data['created_at'] = converted_time
        
            # extract the text from html for each toot content
            content = data['content']
            soup = BeautifulSoup(content, 'lxml')
            data['content'] = soup.get_text()

            data_format = {
                "id": data['id'],
                "created_at": data['created_at'],
                "content": data['content'],
                "account": {
                    "display_name": data['account']['display_name']
                }
            }
            
            # insert data to the elastic search
            client.index(index='mastodon', id=data['id'], body=data_format)
            current_app.logger.info('Indexed data into Elasticsearch')

        except Exception as e:
            return json.dumps({"insert data error": str(e)})

    return 'OK'
