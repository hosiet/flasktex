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
from flasktex.db import ft_db_connect_sqlite
import flasktex.texworker
from flask import make_response, render_template, abort, request
import os
import sqlite3


@app.route("/")
def ft_webpage_welcome():
    return 'PWD:{}.'.format(os.getcwd())

@app.route("/about")
def ft_webpage_about():
    resp = make_response(
            render_template(
                'common.xhtml',
                title="关于",
                body="这是一个在线渲染 LaTeX 文档的尝试")
            )
    resp.headers['Content-Type'] = 'application/xhtml+xml'
    return resp

@app.route("/api/submit", methods=['POST'])
def ft_api_submit():
    """
    Used for XHR to POST desired flasktex job.

    QUERY_STRING example as follows:

    * renderer=xelatex
    * timeout=60
    """
    # TODO AUTH
    # Then, obtain data and start the job
    try:
        data = request.get_data().decode('UTF-8')
    except UnicodeDecodeError as e:
        abort(400, 'UnicodeDecodeError')
    renderer = ft_getconfig('DEFAULTRENDERER')
    timeout = ft_getconfig('WORKERTIMEOUT')
    if not request.args.get('renderer') == None:
        renderer = request.args.get('renderer')
    if not request.args.get('timeout') == None:
        renderer = request.args.get('timeout')
    worker = flasktex.texworker.TexWorker(data, renderer=renderer, timeout=timeout)
    worker.run()
    return make_response('ok workid={}'.format(worker.workid), 200)

@app.route("/api/submit", methods=['GET'])
def ft_api_submit_web():
    if request.args.get('data') == None:
        return "No arg"
    return "Submit here with POST method"

@app.route("/api/status")
def ft_api_status():
    # First, read the database and obtain all the info
    conn = ft_db_connect_sqlite()
    c = conn.cursor()
    c.execute('SELECT id, userid, starttime, stoptime, status FROM `work`;')
    result = c.fetchall()
    conn.close()

    # Second, make a response
    resp = make_response()
    resp.headers['Content-Type'] = 'text/xml'
    resp.data = render_template('status.xml', result=result)
    return resp

@app.route("/api/obtain/<int:work_id>")
def ft_api_obtain(work_id):
    # First, open database conn and find the record
    conn = ft_db_connect_sqlite()
    c = conn.cursor()
    try:
        work_id = int(work_id)
    except ValueError:
        abort(400)
    found = False
    for i in c.execute('SELECT status, output FROM `work` WHERE id=?;', (work_id,)):
        found = True
        break
    if not found or not i[0] == "S": # NOT SUCCESSFUL
        abort(404)
    resp =make_response(i[1], 200)
    resp.headers['Content-Type'] = 'application/pdf'
    conn.close()
    return resp

