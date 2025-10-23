import json
import os
from typing import TypedDict
from pathlib import Path

class ConfigType(TypedDict):
    db_name: str
    db_host: str
    db_port: str
    db_username: str
    db_password: str
    db_type: str
    output_path: str

def load_config(path: str) -> ConfigType:
    with open(f"/app/{path}", "r") as config:
        data: ConfigType = json.load(config)
    return data