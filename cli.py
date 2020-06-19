import argparse
import logging
from logging.config import dictConfig

from logconf import logging_config

from zendat.lib import hello_world


dictConfig(logging_config)
log = logging.getLogger('root')


class ZenDatCLI(object):

    def __init__(self):
        p = argparse.ArgumentParser(
            description='Utility for executing various zenoss data queries',
            usage='zendat [<args>] <command>'
        )
        p.set_defaults(func=p.print_help)

        p.add_argument(
            '-v', '--verbose',
            help='enable INFO output',
            action='store_const',
            dest='loglevel',
            const=logging.INFO
        )
        p.add_argument(
            '--debug',
            help='enable DEBUG output',
            action='store_const',
            dest='loglevel',
            const=logging.DEBUG,
        )

        # Add a subparser to handle sub-commands
        commands = p.add_subparsers(
            dest='command',
            title='commands',
            description='valid commands',
        )
        # hello args
        hello = commands.add_parser(
            'hello',
            description='execute command hello',
            help='for details use hello --help',
        )
        hello.set_defaults(func=self.hello)

        # start args
        start = commands.add_parser(
            'start',
            description='start the web server',
            help='for details use start --help',
        )
        start.set_defaults(func=self.start)
        start.add_argument(
            '-H', '--host', dest='host',
            default='0.0.0.0',
            help='host ip on which the service will be made available',
        )
        start.add_argument(
            '-P', '--port', dest='port',
            default='5000',
            help='port on which the service will be made available'
        )
        start.add_argument(
            '-d', '--debug', dest='debug',
            default=True,
            help='run web service with debug level output'
        )

        # test args
        test = commands.add_parser(
            'test',
            description='run functional tests',
            help='for details use test --help'
        )
        test.set_defaults(func=self.test)
        test.add_argument(
            '-H', '--host', dest='host',
            default='0.0.0.0',
            help='host ip on which the service is running',
        )
        test.add_argument(
            '-P', '--port', dest='port',
            default='5000',
            help='port on which the service is running'
        )

        # run_functional_tests args
        run_functional_tests = commands.add_parser(
            'run_functional_tests',
            description='start the server locally and run functional tests',
            help='for details use test --help'
        )
        run_functional_tests.set_defaults(func=self.run_functional_tests)
        run_functional_tests.add_argument(
            '-H', '--host', dest='host',
            default='0.0.0.0',
            help='host ip on which the service will be run',
        )
        run_functional_tests.add_argument(
            '-P', '--port', dest='port',
            default='5000',
            help='port on which the service service will be run'
        )

        # run_functional_tests args
        run_container_tests = commands.add_parser(
            'run_container_tests',
            description='start docker-compose and run functional tests',
            help='for details use test --help'
        )
        run_container_tests.set_defaults(func=self.run_container_tests)
        run_container_tests.add_argument(
            '-H', '--host', dest='host',
            default='0.0.0.0',
            help='host ip on which the service will be run',
        )
        run_container_tests.add_argument(
            '-P', '--port', dest='port',
            default='5000',
            help='port on which the service service will be run'
        )

        # Data Dictionary commands
        metricdict = commands.add_parser(
            'metricdict',
            description='execute data dictionary queries',
            help='for details use metricdict --help'
        )
        metricdict.set_defaults(func=metricdict.print_help)
        metricdict.add_argument(
            '-c', '--conf', '--config_file',
            dest='config_file',
            default=None,
            help='specify a config file to get environment details from',
        )
        queries = metricdict.add_subparsers(
            dest='querys',
            title='querys',
            description='available data dictionary queries',
        )
        get_metrics = queries.add_parser(
            'get_metrics',
            description='get all metrics',
            help='for details use get_metrics --help'
        )
        get_metrics.set_defaults(func=self.get_metrics)
        get_metric = queries.add_parser(
            'get_metric',
            description='get a metric by name',
            help='for details use get_metric --help'
        )
        get_metric.set_defaults(func=self.get_metric)
        get_metric.add_argument(
            'name', help='metric name to retrieve',
        )

        # Execute
        # get only the first command in args
        args = p.parse_args()
        self.set_log_level(args)
        # execute function set for parsed command
        if not hasattr(self, args.func.__name__):
            p.print_help()
            exit(1)
        args.func(args)
        exit(0)

    def set_log_level(self, args):
        if args.loglevel:
            log.setLevel(args.loglevel)
        else:
            log.setLevel(logging.ERROR)

    def start(self, args):
        from zendat.server import start_server
        start_server(host=args.host, port=args.port, debug=args.debug)

    def test(self, args):
        print('++ run functional tests ++')
        import unittest
        loader = unittest.TestLoader()
        suite = loader.discover('functional_tests', pattern='*_test.py')
        runner = unittest.TextTestRunner()
        runner.run(suite)

    def run_functional_tests(self, args):
        import subprocess
        import os
        import signal
        from time import sleep
        a = subprocess.Popen(['zendat', 'start'])
        sleep(0.5)
        self.test(args)

        os.kill(a.pid, signal.SIGTERM)

    def run_container_tests(self, args):
        import subprocess
        import os
        import signal
        from time import sleep
        a = subprocess.Popen(['docker-compose', 'up'])
        sleep(0.5)
        self.test(args)

        os.kill(a.pid, signal.SIGTERM)
        sleep(0.5)

    def hello(self, args):
        print(hello_world())

    # TODO:
    ''' Add config_file option
    Create a MetricDictionaryClient class to hold config options
    And to collect the metric dictionary querys in
    Add environment argument, to target a specific instance
    '''
    def get_metrics(self, args):
        print('execute data dictionary get_metrics query')
        from zendat.metricdict import get_metrics
        print(get_metrics())

    def get_metric(self, args):
        print(f'get data dictionary definition for metric: {args.name}')
        # TEST: example AnalyticsApiCount
        from zendat.metricdict import get_metric
        print(get_metric(args.name))
