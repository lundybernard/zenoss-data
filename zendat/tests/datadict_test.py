from unittest import TestCase

from zendat.datadict import get_metrics


class DataDictTest(TestCase):

    def test_get_metrics(t):

        ret = get_metrics()
        t.assertTrue(ret)
