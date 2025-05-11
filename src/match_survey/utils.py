import re
import sys
import json
from pathlib import Path
from bs4 import BeautifulSoup

def check_path(filename: str, msg=str(), required=True) -> Path:
    try:
        assert Path(filename).exists(), msg
    except AssertionError as ae:
        print(ae)
        if required:
            sys.exit(ae)

def get_path(filename: str, msg=str(), required=True) -> Path:
    check_path(filename, msg, required)
    _path = Path(filename)

    return _path

def load_json(filename: str, msg: str, required: bool) -> dict:
    _path = get_path(filename, msg, required)

    return json.loads(_path.read_text())

def save_json(filename:str, msg:str, required:bool, data:dict):
    _path = get_path(filename, msg, required)
    Path(_path).write_text(json.dumps(data))

def get_all(element, etype, eterm):
    return element.find_all(etype, class_=re.compile(eterm))

def get(element, etype, eterm):
    return element.find(etype, class_=re.compile(eterm))