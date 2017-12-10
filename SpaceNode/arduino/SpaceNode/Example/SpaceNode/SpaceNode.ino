#include <Arduino_SpaceNode.h>

SpaceNode nodeA;

void setup(){/*Nothing to setup*/};

void loop(){

  // If not connected to the MQTT broker, either because has
  // never been connected or because the connection was lost.
  if (!nodeA.mqttCient.connected()) {
    nodeA.reconnect();
  }

  // Have the MQTT client process any data.
  nodeA.mqttCient.loop();

  // Wait a second before sampling again.
  delay(1000);
}
