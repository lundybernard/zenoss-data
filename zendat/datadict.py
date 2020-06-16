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
    headers = {'zenoss-api-key': api_key}

    r = requests.get(metrics_url, headers=headers,)
    r.raise_for_status()

    return json.loads(r.text)


def get_metric(name: str, url=None, api_key=None) -> dict:

    if not (url and api_key):
        CONF = get_config()
        if not url:
            CONF = get_config()
            url = CONF[CONF['default']]['datadict']['url']
        if not api_key:
            api_key = CONF[CONF['default']]['datadict']['api_key']

    metrics_url = f'{url}/metrics/{name}'
    headers = {'zenoss-api-key': api_key}

    r = requests.get(metrics_url, headers=headers,)
    r.raise_for_status()

    return json.loads(r.text)
