import json

data = {}
with open("config.cfg") as f:
    for x in f.readlines():
        datum = x.split("=")
        data[datum[0].strip()] = datum[1].strip()

def get(name,fallback=None):
    if name.upper() in data:
        return json.loads(data[name.upper()])
    return fallback