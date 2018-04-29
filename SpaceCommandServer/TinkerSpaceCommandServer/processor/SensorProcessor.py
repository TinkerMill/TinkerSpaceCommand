#
# The Sensor Processor takes sensor inpput from the communication channels in
# the comm package, sorts out the type of communication, and forwards the
# information to the appropriate active models found in the entities package.
#

#
# Written by Keith Hughes
#

from TinkerSpaceCommandServer.events.StandardEvents import SensorChannelMeasurementEvent
from TinkerSpaceCommandServer import Messages
from TinkerSpaceCommandServer import Constants
from rx.subjects import Subject
from threading import Thread
import time

class SensorProcessorOfflineThread(Thread):
  """The offline thread periodically checks all sensors to see if they 
     have gone offline.
  """
  
  def __init__(self, sensor_processor):
    Thread.__init__(self)
    self.sensor_processor = sensor_processor
    self.running = True

  def run(self):
    while self.running:
      # let's start by sleeping to give sensors a chance to send their first
      # value before declaring them offline.
      time.sleep(Constants.SENSOR_OFFLINE_CHECK_DELAY)

      current_time = time.time()
      # Check heartbeat to see if sensor has gone offline.
      for active_sensor_model in self.sensor_processor.entity_registry.get_all_sensor_active_models():
        offline = active_sensor_model.check_if_offline_transition(current_time)
      
  def stop(self):
    self.running = False
    
class SensorProcessor:
  """The processor that takes sensor messages apart and updates the sensor models.
  """
  
  def __init__(self, entity_registry):
    self.entity_registry = entity_registry

    # An RX subject for any sensor measurement
    self.sensor_measurement_subject = Subject()

  def start(self):
    self.sensor_processor_thread = SensorProcessorOfflineThread(self)
    self.sensor_processor_thread.start()
    
  def stop(self):
    self.sensor_processor_thread.stop()
    
  def process_sensor_input(self, message, time_received):
    print("Sensor processor got message {} at time {}".format(message, time_received))

    message_type = message[Messages.MESSAGE_FIELD_MESSAGE_TYPE]

    if message_type == Messages.MESSAGE_VALUE_MESSAGE_TYPE_MEASUREMENT:
      self.process_measurement(message, time_received)
    elif message_type == Messages.MESSAGE_VALUE_MESSAGE_TYPE_HEARTBEAT:
      self.process_heartbeat(message, time_received)

  def process_measurement(self, message, time_received):
    """A measurement message has been received. Process it.
    """
    
    # Get the sensor ID out of the message that has just come in.
    sensor_id = message[Messages.MESSAGE_FIELD_SENSOR_ID]

    # Get the active model for the sensor mentioned in the message.
    # We then have to check if the sensor ID in the message is for a known
    # sensor.
    sensor_active_model = self.entity_registry.get_sensor_active_model(sensor_id)
    if sensor_active_model is not None:    
      # The sensor ID was for a known sensor.
      
      # Cycle through the data portion of the message, picking up the
      # channel ID and the data from the channel
      for channel_id, channel_data in message[Messages.MESSAGE_FIELD_DATA].items():

        # Look up the active channel model for the given channel ID.
        # Don't assume the channel ID is actually known, but check
        # that the active channel for the channel ID exists.
        active_channel = sensor_active_model.get_active_channel_model(channel_id)
        if active_channel is not None:
          active_sensed_entity = active_channel.sensed_entity_active_model
          measurement_type = active_channel.channel_description.measurement_type
          value = channel_data[Messages.MESSAGE_FIELD_VALUE]

          sensor_channel_measurement_event = SensorChannelMeasurementEvent(sensor_active_model, active_sensed_entity, active_channel, value, time_received)
          
          # Update the value in the active channel
          active_channel.update_current_value(value, time_received)

          active_sensed_entity.show_values()
          self.sensor_measurement_subject.on_next(sensor_channel_measurement_event)
        else:
          print("Sensor {} has unknown channel {}".format(sensor_id, channel_id))
    else:
      print("Measurement message for unknown sensor with sensor ID {}".format(sensor_id))

  def process_heartbeat(self, message, time_received):
    """A heartbeat message has been received. Process it.
    """
    
    # Get the sensor ID out of the message that has just come in.
    sensor_id = message[Messages.MESSAGE_FIELD_SENSOR_ID]

    # Get the active model for the sensor mentioned in the message.
    # We then have to check if the sensor ID in the message is for a known
    # sensor.
    sensor_active_model = self.entity_registry.get_sensor_active_model(sensor_id)
    if sensor_active_model is not None:    
      # The sensor ID was for a known sensor.
      
      # Tell the sensor it has received a heartbeat.
      sensor_active_model.heartbeat_received(time_received)
    else:
      print("Message for unknown sensor with sensor ID {}".format(sensor_id))
