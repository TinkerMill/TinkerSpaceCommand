/*
 Adruino_SpaceNode.h - Library for ESP8266 Arduino Sensor Nodes

 Created by: Steve Lammers, 10/28/2017

 Adapted from the supplied MQTT example by Keith M. Hughes.


  ToDo------------------------
  MDNS
  MQTT
  structure that contains topic names (default names)

  End user provides a 
    - SSID, 
    - sensing node: a topic for data on 
                    supply a method that reads the sensors
                      we provide a method to put the json message toghther
*/

#ifndef SPACENODE
#define SPACENODE

#define MQTT_MAX_PACKET_SIZE 2048

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#define MQTT_MAX_PACKET_SIZE 2048

// SL Note: ToDo
// class NodeSensor
// class NodeHeartbeat
//

class SpaceNode{

  private:
    // Constructor private to ensure singleton instance of object
    SpaceNode();

    // Copy constructor is also private to ensure that the singleton instance
    //  cannot be copied.
    SpaceNode(SpaceNode const&){};

    // Assignment operator is private so the static instance cannot be passed
    //  to a new object.
    SpaceNode& operator=(SpaceNode const&){};

    // Pointer to singleton object used to ensure that only one instance is created
    static SpaceNode* m_pInstance;

    // The MQTT topic for incoming control messages
    const char* m_mqttControlInputTopic;

    // The MQTT topic for outgoing data messages.
    const char* m_mqttDataOutputTopic;

    // The MQTT client ID.
    char m_mqttClientId[64];

    // The hostname for the WIFI client.
    char m_hostname[24];

    // The WIFI client for communicating with the MQTT broker.
    WiFiClient m_wifiClient;

    // The MQTT client
    PubSubClient m_mqttClient;

    // The time between heartbeats, in milliseconds.
    //
    // The default is 1 second = 1000 milliseconds
    long heartbeatTimer = 1000;

    // Set up the MQTT connection.
    void setupMqttConnection();

    // Serialize and send the JSON message
    void sendMqttMessage(JsonObject& jsonRoot);
  
    // The MQTT callback for incoming messages.
    static void processIncomingMqttMessage(char* topic, byte* payload, unsigned int length);

  public:
    // Get the singleton SpaceNode instance.
    //
    // There can only be one SpaceNode object in existance at at time within
    // an Arduino .ino file.
    static SpaceNode* Instance();

    // Deconstructor
    ~SpaceNode();

    // Set up the node.
    //
    // The data output topic gves the MQTT topic for sensor measurements
    // an heartbeats.
    //
    // The control input topic is for messages coming in that will be controlled
    // by this node.
    void setupNode(
      const char* _mqttDataOutputTopic,
      const char* _mqttControlInputTopic);

    // Reconnect the local MQTT client ot the broker.
    void reconnectMqtt();

    // Check the connection of the local MQTT client to the MQTT broker?
    bool isMqttConnected();

    // Handle everything that needs to happen in a loop iteration of the
    // space node.
    void loopNode();

    // Publish a heartbeat message from this node.
    void publishHeartbeat();

    // Publish a sensor measurement that is a float.
    void publishMeasurement(char* channelId, char* measurementType, float measurementValue);

    
    // Publish a sensor measurement that is an integer.
    void publishMeasurement(char* channelId, char* measurementType, int measurementValue);

    
    // Publish a sensor measurement that is a string.
    void publishMeasurement(char* channelId, char* measurementType, char* measurementValue);


};

// Create an instance of the SpaceNode object to use in the Arduino .ino file.
// This way when the SpaceNode.h file is included, the TMNode object is automatically
// created and the user does not need to know the details.
//SpaceNode & TMNode = *SpaceNode::Instance();


#endif //SPACENODE
