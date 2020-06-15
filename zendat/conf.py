import os
import yaml


def get_config(config_file=None):
    if config_file:
        ENV_PATH = config_file
    elif usr_conf := os.environ.get('ZENDAT_CONFIG', default=None):
        ENV_PATH = usr_conf
    '''else:
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        ENV_PATH = os.path.join(ROOT_DIR, '../example_environments.yaml')
    '''

    with open(ENV_PATH) as env_file:
        ENV = yaml.load(env_file, Loader=yaml.BaseLoader)

    '''
    datadict = {}
    datadict['api_key'] = os.environ.get('DATA_DICT_KEY', default=None)
    datadict['url'] = os.environ.get('DATA_DICT_URL', default=None)

    ENV['default'] = {'datadict': datadict}
    '''
    return ENV


class Environments(object):

    def __init__(self):
        self.datadict = None


class Env(object):

    def __init__(self, url, api_key):
        self._url = url
        self._api_key = api_key

    @property
    def url(self):
        return self._url

    @property
    def api_key(self):
        return self._api_key
