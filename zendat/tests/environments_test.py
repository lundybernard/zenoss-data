from unittest import TestCase

from ..environments import get_environment
import os


class TestEnvironments(TestCase):

    def test_ENV_loads_environments_yaml(t):
        ENV = get_environment()
        example_env = ENV['example']

        t.assertEqual(
            example_env['dictionary']['api_key'],
            'example_dictionary_api_key'
        )
        t.assertEqual(
            example_env['dictionary']['url'],
            'https://api-example.zenoss.io/v1/dictionary'
        )

    def test_ENV_loads_defaults_from_environment(t):
        os.environ['DATA_DICT_KEY'] = 'api key'
        os.environ['DATA_DICT_URL'] = 'zenoss api url'

        ENV = get_environment()
        default_env = ENV['default']

        t.assertEqual(
            default_env['dictionary']['api_key'],
            os.environ['DATA_DICT_KEY']
        )
        t.assertEqual(
            default_env['dictionary']['url'],
            os.environ['DATA_DICT_URL']
        )
