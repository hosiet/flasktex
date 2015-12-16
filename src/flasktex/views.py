from flasktex import app
import flasktex.api_1_0


@app.route("/")
def ft_route_root():
    return 'this is root.'

