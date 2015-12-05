__version__ = "0.0.1"

from flask import Flask
app = Flask(__name__)

import flasktex.views
