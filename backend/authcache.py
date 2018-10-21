import os
import json

def save_auth(token):
    with open('./tokencache.json', 'w') as fp:
        json.dump({
            'token': token
        }, fp)

def load_auth():
    if not os.path.exists('./tokencache.json'):
        raise Exception('token cache file not found')

    with open('./tokencache.json', 'r') as fp:
        return json.load(fp)['token']
