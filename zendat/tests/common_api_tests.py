import requests
import json


class CommonAPITest(object):
    '''Define the API tests in their own inheritable class
    so they may be reused in multiple test cases.
    This was done to allow testing of the api in a container
    and as local service.
    '''

    def test_compose_webservice_exists(t):
        ret = requests.get(t.service_address)
        ret.raise_for_status()
        t.assertEqual(ret.text, 'Hello World!')

    def test_get_metrics(t):
        ret = requests.get(f'{t.service_address}/get_metrics')
        ret.raise_for_status()
        data = json.loads(ret.text)

        # Metrics contains these Keys
        t.assertIn('metrics', data)
        t.assertIn('totalCount', data)

    def test_get_metric_by_name(t):
        ret = requests.get(f'{t.service_address}/get_metrics')
        ret.raise_for_status()
        data = json.loads(ret.text)
        ex = data['metrics'].pop()

        ret = requests.get(f'{t.service_address}/get_metric/{ex["name"]}')
        data = json.loads(ret.text)

        t.assertEqual(data, ex)
