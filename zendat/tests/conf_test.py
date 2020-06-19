from unittest import TestCase

from ..conf import get_config


class TestConfiguration(TestCase):

    def test_get_config_loads_given_config_file(t):
        CONF = get_config('./example_conf.yaml')
        example_env = CONF['example']

        t.assertEqual(
            example_env['metric_dict']['api_key'],
            'example_dictionary_api_key'
        )
        t.assertEqual(
            example_env['metric_dict']['url'],
            'https://api-example.zenoss.io/v1/dictionary'
        )

    def test_config_default_environment(t):
        CONF = get_config('./example_conf.yaml')

        t.assertEqual(CONF['default'], 'example')

        default_env = CONF[CONF['default']]

        t.assertEqual(
            default_env['metric_dict']['api_key'],
            CONF['example']['metric_dict']['api_key']
        )
        t.assertEqual(
            default_env['metric_dict']['url'],
            CONF['example']['metric_dict']['url']
        )
