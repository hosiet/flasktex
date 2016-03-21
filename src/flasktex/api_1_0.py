"""Flasktex API 1.0 views
"""

import flask
from flask import request, abort
from flasktex import app, bundle2tex
from flasktex.upload import UploadedWorkRequest
import flasktex.db
#from flasktex.bundle2tex import ft_uploadedworkrequest_to_request # TODO IMPLEMENT ME

import syslog

import json

def _apiprefix(version):
    return "/api/{}".format(str(version))

@app.route('/ping')
def ft_api_pingback():
    return 'pong'

@app.route(_apiprefix("1.0")+"/submit/xmlbundle", methods=['POST'])
def ft_api_submit_xmlbundle():
    try:
        data = request.get_data().decode('UTF-8')
    except UnicodeDecodeError:
        abort(400, 'UnicodeDecodeError')

    texrequest = bundle2tex.ft_xmlbundle_to_request(data)
    texrequest.process()

    # FIXME: use xml module and set proper Content-Type
    ret_string = """<?xml version="1.0" encoding="UTF-8" ?>
<return>
    <status>true</status>
    <status_string>{}</status_string>
    <worker_id>{}</worker_id>
    <retrieve_id>{}</retrieve_id>
</return>""".format(
            str(texrequest.get_status()),
            str(texrequest.id),
            str(texrequest.retrieve_id),
            )

    return ret_string

@app.route(_apiprefix("1.0")+'/submit', methods=['POST'])
@app.route(_apiprefix("1.0")+'/submit/json', methods=['POST'])
def ft_api_submit_json():
    try:
        data = request.get_data().decode('UTF-8')
    except UnicodeDecodeError:
        abort(400, 'UnicodeDecodeError')
    uploaded_work_request = None

    try:
        uploaded_work_request = UploadedWorkRequest(json.loads(data), objtype='json')
    except:
        abort(400, 'DataCorruptError')

    texrequest = bundle2tex.ft_uploadedworkrequest_to_request(uploaded_work_request)
    texrequest.process()

    from jinja2 import Template
    template = Template(
            '{"status": "{{ status }}", \
"status_string": "{{ status_string }}", \
"worker_id": {{ worker_id }}, \
"retrieve_id": {{ retrieve_id }}}'
                )
    ret_string = template.render(
            status = texrequest.get_status(),
            status_string = 'test',
            worker_id = texrequest.id,
            retrieve_id = texrequest.retrieve_id,
            )

    return ret_string

    # FIXME: finish me, use JSON module
    return None

@app.route(_apiprefix('1.0')+'/result/<int:req_id>/pdf', methods=['GET', 'DELETE'])
def ft_api_result(req_id):
    """
    Deal with requests to obtain pdf or delete record.
    """
    req_retrieve_id = request.args.get('retrieve_id')
    syslog.syslog('given retrieve id is {}.'.format(req_retrieve_id))
    conn = flasktex.db.ft_db_init_conn()
    c = conn.cursor()
    fetched_data = c.execute('SELECT `id`, `retrieve_id`, `output`, `status` FROM `work` WHERE `id`=?;', (req_id,)).fetchall()
    if len(fetched_data) == 0:
        flasktex.db.ft_db_close_conn(conn)
        flask.abort(404)
    syslog.syslog('before match ret id.')
    if not (str(fetched_data[0][1]) == str(req_retrieve_id)):
        syslog.syslog('given retrieve_id is {}, stored is {}. mismatch.'.format(str(fetched_data[0][1]), str(req_retrieve_id)))
        flasktex.db.ft_db_close_conn(conn)
        flask.abort(403)
    syslog.syslog('after match ret id.')
    server_status = str(fetched_data[0][3])
    if server_status == 'INIT' or server_status == 'STARTING' or server_status == 'RUNNING':
        flasktex.db.ft_db_close_conn(conn)
        resp = flask.make_response('Job was accepted and in status "{}".'.format(server_status), 202)
        return resp
    elif server_status[:7] == 'FAILURE':
        flasktex.db.ft_db_close_conn(conn)
        resp = flask.make_response('Process failed. This may be due to wrong latex syntax or wrong file arrangements.', 410)
        return resp
    elif server_status == 'DELETED':
        flasktex.db.ft_db_close_conn(conn)
        return flask.make_response('Requested job was already deleted.', 410)

    if request.method == 'GET':
        resp = flask.make_response(fetched_data[0][2], 200)
        resp.headers['Content-Disposition'] = 'inline; filename="output.pdf"'
        resp.headers['Content-Type'] = 'application/pdf'
        flasktex.db.ft_db_close_conn(conn)
        return resp
    elif request.method == 'DELETE':
        raise NotImplementedError
        pass
    pass
# TODO FINISH ME
# TODO check id
