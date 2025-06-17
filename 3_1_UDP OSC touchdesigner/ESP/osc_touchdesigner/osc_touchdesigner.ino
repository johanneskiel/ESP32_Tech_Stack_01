
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 3_1_UDP OSC touchdesigner:
// ESP32 communication via UDP/OSC (Open Sound Control). 
// Fast real-time communication for TouchDesigner program.
// 
// hands on (OPTIONAL! We will all do this together on one laptop):
//    - If TouchDesigner is installed on your laptop: open the TouchDesigner project
//    - Open a UDP port in the "servercell" for your laptop
//    - Change the port in the OSCin CHOP to the opened port
//    - Turn the potentiometer and observe how the values in the OSCin CHOP change in TouchDesigner
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////



// Include necessary libraries:
// Wifi:
#include <WiFi.h>
// UDP:
#include <WiFiUdp.h>
// OSC:
#include <OSCMessage.h>


// Defines the GPIO pin number in the code.
const int LED_PIN = 2;
const int POTI_PIN = 32;

// Defines name and password of the router
const char* ssid = "servercell";
const char* password = "qwer1234";

// Defines touchdesigner IP and Port
const char* touchdesigner_ip = "192.168.10.136";  
int touchdesigner_port = 12345;

// Defines local port
int local_port = 8888; 

// Defines UDP object for communication
WiFiUDP udp;


// setup() starts automatically as soon as the ESP32 is powered.
void setup() {
  // start the Serial Monitor with Baudrate: 115200 bits per second
  Serial.begin(115200);
  // Sets the respective GPIO pin mode: Input = receive values, Output = send values.
  pinMode(LED_PIN, OUTPUT);
  pinMode(POTI_PIN, INPUT);
  
  // start the internet connection with name and password of the router
  WiFi.begin(ssid, password);
  // loops as long as not (!=) connected
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("connecting...");
  }
  // show the ESP32-IP in the serial monitor
  Serial.println(WiFi.localIP());
  
  // if connected to wifi: 
  if (WiFi.status() == WL_CONNECTED) {
    // start UDP and bind to local port
    udp.begin(local_port);
  } else {
    Serial.println("offline");
    ESP.restart();
  }
}


// after setup(), loop() starts automatically and repeats infinitely (until the ESP32 loses power)
void loop() {
  send_osc();
  delay(100);  
}


// function that sends the measured and smoothed potentiometer value to touchdesigner
void send_osc() {

  // creates a message with the address “/poti”
  OSCMessage msg("/poti");
  // adds the measured potentiometer value to the message
  msg.add(smooth_poti_value());
  
  // sends the message and then empties it
  udp.beginPacket(touchdesigner_ip, touchdesigner_port);
  msg.send(udp);
  udp.endPacket();
  msg.empty();
  
}



// function that returns the measured, smoothed and normalized potentiometer value
float smooth_poti_value(){

  // smoothing: measure 1000 times and then calculate the average
  int poti_value = 0;
  for (int i = 0; i < 1000; i++) {
    poti_value += analogRead(POTI_PIN);
  }
  poti_value = poti_value / 1000;

  // normalizing: Changes the value to a number between 0 and 1 with 3 decimal places
  float poti_normalized = poti_value / 4095.0;  
  poti_normalized = round(poti_normalized * 1000) / 1000.0; 
    
  Serial.println(poti_normalized);
  return poti_normalized;
}
