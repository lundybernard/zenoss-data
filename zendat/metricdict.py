import requests
import json

from .conf import get_config


class MetricDictionaryClient(object):

    def __init__(self, conf=None, env=None):
        self.__conf = conf
        self.__env = env

    @property
    def _conf(self):
        if not self.__conf:
            self.__conf = get_config()
        if not self.__env:
            self.__env = self.__conf['default']

        return self.__conf[self.__env]['metric_dict']

    @property
    def _api_key(self):
        return self._conf['api_key']

    @property
    def _url(self):
        return self._conf['url']

    @property
    def _headers(self):
        return {'zenoss-api-key': self._api_key}

    def get_metrics(self) -> dict:
        metrics_url = f'{self._url}/metrics'

        r = requests.get(metrics_url, headers=self._headers)
        r.raise_for_status()

        return json.loads(r.text)

    def get_metric(self, name: str) -> dict:
        metric_url = f'{self._url}/metrics/{name}'

        r = requests.get(metric_url, headers=self._headers)
        r.raise_for_status()

        return json.loads(r.text)


def get_metrics(url=None, api_key=None) -> dict:

    if not (url and api_key):
        CONF = get_config()
        if not url:
            CONF = get_config()
            url = CONF[CONF['default']]['metric_dict']['url']
        if not api_key:
            api_key = CONF[CONF['default']]['metric_dict']['api_key']

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
            url = CONF[CONF['default']]['metric_dict']['url']
        if not api_key:
            api_key = CONF[CONF['default']]['metric_dict']['api_key']

    metrics_url = f'{url}/metrics/{name}'
    headers = {'zenoss-api-key': api_key}

    r = requests.get(metrics_url, headers=headers,)
    r.raise_for_status()

    return json.loads(r.text)
