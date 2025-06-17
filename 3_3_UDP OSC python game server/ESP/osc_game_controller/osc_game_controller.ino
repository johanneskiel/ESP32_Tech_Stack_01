
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 3_3_UDP OSC python game server
// ESP32 as controller via UDP/OSC and Python game server. 
// Fast multiplayer control for cooperative Pong game.
// 
// hands on (group):
//    - Change name and color in the code
//    - Connect your ESP32 to the game server (The game will be visible to everyone on the projector)
//    - Turn the potentiometer and see what happens
//    - Have fun together :D
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////



#include <WiFi.h>
#include <WiFiUdp.h>
#include <OSCMessage.h>


const char* ssid = "servercell";
const char* password = "qwer1234";
const char* ip = "192.168.10.147";  
int port = 12345;
int local_port = 8888; 

const int LED_PIN = 2;
const int POTI_PIN = 32;

WiFiUDP udp;

const char* name = "Mustermensch";
const char* color = "100 100 100";


void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(POTI_PIN, INPUT);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("connecting...");
  }
  Serial.println(WiFi.localIP());
  
  udp.begin(local_port);
  connectToServer();

  xTaskCreate(loopSendOSC, "send OSC", 2048, NULL, 1, NULL);
  xTaskCreate(loopReceiveOSC, "receive OSC", 2048, NULL, 1, NULL);
}


void loop() {}


void loopSendOSC(void *parameter) {
  while(1) {
    OSCMessage msg("/poti"); 
    float poti_value = smooth_poti_value();
    
    msg.add(poti_value);
    
    udp.beginPacket(ip, port);
    msg.send(udp);
    udp.endPacket();
    msg.empty();
    
    delay(25);  
  }
}


void loopReceiveOSC(void *parameter) {
  while(1) {

    OSCMessage msg;
    int size = udp.parsePacket();
    
    if (size > 0) {
      while (size--) {
        msg.fill(udp.read());
      }
      if (!msg.hasError()) {
        msg.dispatch("/led_blink", led_blink_handler);
      }
    }

  }
}


void connectToServer() {
  OSCMessage msg("/connect");
  msg.add(name);
  msg.add(color);
  
  udp.beginPacket(ip, port);
  msg.send(udp);
  udp.endPacket();
  msg.empty();
}


void led_blink_handler(OSCMessage &msg) {
  digitalWrite(LED_PIN, HIGH);
  delay(200);  
  digitalWrite(LED_PIN, LOW);
}


float smooth_poti_value(){
  int poti_value = 0;
  for (int i = 0; i < 1000; i++) {
    poti_value += analogRead(POTI_PIN);
  }
  poti_value = poti_value / 1000;

  float poti_normalized = poti_value / 4095.0;  
  poti_normalized = round(poti_normalized * 1000) / 1000.0; 
    
  Serial.println(poti_normalized);
  return poti_normalized;
}