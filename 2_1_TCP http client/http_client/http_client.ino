
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 2_1_TCP http client:
// ESP32 as TCP client for web requests. 
// Send HTTP GET requests: read website via TCP protocol.
// 
// hands on:
//    - View the source code of "www.wieistmeineip.de" in the Serial Monitor
//    - Change the URL and look at other source code
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////



// Include necessary libraries:
// Wifi:
#include <WiFi.h>
// TCP http:
#include <HTTPClient.h>


// Defines name and password of the router
const char* ssid = "servercell";
const char* password = "qwer1234";


// Defines TCP http client
HTTPClient http;

// Defines website URL
const char* url = "https://www.wieistmeineip.de/";


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

  // if connected to wifi: start TCP http Client and run fetchWebsite(), otherwise: "offline" and ESP32 restartes. 
  if (WiFi.status() == WL_CONNECTED) {
    http.begin(url);
    fetchWebsite();
  } else {
    Serial.println("offline");
    ESP.restart();
  }
  delay(5000); 
}


// loop() is empty in this case, because we dont loop stuff (but must remain in the code for syntax reasons)
void loop() {}


// Function for the output of website source code
void fetchWebsite() {
  // If the response of the server to the TCP http request is greater than 0 (i.e. has content):
  if (http.GET() > 0) {
    // Converts the response to string, i.e. readable characters, and outputs them in the Serial Monitor
    String payload = http.getString();
    Serial.println(payload);
  } 
}

