from flask import Flask

from zendat.lib import hello_world
from zendat.metricdict import MetricDictionaryClient

app = Flask(__name__)
mdc = MetricDictionaryClient()



@app.route('/')
def hello_api():
    return hello_world()


@app.route('/get_metrics')
def get_metrics_api():
    return(mdc.get_metrics())


@app.route('/get_metric/<name>')
def get_metric_api(name):
    return(mdc.get_metric(name))


def start_server(host='0.0.0.0', port='5000', debug=True):
    app.run(host=host, port=port, debug=debug)
