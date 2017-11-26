#
# Written by Keith Hughes
#

class EntityDescription:
  """This is the base class for all model descriptions.
  """
  def __init__(self, external_id, name, description):
    self.external_id = external_id
    self.name = name
    self.description = description

class PhysicalLocationEntityDescription(EntityDescription):
  """The model description of a physical space.
  """

  def __init__(self, external_id, name, description):
    EntityDescription.__init__(self, external_id, name, description)

class SensorEntityDescription(EntityDescription):
  """The model description of a sensor.
  """

  def __init__(self, external_id, name, description, sensor_details):
    EntityDescription.__init__(self, external_id, name, description)
    self.sensor_details = sensor_details

    # channel_associations is a map of channel IDs to the sensed item they will
    # be sensing.
    self.channel_associations = {}
    
  def add_channel_association(self, channel_id, sensed):
    """Associate the channel ID with the item being sensed by that channel.
    """
    
    self.channel_associations[channel_id] = sensed

class SensorDetailEntityDescription(EntityDescription):
  """The details of a sensor.
     The details include the details of all the channels.
  """

  def __init__(self, external_id, name, description, channels):
    EntityDescription.__init__(self, external_id, name, description)

    # channels is a map from external IDs of channels to their channel detail.
    self.channels = channels

  def get_channel_detail(self, channel_id):
    """Get the channel detail for a specific channel of the sensor.
    """

    return self.channels[channel_id]

class SensorChannelDetail(EntityDescription):
  """The detail of a channel.
     Useful to be able to override the behavior of a specific channel.

  """

  def __init__(self, external_id, name, description, measurement_type, measurement_unit):
    EntityDescription.__init__(self, external_id, name, description)

    self.measurement_type = measurement_type
    self.measurement_unit = measurement_unit

#
# Active models are the models of things in the space that contain the live
# data as it is happening.
#

class ActiveModel:
  """The base class for all active models.
  """

  def __init__(self):
    pass

class SensorActiveChannelModel:
  """Binding information about a sensor channel and the sensed entity that
     receives the information from the sensor channel.
  """

  def __init__(self, channel_id, channel_description, sensed_entity_active_model):
    self.channel_id = channel_id
    self.channel_description = channel_description
    self.sensed_entity_active_model = sensed_entity_active_model
    
class SensorEntityActiveModel(ActiveModel):
  """The active model for a sensor.
  """
  
  def __init__(self, sensor_entity_description):
    self.sensor_entity_description = sensor_entity_description

    # Map of a channel ID to a SensorActiveChannelModel for the channel
    self.active_channels = {}

  def register_active_channel(self, sensor_active_channel_model):
    """Register an active channel with this sensor model.
    """

    self.active_channels[sensor_active_channel_model.channel_id] = sensor_active_channel_model

  def get_active_channel_model(self, channel_id):
    """Get the active channel by the channel ID.
    """
    
    return self.active_channels[channel_id]
    
class SensedEntityActiveModel(ActiveModel):

  def __init__(self, sensed_entity_description):
    self.sensed_entity_description = sensed_entity_description
  
  
class PhysicalLocationActiveModel(SensedEntityActiveModel):
  """The active model for a physical location.
  """

  def __init__(self, physical_location_description):
    SensedEntityActiveModel.__init__(self, physical_location_description)

