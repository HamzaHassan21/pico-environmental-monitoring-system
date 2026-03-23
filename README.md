# IoT Environmental Monitoring System (Pico W + BME280)

A complete IoT prototype built using the Raspberry Pi Pico W and BME280 sensor, demonstrating real-time environmental monitoring, local web-based visualisation, and cloud-based data logging using Google Sheets.

---

## Overview

This project demonstrates a full IoT pipeline:

Sensor data acquisition (Temperature, Pressure, Humidity)
Local processing and validation
Web server for real-time monitoring
Cloud data logging using Google Apps Script
Data analysis across multiple environments

--- 

## Architecture:

BME280 Sensor → Pico W → Wi-Fi → Google Apps Script → Google Sheets

## Key Features
Real-time sensor readings via web interface
Automatic data logging to Google Sheets
Timestamped environmental monitoring
Multi-environment testing and analysis
Error handling for network reliability
Clean modular MicroPython implementation

## System Architecture


![IoT System Architecture](pico-iot-bme280/diagrams/IoT_System_Architecture_Diagram.png)




This diagram shows both:

Local web server operation
Cloud-based data logging pipeline
### 🌐 Web Server Output


![Web_Server_Output](pico-iot-bme280/images/browser_bme_server.png)



The Pico W hosts a local web server that displays live BME280 readings and refreshes automatically every 5 seconds.

### ☁️ Cloud Data Logging

![Google_sheet](pico-iot-bme280/images/google_sheet_bme280_logger.png)


Sensor data is transmitted via HTTP requests and stored in Google Sheets for further analysis.

## 📊 Data Visualisation
### Temperature vs Time (Part A)




Demonstrates stable and consistent data logging over time.

### Temperature vs Location (Part B)




Shows clear variation between environments:

Bedroom (stable)
University (coolest)
Living Room (warmest)
🧪 Testing & Results
Total readings: 182
Environments tested:
Bedroom
University
Living Room

## Key findings:

Sensor detects real environmental differences
Data is consistent and reliable
System performs well across multiple conditions

## Technologies Used
Raspberry Pi Pico W
BME280 Sensor
MicroPython
Google Apps Script
Google Sheets
HTTP (GET requests)
Socket Programming
🔐 Configuration

### Sensitive data has been removed:

```
ssid = ""
password = ""
SCRIPT_URL = ""
TIME_URL = ""
```

Users should insert their own credentials when running the project.

## 🚀 How to Run
Connect BME280 via I2C (GP0 SDA, GP1 SCL)
Upload:
bme280.py
Selected script
Enter Wi-Fi credentials
Run in Thonny
Access via browser or view Google Sheets

### 4️⃣ Access Web Interface

After running:

The Pico will print: Connected on <IP> 

Open browser

Navigate to:

```http://<printed-ip>```

📌 Conclusion

This project demonstrates how low-cost hardware and simple cloud services can be integrated to build a functional IoT system. It highlights key concepts such as real-time monitoring, cloud communication, and data analysis across different environments.

## 📂 Repository Structure
/images/
scripts/
README.md
report.pdf
👤 Author

Hamza Hassan
University of Westminster
IoT Coursework Project
