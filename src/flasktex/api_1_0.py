"""Flasktex API 1.0 views
"""

from flask import request
from flasktex import app

def ft_api_route_prefix(version_string):
    return "/api/{}".format(str(version_string))

@app.route(ft_api_route_prefix("1.0")+"/submit/xmlbundle", methods=['POST'])
def ft_api_submit_xmlbundle():
    try:
        data = request.get_data().decode('UTF-8')
    except UnicodeDecodeError as e:
        abort(400, 'UnicodeDecodeError')
        
    return "hello"
