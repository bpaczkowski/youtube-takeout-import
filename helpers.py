import json
import re
from typing import Union, List


def parse_path(path: str) -> List[str]:
    path = re.sub(r'\[(\d+)\]', r'.\1', path)
    path = path.split('.')

    return path


def base_get(obj: Union[dict, list, object], prop: str, default: any = None) -> any:
    if isinstance(obj, dict):
        return obj.get(prop, default)

    if isinstance(obj, list):
        if not prop.isdigit():
            return default

        prop = int(prop)

        return obj[prop] if len(obj) > prop else default

    if isinstance(obj, object):
        return getattr(obj, prop, default)

    return default


def get(obj: Union[object, dict], path: Union[str, List[str]], default: any = None) -> any:
    if not obj:
        return None

    if not isinstance(path, list):
        path = parse_path(path)

    if len(path) == 0:
        return obj if obj else default

    for prop in path:
        obj = base_get(obj, prop, default)

        if not obj:
            break

    return obj


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
