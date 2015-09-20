#!/usr/bin/python3

from flask import Flask
app = Flask(__name__)

import flasktex.views
from flasktex.config import getconfig

#  vim: set ts=8 sw=4 tw=0 et :
