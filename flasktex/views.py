#!/usr/bin/env python3

from flasktex import app

@app.route("/")
def ft_welcome():
    return 'Hello world!'
