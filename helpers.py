import json
import re
from typing import Union, List


def parse_path(path: str) -> List[str]:
    path = re.sub(r'\[(\d+)\]', r'.\1', path)
    path = path.split('.')

    return path


def get(obj: Union[object, dict], path: Union[str, List[str]], default: any = None) -> any:
    if not isinstance(path, list):
        path = parse_path(path)

    if len(path) == 0:
        return obj if obj else default

    prop = path.pop(0)

    if isinstance(obj, dict):
        obj = obj.get(prop, default)
    elif isinstance(obj, list):
        if not prop.isdigit():
            obj = default

        prop = int(prop)

        obj = obj[prop] if len(obj) > prop else default
    elif isinstance(obj, object):
        obj = getattr(obj, prop, None)
    else:
        obj = default

    if obj and len(path) > 0:
        return get(obj, path, default)

    return obj if obj else default


def has(obj: Union[object, dict], path: Union[str, List[str]]) -> bool:
    return not not get(obj, path)


def safe_json_parse(string: str):
    try:
        return json.loads(string)
    except json.JSONDecodeError:
        return None


def read_file(filename: str) -> Union[str, None]:
    try:
        with open(filename, 'r') as fp:
            return fp.read()
    except OSError:
        return None


def read_json_file(filename: str) -> Union[dict, None]:
    try:
        with open(filename, 'r') as fp:
            return json.load(fp)
    except (OSError, json.JSONDecodeError):
        return None


def write_json_file(filename: str, data, indent = 4) -> bool:
    try:
        with open(filename, 'w') as fp:
            json.dump(data, fp, skipkeys = True, indent = indent)
        return True
    except (OSError, TypeError):
        return False
