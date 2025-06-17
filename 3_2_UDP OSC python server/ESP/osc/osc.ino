
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 3_1_UDP OSC touchdesigner:
// ESP32 communication with Python server via UDP/OSC. Fast data transmission.
// 
// hands on (group):
//    - Change the name and message in the code
//    - Connect your ESP32 to the server (the server terminal will be visible to everyone on the projector)
//    - Turn the potentiometer and see what happens
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

// Defines Server IP and Port
const char* ip = "192.168.10.147";  
int port = 12345;

// Defines local port
int local_port = 8888; 

// Defines UDP object for communication
WiFiUDP udp;

const char* name = "Mustermensch";
const char* message = "Hallo Server";


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

  // Functions are distributed to the cores so that they can be executed simultaneously: 
  // loopSendOSC on ESP32 Core 0
  // loopReceiveOSC on ESP32 Core 1
  xTaskCreatePinnedToCore(loopSendOSC, "LED", 2048, NULL, 1, NULL, 0); // 0 = core 0
  xTaskCreatePinnedToCore(loopReceiveOSC, "Poti", 2048, NULL, 1, NULL, 1); // 1 = core 1
}


// loop() is empty in this case (but must remain in the code for syntax reasons)
// loop() is 'replaced' in this case by two loops on one ESP32 core each
void loop() {}


// loop to core 0 (for sending Data)
void loopSendOSC(void *) {
  while(true) {
    
    // creates a message with the address “/hallo”
    OSCMessage msg("/hallo");

    // if poti_value is not (!=)0
    float poti_value = smooth_poti_value();
    if (poti_value != 0) {

      // adds the measured potentiometer value to the message
      msg.add(message);
      msg.add(name);
      msg.add(poti_value);
      
      // sends the message and then empties it
      udp.beginPacket(ip, port);
      msg.send(udp);
      udp.endPacket();
      msg.empty();
    }

    // Waits depending on the potentiometer value: minimum 2000 - 500 milliseconds
    // The loopSendOSC function therefore repeats faster or slower
    delay(map(poti_value * 1000, 0, 1000, 2000, 500));  
  }
}


// loop to core 1 (for sending Data)
void loopReceiveOSC(void *) {
  while(true) {


    // Check whether UDP data is available (packet size)
    OSCMessage msg;
    int size = udp.parsePacket();
    
    // When data has been received
    if (size > 0) {
      // Reads the raw UDP data byte by byte
      while (size--) {
        msg.fill(udp.read());
      }

      // if the message is directed to the address “/led_blink”: run led_blink_handler
      msg.dispatch("/led_blink", led_blink_handler);
    }

  }
}


// Function causes LED to flash for 200 milliseconds
void led_blink_handler(OSCMessage &msg) {
  digitalWrite(LED_PIN, HIGH);
  delay(200);  
  digitalWrite(LED_PIN, LOW);
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
