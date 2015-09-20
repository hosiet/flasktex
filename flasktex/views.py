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
    resp.headers['Content-Type'] = 'application/xhtml+xml'
    resp.data = render_template('common.xhtml', title="关于", body="这是一个在线渲染 LaTeX 文档的尝试")
    return resp
