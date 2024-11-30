import json

data = {}
with open("config.cfg") as f:
    for x in f.readlines():
        datum = x.split("=")
        data[datum[0]] = datum[1]


def get(name,fallback=None):
    if name in data:
        return data[name]
    return fallback