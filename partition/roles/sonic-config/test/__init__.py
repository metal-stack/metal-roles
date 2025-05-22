import os

def read_template_file(name):
    with open(os.path.join(os.path.dirname(__file__), "..", "templates", name)) as f:
        return f.read()
