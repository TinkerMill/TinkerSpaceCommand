/*
 DHTSensor
  Humidity and temperature sensor for tinkermill TinkerSpace 

 It connects to an MQTT server then:
  - publishes "hello world" to the topic "outTopic" every two seconds
  - subscribes to the topic "inTopic", printing out any messages
    it receives. NB - it assumes the received payloads are strings not binary
  - If the first character of the topic "inTopic" is an 1, switch ON the ESP Led,
    else switch it off

 It will reconnect to the server if the connection is lost using a blocking
 reconnect function. See the 'mqtt_reconnect_nonblocking' example for how to
 achieve the same result without blocking the main loop.

 To install the ESP8266 board, (using Arduino 1.6.4+):
  - Add the following 3rd party board manager under "File -> Preferences -> Additional Boards Manager URLs":
       http://arduino.esp8266.com/stable/package_esp8266com_index.json
  - Open the "Tools -> Board -> Board Manager" and click install for the ESP8266"
  - Select your ESP8266 in "Tools -> Board"

*/
#include <SpaceNode.h>
#include "TimeCheck.h"
#include <DHT.h>

// Node instance, takes care of communication, attaching to network
SpaceNode& DHTNode = *SpaceNode::Instance();

// The writable pins on the Sparkfun Thing Dev board.
const int WRITABLE_PINS[] = { 0, 2, 4, 5, 12, 13, 14, 15, 16 };

// The number of writable pins
const int NUM_WRITABLE_PINS = sizeof(WRITABLE_PINS) / sizeof(int);

// Create heartbeat clock
////TimeCheck heartbeatClock((unsigned long)millis(), (unsigned long)DHTNode.heartbeatTimer);
TimeCheck heartbeatClock((unsigned long)millis(), (unsigned long)20000);

// Setup the Digital Humidity Temperature Sensor (DHT)
#define DHTTYPE DHT22
#define DHTPIN  4

// Initialize DHT sensor 
// NOTE: For working with a faster than ATmega328p 16 MHz Arduino chip, like an ESP8266,
// you need to increase the threshold for cycle counts considered a 1 or 0.
// You can do this by passing a 3rd parameter for this threshold.  It's a bit
// of fiddling to find the right value, but in general the faster the CPU the
// higher the value.  The default for a 16mhz AVR is a value of 6.  For an
// Arduino Due that runs at 84mhz a value of 30 works.
// This is for the ESP8266 processor on ESP-01 
DHT dht(DHTPIN, DHTTYPE, 11); // 11 works fine for ESP8266

// Set up the WiFi connection.
void setupWifi(const char* ssid = "TinkerMill", const char* password = "password") {

  // A slight delay is useful to make sure everything is fully
  // initialized on the chip and board.
  delay(10);
  
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  // Loop until actually connected to the WiFi, waiting half a second
  // between retries.
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void setup(){
  // Initialize all chip pins that are meant to be written to as writable.
  for (int pinIndex = 0; pinIndex < NUM_WRITABLE_PINS; pinIndex++) {
    pinMode(WRITABLE_PINS[pinIndex], OUTPUT);
  }

  // Initialize the BUILTIN_LED pin as an output
  pinMode(BUILTIN_LED, OUTPUT);

  // Output will be sent to the serial monitor at 115200 baud.
  Serial.begin(115200);

  dht.begin();

  // Set up the WiFi connection to the local network.
  // Update these with values suitable for your network.
  setupWifi();

  Serial.println("Wifi Setup Exited................................");

  // Tell the node the MQTT topics for sending the data out on and
  // for incoming 
  DHTNode.setupNode(
    "/tinkermill/sensors/data", 
    "/tinkermill/sensors/control");
}

// This function is called over and over again.
//
// It will give the MQTT client a chance to process any messages
// that have come in.
void loop() {
  // loopNode method must be called once per loop for proper 
  // node operation. It sends and receives MQTT data.
  DHTNode.loopNode();

  // Send heartbeat if enough time has elapsed
  if (heartbeatClock.check_trigger( (unsigned long)millis() )){
    Serial.print("Heartbeat Time: ");
    Serial.println(millis());
    DHTNode.publishHeartbeat();
  }
  
  // Measure DHT and send data.
  // humidity is percent relative humidity.
  // temperature is in Fahrenheit
  float humidity = dht.readHumidity();
  float temp_f = dht.readTemperature(true); 
  
  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity) || isnan(temp_f)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Publish the new data.
  DHTNode.publishMeasurement("temperature", "temperature", temp_f);
  DHTNode.publishMeasurement("humidity", "humidity", humidity);

  delay(5000);
}

