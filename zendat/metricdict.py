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
