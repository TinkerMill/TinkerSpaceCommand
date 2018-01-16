#
# Written by keith M. Hughes
#

from rx import Observer

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
