/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 1_2_ESP32 setup:
// Basic ESP32 hardware setup with GPIO pins. 
// Make LED blink and output potentiometer values via Serial.
// 
// hands on:
//    - Mount the ESP32 on the breadboard and connect the potentiometer to the correct pins (see ESP_poti.png)
//    - Observe how the sketch code shows the potentiometer values in the Serial Monitor (turn the potentiometer)
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////



// Defines the GPIO pin number in the code.
const int LED_PIN = 2;
const int POTI_PIN = 32;


// setup() starts automatically as soon as the ESP32 is powered.
void setup() {
  // start the Serial Monitor with Baudrate: 115200 bits per second
  Serial.begin(115200);
  // Sets the respective GPIO pin mode: Input = receive values, Output = send values.
  pinMode(LED_PIN, OUTPUT);
  pinMode(POTI_PIN, INPUT);
}


// after setup(), loop() starts automatically and repeats infinitely (until the ESP32 loses power)
void loop() {
  // POTI_PIN: show the measured analog potetiometer value in the serial monitor
  Serial.println(analogRead(POTI_PIN));
  
  // LED_PIN: always change the output value to the opposite (!x) of the current output value (LED goes on and off)
  digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  
  // wait 1000 milliseconds
  delay(1000);
}



