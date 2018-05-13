#
# The event persistence layer.
#

#
# Written by Keith Hughes
#

from rx import Observer
from influxdb import InfluxDBClient

class EventPersistenceSubject(Observer):
  def __init__(self, persistence):
    self.persistence = persistence

  def on_next(self, measurement_event):
    print("Received measurement event")

  def on_completed(self):
    print("Event persistence subject Done!")

  def on_error(self, error):
    print("Event persistence subject Error Occurred: {0}".format(error))
    
class EventPersistence:
  def __init__(self):
    self.persistence_subject = EventPersistenceSubject(self)

    self_persistence_client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')

  def attach_sensor_processor(self, sensor_processor):
    sensor_processor.register_sensor_update_observer(self.persistence_subject)

  def start(self):
    pass

  def stop(self):
    pass
