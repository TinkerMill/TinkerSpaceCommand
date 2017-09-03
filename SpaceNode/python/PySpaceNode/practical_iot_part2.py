#
# A Python program that uses mDNS to locate an MQTT broker to connect to.
# It then creates a UI of checkboxes to determine relays to turn on and off.
# The checkboxes determine the bits of an integer and specify whether a
# given bit is on or off. This integer is encoded as a hex number and sent
# over the MQTT channel.
#
#
# pip install zeroconf
# pip install paho-mqtt
#
# Written by Keith M. Hughes
#

from Tkinter import *
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf
import paho.mqtt.client as mqtt
import signal
import time
import sys

# The ID the MQTT client should have.
#
# This should have something unique, like your name, e.g.
# relaycontrol_keith
MQTT_CLIENT_ID = "relaycontrol_myClientId"

# The topic to publish sensor data on.
#
# This must be the same topic found in the Arduino program.
#
# Add on something onto the topic to make it unique, e.g.
# /keith/tinkermill/sensors/control
MQTT_CONTROL_OUTPUT_TOPIC = "/tinkermill/sensors/control"

# The mDNS service name for the MQTT broker.
MDNS_SERVICE_NAME_MQTT = "_mqtt._tcp.local."

# Is the MQTT client connected to the broker?
mqtt_client_connected = False

# Signal handler for sigint.
#
# This is used to catch ^C to the client and will do any needed cleanup, for
# example, shut down the connection to the MQTT broker.
def signal_handler(signal, frame):
  # Close the MQTT client if it is connected.
  if mqtt_client_connected:
    mqtt_client.loop_stop()
      
  # Zeroconf may be closed already but make sure.
  zeroconf.close()
  
  # Exit the program completely.
  sys.exit(0)

# Set the ^C handler.
signal.signal(signal.SIGINT, signal_handler)

#
# This function will be called when a Zeroconf Service Browser finds the
# requested service.
#
def on_zeroconf_service_state_change(zeroconf, service_type, name, state_change):
  # If we see the MQTT service added, a broker has been found.
  if state_change is ServiceStateChange.Added:
    service_info = zeroconf.get_service_info(service_type, name)

    # The IP address of the service info object looks like
    # '\xc0\xa8\x01\x8f', so must be translated into a regular
    # x.y.z.w IP address.
    ipv4_address = '.'.join(str(ord(i)) for i in service_info.address)
        
    print "Found MQTT broker at {}:{}".format(ipv4_address, service_info.port)
        
    connect_mqtt(ipv4_address, service_info.port)
        
    # Don't leave zeroconf running
    zeroconf.close()

# Connect to the MQTT broker and start processing MQTT packets.
def connect_mqtt(mqtt_host, mqtt_port):
  mqtt_client.connect(mqtt_host, mqtt_port, 60)
  mqtt_client.loop_start()

  
# The callback for when the MQTT client receives a connection response from the
# MQTT server.
def on_mqtt_connect(mqtt_client, userdata, flags, rc):
  print("Connected to mqtt broker with result code "+str(rc))
    
  # Mark the client as connected.
  global mqtt_client_connected
  mqtt_client_connected = True

# called when the Send button is pushed in the UI.
def var_states():
  messageContent = (var1.get() | (var2.get() << 1) | (var3.get() << 2) |
      (var4.get() << 3) | (var5.get() << 4) | (var6.get() << 5) |
      (var7.get() << 6) | (var8.get() << 7) | (var9.get() << 8))
  message = "%0.3X" % (messageContent)
  print(message)
  
  if mqtt_client_connected:
    mqtt_client.publish(MQTT_CONTROL_OUTPUT_TOPIC, message)


# Create the MQTT client and connect it to the MQTT server.
mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID)
mqtt_client.on_connect = on_mqtt_connect

# Create the Zeroconf service browser that will look for a local
# service _mqtt._tcp
zeroconf = Zeroconf()
ServiceBrowser(zeroconf, MDNS_SERVICE_NAME_MQTT, handlers=[on_zeroconf_service_state_change])

master = Tk()

Label(master, text="Relay States:").grid(row=0, sticky=W)
var1 = IntVar()
Checkbutton(master, text="Relay 1", variable=var1).grid(row=1, sticky=W)
var2 = IntVar()
Checkbutton(master, text="relay 2", variable=var2).grid(row=2, sticky=W)
var3 = IntVar()
Checkbutton(master, text="relay 3", variable=var3).grid(row=3, sticky=W)
var4 = IntVar()
Checkbutton(master, text="relay 4", variable=var4).grid(row=4, sticky=W)
var5 = IntVar()
Checkbutton(master, text="relay 5", variable=var5).grid(row=5, sticky=W)
var6 = IntVar()
Checkbutton(master, text="relay 6", variable=var6).grid(row=6, sticky=W)
var7 = IntVar()
Checkbutton(master, text="relay 7", variable=var7).grid(row=7, sticky=W)
var8 = IntVar()
Checkbutton(master, text="relay 8", variable=var8).grid(row=8, sticky=W)
var9 = IntVar()
Checkbutton(master, text="relay 9", variable=var9).grid(row=9, sticky=W)
Button(master, text='Send', command=var_states).grid(row=10, sticky=W, pady=4)
Button(master, text='Quit', command=master.quit).grid(row=11, sticky=W, pady=4)

mainloop()
