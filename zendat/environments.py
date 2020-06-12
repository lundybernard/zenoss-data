import os
import yaml


def get_environment():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    ENV_PATH = os.path.join(ROOT_DIR, '../environments.yaml')

    with open(ENV_PATH) as env_file:
        ENV = yaml.load(env_file, Loader=yaml.BaseLoader)

    ENV['default'] = {'datadict': {'api_key': os.environ['DATA_DICT_KEY']}}
    ENV['default']['datadict']['url'] = os.environ['DATA_DICT_URL']

    return ENV
