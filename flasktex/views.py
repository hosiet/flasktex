#!/usr/bin/env python3

from flasktex import app
from flasktex.config import ft_getconfig
from flask import make_response, render_template
import os
import sqlite3

@app.route("/")
def ft_webpage_welcome():
    return 'PWD:{}.'.format(os.getcwd())

@app.route("/about")
def ft_webpage_about():
    resp = make_response();
    resp.headers['Content-Type'] = 'application/xhtml+xml'
    resp.data = render_template('common.xhtml', title="关于", body="这是一个在线渲染 LaTeX 文档的尝试")
    return resp

@app.route("/api/submit")
def ft_api_submit():
    return "Hello"

@app.route("/api/status")
def ft_api_status():
    # First, read the database and obtain all the info
    conn = sqlite3.connect(ft_getconfig('DATABASEPATH')+ft_getconfig('DATABASENAME'))
    c = conn.cursor()
    c.execute('SELECT id, userid, starttime, stoptime, status FROM `work`;')
    result = c.fetchall()
    conn.close()

    # Second, make a response
    resp = make_response();
    resp.headers['Content-Type'] = 'text/xml'
    resp.data = render_template('status.xml', result=result)
    return resp

@app.route("/api/obtain/<int:work_id>")
def ft_api_obtain(work_id):
    return "hello obtain"
