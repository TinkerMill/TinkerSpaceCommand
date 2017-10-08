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

class SensorDetailEntityDescription(EntityDescription):
  """The details of a sensor.
     The details include the details of all the channels.
  """

  def __init__(self, external_id, name, description, channels):
    EntityDescription.__init__(self, external_id, name, description)

    # channls is a map from external IDs of channels to their channel detail.
    self.channels = channels

class SensorChannelDetail(EntityDescription):
  """The detail of a channel.
  """

  def __init__(self, external_id, name, description, measurement_type, measurement_unit):
    EntityDescription.__init__(self, external_id, name, description)

    self.measurement_type = measurement_type
    self.measurement_unit = measurement_unit

