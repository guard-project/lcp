from colorama import Back, Fore, Style
from datetime import datetime
from requests.adapters import HTTPAdapter

import hashlib
import requests
import uuid


def exclude_keys_from_dict(dict_base, *keys):
    """
    Exclude the keys from the dictionary.

    :param dict_base: dictionary to check
    :keys: key to exclude from the dictionary
    :returns: dictionary without the keys
    """
    return {k: v for k, v in dict_base.items() if k not in keys}


def get_none(**vars):
    """
    Get the keys that are None value.

    :param vars: key/value arguments
    :returns: keys with value = None
    """
    res = []
    for text, var in vars.items():
        if var is None:
            res.append(text)
    return ', '.join(res)


def generate_username():
    """
    Generate a new password.

    :returns: new username
    """
    return str(uuid.uuid1())


def generate_password():
    """
    Generate a random password.

    :returns: random password
    """
    return hash(str(uuid.uuid1()))


def str_to_datetime(date_time_str, format='%Y/%m/%d %H:%M:%S'):
    """
    Get a datatime object from the string.

    :params date_time_str: datetime in string
    :params format: datetime format
    :returns datetime object
    """
    return datetime.strptime(date_time_str, format)


def datetime_to_str(date_time = None, format='%Y/%m/%d %H:%M:%S'):
    """
    Convert the datetime to string in the given format.

    :params data_time: datetime input
    :params format: datetime format
    :returns: datetime string in format %Y/%m/%d %H:%M:%S
    """
    if date_time is None:
        date_time = datetime.now()
    return date_time.strftime(format)


def hash(text):
    """
    Make a hash of the text

    :param text: text to make the hash
    :returns: hashed version of the text
    """
    return hashlib.sha224(text.encode('utf-8')).hexdigest()


def wrap(data):
    """
    Wrap the data if an array if it is ont a list of tuple.

    :param data: data to wrap
    :returns: wrapped data
    """
    return data if type(data) in [list, tuple] else [data]
