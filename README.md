# Tech-Stack ESP32 
## About ESP32

The ESP32 is a cost-effective microcontroller with integrated WiFi and Bluetooth, developed by Espressif Systems. It stands out for its small size, low power consumption, and dual-core architecture that enables parallel processing.

What makes it particularly attractive is the open-source ecosystem: The ESP-IDF (Espressif IoT Development Framework) is freely available, and it can be programmed with Arduino IDE, PlatformIO, or MicroPython. These open development environments and the large community provide many free libraries.

For Digital Art, the ESP32 is ideal because it can control sensors, lights and displays, process audio, and through its wireless capabilities enables interactive, networked installations. Its 30+ GPIO pins provide sufficient connections for complex projects, while the open-source tools allow rapid prototyping.

Besides the ESP32, there are other variants like the smaller ESP8266 (WiFi only) or the more powerful ESP32-S3 with improved AI support. These chips are mounted on various development boards, such as the NodeMCU, Wemos D1 Mini, or the official ESP32 DevKit, each offering different form factors and additional features.

In this TechStack, we use the ESP32 DevKit V1 with Arduino IDE for microcontroller programming, Python for server applications, as well as UDP/OSC protocols for low-latency real-time communication and TCP/HTTP for web-based interfaces.


## ESP32 in Artistic Practice
### Empathy Swarm, 2019
by Katrin Hochschuh & Adam Donovan, ZKM Karlsruhe permanent collection
- Video / Documentation: https://hochschuh-donovan.com/portfolio/empathy-swarm

### Viral Infection, 2025
by Johannes Kiel, Diploma 2025, Emergent Digital Media class
- Documentation: https://generativemedia.net/event/diploma-johannes-kiel
- Video: https://vimeo.com/1066045872


## Tech-Stack learning objective

| Experience | Learning goal |
|------|-------------|
| **Beginner** | Overcoming challenges and hurdles: Get to know ESP32 features and program with the Ardunio IDE|
| **Advanced** | Consolidate knowledge base: Recognizing Arduino limitations and working with 32-bit, multithreading and network communication |


## Table of contents

### 1.[  Setup: ESP Arduino IDE & Python](#1-setup-esp-arduino-ide--python)
Installation guide for Arduino IDE, USB drivers, ESP32 boards and Python libraries on Windows, Mac and Linux.

### 2.[  Data Transmission Standards](#2-data-transmission-standards)
Overview of network layers, protocols and the differences between TCP and UDP for ESP32 communication.

### 3.[  ESP32 Hardware and Software](#3-esp32-hardware-and-software)
Hardware specifications of the ESP32 DevKit V1 and practical code examples from basic GPIO functions to network communication.

### 4.[  Terminology Guide](#4-terminology-guide)
Glossary with important terms related to ESP32 hardware, development, data transmission and network technologies.



---


# 1. Setup: ESP Arduino IDE & Python  

All Tech-Stack participants should carry out this step in advance. No problem if something doesn't work out: Feel free to contact me. Setup time: 10 - 15 minutes.

## Windows

### Step 1: Download Arduino IDE
1. Go to: **www.arduino.cc/en/software**
2. Download **"Windows Win 10 and newer, 64 bits"**
3. Install the downloaded file

### Step 2: Install USB Drivers

#### CP2102/CP2104 Driver:
1. Download: **https://www.silabs.com/documents/public/software/CP210x_Universal_Windows_Driver.zip**
2. Extract and **right-click on silabser.inf** → **"Install"**

#### CH340/CH341 Driver:
1. Download: **https://www.wch.cn/download/file?id=65**
2. Download **CH341SER.EXE** and install (Right-click → Run as Administrator)

