#!/usr/bin/env python3

from . import app

@app.route("/")
def ft_welcome():
    return 'Hello world!'
