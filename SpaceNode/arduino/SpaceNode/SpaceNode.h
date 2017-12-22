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


class SpaceNode{

  private:
    const char* m_mqttControlInputTopic;
    char m_mqttClientId[64];
    char m_hostname[24];
    WiFiClient m_wifiClient;
    PubSubClient m_mqttClient;
    //int* static_writablePins;
    //int static_numWritablePins;


  public:
    // 
    //SpaceNode(const char* _mqttControlInputTopic, WiFiClient _wifiClient, PubSubClient _mqttClient);
    SpaceNode(const char* _mqttControlInputTopic);
    // Deconstructor
    ~SpaceNode();

    void setupNode();
    void setup_mqtt_session();
    static void mqttCallback(char* topic, byte* payload, unsigned int length);
    //void mqttCallback(char* topic, byte* payload, unsigned int length);
    //void mqttCallback(char* topic, byte* payload, unsigned int length);
    //void mqttCallback(char* topic, uint8_t* payload, unsigned int length);
    void reconnect();
    bool check_connection();
    void loop_node();

};



#endif //SPACENODE