### Step 3: Add ESP Support
1. Open Arduino IDE
2. **"File"** → **"Preferences"** → **"Settings"**
3. In **"Additional Boards Manager URLs"** paste:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```

### Step 4: Install ESP Boards
1. **"Tools"** → **"Board"** → **"Boards Manager..."**
2. Search for **"ESP32"**
3. Install **"ESP32 by Espressif Systems"**

### Step 5: Libraries for ESP in Arduino IDE
- **OSCMessage.h** - OSC (Open Sound Control) protocol
   - **"Tools"** → **"Manage Libraries..."**
   - Search for **"OSC message"**
   - Install **"OSC by Adrian Freed"**


### Step 6: Python and Libraries

(Recommended: Advanced participants should use an environment manager)

1. Download: **https://www.python.org/downloads/windows/**
2. **Important**: Make sure to check "Add Python to PATH" if offered during installation
3. Install the .exe file and follow the installer instructions. (**"Add Python to PATH"** see 2.)



### Step 7: Required Python Libraries  

Open Command Prompt (cmd) and install:
- **pythonosc** - OSC communication with ESP32
```bash
pip install python-osc
```
- **pygame** - Game development and graphics
```bash
pip install pygame
```
---




## Mac

### **IMPORTANT: Please bring MAC standard USB adapter**

### Step 1: Download Arduino IDE
1. Go to: **www.arduino.cc/en/software**
2. Download **"macOS"**
3. Install in Applications folder

### Step 2: Install USB Driver

#### CH340/CH341 Driver:

1. Download: **https://www.wch.cn/download/file?id=178**
2. Open **CH34xVCPDriver.pkg** from **CH34xVCPDriver.dmg**

### Step 3: Add ESP Support
1. Open Arduino IDE
2. **"Arduino IDE"** → **"Preferences"** → **"Settings"**
3. In **"Additional boards manager URLs"** paste:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```

### Step 4: Install ESP Boards
1. **"Tools"** → **"Board"** → **"Boards Manager..."**
2. Search for **"ESP32"**
3. Install **"ESP32 by Espressif Systems"**


### Step 5: Libraries for ESP in Arduino IDE
- **OSCMessage.h** - OSC (Open Sound Control) protocol
   - **"Tools"** → **"Manage Libraries..."**
   - Search for **"OSC message"**
   - Install **"OSC by Adrian Freed"**



### Step 6: Python and Libraries

(Recommended: Advanced participants should use an environment manager)

1. Open Terminal and type in:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
```
echo >> /Users/username/.zprofile
```
```
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/username/.zprofile
```
- only Apple Silicon Macs (M1/M2/M3): type in:
```
eval "$(/opt/homebrew/bin/brew shellenv)"
```
- only Intel Macs: type in:
```
eval "$(/usr/local/bin/brew shellenv)"
```
2. reopen Terminal and type in:
```
brew install python
```

### Step 7: Required Python Libraries  
Open Terminal and install:
- **pythonosc** - OSC communication with ESP32
```bash
pip3 install python-osc
```
- **pygame** - Game development and graphics
```bash
pip3 install pygame
```

---

## Linux (Ubuntu/Debian)

### Step 1: Download Arduino IDE
1. Go to: **www.arduino.cc/en/software**
2. Download **"Linux 64 bits"** AppImage
3. Run the AppImage file

### Step 2: Install USB Drivers

#### CP2102/CP2104 Driver:
For newer Linux distributions, drivers are already included in the kernel. If you need to install them manually:
1. Download: **https://www.silabs.com/documents/login/software/Linux_3.x.x_4.x.x_VCP_Driver_Source.zip**
2. Extract and follow README instructions
3. Alternatively: check `lsmod | grep cp210x` in terminal
4. If not loaded: `sudo modprobe cp210x`

#### CH340/CH341 Driver:
Drivers are normally already included in the kernel:
1. For manual installation: **https://www.wch-ic.com/downloads/CH341SER_LINUX_ZIP.html**
2. Check: `lsmod | grep ch341` in terminal
3. If not loaded: `sudo modprobe ch341`

#### Set up user permissions for USB ports:
1. Enter in **Terminal**:
   ```bash
   sudo usermod -a -G dialout $USER
   ```
2. **Restart system** (important!)
3. After restart, you can access USB ports without sudo

