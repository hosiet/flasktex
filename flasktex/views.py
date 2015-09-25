#!/usr/bin/env python3
#
# views.py -- view router for flasktex
#
# This file is part of flasktex.
#
# Copyright (c) 2015, Boyuan Yang <073plan@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


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
