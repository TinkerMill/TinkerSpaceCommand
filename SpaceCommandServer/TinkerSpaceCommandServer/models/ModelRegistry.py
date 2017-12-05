#
# This component has a series of classes that support creating a registry
# of all sensors, physical locations, and everything they do in the space.
#
# Written by Keith Hughes
#

import pdb
from . import Models
import yaml

class EntityRegistry:
  def __init__(self):

    # Map of sensor detail entities keyed by their external ID
    self.sensor_details = {}

    # Map of sensor entities keyed by their external ID
    self.sensors = {}

    # Map of sensed entities keyed by their external ID
    self.sensed_entities = {}

    # Map of active models for sensed entities keyed by their external ID
    self.sensed_entity_active_models = {}

    # Map of active models for sensor entities keyed by their external ID
    self.sensor_entity_active_models = {}

  def add_sensor_detail(self, sensor_detail_entity):
    """Add in a new sensor detail entity to the registry.
    """

    self.sensor_details[sensor_detail_entity.external_id] = sensor_detail_entity

  def add_sensor(self, sensor_entity):
    """Add in a new sensor entity to the registry.
    """

    self.sensors[sensor_entity.external_id] = sensor_entity

  def add_sensed_entity(self, sensed_entity):
    """Add in a new sensed entity into the registry.
    """

    self.sensed_entities[sensed_entity.external_id] = sensed_entity

  def register_sensor_association(self, sensor, channel_ids, sensed):
    """Associate the list of channel IDs for the sensor with the
       item being sensed by those channels.
    """

    for channel_id in channel_ids:
      sensor.add_channel_association(channel_id, sensed)

  def prepare_runtime_models(self):
    """Prepare all the runtime models needed for all entities.
    """

    for sensed_entity_key in self.sensed_entities:
      sensed_entity = self.sensed_entities[sensed_entity_key]

      if type(sensed_entity).__name__ == "PhysicalLocationEntityDescription":
        active_model = Models.PhysicalLocationActiveModel(sensed_entity)
        
      self.sensed_entity_active_models[sensed_entity_key] = active_model

    for sensor_key in self.sensors:
      sensor = self.sensors[sensor_key]

      sensor_active_model = Models.SensorEntityActiveModel(sensor)
      self.sensor_entity_active_models[sensor_key] = sensor_active_model
      
      sensor_details = sensor.sensor_details
      
      for channel_id, sensed_item in sensor.channel_associations.items():
        sensed_active_model = self.sensed_entity_active_models[sensed_entity.external_id]
        channel_detail = sensor_details.get_channel_detail(channel_id)
        channel_active_model = Models.SensorActiveChannelModel(channel_id, channel_detail, sensed_active_model)

        sensor_active_model.register_active_channel(channel_active_model)

  def get_sensor_active_model(self, sensor_id):
    """Get the sensor active model associated with a given sensor ID.
    """

    return self.sensor_entity_active_models.get(sensor_id, None)

class YamlEntityRegistryReader:
  """An entity registry reader that uses YAML as the file format.
  """

  def __init__(self):
    pass

  def load_registry(self, sensor_description_file_path, entity_registry):
    with open(sensor_description_file_path) as fp:
      descriptions = yaml.safe_load(fp)

      pdb.set_trace()

      self.read_sensor_details(descriptions, entity_registry)
      self.read_sensor_descriptions(descriptions, entity_registry)
      self.read_physical_location_descriptions(descriptions, entity_registry)
      self.read_sensor_associations(descriptions, entity_registry)

  def read_sensor_details(self, descriptions, entity_registry):
    """Read the sensor details entities from the entity descriptions.
    """
    
    for detail in descriptions["sensorDetails"]:
      external_id = detail["externalId"]
      name = detail["name"]
      description = detail["description"]

      channels = self.read_channel_details(detail)

      pdb.set_trace()

      entity_registry.add_sensor_detail(Models.SensorDetailEntityDescription(external_id, name, description, channels))

  def read_channel_details(self, sensor_detail):
    """Read the channel details from a sensor detail description.
       Returns a map of channel IDs to the channel detail.
    """

    channels = {}
    for detail in sensor_detail["channels"]:
      external_id = detail["externalId"]
      name = detail["name"]
      description = detail["description"]
      measurement_type = detail["measurementType"]
      measurement_unit = detail["measurementUnit"]

      channels[external_id] = Models.SensorChannelDetail(external_id, name, description, measurement_type, measurement_unit)

    return channels
  
  def read_sensor_descriptions(self, descriptions, entity_registry):
    """Read the sensor entities from the entity descriptions.
    """
    
    for detail in descriptions["sensors"]:
      external_id = detail["externalId"]
      name = detail["name"]
      description = detail["description"]

      sensor_detail_id = detail["sensorDetail"]
      sensor_detail = entity_registry.sensor_details[sensor_detail_id]

      if sensor_detail:
        entity_registry.add_sensor(Models.SensorEntityDescription(external_id, name, description, sensor_detail))
      else:
        print("Sensor {} could not find sensor detail {}".format(external_id,  sensor_detail_id))
      
  def read_physical_location_descriptions(self, descriptions, entity_registry):
    for detail in descriptions["physicalLocations"]:
      external_id = detail["externalId"]
      name = detail["name"]
      description = detail["description"]

      entity_registry.add_sensed_entity(Models.PhysicalLocationEntityDescription(external_id, name, description))

  def read_sensor_associations(self, descriptions, entity_registry):
    for detail in descriptions["sensorAssociations"]:
      sensor_id = detail["sensorId"]
      sensed_id = detail["sensedId"]

      sensor = entity_registry.sensors[sensor_id]
      sensed = entity_registry.sensed_entities[sensed_id]

      channel_ids = detail.get("channelIds", "*")
      if channel_ids == "*":
        channel_ids = list(sensor.sensor_details.channels.keys())
      else:
        channel_ids = channel_ids.split(":")

      entity_registry.register_sensor_association(sensor, channel_ids, sensed)

