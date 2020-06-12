import requests
import json

from .environments import get_environment

ENV = get_environment()
default_url = ENV['default']['datadict']['url']
default_key = ENV['default']['datadict']['api_key']


def get_metrics(url=default_url, api_key=default_key):

    metrics_url = f'{url}/metrics'
    headers = {'zenoss-api-key': api_key}

    r = requests.get(metrics_url, headers=headers,)

    return json.loads(r.text)
