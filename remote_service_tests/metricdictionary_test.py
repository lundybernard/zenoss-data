'''This Test Suite targets the remote Metric Dictionary API
It executes queries against the targeted remote server
and verifies the response.
It may be used to verify the validity of this application's api calls
And as a diagnostic tool for the remote service.
'''

from unittest import TestCase

from zendat.datadict import MetricDictionaryClient


class MetricDictionaryClientFunctionalTests(TestCase):

    def assertIsNumeric(t, str):
        try:
            float(str)
        except Exception:
            t.fail(f'"{str}" is not a numeric value')

    def test_get_metrics(t):
        mdc = MetricDictionaryClient()
        data = mdc.get_metrics()

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

    def test_get_metric(t):
        mdc = MetricDictionaryClient()
        data = mdc.get_metrics()
        ex = data['metrics'].pop()

        ret = mdc.get_metric(ex['name'])
        t.assertEqual(ret, ex)
