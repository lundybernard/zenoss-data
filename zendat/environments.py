import os
import yaml


def get_environment():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    ENV_PATH = os.path.join(ROOT_DIR, '../environments.yaml')

    with open(ENV_PATH) as env_file:
        ENV = yaml.load(env_file, Loader=yaml.BaseLoader)

    datadict = {}
    if 'DATA_DICT_KEY' in os.environ:
        datadict['api_key'] = os.environ['DATA_DICT_KEY']
    else:
        datadict['api_key'] = 'DEFAULT DATADICT KEY NOT PROVIDED'

    if 'DATA_DICT_URL' in os.environ:
        datadict['url'] = os.environ['DATA_DICT_URL']
    else:
        datadict['url'] = 'DEFAULT DATADICT URL NOT PROVIDED'

    ENV['default'] = {'datadict': datadict}
    return ENV
