#
# A Python program that uses mDNS to locate an MQTT broker to connect to.
# It then creates a UI of checkboxes to determine relays to turn on and off.
# The checkboxes determine the bits of an integer and specify whether a
# given bit is on or off. This integer is encoded as a hex number and sent
# over the MQTT channel.
#
#
# pip3 install zeroconf
# pip3 install paho-mqtt
# pip3 install pyyaml
#
# Written by Keith M. Hughes
#

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf
import paho.mqtt.client as mqtt
import signal
import time
import sys

class SpaceCommandServer:

  def __init__(self):
    # The ID the MQTT client should have.
    #
    # This should have something unique, like your name, e.g.
    # relaycontrol_keith
    self.MQTT_CLIENT_ID = "tinker_space_command_server"

    # The topic to publish sensor data on.
    self.MQTT_CONTROL_OUTPUT_TOPIC = "/tinkermill/sensors/control"

    # The mDNS service name for the MQTT broker.
    self.MDNS_SERVICE_NAME_MQTT = "_mqtt._tcp.local."

    # Is the MQTT client connected to the broker?
    self.mqtt_client_connected = False


  def start(self):
    print("Starting Tinker Space Command Server")
    
    # Create the MQTT client and connect it to the MQTT server.
    self.mqtt_client = mqtt.Client(client_id=self.MQTT_CLIENT_ID)
    self.mqtt_client.on_connect = self.on_mqtt_connect

    # Create the Zeroconf service browser that will look for a local
    # service _mqtt._tcp
    self.zeroconf = Zeroconf()
    ServiceBrowser(self.zeroconf, self.MDNS_SERVICE_NAME_MQTT, handlers=[self.on_zeroconf_service_state_change])

  def stop(self):
    print("Stopping Tinker Space Command Server")

    # Close the MQTT client if it is connected.
    if self.mqtt_client_connected:
      self.mqtt_client.loop_stop()
      
    # Zeroconf may be closed already but make sure.
    self.zeroconf.close()

  def on_zeroconf_service_state_change(self, zeroconf, service_type, name, state_change):
    #
    # This function will be called when a Zeroconf Service Browser finds the
    # requested service.
    #

    # If we see the MQTT service added, a broker has been found.
    if state_change is ServiceStateChange.Added:
      service_info = zeroconf.get_service_info(service_type, name)

      # The IP address of the service info object looks like
      # '\xc0\xa8\x01\x8f', so must be translated into a regular
      # x.y.z.w IP address.
      ipv4_address = '.'.join(str(ord(i)) for i in service_info.address)
        
      print('Found MQTT broker at {0}:{1}'.format(ipv4_address, service_info.port))
        
      self.connect_mqtt(ipv4_address, service_info.port)
        
      # Don't leave zeroconf running
      self.zeroconf.close()

  # Connect to the MQTT broker and start processing MQTT packets.
  def connect_mqtt(self, mqtt_host, mqtt_port):
    self.mqtt_client.connect(mqtt_host, mqtt_port, 60)
    self.mqtt_client.loop_start()

  
  def on_mqtt_connect(self, mqtt_client, userdata, flags, rc):
    # The callback for when the MQTT client receives a connection response from the
    # MQTT server.
    print("Connected to mqtt broker with result code "+str(rc))
    
    # Mark the client as connected.
    self.mqtt_client_connected = True


server = SpaceCommandServer()
server.start()

# Signal handler for sigint.
#
# This is used to catch ^C to the client and will do any needed cleanup, for
# example, shut down the connection to the MQTT broker.
def signal_handler(signal, frame):
  server.top()
  
  # Exit the program completely.
  sys.exit(0)

# Set the ^C handler.
signal.signal(signal.SIGINT, signal_handler)


