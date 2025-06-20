import json
from typing import Any

data = {}
with open("config.cfg") as f:
    for x in f.readlines():
        if x.strip() == "" or x.strip().startswith("#"):
            continue
        datum = x.split("=")
        data[datum[0].strip()] = datum[1].strip()

def get(name,fallback=...) -> Any:
    if name.upper() in data:
        return json.loads(data[name.upper()])
    
    if fallback == ...:
        raise KeyError(f"Config item {name} cannot be found.")
    return fallback