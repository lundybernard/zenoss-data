from unittest import TestCase

from ..environments import ENV


class TestENV(TestCase):

    def test_ENV_loads_environments_yaml(t):
        example_env = ENV['example']

        t.assertEqual(
            example_env['dictionary']['api_key'],
            'example_dictionary_api_key'
        )
        t.assertEqual(
            example_env['dictionary']['url'],
            'https://api-example.zenoss.io/v1/dictionary'
        )
