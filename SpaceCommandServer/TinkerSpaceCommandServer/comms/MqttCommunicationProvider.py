#
# Written by Keith M. Hughes
#

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf
import paho.mqtt.client as mqtt
import time
import json

class MqttCommunicationProvider:
  """A communication provider for TinkerSpaceCommand that sets up an 
     MQTT client.
  """

  def __init__(self, config):
    mqttConfig = config["communication"]["mqtt"]

    # The ID the MQTT client should have.
    #
    # This should have something unique, like your name, e.g.
    # relaycontrol_keith
    self.MQTT_CLIENT_ID = mqttConfig["serverClientId"]

    # The topic to publish sensor data on.
    self.MQTT_SENSOR_DATA_INPUT_TOPIC = mqttConfig["sensorInputTopic"]

    # The mDNS service name for the MQTT broker.
    self.MDNS_SERVICE_NAME_MQTT = mqttConfig["mqttMdnsServiceName"]

    # Is the MQTT client connected to the broker?
    self.mqtt_client_connected = False

  def start(self):
    print("Starting MQTT Communication Provider")
    
    # Create the MQTT client and add in all needed callbacks.
    self.mqtt_client = mqtt.Client(client_id=self.MQTT_CLIENT_ID)
    self.mqtt_client.on_connect = self.on_mqtt_connect
    self.mqtt_client.on_message = self.on_new_mqtt_message

    # Create the Zeroconf service browser that will look for a local
    # service _mqtt._tcp
    self.zeroconf = Zeroconf()
    self.servicebrowser = ServiceBrowser(self.zeroconf, self.MDNS_SERVICE_NAME_MQTT, handlers=[self.on_zeroconf_service_state_change])

  def stop(self):
    print("Stopping MQTT Communication provider")

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
      ipv4_address = '.'.join(str(i) for i in service_info.address)
        
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

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    self.mqtt_client.subscribe(self.MQTT_SENSOR_DATA_INPUT_TOPIC)
    
    # Mark the client as connected.
    self.mqtt_client_connected = True

  def on_new_mqtt_message(self, mqtt_client, userdata, msg):
    # A new MQTT message has come in.
    
    # Decode the JSON message that has come from sensor nodes.
    # The JSON string is encoded in UTF-8 characters.
    json_data = json.loads(msg.payload.decode('utf-8'))
