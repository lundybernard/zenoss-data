import requests
import json

from .conf import get_config


def get_metrics(url=None, api_key=None) -> dict:

    if not (url and api_key):
        CONF = get_config()
        if not url:
            CONF = get_config()
            url = CONF[CONF['default']]['datadict']['url']
        if not api_key:
            api_key = CONF[CONF['default']]['datadict']['api_key']

    metrics_url = f'{url}/metrics'
    print(f'get metrics from {url}')
    headers = {'zenoss-api-key': api_key}

    r = requests.get(metrics_url, headers=headers,)

    return json.loads(r.text)
