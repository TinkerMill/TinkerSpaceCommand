#
# This component has a series of classes that support creating a registry
# of all sensors, physical locations, and everything they do in the space.
#
# Written by Keith Hughes
#

class EntityRegistry:
  def __init__(self):

    # Map of sensor entities keyed by their external ID
    self.sensors = {}

    # Map of sensed entities keyed by their external ID
    self.sensed_entities = {}

  def add_sensor(self, sensor_entity):
    """Add in a new sensor entity to the registry.
    """

    self.sensors[sensor_entity.external_id] = sensor_entity

  def add_sensed_entity(self, sensed_entity):
    """Add in a new sensed entity into the registry.
    """

class YamlEntityRegistryReader:
  """An entity registry reader that uses YAML as the file format.
  """

  def __init__(self):
    pass

  def load_registry(self, sensor_description_file_path, entity_registry):
    with open(sensor_description_file_path) as fp:
      descriptions = yaml.safe_load(fp)

      self.read_sensor_descriptions(descriptions, entity_registry)
      self.read_physical_location_descriptions(descriptions, entity_registry)

  def read_sensor_descriptions(self, descriptions, entity_registry):
    for sensor_description in descriptions["sensors"]:
      external_id = sensor_description["externalId"]
      name = sensor_description["name"]
      description = sensor_description["description"]

      sensor_detail = sensor_description["sensorDetail"]
      
  def read_physical_location_descriptions(self, descriptions, entity_registry):


  
