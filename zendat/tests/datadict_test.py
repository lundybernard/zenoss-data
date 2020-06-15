from unittest import TestCase
from unittest.mock import Mock, patch

import json

from zendat.datadict import get_metrics

PATH = 'zendat.datadict'


class DataDictTest(TestCase):

    @patch(f'{PATH}.requests', autospec=True)
    def test_get_metrics(t, requests):
        url = 'https://example.zenoss.com'
        api_key = 'somekey'
        data = {'json': 'data'}
        response = Mock(text=json.dumps(data))
        requests.get.return_value = response

        ret = get_metrics(url=url, api_key=api_key)

        requests.get.assert_called_with(
            f'{url}/metrics', headers={'zenoss-api-key': api_key}
        )
        t.assertEqual(ret, data)

    @patch(f'{PATH}.get_config', autospec=True)
    @patch(f'{PATH}.requests', autospec=True)
    def test_get_metrics_default_conf(t, requests, get_config):
        '''uses default config if url and api_key are not given
        '''
        data = {'json': 'data'}
        response = Mock(text=json.dumps(data))
        requests.get.return_value = response

        get_metrics()

        get_config.assert_called_with()
