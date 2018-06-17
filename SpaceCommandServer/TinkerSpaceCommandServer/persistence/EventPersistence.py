#
# The event persistence layer.
#

#
# Written by Keith Hughes
#

import traceback
import datetime
from rx import Observer
from influxdb import InfluxDBClient
from TinkerSpaceCommandServer import Constants

class EventPersistenceObserver(Observer):
  def __init__(self, persistence):
    self.persistence = persistence

  def on_next(self, measurement_event):
    self.persistence.persist_measurement(measurement_event)

  def on_completed(self):
    print("Event persistence subject Done!")

  def on_error(self, error):
    print("Event persistence subject Error Occurred: {0}".format(error))
    
class InfluxEventPersistence:
  def __init__(self, config):
    self.persistence_observer = EventPersistenceObserver(self)

    influxdb_config = config["persistence"]["influxdb"]

    server_host = influxdb_config["server"]["host"]
    server_port = influxdb_config["server"]["port"]
    server_username = influxdb_config["server"]["username"]
    server_password = influxdb_config["server"]["password"]

    sensor_tablename = influxdb_config["sensors"]["databaseName"]
    
    self.persistence_client = InfluxDBClient(server_host, server_port, server_username, server_password, sensor_tablename)

  def attach_sensor_processor(self, sensor_processor):
    sensor_processor.register_sensor_update_observer(self.persistence_observer)

  def start(self):
    pass

  def stop(self):
    pass

  def persist_measurement(self, measurement_event):
    try:
      json_body = [
        {
          "measurement": Constants.INFLUXDB_MEASUREMENT_NAME_SENSORS,
          "tags": {
            Constants.INFLUXDB_TAG_NAME_SENSED: measurement_event.sensed_active_model.sensed_entity_description.external_id,
            Constants.INFLUXDB_TAG_NAME_SENSOR: measurement_event.sensor_active_model.sensor_entity_description.external_id,
            Constants.INFLUXDB_TAG_NAME_CHANNEL: measurement_event.active_channel.channel_id
          },
          "time": datetime.datetime.fromtimestamp(measurement_event.time_received).isoformat() + 'Z',
          "fields": self.create_measurement_fields(measurement_event)
        }
      ]

      self.persistence_client.write_points(json_body)
    except:
      print(traceback.format_exc())

  def create_measurement_fields(self, measurement_event):
    """Add in the measurement value into the message to influx.
    """
    
    fields = {
      "continuous_value": float(measurement_event.value)
    }

    return fields

  def get_channel_measurements(self, channel, startDateTime, endDateTime):
    startTimestamp = datetime.datetime.timestamp(datetime.datetime.strptime(startDateTime, "%Y-%m-%dT%H:%M:%S%Z"))
    endTimestamp = datetime.datetime.timestamp(datetime.datetime.strptime(endDateTime, "%Y-%m-%dT%H:%M:%S%Z"))

    startTimestamp = startTimestamp * 1000000000
    endTimestamp = endTimestamp * 1000000000
        
    query = "select * from sensors where channel = '{0}' and time >= {1:.0f} and time < {2:.0f}".format(channel, startTimestamp, endTimestamp)

    time_array = []
    value_array = []
    sensor_array = []
    sensed_array = []
    results = self.persistence_client.query(query)
    points = results.get_points('sensors', None)
    for point in points:
      time_array.append(point['time'])
      sensor_array.append(point['sensor'])
      sensed_array.append(point['sensed'])
      value_array.append(point['continuous_value'])

    ret = {
      'data': {
        'time': time_array,
        'sensor': sensor_array,
        'sensed': sensed_array,
        'value': value_array
      }
    }

    return ret

  def get_sensor_channel_measurements(self, sensor_id, channel, startDateTime, endDateTime):
    startTimestamp = datetime.datetime.timestamp(datetime.datetime.strptime(startDateTime, "%Y-%m-%dT%H:%M:%S%Z"))
    endTimestamp = datetime.datetime.timestamp(datetime.datetime.strptime(endDateTime, "%Y-%m-%dT%H:%M:%S%Z"))

    startTimestamp = startTimestamp * 1000000000
    endTimestamp = endTimestamp * 1000000000
        
    query = "select * from sensors where sensor = '{0}' and channel = '{1}' and time >= {2:.0f} and time < {3:.0f}".format(sensor_id, channel, startTimestamp, endTimestamp)

    time_array = []
    value_array = []
    sensed_array = []
    results = self.persistence_client.query(query)
    points = results.get_points('sensors', None)
    for point in points:
      time_array.append(point['time'])
      sensed_array.append(point['sensed'])
      value_array.append(point['continuous_value'])

    ret = {
      'data': {
        'time': time_array,
        'sensed': sensed_array,
        'value': value_array
      }
    }

    return ret

  def get_sensor_measurements(self, sensor, startDateTime, endDateTime):
    startTimestamp = datetime.datetime.timestamp(datetime.datetime.strptime(startDateTime, "%Y-%m-%dT%H:%M:%S%Z"))
    endTimestamp = datetime.datetime.timestamp(datetime.datetime.strptime(endDateTime, "%Y-%m-%dT%H:%M:%S%Z"))

    startTimestamp = startTimestamp * 1000000000
    endTimestamp = endTimestamp * 1000000000
        
    query = "select * from sensors where sensor = '{0}' and time >= {1:.0f} and time < {2:.0f}".format(sensor, startTimestamp, endTimestamp)

    results = self.persistence_client.query(query)
    print(results)

  def get_sensed_measurements(self, sensed, startDateTime, endDateTime):
    startTimestamp = datetime.datetime.timestamp(datetime.datetime.strptime(startDateTime, "%Y-%m-%dT%H:%M:%S%Z"))
    endTimestamp = datetime.datetime.timestamp(datetime.datetime.strptime(endDateTime, "%Y-%m-%dT%H:%M:%S%Z"))

    startTimestamp = startTimestamp * 1000000000
    endTimestamp = endTimestamp * 1000000000
        
    query = "select * from sensors where sensed = '{0}' and time >= {1:.0f} and time < {2:.0f}".format(sensed, startTimestamp, endTimestamp)

    results = self.persistence_client.query(query)
    print(results)
    
    
