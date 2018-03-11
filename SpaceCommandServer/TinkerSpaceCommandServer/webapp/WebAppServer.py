#
# The web application for Tinker Space Command Server
#
# Written by Keith M. Hughes
#

from flask import Flask, Response, render_template
import os

class WebAppServer:

    def __init__(self, name, server):
        self.server = server
        
        # need the folder the source file of the web app is in so the
        # templates and static subfolders can be found.
        modpath = __file__

        # Turn pyc files into py files if we can
        if modpath.endswith('.pyc') and os.path.exists(modpath[:-1]):
            modpath = modpath[:-1]
    
        # Sort out symlinks
        modpath = os.path.realpath(modpath)

        self.template_dir = os.path.join(os.path.dirname(modpath), "templates")
        self.static_dir = os.path.join(os.path.dirname(modpath), "static")
        
        self.app = Flask(name, template_folder=self.template_dir, static_folder=self.static_dir)
        
        self.add_endpoint("/<path:path>","root", self.root_endpoint)
        self.add_endpoint("/spaces","spaces", self.spaces_endpoint)
        self.add_endpoint("/space/<string:space_id>","space", self.space_endpoint)
        self.add_endpoint("/sensors","sensors", self.sensors_endpoint)
        self.add_endpoint("/sensor/<string:sensor_id>","sensor", self.sensor_endpoint)

    def start(self):
        self.app.run()

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, handler)

    def root_endpoint(self, path=None, *args):
        template = render_template("foo.html", name="Keith")

        return Response(template, status=200, headers={})

    def spaces_endpoint(self, *args):
        spaces = self.server.sensor_processor.entity_registry.sensed_entity_active_models.values()
        
        template = render_template("spaces.html", spaces=spaces)

        return Response(template, status=200, headers={})

    def space_endpoint(self, space_id=None, *args):
        space = self.server.sensor_processor.entity_registry.get_sensed_active_model(space_id)
        
        template = render_template("space.html", space=space)

        return Response(template, status=200, headers={})

    def sensors_endpoint(self, *args):
        sensors = self.server.sensor_processor.entity_registry.sensor_entity_active_models.values()
        
        template = render_template("sensors.html", sensors=sensors)

        return Response(template, status=200, headers={})

    def sensor_endpoint(self, sensor_id=None, *args):
        sensor = self.server.sensor_processor.entity_registry.get_sensor_active_model(sensor_id)
        
        template = render_template("sensor.html", sensor=sensor)

        return Response(template, status=200, headers={})
    
