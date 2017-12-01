#
# Written by Keith Hughes
#

from TinkerSpaceCommandServer import Messages

class SensorProcessor:
  """The processor that takes sensor messages apart and updates the sensor models.
  """
  
  def __init__(self, model_registry):
    self.model_registry = model_registry

  def process_sensor_input(self, message, time_received):
    print("Sensor processor got message {} at time {}".format(message, time_received))

    message_type = message[Messages.MESSAGE_FIELD_MESSAGE_TYPE]

    if message_type == Messages.MESSAGE_VALUE_MESSAGE_TYPE_MEASUREMENT:
      self.process_measurement(message, time_received)

  def process_measurement(self, message, time_received):
    sensor_id = message[Messages.MESSAGE_FIELD_SENSOR_ID]

    active_model = self.model_registry.get_sensor_active_model(sensor_id)

    if active_model is not None:    
      # Cycle through the data packet, picking up the channel ID and the data
      # from the channel
      for channel_id, channel_data in message[Messages.MESSAGE_FIELD_DATA].items():
        active_channel = active_model.get_active_channel_model(channel_id)
        if active_channel is not None:
          active_sensed_entity = active_channel.sensed_entity_active_model
          measurement_type = active_channel.channel_description.measurement_type
          value = channel_data[Messages.MESSAGE_FIELD_VALUE]
          
          print("Sensor {} channel {} has value {} for {}:{}".format(sensor_id, channel_id, value, active_sensed_entity.sensed_entity_description.external_id, measurement_type))
        else:
          print("Sensor {} has unknown channel {}".format(sensor_id, channel_id))
    else:
      print("Message for unknown sensor with sensor ID {}".format(sensor_id))

    
      
