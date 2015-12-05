__version__ = "0.0.90"

# WORKAROUND FOR STRANGE __name__
__name__ = 'flasktex_app'

from flask import Flask
app = Flask(__name__)

import flasktex.views
import flasktex.texrequest
import flasktex.api_1_0
import flasktex.bundle2tex, flasktex.tex2bundle
import flasktex.db

# Convenience imports
flasktex.TeXRequest = flasktex.texrequest.TeXRequest
