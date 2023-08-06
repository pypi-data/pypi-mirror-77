import json
import datetime

from .web_exc import WebException


def to_map(it, key):
    rs = {}
    for item in it:
        rs[item[key]] = item
    return rs


def read_json_wx(file_name, obj=None):
    try:

        with open(file_name, encoding='utf-8') as f:
            return json.load(f)

    except FileNotFoundError as ex:
        if obj is not None:
            return obj
        else:
            raise WebException(ex) from ex

    except Exception as ex:
        raise WebException(ex) from ex


def write_json_wx(json_data, file_name):
    try:
        with open(file_name, 'w', encoding='utf-8') as outfile:
            json.dump(json_data, outfile, indent=4)
    except Exception as ex:
        raise WebException(ex) from ex


def search(it, fn):
    for item in it:
        if fn(item):
            return item
    return None

# !ValueError
def deserialize_tstamp(s: str) -> datetime.datetime:
    assert isinstance(s, str), s

    return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ')    # %f is microsec, xxxxxx
