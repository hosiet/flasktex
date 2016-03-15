"""Flasktex API 1.0 views
"""

from flask import request, abort
from flasktex import app, bundle2tex
from flasktex.upload import UploadedWorkRequest
#from flasktex.bundle2tex import ft_uploadedworkrequest_to_request # TODO IMPLEMENT ME

import json

def _apiprefix(version):
    return "/api/{}".format(str(version))


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
        uploaded_work_request = UploadedData(json.loads(data), objtype='json')
    except:
        abort(400, 'DataCorruptError')

    # TODO Convert UploadedWorkRequest to TeXRequest
    texrequest = bundle2tex.ft_uploadedworkrequest_to_request(uploaded_work_request)
    texrequest.process()

    ret_string = """{\
"status": {},\
"status_string": {},\
"worker_id": {},\
retrieve_id: {}}""".format(
        str(texrequest.get_status()),
        str(texrequest.id),
        str(texrequest.retrieve_id),
        )

    return ret_string


    # FIXME: finish me, use JSON module
    return None

