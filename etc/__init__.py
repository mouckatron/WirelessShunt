import json

def get_config(filename):
    with(open("{}/{}".format(__name__, filename), 'r') as f:
         settings = json.loads(f.read())