### Step 3: Add ESP Support
1. Open Arduino IDE
2. **"File"** → **"Preferences"** → **"Settings"**
3. In **"Additional boards manager URLs"** paste:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```

### Step 4: Install ESP Boards
1. **"Tools"** → **"Board"** → **"Boards Manager..."**
2. Search for **"ESP32"**
3. Install **"ESP32 by Espressif Systems"**



### Step 5: Libraries for ESP in Arduino IDE
- **OSCMessage.h** - OSC (Open Sound Control) protocol
   - **"Tools"** → **"Manage Libraries..."**
   - Search for **"OSC message"**
   - Install **"OSC by Adrian Freed"**



### Step 6: Python and Libraries

Python is usually pre-installed on most Linux distributions. 

(Recommended: Advanced participants should use an environment manager)

### Step 7: Required Python Libraries  
Open Terminal and install:
- **pythonosc** - OSC communication with ESP32
```bash
pip3 install python-osc
```
- **pygame** - Game development and graphics
```bash
pip3 install pygame
```

---
# 2. Data Transmission Standards

## Network Layers and Protocols

The internet communication follows a layered model where each layer has specific responsibilities. Data travels through these layers from application to physical transmission and back. In this ESP32 Tech-Stack, we work specifically with HTTP, OSC Application layer protocols and TCP, UDP Transport layer protocols while the Internet and Network access layers handle network routing / physical connections. 

| **Layer** | **Example protocols** |
| ----------------------------------------- | -------------------------------- |
| **Network access layer** | Ethernet, WLAN (Wi-Fi) |
| **Internet layer**| IP (IPv4, IPv6) |
| **Transport layer**  | TCP, UDP |
| **Application layer**  | HTTP, OSC, FTP, SMTP, DNS, DHCP|

## TCP | UDP

TCP (Transmission Control Protocol) and UDP (User Datagram Protocol) are the two main transport protocols that determine how data is transmitted over networks. The choice between them depends on your application's requirements: TCP prioritizes reliability and order, while UDP prioritizes speed and efficiency

| | **TCP** | **UDP** |
|-------------|-----|-----|
| **Connection** | Connection-oriented (handshake before data transmission) | Connectionless (direct transmission without handshake) |
| **Reliability** | Reliable (confirms receipt) | Unreliable (no receipt confirmation) |
| **Order** | Correct order (numbers packets) | No order (packets can overtake) |
| **Speed** | Slower (greater overhead / administrative data) | Faster (minimal overhead / administrative data) |
| **Usage** | Websites, email, file transfer | Live audio, gaming, video streaming |
| **Protocols** | HTTP, HTTPS, FTP, SMTP | OSC, DNS, RTP, DHCP|
---


# 3. ESP32 Hardware and Software


## 3. ESP32 DevKit V1

The ESP32 DevKit V1 is a widely used development board that combines the ESP32 microcontroller with all the necessary components for development. It has 30 GPIO pins that support various functions: digital inputs/outputs, analog inputs, PWM outputs, SPI and I2C interfaces. The board is powered and programmed via micro USB.

![ESP32 DevKit V1](https://m.media-amazon.com/images/I/518GSZDPb6L._AC_.jpg)
![ESP32 DevKit V1 Poti](https://raw.githubusercontent.com/johanneskiel/ESP32_Tech_Stack_01/refs/heads/main/ESP32_poti.png)

---






## Buttons on the ESP32 DevKit V1

The ESP32 DevKit V1 has two important buttons:

- **EN Button (Reset)** - Restarts the ESP32 and runs the uploaded sketch from the beginning
- **BOOT Button (Flash/GPIO0)** - Used for uploading sketches when automatic upload fails. Also programmable as regular input button in your code

**Location:** Both buttons are located on the ESP32 development board next to the USB connector.

---

## Uploading Sketches to ESP32 DevKit

**Upload process:**

1. **Connect ESP32 via USB** - Use micro-USB cable to connect to computer
2. **Select Board** - In Arduino IDE: "Tools" → "Board" → "ESP32 Dev Module" 
3. **Select Port** - "Tools" → "Port" → Choose ESP32 USB port:
   - **Windows:** COM3, COM4, COM5...
   - **Mac:** /dev/cu.usbserial-... or /dev/cu.SLAB_USBtoUART
   - **Linux:** /dev/ttyUSB0, /dev/ttyUSB1...
4. **Click Upload** - Arrow symbol in Arduino IDE or Ctrl+U (Cmd+U on Mac)
5. **Wait** - sketch compiles: "Connecting..." appears: Press and hold the **BOOT button** for about **2 seconds** during the "Connecting..." phase, then release.

---

## Open Serial Monitor for the ESP32 DevKit

**Accessing Serial Monitor:**

1. **Upload sketch first** - Make sure your code includes `Serial.begin(115200);` in setup()
2. **Open Serial Monitor** - Click magnifying glass icon in Arduino IDE or "Tools" → "Serial Monitor"
3. **Set baud rate** - Select **115200** in dropdown (bottom right of Serial Monitor window)
4. **View output** - Real-time text output from ESP32 appears here

**Useful for:** Debugging code, monitoring sensor values, checking WiFi connection status, and viewing error messages.

**Tip:** If no output appears, press the **EN (Reset) button** on ESP32 to restart and trigger Serial output.




---



## ESP32 Code Examples

The ESP32 code examples provided systematically guide you through the most important functions of the microcontroller and show practical applications for digital art projects. They start with basic concepts such as the 32-bit architecture and hardware setup, moving through multithreading and WiFi functionality to more complex network protocols. Each example builds on the previous one, covering both technical basics and practical applications.


### 1_1_ESP32 bits/32_bit
Demonstration of ESP32 32-bit architecture. Shows how 8-bit (0-255) and 32-bit (0-4,294,967,295) variables differ in their value ranges and memory usage.
#### hands on: 
- Upload a program sketch to the ESP32 microcontroller for the first time  
- Open the Serial Monitor  
- Observe how the 8-bit variable jumps back to 0 after reaching 255  


### 1_2_ESP32 setup/setup_test
Basic ESP32 hardware setup with GPIO pins. Make LED blink and output potentiometer values via Serial.
#### hands on: 
- Mount the ESP32 on the breadboard and connect the potentiometer to the correct pins (see ESP_poti.png) 
- Observe how the sketch code shows the potentiometer values in the Serial Monitor (turn the potentiometer)  


### 1_3_ESP32 multithreading/multithreading
Use ESP32 dual-core for parallel processing. Execute two separate tasks for LED control and sensor reading simultaneously.
#### hands on: 
- Change the delays and observe that this has no effect on the other task  


### 1_4_ESP32 wifi/wifi
Activate integrated WiFi of ESP32. Connect to network and monitor connection status.
#### hands on: 
- First connect the ESP32 to the Wifi "servercell" and check the connection in the Serial Monitor  
- Connect the ESP32 to the EDM Wifi. To do this, change the ssid and password in the program sketch  


### 2_1_TCP http client/http_client
ESP32 as TCP client for web requests. Send HTTP GET requests: read website via TCP protocol.
#### hands on: 
- View the source code of "www.wieistmeineip.de" in the Serial Monitor  
- Change the URL and look at other source code  


### 2_2_TCP http server/http_server
ESP32 as TCP web server with interactive browser interface: displays live potentiometer values and enables LED control via TCP protocol.
#### hands on: 
- Connect your laptop to the Wifi "servercell" (see code for the password)  
- Read the IP of your ESP32 from the Serial Monitor and copy it  
- Open your browser and paste the ESP32 IP into the URL bar  
- Play with the ESP32 browser interface  


### 3_1_UDP OSC touchdesigner
ESP32 communication via UDP/OSC (Open Sound Control). Fast real-time communication for TouchDesigner program.
#### hands on (OPTIONAL! We will all do this together on one laptop):  
- If TouchDesigner is installed on your laptop: open the TouchDesigner project  
- paste you laptop IP in the ESP32 code
- change the port in the OSCin CHOP to the touchdesigner_port in the ESP32 code  
- Turn the potentiometer and observe how the values in the OSCin CHOP change in TouchDesigner  


### 3_2_UDP OSC python server 
ESP32 communication with Python server via UDP/OSC. Fast data transmission.
#### hands on (group): 
- Change the name and message in the code  
- Connect your ESP32 to the server (the server terminal will be visible to everyone on the projector)  
- Turn the potentiometer and see what happens  
#### hands on, alone (OPTIONAL! We will all do this together on one laptop): 
- IP setup as described in 3_1_UDP  
- Open the terminal on your laptop  
- Navigate to the Python project folder: enter "cd <your path>/3_1_UDP OSC python server/python"  
- (Advanced: enter your python environment)  
- Start the server: enter:  
   - Windows: "python server.py"  
   - Mac / Linux: "python3 server.py"  
- Connect your ESP32 to the server  
- Observe the server prints in the terminal  


### 3_3_UDP OSC python game server
ESP32 as controller via UDP/OSC and Python game server. Fast multiplayer control for cooperative Pong game.
#### hands on (group):
- Change name and color in the code  
- Connect your ESP32 to the game server (The game will be visible to everyone on the projector)  
- Turn the potentiometer and see what happens  
- Have fun together :D  
#### hands on, alone (OPTIONAL! We will all do this together on one laptop): 
- IP setup as described in 3_1_UDP  
- Open the terminal on your laptop  
- Navigate to the Python project folder: enter "cd <your path>/3_3_UDP OSC python game server/python"  
- (Advanced: enter your python environment)  
- Start the game server: enter:  
   - Windows: "python server.py"  
   - Mac / Linux: "python3 server.py"  
- Connect your ESP32 to the game server  
- not quite as much fun alone... ^^



---


# 4. Terminology Guide

## ESP32 Hardware & Development

| Term | Explanation |
|------|-------------|
| **IDE** | Integrated Development Environment - Arduino IDE used for writing and uploading code to ESP32 |
| **USB Drivers** | Software (CP2102/CP2104, CH340/CH341) that enables computer communication with ESP32 via USB |
| **Serial Monitor** | Arduino IDE tool that displays real-time text output from ESP32 for debugging and monitoring sensor data |
| **Baudrate** | Communication speed (bits per second) between ESP32 and computer - common rates: 9600, 115200 bps |
| **Library** | Pre-written code packages (like OSCMessage.h) that add functionality to ESP32 projects |
| **Breadboard** | Solderless prototyping board with connected holes for temporarily connecting ESP32 pins to components |
| **Potentiometer** | Variable resistor component that outputs analog voltage values when turned, commonly used with ESP32 analog pins |
| **Pin** | Individual metal contact point on ESP32 that connects to breadboard or components for electrical connection |
| **GND** | Ground - Reference voltage point that acts as the negative pole/minuspol in ESP32 circuits, completes electrical circuits |
| **VCC** | Voltage Common Collector - General term for positive power supply voltage to components, typically from USB power |
| **5V** | Five volt power supply pin on ESP32 development boards, typically from USB power |
| **3.3V** | Three point three volt power supply pin - ESP32's native operating voltage for logic and sensors |
| **Digital Pins** | ESP32 pins that read/write binary states (HIGH/LOW, 1/0) for LEDs, buttons, switches |
| **Analog Pins** | ESP32 pins that read continuous voltage values (0-3.3V) from sensors like potentiometers |
| **GPIO Pins** | General Purpose Input/Output - ESP32's 30+ configurable (digital / analog) pins for connecting sensors, LEDs, and other components |

## Data Exchange & Networking

| Term | Explanation |
|------|-------------|
| **IP** | Internet Protocol address - Unique numerical identifier (like 192.168.1.100) assigned to ESP32 on network for communication |
| **PORT** | Numerical identifier (0-65535) that specifies which service/application on a device to communicate with (e.g., port 80 for HTTP) |
| **Router** | Network device that connects ESP32 to internet and manages local network traffic, typically provides DHCP and WiFi access |
| **DHCP** | Dynamic Host Configuration Protocol - Automatic IP address assignment service provided by routers to ESP32 and other network devices |
| **DNS** | Domain Name System - Service that translates human-readable domain names (www.wieistmeineip.de) into IP addresses for ESP32 internet requests |
| **Client** | Device or program that requests services/data from servers - ESP32 can act as client making HTTP requests or OSC connections |
| **Server** | Device or program that provides services/data to other devices - ESP32 can act as web server hosting pages or API endpoints |
| **Protocols** | Communication standards (TCP, UDP) that define how devices exchange data |
| **TCP** | Transmission Control Protocol - Reliable, connection-oriented protocol used for web servers and HTTP communication |
| **UDP** | User Datagram Protocol - Fast, connectionless protocol used for real-time communication like OSC messaging with ESP32 |
| **HTTP / HTTPS** | HyperText Transfer Protocol (Secure) - Web communication standard used by ESP32 web servers and clients |
| **OSC** | Open Sound Control - Protocol for real-time communication between ESP32 and applications like TouchDesigner or Python |
| **Handshake** | Connection establishment process in TCP before data transmission (not used in UDP) |
| **Datagram** | Individual data packet sent via UDP without connection establishment or delivery confirmation |
| **Overhead** | Additional administrative data required by protocols - TCP has more overhead than UDP |







