import requests

from zendat.datadict import get_metrics


class DataDictTests(object):

    def assertIsNumeric(t, str):
        try:
            float(str)
        except Exception:
            t.fail(f'"{str}" is not a numeric value')

    def test_get_metrics(t):
        data = get_metrics(t.url, t.api_key)

        # Metrics contains these Keys
        t.assertIn('metrics', data)
        t.assertIn('totalCount', data)

        for metric in data['metrics']:
            t.assertIn('name', metric)

            # optional parameters
            optional_str_fields = [
                'layer', 'label', 'description', 'units', 'scaleFactorString',
            ]
            for opt in optional_str_fields:
                if opt in metric:
                    t.assertIsInstance(metric[opt], str)

            optional_num_fields = ['minimum', 'maximum', 'scaleFactor']
            for opt in optional_num_fields:
                if opt in metric:
                    t.assertIsNumeric(metric[opt])

            if 'tags' in metric:
                # contains a list of strings
                t.assertIsInstance(metric['tags'], list)
                for item in metric['tags']:
                    t.assertIsInstance(item, str)

        t.assertEqual(
            data['totalCount'],
            str(len(data['metrics'])),
        )


class CommonAPITest(object):
    '''Define the API tests in their own inheritable class
    so they may be reused in multiple test cases.
    This was done to allow testing of the api in a container
    and as local service.
    '''

    def test_compose_webservice_exists(self):
        out = requests.get(self.service_address)
        self.assertEqual(out.text, 'Hello World!')
