from unittest import TestCase

from zendat.lib import hello_world


class ZenDatTests(TestCase):

    def test_zendat(t):
        ret = hello_world()
        t.assertEqual(ret, 'Hello World!')
