import json
from core.base import ConfigType

def load_config(path: str) -> ConfigType:
    with open(f"/app/{path}", "r") as config:
        data: ConfigType = json.load(config)
    return data