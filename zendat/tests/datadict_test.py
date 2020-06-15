from unittest import TestCase
from unittest.mock import Mock, patch

import json

from zendat.datadict import get_metrics


class DataDictTest(TestCase):

    @patch('zendat.datadict.requests')
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
