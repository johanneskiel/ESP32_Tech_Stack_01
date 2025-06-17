
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 2_2_TCP http server:
// ESP32 as TCP web server with interactive browser interface: 
// displays live potentiometer values and enables LED control via TCP protocol.
// 
// hands on:
//    - Connect your laptop to the Wifi "servercell" (see code for the password)
//    - Read the IP of your ESP32 from the Serial Monitor and copy it
//    - Open your browser and paste the ESP32 IP into the URL bar
//    - Play with the ESP32 browser interface
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////



// Include necessary libraries:
// Wifi:
#include <WiFi.h>
// TCP http web server:
#include <WebServer.h>


// Defines the GPIO pin number in the code.
const int LED_PIN = 2;
const int POTI_PIN = 32;

// Defines name and password of the router
const char* ssid = "servercell";
const char* password = "qwer1234";

// Defines TCP http web server (standard port: 80)
WebServer server(80);

// Defines the HTML and Java Script code for the web interface 
// HTML defines the appearance of the website
// Java Script is executed in the browser and regularly updates the displayed potentiometer value
const char index_html[] PROGMEM = R"( 
  <html>
    <body>
    
      <h1>ESP32</h1>
      <p>Poti Wert: <span id="poti">0</span></p>
      <button onclick="location.href='/toggle'">LED Toggle</button>
      
      <script>
        setInterval(()=>{
          fetch('/poti').then(r=>r.text()).then(d=>document.getElementById('poti').innerText=d)
        },100)
      </script>

    </body>
  </html>
)";


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

    // Defines the possible request addresses from the server and which function they trigger
    server.on("/", handleRoot);
    server.on("/toggle", handleToggle);
    server.on("/poti", handlePoti);
    // start web server
    server.begin();

  } else {
    Serial.println("offline");
    ESP.restart();
  }
}


// after setup(), loop() starts automatically and repeats infinitely (until the ESP32 loses power)
void loop() {
  // Processes incoming HTTP requests from clients/browsers
  server.handleClient();
}


// server receives “/” request from client / browser:
void handleRoot() {
  // sends 200 (okay) and the HTML code to the client / browser:
  server.send(200, "text/html", index_html);
}


// server receives “/toggle” request from client / browser:
void handleToggle() {
  // toggle the LED 
  digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  // sends 303 (forwarding) to “/” and avoids a change of the URL (ESP32-IP remains and not ESP32-IP/toggle as usual when clicking on links)
  server.sendHeader("Location", "/");
  server.send(303); 
}


// server receives “/poti request from client / browser:
void handlePoti() {
  // sends 200 (okay) and the measured potentiometer value to the client / browser
  server.send(200, "text/plain", String(analogRead(POTI_PIN)));
}