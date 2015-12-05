__version__ = "0.0.90"

from flask import Flask
app = Flask(__name__)

import flasktex.views
import flasktex.texrequest
import flasktex.api_1_0
import flasktex.bundle2tex, flasktex.tex2bundle

# Convenience imports
flasktex.TeXRequest = flasktex.texrequest.TeXRequest
