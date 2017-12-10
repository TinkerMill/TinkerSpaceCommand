/*
 ESP8266 MQTT example using the DHT22 as a sensor.

 This sketch demonstrates the capabilities of the pubsub library in combination
 with the ESP8266 board/library and the DHT sensor library.

 It connects to an MQTT server then:
  - publishes the temperature and humidity from the DHT22 to the topic
    "/sensors/data" every two seconds
  - subscribes to the topic "/sensors/control", printing out any messages
    it receives. NB - it assumes the received payloads are strings not binary
  - If the first character of the topic "/sensors/control" is an 1, switch ON the ESP Led,
    else switch it off

 It will reconnect to the server if the connection is lost using a blocking
 reconnect function. See the 'mqtt_reconnect_nonblocking' example for how to
 achieve the same result without blocking the main loop.

 To install the ESP8266 board, (using Arduino 1.6.4+):
  - Add the following 3rd party board manager under "File -> Preferences -> Additional Boards Manager URLs":
       http://arduino.esp8266.com/stable/package_esp8266com_index.json
  - Open the "Tools -> Board -> Board Manager" and click install for the ESP8266"
  - Select your ESP8266 in "Tools -> Board"

  Adapted from the supplied MQTT and DHT22 examples by Keith M. Hughes.
*/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

// Update these with values suitable for your network.

const char* ssid = "TinkerMill";
const char* password = "";
const char* mqttServerHost = "10.2.0.33";
const int mqttServerPort = 1883;

// The following describe the MQTT topics and client ID.

// The ID the MQTT client should have.
//
// This should have something unique, like your name, e.g.
// sensor_keith
const char* mqttClientId = "sensor_myClientId";

// The topic to publish sensor data on.
//
// This must be the same topic found in the Python program.
//
// Add on something onto the topic to make it unique, e.g.
// /keith/sensors/data
const char* mqttSensorOutputTopic = "/sensors/data";

// The topic to subscribe to for control.
//
// Add on something onto the topic to make it unique, e.g.
// /keith/sensors/control
const char* mqttControlInputTopic = "/sensors/control";

// The type of DHT sensor being used.
#define DHTTYPE DHT22

// The pin on the Sparkfun Thing that the DHT signal wire is attached to.
#define DHTPIN  4

// The WiFi client used to connect to the wireless network.
WiFiClient wifiClient;

// The MQTT Pub/Sub client
PubSubClient mqttClient(wifiClient);

// Initialize DHT sensor 
// NOTE: For working with a faster than ATmega328p 16 MHz Arduino chip, like an ESP8266,
// you need to increase the threshold for cycle counts considered a 1 or 0.
// You can do this by passing a 3rd parameter for this threshold.  It's a bit
// of fiddling to find the right value, but in general the faster the CPU the
// higher the value.  The default for a 16mhz AVR is a value of 6.  For an
// Arduino Due that runs at 84mhz a value of 30 works.
//
// 11 works fine for ESP8266 
DHT dht(DHTPIN, DHTTYPE, 30); 

// Set up the program.
//
// This function is called once when the program starts.
void setup() {
  
  // Initialize the BUILTIN_LED pin as an output
  pinMode(BUILTIN_LED, OUTPUT);

  // Output will be sent to the serial monitor at 115200 baud.
  Serial.begin(115200);

  // Initialize the DHT sensor.
  dht.begin();

  // Set up the WiFi connection to the local network.
  setup_wifi();

  // Set the MQTT server and port to attach to.
  mqttClient.setServer(mqttServerHost, mqttServerPort);

  // Set the function to be called every time a message comes in.
  mqttClient.setCallback(mqttCallback);
}

// Set up the WiFi connection.
void setup_wifi() {

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

// The function to be called whenever a message comes in on
// the input topic.
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is acive low on the ESP-01)
    digitalWrite(BUILTIN_LED, LOW);   
  } else {
    // Turn the LED off by making the voltage HIGH
    digitalWrite(BUILTIN_LED, HIGH); 
  }
}

// The connection to the MQTT broker has been lost. Try and reconnect.
void mqttReconnect() {
  // Loop until we're reconnected
  while (!mqttClient.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (mqttClient.connect(mqttClientId)) {
      Serial.println("connected");
      
      // Resubscribe to the control topic.
      mqttClient.subscribe(mqttControlInputTopic);
    } else {
      Serial.print("failed, return code=");
      Serial.print(mqttClient.state());
      Serial.println(" try again in 5 seconds");
      
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

// This function is called over and over again.
//
// It will give the MQTT client a change to run, read the sensor,
// and publish the temperature and humidy over the MQTT channel.
void loop() {

  // If not connected to the MQTT broker, either because has
  // never been connected or because the connection was lost.
  if (!mqttClient.connected()) {
    mqttReconnect();
  }

  // Have the MQTT client process any data.
  mqttClient.loop();

  // read the temperature and humidy from the DHT.
  // The DHT gives the humidity as relative humidity as a percent.
  float humidity = dht.readHumidity();

  // The true means read the temperature in fahrenheit.
  float temp_f = dht.readTemperature(true);
  
  // Check if any reads failed and exit early (to try again).
  //
  // The values will be Not a Number (NaN) if the values cannot be read.
  if (isnan(humidity) || isnan(temp_f)) {
    Serial.println("Failed to read from DHT sensor!");

    // Wait a second before retry.
    delay(1000);
    
    return;
  }

  // Encode the message in JSON.

  // First create the JSON object.
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();

  // Put the data into the JSON object.
  root["sensor"] = String(ESP.getChipId());

  // -----------------------------------
  // Place temperature and humidity into the JSON object here.
  // -----------------------------------

  // Write out the message for debugging.
  root.printTo(Serial);

  // Turn the JSON structure into a string for sending over the MQTT topic.
  char jsonOutputBuffer[512];
  root.printTo(jsonOutputBuffer, sizeof(jsonOutputBuffer));
  Serial.println();

  // Publish the message on the MQTT topic.
  mqttClient.publish(mqttSensorOutputTopic, jsonOutputBuffer);

  // Wait 5 seconds before sampling again.
  delay(5000);
}
