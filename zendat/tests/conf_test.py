from unittest import TestCase

from ..conf import get_config


class TestConfiguration(TestCase):

    def test_get_config_loads_given_config_file(t):
        CONF = get_config('./example_conf.yaml')
        example_env = CONF['example']

        t.assertEqual(
            example_env['datadict']['api_key'],
            'example_dictionary_api_key'
        )
        t.assertEqual(
            example_env['datadict']['url'],
            'https://api-example.zenoss.io/v1/dictionary'
        )

    def test_config_default_environment(t):
        CONF = get_config('./example_conf.yaml')

        t.assertEqual(CONF['default'], 'example')

        default_env = CONF[CONF['default']]

        t.assertEqual(
            default_env['datadict']['api_key'],
            CONF['example']['datadict']['api_key']
        )
        t.assertEqual(
            default_env['datadict']['url'],
            CONF['example']['datadict']['url']
        )
