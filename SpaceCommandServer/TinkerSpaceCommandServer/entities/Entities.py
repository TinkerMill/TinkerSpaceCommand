#
# The entities for TinkerSpaceCommandServer that are sensors and things
# that are sensed, e.g. physical locations.

#
# Written by Keith Hughes
#

from rx.subjects import Subject
import time

#
# Subclasses of EntityDescription are static descriptions of the entities in
# TinkerSpaceCommandServer. They describe the names and descriptions, the
# capabilities of sensors, etc.
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

  def __init__(self, external_id, name, description, sensor_details, sensor_update_time_limit, sensor_heartbeat_time_limit):
    EntityDescription.__init__(self, external_id, name, description)
    self.sensor_details = sensor_details

    self.sensor_update_time_limit = sensor_update_time_limit
    self.sensor_heartbeat_time_limit = sensor_heartbeat_time_limit

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

  def __init__(self, external_id, name, description, sensor_update_time_limit, sensor_heartbeat_time_limit, channels):
    EntityDescription.__init__(self, external_id, name, description)

    # channels is a map from external IDs of channels to their channel detail.
    self.channels = channels

    # the time limit, in seconds, that we expect to see a sensor value update,
    # if any.
    self.sensor_update_time_limit = sensor_update_time_limit
    
    # the time limit, in seconds, that we expect to see a sensor heartbeat.
    self.sensor_heartbeat_time_limit = sensor_heartbeat_time_limit
    
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
# data as it is happening. There are active models for sensors, things that
# are sensed, etc.
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

  def __init__(self, channel_id, channel_description,
               sensor_entity_active_model, sensed_entity_active_model):
    self.channel_id = channel_id
    self.channel_description = channel_description
    self.sensed_entity_active_model = sensed_entity_active_model
    self.sensor_entity_active_model = sensor_entity_active_model
    
    self.sensor_entity_active_model.register_active_channel(self)
    self.sensed_entity_active_model.register_active_channel(self)

    self.current_value = None
    
  def update_current_value(self, new_value, time_received):
    """Update the current value for the channel.

       This will also trigger signalling value update events for both the sensor
       and the sensed entity.
    """
    
    self.current_value = new_value

    self.sensor_entity_active_model.value_update_received(self, time_received)
    self.sensed_entity_active_model.value_update_received(self, time_received)

class SensorEntityActiveModel(ActiveModel):
  """The active model for a sensor.
  """
  
  def __init__(self, sensor_entity_description):
    self.sensor_entity_description = sensor_entity_description

    # Map of a channel ID to a SensorActiveChannelModel for the channel
    self.active_channels = {}

    self.sensor_value_update_subject = Subject()

    self._item_creation_time = time.time()

    self.value_last_time_received = None
    self.heartbeat_last_time_received = None

    # Offline until proven otherwise
    self._online = False

    self.value_update_time_limit = sensor_entity_description.sensor_update_time_limit
    self.heartbeat_update_time_limit = sensor_entity_description.sensor_heartbeat_time_limit
    self._last_update_time = None
    self.offline_signaled = False

  def register_active_channel(self, sensor_active_channel_model):
    """Register an active channel with this sensor model.
    """

    self.active_channels[sensor_active_channel_model.channel_id] = sensor_active_channel_model
    
  def get_active_channel_model(self, channel_id):
    """Get the active channel by the channel ID.
    """
    
    return self.active_channels.get(channel_id)

  def register_value_update_observer(self, observer):
    """Register an observer interested in sensor value update events.
    """
    self.sensor_value_update_subject.subscribe(observer)

  def value_update_received(self, active_channel, time_received):
    """A measurement message has been received.

       The sensor is not guaranteed to have received the channel values yet.
    """
    
    self.offline_signaled = False
    self.value_last_time_received = time_received
        
    self.sensor_value_update_subject.on_next(active_channel)

  def heartbeat_received(self, time_received):
    """A heartbeat message has been received.
    """

    self.offline_signaled = False
    self.heartbeat_last_time_received = time_received

  def check_if_offline_transition(self, current_time):

    # Only check if the model thinks it is online and there was an update time,
    # otherwise we want the initial 
    if self._online:
      if self.value_update_time_limit is not None:
        # The only way we would ever be considered online is if there has been a
        # value update, so it will not be None
        self._online = not self.is_timeout(current_time, self.value_last_time_received, self.value_update_time_limit)
      elif self.heartbeat_update_time_limit is not None:
        # If this sensor requires a heartbeat, the heartbeat time can be
        # checked.

        # Calculate the update time to use in the timeout calculation.
        if self._value_last_time_received is not Null:
            if self._heartbeat_last_time_received is not Null:
              update_to_use = max(self.value_last_time_received, self.heartbeat_last_time_received)
            else:
              update_to_use = self.value_last_time_received
        else:
            update_to_use = self.heartbeat_last_time_received
            
        self._online = not self.is_timeout(current_time, update_to_use, self.heartbeat_update_time_limit)

      # We knew online was true, so if now offline, then transitioned.
      if not self._online:
        self.signal_offline(current_time)

      return not self._online
    else:
      # Now, we are considered offline. If we have never been updated then we can check at the
      # time of birth of the model. otherwise no need to check.
      if not self.offline_signaled:
        if self.value_update_time_limit is not None:
          if self.value_last_time_received is not None:
            update_to_use = self.value_last_time_received
          else:
            update_to_use = self._item_creation_time
          
          if self.is_timeout(current_time, update_to_use, self.value_update_time_limit):
            self.signal_offline(current_time)

            return True
          else:
            return False
        elif self.heartbeat_update_time_limit is not None:
          # If this sensor requires a heartbeat, the heartbeat time can be checked.
          if self.heartbeat_last_time_received is not None:
            update_to_use = self.heartbeat_last_time_received
          else:
            update_to_use = self._item_creation_time
            
          if self.is_timeout(current_time, update_to_use, self.heartbeat_update_time_limit):
            self.signal_offline(current_time)

            return True
          else:
            return False
        else:
          return False
      else:
        False

  def is_timeout(self, current_time, reference_time, time_limit):
    return current_time - reference_time > time_limit

  def signal_offline(self, current_time):
    self.offline_signaled = True
    print("Sensor {0} offline at {1}".format(self.sensor_entity_description.name, current_time))

class SensedEntityActiveModel(ActiveModel):
  """The base active model for a sensed entity.
  """
  
  def __init__(self, sensed_entity_description):
    self.sensed_entity_description = sensed_entity_description

    # A map of measurement types to the active channel that gives that
    # type.
    self.active_channels = {}

    self.sensed_value_update_subject = Subject()
    
  def register_active_channel(self, active_channel):
    self.active_channels[active_channel.channel_description.measurement_type] = active_channel
    
  def show_values(self):
    for measurement_type, active_channel in self.active_channels.items():
      print("Sensed entity {} has value of {} for measurement type {}".
            format(self.sensed_entity_description.name,
                   active_channel.current_value,
                   measurement_type))

  def value_update_received(self, active_channel, time_received):
    """Signal to everyone who cares that there has been a value update.
    """
    
    self.sensed_value_update_subject.on_next(active_channel)

  def register_value_update_observer(self, observer):
    """Register an observer interested in sensed value update events.
    """
    self.sensed_value_update_subject.subscribe(observer)

    
class PhysicalLocationActiveModel(SensedEntityActiveModel):
  """The active model for a physical location.
  """

  def __init__(self, physical_location_description):
    SensedEntityActiveModel.__init__(self, physical_location_description)

