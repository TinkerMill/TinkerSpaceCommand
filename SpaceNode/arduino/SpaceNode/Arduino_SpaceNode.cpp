/*
 ESP8266 MQTT example for driving digital outputs.

 This sketch demonstrates the capabilities of the pubsub library in combination
 with the ESP8266 board/library and digital output.

 It connects to an MQTT server then:
  - subscribes to the topic "/sensors/control", printing out any messages
    it receives. NB - it assumes the received payloads are strings representing hexadecimal longs not binary
  - The bits of the received long are used to turn the digital outputs of the chip on or off.

 It will reconnect to the server if the connection is lost using a blocking
 reconnect function. See the 'mqtt_reconnect_nonblocking' example for how to
 achieve the same result without blocking the main loop.

 To install the ESP8266 board, (using Arduino 1.6.4+):
  - Add the following 3rd party board manager under "File -> Preferences -> Additional Boards Manager URLs":
       http://arduino.esp8266.com/stable/package_esp8266com_index.json
  - Open the "Tools -> Board -> Board Manager" and click install for the ESP8266"
  - Select your ESP8266 in "Tools -> Board"

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


#include "Arduino_SpaceNode.h"


// The writable pins on the Sparkfun Thing Dev board.
const int WRITABLE_PINS[] = { 0, 2, 4, 5, 12, 13, 14, 15, 16 };

// The number of writable pins
const int NUM_WRITABLE_PINS = sizeof(WRITABLE_PINS) / sizeof(int);


// Constructor
SpaceNode::SpaceNode(const char* _ssid = "TinkerMill", const char* _password = "", const char* _mqttControlInputTopic = "/tinkermill/sensors/control"){

  // Update these with values suitable for your network.
  // The SSID of the wireless network to attach to.
  ssid = _ssid;
  //#define SSID "TinkerMill"
  // The password for the wireless network.
  password = _password;
  // The topic to subscribe to.
  mqttControlInputTopic = _mqttControlInputTopic;
  // Run setup method
  setup();
}

// Deconstructor
SpaceNode::~SpaceNode(){\*Nothing to Deconstruct*\};


// Set up the program.
// This function is called once when the program starts.
void SpaceNode::setup() {
  
  // Initialize all chip pins that are meant to be written to as writable.
  for (int pinIndex = 0; pinIndex < NUM_WRITABLE_PINS; pinIndex++) {
    pinMode(WRITABLE_PINS[pinIndex], OUTPUT);
  }

  // Output will be sent to the serial monitor at 115200 baud.
  Serial.begin(115200);

  // Set up the WiFi connection to the local network.
  setup_wifi();

  Serial.print("ESP Chip ID is ");
  Serial.println(ESP.getChipId());

  // Create a host name for the chip.
  sprintf(hostName, "ESP8266_%06X", ESP.getChipId());

  // Create an MQTT client ID likely unique.
  sprintf(mqttClientId, "/esp8266/%s", hostName);

  setup_mqtt_session();
}

// Set up the WiFi connection.
void SpaceNode::setup_wifi() {

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

// Use mDNS to locate an MQTT broker and attach.
void SpaceNode::setup_mqtt_session() {
  if (!MDNS.begin(hostName)) {
    Serial.println("Unable to set up mDNS");
  }

  // Scan until an MQTT broker is found
  while (true) {
    int n = MDNS.queryService("mqtt", "tcp");
    if (n == 0) {
      Serial.println("No MQTT services found.");
    } else {
      Serial.println("Found MQTT");
      Serial.println(MDNS.hostname(0));
      Serial.println(MDNS.IP(0));
      Serial.println(MDNS.port(0));
    
      // Set the MQTT server and port to attach to.
      mqttCient.setServer(MDNS.IP(0), MDNS.port(0));

      // Set the function to be called every time a message comes in.
      mqttCient.setCallback(mqttCallback);

      break;
    }
  }
}

// The function to be called whenever a message comes in on
// the input topic.
void SpaceNode::mqttCallback(char* topic, byte* payload, unsigned int length) {
  
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // The Arduino MQTT library has a fixed internal buffer and will overwrite
  // old payloads with new payloads. If the new payload is shorter than the
  // old payload, the latter part of the old payload will still be visible
  // in the buffer. So null-terminate the string at the length of the new
  // payload to play it safe.
  payload[length] = NULL;

  // Parse the hex string
  long messageBits = strtol((char *)payload, NULL, 16);
  long pinBit = 1;
  Serial.println(messageBits, HEX);

  // For each writable pin, see if that pin should be turned on or off.
  long pinIndex = 0;
  while (pinIndex < NUM_WRITABLE_PINS) {
    int pinNumber = WRITABLE_PINS[pinIndex];
    int pinValue = messageBits & pinBit ? HIGH : LOW;

    Serial.print(pinNumber);
    Serial.print(" => ");
    Serial.println(pinValue);

    digitalWrite(pinNumber, pinValue);

    pinBit <<= 1;
    pinIndex++;
  }
}

// The connection to the MQTT broker has been lost. Try and reconnect.
void SpaceNode::reconnect() {
  // Loop until we're reconnected
  while (!mqttCient.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (mqttCient.connect(mqttClientId)) {
      Serial.println("connected");
      
      // Resubscribe to the control topic.
      mqttCient.subscribe(mqttControlInputTopic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttCient.state());
      Serial.println(" try again in 5 seconds");
      
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

// This function is called over and over again.
//
// It will give the MQTT client a change to process any messages that
// have come in.
//void loop() {
//
//  // If not connected to the MQTT broker, either because has
//  // never been connected or because the connection was lost.
//  if (!mqttCient.connected()) {
//    reconnect();
//  }
//
//  // Have the MQTT client process any data.
//  mqttCient.loop();
//
//  // Wait a second before sampling again.
//  delay(1000);
//}
