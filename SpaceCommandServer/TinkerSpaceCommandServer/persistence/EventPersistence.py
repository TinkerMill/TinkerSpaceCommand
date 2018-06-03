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
    
class EventPersistence:
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
      print("Perparing persist")
      json_body = [
        {
          "measurement": Constants.INFLUXDB_MEASUREMENT_NAME_SENSORS,
          "tags": {
            Constants.INFLUXDB_TAG_NAME_SENSED: measurement_event.sensed_active_model.sensed_entity_description.external_id,
            Constants.INFLUXDB_TAG_NAME_SENSOR: measurement_event.sensor_active_model.sensor_entity_description.external_id,
            Constants.INFLUXDB_TAG_NAME_CHANNEL: measurement_event.active_channel.channel_id
          },
          "time": datetime.datetime.fromtimestamp(measurement_event.time_received).isoformat() + 'Z',
          "fields": {
            "value": measurement_event.value
          }
        }
      ]

      print(json_body)
      foo = self.persistence_client.write_points(json_body)
      print(foo)
      print("Data point persisted")
    except:
      print(traceback.format_exc())

