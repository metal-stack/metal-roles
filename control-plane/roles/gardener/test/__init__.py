import os

FILTER_PLUGINS_PATH = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), 'filter_plugins')


def read_mock_file(name):
    with open(os.path.join(os.path.dirname(__file__), "mock", name), 'r') as f:
        return f.read()
