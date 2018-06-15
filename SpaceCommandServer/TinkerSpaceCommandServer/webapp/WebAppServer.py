#
# The web application for Tinker Space Command Server
#
# Written by Keith M. Hughes
#

from flask import Flask, Response, render_template, request
import os
import json
import datetime

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
        self.add_endpoint("/api/v1/spaces","api_v1_spaces", self.api_v1_spaces_endpoint)
        self.add_endpoint("/api/v1/<string:space_id>","api_v1_space", self.api_v1_space_endpoint)
        self.add_endpoint("/api/v1/sensors","api_v1_sensors", self.api_v1_sensors_endpoint)
        self.add_endpoint("/api/v1/sensor/<string:sensor_id>","api_v1_sensor", self.api_v1_sensor_endpoint)
        self.add_endpoint("/api/v1/query/sensor/<string:sensor_id>","api_v1_query_sensor", self.api_v1_query_sensor_endpoint)

    def start(self):
        self.app.run(host='0.0.0.0')

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
    

    def api_v1_spaces_endpoint(self, *args):
        spaces = self.server.sensor_processor.entity_registry.sensed_entity_active_models.values()
        
        values = []
        for space in spaces:
            values.append(self.render_space_data(space))

        return Response(json.dumps(values), status=200, headers={'ContentType': 'application/json'})

    def api_v1_space_endpoint(self, space_id=None, *args):
        space = self.server.sensor_processor.entity_registry.get_sensed_active_model(space_id)
        
        value = self.render_space_data(space)

        return Response(json.dumps(value), status=200, headers={'ContentType': 'application/json'})

    def render_space_data(self, space):
        space_data = {
            'externalId': space.sensed_entity_description.external_id,
            'name': space.sensed_entity_description.name
        }

        return space_data
    
    def api_v1_sensors_endpoint(self, *args):
        sensors = self.server.sensor_processor.entity_registry.sensor_entity_active_models.values()
        
        template = render_template("sensors.html", sensors=sensors)

        return Response(template, status=200, headers={'ContentType': 'application/json'})

    def api_v1_sensor_endpoint(self, sensor_id=None, *args):
        sensor = self.server.sensor_processor.entity_registry.get_sensor_active_model(sensor_id)
        
        template = render_template("sensor.html", sensor=sensor)

        return Response(template, status=200, headers={ 'ContentType': 'application/json'})

    def api_v1_query_sensor_endpoint(self, sensor_id=None, *args):
        sensor = self.server.sensor_processor.entity_registry.get_sensor_active_model(sensor_id)

        channel = request.args['channel']
        startDateTime = request.args['startDateTime']
        endDateTime = request.args['endDateTime']

        self.server.event_persistence.get_channel_measurements(channel, startDateTime, endDateTime)
        
        template = render_template("sensor.html", sensor=sensor)

        return Response(template, status=200, headers={ 'ContentType': 'application/json'})

