#!/usr/bin/python3

from flask import Flask
app = Flask(__name__)

import flasktex.views
from flasktex.config import ft_getconfig
import flasktex.texworker

#  vim: set ts=8 sw=4 tw=0 et :
