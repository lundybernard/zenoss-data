from unittest import TestCase
from unittest.mock import Mock, patch

import json

from zendat.datadict import get_metrics, get_metric

PATH = 'zendat.datadict'


class DataDictTest(TestCase):

    def setUp(t):
        t.url = 'https://example.zenoss.com'
        t.api_key = 'somekey'
        t.data = {'json': 'data'}

        patches = ['requests']
        for target in patches:
            patcher = patch(f'{PATH}.{target}', autospec=True)
            setattr(t, target, patcher.start())
            t.addCleanup(patcher.stop)

        t.response = Mock(text=json.dumps(t.data))
        t.requests.get.return_value = t.response

    def test_get_metrics(t):
        ret = get_metrics(url=t.url, api_key=t.api_key)

        t.requests.get.assert_called_with(
            f'{t.url}/metrics', headers={'zenoss-api-key': t.api_key}
        )
        t.assertEqual(ret, t.data)

    @patch(f'{PATH}.get_config', autospec=True)
    def test_get_metrics_default_conf(t, get_config):
        '''uses default config if url and api_key are not given
        '''
        get_metrics()

        get_config.assert_called_with()

    def test_get_metric(t):
        name = 'metric_name'

        ret = get_metric(name=name, url=t.url, api_key=t.api_key)

        t.requests.get.assert_called_with(
            f'{t.url}/metrics/{name}', headers={'zenoss-api-key': t.api_key}
        )
        t.assertEqual(ret, t.data)
