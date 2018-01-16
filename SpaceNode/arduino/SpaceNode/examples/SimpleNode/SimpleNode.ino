#include <SpaceNode.h>

//SpaceNode node("/timkermill/sensors/control", wifiClient, mqttClient);
//SpaceNode node("/timkermill/sensors/control");
SpaceNode* node = SpaceNode::Instance();

// The writable pins on the Sparkfun Thing Dev board.
const int WRITABLE_PINS[] = { 0, 2, 4, 5, 12, 13, 14, 15, 16 };

// The number of writable pins
const int NUM_WRITABLE_PINS = sizeof(WRITABLE_PINS) / sizeof(int);

// Set up the WiFi connection.
void setup_wifi(const char* ssid = "TinkerMill", const char* password = "") {

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

  // Output will be sent to the serial monitor at 115200 baud.
  Serial.begin(115200);

  // Set up the WiFi connection to the local network.
  // Update these with values suitable for your network.
  // The SSID of the wireless network to attach to.
  //    ssid = _ssid;
  //#define SSID "TinkerMill"
  // The password for the wireless network.
  //    password = _password;
  setup_wifi();

  node->setupNode("/timkermill/sensors/control");
}

// This function is called over and over again.
//
// It will give the MQTT client a change to process any messages that
// have come in.
void loop() {

  // If not connected to the MQTT broker, either because has
// never been connected or because the connection was lost.
  if (!node->check_connection()) {
    node->reconnect();
  }

  // Have the MQTT client process any data.
  node->loop_node();

  // Wait a second before sampling again.
  delay(1000);
}
