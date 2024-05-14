from flask import current_app
import logging, requests
from mastodon import Mastodon
import json, time
from datetime import datetime
from bs4 import BeautifulSoup
import pytz

def main():
    m = Mastodon(
        api_base_url=f'https://mastodon.au'
    )

    # Get the ID of the lastid status main the public timeline
    lastid= m.timeline(timeline='public', since_id=None, limit=1, remote=True)[0]['id']

    # Sleep for 30 seconds to allow for some status to be posted before we fetch them
    time.sleep(20)
    data_set = m.timeline(timeline='public', since_id=lastid, remote=True)
    current_app.logger.info(f'Harvested mastodon toots for specifc period')

    # set local zone
    local_zone = pytz.timezone('Australia/Sydney')

    
    for data in data_set:

        # try:
        #     # change the UTC time to Local time
        #     converted_time = data['created_at'].astimezone(local_zone).isoformat()
        #     data['created_at'] = converted_time
        #     current_app.logger.info(f'change the time to local time')
        # except Exception as e:
        #     return json.dumps({"error": str(e)})
        
        try:
            # extract the text from html for each publish
            content = data['content']
            soup = BeautifulSoup(content, 'lxml')
            data['content'] = soup.get_text()
            current_app.logger.info(f'change HTML to text')
        except Exception as e:
            return json.dumps({"error": str(e)})

    # Fetch the statuses from the public timeline since the lastid
    try:
        requests.post(url='http://router.fission/enqueue/mastodon',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data_set)
        )
        current_app.logger.info(f'Send to message queue')
    except Exception as e:
        return json.dumps({"error": str(e)})

    return 'OK'
