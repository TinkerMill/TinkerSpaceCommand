#
# Written by Keith M. Hughes
#

import sys
import yaml
import MqttCommunicationProvider
import SpaceCommandServer

# Read the configuration for the server.
#
# The configuration file is in YAML.
# be used in both languages.
with open(sys.argv[1]) as fp:
  config = yaml.safe_load(fp)

server = SpaceCommandServer.SpaceCommandServer(config)
server.addCommunicationProvider( MqttCommunicationProvider.MqttCommunicationProvider(config) )
server.start()

# TODO(keith): Just start up the server in its own thread so don't need this.
while True:
  pass
