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

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

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
    //
    const char* m_mqttControlInputTopic;
    char m_mqttClientId[64];
    char m_hostname[24];
    WiFiClient m_wifiClient;
    PubSubClient m_mqttClient;
    //int* static_writablePins;
    //int static_numWritablePins;
    //
    int heartbeatTimer = 1000; // default 1s
    //void heartbeat();


  public:
    // 
    //SpaceNode(const char* _mqttControlInputTopic);
    // Instance method returns a static pointer to the SpaceNode object
    //  This ensures only one instance is created for the class
    //  i.e. there can only be one SpaceNode object in existance at at time within
    //  an Arduino .ino file.
    static SpaceNode* Instance();
    // Deconstructor
    ~SpaceNode();

    void setupNode(const char* _mqttControlInputTopic);
    void setup_mqtt_session();
    static void mqttCallback(char* topic, byte* payload, unsigned int length);
    //void mqttCallback(char* topic, byte* payload, unsigned int length);
    //void mqttCallback(char* topic, byte* payload, unsigned int length);
    //void mqttCallback(char* topic, uint8_t* payload, unsigned int length);
    void reconnect();
    bool check_connection();
    void loop_node();

 

};

// Create an instance of the SpaceNode object to use in the Arduino .ino file.
// This way when the SpaceNode.h file is included, the TMNode object is automatically
// created and the user does not need to know the details.
//SpaceNode & TMNode = *SpaceNode::Instance();


#endif //SPACENODE
