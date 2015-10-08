#!/usr/bin/env python3
#
# config.py -- configuration reader for flasktex package
#
# This file is part of flasktex.
#
# Copyright (c) 2015, Boyuan Yang <073plan@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Get Config From config.ini.
"""
import configparser
_BUILTIN_CONFIG_PATH_LIST = ['/home/hosiet/src-nosync/github/flasktex/flasktex/',
        '/var/www/html/flasktex/flasktex/']
try:
    a = CONFIG_PATH
    _BUILTIN_CONFIG_PATH_LIST.append(CONFIG_PATH)
except NameError:
    pass

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
    _config_loaded = False
    for CONFIG_PATH in _BUILTIN_CONFIG_PATH_LIST:
        try:
            config.read(CONFIG_PATH+'config.ini')
            _config_loaded = True
            break
        except Exception as e:
            continue
    if not _config_loaded:
        raise Exception('ERR_NO_VALID_CONFIG_FILE')
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
