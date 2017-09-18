import json
from typing import Union


def get(obj: dict, path: str):
    path = path.split('.')
    value = obj

    for prop in path:
        try:
            value = value[prop]
        except:
            return None

    return value


def safe_json_parse(string: str):
    try:
        return json.loads(string)
    except json.JSONDecodeError:
        return None


def has(obj: Union[object, dict], path: str):
    path = path.split('.')
    value = obj

    if isinstance(obj, dict):
        for prop in path:
            try:
                value = value[prop]
            except:
                return False
    elif isinstance(obj, object):
        for prop in path:
            value = getattr(value, prop, None)

            if not value:
                return False
    else:
        return False

    return True
