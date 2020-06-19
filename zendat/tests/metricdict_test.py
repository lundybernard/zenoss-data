from unittest import TestCase
from unittest.mock import Mock, patch

import json

from zendat.metricdict import MetricDictionaryClient, get_metrics, get_metric

PATH = 'zendat.metricdict'


class MetricDictionaryClientTest(TestCase):

    def setUp(t):
        t.default_api_key = 'example_dictionary_api_key'
        t.default_url = 'https://api-example.zenoss.io/v1/dictionary'
        t.my_api_key = 'my_api_key'
        t.my_url = 'https://my.zenoss.io/v1/dictionary'

        t.config = {
            'default': 'default_env',
            'default_env': {
                'metric_dict': {
                    'api_key': t.default_api_key,
                    'url': t.default_url,
                },
            },
            'my_env': {
                'metric_dict': {
                    'api_key': t.my_api_key,
                    'url': t.my_url,
                },
            },
        }

        patches = ['requests']
        for target in patches:
            patcher = patch(f'{PATH}.{target}', autospec=True)
            setattr(t, target, patcher.start())
            t.addCleanup(patcher.stop)

        t.data = {'json': 'data'}
        t.response = Mock(text=json.dumps(t.data))
        t.requests.get.return_value = t.response

    @patch(f'{PATH}.get_config', autospec=True)
    def test___init__(t, get_config):
        '''Given no configuration, lookup the default using get_config()
        '''
        mdc = MetricDictionaryClient()
        t.assertEqual(
            mdc._conf, get_config.return_value['default_env']['metric_dict']
        )

    def test_conf_default(t):
        '''loads the default config if no environment is specified
        '''
        mdc = MetricDictionaryClient(conf=t.config)
        t.assertEqual(mdc._conf, t.config['default_env']['metric_dict'])
        t.assertEqual(mdc._api_key, t.default_api_key)
        t.assertEqual(mdc._url, t.default_url)

    def test_conf_environment(t):
        '''loads the specified environment config
        '''
        mdc = MetricDictionaryClient(conf=t.config, env='my_env')
        t.assertEqual(mdc._conf, t.config['my_env']['metric_dict'])
        t.assertEqual(mdc._api_key, t.my_api_key)
        t.assertEqual(mdc._url, t.my_url)

    def test__api_key(t):
        mdc = MetricDictionaryClient(conf=t.config)
        t.assertEqual(mdc._api_key, t.default_api_key)

    def test__url(t):
        mdc = MetricDictionaryClient(conf=t.config)
        t.assertEqual(mdc._url, t.default_url)

    def test__headers(t):
        mdc = MetricDictionaryClient(conf=t.config)
        t.assertEqual(mdc._headers, {'zenoss-api-key': t.default_api_key})

    def test_get_metrics(t):
        mdc = MetricDictionaryClient(conf=t.config)

        ret = mdc.get_metrics()

        t.requests.get.assert_called_with(
            f'{t.default_url}/metrics', headers=mdc._headers
        )
        t.assertEqual(ret, t.data)

    def test_get_metric(t):
        name = 'metric_name'
        mdc = MetricDictionaryClient(conf=t.config)

        ret = mdc.get_metric(name)

        t.requests.get.assert_called_with(
            f'{t.default_url}/metrics/{name}', headers=mdc._headers
        )
        t.assertEqual(ret, t.data)


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
