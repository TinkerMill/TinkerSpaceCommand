#
# Written by keith M. Hughes
#

from rx import Observer

class SensorChannelMeasurementEvent:
    """ A measurement event from a sensor
    """
    def __init__(self, sensor_active_model, sensed_active_model, active_channel, value, time_received):
        self.sensor_active_model = sensor_active_model
        self.sensed_active_model = sensed_active_model
        self.active_channel = active_channel
        self.value = value
        self.time_received = time_received
        
class SensedPrintObserver(Observer):

    def on_next(self, value):
        print("Received sensed {0}".format(value))

    def on_completed(self):
        print("Done!")

    def on_error(self, error):
        print("Error Occurred: {0}".format(error))

class SensorPrintObserver(Observer):

    def on_next(self, value):
        print("Received sensor {0}".format(value))

    def on_completed(self):
        print("Done!")

    def on_error(self, error):
        print("Error Occurred: {0}".format(error))
