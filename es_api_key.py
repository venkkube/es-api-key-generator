import os
import time
import logging
import config
import json

from datetime import datetime
import time
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from pathlib import Path

def apply_dotenv():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

def es_client():
    username = os.getenv("ES_USER")
    password = os.getenv("ES_PASSWORD")
    cloud_id = os.getenv('ES_CLOUD_ID')

    es = Elasticsearch(
        cloud_id=cloud_id,
        http_auth=(username, password),
    )

    return es

def get_api_keys_to_renew():   
    resp = es_client().security.get_api_key(username="elastic")
    keys_to_renew =[]

    for api_key in resp['api_keys']: 
        curr = int(time.time() * 1000)
        expiration = api_key['expiration'] - curr
        hours_left=(expiration/(1000*60*60))
        if hours_left < 24 and api_key['invalidated'] == False:
            keys_to_renew.append(api_key['name'])

    return keys_to_renew

def generate_api_keys(apis):
    for key in apis.keys():
        api_key = {}
        api_key['expiration'] = apis[key]['expiration_in_days']
        api_key['name'] = key+"_KEY"
        role_idx=0
        roles = {}
        index = []
        role = {}
        for r in apis[key]['roles']:
            idx = {}
            idx['names'] = r['index']
            idx['privileges'] = r['privileges']
            index.append(idx)
            role['index'] = index
            role['cluster'] = ['all']
            roles["role-"+str(role_idx)] = role
            role_idx=role_idx+1

        api_key["role_descriptors"] = roles

        es_client().security.create_api_key(
        # body={
        #     "name": key,
        #     "expiration": apis[key],   
        #     "role_descriptors": { 
        #         "role-a": {
        #         "cluster": ["all"],
        #         "index": [
        #             {
        #             "names": ["asset-dev"],
        #             "privileges": ["read"]
        #             }
        #         ]
        #         }
        #     }
        # }
        body={json.dumps(api_key)}
        )

        # print(json.dumps(api_key))

     
if __name__ == "__main__":
    apply_dotenv()
    start_time = time.time()
    generate_api_keys(config.api_keys_config)
    # print(get_api_keys_to_renew())
    logging.info(f"Execution time: { time.time() - start_time } secs")