from unittest import TestCase, skip

from zendat.tests.common_api_tests import CommonAPITest, DataDictTests

from zendat.conf import get_config

PT_SVC_ADDR = 'http://0.0.0.0:5000/'


class DataDictTest(TestCase, DataDictTests):
    '''Test cases for the remote zenoss data dictionary service
    These will execute queries against the default remote target
    '''
    def setUp(t):
        CONF = get_config()
        default = CONF['default']
        t.url = CONF[default]['datadict']['url']
        t.api_key = CONF[default]['datadict']['api_key']


@skip('local service is not configured yet')
class ServiceFunctionalTest(TestCase, CommonAPITest):
    '''Test cases for the local service API
    '''

    def setUp(t):
        t.service_address = PT_SVC_ADDR
