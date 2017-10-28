#
# Written by Keith Hughes
#

from TinkerSpaceCommandServer import Messages

class SensorProcessor:
  """The processor that takes sensor messages apart and updates the sensor models.
  """
  
  def __init__(self):
    pass

  def process_sensor_input(self, message, time_received):
    print("Sensor processor got message {} at time {}".format(message, time_received))

    message_type = message[Messages.MESSAGE_FIELD_MESSAGE_TYPE]

    if message_type == Messages.MESSAGE_VALUE_MESSAGE_TYPE_MEASUREMENT:
      self.process_measurement(message, time_received)

  def process_measurement(self, message, time_received):
    sensor_id = message[Messages.MESSAGE_FIELD_SENSOR_ID]

    # Cycle through the data packet, picking up the channel ID and the data
    # from the channel
    for channel_id, channel_data in message[Messages.MESSAGE_FIELD_DATA].items():
      value = channel_data[Messages.MESSAGE_FIELD_VALUE]
      print("Sensor {} channel {} has value {}".format(sensor_id, channel_id, value))

    
      
