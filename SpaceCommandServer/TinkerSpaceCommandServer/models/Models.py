#
# Written by Keith Hughes
#

class ModelDescription:
  """This is the base class for all model descriptions.
  """
  def __init__(self, external_id, name, description):
    self.external_id = external_id
    self.name = name
    self.description = description

class PhysicalLocationModelDescription(ModelDescription):
  """The model description of a physical space.
  """

  def __init__(self, external_id, name, description):
    ModelDescription.__init__(self, external_id, name, description)

class SensorModelDescription(ModelDescription):
  """The model description of a sensor.
  """

  def __init__(self, external_id, name, description):
    ModelDescription.__init__(self, external_id, name, description)

    
  
