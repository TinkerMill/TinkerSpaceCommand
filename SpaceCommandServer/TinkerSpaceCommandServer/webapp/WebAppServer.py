from flask import Flask, Response, render_template

def action():
    print("Hi there")
    
class EndpointAction:
    def __init__(self, app, action):
        self.app = app
        self.action = action
        self.response = Response("Hello world", status=200, headers={})

    def __call__(self, *args):
        self.action()

        foo = render_template("foo.html")
        print(foo)
        return self.response

class WebAppServer:

    def __init__(self, name):
        self.app = Flask(name)
        self.add_endpoint("/","root", action)

    def start(self):
        self.app.run()

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(self.app, handler))

