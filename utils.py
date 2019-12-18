import json

def _write_json(filename, content):
    with open(filename, 'w') as outfile:
        json.dump(content, outfile)


def _read_json(filename):
    with  open(filename, 'r') as f:
        return json.load(f)