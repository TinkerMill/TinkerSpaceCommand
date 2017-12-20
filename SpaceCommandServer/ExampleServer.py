
#
# Written by Keith M. Hughes
#

import pdb
import sys
import yaml

from TinkerSpaceCommandServer.SpaceCommandServer import *
from TinkerSpaceCommandServer.comms.MqttCommunicationProvider import *
from TinkerSpaceCommandServer.processor.SensorProcessor import *
from TinkerSpaceCommandServer.entities.EntityRegistry import *
from TinkerSpaceCommandServer.events.StandardEvents import *

# Read the configuration for the server.
#
# The configuration file is in YAML.
# be used in both languages.


if len(sys.argv) == 1:
  print("usage: ExampleServer.py config.yaml")
  print("       where config.yaml is the YAML configuration file for the server.")
  
  sys.exit(1)

with open(sys.argv[1]) as fp:
  config = yaml.safe_load(fp)

entity_registry = EntityRegistry()
entity_importer = YamlEntityRegistryReader()
entity_importer.load_registry('sensors.yaml', entity_registry)
entity_registry.prepare_runtime_models()

pdb.set_trace()
entity_registry.get_sensed_active_model('tinkermill.bay.main').register_value_update_observer(SensedPrintObserver())
entity_registry.get_sensor_active_model('sensor.esp8266.FE13DE').register_value_update_observer(SensorPrintObserver())

server = SpaceCommandServer(config)
server.sensor_processor = SensorProcessor(entity_registry)
server.addCommunicationProvider( MqttCommunicationProvider(config) )
server.start()



# TODO(keith): Just start up the server in its own thread so don't need this.
while True:
  pass
