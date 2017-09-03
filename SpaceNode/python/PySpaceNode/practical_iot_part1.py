# Animated plot example using phao.mqtt.client library
# 
# This script will make a plot of temperature data recieved
# in json format. The x-axis is numbered 0-11. The y-data
# is fed into a ring-buffer and plotted as it is received
# from the mqtt.client.on_message call. Just about as simple 
# as it gets.
#
# apt-get install libffi6 libffi-dev
# pip install cairocffi
# pip install paho-mqtt
# pip install matplotlib
#
# Written by Steve Lammers
#

import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as mqtt
import json


# The host that the MQTT server is running on.
MQTT_SERVER_HOST = "10.2.0.33"

# The port that the MQTT server is listening on.
MQTT_SERVER_PORT = 1883

# The ID the MQTT client should have.
#
# This should have something unique, like your name, e.g.
# plotter_keith
MQTT_CLIENT_ID = "plotter_me"

# The topic to publish sensor data on.
#
# This must be the same topic found in the Arduino program.
#
# Add on something onto the topic to make it unique, e.g.
# /keith/sensors/data
MQTT_SENSOR_OUTPUT_TOPIC = "/me/sensors/data"

# The arrays for all of our data.
#
# These arrays will have 11 elements in them that are all 0s.
temperature_data = np.linspace(0,0,11)
humidity_data = np.linspace(0,0,11)

# The array for fake time. This array will have 11 slots with
# values 0, 1, 2, 3... 10.
time_data = np.linspace(0,10,11)

# Make the plots so we can update them dynamically.
plt.ion()

# Create a figure with a single plot in it. The plot will consist
# of two graphs, one of time vs temperature, whose color is red,
# and one that is time vs humidity, whose color is blue.
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
line1, = ax1.plot(time_data, temperature_data, '-r')
line2, = ax1.plot(time_data, humidity_data, '-b')

# Add some labels to the x and y axes and place a grid on the graph.
plt.xlabel('time (not really)')
plt.ylabel('temperature/humidity')
plt.title('Last 10x Temperature and Humidity Values')
plt.grid(True)

# Draw the initial graph.
fig.canvas.draw()

# The callback for when the MQTT client receives a connection response from the
# MQTT server.
def on_connect(mqtt_client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    mqtt_client.subscribe(MQTT_SENSOR_OUTPUT_TOPIC)

# The callback for when a message is received from the MQTT server.
def on_message(mqtt_client, userdata, msg):
    global humidity_data
    global temperature_data
    global time_data

    # Decode the JSON message that has come from the ESP8266.
    # The JSON string is encoded in UTF-8 characters.
    json_data = json.loads(msg.payload.decode('utf-8'))
    
    # Print out the incoming message for debugging.
    print(json_data)

    # Shift all the values in the temperature array 1 to the left.
    # The leftmost value at temperature_data[0] will disappear.
    temperature_data = np.roll(temperature_data, -1)
    
    # Place the new temperature value in the rightmost cell. 
    # The -1 means place the new temperature value 1 value from the end of
    # the array, that is the last value in the array.
    # -2 would be the second to last element in the array, -3 the third to
    # last element in the array.
    temperature_data[-1] = json_data['temperature']

    print("temperature_data: ")
    print(temperature_data)

    # Shift all the values in the humidity array 1 to the left.
    # The leftmost value at humidity_data[0] will disappear.
    humidity_data = np.roll(humidity_data, -1)
    
    # Place the new humidity value in the rightmost cell. 
    # The -1 means place the new humidity value 1 value from the end of
    # the array, that is the last value in the array.
    # -2 would be the second to last element in the array, -3 the third to
    # last element in the array.
    humidity_data[-1] = json_data['humidity']

    print("humidity_data: ")
    print(humidity_data)

    # Dynamically modify the ranges of the Y axis to the minimum and maximum
    # values of both temperature and humidity.
    plt.ylim([temperature_data.min(), temperature_data.max(), humidity_data.min(), humidity_data.max()])

    # Update the line objects.
    line1.set_ydata(temperature_data)
    line2.set_ydata(humidity_data)
    
    # Now update the graph on the screen.
    fig.canvas.draw()

# Create the MQTT client and connect it to the MQTT server.

mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_SERVER_HOST, MQTT_SERVER_PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqtt_client.loop_forever()
