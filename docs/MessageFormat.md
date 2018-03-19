The message format for sensors is a JSON-based data structure encoded in UTF-8.
Message types are located in the file: SpaceCommandServer->TinkerSpaceCommandServer->Messages.py
```
{
  sensorId: "the sensor ID",
  messageType: "",
  data: {
    channel1: {
      value: the sensor value
    },
    channel2: {
      value: the sensor value
    },
    ...
  }
}
```

The outer envelope of the message sontains the sensor ID, the
message type, and a data map.

The sensor ID gives the globally unique ID for the sensor.

messageType gives the type of the data packet. For sensor measurements, it will
have a value of 'measurement' or 'heartbeat'.

Heartbeat
---------
The heartbeat is used to validate that a node exists and is currently connected. This is used for nodes that do not send regular chronological data back to the server. If a heartbeat is not recieved within the timeout duration, then the server will update the webserver to indicate that the node is no longer communicating.

Data Packet
-----------
The data packet for a sensor measurement will be a map of channel IDs and the
values for those channels. For example, if the sensor gives temperature and
humidity values, the data section of the sensor packet will look like

```
data: {
  "temperature": {
    "value": 72
  },
  "humidity": {
    "value": 22
  }
}
```

The reason for this format is for sensor units that can take multiple
measurements simultaneously, such as a DHT-22 which measures both temperature
and humidity in one package.

It may be asked why the channel ID could not be the type of the data. In the
example above the channel "temperature" has a type of "temperature". Separating
the channel ID from the type of the data packet allows a given sensor to
make multiple measurements of the same type, for example a single sensor
platform could measure the moisture content for multiple pots of soil.

{
  "messageType": "measurement",
  "sensorId": "sensor.esp8266.FE13DE",
  "data": {
    "temperature": {
      "value": 72
    },
    "humidity": {
      "value": 22
    }
  }
}

A heartbeat message for the sensor would be:


{
  "messageType": "heartbeat",
  "sensorId": "sensor.esp8266.FE13DE",
}
