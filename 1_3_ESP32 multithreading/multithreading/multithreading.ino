
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 1_3_ESP32 multithreading:
// Use ESP32 dual-core for parallel processing. 
// Execute two separate tasks for LED control and sensor reading simultaneously.
// 
// hands on:
//    - Change the delays and observe that this has no effect on the other task
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////



// Include necessary libraries:
// Multithreading:
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"


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
  
  // Functions are distributed to the cores so that they can be executed simultaneously: 
  // loopLEDTask on ESP32 Core 0
  // loopPotiTask on ESP32 Core 1
  xTaskCreatePinnedToCore(loopLEDTask, "LED", 2048, NULL, 1, NULL, 0); // 0 = core 0
  xTaskCreatePinnedToCore(loopPotiTask, "Poti", 2048, NULL, 1, NULL, 1); // 1 = core 1
}


// loop() is empty in this case (but must remain in the code for syntax reasons)
// loop() is 'replaced' in this case by two loops on one ESP32 core each
void loop() {}


// loop to core 0 (for LED blinking)
void loopLEDTask(void *) {

  // loop as long as true is true: so infinitely long (even in times of fake news, lol). like the standard loop()
  while(true) {
    
    // LED_PIN: always change the output value to the opposite (!x) of the current output value (LED goes on and off)
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));

    // wait 1000 milliseconds
    delay(1000);
  }
}


// loop on core 1 (for potentiometer)
void loopPotiTask(void *) { 

  // loop as long as true is true: so infinitely long (even in times of fake news, lol). like the standard loop()
  while(true) {

    // POTI_PIN: show the measured analog potetiometer value in the serial monitor
    Serial.println(analogRead(POTI_PIN));

    // wait 10 milliseconds
    delay(10);
  }
}



