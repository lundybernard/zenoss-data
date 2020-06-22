from unittest import TestCase

from zendat.tests.common_api_tests import CommonAPITest


PT_SVC_ADDR = 'http://0.0.0.0:5000/'


class ServiceFunctionalTest(TestCase, CommonAPITest):
    '''Test cases for the local service API
    '''

    def setUp(t):
        t.service_address = PT_SVC_ADDR
