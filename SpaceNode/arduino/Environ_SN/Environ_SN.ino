
/***************************************************************************
  This is a library for the Environmental SpaceNode Sensor 

  This sketch reads the dual environmental sensor sold by Sparkfun
    ----> https://www.sparkfun.com/products/14348

  The CCS811 chip needs to have the jumper soldered closed so that
  the address is 0x76, as is required by the Adafruit library.
  ----> http://www.adafruit.com/products/3566

  Written by Steve Lammers for Tinkermill, some code adapted from 
  included library example code.

  Exact licence unknown due to included libraries.
 ***************************************************************************/
#include <SpaceNode.h>
#include "TimeCheck.h"
#include "Wire.h"
#include "Adafruit_CCS811.h"
#include "SparkFunBME280.h"

Adafruit_CCS811 ccs;
BME280 mySensor; //Global sensor object

SpaceNode& TMNode = *SpaceNode::Instance();

// The writable pins on the Sparkfun Thing Dev board.const int WRITABLE_PINS[] = { 0, 2, 4, 5, 12, 13, 14, 15, 16 };

// The number of writable 
const int NUM_WRITABLE_PINS = sizeof(WRITABLE_PINS) / sizeof(int);

// Create heartbeat clock
TimeCheck heartbeatClock((unsigned long)millis(), (unsigned long)1000);

// Set up the WiFi connection.
void setup_wifi(const char* ssid = "TinkerMill", const char* password = "password") {

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

  Serial.println("Wifi Setup Exited................................");

  TMNode.setupNode("/timkermill/sensors/data");


  // <<------------------------>> Setup CCS811 >>------------------------->>
  Serial.println("CCS811 test");
  
  if(!ccs.begin()){
    Serial.println("Failed to start sensor! Please check your wiring.");
    while(1);
  }
  //calibrate temperature sensor
  while(!ccs.available());
  float temp = ccs.calculateTemperature();
  ccs.setTempOffset(temp - 25.0);
  // <<------------------------<< Setup CCS811 <<-------------------------<<

  // <<------------------------>> Setup BMD280 >>------------------------->>
  while(!Serial);
  Serial.println("Reading basic values from BME280");

  // Wire has already started from the CCS811 setup. If this library was not 
  // included then the following line would need to be uncommented.
  //Wire.begin();

  if (mySensor.beginI2C() == false) //Begin communication over I2C
  {
    Serial.println("The chip did not respond. Please check wiring.");
    while(1); //Freeze
  }
  // <<------------------------<< Setup BMD280 <<-------------------------<<


} // end Setup



// This function is called over and over again.
//
// It will give the MQTT client a change to process any messages that
// have come in.
void loop() {
  // loop_node method must be called once per loop for proper node operation
  //Serial.println("Enter loop_node");
  TMNode.loop_node();
  //Serial.println("Exit loop_node");

  // Send heartbeat if enough time has elapsed
  if (heartbeatClock.check_trigger( (unsigned long)millis() )){
    Serial.print("Heartbeat Time: ");
    Serial.println(millis());
    TMNode.publish_heartbeat();
  }
}
