#
# The web application for Tinker Space Command Server
#
# Written by Keith M. Hughes
#

from flask import Flask, Response, render_template, request
from flask_cors import CORS
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

        # Set up CORS headers on all API URLs
        CORS(self.app, resources={r"/api/*": {"origins": "*" }})
        
        self.add_endpoint("/<path:path>","root", self.root_endpoint)
        self.add_endpoint("/spaces","spaces", self.spaces_endpoint)
        self.add_endpoint("/space/<string:space_id>","space", self.space_endpoint)
        self.add_endpoint("/sensors","sensors", self.sensors_endpoint)
        self.add_endpoint("/sensor/<string:sensor_id>","sensor", self.sensor_endpoint)
        self.add_endpoint("/api/v1/spaces","api_v1_spaces", self.api_v1_spaces_endpoint)
        self.add_endpoint("/api/v1/space/<string:space_id>","api_v1_space", self.api_v1_space_endpoint)
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
        space_models = self.server.sensor_processor.entity_registry.sensed_entity_active_models.values()
        
        all_space_data = []
        for space_model in space_models:
            all_space_data.append(self.render_space_data(space_model))

        return Response(json.dumps(all_space_data), status=200, headers={'ContentType': 'application/json'})

    def api_v1_space_endpoint(self, space_id=None, *args):
        space = self.server.sensor_processor.entity_registry.get_sensed_active_model(space_id)
        
        value = self.render_space_data(space)

        return Response(json.dumps(value), status=200, headers={'ContentType': 'application/json'})

    def render_space_data(self, space):
        space_data = {
            'externalId': space.sensed_entity_description.external_id,
            'name': space.sensed_entity_description.name,
            'description': space.sensed_entity_description.description,
        }

        return space_data
    
    def api_v1_sensors_endpoint(self, *args):
        sensor_models = self.server.sensor_processor.entity_registry.sensor_entity_active_models.values()

        all_sensor_data = []
        for sensor_model in sensor_models:
            all_sensor_data.append(self.render_sensor_data(sensor_model))
        
        return Response(json.dumps(all_sensor_data), status=200, headers={'ContentType': 'application/json'})

    def api_v1_sensor_endpoint(self, sensor_id=None, *args):
        sensor_model = self.server.sensor_processor.entity_registry.get_sensor_active_model(sensor_id)
        
        sensor_result = self.render_sensor_data(sensor_model)

        return Response(json.dumps(sensor_result), status=200, headers={ 'ContentType': 'application/json'})

    def render_sensor_data(self, sensor_model):
        active_channels = []
        for channel in sensor_model.get_active_channels():
            channel_data = {
                'channelId': channel.channel_description.external_id,
                'channelName': channel.channel_description.name,
                'sensedItemName': channel.sensed_entity_active_model.sensed_entity_description.name,
                'sensedItemId': channel.sensed_entity_active_model.sensed_entity_description.external_id,
                'currentValue': channel.current_value
            }

            active_channels.append(channel_data)
        
        sensor_data = {
            'externalId': sensor_model.sensor_entity_description.external_id,
            'name': sensor_model.sensor_entity_description.name,
            'description': sensor_model.sensor_entity_description.description,
            'online': sensor_model._online,
            'timeLastValueReceived':  sensor_model.value_last_time_received_fmt(),
            'timeLastHeartbeatReceived':  sensor_model.heartbeat_last_time_received_fmt(),
            'activeChannels': active_channels
        }

        return sensor_data

    def api_v1_query_sensor_endpoint(self, sensor_id=None, *args):
        sensor = self.server.sensor_processor.entity_registry.get_sensor_active_model(sensor_id)

        channel = request.args['channel']
        startDateTime = request.args['startDateTime']
        endDateTime = request.args['endDateTime']

        result = self.server.event_persistence.get_sensor_channel_measurements(sensor_id, channel, startDateTime, endDateTime)
        
        return Response(json.dumps(result), status=200, headers={ 'ContentType': 'application/json'})

