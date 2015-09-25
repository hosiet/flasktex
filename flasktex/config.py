#!/usr/bin/env python3
"""
Get Config From config.ini.

"""
import configparser
try:
    a = CONFIG_PATH
except NameError:
    CONFIG_PATH = '/home/hosiet/src-nosync/github/flasktex/flasktex/'

def ft_getconfig(keystr):
    """
    get the value of key from config.ini.

    Will always return str (or none).
    """
    _builtin_config = {\
            "DATABASETYPE": "SQLITE3",\
            "AUTHTYPE": "ALL",\
            "WORKERTIMEOUT": "60",\
            "DEFAULTRENDERER": "xelatex"\
            }

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH+'config.ini')
    assert 'GENERAL' in config
    assert 'RENDER' in config
    # Find keystr in all sections
    for section in config.sections():
        for key in config[str(section)]:
            if str(key).upper() == str(keystr).upper():
                return config[str(section)][str(key)]

    # If not found, set given internal defaults
    mystr = str(keystr).upper()
    if mystr in _builtin_config.keys():
        return _builtin_config[mystr]

    # If really not found, return None
    return None

#  vim: set ts=8 sw=4 tw=0 et :
