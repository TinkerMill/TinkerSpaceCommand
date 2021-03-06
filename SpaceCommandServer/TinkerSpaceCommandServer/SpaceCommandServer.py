#
# Written by Keith M. Hughes
#

import signal
import sys
from TinkerSpaceCommandServer.webapp import WebAppServer

class SpaceCommandServer:
  """The tinkermill space command server takes communication from a variety of 
     communication providers and routes sensor information to the proper sensor
     processors.
  """
  
  def __init__(self, config):
    self.config = config

    self.communicationProviders = []

    self.sensor_processor = None
    self.event_persistence = None
    self.webapp = WebAppServer.WebAppServer(__name__, self)
    
  def start(self):
    print("Starting Tinker Space Command Server")

    self.sensor_processor.start()
    
    for provider in self.communicationProviders:
      provider.sensor_processor = self.sensor_processor
      provider.start()

    self.webapp.start()
    
    # Set the ^C handler.
    signal.signal(signal.SIGINT, self.signal_handler)

  def stop(self):
    print("Stopping Tinker Space Command Server")

    for provider in self.communicationProviders:
      provider.stop()

    self.sensor_processor.stop()

  def addCommunicationProvider(self, provider):
    """Add in a new communication provider to the server.
    """
    
    self.communicationProviders.append(provider)

    
  def signal_handler(self, signal, frame):
    """Signal handler for sigint.

       This is used to catch ^C to the client and will do any needed cleanup, 
       for example, shut down the connection to the MQTT broker.
    """
    self.stop()
  
    # Exit the program completely.
    sys.exit(0)

