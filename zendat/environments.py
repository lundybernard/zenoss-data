import os
import yaml


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(ROOT_DIR, '../environments.yaml')

with open(ENV_PATH) as env_file:
    ENV = yaml.load(env_file, Loader=yaml.BaseLoader)
