from elasticsearch import Elasticsearch
import pandas as pd
from elasticsearch.helpers import bulk

es = Elasticsearch(
    ['https://localhost:9200'],
    verify_certs=False,
    ssl_show_warn=False,
    basic_auth=('elastic', 'epheli0AJ4eir9xaiM2muqu6eehee4oh'),
    request_timeout=180,  
    max_retries=20,
    retry_on_timeout=True
)



df = pd.read_csv("/home/yeshengyao/split_output_part3.csv")
df.fillna("", inplace=True)
records = df.to_dict(orient='records')

def gen_data():
    for record in records:
        yield {
            "_index": "twitter",
            "_source": record,
        }
bulk(es, gen_data(), chunk_size=1000)  


