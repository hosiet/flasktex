"""Flasktex API 1.0 views
"""

from flask import request, abort
from flasktex import app, bundle2tex


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

    # FIXME: finish me
    return None

