#!/usr/bin/env python3

from flasktex import app
from flask import make_response, render_template

@app.route("/")
def ft_webpage_welcome():
    return 'Hello world!'

@app.route("/about")
def ft_webpage_about():
    resp = make_response;
    resp.headers['Content-Type'] = 'application/xhtml+xml'
    resp.data = render_template('common.html', title="关于", body="示例")
    return resp
