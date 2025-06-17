
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 1_4_ESP32 wifi:
// Activate integrated WiFi of ESP32. 
// Connect to network and monitor connection status.
// 
// hands on:
//    - First connect the ESP32 to the Wifi "servercell" and check the connection in the Serial Monitor
//    - Connect the ESP32 to the EDM Wifi. To do this, change the ssid and password in the program sketch
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////



// Include necessary libraries:
// Wifi:
#include <WiFi.h>


// Defines name and password of the router
const char* ssid = "servercell";
const char* password = "qwer1234";


// setup() starts automatically as soon as the ESP32 is powered.
void setup() {
  // start the Serial Monitor with Baudrate: 115200 bits per second
  Serial.begin(115200);
  
  // start the internet connection with name and password of the router
  WiFi.begin(ssid, password);
  // loops as long as not (!=) connected
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("connecting...");
  }
  // show the ESP32-IP in the serial monitor
  Serial.println(WiFi.localIP());
}


// after setup(), loop() starts automatically and repeats infinitely (until the ESP32 loses power)
void loop() {
  // every 2000 milliseconds / 2 seconds: if connected: "online", otherwise: "offline" and ESP32 restarts. 
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("online");
  } else {
    Serial.println("offline");
    ESP.restart();
  }
  delay(2000); 
}