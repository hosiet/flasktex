#!/usr/bin/env python3

from flasktex import app
from flask import make_response, render_template
import os

@app.route("/")
def ft_webpage_welcome():
    return 'PWD:{}.'.format(os.getcwd())

@app.route("/about")
def ft_webpage_about():
    resp = make_response();
    resp.headers['Content-Type'] = 'text/plain'
    resp.data = render_template('common.xhtml', title="关于", body="示例")
    return resp
