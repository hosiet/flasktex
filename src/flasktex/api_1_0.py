from flasktex import app

def ft_api_route_prefix(version_string):
    return "/api/{}".format(str(version_string))

@app.route(ft_api_route_prefix("1.0")+"/submit/xmlbundle")
def ft_route_submit_xmlbundle():
    return "hello"
