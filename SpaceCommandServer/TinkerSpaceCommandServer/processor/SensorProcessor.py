#
# Written by Keith Hughes
#

from TinkerSpaceCommandServer import Messages

class SensorProcessor:
  """The processor that takes sensor messages apart and updates the sensor models.
  """
  
  def __init__(self, entity_registry):
    self.entity_registry = entity_registry

  def process_sensor_input(self, message, time_received):
    print("Sensor processor got message {} at time {}".format(message, time_received))

    message_type = message[Messages.MESSAGE_FIELD_MESSAGE_TYPE]

    if message_type == Messages.MESSAGE_VALUE_MESSAGE_TYPE_MEASUREMENT:
      self.process_measurement(message, time_received)

  def process_measurement(self, message, time_received):
    # Get the sensor ID out of the message that has just come in.
    sensor_id = message[Messages.MESSAGE_FIELD_SENSOR_ID]

    # Get the active model for the sensor mentioned in the message.
    # We then have to check if the sensor ID in the message is for a known
    # sensor.
    active_model = self.entity_registry.get_sensor_active_model(sensor_id)
    if active_model is not None:    
      # The sensor ID was for a known sensor.
      
      # Cycle through the data portion of the message, picking up the
      # channel ID and the data from the channel
      for channel_id, channel_data in message[Messages.MESSAGE_FIELD_DATA].items():

        # Look up the active channel model for the given channel ID.
        # Don't assume the channel ID is actually known, but check
        # that the active channel for the channel ID exists.
        active_channel = active_model.get_active_channel_model(channel_id)
        if active_channel is not None:
          active_sensed_entity = active_channel.sensed_entity_active_model
          measurement_type = active_channel.channel_description.measurement_type
          value = channel_data[Messages.MESSAGE_FIELD_VALUE]

          # Update the value in the active channel
          active_channel.update_current_value(value)

          active_sensed_entity.show_values()
        else:
          print("Sensor {} has unknown channel {}".format(sensor_id, channel_id))
    else:
      print("Message for unknown sensor with sensor ID {}".format(sensor_id))

    
      
