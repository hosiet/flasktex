"""Flasktex API 1.0 views
"""

from flask import request, abort
from flasktex import app, bundle2tex
from flasktex.upload import UploadedWorkRequest
#from flasktex.bundle2tex import ft_uploadedworkrequest_to_request # TODO IMPLEMENT ME

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
    if request.method == 'GET':
        pass
    elif request.method == 'DELETE':
        pass
    pass
# TODO FINISH ME
