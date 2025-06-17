
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 1_1_ESP32 bits:
// Demonstration of ESP32 32-bit architecture. 
// Shows how 8-bit (0-255) and 32-bit (0-4,294,967,295) variables differ in their value ranges and memory usage.
// 
// hands on:
//    - Upload a program sketch to the ESP32 microcontroller for the first time
//    - Open the Serial Monitor
//    - Observe how the 8-bit variable jumps back to 0 after reaching 255
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////



// Two variables are defined that use different amounts of memory: 8 and 32 bits.
uint8_t bit8 = 0;
uint32_t bit32 = 0;

// Two variables are defined to show how large the respective memory sizes are: 8 vs 32 bits. (Binary system: 2 to the power of bits)
uint32_t bit8max = pow(2, 8);
uint64_t bit32max = pow(2, 32);


// setup() starts automatically as soon as the ESP32 is powered.
void setup() {
  // start the Serial Monitor with Baudrate: 115200 bits per second
  Serial.begin(115200);
}


// after setup(), loop() starts automatically and repeats infinitely (until the ESP32 loses power)
void loop() {
  
  // show the 8-bit variables in the Serial Monitor
  Serial.print(bit8);
  Serial.print(" (");
  Serial.print(bit8max);
  Serial.print(")  ");

  // show the 32-bit variables in the Serial Monitor
  Serial.print(bit32);
  Serial.print(" (");
  Serial.print(bit32max);
  Serial.println(")");
  
  // Variable = Variable + 1
  bit8++;
  bit32++;
  
  // wait 25 milliseconds
  delay(25);
}
